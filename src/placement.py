import pandas as pd

# TODO: Seperate the slots according to course level
def course_slots_creating(course_slots, term_count=None, quotas=None):
    """
    Create slot quotas for multiple course terms based on user input or provided arguments.

    Args:
        course_slots (list[int]): List of slot identifiers.
        term_count (int, optional): Number of terms to create slots for. Will prompt if not provided.
        quotas (dict, optional): A dictionary of pre-set quotas for each slot. Will prompt if not provided.

    Returns:
        dict: A dictionary where keys are slot-term combinations (e.g., "11_1") and values are quotas.
    """
    # If term count is not provided, prompt the user
    if term_count is None:
        term_count = int(input("Please write how many terms do you want for creating slots? "
                               "(e.g. 2 for October and November course terms): "))

    # Initialize an empty dictionary for slot quotas
    slot_quotas = {}

    # If quotas aren't provided, prompt the user for each slot-term combination
    if quotas is None:
        for term in range(term_count):
            print(f"\nEntering quotas for term {term + 1}:")
            for slot in course_slots:
                slot_quotas[slot] = int(
                    input(f"Please write the quota for the slot {slot} in term {term + 1}: "))
    else:
        # If pre-set quotas are provided, use them directly
        for term in range(term_count):
            for slot in course_slots:
                slot_key = slot
                if slot_key in quotas:
                    slot_quotas[slot_key] = quotas[slot_key]
                else:
                    # If some quotas are missing in provided dict, prompt for them
                    slot_quotas[slot_key] = int(
                        input(f"Please write the quota for the slot {slot} in term {term + 1}: "))

    return slot_quotas


def place_groups(groups, slots, slot_capacity):
    """
    Place groups into available slots based on their preferences and application times.

    Args:
        groups (List[Group]): List of groups to place.
        slots (Dict[int, int]): Dictionary with slot numbers as keys and their current capacities as values.
        slot_capacity (Dict[int, int]): Dictionary with slot numbers and maximum capacity per slot.

    Returns:
        pd.DataFrame: A dataframe with group placement details.
    """

    # Initialize the result tracking
    placements = []
    unplaced_groups = []

    # First placement loop: try to place all groups based on their first preference
    for group in groups:
        placed = False
        for preferred_slot in group.COURSE_SLOTS:
            if slots[preferred_slot] + len(group.MEMBERS) <= slot_capacity[preferred_slot]:
                # Place the group in this slot
                placements.append({
                    'group': [member.FULLNAME for member in group.MEMBERS],
                    'slot': preferred_slot,
                    'apply_date': group.APPLY_DATE
                })
                # Update slot capacity
                slots[preferred_slot] += len(group.MEMBERS)
                placed = True
                break

        if not placed:
            unplaced_groups.append(group)

    # Save the result of this round
    df_first_round = pd.DataFrame(placements)

    # Second placement round: try to place unplaced groups in their second preferences
    placements = []
    for group in unplaced_groups:
        placed = False
        for preferred_slot in group.COURSE_SLOTS[1:]:  # Start from the second preference
            if slots[preferred_slot] + len(group.MEMBERS) <= slot_capacity[preferred_slot]:
                placements.append({
                    'group': [member.FULLNAME for member in group.MEMBERS],
                    'slot': preferred_slot,
                    'apply_date': group.APPLY_DATE
                })
                slots[preferred_slot] += len(group.MEMBERS)
                placed = True
                break

    df_second_round = pd.DataFrame(placements)

    return df_first_round, df_second_round

# TODO: Print out the ones who couldn't be placed. Try to solve that.
def optimize_placements(group_list, slots, slot_capacity):
    """
    Optimize the placement by running multiple rounds of placement and selecting the one
    with the highest number of placed people.

    Args:
        group_list (List[Group]): List of groups to place.
        slots (Dict[int, int]): Dictionary with slot numbers as keys and their current capacities as values.
        slot_capacity (Dict[int, int]): Dictionary with slot numbers and maximum capacity per slot.

    Returns:
        pd.DataFrame: Optimized placement dataframe.
    """
    best_placement = None
    max_people_placed = 0

    # Iterate multiple times, each time adjusting preferences
    for _ in range(len(slot_capacity)):
        df_first, df_second = place_groups(group_list, slots.copy(), slot_capacity)

        # Calculate how many people are placed in this round
        total_placed = len(df_first) + len(df_second)

        if total_placed > max_people_placed:
            best_placement = pd.concat([df_first, df_second], ignore_index=True)
            max_people_placed = total_placed

    return best_placement
