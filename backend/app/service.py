from itertools import product
from typing import Dict, List

from .enums import SlotType
from .models import Course, Schedule, Slot


def group_slots(courses: List[Course]) -> Dict[str, List[List[Slot]]]:
    """
    Given a list of courses, for each course, generate all possible permutations that have slots of each slot type required for that course
    """

    def is_valid_combination(slots: List[Slot]) -> bool:
        # Check that no slots overlap
        for i, slot1 in enumerate(slots):
            for slot2 in slots[i + 1 :]:
                if slot1.overlap(slot2):
                    return False
        return True

    groups = {}

    for course in courses:
        slots_by_type: Dict[SlotType, List[Slot]] = {}
        for slot in course.slots:
            slots_by_type.setdefault(slot.slot_type, []).append(slot)

        # Get slot lists in order of course.slot_types
        slot_lists = [slots_by_type[st] for st in course.slot_types]

        # Generate all possible combinations
        all_combinations = list(product(*slot_lists))
        valid_combinations = [
            list(comb) for comb in all_combinations if is_valid_combination(list(comb))
        ]

        groups[course.name] = valid_combinations

    return groups


def generate_schedules(courses: List[Course]) -> List[Schedule]:
    """
    Given a list of courses, try to generate all possible schedules
    Only return schedules that include all courses, or return an empty list if none exist.
    """
    schedules: List[Schedule] = []
    groups = group_slots(courses)

    def aux(index: int, rsf: Schedule):
        if index == len(courses):
            if not rsf.empty() and len(rsf.courses) == len(courses):
                schedules.append(rsf)
            return

        # Try to take this course
        course = courses[index]
        valid_combinations = groups[course.name]

        for combination in valid_combinations:
            can_add = all(rsf.can_add(slot) for slot in combination)

            if can_add:
                new_schedule = rsf.clone()
                new_schedule.add_course(course.name)
                for slot in combination:
                    new_schedule.add_slot(course.name, slot)
                aux(index + 1, new_schedule)

    aux(0, Schedule(courses=[]))  # Start recursion with an empty schedule
    return schedules
