import os
import sys
import html
import streamlit as st
from datetime import datetime

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
from services.ui_helpers import (  # noqa: E402
    format_tone_example,
    get_avatar_html,
    render_top_bar,
    render_left_nav,
    render_inbox_row,
    render_reading_pane_message,
)

# Page configuration
st.set_page_config(
    page_title="Gmail Email Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide native sidebar, we'll use custom layout
)

# Gmail-style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@400;500&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #FFFFFF !important;
        font-family: 'Google Sans', Roboto, Arial, sans-serif !important;
    }

    /* Hide Streamlit chrome */
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    footer,
    #MainMenu { display: none !important; }

    /* Remove default Streamlit padding */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Remove gap between Streamlit columns */
    [data-testid="column"] { padding: 0 !important; }

    /* Gmail top bar */
    .gmail-topbar {
        display: flex;
        align-items: center;
        height: 64px;
        padding: 0 16px;
        border-bottom: 1px solid #E0E0E0;
        background: #FFFFFF;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .gmail-logo {
        font-size: 22px;
        color: #5F6368;
        margin-left: 8px;
        margin-right: 24px;
        font-weight: 400;
    }
    .gmail-logo span { color: #EA4335; }
    .gmail-search {
        flex: 1;
        background: #EAF1FB;
        border-radius: 24px;
        height: 46px;
        display: flex;
        align-items: center;
        padding: 0 16px;
        max-width: 720px;
        color: #5F6368;
        font-size: 16px;
    }

    /* Gmail left nav */
    .gmail-nav {
        width: 100%;
        padding: 8px 0;
    }
    .gmail-compose {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #C2E7FF;
        color: #001D35;
        border-radius: 16px;
        padding: 18px 24px;
        font-size: 14px;
        font-weight: 500;
        margin: 8px 16px 16px;
        cursor: pointer;
        width: calc(100% - 32px);
        border: none;
    }
    .gmail-nav-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 16px 4px 24px;
        border-radius: 0 16px 16px 0;
        font-size: 14px;
        height: 32px;
        cursor: pointer;
        margin-right: 16px;
        color: #202124;
    }
    .gmail-nav-item.active {
        background: #D3E3FD;
        font-weight: 700;
    }
    .gmail-nav-count {
        font-size: 12px;
        color: #202124;
        font-weight: 700;
    }
    .gmail-nav-section {
        font-size: 11px;
        font-weight: 700;
        color: #444746;
        padding: 8px 16px 4px 24px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    /* Gmail email rows */
    .gmail-row {
        display: flex;
        align-items: center;
        padding: 0 16px;
        height: 52px;
        border-bottom: 1px solid #F0F0F0;
        cursor: pointer;
        font-size: 14px;
        gap: 8px;
    }
    .gmail-row.unread { background: #FFFFFF; }
    .gmail-row.read { background: #F6F8FC; }
    .gmail-row:hover { background: #F2F6FC; box-shadow: inset 1px 0 0 #DADCE0, inset -1px 0 0 #DADCE0; }
    .gmail-row-sender {
        width: 180px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex-shrink: 0;
    }
    .gmail-row-sender.unread { font-weight: 700; color: #202124; }
    .gmail-row-sender.read { font-weight: 400; color: #5F6368; }
    .gmail-row-subject {
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #202124;
    }
    .gmail-row-subject.unread { font-weight: 600; }
    .gmail-row-subject.read { font-weight: 400; color: #5F6368; }
    .gmail-row-snippet { color: #5F6368; font-weight: 400; }
    .gmail-row-time {
        font-size: 12px;
        color: #5F6368;
        white-space: nowrap;
        flex-shrink: 0;
        width: 50px;
        text-align: right;
    }
    .gmail-row-time.unread { font-weight: 700; color: #202124; }

    /* Gmail tab bar */
    .gmail-tabs {
        display: flex;
        border-bottom: 1px solid #E0E0E0;
        padding: 0 8px;
    }
    .gmail-tab {
        padding: 12px 16px;
        font-size: 14px;
        color: #5F6368;
        cursor: pointer;
        border-bottom: 3px solid transparent;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .gmail-tab.active {
        color: #1A73E8;
        border-bottom-color: #1A73E8;
        font-weight: 500;
    }

    /* Gmail reading pane */
    .gmail-reading-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 24px 8px;
        border-bottom: 1px solid #E0E0E0;
    }
    .gmail-back-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: #5F6368;
        font-size: 20px;
        background: none;
        border: none;
    }
    .gmail-back-btn:hover { background: #F1F3F4; }
    .gmail-reading-subject {
        font-size: 22px;
        font-weight: 400;
        color: #202124;
        flex: 1;
    }
    .gmail-message {
        padding: 16px 24px;
        border-bottom: 1px solid #E0E0E0;
    }
    .gmail-message-header {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-bottom: 16px;
    }
    .gmail-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 500;
        color: white;
        flex-shrink: 0;
    }
    .gmail-sender-name {
        font-size: 14px;
        font-weight: 600;
        color: #202124;
    }
    .gmail-sender-email {
        font-size: 12px;
        color: #5F6368;
    }
    .gmail-message-time {
        margin-left: auto;
        font-size: 12px;
        color: #5F6368;
        white-space: nowrap;
    }
    .gmail-message-body {
        font-size: 14px;
        color: #202124;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
        padding-left: 56px;
    }
    .gmail-reply-bar {
        display: flex;
        gap: 8px;
        padding: 16px 24px 24px 80px;
    }
    .gmail-reply-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid #DADCE0;
        background: white;
        color: #444746;
        font-size: 14px;
        cursor: pointer;
    }

    /* AI Assistant panel */
    .ai-panel {
        border-left: 1px solid #E0E0E0;
        height: 100%;
        background: #FFFFFF;
        display: flex;
        flex-direction: column;
    }
    .ai-panel-header {
        padding: 16px;
        border-bottom: 1px solid #E0E0E0;
        font-size: 14px;
        font-weight: 600;
        color: #202124;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ai-output-card {
        background: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 12px;
        font-size: 13px;
        color: #202124;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
        margin-top: 8px;
    }

    /* Streamlit button overrides for Gmail pill style */
    div[data-testid="stButton"] > button {
        border-radius: 20px !important;
        border: 1px solid #DADCE0 !important;
        background: white !important;
        color: #444746 !important;
        font-family: 'Google Sans', Roboto, Arial, sans-serif !important;
        font-size: 14px !important;
        padding: 6px 16px !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: #F6F8FC !important;
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

if 'selected_thread_idx' not in st.session_state:
    st.session_state.selected_thread_idx = 0
if 'selected_enriched_context' not in st.session_state:
    st.session_state.selected_enriched_context = None
if 'assistant_feature' not in st.session_state:
    st.session_state.assistant_feature = None  # "draft", "summarize", or None
if 'view' not in st.session_state:
    st.session_state.view = "inbox"  # "inbox" | "email"

# ── Top bar (always visible) ──────────────────────────────────────────────
st.markdown(render_top_bar(), unsafe_allow_html=True)

# ── Main layout: nav | content | ai panel ────────────────────────────────
nav_col, content_col, ai_col = st.columns([1, 4, 2], gap="small")

with nav_col:
    st.markdown(
        render_left_nav(inbox_count=len(st.session_state.sample_threads)),
        unsafe_allow_html=True,
    )

with content_col:
    if st.session_state.view == "inbox":
        # Tab bar
        st.markdown("""
        <div class="gmail-tabs">
            <div class="gmail-tab active">📥 Primary</div>
            <div class="gmail-tab">🏷️ Promotions</div>
            <div class="gmail-tab">👥 Social</div>
        </div>
        """, unsafe_allow_html=True)

        # Email rows — first 5 are unread, rest are read
        threads = st.session_state.sample_threads
        for idx, thread in enumerate(threads):
            is_unread = idx < 5
            row_html = render_inbox_row(thread, is_unread=is_unread)
            st.markdown(row_html, unsafe_allow_html=True)
            # Invisible Streamlit button that captures click
            if st.button("", key=f"open_thread_{idx}", use_container_width=True,
                         help=thread.main_topic):
                st.session_state.selected_thread_idx = idx
                st.session_state.view = "email"
                st.session_state.assistant_feature = None
                st.session_state.chat_history = []
                st.rerun()

    else:
        thread = st.session_state.sample_threads[st.session_state.selected_thread_idx]

        # Reading pane header with subject
        st.markdown(f"""
        <div class="gmail-reading-header">
            <div class="gmail-reading-subject">{html.escape(thread.main_topic)}</div>
        </div>
        """, unsafe_allow_html=True)

        # Back button (Streamlit button so it triggers rerun)
        if st.button("← Back", key="back_to_inbox"):
            st.session_state.view = "inbox"
            st.session_state.assistant_feature = None
            st.rerun()

        # Render all messages in the thread
        for message in thread.messages:
            msg_html = render_reading_pane_message(
                sender=message.sender,
                email_addr=message.sender,
                timestamp=message.timestamp,
                body=message.body,
            )
            st.markdown(msg_html, unsafe_allow_html=True)

        # Static reply/forward bar
        st.markdown("""
        <div class="gmail-reply-bar">
            <button class="gmail-reply-btn">↩ Reply</button>
            <button class="gmail-reply-btn">↪ Forward</button>
        </div>
        """, unsafe_allow_html=True)

with ai_col:
    if st.session_state.view == "email":
        thread = st.session_state.sample_threads[st.session_state.selected_thread_idx]
        enriched = st.session_state.enriched_contexts[st.session_state.selected_thread_idx]

        st.markdown('<div class="ai-panel-header">✦ Gmail Assistant</div>', unsafe_allow_html=True)

        col_ask, col_draft, col_summarize = st.columns(3, gap="small")
        with col_ask:
            if st.button("💬 Ask", use_container_width=True, key="ai_ask_btn"):
                st.session_state.assistant_feature = "ask"
        with col_draft:
            if st.button("✏️ Draft", use_container_width=True, key="ai_draft_btn"):
                st.session_state.assistant_feature = "draft"
        with col_summarize:
            if st.button("📊 Sum", use_container_width=True, key="ai_sum_btn"):
                st.session_state.assistant_feature = "summarize"

        st.markdown("---")

        # ── Ask ──────────────────────────────────────────────────────────
        if st.session_state.assistant_feature == "ask":
            question = st.text_area("Your question:", placeholder="What action do I need to take?",
                                    height=80, key="ask_input", label_visibility="collapsed")
            if st.button("Ask", key="ask_submit_btn", use_container_width=True):
                if question.strip():
                    with st.spinner("Thinking..."):
                        answer = ask_question(question, enriched)
                    st.markdown(f'<div class="ai-output-card">{html.escape(answer)}</div>',
                                unsafe_allow_html=True)

        # ── Draft ────────────────────────────────────────────────────────
        elif st.session_state.assistant_feature == "draft":
            intent = st.text_area("Intent (optional):", height=60, key="draft_intent",
                                  placeholder="e.g. Accept and propose a timeline",
                                  label_visibility="collapsed")
            tone = st.selectbox("Tone", ["professional", "collaborative", "assertive", "empathetic"],
                                key="draft_tone", label_visibility="collapsed")
            if st.button("Generate Draft", key="draft_submit_btn", use_container_width=True):
                with st.spinner("Drafting..."):
                    draft = generate_draft_reply(enriched, user_intent=intent or None, tone=tone)
                st.markdown(f'<div class="ai-output-card">{html.escape(draft)}</div>',
                            unsafe_allow_html=True)
                col1, col2 = st.columns(2, gap="small")
                with col1:
                    if st.button("📋 Copy", key="draft_copy_btn", use_container_width=True):
                        st.success("Copied!")
                with col2:
                    if st.button("🔄 Retry", key="draft_retry_btn", use_container_width=True):
                        st.rerun()

        # ── Summarize ────────────────────────────────────────────────────
        elif st.session_state.assistant_feature == "summarize":
            if st.button("Summarize thread", key="sum_submit_btn", use_container_width=True):
                with st.spinner("Summarizing..."):
                    summary = summarize_emails(enriched)
                st.markdown(f'<div class="ai-output-card">{html.escape(summary)}</div>',
                            unsafe_allow_html=True)

        # ── No feature selected ──────────────────────────────────────────
        elif st.session_state.assistant_feature is None:
            st.caption("Select an email and choose an action above.")
