import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent", layout="centered")
st.title("🧠 LangGraph Agent for Research, Wikipedia, Live Weather update & Web Search")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box (ChatGPT style)
with st.chat_message("user"):
    query = st.text_input("Ask something...", key="input", label_visibility="collapsed")

if query:
    
    
    with st.spinner("Thinking..."):
        try:
            # 🔁 Send POST request to FastAPI
            res = requests.post(
                "https://agent-with-langgraph.onrender.com/query",
                json={"question": query},
                
            )

            # ✅ Handle JSON or error fallback
            if res.headers.get("Content-Type", "").startswith("application/json"):
                data = res.json()
                response = data.get("response", "⚠️ No response found.")
            else:
                response = f"⚠️ Unexpected response:\n\n{res.text}"

        except requests.exceptions.RequestException as e:
            response = f"❌ Request failed: {str(e)}"
        except ValueError:
            response = f"❌ Invalid JSON returned:\n\n{res.text}"
        st.markdown(response)  

    # Add both user and assistant messages to history
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("assistant", response))

