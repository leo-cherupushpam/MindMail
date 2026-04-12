"""
Mock email data for MVP showcase and testing.
Generates realistic professional email threads with various urgency levels and scenarios.
"""

from datetime import datetime, timedelta
from services.models import EmailMessage, EmailThread
from services.qa_service import analyze_sentiment


def get_sample_threads() -> list[EmailThread]:
    """
    Get a collection of realistic mock email threads for MVP showcase.
    Includes various scenarios: urgent deadlines, feedback requests, project updates, etc.

    Returns:
        List of EmailThread objects with realistic data
    """

    now = datetime.now()

    # Thread 1: Urgent project deadline
    thread1_messages = [
        EmailMessage(
            sender="sarah.chen@company.com",
            recipient="you@company.com",
            subject="URGENT: Q2 Roadmap Review Due Friday",
            body="""Hi,

Can you get me the final Q2 roadmap by Friday EOD? The exec team needs it for the board meeting Monday.

Key sections needed:
- Feature priorities (with dependencies)
- Timeline with milestones
- Resource allocation
- Risk assessment

This is blocking our strategy discussion, so it's critical we have this locked in.

Thanks,
Sarah""",
            timestamp=(now - timedelta(hours=2)).isoformat(),
            importance_level="high",
            sentiment="negative",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="sarah.chen@company.com",
            subject="RE: URGENT: Q2 Roadmap Review Due Friday",
            body="""Sarah,

I'll have a first draft ready by Wednesday. Can you review earlier in the week so I have time to incorporate feedback?

—You""",
            timestamp=(now - timedelta(hours=1)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=True
        ),
    ]
    thread1 = EmailThread(
        messages=thread1_messages,
        participants=["sarah.chen@company.com", "you@company.com"],
        main_topic="Q2 Roadmap Review Due Friday",
        underlying_need="Get project roadmap completed and reviewed before board meeting",
        urgency="urgent",
        action_items=["Draft Q2 roadmap", "Get exec feedback"]
    )

    # Thread 2: Collaborative design feedback
    thread2_messages = [
        EmailMessage(
            sender="alex.patel@company.com",
            recipient="you@company.com",
            subject="Design Review - New Dashboard Mockups",
            body="""Hey!

I've put together some initial mockups for the new analytics dashboard. Would love your thoughts before we start development.

Key questions:
1. Does the layout make sense for your use cases?
2. Are we missing any critical metrics?
3. Should we add dark mode support?

Check them out here: [Figma link]

Looking forward to hearing what you think!

Alex""",
            timestamp=(now - timedelta(days=1)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="alex.patel@company.com",
            subject="RE: Design Review - New Dashboard Mockups",
            body="""Alex,

The mockups look great! I have a few suggestions:

1. The layout is intuitive, but could we add a collapsed sidebar option?
2. Missing: export to PDF functionality for reports
3. Dark mode would be awesome, but maybe for v2?

Let me know when you want to sync up to discuss.

—You""",
            timestamp=(now - timedelta(hours=16)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread2 = EmailThread(
        messages=thread2_messages,
        participants=["alex.patel@company.com", "you@company.com"],
        main_topic="Design Review - New Dashboard Mockups",
        underlying_need="Get feedback on dashboard design before development starts",
        urgency="normal",
        action_items=["Review mockups", "Provide design feedback"]
    )

    # Thread 3: Status update with hidden concern
    thread3_messages = [
        EmailMessage(
            sender="jessica.lee@company.com",
            recipient="you@company.com",
            subject="RE: API Performance Issues",
            body="""Hi,

Thanks for checking in. We've made progress on the latency issue—it's down to 200ms from 800ms. However, we're seeing some inconsistent results in production that we're still investigating.

We should have this fully resolved by Wednesday, but wanted to flag that there might be a slight delay if we hit any blockers with the database layer.

Will keep you updated.

Jessica""",
            timestamp=(now - timedelta(days=2)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=True
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="jessica.lee@company.com",
            subject="RE: API Performance Issues",
            body="""Jessica,

Thanks for the update. Wednesday works. Let me know if you need any help unblocking the database layer—I have some bandwidth.

Keep me posted on the inconsistencies you're seeing.

—You""",
            timestamp=(now - timedelta(days=1, hours=18)).isoformat(),
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread3 = EmailThread(
        messages=thread3_messages,
        participants=["jessica.lee@company.com", "you@company.com"],
        main_topic="API Performance Issues",
        underlying_need="Resolve API latency and database consistency issues before launch",
        urgency="urgent",
        action_items=["Fix API latency", "Resolve database inconsistencies"]
    )

    # Thread 4: Meeting request with implicit conflict
    thread4_messages = [
        EmailMessage(
            sender="mike.garcia@company.com",
            recipient="you@company.com",
            subject="Budget Review Meeting - Tuesday 2pm?",
            body="""Hi,

Can we schedule the budget review for Q3? I know we just finished Q2, but finance needs our preliminary numbers ASAP for planning.

A few items we should cover:
- Team headcount needs
- Tool/vendor budgets
- Infrastructure costs
- Contingency

Would Tuesday 2pm work for you? If not, let me know what times work better.

Thanks,
Mike""",
            timestamp=(now - timedelta(hours=3)).isoformat(),
            importance_level="normal",
            sentiment="neutral",
            is_reply=False
        ),
    ]
    thread4 = EmailThread(
        messages=thread4_messages,
        participants=["mike.garcia@company.com", "you@company.com"],
        main_topic="Budget Review Meeting - Tuesday 2pm?",
        underlying_need="Schedule budget planning meeting and prepare financial projections",
        urgency="normal",
        action_items=["Schedule budget meeting", "Prepare budget numbers"]
    )

    # Thread 5: Positive feedback and recognition
    thread5_messages = [
        EmailMessage(
            sender="priya.sharma@company.com",
            recipient="you@company.com",
            subject="Great work on the customer success docs!",
            body="""Hi there!

I just reviewed the onboarding documentation you created, and it's excellent. The step-by-step walkthroughs are so clear, and the screenshots are super helpful. Our customers have been giving great feedback.

This is exactly what we needed to reduce support tickets. Really impressed with the quality.

Keep up the great work!

Priya""",
            timestamp=(now - timedelta(days=3)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
    ]
    thread5 = EmailThread(
        messages=thread5_messages,
        participants=["priya.sharma@company.com", "you@company.com"],
        main_topic="Great work on the customer success docs!",
        underlying_need="Recognition and feedback on documentation quality",
        urgency="low",
        action_items=["Acknowledge feedback"]
    )

    # Thread 6: Low priority FYI with data
    thread6_messages = [
        EmailMessage(
            sender="devops@company.com",
            recipient="you@company.com",
            subject="FYI: Weekly Infrastructure Report",
            body="""Weekly infrastructure status:

✓ Uptime: 99.98% (target: 99.95%)
✓ API response time: 185ms avg (target: <200ms)
⚠ Database disk usage: 78% (alert at 85%)
✓ Cache hit rate: 92% (target: >90%)

No incidents this week. All systems nominal.

See dashboard: [link]

—DevOps Team""",
            timestamp=(now - timedelta(days=4)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
    ]
    thread6 = EmailThread(
        messages=thread6_messages,
        participants=["devops@company.com", "you@company.com"],
        main_topic="Weekly Infrastructure Report",
        underlying_need="Stay informed on system health and performance",
        urgency="low",
        action_items=["Monitor disk usage"]
    )

    return [thread1, thread2, thread3, thread4, thread5, thread6]
