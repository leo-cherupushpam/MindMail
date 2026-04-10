import pytest
from services.context_analyzer import ContextAnalyzer
from services.models import EmailMessage, EmailThread


def test_context_analyzer_creation():
    """ContextAnalyzer should instantiate without arguments"""
    analyzer = ContextAnalyzer()
    assert analyzer is not None


def test_analyze_thread_returns_enriched_context():
    """analyze_thread should return EnrichedContext"""
    from services.models import EnrichedContext

    analyzer = ContextAnalyzer()
    msg = EmailMessage(
        sender="alice@example.com",
        recipient="bob@example.com",
        subject="Q1 Budget",
        body="I've compiled the Q1 budget with projections...",
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

    result = analyzer.analyze_thread(thread)
    assert isinstance(result, EnrichedContext)
    assert result.thread == thread
