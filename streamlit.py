import streamlit as st
import asyncio
import threading
import time
from typing import Dict, Any

# Add error handling for the import
try:
    from main import graph
    GRAPH_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Failed to import main.py: {e}")
    st.error("Make sure main.py exists and has no syntax errors")
    GRAPH_AVAILABLE = False
except Exception as e:
    st.error(f"❌ Error importing main.py: {e}")
    GRAPH_AVAILABLE = False

# Stop execution if import failed
if not GRAPH_AVAILABLE:
    st.error("Cannot proceed without main.py. Please fix the import error.")
    st.stop()

# Configure page
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333 !important;  /* Fix: Force dark text color */
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1565c0 !important;  /* Fix: Dark blue text */
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        color: #7b1fa2 !important;  /* Fix: Dark purple text */
    }
    
    .status-info {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 1rem 0;
        color: #e65100 !important;  /* Fix: Dark orange text */
    }
    
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: #212529 !important;  /* Fix: Dark text */
    }
    
    /* Fix: Override Streamlit's default text colors */
    .chat-message p, 
    .chat-message div, 
    .chat-message span {
        color: inherit !important;
    }
    
    /* Fix: Make sure strong tags are visible */
    .chat-message strong {
        color: #000000 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "research_history" not in st.session_state:
    st.session_state.research_history = []

# Sidebar
with st.sidebar:
    st.markdown("## 🔍 AI Research Agent")
    st.markdown("---")
    
    st.markdown("### 📊 Research Sources")
    st.markdown("""
    <div class="sidebar-info">
        <strong>🌐 Google Search</strong><br>
        Web results and knowledge panels
        <br><br>
        <strong>🔎 Bing Search</strong><br>
        Alternative web perspectives
        <br><br>
        <strong>💬 Reddit Analysis</strong><br>
        Community discussions and insights
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Settings")
    show_progress = st.checkbox("Show detailed progress", value=True)
    max_history = st.slider("Max chat history", 5, 50, 20)
    
    st.markdown("### 📈 Statistics")
    if st.session_state.research_history:
        st.metric("Total Researches", len(st.session_state.research_history))
        avg_time = sum([r.get("duration", 0) for r in st.session_state.research_history]) / len(st.session_state.research_history)
        st.metric("Avg Research Time", f"{avg_time:.1f}s")
    
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.session_state.research_history = []
        st.rerun()

# Main content
st.markdown('<h1 class="main-header">🔍 AI Research Agent</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="font-size: 1.2rem; color: #666;">
        Ask me anything and I'll research it using multiple sources including Google, Bing, and Reddit!
    </p>
</div>
""", unsafe_allow_html=True)

# Display chat history - Fix the HTML structure
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🧑 You:</strong><br>
                <span style="color: #1565c0 !important;">{message['content']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 AI Research Agent:</strong><br>
                <span style="color: #7b1fa2 !important;">{message['content']}</span>
            </div>
            """, unsafe_allow_html=True)

# Research function
def perform_research(question: str, progress_placeholder, status_placeholder):
    """Perform research using the graph"""
    start_time = time.time()
    
    try:
        # Create initial state
        state = {
            "messages": [{"role": "user", "content": question}],
            "user_question": question,
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
        
        if show_progress:
            # Show progress steps
            progress_steps = [
                "🌐 Searching Google...",
                "🔎 Searching Bing...", 
                "💬 Searching Reddit...",
                "🔍 Analyzing Reddit posts...",
                "📥 Retrieving detailed content...",
                "🧠 Analyzing Google results...",
                "🧠 Analyzing Bing results...",
                "🧠 Analyzing Reddit discussions...",
                "🎯 Synthesizing final answer..."
            ]
            
            for i, step in enumerate(progress_steps):
                progress_placeholder.progress((i + 1) / len(progress_steps))
                status_placeholder.markdown(f"""
                <div class="status-info">
                    <strong>{step}</strong>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.5)  # Simulate processing time
        
        # Execute the research
        progress_placeholder.progress(0.9)
        status_placeholder.markdown("""
        <div class="status-info">
            <strong>🎯 Generating comprehensive answer...</strong>
        </div>
        """, unsafe_allow_html=True)
        
        final_state = graph.invoke(state)
        
        # Complete progress
        progress_placeholder.progress(1.0)
        status_placeholder.markdown("""
        <div class="status-info">
            <strong>✅ Research completed successfully!</strong>
        </div>
        """, unsafe_allow_html=True)
        
        duration = time.time() - start_time
        
        # Store in history
        st.session_state.research_history.append({
            "question": question,
            "duration": duration,
            "timestamp": time.time()
        })
        
        return final_state["final_answer"], duration
        
    except Exception as e:
        progress_placeholder.progress(0.0)
        status_placeholder.error(f"❌ Research failed: {str(e)}")
        return f"I apologize, but I encountered an error while researching your question: {str(e)}", 0

# Chat input
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your question:",
            placeholder="e.g., What are the latest developments in AI?",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.form_submit_button("🔍 Research", use_container_width=True)

# Handle form submission
if submit_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Keep only recent messages
    if len(st.session_state.messages) > max_history * 2:
        st.session_state.messages = st.session_state.messages[-max_history * 2:]
    
    # Create placeholders for progress and status
    progress_placeholder = st.progress(0)
    status_placeholder = st.empty()
    
    # Perform research
    with st.spinner("🔍 Researching your question..."):
        answer, duration = perform_research(user_input, progress_placeholder, status_placeholder)
    
    # Clear progress indicators
    progress_placeholder.empty()
    status_placeholder.empty()
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Show completion message
    st.success(f"✅ Research completed in {duration:.1f} seconds!")
    
    # Rerun to update the chat display
    st.rerun()

# Example questions
if not st.session_state.messages:
    st.markdown("### 💡 Try these example questions:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Latest AI developments", use_container_width=True):
            st.session_state.example_question = "What are the latest developments in artificial intelligence?"
            st.rerun()
    
    with col2:
        if st.button("🌍 Climate change solutions", use_container_width=True):
            st.session_state.example_question = "What are the most promising solutions to climate change?"
            st.rerun()
    
    with col3:
        if st.button("💰 Investment trends", use_container_width=True):
            st.session_state.example_question = "What are the current investment trends in technology?"
            st.rerun()
    
    # Handle example questions
    if hasattr(st.session_state, 'example_question'):
        user_input = st.session_state.example_question
        del st.session_state.example_question
        
        # Add to messages and process
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        progress_placeholder = st.progress(0)
        status_placeholder = st.empty()
        
        with st.spinner("🔍 Researching your question..."):
            answer, duration = perform_research(user_input, progress_placeholder, status_placeholder)
        
        progress_placeholder.empty()
        status_placeholder.empty()
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.success(f"✅ Research completed in {duration:.1f} seconds!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>
        🔍 AI Research Agent | Powered by GPT-4o | 
        Sources: Google, Bing, Reddit
    </small>
</div>
""", unsafe_allow_html=True)









