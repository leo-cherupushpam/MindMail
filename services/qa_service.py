import os
from openai import OpenAI
from typing import Dict, Any

# --- Configuration ---
# In a real application, these should be loaded from environment variables or a secrets manager.
# Model assignment based on user decision:
SEARCH_MODEL = "gpt-4.1-nano-2025-04-14" # For search/summarization (high-volume)
DRAFTING_MODEL = "gpt-5-nano-2025-08-07" # For quality-critical tasks (drafting)

# Initialize OpenAI client. Assume API key is set in environment variables for local testing.
try:
    client = OpenAI()
except Exception as e:
    # Log the error but allow the function to proceed with graceful fallback
    print(f"Warning: Could not initialize OpenAI client. Ensure OPENAI_API_KEY is set. Error: {e}")
    client = None

def summarize_emails(context_data: Dict[str, Any]) -> str:
    """
    Summarizes the content from a list of emails provided in context_data.
    Uses the Search/Summarization model to create a raw, factual summary.
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure the OPENAI_API_KEY environment variable is set."

    if not context_data.get('emails'):
        return "No email context provided to summarize."

    email_list = ", ".join(context_data['emails'])

    system_prompt = "You are an expert Email Data Analyst. Your task is to synthesize information from the provided email list into a single, comprehensive, and neutral summary."
    user_content = f"""
    Summarize the following emails. Focus on key topics, action items, and main decisions made.
    If the emails cover disparate topics, structure the summary using clear headings or bullet points.

    ---
    Context Sources (Simulated): {email_list}
    ---
    """
    try:
        search_response = client.chat.completions.create(
            model=SEARCH_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1
        )
        return search_response.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return f"Could not summarize emails due to API error: {e}"

def generate_draft_reply(user_query: str, context_data: Dict[str, Any]) -> str:
    """
    Drafts a professional, actionable email reply based on the user's intent and context.
    Uses the Drafting model to adopt a specific tone and structure.

    Args:
        user_query: The intended action or message content.
        context_data: Context including recipients and actions needed.

    Returns:
        A string containing the draft email reply, or an error message.
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure the OPENAI_API_KEY environment variable is set."

    # Gather context elements for the drafting LLM prompt
    recipient = context_data.get('metadata', {}).get('recipient', 'the relevant parties')
    action = context_data.get('metadata', {}).get('action_needed', 'the core topic')

    # Craft the prompt, emphasizing tone and structure for the Drafting model
    synthesis_prompt = f"""
    Draft a professional, actionable email reply. The tone must be: {context_data.get('tone', 'professional and polite')}.
    The core purpose of the email is to communicate: "{user_query}".

    Key Context:
    - Primary Action: {action}
    - Intended Recipient: {recipient}

    Instructions for the draft:
    1. The subject line should be concise and actionable.
    2. The body must be structured: Greeting -> Core Message -> Call to Action.
    3. Use professional salutations and sign-offs.
    4. Do not write filler; be direct and actionable.
    """
    try:
        synthesis_response = client.chat.completions.create(
            model=DRAFTING_MODEL,
            messages=[
                {"role": "system", "content": "You are a highly skilled executive assistant drafting professional emails."},
                {"role": "user", "content": synthesis_prompt}
            ],
            temperature=0.3
        )
        return synthesis_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred during draft generation: {e}"

def ask_question(user_query: str, context_data: Dict[str, Any]) -> str:
    """
    Handles conversational Q&A over emails using a hybrid LLM approach.

    It first uses a fast model for context retrieval/summarization (Search/Summarization)
    and then uses a higher-quality model for final answer synthesis (Drafting).

    Args:
        user_query: The natural language question from the user.
        context_data: A dictionary containing context like 'emails' and 'metadata'.

    Returns:
        A string containing the grounded, natural language answer, or an error message.
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure the OPENAI_API_KEY environment variable is set."

    # 1. Context Grounding/Summarization Step (High Volume, Low Cost)
    # We use the dedicated summarize_emails function here for the initial context lift.
    grounding_summary = summarize_emails(context_data)

    # 2. Final Synthesis Step (Quality Critical, High Cost)
    synthesis_prompt = f"""
    You are a professional AI assistant synthesizing an answer for a user.
    The goal is to answer the query: "{user_query}"
    Use the following context summary derived from emails:
    ---
    {grounding_summary}
    ---

    Your final response must be conversational, professional, and directly answer the user query,
    while strictly being grounded in the provided context summary. Structure it clearly, using appropriate formatting like bullet points or paragraphs.
    """
    try:
        synthesis_response = client.chat.completions.create(
            model=DRAFTING_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful, conversational AI assistant that synthesizes technical summaries into polished, natural language responses."},
                {"role": "user", "content": synthesis_prompt}
            ],
            temperature=0.3
        )
        return synthesis_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred during final response synthesis: {e}"

def organize_threads(user_query: str, context_data: Dict[str, Any]) -> str:
    """
    Organizes and filters email threads based on a user query.
    Returns a structured list of relevant threads organized by topic/date/participant.

    Args:
        user_query: The natural language query for threads (e.g., "Show me all emails about project launch").
        context_data: A dictionary containing 'emails' list and 'metadata' (topic, date_range, etc.).

    Returns:
        A string containing organized thread information, or an error message.
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure the OPENAI_API_KEY environment variable is set."

    if not context_data.get('emails'):
        return "No email threads available to organize."

    email_list = ", ".join(context_data['emails'])
    topic = context_data.get('metadata', {}).get('topic', 'general')
    date_range = context_data.get('metadata', {}).get('date_range', 'all time')

    system_prompt = "You are an expert Email Organization Assistant. Your task is to organize and filter email threads based on user queries."
    user_content = f"""
    Organize the following email threads based on the user's query.

    User Query: "{user_query}"
    Topic Filter: {topic}
    Date Range: {date_range}

    Available Email Threads: {email_list}

    Instructions:
    1. Filter threads relevant to the user's query and topic.
    2. Organize them by date or sub-topic if multiple threads exist.
    3. Provide a brief description of each thread's content.
    4. If no matching threads are found, clearly state that.
    5. Structure the output with clear headings or bullet points.
    """

    try:
        search_response = client.chat.completions.create(
            model=SEARCH_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1
        )
        return search_response.choices[0].message.content
    except Exception as e:
        print(f"Error during thread organization: {e}")
        return f"Could not organize threads due to API error: {e}"

