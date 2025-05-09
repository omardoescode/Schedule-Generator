from typing import List

import pytest

from app.enums import Day, SlotType
from app.models import Course, Slot, TimePoint


# Test fixtures
@pytest.fixture
def normal_course() -> Course:
    return Course(
        name="Math 101",
        slots=[
            Slot(
                start=TimePoint(hour=9, minute=0),
                end=TimePoint(hour=10, minute=30),
                day=Day.MONDAY,
                slot_type=SlotType.LECTURE,
            ),
            Slot(
                start=TimePoint(hour=14, minute=0),
                end=TimePoint(hour=16, minute=0),
                day=Day.WEDNESDAY,
                slot_type=SlotType.LAB,
            ),
        ],
        slot_types=[SlotType.LECTURE, SlotType.LAB],
    )


@pytest.fixture
def sample_courses() -> List[Course]:
    return [
        Course(
            name="Math 101",
            slots=[
                Slot(
                    start=TimePoint(hour=9, minute=0),
                    end=TimePoint(hour=10, minute=30),
                    day=Day.MONDAY,
                    slot_type=SlotType.LECTURE,
                ),
                Slot(
                    start=TimePoint(hour=14, minute=0),
                    end=TimePoint(hour=16, minute=0),
                    day=Day.WEDNESDAY,
                    slot_type=SlotType.LAB,
                ),
            ],
            slot_types=[SlotType.LECTURE, SlotType.LAB],
        ),
        Course(
            name="Physics 201",
            slots=[
                Slot(
                    start=TimePoint(hour=11, minute=0),
                    end=TimePoint(hour=12, minute=30),
                    day=Day.TUESDAY,
                    slot_type=SlotType.LECTURE,
                ),
                Slot(
                    start=TimePoint(hour=13, minute=0),
                    end=TimePoint(hour=14, minute=0),
                    day=Day.THURSDAY,
                    slot_type=SlotType.TUTORIAL,
                ),
            ],
            slot_types=[SlotType.LECTURE, SlotType.TUTORIAL],
        ),
    ]


@pytest.fixture
def conflicting_course() -> Course:
    return Course(
        name="Problematic Course",
        slots=[
            Slot(
                start=TimePoint(hour=9, minute=0),
                end=TimePoint(hour=10, minute=0),
                day=Day.MONDAY,
                slot_type=SlotType.LECTURE,
            ),
            Slot(
                start=TimePoint(hour=9, minute=30),
                end=TimePoint(hour=11, minute=0),
                day=Day.MONDAY,
                slot_type=SlotType.TUTORIAL,
            ),
        ],
        slot_types=[SlotType.LECTURE, SlotType.TUTORIAL],
    )
