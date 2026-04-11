# Gmail Integration Design Spec

**Date:** 2026-04-11  
**Status:** Approved for Implementation  
**Scope:** Add real Gmail authentication and email fetching to replace mock data

---

## Overview

Transform the Gmail Email Assistant from a mock-data demo into a fully functional tool that connects to real Gmail accounts. Users will authenticate once, have their emails cached locally, and analyze real email threads using the existing QA, summarization, and draft reply features.

---

## Requirements

### User Requirements
- Authenticate with Gmail via OAuth 2.0
- Fetch all emails from authenticated Gmail account
- Cache emails locally for fast app startup
- Manually refresh emails from Gmail on demand
- Select and analyze real email threads
- Existing features (Q&A, summarization, etc.) work unchanged

### Technical Requirements
- No credentials stored in git (all in .gitignore)
- Support HTML emails, attachments, and multiple recipients
- Map Gmail API data to existing `EmailThread`/`EmailMessage` models
- Handle API rate limits gracefully
- Preserve existing QA service and ContextAnalyzer integration

---

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────┐
│              Streamlit App (main.py)            │
│  ┌──────────────────────────────────────────┐   │
│  │  Auth UI: "Connect to Gmail" button      │   │
│  │  Thread selector (from cached data)      │   │
│  │  "Refresh" button (sidebar)              │   │
│  └──────────────────────────────────────────┘   │
└──────────┬──────────────────────┬───────────────┘
           │                      │
    ┌──────▼──────┐       ┌──────▼──────┐
    │  Cache      │       │  QA Service │
    │  Manager    │       │  Context    │
    │  (cache.py) │       │  Analyzer   │
    └──────┬──────┘       └──────┬──────┘
           │                      │
    ┌──────▼─────────────────────▼──────┐
    │   Gmail Integration Services       │
    │  ┌─────────────────────────────┐   │
    │  │  gmail_auth.py              │   │
    │  │  - OAuth flow               │   │
    │  │  - Token management         │   │
    │  │  - Credential storage       │   │
    │  └─────────────────────────────┘   │
    │  ┌─────────────────────────────┐   │
    │  │  gmail_fetcher.py           │   │
    │  │  - API calls                │   │
    │  │  - Data mapping             │   │
    │  │  - Thread grouping          │   │
    │  └─────────────────────────────┘   │
    └──────┬──────────────────────┬──────┘
           │                      │
    ┌──────▼──────┐       ┌──────▼────────────┐
    │ credentials │       │ cached_emails.json │
    │ .json       │       │ (local cache)      │
    │ (OAuth      │       │ (all threads)      │
    │ tokens)     │       │ (metadata)         │
    └─────────────┘       └────────────────────┘
                                  │
                          ┌───────▼────────┐
                          │ Gmail API      │
                          │ (Google Cloud) │
                          └────────────────┘
```

### New Services

#### `services/gmail_auth.py`
Handles OAuth 2.0 authentication flow and token lifecycle.

**Key functions:**
- `get_auth_url()` → Returns Google login URL
- `exchange_auth_code(code)` → Trades authorization code for tokens
- `get_gmail_service()` → Returns authenticated Gmail API client (auto-refreshes token)
- `is_authenticated()` → Checks if `credentials.json` exists and is valid
- `logout()` → Deletes `credentials.json`

**Token storage:**
- File: `credentials.json` (in .gitignore)
- Contains: `access_token`, `refresh_token`, `token_expiry`, `email`

#### `services/gmail_fetcher.py`
Fetches emails from Gmail API and maps to app's data models.

**Key functions:**
- `fetch_all_emails()` → Paginated fetch of all emails from Gmail inbox
- `fetch_recent_emails(since_timestamp)` → Incremental fetch for refresh
- `map_gmail_to_thread(gmail_messages)` → Converts raw Gmail API response to `EmailThread` object
- `map_gmail_message(gmail_message)` → Converts Gmail message to `EmailMessage` with sentiment analysis

**Data mapping:**
- Gmail `threadId` → `EmailThread` grouping key
- Gmail messages grouped by thread with sentiment analysis via OpenAI
- HTML emails converted to plain text via `html2text`
- Attachments stored as inline metadata "[Attachment: filename (size)]"
- Multiple recipients handled (CC/BCC preserved)

#### `services/cache.py`
Manages local email cache file.

**Key functions:**
- `load_cache()` → Reads `cached_emails.json`, returns list of `EmailThread`
- `save_cache(threads)` → Writes threads to `cached_emails.json`
- `is_cache_valid()` → Checks if cache file exists
- `get_cache_metadata()` → Returns last fetch timestamp and email count
- `clear_cache()` → Deletes cache file

---

## User Flow

### Initial Authentication
1. User opens app
2. App checks: `credentials.json` exists? No
3. Show: "Connect to Gmail" button
4. User clicks → Browser opens Google login page
5. User grants permission → Redirected back to app
6. App saves tokens to `credentials.json`
7. App shows: "Fetching your emails..." (progress indicator)
8. App fetches all emails via `gmail_fetcher.py` (paginated)
9. App saves to `cached_emails.json`
10. App loads email list, user selects thread to analyze

### Subsequent Sessions
1. User opens app
2. App checks: `credentials.json` exists? Yes
3. App loads cached emails from `cached_emails.json` (instant)
4. User sees email thread list
5. User can click "Refresh" button to fetch latest from Gmail

### Manual Refresh
1. User clicks "Refresh from Gmail" button (sidebar)
2. App fetches emails modified since last refresh timestamp
3. App merges with cached data
4. Shows: "Updated 5 new threads, 3 modified"

---

## Data Models

### EmailMessage (existing, used as-is)
```python
@dataclass
class EmailMessage:
    sender: str              # From header
    recipient: str           # First To recipient
    subject: str            # Subject header
    body: str               # Plain text + attachment info
    timestamp: str          # Date header (ISO 8601)
    importance_level: str   # "high", "normal", "low" (from Gmail flags/labels)
    sentiment: str          # "positive", "neutral", "negative" (via OpenAI)
    is_reply: bool          # Detected from "RE:" in subject
