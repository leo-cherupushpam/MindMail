import os
import sys
import html
import streamlit as st
from datetime import datetime
import streamlit_card as stc

# Add parent directory to path so we can import services module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.qa_service import (  # noqa: E402
    ask_question,
    summarize_emails,
    generate_draft_reply
)
from services.context_analyzer import ContextAnalyzer  # noqa: E402
from services.mock_data import get_sample_threads  # noqa: E402
from services.gmail_auth import (  # noqa: E402
    is_authenticated,
    logout
)
from services.gmail_fetcher import fetch_all_emails  # noqa: E402
from services.cache import load_cache, save_cache, is_cache_valid  # noqa: E402
from services.ui_helpers import format_email_card, format_thread_message  # noqa: E402

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

    /* Email Card Hover State */
    .email-card:hover {
        box-shadow: var(--shadow-md);
        background-color: #F9FAFB;
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

    /* ============================================
       3-COLUMN GRID LAYOUT
       ============================================ */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 2.75fr 1.25fr;
        gap: 0;
        height: calc(100vh - 80px);
        width: 100%;
    }

    .grid-column {
        overflow-y: auto;
        overflow-x: hidden;
    }

    .email-list-col {
        background-color: #F3F4F6;
        border-right: 1px solid #E5E7EB;
        padding: 16px;
    }

    .thread-viewer-col {
        background-color: white;
        padding: 24px;
    }

    .assistant-sidebar-col {
        background-color: #F9FAFB;
        border-left: 1px solid #E5E7EB;
        padding: 16px;
    }

    /* Hide Streamlit's native sidebar and footer */
    [data-testid="stSidebar"] {
        display: none;
    }

    footer {
        display: none;
    }

    /* ============================================
       HEADER TOOLBAR - STICKY
       ============================================ */
    .header-toolbar {
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #F9FAFB;
        border-bottom: 1px solid #E5E7EB;
        padding: 12px 24px;
        height: 60px;
        width: 100%;
        box-sizing: border-box;
    }

    .toolbar-left {
        display: flex;
        align-items: center;
        gap: 16px;
        flex: 1;
    }

    .toolbar-logo {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
    }

    .toolbar-search {
        flex: 1;
        max-width: 300px;
    }

    .toolbar-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .toolbar-account {
        font-size: 14px;
        color: #4B5563;
    }

    .toolbar-timestamp {
        font-size: 12px;
        color: #9CA3AF;
    }

    .toolbar-button {
        padding: 8px 16px;
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 150ms ease;
    }

    .toolbar-button:hover {
        background-color: #1D4ED8;
    }

    /* ============================================
       ENHANCED STYLING - Professional Appearance
       ============================================ */

    /* Email list cards - hover effects */
    .email-card {
        transition: all 150ms ease;
    }

    .email-card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* Thread viewer message styling */
    .thread-message {
        padding: 20px 0;
        border-bottom: 1px solid #E5E7EB;
    }

    .message-sender {
        font-weight: 700;
        color: #111827;
        font-size: 16px;
    }

    .message-time {
        color: #9CA3AF;
        font-size: 13px;
        margin-top: 4px;
    }

    .message-body {
        color: #111827;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
        margin-top: 12px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0 16px;
        border-bottom: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        border-bottom-color: #2563EB;
        color: #2563EB;
    }

    /* Assistant sidebar styling */
    .assistant-context {
        background-color: #DBEAFE;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 13px;
    }

    /* Text areas and inputs */
    .stTextArea textarea {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 14px;
    }

    /* Button styling - enhanced hover effects */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 150ms ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = is_authenticated()

if 'email_threads' not in st.session_state:
    if st.session_state.authenticated and is_cache_valid():
        st.session_state.email_threads = load_cache()
    else:
        st.session_state.email_threads = []

if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None

# Initialize context analyzer and load sample threads
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ContextAnalyzer()

if 'sample_threads' not in st.session_state:
    if st.session_state.authenticated and st.session_state.email_threads:
        st.session_state.sample_threads = st.session_state.email_threads
    else:
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

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

if 'selected_thread_idx' not in st.session_state:
    st.session_state.selected_thread_idx = 0

if 'selected_enriched_context' not in st.session_state:
    st.session_state.selected_enriched_context = None

# ============================================================================
# HEADER TOOLBAR
# ============================================================================
st.markdown('<div class="header-toolbar">', unsafe_allow_html=True)

toolbar_col1, toolbar_col2, toolbar_col3 = st.columns([2, 2, 1], gap="small")

with toolbar_col1:
    st.markdown('<div class="toolbar-logo">📧 Gmail Assistant</div>', unsafe_allow_html=True)

