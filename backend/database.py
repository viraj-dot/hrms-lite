from pymongo import MongoClient

MONGO_URL = (
    "mongodb+srv://hrmsuser:Viraj%402003@hrms.eff28sy.mongodb.net/"
    "hrms_lite?retryWrites=true&w=majority"
)

client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

db = client["hrms_lite"]

def get_database():
    return db
