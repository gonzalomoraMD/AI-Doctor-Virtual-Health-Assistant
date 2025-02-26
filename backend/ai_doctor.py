from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import ollama
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_response(text):
    """Clean up the response to remove meta-commentary or internal reasoning."""
    # Check if the model is outputting its reasoning process
    if "**" in text or "I should" in text or "the user" in text.lower():
        # Try to identify and extract just the patient-facing response
        parts = text.split("I'll")
        if len(parts) > 1:
            return parts[-1].strip()
            
        # Look for the actual response after a thinking process
        matches = re.findall(r'(?:\.|\n\n)((?:[A-Z][^\.]*\.){2,})', text)
        if matches:
            return matches[-1].strip()
    
    return text

def get_doctor_response(conversation_history):
    """Generates a response as a doctor based on the chat history."""
    try:
        # Create a more natural doctor persona with specific instructions
        system_prompt = (
            "You are Dr. Thompson, a warm and experienced family physician with 15 years of clinical practice. "
            "Respond directly to the patient with a natural, conversational tone. Use medical terminology "
            "appropriate for patient communication, with occasional reassuring phrases like 'I understand' "
            "or 'I see'. Start conversations by establishing rapport and asking about symptoms. "
            "Follow up with specific questions about duration, severity, and related symptoms. "
            "Ask about the patient's age, weight, and medical history when relevant to their complaint. "
            "For mild conditions, offer clear advice and home remedies. For potentially serious issues, "
            "recommend appropriate medical attention while maintaining a calm tone. "
            "Avoid overly technical language but maintain medical accuracy and professionalism. "
            "DO NOT include ANY meta-commentary or reasoning about what you should say - speak directly "
            "as if you are having a face-to-face conversation with your patient."
        )
        
        # Create properly formatted messages for Ollama
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation_history:
            role = msg.get("role", "user")
            if role not in ["user", "assistant"]:
                role = "user" if role == "You" else "assistant"
            
            messages.append({
                "role": role,
                "content": msg.get("content", "")
            })
        
        logger.info(f"Sending request to Ollama with {len(messages)} messages")
        response = ollama.chat(model="deepseek-r1:1.5b", messages=messages)
        
        if "message" in response and "content" in response["message"]:
            raw_response = response["message"]["content"]
            # Clean up any meta-commentary if present
            cleaned_response = clean_response(raw_response)
            return cleaned_response
        else:
            logger.warning("Unexpected response format from Ollama")
            return "I'm sorry, I didn't quite catch that. Could you tell me more about what you're experiencing?"
    
    except Exception as e:
        logger.error(f"Error in get_doctor_response: {str(e)}")
        return "I apologize for the technical difficulties. Let's try again. How can I help you today?"

@app.post("/chat")
async def chat_with_doctor(chat_history: List[Dict[str, Any]]):
    try:
        if not isinstance(chat_history, list):
            raise HTTPException(status_code=400, detail="Invalid chat history format")
        
        logger.info(f"Received chat request with {len(chat_history)} messages")
        
        # Handle empty request (connection test)
        if len(chat_history) == 0:
            return {"response": "Connection test successful"}
        
        # For the first message, set a specific introduction if it doesn't exist
        if len(chat_history) == 0 or (len(chat_history) == 1 and chat_history[0]["role"] == "user"):
            return {"response": "Hello, I'm Dr. Thompson. How are you feeling today? Please tell me what symptoms you're experiencing."}
        
        response = get_doctor_response(chat_history)
        return {"response": response}
    
    except Exception as e:
        logger.error(f"Error in chat_with_doctor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Doctor backend server")
    uvicorn.run(app, host="127.0.0.1", port=8000)