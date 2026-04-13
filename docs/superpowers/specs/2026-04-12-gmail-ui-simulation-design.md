# Design Spec: Gmail UI Simulation

**Date:** 2026-04-12
**Goal:** Redesign the Streamlit app to visually simulate Gmail — including inbox view, email reading pane, and an AI assistant sidebar — for portfolio showcase purposes.
**Timeline:** 1 week
**Audience:** Personal portfolio / showcase

---

## Overview

The current Streamlit app has a working AI backend (context analysis, drafting, summarization, Q&A) with a generic 3-column layout. This spec covers replacing the UI layer to simulate Gmail's look and feel, without touching any backend services.

The result is a convincing Gmail lookalike that demonstrates the concept of an AI copilot embedded inside Gmail, using mock data and the existing OpenAI-powered services.

---

## Two UI States

### State 1: Inbox View (default)

Shown on load and when no email is selected. Mimics Gmail's email list.

**Layout:**
```
┌─────────────┬──────────────────────────────────────┬──────┐
│  Left Nav   │  [Primary tab]                       │ Icons│
│             ├──────────────────────────────────────│      │
│  Compose    │ ☐ ★ Sender    Subject - Snippet  Time│  ✦   │
│             │ ☐ ★ Sender    Subject - Snippet  Time│      │
│  Inbox      │ ...                                  │  📅  │
│  Starred    │                                      │      │
│  Sent       │                                      │  👤  │
│  Drafts     │                                      │      │
│  Spam       │                                      │      │
└─────────────┴──────────────────────────────────────┴──────┘
```

**Email row anatomy:**
- Checkbox (static visual)
- Star icon (static visual)
- Sender name — bold + dark `#202124` if unread, normal + gray `#5F6368` if read
- Subject — bold if unread
- Snippet — gray `#5F6368`, truncated
- Timestamp — right-aligned, `12px`, gray
- Unread rows: white background
- Read rows: `#F6F8FC` background
- Hover: `#F2F6FC`

**Unread state:** Mock data has no `is_read` field. For demo purposes, the first 5 threads are treated as unread (bold, white background), the rest as read. This is hardcoded in the renderer — no model changes needed.

### State 2: Email Open View (email clicked)

Replaces the inbox list. Shows reading pane + expanded AI assistant panel.

**Layout:**
```
┌─────────────┬──────────────────────────┬─────────────────┐
│  Left Nav   │  ← Subject       Inbox   │  ✦ AI Assistant │
│             │                          │                 │
│  Compose    │  🔵 Sender Name          │  [Ask][Draft]   │
│             │     email@domain.com     │  [Summarize]    │
│  Inbox      │     timestamp            │                 │
│  Starred    │                          │  Output area    │
│  Sent       │  Email body...           │                 │
│  Drafts     │                          │                 │
│             │  [Reply] [Forward] 😊    │                 │
└─────────────┴──────────────────────────┴─────────────────┘
```

Clicking the back arrow (←) returns to State 1.

