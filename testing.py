import main
from dotenv import load_dotenv
import os

load_dotenv()

# Step One: Auth
auth = main.authHeaders(os.getenv("cookies"))

# Step Two: Harvest comment URLs
courses = main.getEvalURLs(auth, 181, "CS")

# Step Three: Read CSV with Comment URLs, and extract positive and negative comments
main.processEachComments("data.csv")

# Step Four: Collect comments per professor, from JSON or mongo or some shit

print(courses)