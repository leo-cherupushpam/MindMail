# Gmail Email Assistant - UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the Gmail Email Assistant from a feature-selection app into a professional 3-column email client with integrated AI assistant sidebar.

**Architecture:** Redesign `app/main.py` to use custom HTML/CSS grid layout (20/55/25 split) with four main components: sticky header toolbar, left email list, center thread viewer, and right assistant sidebar. Maintain existing services (auth, fetcher, cache, QA) and integrate them into the new layout.

**Tech Stack:** Streamlit (layout), custom HTML/CSS Grid, existing services (gmail_auth, gmail_fetcher, cache, qa_service, context_analyzer)

---

## File Structure

**Modified files:**
- `app/main.py` — Complete redesign: replace 2-column layout with 3-column grid, add header toolbar, refactor components

**New helper files:**
- `services/ui_helpers.py` — Helper functions for rendering email components (thread cards, messages, etc.)

---

## Implementation Plan

### Task 1: Set up 3-column grid layout structure

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Create HTML/CSS grid container**

In `app/main.py`, after page config and before imports, add the grid CSS:

```python
# Page configuration
st.set_page_config(
    page_title="Gmail Email Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for 3-column grid layout
st.markdown("""
<style>
    /* 3-Column Grid Layout */
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
</style>
""", unsafe_allow_html=True)
```

- [ ] **Step 2: Test CSS loads without errors**

```bash
streamlit run app/main.py
```

Expected: App loads, CSS applies (no syntax errors)

- [ ] **Step 3: Commit**

```bash
git add app/main.py
git commit -m "feat: add CSS grid layout for 3-column design"
```

---

### Task 2: Build header toolbar (sticky)

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Add header toolbar CSS and HTML**

After the grid CSS, add:

```python
st.markdown("""
<style>
    /* Header Toolbar */
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
</style>
""", unsafe_allow_html=True)
```

- [ ] **Step 2: Create toolbar HTML structure**

Add this after the CSS block:

```python
# Create toolbar container
toolbar_col1, toolbar_col2, toolbar_col3 = st.columns([2, 2, 1])

with toolbar_col1:
    st.markdown('<div class="toolbar-logo">📧 Gmail Assistant</div>', unsafe_allow_html=True)

with toolbar_col2:
    search_query = st.text_input("Search threads...", label_visibility="collapsed", key="header_search")
    st.session_state.search_query = search_query

with toolbar_col3:
    col_account, col_refresh, col_logout = st.columns(3)
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

st.markdown("---")
```

- [ ] **Step 3: Test toolbar renders**

```bash
streamlit run app/main.py
```

Expected: Header appears with logo, search, account, refresh, logout buttons

- [ ] **Step 4: Commit**

```bash
git add app/main.py
git commit -m "feat: add sticky header toolbar with search and controls"
```

---

### Task 3: Build left column - email list renderer

**Files:**
- Modify: `app/main.py`
- Create: `services/ui_helpers.py`

- [ ] **Step 1: Create email card rendering helper**

Create `services/ui_helpers.py`:

```python
from services.models import EmailThread
from datetime import datetime


def format_email_card(thread: EmailThread, is_selected: bool = False) -> str:
    """
    Render a single email thread as an HTML card.
    
    Args:
        thread: EmailThread object
        is_selected: Whether this thread is selected
    
    Returns:
        HTML string for the card
    """
    sender = thread.messages[0].sender if thread.messages else "Unknown"
    subject = thread.main_topic
    preview = thread.messages[0].body[:80] + "..." if thread.messages and thread.messages[0].body else "No content"
    timestamp = thread.messages[0].timestamp[:10] if thread.messages else "Unknown"
    
    # Truncate subject if too long
    if len(subject) > 40:
        subject = subject[:37] + "..."
    
    border_style = "border-left: 4px solid #2563EB; background-color: #DBEAFE;" if is_selected else "border: 1px solid #E5E7EB; background-color: white;"
    
    html = f"""
    <div style="
        {border_style}
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 150ms ease;
    ">
        <div style="font-weight: 700; font-size: 16px; color: #111827; margin-bottom: 4px;">{sender}</div>
        <div style="font-weight: 600; font-size: 14px; color: #111827; margin-bottom: 4px;">{subject}</div>
        <div style="font-size: 13px; color: #4B5563; margin-bottom: 8px; line-height: 1.4;">{preview}</div>
        <div style="font-size: 12px; color: #9CA3AF;">{timestamp}</div>
    </div>
    """
    return html


def format_thread_message(sender: str, email: str, timestamp: str, body: str) -> str:
    """
    Render a single message in a thread.
    
    Args:
        sender: Sender name
        email: Sender email
        timestamp: Message timestamp
        body: Message body text
    
    Returns:
        HTML string for the message
    """
    html = f"""
    <div style="margin-bottom: 24px;">
        <div style="font-weight: 700; font-size: 16px; color: #111827;">{sender}</div>
        <div style="font-size: 13px; color: #4B5563;">{email}</div>
        <div style="font-size: 13px; color: #9CA3AF; margin-bottom: 12px;">{timestamp}</div>
        <div style="font-size: 15px; color: #111827; line-height: 1.6; white-space: pre-wrap;">{body}</div>
        <hr style="margin: 24px 0; border: none; border-top: 1px solid #E5E7EB;">
    </div>
    """
    return html
```

