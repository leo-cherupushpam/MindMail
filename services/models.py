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


@dataclass
class EnrichedContext:
    """Analyzed insights from a thread"""
    thread: EmailThread
    participants_analysis: str     # Who are key players? Relationships?
    urgency_assessment: str        # What's time-critical?
    implicit_needs: List[str]      # What's not explicitly stated but implied?
    sentiment_arc: str             # How did tone change across messages?
    professional_context: str      # Business norms and expectations
    tone_recommendations: str      # How should response sound?
    extracted_concerns: List[str]  # What worries or blocks are present?
    context_summary: str           # One-paragraph overview
