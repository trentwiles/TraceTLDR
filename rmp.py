import ratemyprofessor
import requests

# ID used on Rate My Professors
NORTHEASTERN_SCHOOL_ID = "U2Nob29sLTY5Ng=="

def getNEU():
    return ratemyprofessor.get_school_by_name("Northeastern University")

def getNEU2(profName):
    data = {
    "query": """
        query NewSearchTeachersQuery(  $query: TeacherSearchQuery!  $count: Int  $includeCompare: Boolean!) {  newSearch {    teachers(query: $query, first: $count) {      didFallback      edges {        cursor        node {          id          legacyId          firstName          lastName          department          departmentId          school {            legacyId            name            id          }          ...CompareProfessorsColumn_teacher @include(if: $includeCompare)        }      }    }  }}fragment CompareProfessorsColumn_teacher on Teacher {  id  legacyId  firstName  lastName  school {    legacyId    name    id  }  department  departmentId  avgRating  avgDifficulty  numRatings  wouldTakeAgainPercentRounded  mandatoryAttendance {    yes    no    neither    total  }  takenForCredit {    yes    no    neither    total  }  ...NoRatingsArea_teacher  ...RatingDistributionWrapper_teacher}fragment NoRatingsArea_teacher on Teacher {  lastName  ...RateTeacherLink_teacher}fragment RatingDistributionWrapper_teacher on Teacher {  ...NoRatingsArea_teacher  ratingsDistribution {    total    ...RatingDistributionChart_ratingsDistribution  }}fragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {  r1  r2  r3  r4  r5}fragment RateTeacherLink_teacher on Teacher {  legacyId  numRatings  lockStatus}
        """,
        "variables": {
            "query": {
                "schoolID": NORTHEASTERN_SCHOOL_ID,
                "text": profName
            },
            "count": 10,
            "includeCompare": False
        }
    }
    
    # dGVzdDp0ZXN0 = "test:test" in base64
    result = requests.post("https://www.ratemyprofessors.com/graphql", json=data, headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0", "Authorization": "Basic dGVzdDp0ZXN0"})
    
    if result.status_code != 200:
        return None
    
    parsed = result.json()
    teacherList = parsed["data"]["newSearch"]["teachers"]["edges"]
    
    if len(teacherList) == 0:
        return None
    
    # now we have a list of possible teacher, but it obviously isn't feasible for a student to pick which one
    # so we'll make the bold assumption that the first teacher is the correct one
    return {"url": "https://www.ratemyprofessors.com/professor/" + str(teacherList[0]["node"]["legacyId"]), "newID": teacherList[0]["node"]["id"]}

def extractTeacher(newID):
    data = {
        "query": """
        query NewSearchTeachersQuery(  $query: TeacherSearchQuery!  $count: Int  $includeCompare: Boolean!) {  newSearch {    teachers(query: $query, first: $count) {      didFallback      edges {        cursor        node {          id          legacyId          firstName          lastName          department          departmentId          school {            legacyId            name            id          }          ...CompareProfessorsColumn_teacher @include(if: $includeCompare)        }      }    }  }}fragment CompareProfessorsColumn_teacher on Teacher {  id  legacyId  firstName  lastName  school {    legacyId    name    id  }  department  departmentId  avgRating  avgDifficulty  numRatings  wouldTakeAgainPercentRounded  mandatoryAttendance {    yes    no    neither    total  }  takenForCredit {    yes    no    neither    total  }  ...NoRatingsArea_teacher  ...RatingDistributionWrapper_teacher}fragment NoRatingsArea_teacher on Teacher {  lastName  ...RateTeacherLink_teacher}fragment RatingDistributionWrapper_teacher on Teacher {  ...NoRatingsArea_teacher  ratingsDistribution {    total    ...RatingDistributionChart_ratingsDistribution  }}fragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {  r1  r2  r3  r4  r5}fragment RateTeacherLink_teacher on Teacher {  legacyId  numRatings  lockStatus}
        """,
        "variables": {
            "id": newID,
        }
    }
    
    result = requests.post("https://www.ratemyprofessors.com/graphql", json=data, headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0", "Authorization": "Basic dGVzdDp0ZXN0"})

    # for our intents and purposes we only need to average rating and the total rating count
    if result.status_code != 200:
        return None
    
    parsed = result.json()
    dataList = parsed["data"]["node"]
    
    if len(dataList) == 0:
        return None
    
    rating = dataList["avgRating"]
    numRatings = dataList["numRatings"]
    reflectiveName = dataList["firstName"] + " " + dataList["lastName"]

    return {"rating": rating, "numRatings": numRatings, "fullName": reflectiveName}    

def getRating(professor):
    
    try:
        data = getNEU2(professor)
        details = getRating(data["newID"])
        return {"rating": details["rating"], "total": details["numRatings"], "url": data["url"]}
    except:
        return {"rating": None, "total": None, "url": "/404"}