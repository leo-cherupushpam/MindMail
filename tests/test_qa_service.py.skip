import pytest
from services.qa_service import (
    ask_question, summarize_emails, generate_draft_reply,
    organize_threads, suggest_inbox_rules, extract_meeting_details
)

# =============================================================================
# Task 1: Conversational Q&A Tests
# =============================================================================

def test_conversational_qa_over_emails():
    """
    GIVEN the user has a query and context from emails
    WHEN ask_question is called with the query and context
    THEN it returns a response grounded in the context, and the response is not empty.
    """
    user_query = "What was the budget discussed by Sarah last week?"
    context_data = {
        "emails": ["email1", "email2"],
        "metadata": {"sender": "Sarah", "topic": "budget"}
    }
    response = ask_question(user_query, context_data)
    assert response is not None, "The Q&A service returned None for a valid query."
    assert "Sarah" in response or "budget" in response.lower(), "Response should mention Sarah or budget, indicating context grounding."
    assert len(response) > 50, "Response is too short, indicating failure to summarize context."

# =============================================================================
# Task 2: Email Summarization Tests
# =============================================================================

def test_summarization_standalone():
    """
    GIVEN a set of emails/context
    WHEN summarize_emails is called
    THEN it returns a concise, accurate summary of the combined emails.
    """
    context_data = {
        "emails": ["email_project_kickoff", "email_budget_update"],
        "metadata": {"project": "Q1 Launch"}
    }
    response = summarize_emails(context_data)
    assert response is not None
    assert len(response.split()) > 20, "Summary is too short to be meaningful."

# =============================================================================
# Task 3: Draft Reply Generation Tests
# =============================================================================

def test_draft_reply_generation():
    """
    GIVEN a user query and context, and a desired tone/action.
    WHEN generate_draft_reply is called
    THEN it returns a reply that adopts the specified tone and addresses the core action item.
    """
    user_query = "I need to tell John I'll review the document by Friday."
    context_data = {
        "emails": ["email_from_john_doc"],
        "metadata": {"recipient": "John", "action_needed": "Review doc"}
    }
    response = generate_draft_reply(user_query, context_data)
    assert response is not None, "Draft reply should not be None."
    assert "Friday" in response or "by Friday" in response, "Draft reply must mention the specified deadline."
    assert "I will" in response or "Please find" in response or "review" in response.lower(), "Draft reply should use clear, professional language."

# =============================================================================
# Task 4: Thread Organization Tests
# =============================================================================

def test_thread_organization():
    """
    GIVEN a query about a topic and email context
    WHEN organize_threads is called
    THEN it returns a structured list of relevant threads organized by topic/date.
    """
    user_query = "Show me all emails about the project launch"
    context_data = {
        "emails": ["email_launch_kickoff", "email_launch_timeline", "email_budget_other"],
        "metadata": {"topic": "project launch", "date_range": "last_30_days"}
    }
    response = organize_threads(user_query, context_data)

    # Assert structure: response should be a non-empty string describing organized threads
    assert response is not None, "Thread organization should return a response."
    assert len(response) > 30, "Response should contain meaningful thread organization details."
    # Response should reference the topic or indicate no matching threads found
    assert "launch" in response.lower() or "no matching" in response.lower() or "thread" in response.lower(), \
        "Response should reference the topic or thread structure."

# =============================================================================
# Task 5: Smart Inbox Rules Tests
# =============================================================================

def test_suggest_inbox_rules():
    """
    GIVEN a set of emails with metadata
    WHEN suggest_inbox_rules is called
    THEN it returns categorization, label suggestions, and auto-archive recommendations.
    """
    context_data = {
        "emails": [
            {"subject": "Newsletter - Weekly Tech Updates", "sender": "newsletter@tech.com", "category": "promotional"},
            {"subject": "Re: Q1 Budget Review", "sender": "cfo@company.com", "category": "important"},
            {"subject": "Meeting Reminder: Standup", "sender": "calendar@company.com", "category": "internal"}
        ]
    }
    response = suggest_inbox_rules(context_data)

    # Assert structure: response should contain categorization or labeling information
    assert response is not None, "Inbox rules suggestion should return a response."
    assert len(response) > 30, "Response should contain meaningful inbox rule suggestions."
    # Response should mention categories, labels, or actions
    assert any(keyword in response.lower() for keyword in ["categor", "label", "archive", "priority", "rule"]), \
        "Response should mention categorization, labels, or inbox rules."

# =============================================================================
# Task 6: Meeting Scheduling Tests
# =============================================================================

def test_meeting_scheduling():
    """
    GIVEN a set of emails containing meeting details
    WHEN extract_meeting_details is called
    THEN it returns structured meeting information (date, time, participants, agenda).
    """
    context_data = {
        "emails": [
            {"subject": "Team Sync Tomorrow", "sender": "pm@company.com", "body": "Let's meet tomorrow at 2pm in Conference Room B to discuss Q2 goals."},
            {"subject": "Re: Team Sync Tomorrow", "sender": "dev@company.com", "body": "2pm works for me. I'll bring the latest mockups."}
        ]
    }
    response = extract_meeting_details(context_data)

    # Assert structure: response should contain meeting-related information
    assert response is not None, "Meeting details extraction should return a response."
    assert len(response) > 30, "Response should contain meaningful meeting details."
    # Response should mention time, date, or meeting keywords
    assert any(keyword in response.lower() for keyword in ["2pm", "tomorrow", "meeting", "time", "date", "agenda", "participant"]), \
        "Response should mention meeting time, date, or related details."