**Thread messages in reading pane:** All messages in the thread are shown stacked chronologically (like Gmail's expanded thread view), each with its own sender avatar, name, timestamp, and body. The most recent message is fully visible; earlier messages are shown in full as well (no collapse for MVP).

**Reply / Forward buttons:** Static visual only — rendered as HTML buttons with no action. They exist to complete the Gmail illusion.

---

## Visual Design

### Color Palette
| Element | Color |
|---|---|
| Page background | `#FFFFFF` |
| Left nav background | `#FFFFFF` |
| Email row hover | `#F2F6FC` |
| Selected/unread row | `#C2DBFF` |
| Read row background | `#F6F8FC` |
| Borders / dividers | `#E0E0E0` |
| Compose button bg | `#C2E7FF` |
| Compose button text | `#001D35` |
| Primary tab underline | `#1A73E8` |
| Body text | `#202124` |
| Secondary text | `#5F6368` |
| AI panel border | `#E0E0E0` left border |
| AI panel bg | `#FFFFFF` |
| AI output card bg | `#F8F9FA` |

### Typography
`font-family: Google Sans, Roboto, Arial, sans-serif`

| Element | Size | Weight |
|---|---|---|
| Sender (unread) | 14px | 700 |
| Sender (read) | 14px | 400 |
| Subject (unread) | 14px | 600 |
| Subject (read) | 14px | 400 |
| Snippet | 14px | 400 |
| Timestamp | 12px | 400 |
| Email body | 14px | 400 |

### Sender Avatars
Each sender gets a colored circle with their initial. Color is determined by the first character of the sender's name, cycling through Google's avatar palette:
```python
AVATAR_COLORS = [
  "#1A73E8",  # blue
  "#34A853",  # green
  "#EA4335",  # red
  "#FBBC04",  # yellow
  "#FF6D00",  # orange
  "#9C27B0",  # purple
  "#00ACC1",  # teal
  "#F06292",  # pink
]
color = AVATAR_COLORS[ord(sender[0].upper()) % len(AVATAR_COLORS)]
```

### AI Assistant Panel
Mimics a Gmail Add-on sidebar:
- Header: `✦ Gmail Assistant` in Google Sans, with subtle sparkle icon
- Feature buttons: outlined pill style → `[Ask]` `[Draft]` `[Summarize]`
- Output: card with `#F8F9FA` background, `1px solid #E0E0E0` border, `8px` radius
- Left border: `3px solid #E0E0E0` separating from reading pane

### Top Bar (static, visual only)
- Hamburger menu icon
- Gmail logo (text: `Gmail` in Google colors or just styled text)
- Search bar (static, non-functional pill shape)
- Right icons: ? ⚙ ✦ ⋮⋮⋮ Avatar circle

### Left Nav (static, visual only)
- Blue pill Compose button (`#C2E7FF`)
- Nav items: Inbox (with count), Starred, Snoozed, Sent, Drafts (count), Spam (count), More
- Labels section header
- Counts pulled from mock data length

### What We Are NOT Simulating
To keep scope within 1 week:
- Tabs (Promotions, Social, Updates) — Primary only, static
- Checkbox interactions (select/deselect emails)
- Star toggling
- Search functionality
- Pagination
- Email actions toolbar (archive, delete, mark as spam)
- Compose modal

---

## Data Flow

```
App load
  → get_sample_threads() → 14 mock EmailThread objects
  → ContextAnalyzer enriches all threads
  → State 1: render inbox list

User clicks email row
  → st.session_state.selected_thread_idx = idx
  → st.session_state.view = "email"
  → State 2: render reading pane + AI panel

User clicks ← back
  → st.session_state.view = "inbox"
  → State 1: render inbox list

User interacts with AI panel (Ask / Draft / Summarize)
  → QA service call (unchanged)
  → Result rendered in AI panel output card
```

---

## Files Changed

| File | Change |
|---|---|
| `app/main.py` | Full UI rewrite — layout, state switching, Gmail-style renderers |
| `services/ui_helpers.py` | Add: `render_email_row()`, `render_reading_pane()`, `render_avatar()`, `render_left_nav()`, `render_top_bar()` |

**No changes to:**
- `services/mock_data.py`
- `services/context_analyzer.py`
- `services/qa_service.py`
- `services/models.py`
- `services/cache.py`
- `services/gmail_auth.py`
- `services/gmail_fetcher.py`

---

## Session State

```python
st.session_state:
  view: "inbox" | "email"          # NEW — controls which state is shown
  selected_thread_idx: int          # existing
  email_threads: list               # existing
  sample_threads: list              # existing
  enriched_contexts: list           # existing
  selected_enriched_context: object # existing
  chat_history: list                # existing
  assistant_feature: str | None     # existing
  analyzer: ContextAnalyzer         # existing
```

---

## Success Criteria

- [ ] Inbox view matches Gmail's visual style closely enough that a viewer recognises it as Gmail
- [ ] Clicking an email transitions to reading pane view smoothly
- [ ] Back arrow returns to inbox
- [ ] AI panel (Ask, Draft, Summarize) works correctly in email view
- [ ] All 14 mock threads are visible and selectable
- [ ] No backend changes required — all AI features continue to work
- [ ] Runs locally with `streamlit run app/main.py`
- [ ] No new Python dependencies required
