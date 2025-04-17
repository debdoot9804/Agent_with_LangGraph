import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent", layout="centered")
st.title("🧠 LangGraph Agent for Research, Wikipedia, Weather & Web")

# Initialize chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display last 3 messages (if available)
for role, message in st.session_state.chat_history[-3:]:
    with st.chat_message(role):
        st.markdown(message)

# Input box at bottom
query = st.chat_input("Ask me anything...")

if query:
    # Show user message instantly
    st.chat_message("user").markdown(query)
    st.session_state.chat_history.append(("user", query))

    with st.spinner("Thinking..."):
        try:
            res = requests.post(
                "https://agent-with-langgraph.onrender.com/query",
                json={"question": query},
            )
            if res.headers.get("Content-Type", "").startswith("application/json"):
                data = res.json()
                response = data.get("response", "⚠️ No response found.")
            else:
                response = f"⚠️ Unexpected response:\n\n{res.text}"
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    # Show assistant message
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append(("assistant", response))
