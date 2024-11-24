import ratemyprofessor

def getNEU():
    return ratemyprofessor.get_school_by_name("Northeastern University")

def getRating(school, professor):
    
    prof = ratemyprofessor.get_professor_by_school_and_name(school, professor) 
    
    try:
        url = "https://www.ratemyprofessors.com/professor/" + str(prof.id)
        return {"rating": prof.rating, "total": prof.num_ratings, "url": url}
    except:
        return {"rating": None, "total": None, "url": url}