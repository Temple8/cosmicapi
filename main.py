from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI setup
openai.api_key = "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"

class UserInput(BaseModel):
    first_name: str
    last_name: str
    birthday: str

@app.post("/generate")
async def generate_reading(data: UserInput):
    prompt = (
        f"Give a fun but insightful astrology + numerology + Chinese zodiac cosmic reading for:\n"
        f"Name: {data.first_name} {data.last_name}\n"
        f"Birthday: {data.birthday}"
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
