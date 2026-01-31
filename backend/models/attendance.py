from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

class AttendanceCreate(BaseModel):
    employee_id: str = Field(..., example="EMP001")
    date: date
    status: Literal["Present", "Absent"]

