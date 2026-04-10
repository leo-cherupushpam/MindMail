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