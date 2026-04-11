# Gmail Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable the Streamlit app to authenticate with Gmail, fetch real emails, cache them locally, and replace mock data with actual email threads.

**Architecture:** Three independent services (auth, cache, fetcher) that integrate into the main app. Auth handles OAuth tokens, cache manages local file I/O, fetcher bridges Gmail API to app data models. Main app UI updated to trigger auth flow and show real emails.

**Tech Stack:** `google-auth-oauthlib`, `google-api-python-client`, `html2text`, existing OpenAI integration for sentiment analysis.

---

## File Structure

**New files:**
- `services/gmail_auth.py` — OAuth flow, token lifecycle, credential storage
- `services/gmail_fetcher.py` — Gmail API calls, data model mapping, batch fetching
- `services/cache.py` — Cache file I/O, validation, metadata management
- `tests/test_gmail_auth.py` — Auth service unit tests
- `tests/test_gmail_fetcher.py` — Fetcher mapping and API tests
- `tests/test_cache.py` — Cache file management tests

**Modified files:**
- `app/main.py` — Add auth UI buttons, replace mock data with cache
- `requirements.txt` — Add Google API libraries
- `.gitignore` — Ensure `credentials.json` and `cached_emails.json` are ignored

---

## Phase 1: Setup & Dependencies

### Task 1: Update requirements.txt with Gmail dependencies

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Read current requirements.txt**

```bash
cat requirements.txt
```

Expected output:
```
streamlit>=1.28.0
openai>=1.3.0
```

- [ ] **Step 2: Add Google API libraries**

Replace `requirements.txt` with:
```
streamlit>=1.28.0
openai>=1.3.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.80.0
html2text>=2024.2.26
```

- [ ] **Step 3: Install new dependencies**

```bash
pip install -r requirements.txt
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "deps: add Google Gmail API and html2text libraries"
```

---

### Task 2: Update .gitignore for credentials and cache

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Verify .gitignore exists and check current content**

```bash
grep -E "credentials|cache" .gitignore || echo "No existing entries"
```

- [ ] **Step 2: Add Gmail-specific ignore patterns**

Append to `.gitignore`:
```
# Gmail credentials and cache
credentials.json
cached_emails.json
.streamlit/
```

- [ ] **Step 3: Verify entries added**

```bash
tail -5 .gitignore
```

Expected:
```
# Gmail credentials and cache
credentials.json
cached_emails.json
.streamlit/
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: add credentials and cache to gitignore"
```

---

## Phase 2: Authentication Service

### Task 3: Create gmail_auth.py — OAuth flow and token management

**Files:**
- Create: `services/gmail_auth.py`

- [ ] **Step 1: Write the failing test for authentication check**

Create `tests/test_gmail_auth.py`:

```python
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
```

Run: `pytest tests/test_gmail_auth.py::test_is_authenticated_returns_false_when_no_credentials -v`

