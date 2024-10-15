from typing import List
from collections import defaultdict
from src.schemas import Group, Human


def initial_grouping(people: dict[int, Human]) -> List[Group]:
    """
    Creates initial groups based on people's friendship relationships.

    Args:
        people (dict[int, Human]): Dictionary where keys are student numbers and values are Human objects.

    Returns:
        List[Group]: List of groups created from the friendship data.
    """
    groups = []

    for person_id, person in people.items():
        # Create a list of student numbers (person and their friends)
        std_nums = [person_id] + person.FRIENDS

        # Retrieve Human objects for all valid student numbers
        group_members = [people[std_num] for std_num in std_nums if std_num in people]

        # Create the group
        group = Group(members=group_members)

        # Get the COURSE_LEVEL of the first member
        first_course_level = group.MEMBERS[0].COURSE_LEVEL if group.MEMBERS else None

        # Check if all members have the same COURSE_LEVEL
        if all(member.COURSE_LEVEL == first_course_level for member in group.MEMBERS):
            # Assign the COURSE_LEVEL to the group and add it to valid groups
            group.COURSE_LEVEL = first_course_level
            groups.append(group)
        else:
            # Dismantle the group and print its details for debugging
            print(f"Dismantling group with members {[member.FULLNAME for member in group.MEMBERS]} "
                  f"due to inconsistent COURSE_LEVELs.")

    return groups


def remove_subset_groups(groups: List[Group]) -> List[Group]:
    """
    Removes groups that are subsets of other groups and filters out duplicates.

    Args:
        groups (List[Group]): List of groups to be filtered.

    Returns:
        List[Group]: List of final non-subset and unique groups.
    """
    final_groups = []

    def is_group_duplicate(new_group: Group, existing_groups: List[Group]) -> bool:
        """
        Checks if a group is a duplicate of any existing group.

        Args:
            new_group (Group): The new group to check for duplication.
            existing_groups (List[Group]): List of existing groups.

        Returns:
            bool: True if the group is a duplicate, False otherwise.
        """
        for group in existing_groups:
            if len(new_group.MEMBERS) == len(group.MEMBERS):
                if all(new_member.FULLNAME == existing_member.FULLNAME for new_member, existing_member in
                       zip(new_group.MEMBERS, group.MEMBERS)):
                    return True  # If all members match, it's a duplicate
        return False

    for i, group in enumerate(groups):
        is_subset = False
        group_members_set = group.get_member_std_numbers()
        for j, other_group in enumerate(groups):
            if i != j:
                other_group_members_set = other_group.get_member_std_numbers()

                # Check if the group is a subset of another group
                if group_members_set.issubset(other_group_members_set):
                    # Skip identical groups (do not remove)
                    if group_members_set == other_group_members_set:
                        break
                    is_subset = True
                    break

        if not is_subset:
            # Sort members by FULLNAME for consistency in comparison
            group.MEMBERS.sort(key=lambda member: member.FULLNAME)
            if not is_group_duplicate(group, final_groups):
                final_groups.append(group)

    # Sort the final groups by the earliest APPLY_DATE
    final_groups.sort(key=lambda g: g.APPLY_DATE)

    return final_groups


def merge_groups_by_members(groups: List[Group]) -> List[Group]:
    """
    Merges groups that share at least one member to create unique groups.

    Args:
        groups (List[Group]): List of initial groups.

    Returns:
        List[Group]: List of unique groups after merging.
    """
    member_to_group = defaultdict(set)

    # Create a mapping of FULLNAME to Human object for easy retrieval
    fullname_to_human = {member.FULLNAME: member for group in groups for member in group.MEMBERS}

    # Iterate through all groups and associate each member with a set of connected members
    for group in groups:
        group_member_names = {member.FULLNAME for member in group.MEMBERS}

        # Merge this group's members with any existing groups that share at least one member
        members_to_merge = set()
        for member_name in group_member_names:
            if member_name in member_to_group:
                members_to_merge.update(member_to_group[member_name])

        # Merge current group members and members from previously merged sets
        merged_group = group_member_names.union(members_to_merge)

        # Update the dictionary for all members in the merged group
        for member_name in merged_group:
            member_to_group[member_name] = merged_group

    # Create new unique groups from the merged member sets
    unique_groups = []
    seen_groups = set()  # To track which member sets have been processed

    for group in member_to_group.values():
        group_frozenset = frozenset(group)  # Create a hashable version of the set for comparison
        if group_frozenset not in seen_groups:
            seen_groups.add(group_frozenset)

            # Convert the merged group back into Group objects using the fullname_to_human mapping
            merged_group_members = [fullname_to_human[name] for name in group]
            new_group = Group(members=merged_group_members)

            # Get the COURSE_LEVEL of the first member
            first_course_level = new_group.MEMBERS[0].COURSE_LEVEL if new_group.MEMBERS else None

            # Check if all members have the same COURSE_LEVEL
            if all(member.COURSE_LEVEL == first_course_level for member in new_group.MEMBERS):
                # Assign the COURSE_LEVEL to the group and add it to valid groups
                new_group.COURSE_LEVEL = first_course_level
                # Sort members in the merged group according to their apply date so that we can remove people if necessary in the future
                new_group.MEMBERS.sort(key=lambda member: member.APPLY_DATE)
                unique_groups.append(new_group)
            else:
                # Dismantle the group and print its details for debugging
                print(f"Dismantling group with members {[member.FULLNAME for member in new_group.MEMBERS]} "
                      f"due to inconsistent COURSE_LEVELs.")

    # Sort the final groups by the earliest APPLY_DATE
    unique_groups.sort(key=lambda g: g.APPLY_DATE)


    return unique_groups