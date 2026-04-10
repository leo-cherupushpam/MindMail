# Design Spec: Feature Enhancements for Gmail Email Assistant

**Date:** 2026-04-10  
**Project:** Gmail Email Assistant  
**Focus:** Deepen quality and intelligence of top 3 features (Q&A, Summarization, Draft Reply)  
**Architecture:** Context-Aware Processing (Hybrid approach: enhanced mock data + Gmail-ready design)

---

## Context & Problem Statement

The Gmail Email Assistant currently implements 6 features with basic functionality. The top 3 features (Conversational Q&A, Email Summarization, Draft Reply Generator) are surface-level: they work with sample email data and produce generic responses without understanding email-specific communication patterns or deeper context.

**Goal:** Improve the quality and intelligence of these 3 features by:
1. **Richer email context** — Analyze multi-message threads with deeper relationships and insights
2. **Email expertise** — Understand professional communication norms, sentiment arcs, underlying needs, and urgency

**Approach:** Build a **Context-Aware Processing layer** that extracts insights from email threads before features use them. This improves quality immediately (with enhanced mock data) and prepares the architecture for real Gmail API integration later without refactoring.

---

## Architecture

### Overall Flow

```
Raw Email Data (enhanced mock or future Gmail API)
         ↓
   ContextAnalyzer
   (extracts insights, tags context)
         ↓
   EnrichedContext
   (structured, tagged, analyzed)
         ↓
   LLM Features
   (Q&A, Summarization, Draft Reply)
   (use enriched context in prompts)
         ↓
   User-Facing Response
```

### Key Components

#### 1. **Data Models** (`services/models.py`)

Structured representations of emails and conversations:

```python
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
```

#### 2. **ContextAnalyzer** (`services/context_analyzer.py`)

Analyzes email threads and extracts rich insights:

```python
class ContextAnalyzer:
    """
    Extracts email-specific insights from threads.
    
    Responsibilities:
    - Analyze participant relationships and roles
    - Identify urgency and time-sensitivity
    - Extract explicit and implicit needs
    - Assess sentiment trajectory
    - Identify professional norms and expectations
    - Recommend tone for responses
    """
    
    def analyze_thread(self, thread: EmailThread) -> EnrichedContext:
        # 1. Who is involved and what are their roles?
        # 2. What's urgent vs informational?
        # 3. What's the explicit ask? Implicit ask?
        # 4. How does sentiment change across messages?
        # 5. What professional norms apply here?
        # 6. What concerns or hesitations exist?
        # 7. What should a response acknowledge?
        
        return EnrichedContext(...)
```

**Key analysis methods:**
- `_analyze_participants()` — Extract roles, power dynamics, relationships
- `_assess_urgency()` — Identify time-sensitive elements
- `_extract_needs()` — Both explicit ("I need approval by Friday") and implicit ("They're anxious about the budget")
- `_analyze_sentiment_arc()` — Track tone changes (positive → concerned → collaborative)
- `_identify_concerns()` — Extract worries, objections, hesitations
- `_recommend_tone()` — Suggest appropriate response tone

#### 3. **Enhanced Mock Data** (`services/mock_data.py`)

Realistic multi-message email threads with rich metadata:

**Instead of:** `['email_1', 'email_2', 'email_3']`

**Use realistic threads like:**
```python
[
    EmailThread(
        messages=[
            EmailMessage(
                sender="sarah@company.com",
                recipient="cfo@company.com",
                subject="Q1 Budget - Need approval by Friday",
                body="Hi [CFO], I've compiled the Q1 budget with projections...",
                timestamp="2026-04-08T10:00:00Z",
                importance_level="high",
                sentiment="urgent"
            ),
            EmailMessage(
                sender="cfo@company.com",
                recipient="sarah@company.com",
                subject="Re: Q1 Budget",
                body="Sarah, I reviewed the numbers. I have concerns about the contingency allocation...",
                timestamp="2026-04-08T14:30:00Z",
                importance_level="high",
                sentiment="cautious"
            ),
            EmailMessage(
                sender="sarah@company.com",
                recipient="cfo@company.com",
                subject="Re: Q1 Budget",
                body="Thanks for the feedback. I've adjusted the contingency based on historical data...",
                timestamp="2026-04-08T16:00:00Z",
                importance_level="high",
                sentiment="collaborative"
            )
        ],
        participants=["sarah@company.com", "cfo@company.com"],
        main_topic="Q1 Budget Approval",
        underlying_need="Secure CFO approval for proposed budget",
        urgency="high",
        action_items=["Get CFO sign-off by Friday"]
    ),
    # ... more threads
]
```

