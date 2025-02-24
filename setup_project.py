import os

# Define project structure
project_structure = {
    "AI-Doctor-Virtual-Health-Assistant": [
        "backend",
        "frontend"
    ],
    "backend": [
        "ai_doctor.py",
        "main.py",
        "voice.py",
        "video_call.py"
    ],
    "frontend": [
        "app.py"
    ]
}

# Create folders and files
for folder, files in project_structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        open(os.path.join(folder, file), "w").close()

print("✅ Project structure created successfully!")
