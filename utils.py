"""
Utility functions for Gmail Email Assistant
Contains reusable helpers to reduce code duplication in main.py
"""
import streamlit as st
from typing import Any, Callable, Dict, Optional, Tuple


def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """
    Safely execute a function with error handling and Streamlit error display.

    Args:
        func: Function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Function result if successful, None if error occurred
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def with_spinner(message: str, func: Callable, *args, **kwargs) -> Any:
    """
    Execute a function with a Streamlit spinner and error handling.

    Args:
        message: Message to display in the spinner
        func: Function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Function result if successful, None if error occurred
    """
    with st.spinner(message):
        return safe_execute(func, *args, **kwargs)


def primary_button(label: str, key: Optional[str] = None) -> bool:
    """
    Create a primary button with consistent styling.

    Args:
        label: Button label
        key: Optional unique key for the button

    Returns:
        True if button was clicked, False otherwise
    """
    return st.button(label, type="primary", use_container_width=True, key=key)


def secondary_button(label: str, key: Optional[str] = None) -> bool:
    """
    Create a secondary button with consistent styling.

    Args:
        label: Button label
        key: Optional unique key for the button

    Returns:
        True if button was clicked, False otherwise
    """
    return st.button(label, use_container_width=True, key=key)


def show_success(content: str) -> None:
    """
    Display content in a success box.

    Args:
        content: Content to display
    """
    st.markdown(f'<div class="success-box">{content}</div>', unsafe_allow_html=True)


def show_info(content: str) -> None:
    """
    Display content in an info box.

    Args:
        content: Content to display
    """
    st.markdown(f'<div class="info-box">{content}</div>', unsafe_allow_html=True)


def show_warning(content: str) -> None:
    """
    Display content in a warning box.

    Args:
        content: Content to display
    """
    st.markdown(f'<div class="warning-box">{content}</div>', unsafe_allow_html=True)


def show_error(content: str) -> None:
    """
    Display content in an error box.

    Args:
        content: Content to display
    """
    st.markdown(f'<div class="error-box">{content}</div>', unsafe_allow_html=True)


def update_context(base_context: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a updated context dictionary without modifying the original.

    Args:
        base_context: Base context dictionary
        updates: Dictionary of updates to apply

    Returns:
        New context dictionary with updates applied
    """
    import copy
    context = copy.deepcopy(base_context)

    def _update_dict(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                _update_dict(d[k], v)
            else:
                d[k] = v

    _update_dict(context, updates)
    return context


def add_chat_exchange(user_message: str, assistant_message: str) -> None:
    """
    Add a user-assistant message exchange to chat history.

    Args:
        user_message: User's message
        assistant_message: Assistant's response
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append({"role": "user", "content": user_message})
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_message})


def render_feature_header(title: str, description: str) -> None:
    """
    Render a consistent feature header with title and description.

    Args:
        title: Feature title
        description: Feature description
    """
    st.markdown(f"### {title}")
    st.markdown(description)


def render_input_section(
    input_type: str,
    label: str,
    placeholder: str = "",
    height: Optional[int] = None,
    key: Optional[str] = None
) -> Any:
    """
    Render a standardized input section.

    Args:
        input_type: Type of input ('text', 'textarea', 'selectbox')
        label: Input label
        placeholder: Placeholder text
        height: Height for textarea (if applicable)
        key: Unique key for the input

    Returns:
        Input value
    """
    if input_type == "text":
        return st.text_input(label, placeholder=placeholder, key=key, label_visibility="collapsed")
    elif input_type == "textarea":
        return st.text_area(label, placeholder=placeholder, height=height, key=key, label_visibility="collapsed")
    elif input_type == "selectbox":
        # This would need options passed differently - for now return placeholder
        return st.selectbox(label, options=[placeholder], key=key, label_visibility="collapsed")
    else:
        return st.text_input(label, placeholder=placeholder, key=key, label_visibility="collapsed")


def render_chat_message(role: str, content: str) -> None:
    """
    Render a styled chat message bubble.

    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Assistant:</strong> {content}
        </div>
        """, unsafe_allow_html=True)


def render_email_card(email_data: Dict[str, str]) -> None:
    """
    Render an email as a styled card.

    Args:
        email_data: Dictionary with keys 'subject', 'sender', 'body' (optional)
    """
    subject = email_data.get('subject', 'No Subject')
    sender = email_data.get('sender', 'Unknown Sender')
    body = email_data.get('body', 'No content available')

    # Truncate body for preview
    preview = body[:100] + "..." if len(body) > 100 else body

    st.markdown(f"""
    <div class="email-card">
        <div class="email-header">
            <strong>From:</strong> {sender}
        </div>
        <div class="email-subject">
            <strong>Subject:</strong> {subject}
        </div>
        <div class="email-preview">
            {preview}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_feature_container(title: str = None) -> Any:
    """
    Render a consistent feature container with optional title.

    Args:
        title: Optional title for the container

    Returns:
        Streamlit container object
    """
    container = st.container()
    if title:
        with container:
            st.markdown(f"### {title}")
    return container


def get_responsive_columns(ratio_desktop: tuple, ratio_mobile: tuple = (1, 1)) -> tuple:
    """
    Get appropriate column ratio based on screen size.
    Note: This is a simplified approach - Streamlit doesn't have built-in media queries.
    In practice, you'd use session state or JavaScript for true responsiveness.

    Args:
        ratio_desktop: Column ratio for desktop (e.g., (3, 1))
        ratio_mobile: Column ratio for mobile (default: equal)

    Returns:
        Column ratio tuple
    """
    # For now, return desktop ratio - true responsiveness would require
    # session state tracking or frontend integration
    return ratio_desktop


# ============================================================================
# DESIGN SYSTEM COMPONENTS - Modern UI
# ============================================================================

def render_feature_card(icon: str, title: str, description: str, is_selected: bool = False) -> None:
    """
    Render a styled feature card with hover and active states.

    Args:
        icon: Emoji icon (e.g., "💬")
        title: Feature title (e.g., "Conversational Q&A")
        description: Feature description (1-2 lines)
        is_selected: Whether this card is selected/active

    Returns:
        None (renders using st.markdown)
    """
    active_class = "active" if is_selected else ""
    card_html = f"""
    <div class="feature-card {active_class}">
        <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
        <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px; color: var(--color-neutral-900);">
            {title}
        </div>
        <div style="font-size: 14px; color: var(--color-neutral-600); line-height: 1.5;">
            {description}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_input_card(label: str, content_html: str = None) -> None:
    """
    Render a styled input card container.

    Args:
        label: Label text displayed above the input
        content_html: HTML content for the input section (optional, use Streamlit widgets instead)

    Returns:
        None (renders using st.markdown)
    """
    label_html = f"""
    <div class="input-card">
        <label>{label}</label>
    """
    st.markdown(label_html, unsafe_allow_html=True)

    if content_html:
        st.markdown(content_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_chat_message(role: str, content: str) -> None:
    """
    Render a styled chat message bubble.

    Args:
        role: 'user' or 'assistant'
        content: Message content

    Returns:
        None (renders using st.markdown)
    """
    message_class = f"chat-message {role}-message"
    message_html = f"""
    <div class="{message_class}">
        <div>
            <strong>{"You:" if role == "user" else "Assistant:"}</strong> {content}
        </div>
    </div>
    """
    st.markdown(message_html, unsafe_allow_html=True)


def show_success_box(content: str, title: str = "Success") -> None:
    """
    Display content in a styled success box with icon.

    Args:
        content: Content to display
        title: Box title (default: "Success")

    Returns:
        None (renders using st.markdown)
    """
    html = f"""
    <div class="success-box">
        <div style="font-weight: 600; color: var(--color-success); margin-bottom: 8px;">✓ {title}</div>
        <div style="font-size: 14px; color: var(--color-neutral-900);">{content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def show_info_box(content: str, title: str = "Information") -> None:
    """
    Display content in a styled info box with icon.

    Args:
        content: Content to display
        title: Box title (default: "Information")

    Returns:
        None (renders using st.markdown)
    """
    html = f"""
    <div class="info-box">
        <div style="font-weight: 600; color: var(--color-primary); margin-bottom: 8px;">ℹ {title}</div>
        <div style="font-size: 14px; color: var(--color-neutral-900);">{content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def show_warning_box(content: str, title: str = "Warning") -> None:
    """
    Display content in a styled warning box with icon.

    Args:
        content: Content to display
        title: Box title (default: "Warning")

    Returns:
        None (renders using st.markdown)
    """
    html = f"""
    <div class="warning-box">
        <div style="font-weight: 600; color: var(--color-warning); margin-bottom: 8px;">⚠ {title}</div>
        <div style="font-size: 14px; color: var(--color-neutral-900);">{content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def show_error_box(content: str, title: str = "Error") -> None:
    """
    Display content in a styled error box with icon.

    Args:
        content: Content to display
        title: Box title (default: "Error")

    Returns:
        None (renders using st.markdown)
    """
    html = f"""
    <div class="error-box">
        <div style="font-weight: 600; color: var(--color-error); margin-bottom: 8px;">✕ {title}</div>
        <div style="font-size: 14px; color: var(--color-neutral-900);">{content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_empty_state(icon: str, title: str, message: str) -> None:
    """
    Render an empty state with icon, title, and message.

    Args:
        icon: Emoji icon (e.g., "📭")
        title: Empty state title
        message: Empty state message

    Returns:
        None (renders using st.markdown)
    """
    html = f"""
    <div style="text-align: center; padding: 48px 24px; color: var(--color-neutral-600);">
        <div style="font-size: 50px; margin-bottom: 16px;">{icon}</div>
        <div style="font-size: 18px; font-weight: 600; color: var(--color-neutral-900); margin-bottom: 8px;">
            {title}
        </div>
        <div style="font-size: 14px; line-height: 1.5;">
            {message}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)