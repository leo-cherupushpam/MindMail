import pytest
from unittest.mock import MagicMock, patch
from services.gmail_fetcher import (
    map_gmail_message,
    group_messages_by_thread,
    fetch_all_emails
)


def test_map_gmail_message_extracts_basic_fields():
    """Test that map_gmail_message extracts sender, recipient, subject"""
    gmail_msg = {
        'id': 'msg123',
        'threadId': 'thread123',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'alice@example.com'},
                {'name': 'To', 'value': 'bob@example.com'},
                {'name': 'Subject', 'value': 'Meeting Notes'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 10:00:00 +0000'}
            ],
            'parts': [
                {'mimeType': 'text/plain', 'body': {'data': 'TWVldGluZyB3YXMgZ3JlYXQ='}}
            ]
        },
        'labelIds': []
    }

    result = map_gmail_message(gmail_msg)

    assert result.sender == 'alice@example.com'
    assert result.recipient == 'bob@example.com'
    assert result.subject == 'Meeting Notes'


def test_map_gmail_message_detects_reply():
    """Test that map_gmail_message detects RE: prefix as reply"""
    gmail_msg = {
        'id': 'msg123',
        'threadId': 'thread123',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'alice@example.com'},
                {'name': 'To', 'value': 'bob@example.com'},
                {'name': 'Subject', 'value': 'RE: Meeting Notes'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 10:00:00 +0000'}
            ],
            'parts': [
                {'mimeType': 'text/plain', 'body': {'data': 'dGhhbmtz'}}
            ]
        },
        'labelIds': []
    }

    result = map_gmail_message(gmail_msg)
    assert result.is_reply is True


def test_group_messages_by_thread_groups_by_thread_id():
    """Test that messages are grouped by threadId"""
    msg1 = {
        'id': 'msg1',
        'threadId': 'thread123',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'alice@example.com'},
                {'name': 'To', 'value': 'bob@example.com'},
                {'name': 'Subject', 'value': 'Hello'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 10:00:00 +0000'}
            ],
            'parts': []
        },
        'labelIds': []
    }

    msg2 = {
        'id': 'msg2',
        'threadId': 'thread123',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'bob@example.com'},
                {'name': 'To', 'value': 'alice@example.com'},
                {'name': 'Subject', 'value': 'RE: Hello'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 11:00:00 +0000'}
            ],
            'parts': []
        },
        'labelIds': []
    }

    msg3 = {
        'id': 'msg3',
        'threadId': 'thread456',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'charlie@example.com'},
                {'name': 'To', 'value': 'dave@example.com'},
                {'name': 'Subject', 'value': 'Another thread'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 12:00:00 +0000'}
            ],
            'parts': []
        },
        'labelIds': []
    }

    result = group_messages_by_thread([msg1, msg2, msg3])

    assert len(result) == 2
    assert 'thread123' in result
    assert 'thread456' in result
    assert len(result['thread123']) == 2
    assert len(result['thread456']) == 1
