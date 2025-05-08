from typing import List

from fastapi import FastAPI

from .models import Course, Schedule
from .service import generate_schedules

app = FastAPI()


@app.post("/schedule")
def schedule(courses: List[Course]) -> List[Schedule]:
    result = generate_schedules(courses)
    result.sort(key=lambda schedule: -len(schedule.courses))
    return result


@app.get("/ping")
async def root():
    return {"ping": "pong"}