- [ ] **Step 2: Add email list rendering to main.py**

After toolbar, add the 3-column layout with email list:

```python
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
        
        # Render email list with clickable cards
        for idx, thread in enumerate(filtered_threads):
            is_selected = (idx == st.session_state.selected_thread_idx)
            
            # Import helper at top of file
            from services.ui_helpers import format_email_card
            html_card = format_email_card(thread, is_selected)
            
            if st.button(
                html_card,
                key=f"email_card_{idx}",
                use_container_width=True,
                help="Click to select this thread"
            ):
                st.session_state.selected_thread_idx = idx
                st.session_state.chat_history = []  # Clear chat for new thread
                st.rerun()
    else:
        st.info("📭 No emails. Click 'Refresh' to fetch emails.")
```

- [ ] **Step 3: Test email list renders**

```bash
streamlit run app/main.py
```

Expected: Left column shows email list with 20 threads (or mock data if not authenticated)

- [ ] **Step 4: Commit**

```bash
git add services/ui_helpers.py app/main.py
git commit -m "feat: add email list rendering in left column"
```

---

### Task 4: Build center column - thread viewer

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Add thread viewer to center column**

In the center column section of main.py:

```python
# CENTER COLUMN: THREAD VIEWER
with col_thread:
    if st.session_state.authenticated and st.session_state.email_threads:
        if 0 <= st.session_state.selected_thread_idx < len(st.session_state.email_threads):
            selected_thread = st.session_state.email_threads[st.session_state.selected_thread_idx]
            
            # Thread header
            st.markdown(f"## {selected_thread.main_topic}")
            st.caption(f"{len(selected_thread.messages)} messages from {len(selected_thread.participants)} participants")
            st.caption(f"**Participants:** {', '.join(selected_thread.participants)}")
            st.markdown("---")
            
            # Thread messages (chronological, oldest to newest)
            from services.ui_helpers import format_thread_message
            for message in selected_thread.messages:
                html_msg = format_thread_message(
                    sender=message.sender,
                    email=message.sender,  # Using sender as email for now
                    timestamp=message.timestamp,
                    body=message.body
                )
                st.markdown(html_msg, unsafe_allow_html=True)
            
            # Update enriched context for selected thread
            enriched = st.session_state.analyzer.analyze_thread(selected_thread)
            if 'selected_enriched_context' not in st.session_state:
                st.session_state.selected_enriched_context = enriched
            else:
                st.session_state.selected_enriched_context = enriched
        else:
            st.info("Select an email thread from the list")
    else:
        st.info("📭 Authenticate and refresh to view emails")
```

- [ ] **Step 2: Test thread viewer renders**

```bash
streamlit run app/main.py
```

Expected: Center column shows selected thread with header, participants, and all messages in chronological order

- [ ] **Step 3: Commit**

```bash
git add app/main.py
git commit -m "feat: add thread viewer in center column with chronological messages"
```

---

### Task 5: Build right column - assistant sidebar with tabs

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Add assistant sidebar with tabbed interface**

In the right column section:

```python
# RIGHT COLUMN: ASSISTANT SIDEBAR
with col_assistant:
    if st.session_state.authenticated and st.session_state.email_threads:
        if 0 <= st.session_state.selected_thread_idx < len(st.session_state.email_threads):
            selected_thread = st.session_state.email_threads[st.session_state.selected_thread_idx]
            
            # Context indicator
            st.markdown(f"📧 **Analyzing:** {selected_thread.main_topic[:40]}...")
            st.markdown("---")
            
            # Tabbed interface
            tab_ask, tab_summarize, tab_draft = st.tabs(["💬 Ask", "📝 Summarize", "✉️ Draft"])
            
            # ASK TAB
            with tab_ask:
                st.session_state.assistant_tab = "ask"
                user_query = st.text_area(
                    "Ask about this email:",
                    placeholder="What was the main topic?",
                    label_visibility="collapsed",
                    height=100,
                    key="ask_input"
                )
                
                if st.button("Ask", use_container_width=True, key="ask_button"):
                    if user_query:
                        context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                        if context:
                            with st.spinner("Thinking..."):
                                response = ask_question(user_query, context)
                            st.session_state.chat_history.append({"role": "user", "content": user_query})
                            st.session_state.chat_history.append({"role": "assistant", "content": response})
                            st.rerun()
                
                # Display chat history
                if st.session_state.chat_history:
                    st.markdown("**Conversation:**")
                    for msg in st.session_state.chat_history:
                        if msg["role"] == "user":
                            st.markdown(f"**You:** {msg['content']}")
                        else:
                            st.markdown(f"**Assistant:** {msg['content']}")
            
            # SUMMARIZE TAB
            with tab_summarize:
                st.session_state.assistant_tab = "summarize"
                if st.button("Generate Summary", use_container_width=True, key="summarize_button"):
                    context = st.session_state.selected_enriched_context if 'selected_enriched_context' in st.session_state else None
                    if context:
                        with st.spinner("Summarizing..."):
                            summary = summarize_emails(context)
                        st.markdown("**Summary:**")
                        st.write(summary)
                        
                        if st.button("📋 Copy Summary", use_container_width=True, key="copy_summary"):
                            st.success("Copied to clipboard!")
            
            # DRAFT TAB
            with tab_draft:
                st.session_state.assistant_tab = "draft"
                intent = st.text_area(
                    "What do you want to say?",
                    placeholder="e.g., Approve the budget",
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
                            with st.spinner("Drafting..."):
                                draft = generate_draft_reply(context, intent, tone.lower())
                            st.markdown("**Your Draft:**")
                            st.text_area(
                                "Edit and copy:",
                                value=draft,
                                height=150,
                                disabled=True,
                                label_visibility="collapsed"
                            )
                            
                            if st.button("📋 Copy Draft", use_container_width=True, key="copy_draft"):
                                st.success("Copied to clipboard!")
        else:
            st.info("Select an email to analyze")
    else:
        st.info("📭 Authenticate to use assistant")
```

