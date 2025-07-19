from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os  # ✅ Add this to read from environment
from datetime import datetime

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI setup (read key from environment)
openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ Safe and clean

class UserInput(BaseModel):
    first_name: str
    last_name: str
    birthday: str

@app.post("/generate")
async def generate_reading(data: UserInput):
    current_date = datetime.now().strftime("%B %d, %Y")
    prompt = (
         f"You are a gifted astrologer, numerologist, and metaphysical branding expert known for delivering scarily accurate cosmic readings that feel deeply personal and insightful. "
         f"Your style is a mix of spiritual depth, psychological precision, and poetic flair. "
         f"Provide a full personalized cosmic report for the user using Western astrology (Sun, Moon, and rising signs), numerology (including Life Path Number, Pinnacle Cycles, and Expression Number), and the Chinese Zodiac. "
         f"Speak with grounded confidence, balancing mysticism and practicality. Include:\n\n"
         f"1. A compelling summary of key personality traits based on name and birthdate.\n"
         f"2. A numerology analysis that strictly shows calculations based on {data.birthday} and the full name {data.first_name} {data.last_name}. Start with the Life Path Number—break down the birthdate into individual digits, add them, and reduce to a single digit or master number (11, 22, 33), showing each step once. Then calculate the Expression/Destiny Number using Pythagorean values for each letter. Conclude with the current Pinnacle Cycle, if possible. Do not recalculate or restate values after you finish the breakdown.\n"
         f"3. A Chinese Zodiac breakdown with animal sign traits and how they combine with Western signs.\n"
         f"4. A detailed month-by-month forecast for the next 3 months starting from {current_date}, covering Love, Career, and Personal Growth.\n"
         f"5. Finish with empowering, heartfelt closing guidance that encourages the user to embrace their unique gifts.\n\n"
         f"- Full name: {data.first_name} {data.last_name}\n"
         f"- Date of birth: {data.birthday}\n\n"
         f"The current date is {current_date}. Use this as your starting point. "
         f"Speak with both precision and flair—like a wise, intuitive guide who also knows how to make it feel magical and exciting."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        result = response["choices"][0]["message"]["content"]
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}
