from services.models import EmailMessage, EmailThread, EnrichedContext
from services.context_analyzer import ContextAnalyzer
from anthropic import Anthropic

# Initialize Anthropic client
try:
    client = Anthropic()
except Exception as e:
    # Log the error but allow the function to proceed with graceful fallback
    print(f"Warning: Could not initialize Anthropic client. Ensure ANTHROPIC_API_KEY is set. Error: {e}")
    client = None

def summarize_emails(enriched_context: EnrichedContext) -> str:
    """
    Summarize email thread with multiple perspectives.

    Args:
        enriched_context: EnrichedContext object with analyzed insights

    Returns:
        Multi-layer summary covering surface, underlying, sentiment, and concerns
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure ANTHROPIC_API_KEY is set."

    thread = enriched_context.thread
    context_str = "\n".join([f"- {msg.subject}: {msg.body[:150]}..." for msg in thread.messages])

    prompt = f"""Summarize this email thread with these perspectives:

1. SURFACE SUMMARY: Key facts, explicit statements, decisions
2. UNDERLYING NEEDS: What's really being asked for?
3. SENTIMENT ARC: How did the tone change across messages?
4. DECISION POINTS: What needs to be decided or approved?
5. ACTION ITEMS: What needs to happen next?
6. PROFESSIONAL CONTEXT: Any implicit power dynamics or norms?
7. IMPLICIT CONCERNS: What worries or hesitations are present?

ENRICHED CONTEXT PROVIDED:
- Participants: {enriched_context.participants_analysis}
- Urgency: {enriched_context.urgency_assessment}
- Main topic: {enriched_context.thread.main_topic}
- Sentiment arc: {enriched_context.sentiment_arc}
- Extracted concerns: {', '.join(enriched_context.extracted_concerns)}

EMAIL THREAD:
{context_str}

Provide a comprehensive summary that shows you understand the full context."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error during summarization: {e}")
        return f"Could not summarize emails due to API error: {e}"

def generate_draft_reply(enriched_context: EnrichedContext, user_intent: str = None, tone: str = "professional") -> str:
    """
    Draft a reply that understands context, concerns, and email norms.

    Args:
        enriched_context: EnrichedContext object with analyzed insights
        user_intent: What the user wants to accomplish with the reply
        tone: Desired tone (professional, collaborative, assertive, etc.)

    Returns:
        Draft reply that addresses underlying needs and concerns
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure ANTHROPIC_API_KEY is set."

    thread = enriched_context.thread
    context_str = "\n".join([f"- {msg.subject}: {msg.body[:100]}..." for msg in thread.messages])

    intent_text = f"\nUSER'S INTENT: {user_intent}" if user_intent else ""

    prompt = f"""Draft a reply to this email thread.

THREAD CONTEXT:
- Participants: {enriched_context.participants_analysis}
- Current sentiment: {enriched_context.sentiment_arc} (latest message)
- Urgency: {enriched_context.urgency_assessment}
- Underlying ask: {enriched_context.thread.underlying_need}
- Key concerns: {', '.join(enriched_context.extracted_concerns)}
- Recommended tone: {enriched_context.tone_recommendations}{intent_text}
- TONE PREFERENCE: {tone}

EMAIL THREAD:
{context_str}

Your draft should:
1. Address the underlying need and concerns (not just the surface request)
2. Match the professional norms and expectations of this thread
3. Acknowledge any concerns or hesitations expressed
4. Use appropriate urgency and formality based on context
5. Show that you understand what's really at stake

Provide a ready-to-send email draft."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"An error occurred during draft generation: {e}"

def ask_question(question: str, enriched_context: EnrichedContext) -> str:
    """
    Answer questions about emails using enriched context.

    Args:
        question: User's question about the emails
        enriched_context: EnrichedContext object with analyzed insights

    Returns:
        Answer that demonstrates understanding of context and implicit meaning
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure ANTHROPIC_API_KEY is set."

    thread = enriched_context.thread
    context_str = "\n".join([f"- {msg.subject}: {msg.body[:100]}..." for msg in thread.messages])

    prompt = f"""Answer this question about emails: {question}

ENRICHED CONTEXT:
- Main topic: {enriched_context.thread.main_topic}
- Underlying need (what's really being asked): {enriched_context.thread.underlying_need}
- Implicit needs: {', '.join(enriched_context.implicit_needs)}
- Sentiment arc (how tone changed): {enriched_context.sentiment_arc}
- Key concerns: {', '.join(enriched_context.extracted_concerns)}
- Professional context: {enriched_context.professional_context}

EMAIL THREAD:
{context_str}

Consider the full conversation history and implicit meanings. Look beyond surface facts to understand what's really needed. Address not just what was asked, but what's underlying the question."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"An error occurred during question answering: {e}"

