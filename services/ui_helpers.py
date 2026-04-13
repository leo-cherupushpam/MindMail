import html
from datetime import datetime
from services.models import EmailThread, EnrichedContext


def format_email_card(thread: EmailThread, is_selected: bool = False, urgency: str = "normal", action_items: list = None) -> str:
    """
    Render a single email thread as a clean, Gmail-like card.

    Args:
        thread: EmailThread object
        is_selected: Whether this thread is selected
        urgency: Thread urgency level ("urgent", "normal", "low")
        action_items: List of action items in thread (optional)

    Returns:
        HTML string for the card
    """
    if action_items is None:
        action_items = []

    sender = thread.messages[0].sender if thread.messages else "Unknown"
    subject = thread.main_topic
    preview = thread.messages[0].body[:80] + "..." if thread.messages and thread.messages[0].body else "No content"

    # Parse and format timestamp from ISO format
    if thread.messages and thread.messages[0].timestamp:
        try:
            dt = datetime.fromisoformat(thread.messages[0].timestamp.replace('Z', '+00:00'))
            timestamp = dt.strftime("%b %d")
        except (ValueError, AttributeError):
            timestamp = "Unknown"
    else:
        timestamp = "Unknown"

    # Truncate subject if too long
    if len(subject) > 50:
        subject = subject[:47] + "..."

    # Escape all user data to prevent XSS vulnerabilities
    sender = html.escape(sender)
    subject = html.escape(subject)
    preview = html.escape(preview)

    # Determine card styling based on selection state
    if is_selected:
        background = "#E3F2FD"
        border = "2px solid #2563EB"
        shadow = "0 2px 8px rgba(37, 99, 235, 0.15)"
    else:
        background = "white"
        border = "1px solid #E5E7EB"
        shadow = "0 1px 2px rgba(0,0,0,0.05)"

    # Determine urgency badge styling
    if "urgent" in urgency.lower() or "high" in urgency.lower():
        urgency_icon = "🔴"
        urgency_color = "#DC2626"
        urgency_bg = "#FEE2E2"
        urgency_text = "High"
    elif "medium" in urgency.lower() or "normal" in urgency.lower():
        urgency_icon = "🟡"
        urgency_color = "#D97706"
        urgency_bg = "#FEF3C7"
        urgency_text = "Medium"
    else:
        urgency_icon = "⚪"
        urgency_color = "#9CA3AF"
        urgency_bg = "#F3F4F6"
        urgency_text = "Low"

    html_content = f"""
    <div style="
        background-color: {background};
        border: {border};
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        cursor: pointer;
        box-shadow: {shadow};
        transition: all 150ms ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <div style="font-weight: 600; font-size: 15px; color: #111827; flex: 1;">{sender}</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
            <div style="font-size: 14px; color: #374151; flex: 1; margin-right: 12px; line-height: 1.3;">{subject}</div>
            <div style="font-size: 12px; color: #9CA3AF; white-space: nowrap;">{timestamp}</div>
        </div>
        <div style="font-size: 13px; color: #6B7280; line-height: 1.4; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{preview}</div>
    </div>
    """
    return html_content


def format_thread_message(sender: str, email: str, timestamp: str, body: str) -> str:
    """
    Render a single message in a thread (Gmail-like format).

    Args:
        sender: Sender name
        email: Sender email
        timestamp: Message timestamp (ISO format, e.g., "2026-04-08T09:15:00Z")
        body: Message body text

    Returns:
        HTML string for the message
    """
    # Parse and format timestamp
    formatted_timestamp = timestamp
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_timestamp = dt.strftime("%b %d, %I:%M %p")  # e.g., "Apr 10, 2:30 PM"
    except (ValueError, AttributeError):
        formatted_timestamp = timestamp  # Fallback to original format if parsing fails

    # Escape all user data to prevent XSS vulnerabilities
    sender = html.escape(sender)
    email = html.escape(email)
    body = html.escape(body)

    html_content = f"""
    <div style="
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 16px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <div>
                <div style="font-weight: 600; font-size: 15px; color: #111827;">{sender}</div>
                <div style="font-size: 13px; color: #6B7280;">{email}</div>
            </div>
            <div style="font-size: 12px; color: #9CA3AF; text-align: right; white-space: nowrap;">{formatted_timestamp}</div>
        </div>
        <div style="
            font-size: 14px;
            color: #374151;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
            border-top: 1px solid #F3F4F6;
            padding-top: 12px;
        ">{body}</div>
    </div>
    """
    return html_content


