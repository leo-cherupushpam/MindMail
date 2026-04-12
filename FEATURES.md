# Feature Guide

## Core Features

### 1. Email Browsing

**Description**: Browse and manage your email threads in an organized inbox view.

**Features:**
- View all email threads in left sidebar
- Threads show key metadata (subject, participants, message count)
- Visual urgency indicators (color-coded by importance)
- Clickable thread selection
- Participant information preview

**How to Use:**
1. Look at the email list in the left panel
2. Click any thread to view its full content
3. Selected thread is highlighted and displayed in the middle panel
4. Inbox is fully scrollable for many emails

**Data Shown:**
- Thread subject/main topic
- Participants involved
- Number of messages
- Urgency level (visual indicator)
- Preview of thread content

---

### 2. Thread Viewer

**Description**: Read complete email conversations with full context and analysis.

**Features:**
- Full email conversation display
- Chronological message ordering
- Sender and recipient information
- Message timestamps
- Automatic context enrichment
- Thread metadata (participants, message count)

**How to Use:**
1. Click an email thread in the inbox
2. Full conversation appears in the middle panel
3. Scroll to see all messages in the thread
4. View metadata at the top (topic, participants, date range)

**What You See:**
- Subject line
- Participant list and email addresses
- Date range of conversation
- All messages in order with:
  - Sender/recipient
  - Email address
  - Timestamp
  - Message body

---

### 3. Ask Questions (💬)

**Description**: Ask natural language questions about email content. The assistant understands context, implicit needs, and underlying concerns.

**Features:**
- Natural language Q&A
- Context-aware answers
- Understands implicit meanings
- Addresses underlying concerns
- Powered by GPT-5 nano for quality responses

**Example Questions:**
- "What's the main issue here?"
- "What action do I need to take?"
- "What are the customer's real concerns?"
- "Is there anything between the lines I should know?"
- "What's the urgency level and why?"
- "What are the implicit needs?"
- "What should my response address?"

**How to Use:**
1. Select an email thread
2. Click **"💬 Ask"** button in the assistant panel
3. Type your question in the text area
4. Press Enter or click Submit
5. The assistant analyzes the thread and provides an answer

**What Makes It Smart:**
- Provides enriched context about the thread
- Understands sentiment and urgency
- Identifies hidden needs and concerns
- Recognizes power dynamics and professional norms
- References specific details from the emails

**Output:**
- Thoughtful answer with specific examples from the thread
- References to relevant context
- Understanding of what's really being asked

---

### 4. Draft Replies (📋)

**Description**: Generate professional email replies that understand context and address underlying needs.

**Features:**
- AI-generated email drafts
- Context-aware tone matching
- Addresses underlying needs (not just surface requests)
- Customizable tone (professional, collaborative, assertive)
- Incorporates concern acknowledgment
- Shows draft with copy/regenerate options

**Tone Options:**
- **Professional**: Formal, respectful, authoritative
- **Collaborative**: Friendly, cooperative, team-oriented
- **Assertive**: Confident, direct, solution-focused
- **Empathetic**: Understanding, supportive, considerate

**How to Use:**
1. Select an email thread
2. Click **"📋 Draft"** button
3. (Optional) Enter your intent in the text area:
   - "Accept this opportunity"
   - "Request more information"
   - "Address concerns and propose solution"
4. (Optional) Select a tone preference
5. Click to generate draft
6. Review the generated email
7. Click **"📋 Copy"** to copy to clipboard
8. Or click **"🔄 Regenerate"** for another version

**What Makes It Smart:**
- Analyzes the full conversation history
- Understands sentiment arc and how tone has changed
- Identifies urgency level and professional norms
- Incorporates tone recommendations
- Addresses implicit concerns
- Shows understanding of what's really at stake

**Output:**
- Ready-to-send email draft
- Professional formatting
- Appropriate length and detail
- Matches thread's tone and formality

---

### 5. Summarize (📊)

**Description**: Create multi-perspective summaries of email threads covering all important aspects.

**Features:**
- AI-generated summaries
- Multi-perspective analysis
- Covers surface facts, underlying needs, sentiment, and concerns
- Identifies decision points and action items
- Fast generation (uses optimized nano model)
- Shows formatted summary with copy option

**Summary Includes:**

1. **Surface Summary**: Key facts, explicit statements, and decisions
2. **Underlying Needs**: What's really being asked for
3. **Sentiment Arc**: How the tone changed across messages
4. **Decision Points**: What needs to be decided or approved
5. **Action Items**: What needs to happen next
6. **Professional Context**: Implicit power dynamics and norms
7. **Implicit Concerns**: Worries, hesitations, and potential blockers

**How to Use:**
1. Select an email thread
2. Click **"📊 Summarize"** button
3. Wait for the AI to generate summary
4. Review the multi-perspective summary
5. Click **"📋 Copy Summary"** to copy to clipboard
6. Or click **"🔄 Regenerate"** for another perspective

**When to Use:**
- Long email chains that are hard to parse
- Understanding complex negotiations
- Getting up to speed on ongoing discussions
- Finding action items quickly
- Understanding underlying concerns
- Preparing for meetings or responses

**Output:**
- Comprehensive summary
- Multiple perspectives
- Specific examples from the thread
- Clear action items
- Highlighted concerns and needs

---

## Context Analysis Features

### Automatic Email Enrichment

Every email thread is automatically analyzed for:

#### Urgency Assessment
- **Critical**: Immediate action required
- **Urgent**: Time-sensitive, needs response soon
- **High**: Important but slightly flexible timeline
- **Normal**: Standard priority
- **Low**: Can wait or is informational