---

## Feature Enhancements

### 1. Conversational Q&A

**Current behavior:** Answers surface-level questions based on email content

**Enhanced behavior:** Understands context, implicit needs, and underlying concerns

**Prompt enhancement:**
```
OLD:
"Answer this question about emails: {question}
Context: {email_list}"

NEW:
"Answer this question about emails: {question}

ENRICHED CONTEXT:
- Main topic: {enriched_context.main_topic}
- Underlying needs (explicit): {enriched_context.implicit_needs}
- What's really being asked: {enriched_context.underlying_need}
- Sentiment arc: {enriched_context.sentiment_arc}
- Key concerns: {enriched_context.extracted_concerns}
- Professional context: {enriched_context.professional_context}

Consider the full conversation history and implicit meanings.
Look beyond surface facts to understand what's really needed."
```

**Examples of improved Q&A:**
- **Old:** "What did the CFO say?" → "They said they have concerns about contingency."
- **New:** "What's the CFO really worried about?" → "They're concerned about our contingency allocation methodology and want to see historical data justifying it. They may be concerned about budget overruns."

---

### 2. Email Summarization

**Current behavior:** Generic summary of emails

**Enhanced behavior:** Multi-layered summary with context and implications

**Prompt enhancement:**
```
Summarize this email thread with these perspectives:

1. SURFACE SUMMARY: Key facts, explicit statements, decisions
2. UNDERLYING NEEDS: What's really being asked for?
3. SENTIMENT ARC: How did the tone change across messages?
4. DECISION POINTS: What needs to be decided or approved?
5. ACTION ITEMS: What needs to happen next?
6. PROFESSIONAL CONTEXT: Any implicit power dynamics or norms?
7. IMPLICIT CONCERNS: What worries or hesitations are present?

ENRICHED CONTEXT PROVIDED:
- Participants: {enriched_context.participants}
- Urgency: {enriched_context.urgency}
- Main topic: {enriched_context.main_topic}
- Sentiment arc: {enriched_context.sentiment_arc}
- Extracted concerns: {enriched_context.extracted_concerns}
```

**Example output:**
```
SURFACE: Sarah proposes Q1 budget; CFO expresses concerns about contingency; Sarah adjusts based on feedback.

UNDERLYING: Sarah needs CFO sign-off by Friday. CFO wants better justification for contingency calculations.

SENTIMENT: Urgent → Cautious → Collaborative (improving tone as Sarah addresses concerns)

DECISION: Budget approval pending CFO's review of adjusted contingency.

ACTION: Sarah to provide historical data; CFO to review and approve by Friday.

CONCERNS: CFO worried about over-allocating contingency (potential budget waste).
```

---

### 3. Draft Reply Generator

**Current behavior:** Generates professional replies with generic tone

**Enhanced behavior:** Drafts replies that understand context, concerns, and email-specific norms

**Prompt enhancement:**
```
Draft a reply to this email thread.

THREAD CONTEXT:
- Participants: {enriched_context.participants}
- Current sentiment: {enriched_context.sentiment_arc} (latest message)
- Urgency: {enriched_context.urgency}
- Underlying ask: {enriched_context.underlying_need}
- Key concerns: {enriched_context.extracted_concerns}
- Recommended tone: {enriched_context.tone_recommendations}

USER'S INTENT: {user_intent}
TONE PREFERENCE: {tone}

Your draft should:
1. Address the underlying need and concerns (not just surface request)
2. Match the professional norms and expectations of this thread
3. Acknowledge any concerns or hesitations expressed
4. Use appropriate urgency and formality based on context
5. Show that you understand what's really at stake
```

**Example improvement:**
```
OLD DRAFT:
"I'll review the budget and get back to you."

NEW DRAFT:
"Thanks for the feedback. I've adjusted the contingency allocation 
based on our last three years of actual expenses. I've attached the 
historical data showing why we believe 8% contingency is appropriate 
for our risk profile. I'm confident this addresses your concerns about 
justification. I can have your sign-off by Friday as planned."
```

The new draft:
- Addresses the concern (justification) directly
- Shows understanding of what matters (historical data)
- Removes hesitation (confident tone)
- Confirms the timeline (Friday)

