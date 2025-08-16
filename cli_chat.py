# cli_chat.py
from prompt import firePrompt, load_memory, save_memory

def main():
    print("Memory AI Agent (Type 'exit' to quit)\n")

    # Load memory
    memory_messages = load_memory()

    # Show previous conversation
    if memory_messages:
        print("=== Previous Chat History ===")
        for m in memory_messages:
            role = "You" if m["role"] == "user" else "Assistant"
            print(f"{role}: {m['content']}")
        print("============================\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting... Goodbye!")
            break

        # Get AI response
        response = firePrompt(user_input)
        print(f"Assistant: {response}\n")

