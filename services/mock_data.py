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
    Includes diverse scenarios: urgent deadlines, feedback, support tickets, hiring, etc.

    Returns:
        List of EmailThread objects with realistic data
    """

    now = datetime.now()

    # Thread 1: Urgent production bug
    thread1_messages = [
        EmailMessage(
            sender="ops.alert@company.com",
            recipient="you@company.com",
            subject="🚨 CRITICAL: Production Database Connection Pool Exhausted",
            body="""ALERT TRIGGERED AT 2024-04-12 14:23 UTC

The payment processing service is returning 503 errors. Root cause: database connection pool at 100% capacity.

Current impact:
- ~5,000 transactions pending
- Error rate: 45%
- Revenue impact: ~$2,500/min

We've temporarily routed traffic to failover, but manual intervention required.

Actions needed immediately:
1. Increase connection pool size
2. Check for connection leaks in recent deploys
3. Monitor recovery

Slack: #incident-war-room

—DevOps""",
            timestamp=(now - timedelta(minutes=15)).isoformat(),
            importance_level="critical",
            sentiment="negative",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="ops.alert@company.com",
            subject="RE: 🚨 CRITICAL: Production Database Connection Pool Exhausted",
            body="""Got it. Starting investigation now.

I see the recent deployment to payment service at 2:15pm - likely introduced a connection leak in the transaction retry logic.

Rolling back now to previous version. ETA 5 minutes.

—You""",
            timestamp=(now - timedelta(minutes=10)).isoformat(),
            importance_level="critical",
            sentiment="neutral",
            is_reply=True
        ),
    ]
    thread1 = EmailThread(
        messages=thread1_messages,
        participants=["ops.alert@company.com", "you@company.com"],
        main_topic="🚨 CRITICAL: Production Database Connection Pool Exhausted",
        underlying_need="Resolve critical production incident affecting payment processing",
        urgency="urgent",
        action_items=["Rollback recent deploy", "Fix connection leak", "Monitor recovery"]
    )

    # Thread 2: Feature request with stakeholder input
    thread2_messages = [
        EmailMessage(
            sender="customer-success@company.com",
            recipient="you@company.com",
            subject="Feature Request: Bulk User Import from CSV",
            body="""Hi,

Enterprise customer (Acme Corp, $50k ARR) is asking if we support bulk importing users from CSV. They have 500+ users to onboard and currently need to add them manually.

This is blocking their implementation and they mentioned potentially moving to competitor if we can't support this.

Can we build this? Estimated effort? Timeline?

Customer wants to go live with their instance next month.

Thanks,
Emma""",
            timestamp=(now - timedelta(hours=6)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=False
        ),
        EmailMessage(
            sender="product@company.com",
            recipient="customer-success@company.com",
            subject="RE: Feature Request: Bulk User Import from CSV",
            body="""Emma,

This is high priority for us too. We've had this on the roadmap for Q3.

Given the customer situation, we can prioritize this for next sprint. Estimate: 5-8 story points, should be done in ~2 weeks.

Format we'll support:
- Email, First Name, Last Name, Department, Role
- Validation and error reporting
- Duplicate detection
- Send welcome emails on import

Can you loop in the customer for requirements gathering?

—Product""",
            timestamp=(now - timedelta(hours=5)).isoformat(),
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread2 = EmailThread(
        messages=thread2_messages,
        participants=["customer-success@company.com", "product@company.com", "you@company.com"],
        main_topic="Feature Request: Bulk User Import from CSV",
        underlying_need="Enable enterprise customer onboarding and prevent churn",
        urgency="urgent",
        action_items=["Gather feature requirements", "Implement CSV import", "Coordinate with customer"]
    )

    # Thread 3: Performance discussion with technical depth
    thread3_messages = [
        EmailMessage(
            sender="engineering@company.com",
            recipient="you@company.com",
            subject="Performance Investigation: Search Queries Timing Out",
            body="""Hi,

