from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os  # ✅ Add this to read from environment

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
    prompt = (
         f"You are a highly skilled astrologer and metaphysical branding guide known for your pinpoint accuracy and insightful, engaging style. "
         f"Deliver a detailed and personalized cosmic forecast using astrology, numerology, and the Chinese zodiac. "
         f"Blend spiritual depth with fun, modern language. Focus on revealing key personality traits, life path insights, detailed forecast for upcoming months, and unique energetic strengths based on:\n"
         f"- Full name: {data.first_name} {data.last_name}\n"
         f"- Date of birth: {data.birthday}\n\n"
         f"When calculating the Life Path Number through numerology, do not guess. Break down the full birthdate (MM/DD/YYYY) into individual digits, add them all together, and reduce the total to a single digit or master number (11, 22, 33) with clear steps. Accuracy is essential.\n\n"
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
