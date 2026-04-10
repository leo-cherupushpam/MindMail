from dataclasses import dataclass
from typing import List


@dataclass
class EmailMessage:
    """Single email in a thread"""
    sender: str
    recipient: str
    subject: str
    body: str
    timestamp: str
    importance_level: str      # "high", "normal", "low"
    sentiment: str             # "positive", "neutral", "negative"
    is_reply: bool


@dataclass
class EmailThread:
    """Conversation of related emails"""
    messages: List[EmailMessage]
    participants: List[str]
    main_topic: str
    underlying_need: str       # What's really being asked?
    urgency: str              # "urgent", "normal", "low"
    action_items: List[str]
