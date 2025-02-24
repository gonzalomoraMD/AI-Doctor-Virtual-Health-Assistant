import os

folders = [
    "backend", "frontend", "models", "data", "tests", "docs", "deployment"
]

files = {
    "backend/main.py": "# FastAPI backend",
    "backend/ai_doctor.py": "# GPT-4 AI doctor logic",
    "backend/speech_to_text.py": "# Whisper STT model",
    "backend/medicine.py": "# Medicine recommendation API",
    "backend/text_to_speech.py": "# Google TTS for doctor response",
    "backend/requirements.txt": "fastapi\nopenai\nwhisper\ngoogle-cloud-texttospeech\naiortc\nopencv-python\nrequests",
    "backend/Dockerfile": "FROM python:3.9\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD uvicorn main:app --host 0.0.0.0 --port 8000",
    "frontend/app.py": "# Streamlit UI",
    "frontend/avatar.py": "# AI doctor avatar integration",
    "frontend/utils.py": "# Helper functions",
    "models/whisper_model/": "",
    "models/fine_tuned_gpt/": "",
    "data/symptoms_dataset.csv": "Symptom,Possible Condition",
    "data/medicine_db.json": "{}",
    "tests/test_api.py": "# API tests",
    "tests/test_ai.py": "# AI response tests",
    "docs/README.md": "# AI Doctor Project",
    "docs/API_DOCS.md": "# API Documentation",
    "deployment/docker-compose.yml": "version: '3'\nservices:\n  backend:\n    build: ./backend",
    "deployment/cloud_run.sh": "# Deployment script",
    ".gitignore": "venv/\n*.pyc\n__pycache__/\n*.mp3",
    "README.md": "# AI Doctor - Virtual Healthcare Assistant\n\n## Setup Instructions\n```bash\npip install -r backend/requirements.txt\n```",
    "requirements.txt": "streamlit\nfastapi\nopenai\nwhisper\ngoogle-cloud-texttospeech\naiortc\nopencv-python\nrequests",
    "setup.py": "from setuptools import setup, find_packages\n\nsetup(name='ai_doctor', version='0.1', packages=find_packages())"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ Project structure created successfully!")