We're seeing intermittent timeouts on search queries (p99 latency: 45s, timeout at 30s). This is affecting ~2% of searches.

Initial investigation:
- Query complexity seems fine
- Database stats are up to date
- No obvious indexing issues

Patterns:
- Worse during 2-5pm (high traffic)
- Affects searches with 3+ filters
- Affects accounts with 50k+ records

Hypotheses:
1. Index needs rebuilding
2. Query planner choosing suboptimal execution path
3. Lock contention on frequently updated columns

Next steps: I'll run EXPLAIN ANALYZE on slow queries. Can you check if there were schema changes recently?

—James""",
            timestamp=(now - timedelta(days=1, hours=3)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="engineering@company.com",
            subject="RE: Performance Investigation: Search Queries Timing Out",
            body="""James,

Good catch. I remember we added a new status_history column last week in that big migration.

Let me check the indexing strategy... I see we didn't add it to the composite index on (account_id, created_at, status). That could be causing the planner to choose a worse path for status-filtered queries.

Recommend:
1. Rebuild the index to include status_history
2. Run REINDEX CONCURRENTLY
3. Monitor the p99 latency

I can deploy this change in the next maintenance window (tomorrow 2am).

Sound good?

—You""",
            timestamp=(now - timedelta(days=1, hours=1)).isoformat(),
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread3 = EmailThread(
        messages=thread3_messages,
        participants=["engineering@company.com", "you@company.com"],
        main_topic="Performance Investigation: Search Queries Timing Out",
        underlying_need="Resolve search performance degradation and improve query execution",
        urgency="urgent",
        action_items=["Rebuild database index", "Deploy index changes", "Monitor latency"]
    )

    # Thread 4: Hiring and recruitment
    thread4_messages = [
        EmailMessage(
            sender="hr@company.com",
            recipient="you@company.com",
            subject="Hiring: Senior Backend Engineer - Your Input Needed",
            body="""Hi,

We're moving forward with recruiting for the Senior Backend Engineer role (req#2024-045). You'll be conducting the technical interview.

The role is for someone to lead our API team and mentor junior engineers.

Candidate: Sarah Kim
- 8 years at Google (Payment Systems team)
- Built high-volume transaction systems
- Knows Go, Rust, Python
- Interview scheduled: Thursday 2pm PT

Can you do Thursday 2pm? The interview will be ~60 min focusing on:
- System design (focus on payment/financial systems)
- Database optimization experience
- Team leadership/mentoring

Let me know if you can make it and if you need anything from the candidate's profile.

Thanks,
Lisa""",
            timestamp=(now - timedelta(days=3)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="hr@company.com",
            subject="RE: Hiring: Senior Backend Engineer - Your Input Needed",
            body="""Lisa,

Thursday 2pm works. I'll prepare some good system design questions. The financial systems background is exactly what we need.

I'll focus on:
1. High-volume transaction design with consistency guarantees
2. Database scaling (they mentioned building at scale)
3. How they approach mentoring/knowledge sharing

I'll have interview notes and recommendation by Friday morning.

—You""",
            timestamp=(now - timedelta(days=2, hours=20)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread4 = EmailThread(
        messages=thread4_messages,
        participants=["hr@company.com", "you@company.com"],
        main_topic="Hiring: Senior Backend Engineer - Your Input Needed",
        underlying_need="Conduct technical interview and evaluate senior engineering candidate",
        urgency="normal",
        action_items=["Prepare interview questions", "Conduct technical interview", "Provide recommendation"]
    )

    # Thread 5: Design collaboration with iterations
    thread5_messages = [
        EmailMessage(
            sender="design@company.com",
            recipient="you@company.com",
            subject="Design Feedback: New Onboarding Flow v3",
            body="""Hi,

I've revised the onboarding flow based on the feedback from our last sync. Key changes:

v3 Updates:
✓ Moved permission explanation earlier (users were confused)
✓ Reduced steps from 7 to 5
✓ Added inline help for technical fields
✓ Streamlined integrations setup

