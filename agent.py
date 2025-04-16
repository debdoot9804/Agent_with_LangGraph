import os
from dotenv import load_dotenv

from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AnyMessage,AIMessage
from typing_extensions import TypedDict
from typing import Annotated

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# --- Tool Setup ---
arxiv = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500),
    description="Search research papers from Arxiv"
)

wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500),
    description="Search Wikipedia articles"
)

tavily = TavilySearchResults(
    api_key=TAVILY_API_KEY,
    description="Search the web using Tavily"
)

import os
import requests
from langchain_core.tools import tool



@tool
def get_weather(city: str) -> str:
    """Returns current weather for a city using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        if res.status_code != 200:
            return f" Couldn't fetch weather for '{city}'. Please check the city name."

        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]

        return f" Weather in {city}: {weather_desc}, {temp}°C (feels like {feels}°C)."
    
    except Exception as e:
        return f" Error fetching weather: {str(e)}"


tools = [arxiv, wikipedia, tavily,get_weather]

# --- LLM Setup ---
llm = ChatGroq(model="llama3-70b-8192", api_key=GROQ_API_KEY)
llm_with_tools = llm.bind_tools(tools)

# --- State Definition ---
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# --- Nodes ---
def assistant(state: State) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# --- LangGraph Setup ---
builder = StateGraph(State)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
builder.add_edge("assistant",END)

graph = builder.compile()

# --- Single call function for FastAPI ---
def ask_agent(user_query: str) -> str:
    input = {"messages": [HumanMessage(content=user_query)]}
    final_state = graph.invoke(input)
    return final_state["messages"][-1].content
