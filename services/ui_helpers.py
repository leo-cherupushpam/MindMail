import html
from datetime import datetime
from services.models import EmailThread


def format_email_card(thread: EmailThread, is_selected: bool = False, urgency: str = "normal", action_items: list = None) -> str:
    """
    Render a single email thread as an HTML card with urgency indicators.

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
    message_count = len(thread.messages)

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
    if len(subject) > 40:
        subject = subject[:37] + "..."

    # Escape all user data to prevent XSS vulnerabilities
    sender = html.escape(sender)
    subject = html.escape(subject)
    preview = html.escape(preview)

    # Determine accent color and icon based on urgency
    if "urgent" in urgency.lower():
        accent_color = "#EF4444"  # Red
        urgency_icon = "🔴"
    elif action_items:
        accent_color = "#F59E0B"  # Orange
        urgency_icon = "📌"
    else:
        accent_color = "#10B981"  # Green
        urgency_icon = "📄"

    # Determine card styling based on selection state
    if is_selected:
        background = "#F0F7FF"
        border = f"4px solid #2563EB"
        shadow = "0 10px 25px rgba(37, 99, 235, 0.2)"
    else:
        background = "white"
        border = f"4px solid {accent_color}; border-right: 1px solid #E5E7EB; border-top: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB;"
        shadow = "0 1px 3px rgba(0,0,0,0.08)"

    html_content = f"""
    <div class="email-card" style="
        border-left: {border};
        background-color: {background};
        border-radius: 8px;
        padding: 16px;
        margin: 8px;
        cursor: pointer;
        box-shadow: {shadow};
        transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    ">
        <!-- Sender with urgency icon -->
        <div style="font-weight: 700; font-size: 16px; color: #111827; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <span>{urgency_icon}</span>
            <span>{sender}</span>
        </div>

        <!-- Subject (prominent) -->
        <div style="font-weight: 600; font-size: 14px; color: #111827; margin-bottom: 8px; line-height: 1.4;">{subject}</div>

        <!-- Preview -->
        <div style="font-size: 13px; color: #4B5563; margin-bottom: 12px; line-height: 1.4;">{preview}</div>

        <!-- Footer metadata -->
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #9CA3AF;">
            <span>{timestamp}</span>
            <span>{message_count} message{'s' if message_count != 1 else ''}</span>
        </div>
    </div>
    """
    return html_content


def format_thread_message(sender: str, email: str, timestamp: str, body: str) -> str:
    """
    Render a single message in a thread.

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
    <div style="margin-bottom: 24px;">
        <div style="font-weight: 700; font-size: 16px; color: #111827;">{sender}</div>
        <div style="font-size: 14px; color: #4B5563;">{email}</div>
        <div style="font-size: 14px; color: #9CA3AF; margin-bottom: 12px;">{formatted_timestamp}</div>
        <div style="font-size: 16px; color: #111827; line-height: 1.75; white-space: pre-wrap; word-break: break-word;">{body}</div>
        <hr style="margin: 24px 0; border: none; border-top: 1px solid #E5E7EB;">
    </div>
    """
    return html_content
