import ratemyprofessor

def getRating(professor):

    print(professor)
    
    school = ratemyprofessor.get_school_by_name("Northeastern University")
    prof = ratemyprofessor.get_professor_by_school_and_name(school, professor) 
    
    return {"rating": prof.rating}