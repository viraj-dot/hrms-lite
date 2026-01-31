from fastapi import APIRouter, HTTPException, status
from models.employee import EmployeeCreate
from database import get_database

router = APIRouter(prefix="/employees", tags=["Employees"])

db = get_database()
employee_collection = db["employees"]


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_employee(employee: EmployeeCreate):
    # Check duplicate employee_id
    if employee_collection.find_one({"employee_id": employee.employee_id}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this ID already exists"
        )

    employee_collection.insert_one(employee.dict())
    return {"message": "Employee added successfully"}


@router.get("/")
def list_employees():
    employees = list(employee_collection.find({}, {"_id": 0}))
    return employees


@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    result = employee_collection.delete_one({"employee_id": employee_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return {"message": "Employee deleted successfully"}
