import os
import json
import pytest
from unittest.mock import patch, mock_open
from services.cache import get_cache_path, is_cache_valid, load_cache, save_cache
from services.models import EmailMessage, EmailThread


def test_get_cache_path_returns_correct_path():
    """Test cache path is correct"""
    path = get_cache_path()
    assert path.endswith('cached_emails.json')


def test_is_cache_valid_returns_false_when_missing():
    """Test that is_cache_valid returns False when cache doesn't exist"""
    with patch('os.path.exists', return_value=False):
        assert is_cache_valid() is False


def test_is_cache_valid_returns_true_when_exists():
    """Test that is_cache_valid returns True when cache exists"""
    with patch('os.path.exists', return_value=True):
        assert is_cache_valid() is True


def test_load_cache_returns_empty_list_when_missing():
    """Test that load_cache returns empty list when cache doesn't exist"""
    with patch('os.path.exists', return_value=False):
        result = load_cache()
        assert result == []


def test_save_cache_writes_json_file():
    """Test that save_cache writes threads to JSON"""
    mock_thread = EmailThread(
        messages=[],
        participants=['test@example.com'],
        main_topic='Test',
        underlying_need='test need',
        urgency='normal',
        action_items=[]
    )

    with patch('builtins.open', mock_open()) as mock_file:
        save_cache([mock_thread])
        mock_file.assert_called_once()
