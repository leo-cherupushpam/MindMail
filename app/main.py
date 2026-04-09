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

# Page configuration
st.set_page_config(
    page_title="Gmail Email Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📧 Gmail Email Assistant")
st.markdown("""
Your AI-powered email assistant for smarter inbox management.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
feature = st.sidebar.selectbox(
    "Choose a feature",
    [
        "💬 Conversational Q&A",
        "📝 Email Summarization",
        "✉️ Draft Reply Generator",
        "🧵 Thread Organization",
        "🏷️ Smart Inbox Rules",
        "📅 Meeting Scheduler"
    ]
)

# Initialize session state for email context (simulated)
if 'email_context' not in st.session_state:
    st.session_state.email_context = {
        'emails': ['email_1', 'email_2', 'email_3'],
        'metadata': {
            'project': 'Q1 Planning',
            'date_range': 'last_week'
        }
    }

# Feature implementations
if feature == "💬 Conversational Q&A":
    st.header("💬 Conversational Q&A")
    st.markdown("Ask questions about your emails and get contextual answers.")

    # Input for user question
    user_query = st.text_input(
        "Ask a question about your emails:",
        placeholder="What did John say about the project deadline?"
    )

    if st.button("Get Answer", type="primary"):
        if user_query:
            with st.spinner("Thinking..."):
                try:
                    response = ask_question(user_query, st.session_state.email_context)
                    st.success("Answer:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question.")

elif feature == "📝 Email Summarization":
    st.header("📝 Email Summarization")
    st.markdown("Get a concise summary of your email threads.")

    if st.button("Generate Summary", type="primary"):
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_emails(st.session_state.email_context)
                st.success("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif feature == "✉️ Draft Reply Generator":
    st.header("✉️ Draft Reply Generator")
    st.markdown("Generate professional email replies based on your intent.")

    # Input for what user wants to communicate
    user_intent = st.text_area(
        "What do you want to communicate?",
        placeholder="I need to tell the team I'll be delayed for the meeting",
        height=100
    )

    # Tone selection
    tone = st.selectbox(
        "Select tone:",
        ["Professional and polite", "Direct and actionable", "Friendly and casual", "Formal and detailed"]
    )

    # Update context with tone
    context_with_tone = st.session_state.email_context.copy()
    context_with_tone['metadata'] = context_with_tone.get('metadata', {}).copy()
    context_with_tone['metadata']['tone'] = tone

    if st.button("Generate Draft", type="primary"):
        if user_intent:
            with st.spinner("Drafting..."):
                try:
                    draft = generate_draft_reply(user_intent, context_with_tone)
                    st.success("Draft Reply:")
                    st.text_area("Your draft:", draft, height=150)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please describe what you want to communicate.")

elif feature == "🧵 Thread Organization":
    st.header("🧵 Thread Organization")
    st.markdown("Organize and filter email threads by topic or participant.")

    # Input for organization query
    org_query = st.text_input(
        "How would you like to organize your threads?",
        placeholder="Show me all emails about the budget review"
    )

    if st.button("Organize Threads", type="primary"):
        if org_query:
            with st.spinner("Organizing..."):
                try:
                    organized = organize_threads(org_query, st.session_state.email_context)
                    st.success("Organized Threads:")
                    st.write(organized)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter how you'd like to organize your threads.")

elif feature == "🏷️ Smart Inbox Rules":
    st.header("🏷️ Smart Inbox Rules")
    st.markdown("Get automated suggestions for email categorization and labeling.")

    # Sample emails for demonstration
    sample_emails = [
        {"subject": "Weekly Newsletter: Tech Updates", "sender": "newsletter@techblog.com", "category": "promotional"},
        {"subject": "URGENT: Server Down", "sender": "alerts@monitoring.com", "category": "important"},
        {"subject": "Re: Q1 Budget Approval", "sender": "cfo@company.com", "category": "internal"},
        {"subject": "Meeting Reminder: Team Sync", "sender": "calendar@company.com", "category": "internal"},
        {"subject": "Your Amazon Order Shipped", "sender": "amazon@amazon.com", "category": "promotional"}
    ]

    # Update context with sample emails
    context_with_emails = st.session_state.email_context.copy()
    context_with_emails['emails'] = sample_emails

    if st.button("Get Inbox Rule Suggestions", type="primary"):
        with st.spinner("Analyzing emails..."):
            try:
                suggestions = suggest_inbox_rules(context_with_emails)
                st.success("Inbox Rule Suggestions:")
                st.write(suggestions)
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif feature == "📅 Meeting Scheduler":
    st.header("📅 Meeting Scheduler")
    st.markdown("Extract meeting details from email threads.")

    # Sample meeting emails for demonstration
    meeting_emails = [
        {"subject": "Team Sync Tomorrow", "sender": "pm@company.com", "body": "Let's meet tomorrow at 2pm in Conference Room B to discuss Q2 goals."},
        {"subject": "Re: Team Sync Tomorrow", "sender": "dev@company.com", "body": "2pm works for me. I'll bring the latest mockups."},
        {"subject": "Re: Team Sync Tomorrow", "sender": "designer@company.com", "body": "Can we make it 2:30pm instead? I have a conflict at 2."}
    ]

    # Update context with meeting emails
    context_with_meetings = st.session_state.email_context.copy()
    context_with_meetings['emails'] = meeting_emails

    if st.button("Extract Meeting Details", type="primary"):
        with st.spinner("Extracting meeting details..."):
            try:
                meeting_details = extract_meeting_details(context_with_meetings)
                st.success("Meeting Details:")
                st.write(meeting_details)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Gmail Email Assistant MVP • Built with Streamlit & OpenAI"
    "</div>",
    unsafe_allow_html=True
)