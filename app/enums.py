from enum import Enum


class InsensitiveCaseEnum(Enum):
    @classmethod
    def _missing_(cls, value: object):
        value = str(value).lower()
        for member in cls:
            if str(member.value).lower() == value:
                return member
        return None


class Day(InsensitiveCaseEnum):
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    THURSDAY = "THURSDAY"
    WEDNESDAY = "WEDNESDAY"
    TUESDAY = "TUESDAY"
    FRIDAY = "FRIDAY"


class SlotType(InsensitiveCaseEnum):
    LECTURE = "LECTURE"
    TUTORIAL = "TUTORIAL"
    LAB = "LAB"
