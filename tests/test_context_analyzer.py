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


def test_analyze_participants_with_role_inference():
    """Should infer roles from context and email patterns"""
    analyzer = ContextAnalyzer()

    msg1 = EmailMessage(
        sender="sarah@company.com",
        recipient="cfo@company.com",
        subject="Q1 Budget - Need approval by Friday",
        body="Hi CFO, I've compiled the Q1 budget with projections...",
        timestamp="2026-04-08T10:00:00Z",
        importance_level="high",
        sentiment="urgent",
        is_reply=False
    )

    thread = EmailThread(
        messages=[msg1],
        participants=["sarah@company.com", "cfo@company.com"],
        main_topic="Q1 Budget Approval",
        underlying_need="Secure CFO approval for proposed budget",
        urgency="high",
        action_items=["Get CFO sign-off by Friday"]
    )

    result = analyzer._analyze_participants(thread)
    assert "Sarah" in result or "Finance" in result or "role" in result.lower()


def test_extract_needs_includes_implicit():
    """Should extract both explicit and implicit needs"""
    analyzer = ContextAnalyzer()

    thread = EmailThread(
        messages=[],
        participants=["alice@example.com", "bob@example.com"],
        main_topic="Q1 Budget Approval",
        underlying_need="Secure CFO approval for proposed budget",
        urgency="high",
        action_items=["Get CFO sign-off by Friday"]
    )

    needs = analyzer._extract_needs(thread)
    assert len(needs) > 0
    assert "approval" in " ".join(needs).lower() or "budget" in " ".join(needs).lower()


def test_sentiment_arc_with_multiple_messages():
    """Should track sentiment changes across messages"""
    analyzer = ContextAnalyzer()

    msgs = [
        EmailMessage(
            sender="alice@example.com",
            recipient="bob@example.com",
            subject="Q1 Budget",
            body="I've compiled the Q1 budget...",
            timestamp="2026-04-08T10:00:00Z",
            importance_level="high",
            sentiment="urgent",
            is_reply=False
        ),
        EmailMessage(
            sender="bob@example.com",
            recipient="alice@example.com",
            subject="Re: Q1 Budget",
            body="I reviewed the numbers. I have concerns about contingency...",
            timestamp="2026-04-08T14:30:00Z",
            importance_level="high",
            sentiment="cautious",
            is_reply=True
        ),
        EmailMessage(
            sender="alice@example.com",
            recipient="bob@example.com",
            subject="Re: Q1 Budget",
            body="Thanks for feedback. I've adjusted the contingency based on historical data...",
            timestamp="2026-04-08T16:00:00Z",
            importance_level="high",
            sentiment="collaborative",
            is_reply=True
        )
    ]

    thread = EmailThread(
        messages=msgs,
        participants=["alice@example.com", "bob@example.com"],
        main_topic="Q1 Budget Approval",
        underlying_need="Secure CFO approval for proposed budget",
        urgency="high",
        action_items=["Get CFO sign-off by Friday"]
    )

    arc = analyzer._analyze_sentiment_arc(thread)
    assert "urgent" in arc.lower()
    assert "cautious" in arc.lower()
    assert "collaborative" in arc.lower()
    assert "→" in arc  # Arrow separator present
