import requests

# ID used on Rate My Professors
NORTHEASTERN_SCHOOL_ID = "U2Nob29sLTY5Ng=="

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
        query TeacherRatingsPageQuery(  $id: ID!) {  node(id: $id) {    __typename    ... on Teacher {      id      legacyId      firstName      lastName      department      school {        legacyId        name        city        state        country        id      }      lockStatus      ...StickyHeaderContent_teacher      ...RatingDistributionWrapper_teacher      ...TeacherInfo_teacher      ...SimilarProfessors_teacher      ...TeacherRatingTabs_teacher    }    id  }}fragment StickyHeaderContent_teacher on Teacher {  ...HeaderDescription_teacher  ...HeaderRateButton_teacher}fragment RatingDistributionWrapper_teacher on Teacher {  ...NoRatingsArea_teacher  ratingsDistribution {    total    ...RatingDistributionChart_ratingsDistribution  }}fragment TeacherInfo_teacher on Teacher {  id  lastName  numRatings  ...RatingValue_teacher  ...NameTitle_teacher  ...TeacherTags_teacher  ...NameLink_teacher  ...TeacherFeedback_teacher  ...RateTeacherLink_teacher  ...CompareProfessorLink_teacher}fragment SimilarProfessors_teacher on Teacher {  department  relatedTeachers {    legacyId    ...SimilarProfessorListItem_teacher    id  }}fragment TeacherRatingTabs_teacher on Teacher {  numRatings  courseCodes {    courseName    courseCount  }  ...RatingsList_teacher  ...RatingsFilter_teacher}fragment RatingsList_teacher on Teacher {  id  legacyId  lastName  numRatings  school {    id    legacyId    name    city    state    avgRating    numRatings  }  ...Rating_teacher  ...NoRatingsArea_teacher  ratings(first: 20) {    edges {      cursor      node {        ...Rating_rating        id        __typename      }    }    pageInfo {      hasNextPage      endCursor    }  }}fragment RatingsFilter_teacher on Teacher {  courseCodes {    courseCount    courseName  }}fragment Rating_teacher on Teacher {  ...RatingFooter_teacher  ...RatingSuperHeader_teacher  ...ProfessorNoteSection_teacher}fragment NoRatingsArea_teacher on Teacher {  lastName  ...RateTeacherLink_teacher}fragment Rating_rating on Rating {  comment  flagStatus  createdByUser  teacherNote {    id  }  ...RatingHeader_rating  ...RatingSuperHeader_rating  ...RatingValues_rating  ...CourseMeta_rating  ...RatingTags_rating  ...RatingFooter_rating  ...ProfessorNoteSection_rating}fragment RatingHeader_rating on Rating {  legacyId  date  class  helpfulRating  clarityRating  isForOnlineClass}fragment RatingSuperHeader_rating on Rating {  legacyId}fragment RatingValues_rating on Rating {  helpfulRating  clarityRating  difficultyRating}fragment CourseMeta_rating on Rating {  attendanceMandatory  wouldTakeAgain  grade  textbookUse  isForOnlineClass  isForCredit}fragment RatingTags_rating on Rating {  ratingTags}fragment RatingFooter_rating on Rating {  id  comment  adminReviewedAt  flagStatus  legacyId  thumbsUpTotal  thumbsDownTotal  thumbs {    thumbsUp    thumbsDown    computerId    id  }  teacherNote {    id  }  ...Thumbs_rating}fragment ProfessorNoteSection_rating on Rating {  teacherNote {    ...ProfessorNote_note    id  }  ...ProfessorNoteEditor_rating}fragment ProfessorNote_note on TeacherNotes {  comment  ...ProfessorNoteHeader_note  ...ProfessorNoteFooter_note}fragment ProfessorNoteEditor_rating on Rating {  id  legacyId  class  teacherNote {    id    teacherId    comment  }}fragment ProfessorNoteHeader_note on TeacherNotes {  createdAt  updatedAt}fragment ProfessorNoteFooter_note on TeacherNotes {  legacyId  flagStatus}fragment Thumbs_rating on Rating {  id  comment  adminReviewedAt  flagStatus  legacyId  thumbsUpTotal  thumbsDownTotal  thumbs {    computerId    thumbsUp    thumbsDown    id  }  teacherNote {    id  }}fragment RateTeacherLink_teacher on Teacher {  legacyId  numRatings  lockStatus}fragment RatingFooter_teacher on Teacher {  id  legacyId  lockStatus  isProfCurrentUser  ...Thumbs_teacher}fragment RatingSuperHeader_teacher on Teacher {  firstName  lastName  legacyId  school {    name    id  }}fragment ProfessorNoteSection_teacher on Teacher {  ...ProfessorNote_teacher  ...ProfessorNoteEditor_teacher}fragment ProfessorNote_teacher on Teacher {  ...ProfessorNoteHeader_teacher  ...ProfessorNoteFooter_teacher}fragment ProfessorNoteEditor_teacher on Teacher {  id}fragment ProfessorNoteHeader_teacher on Teacher {  lastName}fragment ProfessorNoteFooter_teacher on Teacher {  legacyId  isProfCurrentUser}fragment Thumbs_teacher on Teacher {  id  legacyId  lockStatus  isProfCurrentUser}fragment SimilarProfessorListItem_teacher on RelatedTeacher {  legacyId  firstName  lastName  avgRating}fragment RatingValue_teacher on Teacher {  avgRating  numRatings  ...NumRatingsLink_teacher}fragment NameTitle_teacher on Teacher {  id  firstName  lastName  department  school {    legacyId    name    id  }  ...TeacherDepartment_teacher  ...TeacherBookmark_teacher}fragment TeacherTags_teacher on Teacher {  lastName  teacherRatingTags {    legacyId    tagCount    tagName    id  }}fragment NameLink_teacher on Teacher {  isProfCurrentUser  id  legacyId  firstName  lastName  school {    name    id  }}fragment TeacherFeedback_teacher on Teacher {  numRatings  avgDifficulty  wouldTakeAgainPercent}fragment CompareProfessorLink_teacher on Teacher {  legacyId}fragment TeacherDepartment_teacher on Teacher {  department  departmentId  school {    legacyId    name    id  }}fragment TeacherBookmark_teacher on Teacher {  id  isSaved}fragment NumRatingsLink_teacher on Teacher {  numRatings  ...RateTeacherLink_teacher}fragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {  r1  r2  r3  r4  r5}fragment HeaderDescription_teacher on Teacher {  id  legacyId  firstName  lastName  department  school {    legacyId    name    city    state    id  }  ...TeacherTitles_teacher  ...TeacherBookmark_teacher  ...RateTeacherLink_teacher  ...CompareProfessorLink_teacher}fragment HeaderRateButton_teacher on Teacher {  ...RateTeacherLink_teacher  ...CompareProfessorLink_teacher}fragment TeacherTitles_teacher on Teacher {  department  school {    legacyId    name    id  }}
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
        details = extractTeacher(data["newID"])
        return {"rating": details["rating"], "total": details["numRatings"], "url": data["url"]}
    except:
        return {"rating": None, "total": None, "url": "/404"}