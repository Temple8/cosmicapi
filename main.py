from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

from pydantic import BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ENV setup (in real deployment, use os.environ or secrets manager)
OPENAI_API_KEY = "your-openai-api-key"
EMAIL_FROM = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password"

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

    # Email result
    conf = ConnectionConfig(
        MAIL_USERNAME=EMAIL_FROM,
        MAIL_PASSWORD=EMAIL_PASSWORD,
        MAIL_FROM=EMAIL_FROM,
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True
    )

    message = MessageSchema(
        subject="Your Cosmic Reading ✨",
        recipients=[data.email],
        body=result,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    return {"result": result}
