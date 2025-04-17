# 🧠 LangGraph Agent – Research, Web Search, Wikipedia & Weather Assistant

An intelligent assistant built with **LangGraph** and LLMs to help you:
- 📚 Explore research papers (Arxiv)
- 🌐 Search the web in real-time
- 🔍 Get Wikipedia summaries
- 🌦️ Fetch live weather updates

> **Live Demo:**  
> 🚀 Streamlit Frontend: [langgraph-agent-first.streamlit.app](https://langgraph-agent-first.streamlit.app/)  
> ⚙️ Backend: Hosted on **AWS EC2** using **FastAPI**

---

## 🛠️ Tech Stack

| Component    | Stack                            |
|--------------|----------------------------------|
| Frontend     | Streamlit                        |
| Backend      | FastAPI, LangGraph, Uvicorn      |
| Deployment   | AWS EC2 (Backend), Streamlit Cloud (Frontend) |
| Extras       | Requests, tmux, Linux (Ubuntu)   |

---

⚙️ Deployment Notes
✅ FastAPI on EC2
Deployed on AWS EC2 Ubuntu instance

Kept running with tmux so it stays alive even after SSH disconnect

Accessible at: (http://3.110.208.173:8000/docs)

✅ Streamlit App
Hosted via Streamlit Cloud

Communicates with EC2 backend through requests.post()

![image](https://github.com/user-attachments/assets/9ab62a2d-c7d3-48f8-8af7-8d7f0ebe0455)