Would love your thoughts before we do user testing. Specific areas:
1. Does the 'connect integrations' step feel in the right place?
2. Any steps that still feel confusing?
3. Can we simplify the auth flow further?

Figma: [link]

Thanks,
Maya""",
            timestamp=(now - timedelta(days=4)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="design@company.com",
            subject="RE: Design Feedback: New Onboarding Flow v3",
            body="""Maya,

Great improvements! The flow is much clearer now.

Feedback:
1. Integrations placement is good—right after workspace setup makes sense
2. One confusing part: "API Key Management" step uses jargon. Could we add an explainer button?
3. Auth flow is much simpler, but maybe show a progress bar? Users won't know how many steps left

Minor: Typography looks great but the form labels are a bit small on mobile.

Overall: Really solid. Ready for user testing with these small tweaks.

Can you schedule a design review with the product team?

—You""",
            timestamp=(now - timedelta(days=3, hours=20)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread5 = EmailThread(
        messages=thread5_messages,
        participants=["design@company.com", "you@company.com"],
        main_topic="Design Feedback: New Onboarding Flow v3",
        underlying_need="Refine onboarding UX based on user feedback and technical feasibility",
        urgency="normal",
        action_items=["Review design iterations", "Provide UX feedback", "Prepare for user testing"]
    )

    # Thread 6: Customer support escalation
    thread6_messages = [
        EmailMessage(
            sender="support@company.com",
            recipient="you@company.com",
            subject="ESCALATION: Customer Data Export Bug - Urgent",
            body="""Hi,

Customer (TechCorp) reported a critical issue: their data export is missing ~30% of records. They're trying to migrate to another system and this is blocking them.

Details:
- Export date range: Jan 1 - Mar 31, 2024
- Records in system: 15,847
- Records in export: 11,082
- Missing records: 4,765

They've been a customer for 2 years ($30k ARR) and threatening legal action if data isn't recovered.

This needs immediate attention. Can you investigate?

They need this resolved by EOD tomorrow.

—Support Team""",
            timestamp=(now - timedelta(hours=2)).isoformat(),
            importance_level="critical",
            sentiment="negative",
            is_reply=False
        ),
    ]
    thread6 = EmailThread(
        messages=thread6_messages,
        participants=["support@company.com", "you@company.com"],
        main_topic="ESCALATION: Customer Data Export Bug - Urgent",
        underlying_need="Recover missing customer data and resolve export functionality",
        urgency="urgent",
        action_items=["Investigate export bug", "Recover missing data", "Provide data to customer"]
    )

    # Thread 7: Retrospective discussion
    thread7_messages = [
        EmailMessage(
            sender="team@company.com",
            recipient="you@company.com",
            subject="Sprint 24 Retrospective - What We Can Improve",
            body="""Hi team,

Thanks everyone for a solid sprint! We shipped 47 story points and hit all our major milestones.

For the retro, I'd love to discuss:
1. What went well: Async code review process was much faster
2. What didn't work: CI/CD pipeline was flaky again (3x failed deploys)
3. What we should try: Dedicated infra time to stabilize the pipeline

Meeting: Friday 10am PT
Duration: 60 minutes

Please add any agenda items by Thursday EOD.

Looking forward to it!

—Manager""",
            timestamp=(now - timedelta(days=5)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
    ]
    thread7 = EmailThread(
        messages=thread7_messages,
        participants=["team@company.com", "you@company.com"],
        main_topic="Sprint 24 Retrospective - What We Can Improve",
        underlying_need="Continuous improvement through team reflection and process optimization",
        urgency="low",
        action_items=["Attend retrospective", "Share CI/CD concerns", "Plan improvements"]
    )

    # Thread 8: Security vulnerability
    thread8_messages = [
        EmailMessage(
            sender="security@company.com",
            recipient="you@company.com",
            subject="Security Alert: Vulnerable Dependency Found",
            body="""Hi,

