from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., example="EMP001")
    full_name: str = Field(..., example="John Doe")
    email: EmailStr
    department: str = Field(..., example="Engineering")
