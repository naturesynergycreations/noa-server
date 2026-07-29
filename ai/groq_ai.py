from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Simple memory for current conversation
messages = [
    {
        "role": "system",
        "content": (
            "Your name is Noa. "
            "You are Noa, a friendly AI voice assistant built for students. "
            "Whenever someone asks your name, always reply 'My name is Noa.' "
            "Accept both 'Noa' and 'Noah' as referring to you. "
            "Never correct the user's pronunciation or spelling if they say 'Noah'. "
            "Never say your name is Assistant, AI, ChatGPT, Groq or anything else. "
            "Answer in simple English. "
            "Keep answers short unless the user asks for details. "
            "Be polite and conversational."
        ),
    }
]

def ask_ai(question):
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=300,
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})

    return reply

def summarize_search(search_text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly AI assistant. "
                    "Summarize the given search results in simple English. "
                    "Give only the important points. "
                    "Keep the answer under 100 words. "
                    "Do not include advertisements, links, or unnecessary details."
                )
            },
            {
                "role": "user",
                "content": search_text
            }
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content