---

## Implementation Structure

### Files to Create
- `services/models.py` — Data classes (EmailMessage, EmailThread, EnrichedContext)
- `services/context_analyzer.py` — ContextAnalyzer class
- `services/mock_data.py` — Enhanced realistic email threads (replaces inline data)

### Files to Modify
- `services/qa_service.py` — Update prompts for all 3 features to use EnrichedContext
- `app/main.py` — Instantiate ContextAnalyzer, call it before features

### Data Flow in Features
```python
# Before:
response = ask_question(user_query, email_context)

# After:
analyzer = ContextAnalyzer()
enriched = analyzer.analyze_thread(email_thread)
response = ask_question(user_query, enriched)  # Prompt now uses enriched context
```

---

## Gmail API Readiness

**This design is Gmail-ready because:**

1. **Mock data is separable** — All sample emails live in `mock_data.py`. To use real Gmail:
   - Create `gmail_fetcher.py` that returns EmailThread objects
   - Swap import: `from mock_data import ...` → `from gmail_fetcher import ...`
   - Features and ContextAnalyzer work unchanged

2. **Data models are neutral** — EmailMessage/EmailThread are agnostic to source (mock or API)

3. **ContextAnalyzer is reusable** — Works with any EmailThread, regardless of origin

4. **Prompts are enhanced but stable** — No breaking changes to feature logic

**Future Gmail integration:**
```python
# Create gmail_fetcher.py
class GmailFetcher:
    def get_thread(self, thread_id: str) -> EmailThread:
        # Fetch from Gmail API
        # Convert to EmailThread format
        # Return enriched thread
        
# In main.py, just swap imports
# Everything else works unchanged
```

---

## Success Criteria

### Immediate (Enhanced Mock Data)
- ✅ Q&A understands implicit needs and concerns
- ✅ Summarization shows multiple layers (surface, underlying, sentiment, action items)
- ✅ Draft replies acknowledge concerns and match context
- ✅ All 3 features show understanding of email-specific patterns

### Future (Gmail Ready)
- ✅ Can swap mock data for real Gmail API without changing features
- ✅ ContextAnalyzer works with real threads
- ✅ All prompts reference enriched context consistently

---

## Testing & Validation

### Unit Tests
- ContextAnalyzer correctly extracts sentiment arc
- ContextAnalyzer identifies implicit needs
- Data models serialize/deserialize correctly

### Integration Tests
- Q&A prompt includes enriched context
- Summarization prompt uses all context layers
- Draft reply prompt references concerns and tone

### Manual Validation
- Try each feature with sample threads
- Verify responses show understanding of:
  - What's really being asked
  - Professional norms in the thread
  - Concerns and hesitations
  - Appropriate tone and urgency

---

## Scope & Constraints

**In scope:**
- Enhanced mock data with realistic threads
- ContextAnalyzer implementation
- Data model classes
- Prompt updates for 3 features

**Out of scope:**
- Real Gmail API integration (future work)
- Additional features beyond the top 3
- Dark mode or mobile optimization
- Real-time updates

**Constraints:**
- Must work with existing Streamlit UI (no changes needed)
- Must maintain backward compatibility with current feature signatures
- Mock data should be realistic but not require external APIs

---

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| Separate ContextAnalyzer class | Single responsibility, reusable, testable |
| Mock data in separate file | Easy to swap for real Gmail API later |
| EnrichedContext data class | Type-safe, clear contract, easy to extend |
| Enhance prompts (not code) | Leverage LLM reasoning, minimal code changes |
| Hybrid approach (mock now, Gmail later) | Get benefits immediately, prepare for future |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| ContextAnalyzer becomes too complex | Break into smaller methods, unit test each |
| Prompts become unwieldy | Use structured prompt templates, document sections |
| Mock data isn't realistic enough | Include multi-message threads, sentiment changes, concerns |
| LLM doesn't use enriched context well | Validate with manual tests, iterate prompts |
| Gmail integration later proves incompatible | Use data models that match Gmail API output structure |

---

## Next Steps

1. **Phase 1: Implementation** — Build models, ContextAnalyzer, mock data, update prompts
2. **Phase 2: Testing** — Unit tests for analyzer, manual validation of feature outputs
3. **Phase 3: Polish** — Refine prompts based on results, improve mock data realism
4. **Phase 4: Gmail Prep** — Document Gmail integration points, design fetcher module