def format_context_panel(enriched_context: EnrichedContext) -> str:
    """
    Render the context panel showing urgency, sentiment, key needs, and participants.

    Args:
        enriched_context: EnrichedContext object with analyzed email insights

    Returns:
        HTML string for the context panel
    """
    # Extract values with safe defaults
    urgency = enriched_context.urgency_assessment if enriched_context.urgency_assessment else "normal"
    sentiment_arc = enriched_context.sentiment_arc if enriched_context.sentiment_arc else "unknown"
    participants = enriched_context.thread.participants if enriched_context.thread.participants else []
    implicit_needs = enriched_context.implicit_needs if enriched_context.implicit_needs else []

    # Determine urgency badge styling
    if "urgent" in urgency.lower():
        urgency_icon = "🔴"
        urgency_bg = "#FEE2E2"
        urgency_text = "High"
    elif "high" in urgency.lower():
        urgency_icon = "🔴"
        urgency_bg = "#FEE2E2"
        urgency_text = "High"
    elif "medium" in urgency.lower() or "normal" in urgency.lower():
        urgency_icon = "🟡"
        urgency_bg = "#FEF3C7"
        urgency_text = "Medium"
    else:
        urgency_icon = "⚪"
        urgency_bg = "#F3F4F6"
        urgency_text = "Low"

    # Determine sentiment emoji
    if "positive" in sentiment_arc.lower():
        sentiment_emoji = "😊"
    elif "negative" in sentiment_arc.lower():
        sentiment_emoji = "😟"
    else:
        sentiment_emoji = "😐"

    # Get first key need or use generic placeholder
    key_need = implicit_needs[0] if implicit_needs else "Follow-up"
    key_need = html.escape(key_need)[:30]  # Truncate to 30 chars

    # Format participants list
    participants_text = ", ".join(html.escape(p) for p in participants[:3])
    if len(participants) > 3:
        participants_text += f", +{len(participants)-3} more"

    html_content = f"""
    <div style="
        background-color: #F9FAFB;
        border-bottom: 1px solid #E5E7EB;
        padding: 16px;
        margin-bottom: 16px;
        border-radius: 6px;
    ">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 13px;">
            <!-- Urgency Badge -->
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 600; color: #6B7280;">Urgency:</span>
                <div style="
                    background-color: {urgency_bg};
                    padding: 4px 8px;
                    border-radius: 4px;
                    color: #991B1B;
                    font-weight: 600;
                ">
                    {urgency_icon} {urgency_text}
                </div>
            </div>

            <!-- Sentiment Badge -->
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 600; color: #6B7280;">Sentiment:</span>
                <div style="color: #4B5563;">
                    {sentiment_emoji} {sentiment_arc[:20]}
                </div>
            </div>

            <!-- Key Need -->
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 600; color: #6B7280;">Key Need:</span>
                <div style="
                    background-color: #DBEAFE;
                    padding: 4px 8px;
                    border-radius: 4px;
                    color: #2563EB;
                    font-weight: 600;
                ">
                    {key_need}
                </div>
            </div>

            <!-- Participants -->
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 600; color: #6B7280;">Participants:</span>
                <div style="color: #4B5563;">
                    [{len(participants)}] {participants_text}
                </div>
            </div>
        </div>
    </div>
    """
    return html_content


def format_tone_example(tone: str) -> str:
    """
    Return an example draft response for a given tone.

    Args:
        tone: Tone type ("professional", "collaborative", "assertive", "empathetic")

    Returns:
        Example draft string
    """
    examples = {
        "professional": "Thank you for reaching out. I appreciate your input and will review the details carefully. I'll have a response for you by Friday.",
        "collaborative": "Got it—great points! Let's sync up to align on next steps. I'm thinking we could tackle this together.",
        "assertive": "I understand the urgency. Here's what I can commit to: completion by Friday. I'll need X and Y from your team to proceed.",
        "empathetic": "I hear you, and I understand how important this is. I'm here to help. Let me dig into this and get you an answer soon."
    }
    return examples.get(tone.lower(), examples["professional"])


AVATAR_COLORS = [
    "#1A73E8",  # blue
    "#34A853",  # green
    "#EA4335",  # red
    "#FBBC04",  # yellow
    "#FF6D00",  # orange
    "#9C27B0",  # purple
    "#00ACC1",  # teal
    "#F06292",  # pink
]


def get_avatar_html(sender: str, size: int = 40) -> str:
    """Return an HTML colored circle avatar with the sender's initial."""
    initial = sender[0].upper() if sender else "?"
    color = AVATAR_COLORS[ord(initial) % len(AVATAR_COLORS)]
    return (
        f'<div class="gmail-avatar" style="width:{size}px;height:{size}px;background:{color};">'
        f'{html.escape(initial)}</div>'
    )


