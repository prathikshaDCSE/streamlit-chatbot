import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("groq_api_key")

# Load external CSS
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar for personalization
st.sidebar.title("🛠 Personalization", anchor="personalization")
st.sidebar.markdown("<div class='sidebar-subtitle'>Configure your settings below:</div>", unsafe_allow_html=True)

system_prompt = st.sidebar.text_area("System Prompt", placeholder="Enter a system prompt...")
model = st.sidebar.selectbox(
    "Choose a model",
    ['Llama3-8b-8192', 'Llama3-70b-8192', 'Mixtral-8x7b-32768', 'Gemma-7b-It'],
)

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Main Interface
st.title("🗪 Chat Assistant")
st.markdown(
    """
    Welcome! Enter your query below, and let the AI assist you. Adjust settings from the sidebar to customize your experience.
    """
)

# Load custom CSS
load_css("styles.css")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Enter your question:", "")

# Handle Submit button
if st.button("Submit"):
    if user_input.strip():
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": user_input}],
                model=model,
            )
            response = chat_completion.choices[0].message.content
            st.session_state.history.append({"query": user_input, "response": response})

            # Display the response
            st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a query before submitting!")

# Display history in an accordion format
st.sidebar.title("📜 History")
for i, entry in enumerate(st.session_state.history):
    with st.sidebar.expander(f"Query {i+1}: {entry['query']}"):
        st.markdown(f"**Response:** {entry['response']}")