Our dependency scanner found a vulnerability in Express.js (CVE-2024-1234 - High severity).

Affected:
- Version: 4.17.1
- Vulnerability: Path traversal in static file serving
- Our usage: We use express.static() for serving user-uploaded files

Impact: Medium - requires authentication, but could be exploited to read arbitrary files.

Fix: Update to 4.18.0+

Timeline: Should be patched in the next 48 hours (before we do the big customer demo on Monday).

Can you coordinate with the team to get this done?

—Security Team""",
            timestamp=(now - timedelta(days=2)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=False
        ),
    ]
    thread8 = EmailThread(
        messages=thread8_messages,
        participants=["security@company.com", "you@company.com"],
        main_topic="Security Alert: Vulnerable Dependency Found",
        underlying_need="Patch critical security vulnerability before production exposure",
        urgency="urgent",
        action_items=["Update Express.js", "Test file serving", "Deploy patch"]
    )

    # Thread 9: Positive recognition
    thread9_messages = [
        EmailMessage(
            sender="cto@company.com",
            recipient="you@company.com",
            subject="Recognition: Outstanding Work on Architecture Redesign",
            body="""Hi,

I wanted to personally thank you for the outstanding work on the microservices architecture redesign.

Your proposal was thoughtful, well-researched, and the implementation has been flawless. The team executed beautifully under your leadership.

Results:
- 40% reduction in API latency
- 25% reduction in infrastructure costs
- Much better scalability for future growth

This is exactly the kind of strategic thinking we need. You've been a game-changer for our engineering organization.

Keep up the excellent work!

—CTO""",
            timestamp=(now - timedelta(days=6)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
    ]
    thread9 = EmailThread(
        messages=thread9_messages,
        participants=["cto@company.com", "you@company.com"],
        main_topic="Recognition: Outstanding Work on Architecture Redesign",
        underlying_need="Recognition and positive feedback on major technical initiative",
        urgency="low",
        action_items=["Share appreciation", "Document lessons learned"]
    )

    # Thread 10: Meeting scheduling coordination
    thread10_messages = [
        EmailMessage(
            sender="manager@company.com",
            recipient="you@company.com",
            subject="Scheduling: 1:1 Check-in - Career Development",
            body="""Hi,

Time for our quarterly 1:1 to discuss career development and goals. It's been great seeing your growth this year.

I want to talk about:
1. Your interest in leadership (we discussed this last month)
2. Growth opportunities and mentoring roles
3. Professional development plans for next year

Available slots:
- Tuesday 2-3pm
- Wednesday 3-4pm
- Thursday 10-11am or 2-3pm

What works best for you?

—Manager""",
            timestamp=(now - timedelta(hours=4)).isoformat(),
            importance_level="normal",
            sentiment="positive",
            is_reply=False
        ),
    ]
    thread10 = EmailThread(
        messages=thread10_messages,
        participants=["manager@company.com", "you@company.com"],
        main_topic="Scheduling: 1:1 Check-in - Career Development",
        underlying_need="Discuss career growth and development opportunities",
        urgency="normal",
        action_items=["Schedule 1:1", "Prepare development goals", "Discuss mentoring opportunities"]
    )

    # Thread 11: Long email chain with sentiment arc - great for summarization testing
    thread11_messages = [
        EmailMessage(
            sender="client@external.com",
            recipient="you@company.com",
            subject="Contract Renewal Discussion - Need Your Input",
            body="""Hi,

We're approaching the end of our annual contract period and need to discuss renewal terms. There have been some concerns from our side about pricing and feature delivery.

Specifically:
- Your pricing increased 30% YoY, which is more than our budget allows
- We were promised real-time analytics in Q2, but it's now Q4 and still not delivered
- Support response times have degraded (now averaging 8 hours vs 2 hours last year)

Before we negotiate renewal terms, we need clarity on:
1. Can you commit to timeline for real-time analytics?
2. Would you be open to pricing adjustments given delivery delays?
3. What's your plan to improve support?

