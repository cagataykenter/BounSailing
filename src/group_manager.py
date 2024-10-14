from typing import List

from src.schemas import Group

def initial_grouping(people):
    groups = []

    for person in people:
        std_nums = [person] + people[person].FRIENDS

        # Retrieve Human objects for all std_nums
        group_members = [people[std_num] for std_num in std_nums if std_num in people]

        # Create the group
        group = Group(members=group_members)

        groups.append(group)

    return groups

# TODO: The group with the highest population for each person will remain, and the other groups will be deleted. If in the last case there are two groups with the same population for a person, the two groups will be merged and 'set' to prevent repetition
# Function to check and remove subset groups
def remove_subset_groups(groups: List[Group]) -> List[Group]:
    final_groups = []
    for i, group in enumerate(groups):
        is_subset = False
        group_members_set = group.get_member_std_numbers()
        for j, other_group in enumerate(groups):
            if i != j:
                other_group_members_set = other_group.get_member_std_numbers()
                if group_members_set.issubset(other_group_members_set):
                    is_subset = True
                    break  # If group is a subset, skip it

        if not is_subset:
            final_groups.append(group)

    # Sort the final groups by the earliest APPLY_DATE
    final_groups.sort(key=lambda g: g.APPLY_DATE)

    return final_groups