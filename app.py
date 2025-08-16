import streamlit as st

# Define your password (for local testing)
PASSWORD = "mypassword"  # change this to whatever you want

# Ask user for password
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    user_pass = st.text_input("Enter password to access AI Agent:", type="password")
    if user_pass == PASSWORD:
        st.session_state.auth = True
        st.success("Access granted ✅")
    elif user_pass:
        st.error("Incorrect password ❌")
    st.stop()  # stop the app until correct password




import streamlit as st
from prompt import firePrompt
import os, json, time

os.environ["BROWSER"] = "none"

st.set_page_config(page_title='Memory AI Agent', page_icon='🤖')

# Load previous messages
if 'messages' not in st.session_state:
    try:
        with open("memory.json", "r", encoding="utf-8") as f:
            st.session_state.messages = json.load(f)
    except:
        st.session_state.messages = []

# Default temperature
if 'temp' not in st.session_state:
    st.session_state.temp = 0.3

# Sidebar for temperature
st.sidebar.slider('Temperature', 0.0, 1.0, 0.3, 0.1, key='temp')

# Page header
st.markdown('# Memory AI Assistant 🤖')

# Display chat history
for msg in st.session_state.messages:
    role = msg["role"]
    st.markdown(f"**{role.capitalize()}:** {msg['content']}")

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"**You:** {prompt}")

    # Display AI response with "typing" effect
    message_placeholder = st.empty()
    full_response = ""

    try:
        ai_response = firePrompt(prompt, temp=st.session_state.temp)
        for word in ai_response.split():
            full_response += word + " "
            message_placeholder.markdown(f"**Assistant:** {full_response}▌")
            time.sleep(0.05)  # adjust speed of typing here
        message_placeholder.markdown(f"**Assistant:** {full_response}")  # final message
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except:
        message_placeholder.markdown("**Assistant:** Error generating response.")

# Save memory
with open("memory.json", "w", encoding="utf-8") as f:
    json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
