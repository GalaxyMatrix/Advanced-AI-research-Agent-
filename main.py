from dotenv import load_dotenv
import os
import concurrent.futures
import time
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

# API key setup
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Use faster models for analysis, keep GPT-4 for synthesis
fast_llm = init_chat_model("gpt-4o-mini", api_key=api_key)  # 3x faster, 15x cheaper
main_llm = init_chat_model("gpt-4o", api_key=api_key)       # For final synthesis

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
    selected_reddit_urls: List[str] = Field(description="List of Reddit URLs that contain valuable information for answering the user's question")

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
    
    structured_llm = fast_llm.with_structured_output(RedditURLAnalysis)  # Use fast model
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

# 🚀 OPTIMIZED: Parallel Analysis Function
def fast_parallel_analysis(state: State) -> State:
    """Run all analysis tasks in parallel - 3x speed improvement"""
    
    def analyze_google():
        user_question = state.get("user_question", "")
        google_results = state.get("google_results", "")
        if not google_results:
            return ("google_analysis", "No Google results available")
        messages = get_google_analysis_messages(user_question, google_results)
        reply = fast_llm.invoke(messages)  # Use fast model
        return ("google_analysis", reply.content)
    
    def analyze_bing():
        user_question = state.get("user_question", "")
        bing_results = state.get("bing_results", "")
        if not bing_results:
            return ("bing_analysis", "No Bing results available")
        messages = get_bing_analysis_messages(user_question, bing_results)
        reply = fast_llm.invoke(messages)  # Use fast model
        return ("bing_analysis", reply.content)
    
    def analyze_reddit():
        user_question = state.get("user_question", "")
        reddit_results = state.get("reddit_results", "")
        reddit_post_data = state.get("reddit_post_data", [])
        if not reddit_results and not reddit_post_data:
            return ("reddit_analysis", "No Reddit results available")
        messages = get_reddit_analysis_messages(user_question, reddit_results, reddit_post_data)
        reply = fast_llm.invoke(messages)  # Use fast model
        return ("reddit_analysis", reply.content)
    
    # 🚀 Run all analysis in parallel
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(analyze_google),
            executor.submit(analyze_bing),
            executor.submit(analyze_reddit)
        ]
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                key, value = future.result()
                results[key] = value
            except Exception as e:
                print(f"Analysis error: {e}")
    
    analysis_time = time.time() - start_time
    print(f"⚡ Parallel analysis completed in {analysis_time:.1f}s")
    
    return results

# 🚀 OPTIMIZED: Streaming Synthesis
def synthesize_results_fast(state: State) -> State:
    """Fast synthesis with streaming response"""
    user_question = state.get("user_question", "")
    google_analysis = state.get("google_analysis", "")
    bing_analysis = state.get("bing_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    start_time = time.time()
    messages = get_synthesis_messages(user_question, google_analysis, bing_analysis, reddit_analysis)
    
    # Use streaming for faster perceived response
    final_answer_parts = []
    try:
        for chunk in main_llm.stream(messages):  # Use streaming
            if hasattr(chunk, 'content') and chunk.content:
                final_answer_parts.append(chunk.content)
        
        final_answer = ''.join(final_answer_parts)
    except Exception as e:
        # Fallback to regular invoke if streaming fails
        final_answer_response = main_llm.invoke(messages)
        final_answer = final_answer_response.content
    
    synthesis_time = time.time() - start_time
    print(f"🎯 Synthesis completed in {synthesis_time:.1f}s")
    
    return {
        "final_answer": final_answer,
        'messages': [{"role": "assistant", "content": final_answer}]
    }

# 🚀 OPTIMIZED: Build faster graph
graph_builder = StateGraph(State)

# Search nodes (parallel from start)
graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)

# Reddit processing
graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)

# 🚀 NEW: Single parallel analysis node instead of 3 sequential ones
graph_builder.add_node("fast_parallel_analysis", fast_parallel_analysis)

# 🚀 NEW: Fast streaming synthesis
graph_builder.add_node("synthesize_results_fast", synthesize_results_fast)

# Edges - optimized flow
graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")

graph_builder.add_edge("google_search", "analyze_reddit_posts")
graph_builder.add_edge("bing_search", "analyze_reddit_posts")
graph_builder.add_edge("reddit_search", "analyze_reddit_posts")
graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")

# 🚀 NEW: Direct to parallel analysis
graph_builder.add_edge("retrieve_reddit_posts", "fast_parallel_analysis")

# 🚀 NEW: Direct to fast synthesis
graph_builder.add_edge("fast_parallel_analysis", "synthesize_results_fast")
graph_builder.add_edge("synthesize_results_fast", END)

graph = graph_builder.compile()

def run_chatbot():
    print("Welcome to the Multi-Source Chatbot! ⚡ OPTIMIZED VERSION")
    print("Type exit to quit \n")

    research_times = []  # Track performance

    while True:
        user_input = input("Ask me anything: ")
        if user_input.lower() == "exit": 
            if research_times:
                avg_time = sum(research_times) / len(research_times)
                print(f"\n📊 Average research time: {avg_time:.1f}s")
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

        print("\n🔍 Researching your question...")
        start_time = time.time()
        
        try:
            final_state = graph.invoke(state)
            total_time = time.time() - start_time
            research_times.append(total_time)
            
            print(f"\n⚡ Research completed in {total_time:.1f}s")
            
            if final_state["final_answer"]:
                print(f"\n{final_state['final_answer']}")
            else:
                print("\n❌ No answer generated")
                
        except Exception as e:
            print(f"\n❌ Research failed: {e}")
        
        print("-" * 80)

if __name__ == "__main__":
    run_chatbot()
