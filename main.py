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
        f"You are a gifted astrologer, numerologist, and metaphysical branding expert renowned for delivering scarily accurate, soul-stirring cosmic readings that feel uncannily personal and profound. "
    f"Your style combines spiritual depth, poetic insight, psychological precision, and cosmic wisdom. "
    f"Craft a full personalized cosmic report for the user, drawing from Western astrology (Sun sign only — use precise zodiac date ranges and make sure you are correct when choosing the astrology symbol and double check to make sure you are correct with exact dates for the sign), numerology (Life Path Number, Pinnacle Cycles, Expression Number), and the Chinese Zodiac. "
    f"Speak with grounded confidence and mystical allure—your words should feel like an awakening.\n\n"
    
    f"Include the following sections:\n\n"
    
    f"1. **Soul Signature: Personality Portrait** — Open with a compelling summary of the user's most defining personality traits based on their full name and birthdate. Reveal deep patterns, emotional tendencies, strengths, and shadow sides. Make it feel eerily accurate, intimate, and empowering.\n\n"
    
    f"2. **Numerology Blueprint** — Analyze strictly from {data.birthday} and the full name {data.first_name} {data.last_name}:\n"
    f"   - Calculate the **Life Path Number** by breaking down the birthdate into individual digits (month, day, year). Reduce to a single digit or master number (11, 22, 33). Show each step exactly once.\n"
    f"   - Calculate the **Expression Number** using the Pythagorean system for each letter of the full name. Add, reduce, and interpret clearly—no re-stating or contradiction.\n"
    f"   - Determine and describe the **current Pinnacle Cycle** and what it reveals about this period of their life.\n\n"
    
    f"3. **Celestial Animal Wisdom** — Describe the user’s Chinese Zodiac sign with personality insights and how it blends with their Western Sun sign. Highlight rare traits, internal conflicts, or superpowers from this fusion.\n\n"
    
    f"4. **3-Month Forecast: Your Cosmic Weather** — Provide an emotionally intelligent, scarily accurate month-by-month forecast for the next 3 months starting from {current_date}. Include predictions and symbolic themes for:\n"
    f"   - **Love**: One message for singles, one for those in a relationship.\n"
    f"   - **Career & Calling**: Show them what they’re building or should be focused on.\n"
    f"   - **Personal Growth**: Deliver insights that inspire action, reflection, or change.\n"
    f"   Go into exquisite detail. Channel intuition. Leave the reader feeling seen and stirred.\n\n"
    
    f"5. **Final Insight & Empowerment** — End with heartfelt guidance that anchors the reading. Offer spiritual advice and tell them what their higher self is guiding them toward right now. Close like a trusted oracle passing a torch.\n\n"

    f"- Full name: {data.first_name} {data.last_name}\n"
    f"- Date of birth: {data.birthday}\n"
    f"The current date is {current_date}. Use this as your starting point.\n\n"

    f"Speak like a wise, magical guide with lyrical warmth. Make every word shimmer with purpose and soul-level truth."
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
