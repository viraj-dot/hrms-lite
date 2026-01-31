from fastapi import FastAPI
from database import get_database
from models.employee import EmployeeCreate


app = FastAPI(title="HRMS Lite Backend")

@app.get("/")
def root():
    return {"message": "HRMS Lite Backend is running"}

@app.get("/health")
def health_check():
    db = get_database()
    return {"status": "Database connected"}