with toolbar_col2:
    search_query = st.text_input("Search threads...", label_visibility="collapsed", key="header_search")
    st.session_state.search_query = search_query

with toolbar_col3:
    col_account, col_refresh, col_logout = st.columns(3, gap="small")
    with col_account:
        if st.session_state.authenticated:
            st.caption("leocherupushpam@gmail.com")
    with col_refresh:
        if st.button("🔄 Refresh", use_container_width=True, key="toolbar_refresh"):
            with st.spinner("Fetching emails..."):
                threads = fetch_all_emails()
                save_cache(threads)
                st.session_state.email_threads = threads
                st.session_state.selected_thread_idx = 0
                st.session_state.last_refresh = datetime.now().isoformat()
            st.rerun()
    with col_logout:
        if st.button("🚪 Logout", use_container_width=True, key="toolbar_logout"):
            logout()
            st.session_state.authenticated = False
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Initialize session state if needed
if 'selected_thread_idx' not in st.session_state:
    st.session_state.selected_thread_idx = 0
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'assistant_tab' not in st.session_state:
    st.session_state.assistant_tab = "ask"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Create 3-column layout
col_list, col_thread, col_assistant = st.columns([1, 2.75, 1.25], gap="small")

# LEFT COLUMN: EMAIL LIST
with col_list:
    st.markdown("### 📧 Inbox")

    if st.session_state.authenticated and st.session_state.email_threads:
        # Filter threads by search query
        filtered_threads = st.session_state.email_threads
        if st.session_state.search_query:
            filtered_threads = [
                t for t in st.session_state.email_threads
                if st.session_state.search_query.lower() in t.main_topic.lower()
                or any(st.session_state.search_query.lower() in msg.sender.lower() for msg in t.messages)
            ]

        # Render email list with clickable cards using streamlit-card
        for display_idx, thread in enumerate(filtered_threads):
            # Find the actual index in the unfiltered list
            actual_idx = st.session_state.email_threads.index(thread)
            is_selected = (actual_idx == st.session_state.selected_thread_idx)

            # Extract email data
            sender = thread.messages[0].sender if thread.messages else "Unknown"
            preview = thread.messages[0].body[:80] + "..." if thread.messages and thread.messages[0].body else "No content"

            # Create clickable card with text as list [sender, preview]
            stc.card(
                title=thread.main_topic,
                text=[f"From: {sender}", preview],
                on_click=lambda actual_idx=actual_idx: (
                    st.session_state.update({'selected_thread_idx': actual_idx}),
                    st.session_state.update({'chat_history': []}),
                    st.rerun()
                ),
                key=f"email_card_{actual_idx}"
            )
    else:
        st.info("📭 No emails. Click 'Refresh' to fetch emails.")

# ============================================================================
# CENTER COLUMN: THREAD VIEWER (Task 4 - to be implemented)
# ============================================================================
with col_thread:
    st.markdown("### 📧 Email Thread")

    if st.session_state.authenticated and st.session_state.email_threads:
        if 0 <= st.session_state.selected_thread_idx < len(st.session_state.email_threads):
            selected_thread = st.session_state.email_threads[st.session_state.selected_thread_idx]

            # Thread header
            st.markdown(f"## {selected_thread.main_topic}")

            # Calculate date range from messages
            if selected_thread.messages:
                try:
                    dates = []
                    for msg in selected_thread.messages:
                        dt = datetime.fromisoformat(msg.timestamp.replace('Z', '+00:00'))
                        dates.append(dt.strftime("%b %d"))
                    date_range = f"{dates[0]} - {dates[-1]}" if len(dates) > 1 else dates[0]
                except (ValueError, AttributeError):
                    date_range = "unknown dates"
            else:
                date_range = "unknown dates"

            st.caption(f"{len(selected_thread.messages)} messages from {date_range}")
            st.caption(f"From: {', '.join(selected_thread.participants)}")
            st.markdown("---")

            # Thread messages (chronological, oldest to newest)
            for message in selected_thread.messages:
                html_msg = format_thread_message(
                    sender=message.sender,
                    email=message.sender,
                    timestamp=message.timestamp,
                    body=message.body
                )
                st.markdown(html_msg, unsafe_allow_html=True)

            # Update enriched context for selected thread (for Task 5 - assistant sidebar)
            enriched = st.session_state.analyzer.analyze_thread(selected_thread)
            st.session_state.selected_enriched_context = enriched
        else:
            st.info("Select an email thread from the list")
    else:
        st.info("📭 Authenticate and refresh to view emails")

