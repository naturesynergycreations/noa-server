from memory.user_memory import remember, recall, get_all_memory

remember("name", "Harshini")
remember("education", "MCA")

print("Name:", recall("name"))
print("Education:", recall("education"))

print(get_all_memory())