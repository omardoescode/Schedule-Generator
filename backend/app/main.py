from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import Course, Schedule
from .service import generate_schedules

app = FastAPI()

# Allow CORS for frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/schedule")
def schedule(courses: List[Course]) -> List[Schedule]:
    # Validation: every slot_type must have at least one slot of that type
    for course in courses:
        slot_types_in_slots = {slot.slot_type for slot in course.slots}
        for required in course.slot_types:
            if required not in slot_types_in_slots:
                raise HTTPException(
                    status_code=400,
                    detail=f"Course '{course.name}' is missing slot(s) for required type: {required}"
                )
    result = generate_schedules(courses)
    result.sort(key=lambda schedule: -len(schedule.courses))
    return result


@app.get("/ping")
async def root():
    return {"ping": "pong"}
