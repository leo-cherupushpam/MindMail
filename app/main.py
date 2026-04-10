import streamlit as st
import os
import sys

# Add parent directory to path so we can import services module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.qa_service import (
    ask_question,
    summarize_emails,
    generate_draft_reply
)

from services.models import EmailThread, EmailMessage, EnrichedContext
from services.context_analyzer import ContextAnalyzer
from services.mock_data import get_sample_threads

# Import utility functions
from utils import (
    safe_execute,
    with_spinner,
    primary_button,
    show_success,
    show_info,
    update_context,
    add_chat_exchange,
    render_chat_message,
    show_success_box,
    show_info_box,
    show_warning_box,
    show_error_box,
    render_empty_state
)

# Page configuration
st.set_page_config(
    page_title="Gmail Email Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide native sidebar, we'll use custom layout
)

# Design System & Custom CSS
st.markdown("""
<style>
    /* ============================================
       DESIGN TOKENS - Color Palette
       ============================================ */
    :root {
        /* Primary Colors */
        --color-primary: #2563EB;
        --color-primary-dark: #1D4ED8;
        --color-primary-light: #DBEAFE;

        /* Semantic Colors */
        --color-success: #10B981;
        --color-success-light: #ECFDF5;
        --color-warning: #F59E0B;
        --color-warning-light: #FFFBEB;
        --color-error: #EF4444;
        --color-error-light: #FEF2F2;

        /* Neutral Colors */
        --color-neutral-50: #F9FAFB;
        --color-neutral-100: #F3F4F6;
        --color-neutral-200: #E5E7EB;
        --color-neutral-400: #9CA3AF;
        --color-neutral-600: #4B5563;
        --color-neutral-900: #111827;

        /* ============================================
           DESIGN TOKENS - Typography
           ============================================ */
        --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

        /* Font Sizes */
        --font-size-xs: 12px;
        --font-size-sm: 14px;
        --font-size-base: 16px;
        --font-size-lg: 18px;
        --font-size-xl: 24px;
        --font-size-2xl: 32px;

        /* Font Weights */
        --font-weight-regular: 400;
        --font-weight-medium: 500;
        --font-weight-semibold: 600;
        --font-weight-bold: 700;

        /* ============================================
           DESIGN TOKENS - Spacing (8px base unit)
           ============================================ */
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 16px;
        --spacing-lg: 24px;
        --spacing-xl: 32px;
        --spacing-2xl: 48px;

        /* ============================================
           DESIGN TOKENS - Border & Shadow
           ============================================ */
        --border-radius-sm: 4px;
        --border-radius-md: 8px;
        --border-radius-lg: 12px;

        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);

        /* Line Height */
        --line-height-tight: 1.25;
        --line-height-normal: 1.5;
        --line-height-relaxed: 1.75;
    }

    /* ============================================
       GLOBAL STYLES & RESETS
       ============================================ */
    * {
        box-sizing: border-box;
    }

    body {
        font-family: var(--font-family);
        font-size: var(--font-size-base);
        line-height: var(--line-height-normal);
        color: var(--color-neutral-900);
        background-color: white;
        margin: 0;
        padding: 0;
    }

    /* ============================================
       ACCESSIBILITY - Focus States
       ============================================ */

    /* Global Focus Style */
    *:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    /* Skip to Main Link */
    .skip-to-main {
        position: absolute;
        top: -40px;
        left: 0;
        background-color: var(--color-primary);
        color: white;
        padding: 8px 16px;
        text-decoration: none;
        border-radius: var(--border-radius-md);
        font-size: var(--font-size-sm);
    }

    .skip-to-main:focus {
        top: 0;
        z-index: 10000;
    }

    /* Link Styles */
    a {
        color: var(--color-primary);
        text-decoration: none;
        transition: color 150ms ease;
    }

    a:hover {
        color: var(--color-primary-dark);
        text-decoration: underline;
    }

    /* ============================================
       COMPONENT STYLES
       ============================================ */

    /* Main Header */
    .main-header {
        font-size: var(--font-size-2xl);
        font-weight: var(--font-weight-bold);
        margin-bottom: var(--spacing-sm);
        color: var(--color-neutral-900);
    }

    /* Feature Card */
    .feature-card {
        background-color: var(--color-neutral-50);
        border: 1px solid var(--color-neutral-200);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-md);
        height: 180px;
        box-shadow: var(--shadow-sm);
        transition: all 200ms ease-out;
        cursor: pointer;
    }

    .feature-card:hover {
        box-shadow: var(--shadow-md);
        transform: scale(1.02);
    }

    .feature-card.active {
        background-color: var(--color-primary-light);
        color: var(--color-primary);
        border-color: var(--color-primary);
    }

    /* Success Box */
    .success-box {
        background-color: var(--color-success-light);
        border-left: 4px solid var(--color-success);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        margin: var(--spacing-lg) 0;
        color: var(--color-neutral-900);
    }

    /* Info Box */
    .info-box {
        background-color: #EFF6FF;
        border-left: 4px solid var(--color-primary);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        margin: var(--spacing-lg) 0;
        color: var(--color-neutral-900);
    }

    /* Warning Box */
    .warning-box {
        background-color: var(--color-warning-light);
        border-left: 4px solid var(--color-warning);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        margin: var(--spacing-lg) 0;
        color: var(--color-neutral-900);
    }

    /* Error Box */
    .error-box {
        background-color: var(--color-error-light);
        border-left: 4px solid var(--color-error);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        margin: var(--spacing-lg) 0;
        color: var(--color-neutral-900);
    }

    /* Input Card Container */
    .input-card {
        background-color: var(--color-neutral-50);
        border: 1px solid var(--color-neutral-200);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-sm);
        margin-bottom: var(--spacing-lg);
    }

    .input-card label {
        display: block;
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        color: var(--color-neutral-900);
        margin-bottom: var(--spacing-sm);
    }

    /* Chat Message Bubble - User */
    .chat-message.user-message {
        margin-bottom: var(--spacing-md);
        display: flex;
        justify-content: flex-end;
    }

    .chat-message.user-message > div {
        background-color: var(--color-primary);
        color: white;
        padding: 12px 16px;
        border-radius: var(--border-radius-lg);
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 150ms ease;
    }

    .chat-message.user-message > div:hover {
        box-shadow: var(--shadow-md);
    }

    /* Chat Message Bubble - Assistant */
    .chat-message.assistant-message {
        margin-bottom: var(--spacing-md);
        display: flex;
        justify-content: flex-start;
    }

    .chat-message.assistant-message > div {
        background-color: var(--color-neutral-100);
        color: var(--color-neutral-900);
        padding: 12px 16px;
        border-radius: var(--border-radius-lg);
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 150ms ease;
    }

    .chat-message.assistant-message > div:hover {
        box-shadow: var(--shadow-md);
    }

    /* Button Styles */
    .stButton > button {
        width: 100%;
        border-radius: var(--border-radius-md);
        padding: 10px 16px;
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        border: none;
        cursor: pointer;
        transition: all 150ms ease;
    }

    /* Primary Button */
    .stButton > button {
        background-color: var(--color-primary);
        color: white;
    }

    .stButton > button:hover:not(:disabled) {
        background-color: var(--color-primary-dark);
        box-shadow: var(--shadow-md);
    }

    .stButton > button:active:not(:disabled) {
        background-color: #1E40AF;
    }

    .stButton > button:disabled {
        background-color: var(--color-neutral-200);
        color: var(--color-neutral-400);
        cursor: not-allowed;
        opacity: 0.6;
    }

    .stButton > button:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
        box-shadow: var(--shadow-md);
    }

    /* Enhanced keyboard focus for buttons */
    .stButton > button:focus {
        outline: 3px solid var(--color-primary);
        outline-offset: 2px;
    }

    /* Input Field Styling */
    input, textarea, select {
        font-family: var(--font-family);
        font-size: var(--font-size-sm);
        border: 1px solid var(--color-neutral-200);
        border-radius: var(--border-radius-md);
        padding: 12px 16px;
        color: var(--color-neutral-900);
        transition: all 150ms ease;
    }

    input::placeholder, textarea::placeholder {
        color: var(--color-neutral-400);
    }

    input:focus, textarea:focus, select:focus {
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15), inset 0 0 0 1px rgba(37, 99, 235, 0.1);
        outline: 2px solid transparent;
        outline-offset: 2px;
    }

    input:focus-visible, textarea:focus-visible, select:focus-visible {
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15), inset 0 0 0 1px rgba(37, 99, 235, 0.1);
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    input:disabled, textarea:disabled, select:disabled {
        background-color: var(--color-neutral-100);
        color: var(--color-neutral-400);
        cursor: not-allowed;
    }

    /* Loading Spinner */
    .spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid var(--color-neutral-200);
        border-top-color: var(--color-primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* ============================================
       LAYOUT COMPONENTS - Fixed Sidebar
       ============================================ */

    /* Sidebar Header */
    .sidebar-header {
        font-size: var(--font-size-lg);
        font-weight: var(--font-weight-bold);
        color: var(--color-neutral-900);
        padding: var(--spacing-lg);
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        background-color: white;
    }

    /* Sidebar Navigation Container */
    .sidebar-nav {
        padding: 0 var(--spacing-md);
    }

    /* Sidebar Navigation Item */
    .sidebar-nav-item {
        display: flex;
        align-items: center;
        padding: var(--spacing-md) var(--spacing-lg);
        margin-bottom: var(--spacing-sm);
        border-radius: var(--border-radius-md);
        cursor: pointer;
        background-color: transparent;
        color: var(--color-neutral-900);
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        transition: all 150ms ease;
        text-decoration: none;
        border: none;
        width: 100%;
        text-align: left;
    }

    .sidebar-nav-item:hover {
        background-color: var(--color-neutral-100);
        color: var(--color-primary);
    }

    .sidebar-nav-item.active {
        background-color: var(--color-primary-light);
        color: var(--color-primary);
        font-weight: var(--font-weight-semibold);
    }

    /* Sidebar Divider */
    .sidebar-divider {
        height: 1px;
        background-color: var(--color-neutral-200);
        margin: var(--spacing-lg) 0;
    }

    /* Sidebar Settings Section */
    .sidebar-settings {
        padding: 0 var(--spacing-md) var(--spacing-lg);
        margin-top: auto;
    }

    .settings-label {
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-semibold);
        color: var(--color-neutral-600);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: var(--spacing-md);
        display: block;
    }

    /* Main Content Header */
    .content-header {
        margin-bottom: var(--spacing-lg);
    }

    .content-title {
        font-size: var(--font-size-2xl);
        font-weight: var(--font-weight-bold);
        color: var(--color-neutral-900);
        margin-bottom: var(--spacing-sm);
    }

    .content-subtitle {
        font-size: var(--font-size-base);
        color: var(--color-neutral-600);
        margin-bottom: var(--spacing-lg);
    }

    /* Sidebar Container Styling */
    .sidebar-container {
        background-color: var(--color-neutral-50);
        border-right: 1px solid var(--color-neutral-200);
        height: 100vh;
        overflow-y: auto;
        position: relative;
    }

    /* Main Content Container */
    .main-content-container {
        padding: var(--spacing-lg);
        background-color: white;
        overflow-y: auto;
    }

    /* ============================================
       ACCESSIBILITY - Enhanced Keyboard Navigation
       ============================================ */

    /* Sidebar navigation keyboard focus */
    .sidebar-nav-item:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
        background-color: var(--color-primary-light);
        color: var(--color-primary);
    }

    /* Link keyboard focus */
    a:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
        border-radius: 2px;
    }

    /* Reduce motion for users who prefer it */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* High contrast mode support */
    @media (prefers-contrast: more) {
        .sidebar-nav-item {
            border: 1px solid transparent;
        }

        .sidebar-nav-item:focus-visible {
            border: 2px solid var(--color-primary);
        }

        button {
            border: 1px solid currentColor;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize context analyzer and load sample threads
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ContextAnalyzer()

if 'sample_threads' not in st.session_state:
    st.session_state.sample_threads = get_sample_threads()

if 'enriched_contexts' not in st.session_state:
    st.session_state.enriched_contexts = []
    for thread in st.session_state.sample_threads:
        enriched = st.session_state.analyzer.analyze_thread(thread)
        st.session_state.enriched_contexts.append(enriched)

# Initialize session state
if 'email_context' not in st.session_state:
    st.session_state.email_context = {
        'emails': ['email_1', 'email_2', 'email_3'],
        'metadata': {'project': 'Q1 Planning', 'date_range': 'last_week'}
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'selected_feature' not in st.session_state:
    st.session_state.selected_feature = "💬 Conversational Q&A"

# Define feature list
FEATURES = [
    "💬 Conversational Q&A",
    "📝 Email Summarization",
    "✉️ Draft Reply Generator",
    "🧵 Thread Organization",
    "🏷️ Smart Inbox Rules",
    "📅 Meeting Scheduler"
]

# Feature metadata for display
FEATURE_METADATA = {
    "💬 Conversational Q&A": {"icon": "💬", "title": "Ask Questions About Your Emails", "subtitle": "Get intelligent answers grounded in your email context."},
    "📝 Email Summarization": {"icon": "📝", "title": "Email Summarization", "subtitle": "Get concise summaries of your email threads."},
    "✉️ Draft Reply Generator": {"icon": "✉️", "title": "Draft Reply Generator", "subtitle": "Generate professional email replies based on your intent."},
    "🧵 Thread Organization": {"icon": "🧵", "title": "Thread Organization", "subtitle": "Organize and filter email threads by topic or participant."},
    "🏷️ Smart Inbox Rules": {"icon": "🏷️", "title": "Smart Inbox Rules", "subtitle": "Get automated suggestions for email categorization."},
    "📅 Meeting Scheduler": {"icon": "📅", "title": "Meeting Scheduler", "subtitle": "Extract meeting details from email threads."}
}

# Create 2-column layout: sidebar (1) and main content (4)
col_sidebar, col_main = st.columns([1, 4], gap="small")

# ============================================================================
# LEFT COLUMN: FIXED SIDEBAR NAVIGATION
# ============================================================================
with col_sidebar:
    # Sidebar Header
    st.markdown("""
    <div class="sidebar-header">
        <span style="font-size: 24px;">📧</span>
        <span>Gmail Assistant</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Feature Navigation
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

    for feature in FEATURES:
        # Create a button-like experience for each feature
        is_active = st.session_state.selected_feature == feature
        active_class = "active" if is_active else ""

        if st.button(
            feature,
            key=f"nav_{feature}",
            use_container_width=True,
            help=f"Select {feature}"
        ):
            st.session_state.selected_feature = feature
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar Divider
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Settings Section
    st.markdown('<div class="sidebar-settings">', unsafe_allow_html=True)
    st.markdown('<span class="settings-label">⚙️ Settings</span>', unsafe_allow_html=True)

    if primary_button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RIGHT COLUMN: MAIN CONTENT AREA
# ============================================================================
with col_main:
    # Get selected feature and metadata
    feature = st.session_state.selected_feature
    metadata = FEATURE_METADATA.get(feature, {})

    # Render Content Header
    st.markdown('<div class="content-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="content-title">{metadata.get("title", feature)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-subtitle">{metadata.get("subtitle", "")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ====================================================================
    # FEATURE: Conversational Q&A
    # ====================================================================
    if feature == "💬 Conversational Q&A":
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
            if st.session_state.enriched_contexts:
                response = with_spinner("Analyzing your emails...", ask_question, user_query, st.session_state.enriched_contexts[0])
            else:
                response = "No enriched context available"
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

    # ====================================================================
    # FEATURE: Email Summarization
    # ====================================================================
    elif feature == "📝 Email Summarization":
        st.markdown("### 📝 Sample Emails")
        st.markdown("- **email_1**: Project kickoff")
        st.markdown("- **email_2**: Budget update")
        st.markdown("- **email_3**: Team announcements")
        st.markdown("")  # Spacing

        if primary_button("Generate Summary"):
            if st.session_state.enriched_contexts:
                summary = with_spinner("Summarizing emails...", summarize_emails, st.session_state.enriched_contexts[0])
            else:
                summary = "No enriched context available"
            if summary is not None:
                show_success_box(summary, "Summary Generated")

    # ====================================================================
    # FEATURE: Draft Reply Generator
    # ====================================================================
    elif feature == "✉️ Draft Reply Generator":
        user_intent = st.text_area(
            "What do you want to communicate?",
            placeholder="I need to tell John I'll review the document by Friday...",
            height=100
        )

        col1, col2 = st.columns(2)
        with col1:
            tone = st.selectbox("Tone", ["professional", "collaborative", "assertive", "empathetic"])
        with col2:
            recipient = st.text_input("Recipient (optional)", placeholder="John")

        if primary_button("Generate Draft"):
            if user_intent:
                if st.session_state.enriched_contexts:
                    draft = with_spinner("Drafting your reply...", generate_draft_reply, st.session_state.enriched_contexts[0], user_intent, tone)
                else:
                    draft = "No enriched context available"
                if draft is not None:
                    st.markdown("### 📝 Your Draft")
                    st.text_area("Copy and edit:", draft, height=200)
            else:
                st.warning("Please enter what you want to communicate.")

    # ====================================================================
    # FEATURE: Thread Organization
    # ====================================================================
    elif feature == "🧵 Thread Organization":
        org_query = st.text_input(
            "How would you like to organize your threads?",
            placeholder="Show me all emails about the project launch"
        )

        if primary_button("Organize"):
            if org_query:
                organized = with_spinner("Organizing threads...", organize_threads, org_query, st.session_state.email_context)
                if organized is not None:
                    show_info_box(organized, "Organized Threads")
            else:
                st.warning("Please enter how you'd like to organize your threads.")

    # ====================================================================
    # FEATURE: Smart Inbox Rules
    # ====================================================================
    elif feature == "🏷️ Smart Inbox Rules":
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
                st.markdown("")
                show_success_box(suggestions, "Suggested Inbox Rules")

    # ====================================================================
    # FEATURE: Meeting Scheduler
    # ====================================================================
    elif feature == "📅 Meeting Scheduler":
        meeting_emails = [
            {"subject": "Team Sync Tomorrow", "sender": "pm@company.com", "body": "Let's meet tomorrow at 2pm in Conference Room B to discuss Q2 goals."},
            {"subject": "Re: Team Sync Tomorrow", "sender": "dev@company.com", "body": "2pm works for me. I'll bring the latest mockups."},
            {"subject": "Re: Team Sync Tomorrow", "sender": "designer@company.com", "body": "Can we make it 2:30pm instead? I have a conflict at 2."}
        ]

        if primary_button("Extract Details"):
            context_with_meetings = update_context(st.session_state.email_context, {'emails': meeting_emails})
            meeting_details = with_spinner("Extracting meeting information...", extract_meeting_details, context_with_meetings)
            if meeting_details is not None:
                st.markdown("")
                show_info_box(meeting_details, "Meeting Details Extracted")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 12px;'>"
        "Gmail Email Assistant MVP • Built with Streamlit & OpenAI"
        "</div>",
        unsafe_allow_html=True
    )