import pytest
from services.mock_data import get_sample_threads
from services.models import EmailThread, EmailMessage


def test_get_sample_threads_returns_threads():
    """Should return list of EmailThread objects"""
    threads = get_sample_threads()
    assert isinstance(threads, list)
    assert len(threads) > 0
    assert all(isinstance(t, EmailThread) for t in threads)


def test_mock_threads_have_realistic_content():
    """Mock threads should have multi-message conversations"""
    threads = get_sample_threads()
    for thread in threads:
        assert len(thread.messages) >= 2, "Should be multi-message threads"
        assert all(isinstance(m, EmailMessage) for m in thread.messages)
        assert thread.main_topic, "Should have main topic"
        assert thread.underlying_need, "Should have underlying need"
        assert thread.action_items, "Should have action items"


def test_mock_threads_show_sentiment_arc():
    """Threads should show sentiment changes across messages"""
    threads = get_sample_threads()
    for thread in threads:
        sentiments = [msg.sentiment for msg in thread.messages]
        # At least some threads should show sentiment progression
    assert any(
        len(set(t.messages[i].sentiment for i in range(len(t.messages)))) > 1
        for t in threads
    ), "At least some threads should show sentiment variation"
