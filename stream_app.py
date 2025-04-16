import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent", layout="centered")
st.title("🧠 LangGraph Agent for Arxiv-Wikipedia-Tavily-OpenWeather")

# Initialize chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show last two messages
for sender, message in st.session_state.chat_history[-2:]:
    with st.chat_message(sender):
        st.markdown(message)

# Input box
query = st.text_input("Ask something...", key="input")

if query:
    # Get response from API
    try:
        res = requests.post("http://3.110.208.173:8000/query", json={"question": query})
        response = res.json().get("response", "No response.")
    except requests.exceptions.RequestException:
        response = "❌ Request failed."

    # Show response and update history
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("assistant", response))

    with st.chat_message("assistant"):
        st.markdown(response)
