from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import ai
import re

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
    
    for y in comments["all_good_comments"]:
        goodCommentsString += y + ", "
        
    for y in comments["all_bad_comments"]:
        badCommentsString += y + ", "
    
    goodWords = ai.summarize("positive", goodCommentsString)
    badWords = ai.summarize("critical", badCommentsString)
    
    x.update_one({"teacherID": id}, {"$set": {"good_summary": goodWords}})
    x.update_one({"teacherID": id}, {"$set": {"bad_summary": badWords}})
    
def _buildJSON(comments):
    if comments:
        comments.pop("_id", None)
        json_document = json.dumps(comments, default=str, indent=4)
        return json_document
    else:
        return json.dumps({}, default=str, indent=4)
# methods for usage in the API

def apiSelectTeacher(id):
    x = db["allComments"]
    comments = x.find_one({"teacherID": id})
    
    return _buildJSON(comments)

def searchTeacher(q):
    q = re.escape(q)
    x = db["allComments"]
    query = {"teacherName": {"$regex": q, "$options": "i"}}  # Case-insensitive regex
    search = x.find(query).limit(10)
    
    results = []
    for result in search:
        results.append({"id": result["teacherID"], "name": result["teacherName"], "goodCount": len(result["all_good_comments"]), "badCount": len(result["all_bad_comments"]), "url": "/teacher/" + str(result["teacherID"])})
        
    return results

def getRandomFrontend(count:int):
    data = collection.aggregate([{"$sample": {"size": 3}}])
    
    formatData = []
    
    for d in data:
        goodL = len(d["all_good_comments"])
        badL = len(d["all_bad_comments"])
        formatData.append({"teacherName": d["teacherName"], "url": "/teacher/" + str(d["teacherID"]), "description": f"{str(goodL)} positive comments, {str(badL)} critical comments"})
        
    return formatData