import main
from dotenv import load_dotenv
import os

load_dotenv()


auth = main.authHeaders(os.getenv("cookies"))

main.processEachComments('data.csv', auth)