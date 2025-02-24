from transformers import pipeline

def get_doctor_response(user_input):
    model = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
    response = model(f"Patient: {user_input}\nDoctor:", max_length=50, do_sample=True)
    return response[0]['generated_text']
