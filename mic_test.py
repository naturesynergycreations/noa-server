from speech.speech_to_text import listen

while True:

    text = listen()

    print("\nYou said:", text)

    if text.lower() == "exit":
        break