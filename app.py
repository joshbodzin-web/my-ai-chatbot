import streamlit as st
import google.generativeai as genai

# 1. Configure page settings
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("My AI Chatbot 🤖")

# 2. Capture the API Key from Streamlit Secrets (for security)
# This handles the connection to Google.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Missing API Key. Please add it to Streamlit Secrets.")

# 3. Initialize the Model (Use the model name you used in AI Studio)
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. Initialize Chat History (so the bot remembers the conversation)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle User Input
if prompt := st.chat_input("What is up?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    with st.chat_message("assistant"):
        try:
            # Create a chat session with history
            history = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ]
            chat = model.start_chat(history=history)
            
            # Send message to Google
            response = chat.send_message(prompt)
            st.markdown(response.text)
            
            # Save AI response to history
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
