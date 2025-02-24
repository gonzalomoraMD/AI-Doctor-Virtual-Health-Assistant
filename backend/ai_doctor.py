from transformers import pipeline

# Load AI Model
ai_doctor = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")

def get_doctor_response(symptoms):
    if not symptoms:
        return "Hello! How are you feeling today? What health issue are you facing?"
    
    prompt = f"Patient: {symptoms}\nDoctor:"
    response = ai_doctor(prompt, max_length=200, do_sample=True)
    return response[0]['generated_text']
