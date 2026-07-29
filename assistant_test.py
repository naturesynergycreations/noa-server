from assistant.assistant import Assistant

assistant = Assistant()

question, reply = assistant.process()

print("You :", question)
print("AI  :", reply)