def render_top_bar() -> str:
    """Return the static Gmail top bar HTML."""
    return """
    <div class="gmail-topbar">
        <span style="font-size:20px; color:#5F6368; cursor:pointer;">☰</span>
        <div class="gmail-logo">
            <span>G</span>mail
        </div>
        <div class="gmail-search">
            🔍&nbsp;&nbsp;Search mail
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-left:auto; color:#5F6368; font-size:20px; padding-left:16px;">
            <span style="cursor:pointer;">?</span>
            <span style="cursor:pointer;">⚙</span>
            <span style="cursor:pointer;">✦</span>
            <div style="width:32px;height:32px;border-radius:50%;background:#1A73E8;display:flex;align-items:center;justify-content:center;color:white;font-size:14px;cursor:pointer;">L</div>
        </div>
    </div>
    """


def render_left_nav(inbox_count: int = 14) -> str:
    """Return the static Gmail left navigation HTML."""
    return f"""
    <div class="gmail-nav">
        <button class="gmail-compose">✏️&nbsp;&nbsp;Compose</button>
        <div class="gmail-nav-item active">
            <span>📥 Inbox</span>
            <span class="gmail-nav-count">{inbox_count}</span>
        </div>
        <div class="gmail-nav-item"><span>⭐ Starred</span></div>
        <div class="gmail-nav-item"><span>🕐 Snoozed</span></div>
        <div class="gmail-nav-item"><span>📤 Sent</span></div>
        <div class="gmail-nav-item">
            <span>📝 Drafts</span>
            <span class="gmail-nav-count">3</span>
        </div>
        <div class="gmail-nav-item">
            <span>🚫 Spam</span>
            <span class="gmail-nav-count">12</span>
        </div>
        <div class="gmail-nav-item"><span>🗑️ Trash</span></div>
        <div class="gmail-nav-item"><span>▾ More</span></div>
        <div class="gmail-nav-section">Labels</div>
        <div class="gmail-nav-item"><span>🏷️ Work</span></div>
    </div>
    """


def render_inbox_row(thread: EmailThread, is_unread: bool = True) -> str:
    """Return a single Gmail-style email list row as HTML."""
    sender_raw = thread.messages[0].sender.split("@")[0].replace(".", " ").title() if thread.messages else "Unknown"
    sender = html.escape(sender_raw)
    subject = html.escape(thread.main_topic[:60])
    snippet = html.escape(thread.messages[0].body[:80].replace("\n", " ")) if thread.messages else ""
    snippet = snippet + "..." if len(thread.messages[0].body) > 80 else snippet

    # Format timestamp
    timestamp = ""
    if thread.messages and thread.messages[0].timestamp:
        try:
            dt = datetime.fromisoformat(thread.messages[0].timestamp.replace("Z", "+00:00"))
            now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
            diff = now - dt
            if diff.days == 0:
                timestamp = dt.strftime("%-I:%M %p")
            elif diff.days < 7:
                timestamp = dt.strftime("%a")
            else:
                timestamp = dt.strftime("%b %d")
        except (ValueError, AttributeError):
            timestamp = ""

    read_class = "unread" if is_unread else "read"

    return f"""
    <div class="gmail-row {read_class}">
        <span style="color:#5F6368; flex-shrink:0;">☐</span>
        <span style="color:#5F6368; flex-shrink:0;">☆</span>
        <div class="gmail-row-sender {read_class}">{sender}</div>
        <div class="gmail-row-subject {read_class}">
            {subject}
            <span class="gmail-row-snippet">&nbsp;– {snippet}</span>
        </div>
        <div class="gmail-row-time {read_class}">{timestamp}</div>
    </div>
    """


def render_reading_pane_message(sender: str, email_addr: str, timestamp: str, body: str) -> str:
    """Return a single message bubble in the Gmail reading pane."""
    # Format timestamp
    formatted_ts = timestamp
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        formatted_ts = dt.strftime("%a, %b %d, %Y, %-I:%M %p")
    except (ValueError, AttributeError):
        pass

    avatar = get_avatar_html(sender)
    sender_display = html.escape(sender.split("@")[0].replace(".", " ").title())
    email_display = html.escape(email_addr)
    body_escaped = html.escape(body)

    return f"""
    <div class="gmail-message">
        <div class="gmail-message-header">
            {avatar}
            <div>
                <div class="gmail-sender-name">{sender_display}</div>
                <div class="gmail-sender-email">&lt;{email_display}&gt;</div>
            </div>
            <div class="gmail-message-time">{html.escape(formatted_ts)}</div>
        </div>
        <div class="gmail-message-body">{body_escaped}</div>
    </div>
    """
