from pymongo import MongoClient
from dotenv import load_dotenv
import os
import ai

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
        'good_summary': '',
        'bad_summary': ''
    }
    
    x = db["allComments"]
    x.insert_one(data)

def selectTeacherAllCommentsAndSummarize(id):
    x = db["allComments"]
    comments = x.find_one({"teacherID": id})
    
    goodCommentsString = ""
    badCommentsString = ""
    
    for x in comments["all_good_comments"]:
        goodCommentsString += x + ", "
        
    for x in comments["all_bad_comments"]:
        badCommentsString += x + ", "
    
    goodWords = ai.summarize("positive", goodCommentsString)
    badWords = ai.summarize("critical", badCommentsString)
    
    x.update_one({"teacherID": id}, {"$set": {"good_summary": goodWords}})
    x.update_one({"teacherID": id}, {"$set": {"bad_summary": badWords}})
    
    