If these issues aren't addressed, we're considering alternatives.

Looking forward to resolving this.

—Client""",
            timestamp=(now - timedelta(days=7)).isoformat(),
            importance_level="high",
            sentiment="negative",
            is_reply=False
        ),
        EmailMessage(
            sender="sales@company.com",
            recipient="you@company.com",
            subject="FW: Contract Renewal Discussion - Need Your Input",
            body="""Hi,

This came in from our largest customer ($200k ARR). I'm escalating to you because:
1. Real-time analytics is your area
2. They're right that we promised Q2, now it's overdue
3. We need engineering input to commit to a realistic timeline

Can you take a look and help us respond? This is critical—we can't afford to lose them.

—Sales""",
            timestamp=(now - timedelta(days=7)).isoformat(),
            importance_level="high",
            sentiment="negative",
            is_reply=False
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="sales@company.com",
            subject="RE: Contract Renewal Discussion - Need Your Input",
            body="""I've reviewed the request. Here's my analysis:

Real-time analytics:
- Current status: 85% complete, blocked on streaming pipeline optimization
- Root cause: Underestimated complexity of low-latency data propagation
- Realistic timeline: 3 weeks with dedicated resources
- Recommendation: Commit to mid-January delivery with beta access

Support degradation:
- Yes, we've seen this due to increased volume
- We need 2 more support engineers (budget pending)
- Interim: Prioritize their tickets during ramp-up

Pricing:
- The 30% increase was due to infrastructure costs (which they benefit from)
- We could offer 15% discount if they commit to 2-year term
- Or price hold if they accept current release timeline

My recommendation:
- Commit to Jan 15 for real-time analytics
- Offer 2-year pricing lock if they sign within 2 weeks
- Show our plan to improve support (hiring timeline)

Let me know how to proceed.

—You""",
            timestamp=(now - timedelta(days=6, hours=20)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=True
        ),
        EmailMessage(
            sender="sales@company.com",
            recipient="you@company.com",
            subject="RE: Contract Renewal Discussion - Need Your Input",
            body="""Perfect, this is exactly what I needed. I'm going to send them a response based on your analysis.

Just to confirm:
- Jan 15 deadline is firm for real-time analytics, correct?
- We're comfortable offering 15% discount for 2-year commitment?
- Should I mention the support team growth plans?

I'll frame it as we're invested in their success and willing to make commitments to prove it.

Great work, thanks for the quick turnaround.

—Sales""",
            timestamp=(now - timedelta(days=6, hours=18)).isoformat(),
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
        EmailMessage(
            sender="you@company.com",
            recipient="sales@company.com",
            subject="RE: Contract Renewal Discussion - Need Your Input",
            body="""Yes, confirmed:
