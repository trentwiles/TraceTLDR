import db

for id in db.getTeachers():
    db.selectTeacher(id)
    
for id in db.getTeachers():
    db.selectTeacherAllComments(id)