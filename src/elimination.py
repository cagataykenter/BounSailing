def person_background_check(people: dict) -> dict:
    """
    Filters out people from the dictionary based on membership status and course-related criteria.

    Args:
        people (dict): A dictionary where the key is the person's ID, and the value is their details.

    Returns:
        dict: A dictionary containing only the people who meet the criteria.
    """
    filtered_people = {}

    for person_id, person_data in people.items():
        # Check if the person is a member
        if not getattr(person_data, 'isMember', False):
            continue

        # Check for specific course level and ensure LAST_COMPLETED_COURSE is valid
        if person_data.COURSE_LEVEL == '2* İleri Yelken Eğitimi':
            if not getattr(person_data, 'LAST_COMPLETED_COURSE', None):
                continue

        # Add person to the filtered list if all conditions are met
        filtered_people[person_id] = person_data

    return filtered_people
