import os
from dotenv import load_dotenv
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq

load_dotenv()

# Environment variabless
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Tool 1: Arxiv
arxiv = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500),
    description="Search for research papers on Arxiv"
)

# Tool 2: Wikipedia
wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500),
    description="Search Wikipedia for general information"
)

# Tool 3: Tavily
tavily = TavilySearchResults(
    api_key=TAVILY_API_KEY,
    description="Search the web using Tavily"
)

# Combine tools
tools = [arxiv, wikipedia, tavily]

# Groq LLM
llm = ChatGroq(model="llama3-70b-8192", api_key=GROQ_API_KEY)
llm_with_tools = llm.bind_tools(tools)

def ask_agent(query: str) -> str:
    return llm_with_tools.invoke(query).content