- [ ] **Step 2: Test assistant sidebar**

```bash
streamlit run app/main.py
```

Expected: Right column shows tabbed assistant with Ask, Summarize, Draft tabs functional

- [ ] **Step 3: Commit**

```bash
git add app/main.py
git commit -m "feat: add assistant sidebar with tabbed interface (Ask/Summarize/Draft)"
```

---

### Task 6: Add CSS styling polish

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Enhance CSS for professional appearance**

Add to the CSS block in main.py (expand existing styles):

```python
st.markdown("""
<style>
    /* Enhanced styling for professional appearance */
    
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
    
    /* Button styling */
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
```

- [ ] **Step 2: Test styling looks professional**

```bash
streamlit run app/main.py
```

Expected: App has polish - hover effects, proper spacing, professional appearance

- [ ] **Step 3: Commit**

```bash
git add app/main.py
git commit -m "style: add CSS polish for professional appearance"
```

---

### Task 7: Clean up old code and finalize

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Remove old feature card code**

Remove the old FEATURES list, feature cards, and feature-specific sections that are no longer needed. Keep only:
- Imports
- Page config
- CSS (grid + styling)
- Initialization
- Toolbar
- 3-column layout with email list, thread viewer, and sidebar

Remove:
- Old `st.columns([1, 4])` layout code
- Feature card selection code
- Old feature-specific implementations
- Settings section (moved to toolbar)

- [ ] **Step 2: Verify all necessary imports are present**

Ensure these are imported at the top:
```python
import os
import sys
import streamlit as st
from datetime import datetime

from services.qa_service import ask_question, summarize_emails, generate_draft_reply
from services.context_analyzer import ContextAnalyzer
from services.mock_data import get_sample_threads
from services.gmail_auth import is_authenticated, start_oauth_flow, logout
from services.gmail_fetcher import fetch_all_emails
from services.cache import load_cache, save_cache, is_cache_valid
from services.ui_helpers import format_email_card, format_thread_message
from utils import with_spinner, primary_button, add_chat_exchange, show_success_box
```

- [ ] **Step 3: Test app runs without errors**

```bash
streamlit run app/main.py
```

Expected: No errors, clean 3-column layout appears

- [ ] **Step 4: Test end-to-end workflow**

1. Authenticate (if not already)
2. Refresh emails
3. Click on an email thread
4. Thread displays in center
5. Ask a question in sidebar
6. Get response
7. Switch to Summarize tab
8. Switch to Draft tab

Expected: All features work smoothly

- [ ] **Step 5: Commit final version**

```bash
git add app/main.py
git commit -m "refactor: clean up old code and finalize UI redesign"
```

---

### Task 8: Test on real Gmail and document

**Files:**
- No code changes (testing task)

- [ ] **Step 1: Full manual testing workflow**

1. Set up Gmail credentials if needed (from GMAIL_SETUP.md)
2. Run app: `streamlit run app/main.py`
3. Authenticate with Gmail
4. Click "Refresh" in header
5. Verify 20 emails load in left column
6. Select different threads - verify center and right update
7. Test search in header
8. Ask questions in sidebar
9. Generate summaries
10. Generate draft replies
11. Click logout

Expected: All features work, UI is responsive, no errors

- [ ] **Step 2: Check for performance issues**

- Email list renders quickly
- Thread viewer doesn't lag with large messages
- Assistant responds in reasonable time
- No unnecessary reloads

- [ ] **Step 3: Document any issues found**

If issues found, note them and create follow-up tasks

- [ ] **Step 4: Note completion**

Commit a note:
```bash
git add -A
git commit -m "test: manual testing complete - UI redesign fully functional"
```

---

## Summary

**8 Implementation Tasks:**
1. Set up 3-column grid layout
2. Build header toolbar
3. Build email list renderer
4. Build thread viewer
5. Build assistant sidebar with tabs
6. Add CSS styling polish
7. Clean up old code
8. Manual testing and finalization

**Total scope:** Replace current main.py with professional 3-column email client UI