✓ Jan 15 is firm (I've already scheduled the team)
✓ 15% discount OK for 2-year commitment
✓ Yes, mention support expansion (shows we're taking feedback seriously)

Also tell them we want to do a quarterly business review starting this month—shows we're committed to partnership not just renewal.

Good luck with the negotiation. Let me know if they need anything else.

—You""",
            timestamp=(now - timedelta(days=6, hours=16)).isoformat(),
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]
    thread11 = EmailThread(
        messages=thread11_messages,
        participants=["client@external.com", "sales@company.com", "you@company.com"],
        main_topic="Contract Renewal Discussion - Strategic Account",
        underlying_need="Retain major customer by addressing concerns and negotiating favorable terms",
        urgency="urgent",
        action_items=["Commit to Jan 15 for real-time analytics", "Approve 15% discount", "Prepare for customer meeting"]
    )

    # Thread 12: Short thread perfect for drafting a reply
    thread12_messages = [
        EmailMessage(
            sender="team-lead@company.com",
            recipient="you@company.com",
            subject="Can You Lead the API Refactoring Initiative?",
            body="""Hi,

We're kicking off a major initiative to refactor our API layer (lots of technical debt accumulated). Given your recent work on the architecture redesign, you'd be perfect to lead this.

Scope:
- Refactor endpoints for consistency
- Implement versioning strategy
- Add request validation middleware
- Improve error handling

Timeline: 8 weeks, 3 engineers
Impact: Will unblock a ton of other work downstream

Interested? If yes, we should sync up this week to scope it out.

—Team Lead""",
            timestamp=(now - timedelta(hours=24)).isoformat(),
            importance_level="high",
            sentiment="positive",
            is_reply=False
        ),
    ]
    thread12 = EmailThread(
        messages=thread12_messages,
        participants=["team-lead@company.com", "you@company.com"],
        main_topic="Can You Lead the API Refactoring Initiative?",
        underlying_need="Find leader for major technical initiative with clear scope and timeline",
        urgency="normal",
        action_items=["Decide on API refactoring leadership", "Schedule scope discussion"]
    )

    # Thread 13: Hidden concerns and implications - good for implicit need extraction
    thread13_messages = [
        EmailMessage(
            sender="product-lead@company.com",
            recipient="you@company.com",
            subject="Q1 Planning - Your Input Needed on Tech Investment",
            body="""Hi,

We're planning Q1 roadmap and I wanted to get your input on technical priorities.

Currently proposed:
- Customer analytics dashboard (3 weeks)
- Mobile app improvements (2 weeks)
- Compliance reporting (2 weeks)
- Tech debt: None allocated

I'm worried that without tech debt work, we'll hit scalability walls in Q2. Last quarter we spent so much time firefighting production issues that we barely hit our feature targets.

Can you help me build a case for 2 weeks of dedicated infrastructure/database work in Q1? I'm concerned the business side won't see the value without your input.

Also, would love your thoughts on the mobile improvements—I'm not sure we're prioritizing what customers actually need there.

—Product Lead""",
            timestamp=(now - timedelta(days=5)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=False
        ),
    ]
    thread13 = EmailThread(
        messages=thread13_messages,
        participants=["product-lead@company.com", "you@company.com"],
        main_topic="Q1 Planning - Your Input Needed on Tech Investment",
        underlying_need="Secure engineering input and support for technical debt allocation in roadmap",
        urgency="normal",
        action_items=["Provide technical assessment of Q1 roadmap", "Build case for tech debt allocation"]
    )

    # Thread 14: Approval-seeking with evidence needed
    thread14_messages = [
        EmailMessage(
            sender="engineer@company.com",
            recipient="you@company.com",
            subject="Architecture Approval Needed: Caching Layer Redesign",
            body="""Hi,

I've designed a new caching architecture to improve API response times. Before I start implementation, I need your approval on the approach.

Proposal:
- Replace Redis cluster with Redis Sentinel + persistent backup
- Implement cache warming on startup
- Add automatic cache invalidation triggers
- Estimated improvement: 35-40% latency reduction

Benefits:
- Faster response times for end users
- Better reliability (failover without data loss)
- Easier cache troubleshooting

Concerns I've flagged:
- Requires 2 weeks of implementation time
- Need to coordinate with infra team on Redis setup
- Risk: Cache invalidation logic is complex and prone to bugs

I've documented the full proposal here: [link]

Would you be comfortable approving this approach? Or do you have concerns about the timeline or technical approach?

—Engineer""",
            timestamp=(now - timedelta(days=3)).isoformat(),
            importance_level="high",
            sentiment="neutral",
            is_reply=False
        ),
    ]
    thread14 = EmailThread(
        messages=thread14_messages,
        participants=["engineer@company.com", "you@company.com"],
        main_topic="Architecture Approval Needed: Caching Layer Redesign",
        underlying_need="Obtain approval on technical architecture before implementation",
        urgency="normal",
        action_items=["Review caching architecture proposal", "Approve or provide feedback"]
    )

    return [thread1, thread2, thread3, thread4, thread5, thread6, thread7, thread8, thread9, thread10, thread11, thread12, thread13, thread14]
