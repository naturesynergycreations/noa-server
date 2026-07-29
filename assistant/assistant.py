from speech.speech_to_text import listen
from ai.groq_ai import ask_ai
from speech.text_to_speech import speak


class Assistant:

    def process(self):

        question = listen()

        if not question:
            return None, None

        reply = ask_ai(question)

        speak(reply)

        return question, reply