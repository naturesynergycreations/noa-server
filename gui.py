import threading
import time

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout
)

from speech.speech_to_text import listen
from speech.text_to_speech import speak

from ai.router import ask
from emotion import detect_emotion
from utils.wake_word import is_wake_word, remove_wake_word
from utils.safety import check_question


class VoiceAssistant(QWidget):

    def __init__(self):
        super().__init__()

        # Prevent multiple assistant threads
        self.running = False

        # Wake word session
        self.awake = False
        self.last_activity = 0

        self.setWindowTitle("Noa AI Assistant")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Title
        self.title = QLabel("Noa AI Assistant")
        self.title.setStyleSheet("font-size:24px; font-weight:bold;")

        # Status
        self.status = QLabel("Status : Ready")

        # Chat Area
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        # Start Button
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_assistant)

        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.chat)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def start_assistant(self):

        # Prevent multiple threads
        if self.running:
            return

        self.running = True
        self.start_btn.setEnabled(False)

        thread = threading.Thread(target=self.run_assistant)
        thread.daemon = True
        thread.start()

    def run_assistant(self):

        while True:

            # ----------------------------
            # Listen
            # ----------------------------
            self.status.setText("Status : Listening...")

            question = listen()
            print("Heard:", question)

            if not question:
                continue

            # ----------------------------
            # Wake Word Detection
            # ----------------------------
            # Sleep after 30 seconds of inactivity
            if self.awake and time.time() - self.last_activity > 30:
                self.awake = False

            # Need wake word only if sleeping
            if not self.awake:

                if not is_wake_word(question):
                    continue

                self.awake = True

            question = remove_wake_word(question)

            # ----------------------------
            # Safety Check
            # ----------------------------
            status = check_question(question)

            if status == "restricted":

                emotion = "warning"

                reply = "Sorry, I cannot answer inappropriate questions."

                self.chat.append(f"You : {question}")
                self.chat.append(f"Noa : {reply}")
                self.chat.append(f"Emotion : {emotion}\n")

                self.status.setText("Status : Warning")

                speak(reply)

                continue


            if status == "long":

                emotion = "warning"

                reply = "Please ask one short question at a time."

                self.chat.append(f"You : {question}")
                self.chat.append(f"Noa : {reply}")
                self.chat.append(f"Emotion : {emotion}\n")

                self.status.setText("Status : Warning")

                speak(reply)

                continue


            if status == "long":

                reply = "Please ask one short question at a time."

                self.chat.append(f"You : {question}")
                self.chat.append(f"Noa : {reply}")
                self.chat.append("Emotion : warning\n")

                self.status.setText("Status : Warning")

                speak(reply)

                continue

            self.last_activity = time.time()

            # Only wake word spoken
            if question == "":

                reply = "Hello! I am Noa. How can I help you today?"

                self.chat.append("You : Hello Noa")
                self.chat.append(f"Noa : {reply}\n")

                self.status.setText("Status : Speaking...")

                speak(reply)

                self.last_activity = time.time()

                continue

            # ----------------------------
            # Show User Question
            # ----------------------------
            self.chat.append(f"You : {question}")

            # ----------------------------
            # AI Thinking
            # ----------------------------
            self.status.setText("Status : Thinking...")

            try:

                reply = ask(question)

                emotion = detect_emotion(reply)

                print("Emotion :", emotion)

                self.chat.append(f"Noa : {reply}")
                self.chat.append(f"Emotion : {emotion}\n")

                self.status.setText(
                    f"Status : {emotion.capitalize()}..."
                )

                speak(reply)

                self.status.setText("Status : Listening...")

            except Exception as e:

                print(e)

                error = "Sorry, I cannot answer right now."

                self.chat.append(f"Noa : {error}\n")

                self.status.setText("Status : Error")

                speak(error)

                self.status.setText("Status : Listening...")