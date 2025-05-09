from typing import Dict

from app.enums import Day, SlotType
from app.models import Course, Slot, TimePoint
from app.service import group_slots

from ..fixtures.Courses import conflicting_course, sample_courses


def test_groups_slots_return_dict(sample_courses):
    assert isinstance(group_slots(sample_courses), Dict)


def test_groups_slots_empty_courses_list():
    result = group_slots([])
    assert isinstance(result, Dict)
    assert len(result) == 0


def test_groups_slots_sample_courses():
    course = Course(
        name="Simple Course",
        slots=[
            Slot(
                start=TimePoint(hour=9, minute=0),
                end=TimePoint(hour=10, minute=0),
                day=Day.MONDAY,
                slot_type=SlotType.LECTURE,
            ),
            Slot(
                start=TimePoint(hour=11, minute=0),
                end=TimePoint(hour=12, minute=0),
                day=Day.MONDAY,
                slot_type=SlotType.TUTORIAL,
            ),
        ],
        slot_types=[SlotType.LECTURE, SlotType.TUTORIAL],
    )
    result = group_slots([course])
    assert len(result[course.name]) == 1
    assert len(result[course.name][0]) == 2


def test_groups_slots_problamtic_course(conflicting_course):
    result = group_slots([conflicting_course])
    print(result)
    assert len(result[conflicting_course.name]) == 0
