from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ENV setup
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

class UserInput(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    email: str

@app.post("/generate")
async def generate_reading(data: UserInput):
    prompt = (
        f"Give a fun but insightful astrology + numerology + Chinese zodiac cosmic reading for:\n"
        f"Name: {data.first_name} {data.last_name}\n"
        f"Birthday: {data.birthday}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response['choices'][0]['message']['content']
    return {"result": result}
