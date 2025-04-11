from memory.embedding_store import store_message, search_similar_messages

# Store some sample messages in the vector database
store_message("I love hiking!", "That's great! Nature is healing.", "happy")
store_message("I'm tired of everything", "I’m here for you. Want to talk?", "sad")
store_message("Music makes me feel alive", "It really lifts the spirit!", "joyful")

# Try to retrieve similar past messages
query = "Feeling low today"
results = search_similar_messages(query)

print(f"🔍 Top messages similar to: '{query}'\n")
for i, (user_input, response, emotion) in enumerate(results, start=1):
    print(f"{i}.")
    print(f"User said     : {user_input}")
    print(f"SoulMate.AGI  : {response}")
    print(f"Emotion       : {emotion}")
    print("-" * 30)
