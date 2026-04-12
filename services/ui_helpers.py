import html
from datetime import datetime
from services.models import EmailThread


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
        border = "1px solid #2563EB"
        shadow = "0 2px 8px rgba(37, 99, 235, 0.15)"
    else:
        background = "white"
        border = "1px solid #E5E7EB"
        shadow = "0 1px 2px rgba(0,0,0,0.05)"

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
        <div style="font-weight: 600; font-size: 15px; color: #111827; margin-bottom: 4px;">{sender}</div>
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
