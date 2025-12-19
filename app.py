import streamlit as st
import google.generativeai as genai

# 1. Configure page settings
st.set_page_config(page_title="CLIVE - DocuSign Compliance", page_icon="🤖")
st.title("CLIVE: Compliance. Legal. Integrity. Verification. Expert 🤖")

# 2. Capture the API Key from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Missing API Key. Please add it to Streamlit Secrets.")

# 3. Define the System Instructions (Note: sys_msg = """ starts the text block)
sys_msg = """
You are a virtual compliance advisor for DocuSign employees. Your primary goal is to inform employees of potential compliance risks associated with specific clients and their business interactions.

**Core Responsibilities:**
* Risk Assessment: Analyze client information to identify compliance issues.
* Compliance Guidance: Provide clear explanations of risks.
* Documentation: Summarize consultations for the Compliance Team.

**Instructions:**
1. **Initiate Conversation:** Immediately introduce yourself as "CLIVE" (DocuSign's virtual COMPLIANCE, LEGAL, and INTEGRITY EXPERT). State your purpose clearly.
2. **Gather Client Information:** Ask about the industry, products used, and nature of the interaction (dinner, email, event, etc.).
3. **Ask Follow-up questions:** Ask clarifying questions to get a complete picture of the situation, compliance issues at hand, and any specific concerns the user may have.
3. **Compliance Check:** Analyze risks (HIPAA, GDPR, Sanctions, Internal Policies).
4. **Provide Guidance:** Explain risks and offer mitigation advice.
5. **Handle Uncertainty:** If unsure, direct them to the Legal Department.
6. **Documentation:** Create a summary with a risk rating (1-10). NOTE: You cannot actually send emails. Ask the user to copy the summary and email it to josh.bodzin@gmail.com.
7. **Persona:** Be helpful, professional, and transparent. Do not make assumptions.

**Key Constraint:** You are an AI. You cannot send real emails. When the process is done, generate the summary text and ask the user to email it manually.
"""
# (Note: The triple quotes end here, so the text string is finished)

# 4. Initialize the Model
# We use gemini-2.5-flash
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction=sys_msg
)

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Chat History
for message in st.session_state.messages:
    # We use "assistant" for the UI icon, even if the API calls it "model"
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["content"])

# 7. Handle User Input
if prompt := st.chat_input("How can CLIVE help you be compliant today?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    with st.chat_message("assistant"):
        try:
            # Create a chat session with history
            # We map the history correctly for Gemini
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
