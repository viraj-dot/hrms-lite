from fastapi import APIRouter, HTTPException, status
from models.attendance import AttendanceCreate
from database import get_database

router = APIRouter(prefix="/attendance", tags=["Attendance"])

db = get_database()
attendance_collection = db["attendance"]
employee_collection = db["employees"]


@router.post("/", status_code=status.HTTP_201_CREATED)
def mark_attendance(attendance: AttendanceCreate):
    # Check employee exists
    if not employee_collection.find_one({"employee_id": attendance.employee_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    attendance_data = attendance.dict()
    attendance_data["date"] = attendance_data["date"].isoformat()

    attendance_collection.insert_one(attendance_data)
    return {"message": "Attendance marked successfully"}


@router.get("/{employee_id}")
def get_attendance(employee_id: str):
    records = list(
        attendance_collection.find(
            {"employee_id": employee_id},
            {"_id": 0}
        )
    )
    return records
