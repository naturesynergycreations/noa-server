import json
import os

FILE_NAME = "memory.json"

# Load previous conversation
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        conversation_history = json.load(file)
else:
    conversation_history = []


def save_memory():
    with open(FILE_NAME, "w") as file:
        json.dump(conversation_history, file, indent=4)


def add_user_message(message):
    conversation_history.append({
        "role": "user",
        "parts": [{"text": message}]
    })
    save_memory()


def add_ai_message(message):
    conversation_history.append({
        "role": "model",
        "parts": [{"text": message}]
    })
    save_memory()


def get_history():
    return conversation_history