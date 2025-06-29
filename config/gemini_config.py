# config/gemini_config.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-2.5-flash"

# Configure Gemini globally
genai.configure(api_key=GEMINI_API_KEY)

def get_model(model=GEMINI_MODEL_NAME):
    return genai.GenerativeModel(model)
