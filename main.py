import requests
import os
from bs4 import BeautifulSoup
import db

def authHeaders(cookieBlob):
    return  {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Cookie": cookieBlob,
    }

def getInternalColleges(auth):
    r = requests.get("https://www.applyweb.com/eval/new/reportbrowser/schools", headers=auth)
    codes = []
    for code in r.json():
        codes.append(code["schoolCode"])
        
    return codes

# 181, "CS"
def getEvalURLs(auth, termID, collegeID):
    try:
        os.remove("data.csv")
    except:
        print("didn't remove data.csv")
        
    with open("data.csv", "a") as x:
        x.write("courseID,teacherID,teacherName,commentsURL\n")
        
    go = True
    pge = 1
    while go:
        call = getEvalClassesInternal(auth, termID, collegeID, pge)
        if call == None:
            go = False
        pge += 1

def getEvalClassesInternal(auth, termID, collegeID, page):
    data = {
        "page": page,
        "rpp": 200,
        "termIds": [termID],
        "schoolCodes": collegeID,
        "excludeTA": False,
        "sort": None
    }
    print(data)

    r = requests.post("https://www.applyweb.com/eval/new/reportbrowser/evaluatedCourses", json=data, headers=auth)
    
    if "json" not in r.headers["Content-type"]:
        raise ValueError("json not in http")
    
    if r.status_code != 200:
        raise ValueError("non-200 status")
    
    api = r.json()
    
    if len(api["data"]) == 0:
        return None
    
    for course in api["data"]:
        print("course")
        id = course["courseId"]
        teacherID = course["instructorId"]
        teacher = course["instructorFirstName"] + "-" + course["instructorLastName"]
        url = f"https://www.applyweb.com/eval/new/showreport?c={str(id)}&i={str(teacherID)}&t={termID}&r=9&d=true"
        with open("data.csv", "a") as d:
            d.write(f"{str(id)},{str(teacherID)},{str(teacher)},{str(url)}\n")
    
    return 'ok'

def processEachComments(csvFile, auth):
    # assumes CSV file is in the format
    # courseID,teacherID,teacherName,commentsURL
    with open(csvFile, "r") as file:
        for line in file:
            l = line.strip()
            if "courseID" not in l:
                data = l.split(",")
                try:
                    comments = scrapeCommentsPage(data[3], auth)
                    mongoData = {
                        "courseID": int(data[0]),
                        "teacherID": int(data[1]),
                        "teacherName": data[2].replace("-", " "),
                        "comments": comments
                    }
                    db.insert(mongoData)
                except AttributeError:
                    print("couldn't scrape, some error")
                
                
def scrapeCommentsPage(url, auth):
    print("scraping url " + url)
    auth["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    r = requests.get(url, headers=auth)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # " Q: What were the strengths of this course and/or this instructor? "
    good_comments = soup.find("div", {"id": "11_3_402"})
    good_comments_table = good_comments.find("table")
    
    # " Q: What could the instructor do to make this course better? "
    bad_comments = soup.find("div", {"id": "11_3_403"})
    bad_comments_table = bad_comments.find("table")
    
    good = []
    for td in good_comments_table.find_all("td"):
        if td.find("a") != None:
            good.append(td.text.strip())
            
    bad = []
    for td in bad_comments_table.find_all("td"):
        if td.find("a") != None:
            bad.append(td.text.strip())
    
    
    return {"good_comments": good, "bad_comments": bad}

def getAllCommentsPerProf():
    return