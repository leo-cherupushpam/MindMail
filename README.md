# Gmail Email Assistant

An intelligent email management tool for GMAIL that uses AI to help you understand, summarize, and respond to emails with context-aware insights.

## Features

### 📧 Smart Email Management
- **Email Inbox**: Browse and organize email threads with intelligent prioritization
- **Thread Viewer**: Read full email conversations with context analysis
- **Scrollable Interface**: Smooth navigation with inbox and assistant panels independently scrollable

### 🤖 AI-Powered Assistant

#### For Existing Emails
Access full AI features when viewing any email thread in the inbox.

**Ask (💬)** - Ask questions about email content
- Contextual understanding of implicit needs
- Answers grounded in enriched email analysis
- Example questions:
  - "What's the main concern in this thread?"
  - "What action do I need to take?"
  - "What are the implicit concerns from the customer?"

**Draft (📋)** - Generate professional email replies
- Context-aware response generation
- Matches appropriate tone based on sentiment and urgency
- Tone customization: professional, collaborative, assertive, empathetic
- Concern-aware drafting
- Intent-based reply generation

**Summarize (📊)** - Create multi-perspective summaries
- Surface facts and explicit statements
- Underlying needs and implicit asks
- Sentiment arc and tone changes
- Decision points requiring action
- Professional context and power dynamics
- Implicit concerns and hesitations

#### For Composing New Emails
Click **Compose** to open a modal for drafting new emails with AI assistance.

**Draft (✏️)** - Generate email from topic
- Create complete emails from a subject line
- Example: Topic "Q2 Status Update" → generates full professional email

**Ask (💬)** - Get writing advice
- Answer writing questions
- Example: "Should this sound more urgent?"

**Refine (✨)** - Improve existing email text
- Enhance tone, clarity, or length
- Example: "Make it more concise" or "Sound more professional"

#### Panel Controls
- **✦ Toggle Button** (top right of email header) - Hide/show AI panel to maximize email space
- **✕ Close Button** (in AI panel header) - Close panel from within
- Panel state persists while viewing the same email

### 🧠 Context Analysis
Every email is enriched with intelligent analysis:
- **Urgency Assessment**: Automatic detection of time-sensitive emails (urgent, high, normal, low)
- **Action Items**: Extraction of explicit and implicit action items
- **Sentiment Analysis**: Understanding tone and how it changes across messages
- **Implicit Needs**: Identification of what's really being asked for
- **Concern Detection**: Flagging worries, hesitations, and potential blockers
- **Tone Recommendations**: Suggested response tone based on context

## Architecture

### Tech Stack
- **Frontend**: FastAPI + Vanilla HTML/CSS/JS with Modern Design
- **AI Models**: 
  - `gpt-4o-mini` for summarization (high-volume, cost-optimized)
  - `gpt-4o` for drafting and Q&A (quality-critical)
- **API**: OpenAI API with `max_completion_tokens` parameter
- **Data**: Mock email threads for MVP showcase
- **Server**: Uvicorn with hot reload

### Project Structure
```
gmail-email-assistant/
├── app/
│   ├── api.py                  # FastAPI application and routes
│   └── static/                 # Vanilla HTML/CSS/JS frontend
├── services/
│   ├── models.py               # Data models (EmailMessage, EmailThread, EnrichedContext)
│   ├── context_analyzer.py     # Email context analysis and enrichment
│   ├── qa_service.py           # AI-powered Q&A, drafting, summarization
│   ├── mock_data.py            # 14 realistic mock email threads
│   ├── gmail_auth.py           # Gmail authentication (future)
│   ├── gmail_fetcher.py        # Gmail API integration (future)
│   └── cache.py                # Email caching
└── README.md                   # This file
```

### Core Components

#### EmailThread Model
Represents a complete email conversation with:
- List of messages (EmailMessage objects)
- Participants
- Main topic
- Underlying need
- Urgency level
- Action items

#### ContextAnalyzer
Enriches email threads with intelligent analysis:
- Participant role inference
- Urgency assessment
- Implicit need extraction
- Sentiment trajectory analysis
- Professional context identification
- Tone recommendations
- Concern extraction

#### QA Service
Provides AI-powered capabilities:
- `ask_question()`: Answer questions about email content with context awareness
- `generate_draft_reply()`: Create context-aware email drafts
- `summarize_emails()`: Generate multi-perspective summaries
- `analyze_sentiment()`: Quick sentiment classification

## Mock Data

The MVP includes **14 realistic email threads** covering diverse scenarios:

