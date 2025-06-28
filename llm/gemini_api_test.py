import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

img = Image.open("test_image.png")

response = model.generate_content(
    ["What do you see in this picture? Please answer only with the keywords. "
     "If nothing is shown or unclear, answer 'None'", img]
)

print(response.text)
