from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import ask_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "LangGraph Groq Agent API is running"}

@app.post("/query")
async def query_agent(request: Request):
    data = await request.json()
    question = data.get("question", "")
    result = ask_agent(question)
    return {"response": result}






