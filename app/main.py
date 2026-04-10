import streamlit as st
import os
import sys

# Add parent directory to path so we can import services module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.qa_service import (
    ask_question,
    summarize_emails,
    generate_draft_reply,
    organize_threads,
    suggest_inbox_rules,
    extract_meeting_details
)

# Import utility functions
from utils import (
    safe_execute,
    with_spinner,
    primary_button,
    show_success,
    show_info,
    update_context,
    add_chat_exchange
)

# Page configuration
st.set_page_config(
    page_title="Gmail Email Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'email_context' not in st.session_state:
    st.session_state.email_context = {
        'emails': ['email_1', 'email_2', 'email_3'],
        'metadata': {'project': 'Q1 Planning', 'date_range': 'last_week'}
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("📧 Gmail Assistant")
    st.markdown("---")

    feature = st.selectbox(
        "Choose a feature",
        [
            "💬 Conversational Q&A",
            "📝 Email Summarization",
            "✉️ Draft Reply Generator",
            "🧵 Thread Organization",
            "🏷️ Smart Inbox Rules",
            "📅 Meeting Scheduler"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    if primary_button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main content
st.markdown('<p class="main-header">📧 Gmail Email Assistant</p>', unsafe_allow_html=True)
st.markdown("Your AI-powered email assistant for smarter inbox management.")

# Feature: Conversational Q&A
if feature == "💬 Conversational Q&A":
    st.markdown("### 💬 Ask Questions About Your Emails")
    st.markdown("Get intelligent answers grounded in your email context.")

    col1, col2 = st.columns([3, 1])
    with col1:
        user_query = st.text_input(
            "Ask anything about your emails:",
            placeholder="What did Sarah say about the budget?",
            label_visibility="collapsed"
        )
    with col2:
        submit_btn = primary_button("Ask")

    if submit_btn and user_query:
        response = with_spinner("Analyzing your emails...", ask_question, user_query, st.session_state.email_context)
        if response is not None:
            add_chat_exchange(user_query, response)

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation")
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Assistant:** {msg['content']}")
            st.markdown("---")

# Feature: Email Summarization
elif feature == "📝 Email Summarization":
    st.markdown("### 📝 Email Summarization")
    st.markdown("Get concise summaries of your email threads.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("**Sample emails loaded:**")
        st.write("- email_1: Project kickoff")
        st.write("- email_2: Budget update")
        st.write("- email_3: Team announcements")

    if primary_button("Generate Summary"):
        summary = with_spinner("Summarizing emails...", summarize_emails, st.session_state.email_context)
        if summary is not None:
            show_success(summary)

# Feature: Draft Reply Generator
elif feature == "✉️ Draft Reply Generator":
    st.markdown("### ✉️ Draft Reply Generator")
    st.markdown("Generate professional email replies based on your intent.")

    user_intent = st.text_area(
        "What do you want to communicate?",
        placeholder="I need to tell John I'll review the document by Friday...",
        height=100
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("Tone", ["Professional and polite", "Direct and actionable", "Friendly and casual", "Formal and detailed"])
    with col2:
        recipient = st.text_input("Recipient (optional)", placeholder="John")

    if primary_button("Generate Draft"):
        if user_intent:
            # Update context with tone and recipient
            context_updates = {'metadata': {'tone': tone}}
            if recipient:
                context_updates['metadata']['recipient'] = recipient

            context_with_tone = update_context(st.session_state.email_context, context_updates)

            draft = with_spinner("Drafting your reply...", generate_draft_reply, user_intent, context_with_tone)
            if draft is not None:
                st.markdown("### 📝 Your Draft")
                st.text_area("Copy and edit:", draft, height=200)
        else:
            st.warning("Please enter what you want to communicate.")

# Feature: Thread Organization
elif feature == "🧵 Thread Organization":
    st.markdown("### 🧵 Thread Organization")
    st.markdown("Organize and filter email threads by topic or participant.")

    org_query = st.text_input(
        "How would you like to organize your threads?",
        placeholder="Show me all emails about the project launch"
    )

    if primary_button("Organize"):
        if org_query:
            organized = with_spinner("Organizing threads...", organize_threads, org_query, st.session_state.email_context)
            if organized is not None:
                show_info(organized)
        else:
            st.warning("Please enter how you'd like to organize your threads.")

# Feature: Smart Inbox Rules
elif feature == "🏷️ Smart Inbox Rules":
    st.markdown("### 🏷️ Smart Inbox Rules")
    st.markdown("Get automated suggestions for email categorization.")

    sample_emails = [
        {"subject": "Weekly Newsletter: Tech Updates", "sender": "newsletter@techblog.com", "category": "promotional"},
        {"subject": "URGENT: Server Down", "sender": "alerts@monitoring.com", "category": "important"},
        {"subject": "Re: Q1 Budget Approval", "sender": "cfo@company.com", "category": "internal"},
        {"subject": "Meeting Reminder: Team Sync", "sender": "calendar@company.com", "category": "internal"},
        {"subject": "Your Amazon Order Shipped", "sender": "amazon@amazon.com", "category": "promotional"}
    ]

    if primary_button("Analyze & Suggest Rules"):
        context_with_emails = update_context(st.session_state.email_context, {'emails': sample_emails})
        suggestions = with_spinner("Analyzing email patterns...", suggest_inbox_rules, context_with_emails)
        if suggestions is not None:
            st.markdown("### 📋 Suggested Rules")
            show_success(suggestions)

# Feature: Meeting Scheduler
elif feature == "📅 Meeting Scheduler":
    st.markdown("### 📅 Meeting Scheduler")
    st.markdown("Extract meeting details from email threads.")

    meeting_emails = [
        {"subject": "Team Sync Tomorrow", "sender": "pm@company.com", "body": "Let's meet tomorrow at 2pm in Conference Room B to discuss Q2 goals."},
        {"subject": "Re: Team Sync Tomorrow", "sender": "dev@company.com", "body": "2pm works for me. I'll bring the latest mockups."},
        {"subject": "Re: Team Sync Tomorrow", "sender": "designer@company.com", "body": "Can we make it 2:30pm instead? I have a conflict at 2."}
    ]

    if primary_button("Extract Details"):
        context_with_meetings = update_context(st.session_state.email_context, {'emails': meeting_emails})
        meeting_details = with_spinner("Extracting meeting information...", extract_meeting_details, context_with_meetings)
        if meeting_details is not None:
            st.markdown("### 📅 Meeting Details")
            show_info(meeting_details)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Gmail Email Assistant MVP • Built with Streamlit & OpenAI"
    "</div>",
    unsafe_allow_html=True
)