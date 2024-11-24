from dotenv import load_dotenv
import os
import main

load_dotenv()

auth = main.authHeaders(os.getenv("cookies"))
colleges = main.getInternalColleges(auth)

print(main.getEvalURLs(auth, 181, colleges))