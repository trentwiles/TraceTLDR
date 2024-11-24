# google gemini integration
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

def summarize(commentType, comments):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"The following are a few {commentType} comments left by students, separed by commas, given these comments, provide five words describing their preformance, ONLY LIST THE LOWERCASE WORDS (separated by commas), nothing more: ${comments}")
    
    return response.text.strip()