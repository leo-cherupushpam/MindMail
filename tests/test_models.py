import pytest
from dataclasses import is_dataclass
from services.models import EmailMessage, EmailThread, EnrichedContext


def test_email_message_is_dataclass():
    """EmailMessage should be a dataclass with required fields"""
    assert is_dataclass(EmailMessage)


def test_email_message_creation():
    """Should create EmailMessage with all required fields"""
    msg = EmailMessage(
        sender="alice@example.com",
        recipient="bob@example.com",
        subject="Test Subject",
        body="Test body content",
        timestamp="2026-04-10T10:00:00Z",
        importance_level="high",
        sentiment="positive",
        is_reply=False
    )
    assert msg.sender == "alice@example.com"
    assert msg.importance_level == "high"
    assert msg.sentiment == "positive"
    assert msg.is_reply == False


def test_email_thread_creation():
    """Should create EmailThread with messages and metadata"""
    msg1 = EmailMessage(
        sender="alice@example.com",
        recipient="bob@example.com",
        subject="Q1 Budget",
        body="I've compiled the Q1 budget...",
        timestamp="2026-04-08T10:00:00Z",
        importance_level="high",
        sentiment="urgent",
        is_reply=False
    )

    thread = EmailThread(
        messages=[msg1],
        participants=["alice@example.com", "bob@example.com"],
        main_topic="Q1 Budget Approval",
        underlying_need="Secure CFO approval for proposed budget",
        urgency="high",
        action_items=["Get CFO sign-off by Friday"]
    )

    assert len(thread.messages) == 1
    assert thread.main_topic == "Q1 Budget Approval"
    assert thread.urgency == "high"


def test_enriched_context_creation():
    """EnrichedContext should hold analyzed insights"""
    msg = EmailMessage(
        sender="alice@example.com",
        recipient="bob@example.com",
        subject="Q1 Budget",
        body="I've compiled the Q1 budget...",
        timestamp="2026-04-08T10:00:00Z",
        importance_level="high",
        sentiment="urgent",
        is_reply=False
    )

    thread = EmailThread(
        messages=[msg],
        participants=["alice@example.com", "bob@example.com"],
        main_topic="Q1 Budget Approval",
        underlying_need="Secure CFO approval for proposed budget",
        urgency="high",
        action_items=["Get CFO sign-off by Friday"]
    )

    enriched = EnrichedContext(
        thread=thread,
        participants_analysis="Alice (Finance Manager) requesting approval from Bob (CFO)",
        urgency_assessment="Deadline Friday - time-critical decision",
        implicit_needs=["Historical data justification", "Risk analysis"],
        sentiment_arc="Urgent → Cautious → Collaborative",
        professional_context="Budget approval process with stakeholder concerns",
        tone_recommendations="Professional, data-driven, confidence-building",
        extracted_concerns=["Contingency allocation methodology", "Budget overruns"],
        context_summary="Alice proposes Q1 budget to CFO with Friday deadline. CFO concerned about contingency justification."
    )

    assert enriched.thread == thread
    assert enriched.urgency_assessment == "Deadline Friday - time-critical decision"
