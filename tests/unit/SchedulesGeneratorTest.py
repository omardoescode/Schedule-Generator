from typing import List

from app.enums import Day, SlotType
from app.models import Course, Schedule, Slot, TimePoint
from app.service import generate_schedules

from ..fixtures.Courses import conflicting_course, normal_course


def test_generate_schedules_return_list(normal_course):
    result = generate_schedules([normal_course])
    assert isinstance(result, List)
    assert all(isinstance(schedule, Schedule) for schedule in result)


def test_generate_schedules_empty_courses_list():
    result = generate_schedules([])
    assert isinstance(result, List)
    assert len(result) == 0


def test_generate_schedules_single_course():
    course = Course(
        name="Single Course",
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
    result = generate_schedules([course])
    assert len(result) == 1
    assert len(result[0].courses) == 1


def test_generate_schedules_conflicting_course(conflicting_course):
    result = generate_schedules([conflicting_course])
    print(result)
    assert len(result) == 0
