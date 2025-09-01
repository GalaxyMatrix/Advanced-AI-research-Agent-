from dotenv import load_dotenv
from typing import Annotated, List
from langgraph.graph import StateGraph, START, END 
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


load_dotenv()

llm = init_chat_model("gpt-4o")

class State(TypedDict):
    messages: Annotated[dict, add_messages()]
    user_question: str | None 
    google_results: str | None
    bing_results: str | None
    reddit_results: str | None 
    selected_reddit_urls: List[str] | None
    reddit_post_data: List | None 
    google_analysis: str | None 
    bing_analysis: str | None
    reddit_analysis: str | None
    final_answer: str | None


def google_search(state: State) -> State:
    # Perform Google search and update state
    return 

def bing_search(state: State) -> State:
    # Perform Bing search and update state
    return

def reddit_search(state: State) -> State:
    # Perform Reddit search and update state
    return


def analyze_reddit_posts(state: State) -> State:
    # Analyze Reddit posts and update state
    return


def retrieve_reddit_posts(state: State) -> State:
    # Retrieve Reddit posts and update state
    return


def analyze_google_results(state: State) -> State:
    # Analyze Google search results and update state
    return


def analyze_bing_results(state: State) -> State:
    # Analyze Bing search results and update state
    return



def analyze_reddit_results(state: State) -> State:
    # Analyze Reddit search results and update state
    return


def synthesize_results(state: State) -> State:
    # Synthesize results from all sources and update state
    return


graph_builder = StateGraph(State)

graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)
graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
graph_builder.add_node("analyze_google_results", analyze_google_results)
graph_builder.add_node("analyze_bing_results", analyze_bing_results)
graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
graph_builder.add_node("synthesize_results", synthesize_results)


graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")

graph_builder.add_edge("google_search", "analyze_reddit_posts")
graph_builder.add_edge("bing_search", "analyze_reddit_posts")
graph_builder.add_edge("reddit_search", "analyze_reddit_posts")
graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_google_results")
