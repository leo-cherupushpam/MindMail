# Architecture Documentation

## System Overview

The Gmail Email Assistant MVP is designed with a clean separation of concerns between UI, business logic, and AI services.

```
┌─────────────────────────────────────────────────────┐
│            Streamlit UI (app/main.py)               │
│  - Email browsing                                   │
│  - Thread viewing                                   │
│  - Assistant panel (Ask, Draft, Summarize)          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         Business Logic Layer                        │
│  - ContextAnalyzer (services/context_analyzer.py)   │
│  - Data Models (services/models.py)                 │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│          AI Services Layer                          │
│  - QA Service (services/qa_service.py)              │
│  - OpenAI API calls                                 │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│          Data & Cache Layer                         │
│  - Mock Data (services/mock_data.py)                │
│  - Cache Management (services/cache.py)             │
└─────────────────────────────────────────────────────┘
```

## Data Models

### EmailMessage
Represents a single email message within a thread.

```python
class EmailMessage:
    sender: str                  # Email address
    recipient: str              # Email address
    subject: str                # Email subject
    body: str                   # Email body content
    timestamp: str              # ISO 8601 timestamp
    importance_level: str       # "high", "normal", "low"
    sentiment: str              # "positive", "neutral", "negative"
    is_reply: bool              # Whether this is a reply
```

### EmailThread
Represents a complete email conversation.

```python
class EmailThread:
    messages: List[EmailMessage]        # All messages in thread
    participants: List[str]             # Email addresses
    main_topic: str                     # Thread subject
    underlying_need: str                # What's really needed
    urgency: str                        # "urgent", "high", "normal", "low"
    action_items: List[str]             # Required actions
```

### EnrichedContext
Enriched analysis of an email thread.

```python
class EnrichedContext:
    thread: EmailThread                          # Original thread
    participants_analysis: str                   # Role/relationship analysis
    urgency_assessment: str                      # Urgency determination
    implicit_needs: List[str]                    # Hidden needs
    sentiment_arc: str                           # Tone progression
    professional_context: str                    # Context/norms
    tone_recommendations: str                    # Suggested response tone
    extracted_concerns: List[str]                # Identified concerns
    context_summary: str                         # Summary of analysis
```

## Core Services

### ContextAnalyzer

Enriches email threads with intelligent analysis.

**Methods:**
- `analyze_thread(thread)` → EnrichedContext
- `_analyze_participants(thread)` → Role inference
- `_assess_urgency(thread)` → Urgency level
- `_extract_needs(thread)` → Implicit need detection
- `_analyze_sentiment_arc(thread)` → Tone progression
- `_identify_concerns(thread)` → Concern extraction
- `_recommend_tone(thread)` → Tone recommendation

**Analysis Patterns:**
- Urgency keywords: URGENT, deadline, asap, critical, blocking
- Need indicators: approval, data/evidence, historical context
- Concern triggers: worry, concern, worried, hesitation, risk
- Sentiment tracking: Tracks tone changes across messages

### QA Service

Provides AI-powered email intelligence.

**Models Used:**
```
SEARCH_MODEL = "gpt-4.1-nano-2025-04-14"
  └─ Used for summarize_emails() - high-volume, fast
  
DRAFTING_MODEL = "gpt-5-nano-2025-08-07"
  └─ Used for generate_draft_reply() and ask_question()
  └─ Quality-critical tasks requiring nuanced understanding
```

**Functions:**

#### summarize_emails(enriched_context)
Generates multi-perspective summaries using SEARCH_MODEL.

