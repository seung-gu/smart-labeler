from PIL import Image
from dotenv import load_dotenv
from config.gemini_config import get_model

load_dotenv()


model = get_model(model="gemini-2.0-flash")

img = Image.open("../images/test_image.png")

response = model.generate_content(
    ["What do you see in this picture? Please answer only with the keywords. "
     "If nothing is shown or unclear, answer 'None'", img]
)

print(response.text)
