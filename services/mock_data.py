from typing import List
from services.models import EmailThread, EmailMessage


def get_sample_threads() -> List[EmailThread]:
    """Return 3 realistic multi-message email threads with sentiment arcs"""

    # Thread 1: Q1 Budget Approval (urgent → cautious → collaborative)
    thread1_messages = [
        EmailMessage(
            sender="sarah@company.com",
            recipient="cfo@company.com",
            subject="Q1 Budget Approval - Sign-off Needed by Friday",
            body="""Hi,

I've compiled the Q1 budget proposal with detailed projections across all departments. Here's the summary:

- Sales: +12% YoY growth projection, assuming market expansion into 2 new regions
- Marketing: -5% reduction, consolidating digital channels and reducing event spending
- Operations: +3% for infrastructure upgrades and efficiency tools
- Contingency Buffer: 8% of total budget

All numbers are based on conservative market analysis and account for the recent headcount changes. The contingency buffer is higher than last year due to the new product launch uncertainties.

I need executive sign-off by close of business Friday to finalize vendor contracts and spending authorizations. Attached are the detailed spreadsheets with department breakdowns, historical comparisons, and vendor quotes.

Please let me know if you need any clarifications or additional analysis.

Best regards,
Sarah""",
            timestamp="2026-04-08T09:15:00Z",
            importance_level="high",
            sentiment="positive",
            is_reply=False
        ),
        EmailMessage(
            sender="cfo@company.com",
            recipient="sarah@company.com",
            subject="RE: Q1 Budget Approval - Sign-off Needed by Friday",
            body="""Sarah,

Thanks for putting together a comprehensive proposal. The structure looks solid overall, and I appreciate the detailed departmental breakdowns. However, I do have some concerns.

The 8% contingency buffer is notably higher than our historical average of 5-6%. While I understand the rationale about product launch uncertainties, I want to make sure we're not over-allocating and creating waste. Can you provide:

1. Historical data on how often we've actually needed to tap into contingency reserves?
2. What specifically about the product launch creates these additional risks?
3. Are there other departments where we could tighten spending instead?

I'm also curious about the Sales +12% projection given the current market conditions. Is this based on pipeline data or market assumptions?

Let's schedule a call tomorrow morning if you can walk me through the contingency analysis. I want to move forward, but need to understand the rationale better before committing to 8%.

Thanks,
David""",
            timestamp="2026-04-08T14:30:00Z",
            importance_level="high",
            sentiment="neutral",
            is_reply=True
        ),
        EmailMessage(
            sender="sarah@company.com",
            recipient="cfo@company.com",
            subject="RE: Q1 Budget Approval - Sign-off Needed by Friday",
            body="""David,

Excellent questions - I anticipated these and have prepared detailed analysis. Please find attached:

Attachment 1: Historical Contingency Analysis (Last 3 Years)
- Q4 2025: Tapped 7.2% of contingency reserve (product bug fixes)
- Q3 2025: Tapped 6.1% of contingency reserve (vendor rate increase)
- Q2 2025: Tapped 3.8% of contingency reserve (hiring freeze impact)
- Average utilization: 5.7% over 12 months

The pattern shows we're consistently at or above 6% when accounting for product launches, vendor volatility, and market shifts. Given we have a major product launch in Q1 and recent vendor rate increases across the industry, 8% provides appropriate buffer without being excessive.

Attachment 2: Sales Projection Validation
The +12% is based on:
- Confirmed pipeline from enterprise sales team: $2.3M (conservative 60% close rate)
- SMB market expansion (2 new regions): $800K projected
- This is tied to actual customer conversations, not market assumptions

Attachment 3: Tightening Options
I reviewed alternatives:
- Marketing: Could reduce to -7% but risks brand awareness during expansion
- Operations: Items are necessary for infrastructure scaling
- Recommended approach: Accept the 8% contingency as data-driven

Can you review the attachments and let's talk through tomorrow? I'm confident this approach balances prudent risk management with business growth needs.

Best,
Sarah""",
            timestamp="2026-04-09T08:45:00Z",
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]

    thread1 = EmailThread(
        messages=thread1_messages,
        participants=["sarah@company.com", "cfo@company.com"],
        main_topic="Q1 Budget Approval with Contingency Buffer",
        underlying_need="Secure executive sign-off for Q1 spending while addressing concerns about contingency allocation",
        urgency="urgent",
        action_items=[
            "Review historical contingency analysis and vendor rate data",
            "Validate sales pipeline assumptions with enterprise team",
            "Schedule follow-up call to finalize budget sign-off",
            "Execute vendor contracts upon approval"
        ]
    )

    # Thread 2: Product Feature Request (positive → cautious → collaborative)
    thread2_messages = [
        EmailMessage(
            sender="pm@company.com",
            recipient="engineering@company.com",
            subject="Feature Request: Advanced Analytics Dashboard - Q2 Release Priority",
            body="""Engineering Team,

We've received strong customer feedback and internal requests for an advanced analytics dashboard. This is a high-priority initiative for Q2 and I'd like to propose starting Monday if possible.

Feature Requirements:
1. Real-time metrics display (updated every 30 seconds minimum)
2. Custom report builder (drag-and-drop interface for selecting metrics)
3. Data export functionality (CSV, PDF, Excel formats)
4. Configurable dashboards (users can save/share custom views)
5. Historical trend analysis (12-month lookback capability)

Timeline: 6 weeks from start to launch (first week of May)
Resources: 2 FE engineers, 1 BE engineer, 1 QA engineer (proposed)
Target: Enterprise tier customers only (reduces scope compared to full rollout)

This directly addresses our top 3 customer requests and will help with retention in the enterprise segment. Our sales team has already identified 5 prospects waiting on this feature.

Can we schedule time tomorrow to go through the technical approach? I want to make sure we align on architecture before kicking off.

Thanks,
Maria""",
            timestamp="2026-04-08T10:00:00Z",
            importance_level="high",
            sentiment="positive",
            is_reply=False
        ),
        EmailMessage(
            sender="engineering@company.com",
            recipient="pm@company.com",
            subject="RE: Feature Request: Advanced Analytics Dashboard - Q2 Release Priority",
            body="""Maria,

Thanks for the detailed requirements. I've reviewed the proposal with the team, and we have some concerns about the timeline and technical implications:

Timeline Concerns:
- 6 weeks is aggressive for this scope. Realistically, core feature development is 8-10 weeks
- Real-time metrics (30-second refresh) requires significant DB optimization work - we haven't done this before
- Data export with compliance (PDF, Excel) adds regulatory complexity we need to validate

Technical Risks:
- Real-time data querying at scale could cause performance degradation on existing features
- CSV is straightforward, but PDF/Excel require third-party library integration and extensive testing
- Custom report builder UI is complex and will need 2+ weeks of iteration

Proposal:
We can deliver a solid MVP in 6 weeks if we scope down:
1. Core dashboard with top 5 most-requested metrics (fixed, not custom)
2. Basic CSV export only (no PDF/Excel initially)
3. No real-time refresh initially - hourly batch updates instead
4. Pre-built templates instead of drag-and-drop builder

This would still address 80% of customer needs while reducing risk. We'd need security review for data export before launch.

Can we discuss tradeoffs? Happy to break down effort estimates for each feature component.

Thanks,
Alex""",
            timestamp="2026-04-08T15:45:00Z",
            importance_level="high",
            sentiment="neutral",
            is_reply=True
        ),
        EmailMessage(
            sender="pm@company.com",
            recipient="engineering@company.com",
            subject="RE: Feature Request: Advanced Analytics Dashboard - Q2 Release Priority",
            body="""Alex,

Thank you for the honest assessment. I appreciate the realistic timeline and the technical risks you've flagged. Let's go with the MVP approach - it's actually better for customer adoption anyway.

Revised Scope Agreement:
1. Core dashboard with top 5 metrics (based on customer feedback analysis we did last month)
2. CSV export only for now (can add PDF/Excel in Q3 based on usage)
3. Hourly batch updates instead of real-time (still a major improvement over no dashboard)
4. Pre-built templates (we can iterate on builder in Q3)

This still addresses the core customer need and gets us to market faster. Sales can work with the hourly update limitation - most customers are fine with daily/hourly reporting.

Timeline: Let's target 6 weeks still, with emphasis on quality over polish. Security review for data export - I'll coordinate with compliance this week.

Action Items:
- Alex: Provide detailed effort breakdown by component by EOD Thursday
- Me: Finalize top 5 metrics list and templates with product team
- Both: Schedule architecture review for Monday 2pm

Thanks for pushing back on scope - this is the right approach.

Maria""",
            timestamp="2026-04-09T09:30:00Z",
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]

    thread2 = EmailThread(
        messages=thread2_messages,
        participants=["pm@company.com", "engineering@company.com"],
        main_topic="Advanced Analytics Dashboard Feature Request for Q2 Release",
        underlying_need="Deliver analytics capability for enterprise customers while managing technical risks and timeline constraints",
        urgency="urgent",
        action_items=[
            "Finalize top 5 metrics based on customer feedback",
            "Provide detailed effort breakdown by feature component",
            "Schedule architecture review meeting",
            "Coordinate security review for data export functionality",
            "Validate hourly batch update approach with sales team"
        ]
    )

    # Thread 3: Project Status - Performance Issue (cautious → negative → collaborative)
    thread3_messages = [
        EmailMessage(
            sender="lead@company.com",
            recipient="stakeholders@company.com",
            subject="Web Platform Rebuild - March Status Update & Critical Performance Finding",
            body="""Team,

Here's the March status update on the Web Platform Rebuild initiative:

Progress to Date:
- API redesign: COMPLETE (100% - all endpoints refactored and tested)
- Component library: IN PROGRESS (70% - core components done, utilities and helpers remaining)
- Performance optimization: IDENTIFIED ISSUE (see below)

Critical Issue Discovered:
During load testing this week, we identified a performance regression in pages with large datasets. Specifically:

- Dashboard pages with 10K+ records: Response time degraded from 1.2s to 3.8s
- Report generation with complex queries: Now timing out (previously 4s, now >30s)
- Root cause: New API design isn't optimized for bulk data queries - needs caching layer and query optimization

This is significant because our enterprise customers rely heavily on these features for reporting and analytics.

Recommendation:
I recommend we invest 2 additional weeks in performance optimization before completing the rebuild. Shipping with known performance regressions creates major adoption friction and customer support burden. The extra time will:

1. Implement Redis caching layer for frequently accessed data
2. Optimize bulk query endpoints
3. Add query result pagination (currently fetches all data)
4. Perform full load testing at scale

Revised Timeline: Instead of March completion, targeting end of April (2 weeks additional).

The alternative of "ship and patch later" is risky because:
- Performance affects user perception of quality
- Performance issues are harder to debug after release
- Enterprise customers will encounter issues immediately
- Patches would still require the same 2-week effort

This is a quality vs. speed decision, but I believe absorbing the 2 weeks ensures success.

Detailed analysis attached. Happy to discuss.

Best,
James""",
            timestamp="2026-04-07T11:00:00Z",
            importance_level="high",
            sentiment="neutral",
            is_reply=False
        ),
        EmailMessage(
            sender="stakeholders@company.com",
            recipient="lead@company.com",
            subject="RE: Web Platform Rebuild - March Status Update & Critical Performance Finding",
            body="""James,

This is concerning. The performance regression is problematic, but so is pushing the timeline out another 2 weeks. We've already had this project extending beyond original estimates.

Key Questions:
1. Is there any way to parallelize the optimization work while component library finishes?
2. What's the actual business impact of shipping with the performance issue and patching iteratively?
3. Have we considered a phased rollout - new API to subset of users first?
4. What's the risk if we ship in 2 weeks with the optimization work still ongoing?

I understand quality is important, but we also need to balance time-to-market. Enterprise customers have been waiting for this update. A slightly slower performance for 2 weeks might be acceptable if we communicate clearly.

The 2-week extension puts us into May, which has other strategic initiatives scheduled. This needs executive review.

Can you send me:
- Cost impact of 2-week delay
- Risk assessment of shipping with performance issues
- Effort breakdown for optimization work (which pieces are critical, which can wait)

This requires a decision at the executive level.

Thanks,
Director""",
            timestamp="2026-04-07T15:30:00Z",
            importance_level="high",
            sentiment="negative",
            is_reply=True
        ),
        EmailMessage(
            sender="lead@company.com",
            recipient="stakeholders@company.com",
            subject="RE: Web Platform Rebuild - March Status Update & Critical Performance Finding",
            body="""Director,

I understand the timeline pressure. Let me address your questions directly:

Parallelization:
- Component library and optimization work use different team members, so we can run in parallel
- However, we can't optimize endpoints until component library is integrated (would optimize the old API)
- Real constraint: Both need to be done before launch testing, which requires sequence

Shipping with Performance Issues - Risk Analysis:
- HIGH RISK approach: "Ship and patch later"
  * Enterprise customers will immediately hit slowness on their most-critical workflows
  * Performance creates perception of "broken" even if technically functional
  * Support escalations on performance issues are highest-priority
  * Post-launch performance fixes still require full regression testing and deployment
  * Customer frustration impacts retention and upsell opportunities

- Cost: The 2-week optimization effort would STILL be required post-launch, just with added support load
- Phased rollout: Not viable - our architecture is monolithic, would need code branching

Reality Check:
- We spend 2 weeks now, or we spend 2 weeks later PLUS support costs and reputation damage
- Enterprise contracts often have performance SLAs - we'd be breaching those
- This isn't an opinion - it's engineering reality. Performance debt always comes due

Timeline Impact:
- Yes, this pushes to end of April
- But shipping broken performance and then fixing it also takes to end of April or later
- The difference: one approach delivers a quality product, the other ships a problem

I respectfully recommend absorbing the 2 weeks. Happy to brief executive team on the technical tradeoffs if that helps with the decision.

Detailed cost/risk breakdown attached.

James""",
            timestamp="2026-04-08T10:15:00Z",
            importance_level="high",
            sentiment="positive",
            is_reply=True
        ),
    ]

    thread3 = EmailThread(
        messages=thread3_messages,
        participants=["lead@company.com", "stakeholders@company.com"],
        main_topic="Web Platform Rebuild - Performance Regression and Timeline Impact",
        underlying_need="Secure stakeholder agreement on quality-vs-speed tradeoff for discovered performance issue",
        urgency="urgent",
        action_items=[
            "Complete component library integration",
            "Implement Redis caching layer for bulk queries",
            "Optimize API endpoints for large dataset queries",
            "Add pagination to query results",
            "Complete full load testing at scale",
            "Executive decision on quality vs. timeline tradeoff",
            "Communicate revised timeline to enterprise customers"
        ]
    )

    return [thread1, thread2, thread3]
