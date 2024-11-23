from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("mongo"))

db = client["trace"]
collection = db["comments"]

def insert(data):
    collection.insert_one(data)
    
def getTeachers():
    return collection.distinct("teacherID")

def selectTeacher(id):
    teachers = collection.find({"teacherID": id}).toArray()
    all_good_comments = []
    all_bad_comments = []
    
    if len(teachers) == 0:
        return None
    
    for teacher in teachers:
        print(teacher)
    