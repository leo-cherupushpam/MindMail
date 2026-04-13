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

# Create 3-column layout: Gmail inbox (left) | Thread (middle) | Assistant sidebar (right)
col_list, col_thread, col_assistant = st.columns([1, 1.5, 1], gap="small")

# LEFT COLUMN: EMAIL LIST
with col_list:
    st.markdown("### 📧 Inbox")

    if st.session_state.sample_threads:
        # Render email list with clickable cards
        for display_idx, thread in enumerate(st.session_state.sample_threads):
            # Find the actual index in the unfiltered list
            actual_idx = st.session_state.sample_threads.index(thread)
            is_selected = (actual_idx == st.session_state.selected_thread_idx)

            # Get urgency from enriched context if available
            urgency = "normal"
            if st.session_state.enriched_contexts and actual_idx < len(st.session_state.enriched_contexts):
                enriched = st.session_state.enriched_contexts[actual_idx]
                if enriched.urgency_assessment:
                    urgency = enriched.urgency_assessment

            # Render email card
            html_card = format_email_card(thread, is_selected, urgency)
            st.markdown(html_card, unsafe_allow_html=True)

            # Hidden button (empty label, styled minimally)
            if st.button("", key=f"select_{actual_idx}", use_container_width=True):
                st.session_state.selected_thread_idx = actual_idx
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.info("📭 No emails. Click 'Refresh' to fetch emails.")

# ============================================================================
# MIDDLE COLUMN: THREAD VIEWER
# ============================================================================
with col_thread:
    st.markdown("### 📧 Email Thread")

    if st.session_state.sample_threads:
        if 0 <= st.session_state.selected_thread_idx < len(st.session_state.sample_threads):
            selected_thread = st.session_state.sample_threads[st.session_state.selected_thread_idx]

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

            # Collect all messages into a scrollable container
            messages_html = []
            for message in selected_thread.messages:
                html_msg = format_thread_message(
                    sender=message.sender,
                    email=message.sender,
                    timestamp=message.timestamp,
                    body=message.body
                )
                messages_html.append(html_msg)

            # Render messages in a fixed-height scrollable container
            container_html = f"""
            <div class="thread-messages-container">
                {''.join(messages_html)}
            </div>
            """
            st.html(container_html)

            # Update enriched context for selected thread
            enriched = st.session_state.analyzer.analyze_thread(selected_thread)
            st.session_state.selected_enriched_context = enriched
        else:
            st.info("Select an email thread from the list")
    else:
        st.info("📭 No emails. Click 'Refresh' to fetch emails.")