# ============================================================================
# RIGHT COLUMN: ASSISTANT SIDEBAR
# ============================================================================
with col_assistant:
    if st.session_state.authenticated and st.session_state.email_threads:
        if 0 <= st.session_state.selected_thread_idx < len(st.session_state.email_threads):
            selected_thread = st.session_state.email_threads[st.session_state.selected_thread_idx]

            # Context indicator - show sender + subject
            if selected_thread.messages:
                sender = selected_thread.messages[0].sender
                subject = selected_thread.main_topic[:30]
                st.markdown(f"📧 **Analyzing:** {sender} — {subject}...")
            else:
                st.markdown(f"📧 **Analyzing:** {selected_thread.main_topic[:40]}...")
            st.markdown("---")

            # Tabbed interface
            tab_ask, tab_summarize, tab_draft = st.tabs(["💬 Ask", "📝 Summarize", "✉️ Draft"])

            # ASK TAB
            with tab_ask:
                st.session_state.assistant_tab = "ask"
                user_query = st.text_area(
                    "Ask about this email:",
                    placeholder="Ask about this email thread...",
                    label_visibility="collapsed",
                    height=100,
                    key="ask_input"
                )

                if st.button("Ask", use_container_width=True, key="ask_button"):
                    if user_query:
                        context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                        if context:
                            try:
                                with st.spinner("Thinking..."):
                                    response = ask_question(user_query, context)
                                if response and not response.startswith("Error:"):
                                    st.session_state.chat_history.append({"role": "user", "content": user_query})
                                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                                    st.rerun()
                                else:
                                    st.error(f"Failed to get response: {response}")
                            except Exception as e:
                                st.error(f"Error processing question: {str(e)}")

                # Display chat history with HTML cards
                if st.session_state.chat_history:
                    st.markdown("**Conversation:**")
                    for msg in st.session_state.chat_history:
                        escaped_content = html.escape(msg['content'])
                        if msg["role"] == "user":
                            st.markdown(f"""
                            <div style="background-color: white; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #2563EB;">
                                <div style="font-weight: 600; color: #111827; margin-bottom: 4px;">You:</div>
                                <div style="color: #4B5563; white-space: pre-wrap;">{escaped_content}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background-color: white; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #10B981;">
                                <div style="font-weight: 600; color: #111827; margin-bottom: 4px;">Assistant:</div>
                                <div style="color: #4B5563; white-space: pre-wrap;">{escaped_content}</div>
                            </div>
                            """, unsafe_allow_html=True)

            # SUMMARIZE TAB
            with tab_summarize:
                st.session_state.assistant_tab = "summarize"
                if st.button("Generate Summary", use_container_width=True, key="summarize_button"):
                    context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                    if context:
                        try:
                            with st.spinner("Summarizing..."):
                                summary = summarize_emails(context)
                            if summary and not summary.startswith("Error:"):
                                st.markdown("**Summary:**")
                                st.write(summary)
                                st.info("💡 Tip: Select the text above and use Ctrl+C / Cmd+C to copy")
                            else:
                                st.error(f"Failed to generate summary: {summary}")
                        except Exception as e:
                            st.error(f"Error generating summary: {str(e)}")

            # DRAFT TAB
            with tab_draft:
                st.session_state.assistant_tab = "draft"
                intent = st.text_area(
                    "What do you want to say?",
                    placeholder="What do you want to say? (e.g., 'Approve the budget')",
                    label_visibility="collapsed",
                    height=100,
                    key="draft_input"
                )

                tone = st.selectbox(
                    "Tone:",
                    ["Professional", "Collaborative", "Assertive", "Empathetic"],
                    key="draft_tone"
                )

                if st.button("Generate Draft", use_container_width=True, key="draft_button"):
                    if intent:
                        context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                        if context:
                            try:
                                with st.spinner("Drafting..."):
                                    draft = generate_draft_reply(context, intent, tone.lower())
                                if draft and not draft.startswith("Error:"):
                                    st.markdown("**Your Draft:**")
                                    st.text_area(
                                        "Edit and copy:",
                                        value=draft,
                                        height=150,
                                        disabled=True,
                                        label_visibility="collapsed"
                                    )
                                    st.info("💡 Tip: Select the text above and use Ctrl+C / Cmd+C to copy")
                                else:
                                    st.error(f"Failed to generate draft: {draft}")
                            except Exception as e:
                                st.error(f"Error generating draft: {str(e)}")
        else:
            st.info("Select an email to analyze")
    else:
        st.info("📭 Authenticate to use assistant")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "Gmail Email Assistant MVP • Built with Streamlit & OpenAI"
    "</div>",
    unsafe_allow_html=True
)
