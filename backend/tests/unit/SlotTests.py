from app.enums import Day, SlotType
from app.models import Slot, TimePoint


def test_overlaping_slots():
    slot1 = Slot(
        start=TimePoint(hour=9, minute=0),
        end=TimePoint(hour=10, minute=0),
        day=Day.MONDAY,
        slot_type=SlotType.LECTURE,
    )

    slot2 = Slot(
        start=TimePoint(hour=9, minute=30),
        end=TimePoint(hour=11, minute=0),
        day=Day.MONDAY,
        slot_type=SlotType.TUTORIAL,
    )

    assert slot1.overlap(slot1)
    assert slot1.overlap(slot2)
