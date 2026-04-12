# Gmail Email Assistant

An intelligent email management tool for GMAIL that uses AI to help you understand, summarize, and respond to emails with context-aware insights.

## Features

### 📧 Smart Email Management
- **Email Inbox**: Browse and organize email threads with intelligent prioritization
- **Thread Viewer**: Read full email conversations with context analysis
- **Scrollable Interface**: Smooth navigation with inbox and assistant panels independently scrollable

### 🤖 AI-Powered Assistant

#### Ask (💬)
Ask natural language questions about email content. The assistant understands context, implicit needs, and underlying concerns to provide insightful answers.

**Example questions:**
- "What's the main concern in this thread?"
- "What action do I need to take?"
- "What are the implicit concerns from the customer?"

<img width="1895" height="900" alt="image" src="https://github.com/user-attachments/assets/24326679-8d2a-40e0-902d-10623071d8f4" />


#### Draft (📋)
Generate professional email replies that understand context and address underlying needs. Matches the appropriate tone based on the email thread's sentiment and urgency.

<img width="1853" height="842" alt="image" src="https://github.com/user-attachments/assets/64db2348-f5b7-4c32-8b91-2561e8d8fcb2" />

**Supports:**
- Professional tone recommendations
- Concern-aware drafting
- Intent-based reply generation
- Tone customization (professional, collaborative, assertive, etc.)

#### Summarize (📊)
Create multi-perspective summaries of email threads covering:
- Surface facts and explicit statements
- Underlying needs and implicit asks
- Sentiment arc and tone changes
- Decision points requiring action
- Professional context and power dynamics
- Implicit concerns and hesitations

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
- **Frontend**: Streamlit (Python web framework)
- **AI Models**: 
  - `gpt-4.1-nano-2025-04-14` for summarization (high-volume, cost-optimized)
  - `gpt-5-nano-2025-08-07` for drafting and Q&A (quality-critical)
- **API**: OpenAI API
- **Data**: Mock email threads for MVP showcase

### Project Structure
```
gmail-email-assistant/
├── app/
│   └── main.py                 # Streamlit UI application
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
- OpenAI API key
- Streamlit

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd gmail-email-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the App

```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

## Usage

1. **Browse Emails**: Click on email threads in the inbox (left panel)
2. **View Thread**: Read full conversation in the thread viewer (middle panel)
3. **Ask Questions**: Use the "Ask" feature to ask about the email
4. **Draft Replies**: Click "Draft" to generate a context-aware response
5. **Summarize**: Click "Summarize" to get a multi-perspective summary

## Model Strategy

### SEARCH_MODEL: `gpt-4.1-nano-2025-04-14`
Used for high-volume, lower-latency tasks:
- Email summarization
- Content organization
- Rule suggestion

**Why nano**: Cost-optimized while maintaining quality for summary tasks

### DRAFTING_MODEL: `gpt-5-nano-2025-08-07`
Used for quality-critical, complex reasoning tasks:
- Draft reply generation
- Complex question answering
- Context-aware decision support

**Why GPT-5**: Better quality for tasks that directly impact user experience

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
# Make sure .env file exists and contains:
OPENAI_API_KEY=your_key_here
```

### Model Not Available
Check that your OpenAI account has access to:
- `gpt-4.1-nano-2025-04-14`
- `gpt-5-nano-2025-08-07`

## Performance Notes

- **Summarization**: Uses nano model for faster responses (typically <5s)
- **Drafting**: Uses GPT-5 for quality (typically <8s)
- **Q&A**: Depends on question complexity (typically 5-15s)

## License

MIT License - See LICENSE file for details

## Contact

For questions or feedback about this MVP, please reach out to the development team.