**Summary includes:**
1. Surface summary (facts, statements, decisions)
2. Underlying needs (what's really being asked)
3. Sentiment arc (how tone changed)
4. Decision points (what needs approval)
5. Action items (what needs to happen)
6. Professional context (power dynamics, norms)
7. Implicit concerns (worries, hesitations)

#### generate_draft_reply(enriched_context, user_intent, tone)
Creates context-aware email drafts using DRAFTING_MODEL.

**Context passed to model:**
- Participant analysis and power dynamics
- Sentiment arc and urgency
- Underlying needs and concerns
- Recommended tone
- User intent (optional)
- Tone preference (optional)

**Draft quality factors:**
- Addresses underlying needs, not just surface request
- Matches professional norms of the thread
- Acknowledges concerns and hesitations
- Uses appropriate urgency and formality
- Demonstrates understanding of what's at stake

#### ask_question(question, enriched_context)
Answers questions about email content using DRAFTING_MODEL.

**Context provided:**
- Enriched analysis from ContextAnalyzer
- Full email thread
- Implicit meanings and context

**Question handling:**
- Looks beyond surface facts
- Understands implicit meanings
- Addresses underlying questions

#### analyze_sentiment(text)
Quick sentiment classification using heuristic patterns.

**Words trigger:**
- Positive: great, excellent, thanks, appreciate, love, excited
- Negative: bad, terrible, problem, issue, failed, frustrated, worried

## UI Architecture

### Layout
Three-column responsive layout using Streamlit columns:
- **Left Column** (Email List): Scrollable inbox with thread cards
- **Middle Column** (Thread Viewer): Fixed height with scrollable messages
- **Right Column** (Assistant Sidebar): Scrollable AI assistant panel

### Styling
CSS-based theming with:
- Design tokens for colors, typography, spacing
- Responsive design patterns
- Custom scrollbar styling
- Card-based UI components
- Smooth interactions and transitions

### Features

**Email List**
- Displays all available threads
- Shows urgency with color coding
- Clickable thread selection
- Shows message count and participant info

**Thread Viewer**
- Shows thread title and metadata
- Displays all messages chronologically
- Shows sender, email, timestamp for each message
- Scrollable message container

**Assistant Sidebar**
Three main features:
1. **Ask** (💬): Natural language Q&A
2. **Draft** (📋): Email reply generation
3. **Summarize** (📊): Thread summarization

Each feature:
- Takes context-aware input
- Shows progress indicators
- Displays formatted output
- Provides copy functionality

## State Management

**Streamlit Session State:**
```python
st.session_state:
    authenticated: bool                  # Auth status
    email_threads: List[EmailThread]     # User's emails
    sample_threads: List[EmailThread]    # Demo data
    selected_thread_idx: int             # Active thread
    chat_history: List                   # Q&A history
    selected_enriched_context: EnrichedContext
    enriched_contexts: List[EnrichedContext]
    analyzer: ContextAnalyzer            # Analysis engine
    last_refresh: str                    # Last sync timestamp
```

## Data Flow

### Thread Analysis Flow
```
EmailThread
    ↓
ContextAnalyzer.analyze_thread()
    ├─ _analyze_participants() → participants_analysis
    ├─ _assess_urgency() → urgency_assessment
    ├─ _extract_needs() → implicit_needs
    ├─ _analyze_sentiment_arc() → sentiment_arc
    ├─ _identify_professional_context() → professional_context
    ├─ _recommend_tone() → tone_recommendations
    ├─ _identify_concerns() → extracted_concerns
    └─ _create_summary() → context_summary
    ↓
EnrichedContext (UI display + AI input)
```

### AI Request Flow
```
User Input (Question/Intent/Tone)
    ↓
EnrichedContext + User Input
    ↓
QA Service:
    ├─ Build context prompt
    ├─ Add enriched analysis
    ├─ Add email thread content
    ├─ Select appropriate model
    └─ Call OpenAI API
    ↓
AI Response (Summary/Draft/Answer)
    ↓
Format + Display in UI
    ↓
Copy/Regenerate options
```

## Performance Considerations

### Model Selection Strategy
- **SEARCH_MODEL (nano)**: 50-70% cost reduction for summarization
- **DRAFTING_MODEL (GPT-5)**: Better quality for critical user-facing tasks
- **Mixed strategy**: Cost-effective while maintaining quality

### Caching
- Email thread caching (services/cache.py)
- Session state persistence within Streamlit
- EnrichedContext caching per thread

### Latency Targets
- Summarization: <5s (nano model efficiency)
- Draft generation: <8s (GPT-5 quality)
- Q&A: 5-15s (depends on complexity)

## Future Architecture Improvements

### Real Email Integration
- Replace mock data with Gmail API
- Handle real authentication (OAuth 2.0)
- Implement incremental sync
- Support multiple email accounts

### Scalability
- Move to backend API (FastAPI/Django)
- Add task queues for long-running tasks (Celery)
- Database for email storage (PostgreSQL)
- Caching layer (Redis)

### Advanced Features
- Custom model fine-tuning
- Sentiment trend analysis
- Intelligent email routing
- Template suggestions
- Multi-language support

## Testing Strategy

### Unit Tests
- Model inference (ContextAnalyzer)
- Sentiment analysis accuracy
- Data model validation

### Integration Tests
- End-to-end AI workflows
- Streamlit UI interactions
- API response handling

### Validation Tests
- Mock data comprehensiveness
- Feature coverage (all MVP features tested)
- Edge case handling

## Error Handling

**Service Failures:**
- OpenAI API unavailable → Graceful error messages
- Missing API key → Configuration validation
- Rate limiting → User feedback

**Data Validation:**
- Empty email bodies → Safe defaults
- Missing fields → Required field validation
- Malformed timestamps → ISO 8601 parsing

**UI Resilience:**
- Non-blocking error states
- Fallback content
- Clear error messaging
