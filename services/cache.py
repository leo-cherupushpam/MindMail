import os
import json
from typing import List
from services.models import EmailThread, EmailMessage


def get_cache_path():
    """Return the path to cached_emails.json"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cached_emails.json')


def is_cache_valid():
    """Check if cache file exists"""
    cache_path = get_cache_path()
    return os.path.exists(cache_path)


def load_cache() -> List[EmailThread]:
    """Load email threads from cache file"""
    cache_path = get_cache_path()

    if not os.path.exists(cache_path):
        return []

    try:
        with open(cache_path, 'r') as f:
            data = json.load(f)

        threads = []
        for thread_data in data:
            messages = [
                EmailMessage(
                    sender=msg['sender'],
                    recipient=msg['recipient'],
                    subject=msg['subject'],
                    body=msg['body'],
                    timestamp=msg['timestamp'],
                    importance_level=msg['importance_level'],
                    sentiment=msg['sentiment'],
                    is_reply=msg['is_reply']
                )
                for msg in thread_data['messages']
            ]

            thread = EmailThread(
                messages=messages,
                participants=thread_data['participants'],
                main_topic=thread_data['main_topic'],
                underlying_need=thread_data['underlying_need'],
                urgency=thread_data['urgency'],
                action_items=thread_data['action_items']
            )
            threads.append(thread)

        return threads
    except (json.JSONDecodeError, KeyError, ValueError):
        # Cache corrupted, return empty
        return []


def save_cache(threads: List[EmailThread]):
    """Save email threads to cache file"""
    cache_path = get_cache_path()

    data = []
    for thread in threads:
        thread_dict = {
            'messages': [
                {
                    'sender': msg.sender,
                    'recipient': msg.recipient,
                    'subject': msg.subject,
                    'body': msg.body,
                    'timestamp': msg.timestamp,
                    'importance_level': msg.importance_level,
                    'sentiment': msg.sentiment,
                    'is_reply': msg.is_reply
                }
                for msg in thread.messages
            ],
            'participants': thread.participants,
            'main_topic': thread.main_topic,
            'underlying_need': thread.underlying_need,
            'urgency': thread.urgency,
            'action_items': thread.action_items
        }
        data.append(thread_dict)

    with open(cache_path, 'w') as f:
        json.dump(data, f, indent=2)


def clear_cache():
    """Delete cache file"""
    cache_path = get_cache_path()
    if os.path.exists(cache_path):
        os.remove(cache_path)


def get_cache_metadata():
    """Get cache metadata (last modified, thread count)"""
    cache_path = get_cache_path()

    if not os.path.exists(cache_path):
        return {'exists': False, 'thread_count': 0}

    threads = load_cache()
    stat = os.stat(cache_path)

    return {
        'exists': True,
        'thread_count': len(threads),
        'last_modified': stat.st_mtime,
        'file_size_kb': stat.st_size / 1024
    }
