import main
from dotenv import load_dotenv
import db
import os

load_dotenv()

# Step One: Auth
print("Step One: Auth")
auth = main.authHeaders(os.getenv("cookies"))

# Step Five: Add Google Gemini Summary to MongoDB
print("Step Five: Add Google Gemini Summary to MongoDB")
for id in db.getTeachers():
    db.selectTeacherAllCommentsAndSummarize(id)