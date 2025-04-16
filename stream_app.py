import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent", layout="centered")
st.title("🧠 LangGraph Agent for Research, Wikipedia, Live Weather update & Web Search")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input at the bottom like ChatGPT
with st.chat_message("user"):
    query = st.text_input("Ask something...", key="input", label_visibility="collapsed")

if query:
    # Display user message
    st.chat_message("user").markdown(query)

    with st.spinner("Thinking..."):
        try:
            res = requests.post("https://your-fastapi-app.onrender.com/query", json={"question": query})

            response = res.json().get("response", "No response")
        except Exception as e:
            response = f" Error: {str(e)}"

    # Save to chat history
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("assistant", response))

    # Display assistant response
    st.chat_message("assistant").markdown(response)

# Show previous chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
