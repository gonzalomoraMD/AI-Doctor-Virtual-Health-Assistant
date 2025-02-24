from fastapi import FastAPI
from backend.ai_doctor import get_doctor_response
from backend.voice import speech_to_text, text_to_speech

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Doctor is running!"}

@app.post("/chat")
def chat_with_doctor(user_input: str):
    response = get_doctor_response(user_input)
    return {"response": response}

@app.post("/voice")
def voice_chat():
    text = speech_to_text()
    response = get_doctor_response(text)
    text_to_speech(response)
    return {"response": response}
