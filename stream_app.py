import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent", layout="centered")
st.title("🧠 LangGraph + Groq Agent")

query = st.text_input("Ask something:")
if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/query", json={"question": query})
        st.write(res.json().get("response", "No response"))