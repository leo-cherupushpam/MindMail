import base64
import re
from typing import List, Dict
from datetime import datetime
from email.utils import parsedate_to_datetime
import html2text
from googleapiclient.errors import HttpError

from services.models import EmailMessage, EmailThread
from services.gmail_auth import get_gmail_service
from services.qa_service import analyze_sentiment


def get_header_value(headers, header_name, default=''):
    """Extract header value from Gmail message headers"""
    for header in headers:
        if header['name'].lower() == header_name.lower():
            return header['value']
    return default


def decode_mime_message(part):
    """Decode base64-encoded MIME message part"""
    if 'data' not in part.get('body', {}):
        return ''

    try:
        data = part['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    except Exception:
        return ''


def extract_html_to_text(html_content):
    """Convert HTML email to plain text"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0

    try:
        return h.handle(html_content)
    except Exception:
        return html_content


def get_message_body(payload):
    """Extract plain text body from Gmail message payload"""
    if 'parts' in payload:
        # Multipart message
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')

            if mime_type == 'text/plain':
                return decode_mime_message(part)
            elif mime_type == 'text/html':
                html = decode_mime_message(part)
                return extract_html_to_text(html)

    # Single part message
    mime_type = payload.get('mimeType', '')
    if mime_type == 'text/plain':
        return decode_mime_message(payload)
    elif mime_type == 'text/html':
        html = decode_mime_message(payload)
        return extract_html_to_text(html)

    return ''


def get_importance_level(labels):
    """Determine importance level from Gmail labels"""
    for label in labels:
        if 'IMPORTANT' in label or 'STARRED' in label:
            return 'high'
    return 'normal'


def map_gmail_message(gmail_message: dict) -> EmailMessage:
    """
    Convert a Gmail API message to EmailMessage model.

    Args:
        gmail_message: Raw Gmail API message object

    Returns:
        EmailMessage instance
    """
    headers = gmail_message['payload'].get('headers', [])

    sender = get_header_value(headers, 'From')
    recipient = get_header_value(headers, 'To')
    subject = get_header_value(headers, 'Subject')
    date_str = get_header_value(headers, 'Date')

    # Parse date
    try:
        timestamp = parsedate_to_datetime(date_str).isoformat()
    except Exception:
        timestamp = datetime.now().isoformat()

    # Extract body
    body = get_message_body(gmail_message['payload'])

    # Detect if reply
    is_reply = subject.startswith('RE:') or subject.startswith('Fwd:')

    # Get importance
    labels = gmail_message.get('labelIds', [])
    importance_level = get_importance_level(labels)

    # Analyze sentiment (using existing service)
    sentiment = analyze_sentiment(body) if body else 'neutral'

    return EmailMessage(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        timestamp=timestamp,
        importance_level=importance_level,
        sentiment=sentiment,
        is_reply=is_reply
    )


def group_messages_by_thread(gmail_messages: List[dict]) -> Dict[str, List[dict]]:
    """Group Gmail messages by threadId"""
    threads = {}
    for msg in gmail_messages:
        thread_id = msg['threadId']
        if thread_id not in threads:
            threads[thread_id] = []
        threads[thread_id].append(msg)
    return threads


def create_email_thread(thread_id: str, gmail_messages: List[dict]) -> EmailThread:
    """
    Convert a group of Gmail messages into an EmailThread.

    Args:
        thread_id: Gmail thread ID
        gmail_messages: List of Gmail messages in the thread

    Returns:
        EmailThread instance
    """
    messages = [map_gmail_message(msg) for msg in gmail_messages]

    # Extract participants
    participants = set()
    for msg in messages:
        participants.add(msg.sender)
        participants.add(msg.recipient)
    participants.discard('')

    # Main topic is first message subject (without RE:)
    main_topic = messages[0].subject if messages else 'Unknown'
    main_topic = re.sub(r'^(RE:|FWD:)\s*', '', main_topic, flags=re.IGNORECASE)

    # Get urgency from importance levels
    importance_levels = [msg.importance_level for msg in messages]
    urgency = 'urgent' if 'high' in importance_levels else 'normal'

    return EmailThread(
        messages=messages,
        participants=sorted(list(participants)),
        main_topic=main_topic,
        underlying_need='',  # Will be filled by ContextAnalyzer
        urgency=urgency,
        action_items=[]  # Will be filled by ContextAnalyzer
    )


def fetch_all_emails(max_results=20) -> List[EmailThread]:
    """
    Fetch latest emails from Gmail and return as EmailThread list.

    Args:
        max_results: Number of messages to fetch (default 20 for quick testing)

    Returns:
        List of EmailThread objects
    """
    service = get_gmail_service()
    if not service:
        return []

    try:
        # Fetch latest messages (no pagination for simplicity)
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results
        ).execute()

        message_ids = [msg['id'] for msg in results.get('messages', [])]

        if not message_ids:
            return []

        # Get full message details
        gmail_messages = []
        for msg_id in message_ids:
            msg = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            gmail_messages.append(msg)

        # Group by thread and convert
        threads_dict = group_messages_by_thread(gmail_messages)
        all_threads = [create_email_thread(thread_id, msgs) for thread_id, msgs in threads_dict.items()]

        return all_threads

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