# ============================================================================
# RIGHT COLUMN: ASSISTANT SIDEBAR
# ============================================================================
with col_assistant:
    if st.session_state.sample_threads:
        if 0 <= st.session_state.selected_thread_idx < len(st.session_state.sample_threads):
            selected_thread = st.session_state.sample_threads[st.session_state.selected_thread_idx]

            # ========== ASSISTANT FEATURES ==========
            st.markdown("### How can I help?")
            col_ask_btn, col_draft_btn, col_summarize_btn = st.columns(3, gap="small")

            with col_ask_btn:
                if st.button(
                    "💬 Ask",
                    use_container_width=True,
                    key="feature_ask_btn",
                    type="primary" if st.session_state.assistant_feature == "ask" else "secondary"
                ):
                    st.session_state.assistant_feature = None if st.session_state.assistant_feature == "ask" else "ask"
                    st.rerun()

            with col_draft_btn:
                if st.button(
                    "📝 Draft",
                    use_container_width=True,
                    key="feature_draft_btn",
                    type="primary" if st.session_state.assistant_feature == "draft" else "secondary"
                ):
                    st.session_state.assistant_feature = None if st.session_state.assistant_feature == "draft" else "draft"
                    st.rerun()

            with col_summarize_btn:
                if st.button(
                    "📋 Summarize",
                    use_container_width=True,
                    key="feature_summarize_btn",
                    type="primary" if st.session_state.assistant_feature == "summarize" else "secondary"
                ):
                    st.session_state.assistant_feature = None if st.session_state.assistant_feature == "summarize" else "summarize"
                    st.rerun()

            st.markdown("---")

            # ========== ASK FEATURE ==========
            if st.session_state.assistant_feature == "ask":
                st.markdown("#### 💬 Ask a Question")

                # Display conversation history
                if st.session_state.chat_history:
                    for message in st.session_state.chat_history:
                        if message["role"] == "user":
                            st.markdown(f"**You:** {message['content']}")
                        else:
                            st.markdown(f"**Assistant:** {message['content']}")
                        st.markdown("---")

                # Question input
                user_question = st.text_input(
                    "Ask about this email:",
                    placeholder="E.g., 'What's the main topic?' or 'When is the deadline?'",
                    key="ask_question_input"
                )

                # Ask button
                if st.button("Send →", use_container_width=True, key="ask_send_btn"):
                    if user_question:
                        # Add user message to history
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": user_question
                        })

                        # Get answer using enriched context
                        context = st.session_state.selected_enriched_context
                        if context:
                            try:
                                with st.spinner("Thinking..."):
                                    answer = ask_question(user_question, context)

                                if answer and not answer.startswith("Error:"):
                                    # Add assistant response to history
                                    st.session_state.chat_history.append({
                                        "role": "assistant",
                                        "content": answer
                                    })
                                    st.rerun()
                                else:
                                    st.error(f"Failed to get answer: {answer}")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                        else:
                            st.error("No context available for this email")
                    else:
                        st.warning("Please ask a question about this email")

            # ========== DRAFT FEATURE ==========
            if st.session_state.assistant_feature == "draft":
                st.markdown("#### ✉️ Draft a Reply")

                st.markdown("**What do you want to convey?**")
                intent = st.text_area(
                    "Intent:",
                    placeholder="E.g., 'Confirm the meeting time' or 'Ask for approval on budget'",
                    label_visibility="collapsed",
                    height=80,
                    key="draft_intent"
                )

                # Tone selector dropdown and character count on same line
                col_tone, col_char = st.columns([1, 1.2], gap="small")
                with col_tone:
                    selected_tone = st.selectbox(
                        "Tone:",
                        ["Professional", "Collaborative", "Assertive", "Empathetic"],
                        index=0,
                        label_visibility="collapsed",
                        key="draft_tone_selector"
                    ).lower()

                with col_char:
                    char_count = len(intent) if intent else 0
                    st.caption(f"**Tone:** {selected_tone.capitalize()} | **Characters:** {char_count} / 500")

                if st.button("Draft Reply →", use_container_width=True, key="draft_generate_btn"):
                    if intent:
                        context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                        if context:
                            try:
                                # Show processing steps
                                progress_container = st.container()
                                with progress_container:
                                    col_steps = st.columns([0.05, 0.95])
                                    with col_steps[0]:
                                        st.write("🔄")
                                    with col_steps[1]:
                                        st.write("Analyzing email...")

                                # Generate draft
                                draft = generate_draft_reply(context, intent, selected_tone.lower())

                                # Clear and update progress
                                progress_container.empty()

                                if draft and not draft.startswith("Error:"):
                                    with progress_container:
                                        st.success(f"✅ Draft generated in {selected_tone} tone")

                                    # Display draft
                                    st.markdown("**Your Draft:**")
                                    draft_html = f"""
                                    <div class="output-card">{html.escape(draft)}</div>
                                    """
                                    st.html(draft_html)

                                    # Action buttons
                                    col1, col2 = st.columns(2, gap="small")
                                    with col1:
                                        if st.button("📋 Copy", use_container_width=True, key="draft_copy_btn"):
                                            st.success("✅ Copied to clipboard!")
                                    with col2:
                                        if st.button("🔄 Try Again", use_container_width=True, key="draft_regen_btn"):
                                            st.rerun()
                                else:
                                    progress_container.empty()
                                    st.error(f"Failed to generate draft: {draft}")
                            except Exception as e:
                                st.error(f"Error generating draft: {str(e)}")
                    else:
                        st.warning("Please describe what you want to convey")

            # ========== SUMMARIZE FEATURE ==========
            elif st.session_state.assistant_feature == "summarize":
                st.markdown("#### 📊 Summarize")

                if st.button("Generate Summary", use_container_width=True, key="summarize_generate_btn"):
                    context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                    if context:
                        try:
                            with st.spinner("Analyzing thread..."):
                                summary = summarize_emails(context)

                            if summary and not summary.startswith("Error:"):
                                st.markdown("**Summary:**")
                                summary_html = f"""
                                <div class="output-card">{html.escape(summary)}</div>
                                """
                                st.html(summary_html)

                                # Copy button
                                col1, col2 = st.columns(2, gap="small")
                                with col1:
                                    if st.button("📋 Copy Summary", use_container_width=True, key="summary_copy_btn"):
                                        st.success("✅ Copied to clipboard!")
                                with col2:
                                    if st.button("🔄 Regenerate", use_container_width=True, key="summary_regen_btn"):
                                        st.rerun()
                            else:
                                st.error(f"Failed to generate summary: {summary}")
                        except Exception as e:
                            st.error(f"Error generating summary: {str(e)}")

            # ========== NO FEATURE SELECTED ==========
            else:
                st.info("👆 Click 'Draft' or 'Summarize' to get started")

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
