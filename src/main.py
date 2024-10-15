# Importing necessary modules
from idlelib.search import find_again
from typing import List

import pandas as pd  # Use standard alias for pandas
from pandas.core.interchange.dataframe_protocol import DataFrame

# Custom modules for various processing steps
from identification import human_identification, course_slots_automate
from elimination import person_background_check
from group_manager import initial_grouping, remove_subset_groups, merge_groups_by_members
from placement import place_groups, optimize_placements
from schemas import slots

# Constants
DATA_FILE_PATH = r"/Users/cagataykenter/Desktop/cagataykenter/Career/Personal/BounSailing/data/Bounsailing Güz'24 _ 1_ ve 2_ Eğitim Başvuru Formu (Yanıtlar) - Form Yanıtları 1.csv"


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


def execution(data: pd.DataFrame):
    """
    Execute the process pipeline: identification, background check, grouping, and cleaning.

    Args:
        data (pd.DataFrame): Raw data to be processed.

    Returns:
        list: List of final grouped people after processing and cleaning.
    """
    # Process data
    people = human_identification(data)
    chosen_course_slots = course_slots_automate(people)
    people = person_background_check(people)

    # Grouping
    groups = initial_grouping(people)
    final_groups = remove_subset_groups(groups)
    final_groups = merge_groups_by_members(final_groups)

    # Placement
    # slot_capacity = course_slots_creating(slots.values())
    df_first_round, df_second_round = place_groups(final_groups,  slots={11: 0, 12: 0, 13: 0, 21: 0, 22: 0, 23: 0, 31: 0, 32: 0, 33: 0, 41: 0, 42: 0, 43: 0, 51: 0, 52: 0, 53: 0, 61: 0, 62: 0, 63: 0, 71: 0, 72: 0, 73: 0} , slot_capacity={11: 0, 12: 11, 13: 12, 21: 0, 22: 0, 23: 0, 31: 0, 32: 11, 33: 12, 41: 0, 42: 13, 43: 12, 51: 11, 52: 16, 53: 17, 61: 20, 62: 20, 63: 20, 71: 20, 72: 20, 73: 20})
    best_placement = optimize_placements(final_groups, slots={11: 0, 12: 0, 13: 0, 21: 0, 22: 0, 23: 0, 31: 0, 32: 0, 33: 0, 41: 0, 42: 0, 43: 0, 51: 0, 52: 0, 53: 0, 61: 0, 62: 0, 63: 0, 71: 0, 72: 0, 73: 0} , slot_capacity={11: 0, 12: 11, 13: 12, 21: 0, 22: 0, 23: 0, 31: 0, 32: 11, 33: 12, 41: 0, 42: 13, 43: 12, 51: 11, 52: 16, 53: 17, 61: 20, 62: 20, 63: 20, 71: 20, 72: 20, 73: 20})

    return final_groups, best_placement


def display_result(placement: DataFrame, final_groups: List) -> None:
    """
    Display the placement output.

    Args:
        groups (list): Final result to be displayed.
    """

    data = {}

    for index, row in placement.iterrows():
        if row['slot'] in data.keys():
            data[row['slot']].append(row['group'])
        else:
            data[row['slot']] = [row['group']]

    # Find the maximum length of the slot lists
    max_len = max(len(groups) for groups in data.values())

    # Normalize the length of each slot's group list by padding with empty lists
    for slot in data:
        while len(data[slot]) < max_len:
            data[slot].append('')

    df = pd.DataFrame(data)
    print(df)

    for group in final_groups:
        print(group)


if __name__ == "__main__":
    # Load data and process it
    data = load_data(DATA_FILE_PATH)

    # Process and group people
    final_groups, best_placement = execution(data)

    # Display the results
    display_result(best_placement, final_groups)
