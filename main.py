from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
from pydantic import BaseModel

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key setup
OPENAI_API_KEY = "your-openai-api-key"
openai.api_key = OPENAI_API_KEY

# Request body model
class UserInput(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    email: str  # still collected but unused

# Route to generate reading
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

    result = response["choices"][0]["message"]["content"]
    return {"result": result}