**Detection:** Analyzes keywords, deadlines, business impact, and explicit urgency markers.

#### Action Items Extraction
- **Explicit**: "You need to...", "Please...", "Can you..."
- **Implicit**: Unspoken expectations from context
- **Deadline-dependent**: Actions tied to specific dates

#### Sentiment Analysis
- **Positive**: Supportive, collaborative, appreciative tone
- **Neutral**: Matter-of-fact, professional, balanced
- **Negative**: Critical, frustrated, urgent concerns

Tracks **sentiment arc** (how sentiment changes across messages).

#### Implicit Needs Detection
Identifies what's really being asked for:
- **Approval-seeking**: Needs sign-off or authorization
- **Data/Evidence**: Requires supporting information
- **Concern addressing**: Needs to acknowledge worries
- **Decision support**: Needs help deciding
- **Relationship building**: Needs reassurance or connection

#### Concern Extraction
Identifies worries and hesitations:
- Performance concerns
- Budget concerns
- Timeline concerns
- Technical concerns
- Relationship concerns
- Strategic concerns

#### Tone Recommendations
Suggests appropriate response tone based on:
- Thread sentiment and urgency
- Professional relationships
- Power dynamics
- Time sensitivity
- Emotional content

---

## UI Features

### Responsive Layout
- **Left Panel**: Scrollable email inbox (width scales to content)
- **Middle Panel**: Fixed-height thread viewer with scrollable messages
- **Right Panel**: Scrollable assistant sidebar for tools and output

### Scrolling Behavior
- **Inbox**: Fully scrollable when many emails present
- **Messages**: Scrollable message container within fixed height
- **Assistant**: Scrollable output and tool results

### Color Coding & Visual Indicators
- Urgency levels shown with visual indicators
- Selected thread highlighted
- Clear button states (hover, active, disabled)
- Responsive button sizing

### Interactive Elements
- Clickable thread selection
- Expandable/collapsible sections
- Copy buttons for generated content
- Regenerate buttons for alternative outputs
- Progress indicators during AI processing

---

## Using the Assistant Effectively

### Best Practices

**For Asking Questions:**
- Be specific about what you want to know
- Reference specific people or statements
- Ask about implications and underlying meanings
- Use follow-up questions to dig deeper

**For Drafting:**
- State your intent clearly (what you want to accomplish)
- Choose the right tone for your relationship
- Review the draft before sending
- Use regenerate if tone isn't quite right

**For Summarizing:**
- Use when threads are long (5+ messages)
- Great for getting colleagues up to speed
- Helps identify action items quickly
- Useful before meetings

### Tips & Tricks

1. **Understanding Concerns**: Ask "What is this person concerned about?"
2. **Hidden Agendas**: Ask "What's the real ask here?"
3. **Decision Support**: Ask "What information would help me decide?"
4. **Tone Matching**: Ask "What tone should I use in my response?"
5. **Urgency**: Ask "How urgent is this really?"

---

## Examples

### Example 1: Production Bug (Urgent Context)

**Thread**: Customer reports critical data loss bug

**Good Questions:**
- "What's the business impact?"
- "What caused this and how do we prevent it?"
- "What's the customer's real concern?"

**Draft Use Case:**
- Intent: "I'm going to investigate and provide updates"
- Tone: "Confident and reassuring"

**Summarize Use Case:**
- Understand full scope of issue
- Identify action items
- See customer's concerns

---

### Example 2: Collaboration (Design Feedback)

**Thread**: Designer requesting feedback on mockups

**Good Questions:**
- "What specific feedback is most important?"
- "What are the design constraints?"

**Draft Use Case:**
- Intent: "Provide constructive feedback"
- Tone: "Collaborative"

**Summarize Use Case:**
- Quick feedback on changes
- What's needed next

---

### Example 3: Negotiation (Contract Renewal)

**Thread**: Long negotiation about contract terms

**Good Questions:**
- "What's the customer's main concern?"
- "What are the implicit needs here?"
- "What can we compromise on?"

**Draft Use Case:**
- Intent: "Propose a solution that works for both sides"
- Tone: "Professional and collaborative"

**Summarize Use Case:**
- Understand full negotiation context
- See sentiment arc and how things are progressing
- Identify decision points

---

## Performance & Tips

### Response Times
- **Summarize**: ~2-5 seconds (uses fast nano model)
- **Draft**: ~5-8 seconds (uses higher quality model)
- **Ask**: ~5-15 seconds (depends on question complexity)

### Tips for Better Results
1. **Long threads**: Summarize first to understand context
2. **Multiple questions**: Ask progressive questions to go deeper
3. **Drafting**: Start with clear intent for better results
4. **Tone matters**: Choose appropriate tone for the relationship
5. **Review drafts**: Always review before sending

### Limitations & Future Work
- Single thread focus (multi-thread comparisons coming)
- No email scheduling yet
- No template suggestions yet
- No custom AI fine-tuning yet

---

## Keyboard Shortcuts & Accessibility

- **Tab**: Navigate between elements
- **Enter**: Submit in text areas
- **Escape**: Close dialogs (when implemented)
- **Copy**: Use copy buttons for generated content

## Troubleshooting

**Q: Assistant features not responding**
A: Check that your OpenAI API key is set correctly

**Q: Drafts don't match my tone**
A: Try regenerating with explicit tone selection, or add tone preferences in your intent

**Q: Questions get off-topic answers**
A: Be more specific with your question and reference specific people/dates in the email

**Q: Summaries are too long**
A: They cover multiple perspectives - select relevant sections for what you need