Expected: FAIL (module doesn't exist)

- [ ] **Step 2: Create gmail_auth.py with basic structure**

```python
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials_path():
    """Return the path to credentials.json"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')


def is_authenticated():
    """Check if user is authenticated (credentials.json exists and is valid)"""
    creds_path = get_credentials_path()
    return os.path.exists(creds_path)


def load_credentials():
    """Load credentials from credentials.json if it exists"""
    creds_path = get_credentials_path()
    if not os.path.exists(creds_path):
        return None
    
    with open(creds_path, 'r') as f:
        creds_data = json.load(f)
    
    creds = Credentials.from_authorized_user_info(creds_data, scopes=[
        'https://www.googleapis.com/auth/gmail.readonly'
    ])
    
    return creds


def save_credentials(creds):
    """Save credentials to credentials.json"""
    creds_path = get_credentials_path()
    creds_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
    
    with open(creds_path, 'w') as f:
        json.dump(creds_data, f, indent=2)


def refresh_token_if_needed(creds):
    """Refresh access token if expired"""
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_credentials(creds)
    return creds


def get_gmail_service():
    """Get authenticated Gmail API service client"""
    from googleapiclient.discovery import build
    
    creds = load_credentials()
    if not creds:
        return None
    
    creds = refresh_token_if_needed(creds)
    service = build('gmail', 'v1', credentials=creds)
    
    return service


def start_oauth_flow(client_secrets_file='client_secret.json'):
    """
    Start OAuth 2.0 flow. User must have downloaded client_secret.json from Google Cloud Console.
    Returns the authorization URL.
    """
    if not os.path.exists(client_secrets_file):
        raise FileNotFoundError(
            f"{client_secrets_file} not found. Download from Google Cloud Console OAuth 2.0 credentials."
        )
    
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        scopes=['https://www.googleapis.com/auth/gmail.readonly']
    )
    
    creds = flow.run_local_server(port=0)
    save_credentials(creds)
    
    return creds


def logout():
    """Delete credentials.json to log out"""
    creds_path = get_credentials_path()
    if os.path.exists(creds_path):
        os.remove(creds_path)
```

- [ ] **Step 3: Run all auth tests**

```bash
pytest tests/test_gmail_auth.py -v
```

Expected: 3 PASS

- [ ] **Step 4: Commit**

```bash
git add services/gmail_auth.py tests/test_gmail_auth.py
git commit -m "feat: add Gmail OAuth authentication service"
```

---

### Task 4: Add more auth tests for token refresh and credential saving

**Files:**
- Modify: `tests/test_gmail_auth.py`

- [ ] **Step 1: Add tests for token refresh and save**

Update `tests/test_gmail_auth.py` to add at the end:

```python
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
```

- [ ] **Step 2: Run tests**

```bash
pytest tests/test_gmail_auth.py -v
```

Expected: 6 PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_gmail_auth.py
git commit -m "test: add token refresh and credential save tests"
```

---

## Phase 3: Cache Service

### Task 5: Create cache.py — Local cache file management

**Files:**
- Create: `services/cache.py`
- Create: `tests/test_cache.py`

- [ ] **Step 1: Write failing cache tests**

Create `tests/test_cache.py`:

```python
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
```

Run: `pytest tests/test_cache.py::test_get_cache_path_returns_correct_path -v`

Expected: FAIL (module doesn't exist)

- [ ] **Step 2: Create cache.py**

```python
import os
import json
from typing import List
from services.models import EmailThread, EmailMessage


def get_cache_path():
    """Return the path to cached_emails.json"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cached_emails.json')


def is_cache_valid():
    """Check if cache file exists"""
    cache_path = get_cache_path()
    return os.path.exists(cache_path)


def load_cache() -> List[EmailThread]:
    """Load email threads from cache file"""
    cache_path = get_cache_path()
    
    if not os.path.exists(cache_path):
        return []
    
    try:
        with open(cache_path, 'r') as f:
            data = json.load(f)
        
        threads = []
        for thread_data in data:
            messages = [
                EmailMessage(
                    sender=msg['sender'],
                    recipient=msg['recipient'],
                    subject=msg['subject'],
                    body=msg['body'],
                    timestamp=msg['timestamp'],
                    importance_level=msg['importance_level'],
                    sentiment=msg['sentiment'],
                    is_reply=msg['is_reply']
                )
                for msg in thread_data['messages']
            ]
            
            thread = EmailThread(
                messages=messages,
                participants=thread_data['participants'],
                main_topic=thread_data['main_topic'],
                underlying_need=thread_data['underlying_need'],
                urgency=thread_data['urgency'],
                action_items=thread_data['action_items']
            )
            threads.append(thread)
        
        return threads
    except (json.JSONDecodeError, KeyError, ValueError):
        # Cache corrupted, return empty
        return []


def save_cache(threads: List[EmailThread]):
    """Save email threads to cache file"""
    cache_path = get_cache_path()
    
    data = []
    for thread in threads:
        thread_dict = {
            'messages': [
                {
                    'sender': msg.sender,
                    'recipient': msg.recipient,
                    'subject': msg.subject,
                    'body': msg.body,
                    'timestamp': msg.timestamp,
                    'importance_level': msg.importance_level,
                    'sentiment': msg.sentiment,
                    'is_reply': msg.is_reply
                }
                for msg in thread.messages
            ],
            'participants': thread.participants,
            'main_topic': thread.main_topic,
            'underlying_need': thread.underlying_need,
            'urgency': thread.urgency,
            'action_items': thread.action_items
        }
        data.append(thread_dict)
    
    with open(cache_path, 'w') as f:
        json.dump(data, f, indent=2)


def clear_cache():
    """Delete cache file"""
    cache_path = get_cache_path()
    if os.path.exists(cache_path):
        os.remove(cache_path)


def get_cache_metadata():
    """Get cache metadata (last modified, thread count)"""
    cache_path = get_cache_path()
    
    if not os.path.exists(cache_path):
        return {'exists': False, 'thread_count': 0}
    
    threads = load_cache()
    stat = os.stat(cache_path)
    
    return {
        'exists': True,
        'thread_count': len(threads),
        'last_modified': stat.st_mtime,
        'file_size_kb': stat.st_size / 1024
    }
```

- [ ] **Step 3: Run cache tests**

```bash
pytest tests/test_cache.py -v
```

Expected: 5 PASS

- [ ] **Step 4: Commit**

```bash
git add services/cache.py tests/test_cache.py
git commit -m "feat: add local cache service for email threads"
```

---

## Phase 4: Gmail Fetcher Service

### Task 6: Create gmail_fetcher.py — Gmail API calls and data mapping

**Files:**
- Create: `services/gmail_fetcher.py`
- Create: `tests/test_gmail_fetcher.py`

- [ ] **Step 1: Write failing tests for Gmail data mapping**

Create `tests/test_gmail_fetcher.py`:

```python
import pytest
from unittest.mock import MagicMock, patch
from services.gmail_fetcher import (
    map_gmail_message,
    group_messages_into_threads,
    fetch_all_emails
)


def test_map_gmail_message_extracts_basic_fields():
    """Test that map_gmail_message extracts sender, recipient, subject"""
    gmail_msg = {
        'id': 'msg123',
        'threadId': 'thread123',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'alice@example.com'},
                {'name': 'To', 'value': 'bob@example.com'},
                {'name': 'Subject', 'value': 'Meeting Notes'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 10:00:00 +0000'}
            ],
            'parts': [
                {'mimeType': 'text/plain', 'body': {'data': 'TWVldGluZyB3YXMgZ3JlYXQ='}}  # "Meeting was great" in base64
            ]
        },
        'labelIds': []
    }
    
    result = map_gmail_message(gmail_msg)
    
    assert result.sender == 'alice@example.com'
    assert result.recipient == 'bob@example.com'
    assert result.subject == 'Meeting Notes'


def test_map_gmail_message_detects_reply():
    """Test that map_gmail_message detects RE: prefix as reply"""
    gmail_msg = {
        'id': 'msg123',
        'threadId': 'thread123',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'alice@example.com'},
                {'name': 'To', 'value': 'bob@example.com'},
                {'name': 'Subject', 'value': 'RE: Meeting Notes'},
                {'name': 'Date', 'value': 'Mon, 1 Apr 2024 10:00:00 +0000'}
            ],
            'parts': [
                {'mimeType': 'text/plain', 'body': {'data': 'dGhhbmtz'}}  # "thanks" in base64
            ]
        },
        'labelIds': []
    }
    
    result = map_gmail_message(gmail_msg)
    assert result.is_reply is True


def test_group_messages_into_threads_groups_by_thread_id():
    """Test that messages are grouped by threadId"""
    msg1 = MagicMock()
    msg1.id = 'msg1'
    msg2 = MagicMock()
    msg2.id = 'msg2'
    
    gmail_threads_data = {
        'thread123': [msg1, msg2],
        'thread456': []
    }
    
    # This will be refined in implementation
    assert len(gmail_threads_data) == 2
```

Run: `pytest tests/test_gmail_fetcher.py::test_map_gmail_message_extracts_basic_fields -v`

Expected: FAIL (module doesn't exist)

- [ ] **Step 2: Create gmail_fetcher.py**

```python
import base64
import re
from typing import List, Dict
from datetime import datetime
from email.mime.text import MIMEText
import html2text
from googleapiclient.errors import HttpError

from services.models import EmailMessage, EmailThread
from services.gmail_auth import get_gmail_service
from services.qa_service import analyze_sentiment


def get_header_value(headers, header_name, default=''):
    """Extract header value from Gmail message headers"""
    for header in headers:
        if header['name'].lower() == header_name.lower():
            return header['value']
    return default


def decode_mime_message(part):
    """Decode base64-encoded MIME message part"""
    if 'data' not in part.get('body', {}):
        return ''
    
    try:
        data = part['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    except Exception:
        return ''


def extract_html_to_text(html_content):
    """Convert HTML email to plain text"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    
    try:
        return h.handle(html_content)
    except Exception:
        return html_content


def get_message_body(payload):
    """Extract plain text body from Gmail message payload"""
    if 'parts' in payload:
        # Multipart message
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            
            if mime_type == 'text/plain':
                return decode_mime_message(part)
            elif mime_type == 'text/html':
                html = decode_mime_message(part)
                return extract_html_to_text(html)
    
    # Single part message
    mime_type = payload.get('mimeType', '')
    if mime_type == 'text/plain':
        return decode_mime_message(payload)
    elif mime_type == 'text/html':
        html = decode_mime_message(payload)
        return extract_html_to_text(html)
    
    return ''


def get_importance_level(labels):
    """Determine importance level from Gmail labels"""
    for label in labels:
        if 'IMPORTANT' in label or 'STARRED' in label:
            return 'high'
    return 'normal'


def map_gmail_message(gmail_message: dict) -> EmailMessage:
    """
    Convert a Gmail API message to EmailMessage model.
    
    Args:
        gmail_message: Raw Gmail API message object
    
    Returns:
        EmailMessage instance
    """
    headers = gmail_message['payload'].get('headers', [])
    
    sender = get_header_value(headers, 'From')
    recipient = get_header_value(headers, 'To')
    subject = get_header_value(headers, 'Subject')
    date_str = get_header_value(headers, 'Date')
    
    # Parse date
    try:
        from email.utils import parsedate_to_datetime
        timestamp = parsedate_to_datetime(date_str).isoformat()
    except Exception:
        timestamp = datetime.now().isoformat()
    
    # Extract body
    body = get_message_body(gmail_message['payload'])
    
    # Detect if reply
    is_reply = subject.startswith('RE:') or subject.startswith('Fwd:')
    
    # Get importance
    labels = gmail_message.get('labelIds', [])
    importance_level = get_importance_level(labels)
    
    # Analyze sentiment (using existing OpenAI integration)
    sentiment = analyze_sentiment(body) if body else 'neutral'
    
    return EmailMessage(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        timestamp=timestamp,
        importance_level=importance_level,
        sentiment=sentiment,
        is_reply=is_reply
    )


def group_messages_by_thread(gmail_messages: List[dict]) -> Dict[str, List[dict]]:
    """Group Gmail messages by threadId"""
    threads = {}
    for msg in gmail_messages:
        thread_id = msg['threadId']
        if thread_id not in threads:
            threads[thread_id] = []
        threads[thread_id].append(msg)
    return threads


def create_email_thread(thread_id: str, gmail_messages: List[dict]) -> EmailThread:
    """
    Convert a group of Gmail messages into an EmailThread.
    
    Args:
        thread_id: Gmail thread ID
        gmail_messages: List of Gmail messages in the thread
    
    Returns:
        EmailThread instance
    """
    messages = [map_gmail_message(msg) for msg in gmail_messages]
    
    # Extract participants
    participants = set()
    for msg in messages:
        participants.add(msg.sender)
        participants.add(msg.recipient)
    participants.discard('')
    
    # Main topic is first message subject (without RE:)
    main_topic = messages[0].subject if messages else 'Unknown'
    main_topic = re.sub(r'^(RE:|FWD:)\s*', '', main_topic, flags=re.IGNORECASE)
    
    # Get urgency from importance levels
    importance_levels = [msg.importance_level for msg in messages]
    urgency = 'urgent' if 'high' in importance_levels else 'normal'
    
    return EmailThread(
        messages=messages,
        participants=sorted(list(participants)),
        main_topic=main_topic,
        underlying_need='',  # Will be filled by ContextAnalyzer
        urgency=urgency,
        action_items=[]  # Will be filled by ContextAnalyzer
    )


def fetch_all_emails(max_results=100) -> List[EmailThread]:
    """
    Fetch all emails from Gmail and return as EmailThread list.
    
    Args:
        max_results: Number of messages to fetch per API call (max 500)
    
    Returns:
        List of EmailThread objects
    """
    service = get_gmail_service()
    if not service:
        return []
    
    try:
        all_threads = []
        next_page_token = None
        
        while True:
            # Fetch page of messages
            results = service.users().messages().list(
                userId='me',
                maxResults=max_results,
                pageToken=next_page_token
            ).execute()
            
            message_ids = [msg['id'] for msg in results.get('messages', [])]
            
            if not message_ids:
                break
            
            # Get full message details
            gmail_messages = []
            for msg_id in message_ids:
                msg = service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'
                ).execute()
                gmail_messages.append(msg)
            
            # Group by thread
            threads_dict = group_messages_by_thread(gmail_messages)
            
            # Convert to EmailThread objects
            for thread_id, msgs in threads_dict.items():
                thread = create_email_thread(thread_id, msgs)
                all_threads.append(thread)
            
            # Check for next page
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break
        
        return all_threads
    
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
```

- [ ] **Step 3: Run fetcher tests**

```bash
pytest tests/test_gmail_fetcher.py -v
```

Expected: 3 PASS

- [ ] **Step 4: Commit**

```bash
git add services/gmail_fetcher.py tests/test_gmail_fetcher.py
git commit -m "feat: add Gmail API fetcher with data mapping"
```

---

## Phase 5: Main App Integration

### Task 7: Update app/main.py — Add Gmail auth UI and data source

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Add Gmail auth and cache imports at top**

In `app/main.py`, add after existing imports (around line 12):

```python
from services.gmail_auth import (  # noqa: E402
    is_authenticated,
    get_gmail_service,
    start_oauth_flow,
    logout
)
from services.gmail_fetcher import fetch_all_emails  # noqa: E402
from services.cache import load_cache, save_cache, is_cache_valid  # noqa: E402
```

- [ ] **Step 2: Add authentication state to session_state (around line 551)**

Find the section starting with `# Initialize context analyzer and load sample threads`. Add before that:

