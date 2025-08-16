# prompt.py
import json
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT = """
You are a helpful and honest AI assistant.
Always remember the previous conversations stored in memory.
"""

MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_memory(messages):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def firePrompt(prompt: str, temp=0.4) -> str:
    memory_messages = load_memory()
    
    # Prepare messages for the model
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in memory_messages:
        role = m["role"]
        content = m["content"]
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))  # For Ollama we treat assistant output as HumanMessage too

    # Add current user input
    messages.append(HumanMessage(content=prompt))
    
    # Call the LLM
    chat = ChatOllama(model="gemma2:2b", temperature=temp)
    res = chat.invoke(messages)
    
    # Update memory and save
    memory_messages.append({"role": "user", "content": prompt})
    memory_messages.append({"role": "assistant", "content": res.content})
    save_memory(memory_messages)
    
    return res.content
