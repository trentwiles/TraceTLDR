import main
from dotenv import load_dotenv
import db
import os

load_dotenv()

SKIP_MONGO = False
SKIP_GEMINI = False

# Step One: Auth
print("Step One: Auth")
auth = main.authHeaders(os.getenv("cookies"))

# Step Two: Harvest comment URLs
print("Step Two: Harvest comment URLs")
if not os.path.exists("data.csv"):
    courses = main.getEvalURLs(auth, 181, "CS")
else:
    print("data.csv already exists, skipping this step")

# Step Three: Read CSV with Comment URLs, and extract positive and negative comments
print("Step Three: Read CSV with Comment URLs, and extract positive and negative comments")
if not SKIP_MONGO:
    main.processEachComments("data.csv", auth)
else:
    print("Honored request to skip MongoDB adding")

# Step Four: Collect comments per professor, from mongo, then add them to allComments
print("Step Four: Collect comments per professor, from mongo, then add them to allComments")
if not SKIP_MONGO:
    for id in db.getTeachers():
        db.selectTeacher(id)
else:
    print("Honored request to skip MongoDB adding (2)")

# Step Five: Add Google Gemini Summary to MongoDB
print("Step Five: Add Google Gemini Summary to MongoDB")
if not SKIP_MONGO:
    for id in db.getTeachers():
        db.selectTeacherAllCommentsAndSummarize(id)
else:
    print("Honored request to skip Gemini")