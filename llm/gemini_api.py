# llm/gemini_api.py
from dotenv import load_dotenv
from config.gemini_config import get_model

load_dotenv()


model = get_model(model="gemini-2.5-flash")

def query_keywords(img_bgr, prompt=None):
    if prompt is None:
        prompt = ("What do you see in this picture? "
                  "Please answer only with the keywords. "
                  "If nothing is shown or unclear, answer 'None'.")

    # Convert OpenCV BGR → PIL Image
    from cv2 import cvtColor, COLOR_BGR2RGB
    from PIL import Image
    rgb = cvtColor(img_bgr, COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    response = model.generate_content([prompt, pil_img])
    return response.text
