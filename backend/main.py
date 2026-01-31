from fastapi import FastAPI
from database import get_database
from routes.employee import router as employee_router

app = FastAPI(title="HRMS Lite Backend")

@app.get("/")
def root():
    return {"message": "HRMS Lite Backend is running"}

@app.get("/health")
def health_check():
    db = get_database()
    return {"status": "Database connected"}

app.include_router(employee_router)
