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
