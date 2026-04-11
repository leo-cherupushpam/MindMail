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


def test_save_credentials_writes_json_file(tmp_path):
    """Test that save_credentials writes valid JSON"""
    from services.gmail_auth import save_credentials

    mock_creds = MagicMock()
    mock_creds.token = 'test_token'
    mock_creds.refresh_token = 'test_refresh'
    mock_creds.token_uri = 'https://oauth2.googleapis.com/token'
    mock_creds.client_id = 'test_client_id'
    mock_creds.client_secret = 'test_client_secret'
    mock_creds.scopes = ['https://www.googleapis.com/auth/gmail.readonly']

    # Mock file write
    with patch('builtins.open', create=True) as mock_file:
        with patch('services.gmail_auth.get_credentials_path', return_value=str(tmp_path / 'creds.json')):
            save_credentials(mock_creds)
            mock_file.assert_called_once()


def test_load_credentials_returns_none_when_missing():
    """Test that load_credentials returns None when file doesn't exist"""
    from services.gmail_auth import load_credentials

    with patch('os.path.exists', return_value=False):
        result = load_credentials()
        assert result is None


def test_refresh_token_if_needed_skips_when_not_expired():
    """Test that refresh_token_if_needed skips refresh when token not expired"""
    from services.gmail_auth import refresh_token_if_needed

    mock_creds = MagicMock()
    mock_creds.expired = False

    result = refresh_token_if_needed(mock_creds)
    mock_creds.refresh.assert_not_called()
    assert result == mock_creds
