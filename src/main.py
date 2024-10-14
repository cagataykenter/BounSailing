# Importing necessary modules
import pandas as pd  # Use standard alias for pandas

# Custom modules for various processing steps
from identification import human_identification
from elimination import person_background_check
from group_manager import initial_grouping, remove_subset_groups

# Constants
DATA_FILE_PATH = r"D:\Cagatay\Career\Ongoing\BounSailing\BounSailing\data\Bounsailing Güz'24 _ 1_ ve 2_ Eğitim Başvuru Formu (Yanıtlar) - Form Yanıtları 1.csv"


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data from the CSV file.

    Raises:
        FileNotFoundError: If the file cannot be found.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file has invalid format.
    """
    try:
        return pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error loading data: {e}")
        raise


def process_and_group_people(data: pd.DataFrame):
    """
    Execute the process pipeline: identification, background check, grouping, and cleaning.

    Args:
        data (pd.DataFrame): Raw data to be processed.

    Returns:
        list: List of final grouped people after processing and cleaning.
    """
    # Process data
    people = human_identification(data)
    people = person_background_check(people)

    # Grouping
    groups = initial_grouping(people)
    final_groups = remove_subset_groups(groups)

    return final_groups


def display_groups(groups: list) -> None:
    """
    Display group details.

    Args:
        groups (list): List of final groups to be displayed.
    """
    for group in groups:
        print(group)


if __name__ == "__main__":
    # Load data and process it
    data = load_data(DATA_FILE_PATH)

    # Process and group people
    final_groups = process_and_group_people(data)

    # Display the results
    display_groups(final_groups)
