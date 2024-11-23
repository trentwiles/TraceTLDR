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
    teachers = collection.find({"teacherID": id})
    all_good_comments = []
    all_bad_comments = []
        
    name = ""
    for teacher in teachers:
        for c in teacher["comments"]["good_comments"]:
            all_good_comments.append(c)
            
        for c in teacher["comments"]["bad_comments"]:
            all_bad_comments.append(c)
            
        name = teacher["teacherName"]
    
    data = {
        'teacherID': id,
        'teacherName': name,
        'all_good_comments': all_good_comments,
        'all_bad_comments': all_bad_comments,
        'summary': ''
    }
    
    x = db["allComments"]
    x.insert_one(data)

def selectTeacherAllComments(id):
    x = db["allComments"]
    comments = x.find_one({"teacherID": id})
    
    
    