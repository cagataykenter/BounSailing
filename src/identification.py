from schemas import Human, slots
import pandas as pd
from typing import Dict
from datetime import datetime


def parse_date(date_str: str) -> datetime:
    """
    Parses a date string into a datetime object.

    Args:
        date_str (str): Date string to be parsed.

    Returns:
        datetime: Parsed datetime object or None if invalid.
    """
    try:
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    except (ValueError, TypeError):
        print(f"Invalid date format or value: {date_str}")
        return None  # Return None if parsing fails


def human_identification(data: pd.DataFrame) -> Dict[int, Human]:
    """
    Identifies and processes human entries from the given data.

    Args:
        data (pd.DataFrame): DataFrame containing information about people.

    Returns:
        Dict[int, Human]: Dictionary where keys are student numbers and values are Human objects.
    """
    people = {}

    for idx, row in data.iterrows():
        person = Human()

        # Basic details
        person.STD_NUMBER = row['Öğrenci Numarası']
        person.FULLNAME = row['Ad Soyad']
        person.PHONE_NUMBER = row['Telefon Numarası']
        person.isMember = True  # TODO: Dynamically check this in the future.
        person.COURSE_LEVEL = row['Başvurduğunuz Eğitim']
        person.APPLY_DATE = parse_date(row['Zaman damgası'])

        # Collecting friends' student numbers into a list, if they are valid (not NaN)
        friend_columns = [
            '1. Arkadaşınızın Öğrenci Numarası',
            '2. Arkadaşınızın Öğrenci Numarası',
            '3. Arkadaşınızın Öğrenci Numarası',
            '4. Arkadaşınızın Öğrenci Numarası'
        ]

        person.FRIENDS = [
            int(row[friend_col]) for friend_col in friend_columns
            if pd.notna(row[friend_col])  # Only add valid, non-NaN student numbers
        ]

        # Process course slots and map them to slot numbers using the slots dictionary
        course_slots_raw = row['Eğitime Katılabileceğiniz Slotlar']
        person.COURSE_SLOTS = [
            slots[slot.strip()] for slot in course_slots_raw.split(',')
            if slot.strip() in slots  # Only map valid slot names
        ]

        person.isPlaced = False  # Initialize with False
        person.LAST_COMPLETED_COURSE = '1* Temel Yelken Eğitimi'  # TODO: Check this info from the database in the future

        # Store the person in the people dictionary using the student number as key
        people[person.STD_NUMBER] = person

    return people