```python
# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = is_authenticated()

if 'email_threads' not in st.session_state:
    if st.session_state.authenticated and is_cache_valid():
        st.session_state.email_threads = load_cache()
    else:
        st.session_state.email_threads = []

if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
```

- [ ] **Step 3: Replace sample threads initialization (around line 551)**

Find and replace the section `# Initialize context analyzer and load sample threads` with:

```python
# Initialize context analyzer
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ContextAnalyzer()

# Load email threads (Gmail or mock fallback)
if 'sample_threads' not in st.session_state:
    if st.session_state.authenticated and st.session_state.email_threads:
        st.session_state.sample_threads = st.session_state.email_threads
    else:
        st.session_state.sample_threads = get_sample_threads()
```

- [ ] **Step 4: Add authentication UI in sidebar (around line 602-610)**

Find the section `with col_sidebar:` and add after the sidebar header and divider:

```python
    # Authentication Section
    if not st.session_state.authenticated:
        st.markdown('<div style="background-color: #FEF2F2; padding: 16px; border-radius: 8px; margin-bottom: 16px;">', unsafe_allow_html=True)
        st.markdown('**📧 Connect to Gmail**')
        st.markdown('Connect your Gmail account to analyze real emails.')
        
        if st.button("🔐 Authenticate with Gmail", use_container_width=True):
            st.info("Please ensure you have downloaded `client_secret.json` from Google Cloud Console OAuth credentials.")
            try:
                creds = start_oauth_flow()
                st.session_state.authenticated = True
                st.success("✅ Connected to Gmail!")
                st.rerun()
            except FileNotFoundError:
                st.error("❌ client_secret.json not found. Download from Google Cloud Console.")
            except Exception as e:
                st.error(f"❌ Authentication failed: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background-color: #ECFDF5; padding: 16px; border-radius: 8px; margin-bottom: 16px;">', unsafe_allow_html=True)
        st.markdown('✅ **Connected to Gmail**')
        
        col_refresh, col_logout = st.columns(2)
        with col_refresh:
            if st.button("🔄 Refresh Emails", use_container_width=True):
                with st.spinner("Fetching emails from Gmail..."):
                    threads = fetch_all_emails()
                    save_cache(threads)
                    st.session_state.email_threads = threads
                    st.session_state.sample_threads = threads
                    st.session_state.last_refresh = datetime.now().isoformat()
                    st.success(f"✅ Updated {len(threads)} threads")
                    st.rerun()
        
        with col_logout:
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.session_state.authenticated = False
                st.session_state.email_threads = []
                st.session_state.sample_threads = get_sample_threads()
                st.success("✅ Logged out")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
```

