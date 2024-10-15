from datetime import datetime
from typing import List, Set, Optional, Dict


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parses a date string into a datetime object.

    Args:
        date_str (str): Date string in the format 'DD.MM.YYYY'.

    Returns:
        Optional[datetime]: Parsed datetime object or None if invalid.
    """
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except (ValueError, TypeError):
        return None


class Human:
    def __init__(self):
        self.STD_NUMBER: int = 0
        self.FULLNAME: str = ''
        self.PHONE_NUMBER: str = ''
        self.APPLY_DATE: Optional[datetime] = None
        self.isMember: bool = False
        self.COURSE_LEVEL: str = ''
        self.COURSE_SLOTS: List[int] = []
        self.FRIENDS: List[int] = []
        self.isPlaced: bool = False
        self.LAST_COMPLETED_COURSE: str = ''


class Group:
    def __init__(self, members: List[Human]):
        """
        Initializes the group with members and calculates key attributes.

        Args:
            members (List[Human]): List of Human objects that belong to the group.
        """
        self.MEMBERS: List[Human] = members
        self.APPLY_DATE: Optional[datetime] = self.calculate_earliest_apply_date()
        self.COURSE_SLOTS: List[int] = self.calculate_course_slots_intersection()
        self.isPlaced: bool = False
        self.PLACED_SLOTS: List[int] = []
        self.COURSE_LEVEL: str = ''
        self.check_course_level()

    def calculate_earliest_apply_date(self) -> Optional[datetime]:
        """
        Calculate the earliest application date among group members.

        Returns:
            Optional[datetime]: Earliest application date or None if no valid dates.
        """
        valid_dates = [member.APPLY_DATE for member in self.MEMBERS if member.APPLY_DATE is not None]
        return min(valid_dates, default=None)  # Use default=None to avoid ValueError on empty list

    def calculate_course_slots_intersection(self) -> List[int]:
        """
        Calculate the intersection of available course slots among group members.

        Returns:
            List[int]: A list of course slots available to all members.
        """
        if not self.MEMBERS:
            return []
        common_slots = set(self.MEMBERS[0].COURSE_SLOTS)
        for member in self.MEMBERS[1:]:
            common_slots.intersection_update(member.COURSE_SLOTS)
        return list(common_slots)

    def check_course_level(self):
        """
        Ensure all members are enrolled in the same course level.
        Removes members not matching the earliest member's course level.
        """
        if not self.MEMBERS:
            return

        # Use the course level of the earliest applicant
        earliest_course_level = self.MEMBERS[0].COURSE_LEVEL

        # Retain only members with the same course level
        self.MEMBERS = [member for member in self.MEMBERS if member.COURSE_LEVEL == earliest_course_level]

        # Recalculate apply date and course slots after filtering members
        self.APPLY_DATE = self.calculate_earliest_apply_date()
        self.COURSE_SLOTS = self.calculate_course_slots_intersection()

    def get_member_std_numbers(self) -> Set[int]:
        """
        Get the set of student numbers of all group members.

        Returns:
            Set[int]: Set of student numbers.
        """
        return {member.STD_NUMBER for member in self.MEMBERS}

    def __str__(self) -> str:
        """
        String representation of the group object.

        Returns:
            str: String description of the group members and earliest apply date.
        """
        return f"Group with members {[member.FULLNAME for member in self.MEMBERS]} and earliest apply date {self.APPLY_DATE}"


# Example slot dictionary mapping from time slots to integers
slots: Dict[str, int] = {
    "Pazartesi - 1.Slot - 9.00 - 12.00": 11,
    "Pazartesi - 2.Slot - 12.00 - 15.00": 12,
    "Pazartesi - 3.Slot - 15.00 - 18.00": 13,
    "Salı - 1.Slot - 9.00 - 12.00": 21,
    "Salı - 2.Slot - 12.00 - 15.00": 22,
    "Salı - 3.Slot - 15.00 - 18.00": 23,
    "Çarşamba - 1.Slot - 9.00 - 12.00": 31,
    "Çarşamba - 2.Slot - 12.00 - 15.00": 32,
    "Çarşamba - 3.Slot - 15.00 - 18.00": 33,
    "Perşembe - 1.Slot - 9.00 - 12.00": 41,
    "Perşembe - 2.Slot - 12.00 - 15.00": 42,
    "Perşembe - 3.Slot - 15.00 - 18.00": 43,
    "Cuma - 1.Slot - 9.00 - 12.00": 51,
    "Cuma - 2.Slot - 12.00 - 15.00": 52,
    "Cuma - 3.Slot - 15.00 - 18.00": 53,
    "Cumartesi - 1.Slot - 9.00 - 12.00": 61,
    "Cumartesi - 2.Slot - 12.00 - 15.00": 62,
    "Cumartesi - 3.Slot - 15.00 - 18.00": 63,
    "Pazar - 1.Slot - 9.00 - 12.00": 71,
    "Pazar - 2.Slot - 12.00 - 15.00": 72,
    "Pazar - 3.Slot - 15.00 - 18.00": 73
}
