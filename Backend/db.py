import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv(
    'MONGODB_URI',
    'mongodb+srv://krishnadarapaneni85_db_user:KRISHNA%40681d@cluster0.63tdiai.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
)
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'EmployeePayrollDB')

client = None
db = None


def get_db():
    global client, db
    if db is None:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB_NAME]
    return db


def get_collection(name):
    database = get_db()
    return database[name]
