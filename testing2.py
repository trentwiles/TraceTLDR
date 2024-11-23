import main
from dotenv import load_dotenv
import db
import os

load_dotenv()

# Step One: Auth
print("Step One: Auth")
auth = main.authHeaders(os.getenv("cookies"))


# Step Three: Read CSV with Comment URLs, and extract positive and negative comments
print("Step Three: Read CSV with Comment URLs, and extract positive and negative comments")
main.processEachComments("data.csv", auth)

# Step Four: Collect comments per professor, from mongo, then add them to allComments
print("Step Four: Collect comments per professor, from mongo, then add them to allComments")
for id in db.getTeachers():
    db.selectTeacher(id)

# Step Five: Add Google Gemini Summary to MongoDB
print("Step Five: Add Google Gemini Summary to MongoDB")
for id in db.getTeachers():
    db.selectTeacherAllCommentsAndSummarize(id)