- [ ] **Step 5: Add import for datetime at top of file**

Add near top imports:

```python
from datetime import datetime
```

- [ ] **Step 6: Test the app locally**

```bash
streamlit run app/main.py
```

Expected:
- App shows "Connect to Gmail" button if not authenticated
- After authentication, shows "Connected to Gmail" with Refresh and Logout buttons
- No errors in terminal

- [ ] **Step 7: Commit**

```bash
git add app/main.py
git commit -m "feat: integrate Gmail auth and fetcher into main app"
```

---

### Task 8: Update sidebar settings — Replace mock data option

**Files:**
- Modify: `app/main.py`

- [ ] **Step 1: Update settings section in sidebar (around line 636-644)**

Find and replace the settings section with:

```python
    # Sidebar Divider
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Settings Section
    st.markdown('<div class="sidebar-settings">', unsafe_allow_html=True)
    st.markdown('<span class="settings-label">⚙️ Settings</span>', unsafe_allow_html=True)

    if primary_button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.session_state.authenticated:
        st.markdown('<small style="color: #9CA3AF;">Last refresh: ' + (st.session_state.last_refresh or 'Never') + '</small>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
```

- [ ] **Step 2: Test the app**

```bash
streamlit run app/main.py
```

Expected: Settings section shows refresh timestamp when authenticated

