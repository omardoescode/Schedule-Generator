from copy import deepcopy
from functools import total_ordering
from typing import List, Self

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from .enums import Day, SlotType
from .utils import find, flatmap


@total_ordering
class TimePoint(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour in 0–23")
    minute: int = Field(..., ge=0, le=59, description="Minute in 0–59")

    def total_minutes(self):
        return self.hour * 60 + self.minute

    def __lt__(self, other: "TimePoint") -> bool:
        return self.total_minutes() < other.total_minutes()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimePoint):
            return NotImplemented
        return self.total_minutes() == other.total_minutes()


class Slot(BaseModel):
    start: TimePoint
    end: TimePoint
    day: Day
    slot_type: SlotType

    @field_validator("end")
    @classmethod
    def end_after_start(cls, end: TimePoint, info: ValidationInfo):
        if end < info.data["start"]:
            raise ValueError("end must be after start")
        return end

    def overlap(self, other: "Slot") -> bool:
        return self.day == other.day and not (
            self.end <= other.start or self.start >= other.end
        )


class Course(BaseModel):
    name: str
    slots: List[Slot]
    slot_types: List[SlotType]


class RegisteredCourse(BaseModel):
    name: str
    slots: List[Slot]


class Schedule(BaseModel):
    courses: List[RegisteredCourse]

    def empty(self):
        return len(self.courses) == 0

    def add_slot(self, course_name: str, slot: Slot):
        if not self.can_add(slot):
            raise ValueError("Cannot add slot to schedule")
        course = find(lambda course: course.name == course_name, self.courses)
        if not course:
            raise ValueError("Unidentified Course")
        course.slots.append(slot)

    def can_add(self, test: Slot) -> bool:
        all_slots = flatmap(lambda course: course.slots, self.courses)
        return not any(slot.overlap(test) for slot in all_slots)

    def add_course(self, course_name: str):
        if any(course.name == course_name for course in self.courses):
            return
        self.courses.append(RegisteredCourse(name=course_name, slots=[]))

    def clone(self) -> Self:
        return deepcopy(self)
