from ai.groq_ai import ask_ai

while True:
    question = input("You : ")

    if question.lower() == "exit":
        break

    reply = ask_ai(question)

    print("AI :", reply)