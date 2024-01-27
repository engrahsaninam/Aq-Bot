import streamlit as st
import os
import google.generativeai as genai
# from dotenv import load_dotenv

def extract_subtext(text):
    start_marker = "[["
    end_marker = "]]"
    
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index != -1 and end_index != -1 and start_index < end_index:
        subtext = text[start_index + len(start_marker):end_index]
        return subtext
    else:
        return None


# load_dotenv()
st.set_page_config(
    page_title="Welcome To AQ Institute",
    page_icon=":robot_face:",
    layout="wide",
)

# Initialize Gemini-Pro
genai.configure(api_key='AIzaSyA7pwwY9mUN_XrDGihJNeA1QSgEg2lvUDc')
model = genai.GenerativeModel("gemini-pro")

def role_to_streamlit(role):
    return "assistant" if role == "model" else role

# Store only prompt messages in chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("Welcome To AQ Institute")

# Display prompt messages from history
for message in st.session_state.chat.history:
    if message.role == "user":
        prompt_text = extract_subtext(message.parts[0].text)  # Extract prompt from first line
        with st.chat_message("user"):
            st.markdown(prompt_text)
    else:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

if prompt := st.chat_input("I'm here to help with your cybersecurity questions. Ask away!"):
    # Display only the prompt
    st.chat_message("user").markdown(prompt.splitlines()[0])

    tailored_prompt = f"""
    **Context:** Acting as a representative of cybersecurity academy, answering a cybersecurity question for a potential student at my academy.
    **Query:** [[{prompt}]]
    **Desired tone:** Human-like, concise, and precise.
    **Additional requirements:**
    - Use welcoming tone and show some courtesy
    - Don't explain the answer, just give the answer.
    - If the user asks who are you, tell you are a representative of AQ Institute, otherwise don't.
    - If the user expresses interest in cybersecurity, recommend joining my academy, otherwise don't.
    - If the user asks for a cybersecurity roadmap, provide one, otherwise don't.
    - If the user says hey or hello, greet him, otherwise don't.
    """

    response = st.session_state.chat.send_message(tailored_prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)