1. **Production Incident**: Critical database issue with financial impact
2. **Feature Request**: Customer-driven CSV import with stakeholder discussion
3. **Performance Investigation**: Technical deep-dive with database optimization
4. **Hiring**: Recruitment coordination and technical interview
5. **Design Collaboration**: Iterative UX feedback with specific suggestions
6. **Customer Support Escalation**: Critical data export bug
7. **Sprint Retrospective**: Team process improvement discussion
8. **Security Vulnerability**: Dependency patch coordination
9. **Recognition**: Positive feedback on major initiative
10. **Career Development**: 1:1 scheduling for growth discussion
11. **Contract Renewal**: Long chain (5 messages) showing sentiment arc
12. **Leadership Opportunity**: Single message perfect for drafting replies
13. **Q1 Planning**: Hidden concerns and strategic priorities
14. **Architecture Approval**: Approval-seeking with technical evidence

Each thread is designed to validate MVP features and demonstrate real-world usage patterns.

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (free trial or paid account)

### Installation

```bash
# Clone the repository
git clone https://github.com/leo-cherupushpam/gmail-email-assistant.git
cd gmail-email-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY=sk-your-api-key-here
```

### Running the App

```bash
# Start the FastAPI server with hot reload
uvicorn app.api:app --reload

# Server will be available at:
# http://127.0.0.1:8000
```

Open http://127.0.0.1:8000 in your browser and start exploring the AI-powered email assistant!

## Usage

### Viewing & Analyzing Emails
1. **Browse Inbox**: Email list appears in left sidebar with sender, subject, and snippet
2. **Open Email**: Click any email to view full conversation with enriched analysis
3. **Ask Questions**: Click "💬 Ask" button to ask contextual questions about the email
   - Examples: "What's the main topic?", "When is the deadline?", "What action do I need to take?"
4. **Draft Reply**: Click "✏️ Draft" to generate a professional response
   - Choose tone: Professional, Collaborative, Assertive, or Empathetic
   - Optionally add intent to guide the response
5. **Summarize**: Click "📊 Summarize" to get a comprehensive multi-perspective summary
6. **Toggle Panel**: Click "✦" button (top right) to hide AI panel and maximize email space

### Composing New Emails
1. **Click Compose**: Button in left sidebar opens email composition modal
2. **Enter Subject**: Subject line for the new email
3. **AI Draft**: Click "✏️ Draft" to auto-generate email body from subject
4. **Ask for Help**: Click "💬 Ask" to get writing advice (e.g., "Should this sound urgent?")
5. **Refine Text**: Click "✨ Refine" to improve existing email (e.g., "Make it shorter")
6. **Send or Cancel**: Click "Send" to log email (MVP) or "Cancel" to close modal

## AI Model Strategy

### SEARCH_MODEL: `gpt-4o-mini`
Used for high-volume, lower-latency tasks:
- Email summarization (📊 Summarize feature)
- Content organization
- Efficient processing

**Why gpt-4o-mini**: Cost-optimized while maintaining quality for summary tasks. Good balance of speed and accuracy.

### DRAFTING_MODEL: `gpt-4o`
Used for quality-critical, complex reasoning tasks:
- Draft reply generation (✏️ Draft for threads)
- Complex question answering (💬 Ask about threads)
- Context-aware decision support
- New email composition (Compose modal features)
- Email text refinement (✨ Refine)

**Why gpt-4o**: Best quality for tasks that directly impact user experience and require deep understanding of context and implications.

## Development

### Code Style
- Python 3.8+ compatible
- Type hints for clarity
- Docstrings for all functions
- Clean separation of concerns

### Testing
Run mock data validation:
```bash
python -c "from services.mock_data import get_sample_threads; threads = get_sample_threads(); print(f'Loaded {len(threads)} test threads')"
```

## Troubleshooting

### OpenAI API Key Not Found
```bash
# Make sure the environment variable is set:
export OPENAI_API_KEY=sk-your-api-key-here

# Or check if it's set:
echo $OPENAI_API_KEY
```

### Model Not Available
Check that your OpenAI account has access to:
- `gpt-4o-mini` (for summarization)
- `gpt-4o` (for drafting and Q&A)

These are the latest Claude-compatible models. If you get a model not found error, check your OpenAI account billing status.

### Server Port Already in Use
If port 8000 is already in use, run on a different port:
```bash
uvicorn app.api:app --reload --port 8001
# Then open http://127.0.0.1:8001
```

## Performance Notes

- **Summarization** (📊): Uses gpt-4o-mini for faster responses (typically <5s)
- **Drafting** (✏️): Uses gpt-4o for quality (typically <8s)
- **Q&A** (💬): Uses gpt-4o for accuracy (typically 5-15s depending on complexity)
- **Compose Features**: Compose draft/refine/ask all use gpt-4o (typically <10s per request)

*Note: Response times depend on OpenAI API load and your internet connection*

## License

MIT License - See LICENSE file for details

## Contact

For questions or feedback about this MVP, please reach out to the development team.
