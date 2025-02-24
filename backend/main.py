from fastapi import FastAPI
from pydantic import BaseModel
from ai_doctor import get_doctor_response

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str  # Expect user input as JSON

@app.get("/")
def home():
    return {"message": "AI Doctor API is Running!"}

@app.post("/chat/")
def chat_with_doctor(request: ChatRequest):
    response = get_doctor_response(request.user_input)
    return {"doctor_response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
