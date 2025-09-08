from dotenv import load_dotenv
from typing import Annotated, List
from langgraph.graph import StateGraph, START, END 
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from webOperations import serp_search, reddit_search_api, reddit_post_retrieval
from prompts import (
     get_google_analysis_messages, 
     get_bing_analysis_messages, 
     get_reddit_analysis_messages, 
     get_synthesis_messages,
     get_reddit_url_analysis_messages
     )



load_dotenv()



llm = init_chat_model("gpt-4o")

class State(TypedDict):
    messages: Annotated[list, add_messages]
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


class RedditURLAnalysis(BaseModel):
    selected_reddit_urls: List[str] = Field( description="List of Reddit URLs that contain valuable information for answering the user's question")


def google_search(state: State) -> State:
    user_question = state.get("user_question", "")
    google_results = serp_search(user_question, engine="google")
    return {"google_results": google_results}

def bing_search(state: State) -> State:
    user_question = state.get("user_question", "")
    bing_results = serp_search(user_question, engine="bing")
    return {"bing_results": bing_results}

def reddit_search(state: State) -> State:
    user_question = state.get("user_question", "")
    reddit_results = reddit_search_api(user_question)
    return {"reddit_results": reddit_results}


def analyze_reddit_posts(state: State) -> State:
    user_question = state.get("user_question", "")
    reddit_results = state.get("reddit_results", "")

    if not reddit_results:
        return {"selected_reddit_urls": []}
    
    structured_llm = llm.with_structured_output(RedditURLAnalysis)
    messages = get_reddit_url_analysis_messages(user_question, reddit_results)

    try:
        analysis = structured_llm.invoke(messages)
        selected_urls = analysis.selected_reddit_urls
    except Exception as e:
        selected_urls = []

    return {"selected_reddit_urls": selected_urls}


def retrieve_reddit_posts(state: State) -> State:
    selected_urls = state.get("selected_reddit_urls", [])

    if not selected_urls:
        return {"reddit_post_data": []}
    
    reddit_post_data = reddit_post_retrieval(selected_urls)

    if not reddit_post_data:
        reddit_post_data = []
    
    return {"reddit_post_data": reddit_post_data}


def analyze_google_results(state: State) -> State:
    user_question = state.get("user_question", "")
    google_results = state.get("google_results", "")
    messages = get_google_analysis_messages(user_question, google_results)
    reply = llm.invoke(messages)
    return {"google_analysis": reply.content}


def analyze_bing_results(state: State) -> State:
    user_question = state.get("user_question", "")
    bing_results = state.get("bing_results", "")
    messages = get_bing_analysis_messages(user_question, bing_results)
    reply = llm.invoke(messages)
    return {"bing_analysis": reply.content}



def analyze_reddit_results(state: State) -> State:
    user_question = state.get("user_question", "")
    reddit_results = state.get("reddit_results", "")
    reddit_post_data = state.get("reddit_post_data", [])
    messages = get_reddit_analysis_messages(user_question, reddit_results, reddit_post_data)
    reply = llm.invoke(messages)
    return {"reddit_analysis": reply.content}


def synthesize_results(state: State) -> State:
    user_question = state.get("user_question", "")
    google_analysis = state.get("google_analysis", "")
    bing_analysis = state.get("bing_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    messages = get_synthesis_messages(user_question, google_analysis, bing_analysis, reddit_analysis)
    final_answer = llm.invoke(messages)
    
    return {
        "final_answer": final_answer.content,
        'messages': [{"role": "assistant", "content": final_answer.content}]
    }


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
graph_builder.add_edge("retrieve_reddit_posts", "analyze_bing_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_reddit_results")


graph_builder.add_edge("analyze_google_results", "synthesize_results")
graph_builder.add_edge("analyze_bing_results", "synthesize_results")
graph_builder.add_edge("analyze_reddit_results", "synthesize_results")


graph_builder.add_edge("synthesize_results", END)

graph = graph_builder.compile()


def run_chatbot():
    print("Welcome to the Multi-Source Chatbot!")
    print("Type exit to quit \n")

    while True:
        user_input = input("Ask me anything: ")
        if user_input.lower() == "exit": 
            print("Bye!")
            break 

        state = {
            "messages": [{"role": "user", "content": user_input}],
            "user_question": user_input,
            "google_results": None,
            "bing_results": None,
            "reddit_results": None,
            "selected_reddit_urls": None,
            "reddit_post_data": None,
            "google_analysis": None,
            "bing_analysis": None,
            "reddit_analysis": None,
            "final_answer": None
        }

        # Removed: All the progress messages
        print("\n🔍 Researching your question...")
        final_state = graph.invoke(state)

        if final_state["final_answer"]:
            print(f"\n{final_state['final_answer']}")  # Removed "Final Answer:" label
        
        print("-" * 80)



if __name__ == "__main__":
    run_chatbot()
