import os
import json
import pytest
from unittest.mock import patch, MagicMock
from services.gmail_auth import is_authenticated, get_credentials_path


def test_is_authenticated_returns_false_when_no_credentials():
    """Test that is_authenticated returns False when credentials.json doesn't exist"""
    with patch('os.path.exists', return_value=False):
        assert is_authenticated() is False


def test_is_authenticated_returns_true_when_credentials_exist():
    """Test that is_authenticated returns True when credentials.json exists"""
    with patch('os.path.exists', return_value=True):
        assert is_authenticated() is True


def test_get_credentials_path_returns_correct_path():
    """Test that credentials path is correct"""
    path = get_credentials_path()
    assert path.endswith('credentials.json')