def suggest_inbox_rules(context_data: Dict[str, Any]) -> str:
    """
    Analyzes emails and suggests inbox rules for categorization, labeling, and auto-archiving.

    Args:
        context_data: A dictionary containing 'emails' list with email metadata (subject, sender, category).

    Returns:
        A string containing suggested inbox rules, or an error message.
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure the OPENAI_API_KEY environment variable is set."

    if not context_data.get('emails'):
        return "No emails available to analyze for inbox rules."

    # Format emails for the prompt
    emails_info = "\n".join([
        f"- Subject: {email.get('subject', 'N/A')}, Sender: {email.get('sender', 'N/A')}, Category: {email.get('category', 'N/A')}"
        for email in context_data['emails']
    ])

    system_prompt = "You are an expert Email Productivity Consultant. Your task is to analyze email patterns and suggest actionable inbox rules for categorization, labeling, and auto-archiving."
    user_content = f"""
    Analyze the following emails and suggest inbox rules for better organization.

    Emails to Analyze:
    {emails_info}

    Instructions:
    1. Identify patterns in senders, subjects, or content that suggest automatic categorization.
    2. Suggest labels or tags for different types of emails (e.g., "Promotional", "Important", "Internal", "Newsletters").
    3. Recommend which emails could be auto-archived (low priority, bulk notifications).
    4. Recommend which emails should be marked as high priority (from key contacts, urgent subjects).
    5. Structure the output with clear rule suggestions in the format: "IF [condition] THEN [action]".
    """

    try:
        search_response = client.chat.completions.create(
            model=SEARCH_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1
        )
        return search_response.choices[0].message.content
    except Exception as e:
        print(f"Error during inbox rules analysis: {e}")
        return f"Could not analyze inbox rules due to API error: {e}"

def extract_meeting_details(context_data: Dict[str, Any]) -> str:
    """
    Extracts meeting details (date, time, participants, agenda) from email threads.

    Args:
        context_data: A dictionary containing 'emails' list with email metadata (subject, sender, body).

    Returns:
        A string containing structured meeting information, or an error message.
    """
    if client is None:
        return "Error: LLM client not configured. Please ensure the OPENAI_API_KEY environment variable is set."

    if not context_data.get('emails'):
        return "No emails available to extract meeting details from."

    # Format emails for the prompt
    emails_info = "\n".join([
        f"- Subject: {email.get('subject', 'N/A')}\n  From: {email.get('sender', 'N/A')}\n  Body: {email.get('body', 'N/A')}"
        for email in context_data['emails']
    ])

    system_prompt = "You are an expert Meeting Scheduler Assistant. Your task is to extract meeting details from email threads, including proposed dates, times, participants, and agenda topics."
    user_content = f"""
    Extract meeting details from the following email thread.

    Email Thread:
    {emails_info}

    Instructions:
    1. Identify any proposed meeting dates and times.
    2. List all participants mentioned in the thread.
    3. Extract the meeting agenda or purpose.
    4. If no meeting details are found, clearly state that.
    5. Structure the output with clear sections: Date/Time, Participants, Agenda.
    """

    try:
        search_response = client.chat.completions.create(
            model=SEARCH_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1
        )
        return search_response.choices[0].message.content
    except Exception as e:
        print(f"Error during meeting details extraction: {e}")
        return f"Could not extract meeting details due to API error: {e}"