```

### EmailThread (existing, used as-is)
```python
@dataclass
class EmailThread:
    messages: List[EmailMessage]    # All messages in thread
    participants: List[str]         # Unique emails from To/From/CC
    main_topic: str                 # Subject line
    underlying_need: str            # Inferred via OpenAI
    urgency: str                    # "urgent", "normal", "low"
    action_items: List[str]         # Extracted via OpenAI
```

### Gmail → App Mapping
| EmailMessage Field | Gmail Source | Processing |
|---|---|---|
| `sender` | Message `From` header | Direct |
| `recipient` | Message `To` header | First recipient only |
| `subject` | Message `Subject` header | Direct |
| `body` | Message payload (plain + HTML) | HTML → plain text via `html2text`; append "[Attachment: ...]" for each file |
| `timestamp` | Message `internalDate` | Convert to ISO 8601 |
| `importance_level` | Gmail labels + flags | IMPORTANT label → "high", STARRED → "high", else "normal" |
| `sentiment` | Message body | Analyze via OpenAI (existing code) |
| `is_reply` | Subject line | `subject.startswith("RE:")` |

---

## Error Handling

### Authentication Errors
| Error | User Experience |
|---|---|
| Token expired | Auto-refresh in background; if fails, show "Re-authenticate" button |
| Invalid credentials | Show "Session expired, please reconnect to Gmail" with button |
| Network error during OAuth | Show error + "Retry" button |
| User denies Gmail permission | Show "Permission required to proceed" with retry option |

### Fetch Errors
| Error | User Experience |
|---|---|
| Gmail API quota exceeded | Show "Rate limited. Try again in 1 hour." |
| Network timeout | Show "Connection failed. Retry?" button |
| Empty inbox | Show "No emails found in your inbox" |
| Large inbox (10K+ emails) | Show progress bar, paginate in background |

### Data Errors
| Error | User Experience |
|---|---|
| Malformed email | Skip email, log error, continue |
| Missing required fields | Use default: sender="unknown", body="[Unable to parse]" |
| Email body > 10KB | Truncate to 10KB with "[... truncated]" |
| Corrupted cache file | Delete cache, prompt fresh fetch |

---

## Integration with Existing Features

### QA Service (`services/qa_service.py`)
- **No changes needed**
- Works with any `EmailThread` object (mock or real)
- Simply processes real Gmail threads instead of samples

### ContextAnalyzer (`services/context_analyzer.py`)
- **No changes needed**
- Same interface, analyzes real email threads

### Main App (`app/main.py`)
- **Replace mock data source:**
  - Old: `get_sample_threads()` from `services/mock_data.py`
  - New: `load_cache()` from `services/cache.py`
- **Add authentication UI:**
  - Show "Connect to Gmail" button if not authenticated
  - Add "Refresh from Gmail" button in settings section
- **Update state management:**
  - `st.session_state.authenticated` → bool
  - `st.session_state.email_threads` → from cache
  - `st.session_state.last_refresh` → timestamp

### requirements.txt
Add:
```
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.80.0
html2text>=2024.2.26
```

---

## Implementation Order

1. **Phase 1: Authentication** → `gmail_auth.py` (OAuth flow, token storage)
2. **Phase 2: Fetching** → `gmail_fetcher.py` (API calls, data mapping)
3. **Phase 3: Caching** → `cache.py` (cache file management)
4. **Phase 4: Integration** → Update `app/main.py` to use real data

---

## Assumptions & Constraints

**Assumptions:**
- User has a Gmail account
- User has permission to create a Google Cloud project
- Inbox fits in memory (reasonable for personal use)
- One user per local project instance

**Constraints:**
- Gmail API rate limits: 1,000 requests/second (more than sufficient)
- Cannot access shared mailboxes or delegated accounts (Gmail limitation)
- Token refresh happens automatically; user only re-authenticates if refresh fails
- Cache file grows with inbox size (no limit, assumes reasonable inbox <50K emails)

**Out of scope:**
- Multiple Gmail accounts
- Drafts, sent mail, or custom labels (only inbox)
- Email scheduling or sending
- Two-factor authentication edge cases (Gmail handles transparently)

---

## Success Criteria

✅ User can authenticate with Gmail via OAuth  
✅ All emails from inbox are fetched and cached  
✅ Cached emails load instantly on app restart  
✅ Manual "Refresh" button updates cache with new emails  
✅ Email threads are correctly grouped  
✅ Sentiment analysis works on real emails  
✅ QA, summarization, and draft reply features work unchanged  
✅ Credentials never committed to git  
✅ Graceful error handling for network/API issues  
✅ App runs locally without external dependencies (except Google API)

---

## Next Steps

- User reviews this spec
- Implement in phases (auth → fetch → cache → integrate)
- Test with real Gmail account
- Verify error handling with edge cases