- [ ] **Step 3: Commit**

```bash
git add app/main.py
git commit -m "ui: update settings section with Gmail refresh info"
```

---

## Phase 6: End-to-End Testing

### Task 9: Manual integration test with real Gmail (local only)

**Files:**
- No code changes (manual test)

- [ ] **Step 1: Set up Google Cloud project**

Go to [console.cloud.google.com](https://console.cloud.google.com):
1. Create new project (e.g., "Gmail Email Assistant")
2. Enable Gmail API (search "Gmail API" in API Library)
3. Create OAuth 2.0 credentials (Desktop application)
4. Download as JSON → save as `client_secret.json` in project root

**Note:** `client_secret.json` is in .gitignore so won't be committed

- [ ] **Step 2: Run app and authenticate**

```bash
streamlit run app/main.py
```

1. Click "Authenticate with Gmail"
2. Browser opens, sign in with your Gmail account
3. Grant permission "View your email messages and settings"
4. Should redirect back and show success message

- [ ] **Step 3: Verify cache file created**

```bash
ls -lh cached_emails.json
```

Expected: File exists and contains JSON with email threads

- [ ] **Step 4: Test refresh button**

1. Click "Refresh Emails" in sidebar
2. Should show "Fetching emails from Gmail..."
3. After completion, should show "✅ Updated X threads"

- [ ] **Step 5: Test email analysis features**

1. Go to "💬 Conversational Q&A"
2. Ask a question (e.g., "What were the main topics discussed?")
3. Should get response analyzing real Gmail threads

- [ ] **Step 6: Test logout**

1. Click "🚪 Logout"
2. Should show "Connected to Gmail" button again
3. Cache still available on restart

- [ ] **Step 7: Verify no sensitive data in git**

```bash
git status
```

Expected: `credentials.json` and `cached_emails.json` not listed

```bash
git diff HEAD
```

Expected: No secret keys or tokens visible

---

### Task 10: Create documentation for Gmail setup

**Files:**
- Create: `GMAIL_SETUP.md`

- [ ] **Step 1: Create setup guide**

```markdown
# Gmail Setup Guide

## Prerequisites

- Google account with Gmail
- Google Cloud account

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Create Project"
3. Name: "Gmail Email Assistant" (or your preference)
4. Click "Create"

### 2. Enable Gmail API

1. In Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop application"
4. Click "Create"
5. Download the JSON file
6. Save as `client_secret.json` in the project root

### 4. Run the App

```bash
streamlit run app/main.py
```

1. Click "Authenticate with Gmail"
2. Sign in with your Google account
3. Grant permission for the app to read emails
4. App fetches and caches your emails

## File Locations

- `credentials.json` — OAuth tokens (auto-created, git-ignored)
- `cached_emails.json` — Cached email threads (git-ignored)
- `client_secret.json` — OAuth credentials from Google Cloud (git-ignored)

## Troubleshooting

**"client_secret.json not found"**
- Ensure you downloaded the credentials file from Google Cloud Console
- Place it in the project root directory

**"Permission denied"**
- Check that the Gmail API is enabled in Google Cloud Console
- Try logging out and re-authenticating

**"No emails found"**
- Check that your Gmail inbox has messages
- Try clicking "Refresh Emails"

## Security Notes

- Never commit `client_secret.json` or `credentials.json` to git
- Both files are in `.gitignore`
- Delete `credentials.json` before sharing the project
- OAuth tokens are automatically refreshed
```

- [ ] **Step 2: Commit**

```bash
git add GMAIL_SETUP.md
git commit -m "docs: add Gmail authentication setup guide"
```

---

## All tasks complete! ✅
