# Gmail Email Assistant - UI Redesign Specification

**Date:** 2026-04-11  
**Status:** Approved for Implementation  
**Approach:** Custom HTML/CSS Grid Layout

---

## Overview

Transform the Gmail Email Assistant from a feature-selection app into a professional email client with an integrated AI assistant panel, inspired by Microsoft Outlook's Copilot sidebar experience.

The new layout uses a 3-column grid design:
- **Left (20%):** Gmail-style email list with thread previews
- **Center (55%):** Full email thread viewer
- **Right (25%):** Tabbed AI assistant sidebar (Ask, Summarize, Draft Reply)
- **Top (Full width, sticky):** Toolbar with account, search, and controls

---

## User Experience Goals

1. **Natural email reading** - Read emails like Gmail, not form-filling
2. **Context-aware AI** - Assistant automatically analyzes selected thread
3. **Professional appearance** - Looks like a real email client, not a prototype
4. **Efficient workflow** - Minimal clicks to get from email to analysis to action
5. **Mobile-responsive** (future) - Layout adapts but prioritizes desktop

---

## Detailed Design

### 1. Layout Structure (Custom CSS Grid)

**Page Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ HEADER TOOLBAR (sticky, full width)                     │
├─────────────┬──────────────────────┬──────────────────┤
│             │                      │                  │
│  EMAIL LIST │  EMAIL THREAD        │   ASSISTANT      │
│  (20%)      │  VIEWER (55%)        │   SIDEBAR (25%)  │
│             │                      │                  │
│             │                      │                  │
│  [scroll]   │  [scroll]            │   [scroll]       │
│             │                      │                  │
└─────────────┴──────────────────────┴──────────────────┘
```

**CSS Grid Implementation:**
- Use CSS Grid with 3-column layout: `1fr 2.75fr 1.25fr`
- Each column is a separate scrollable container
- Header is `grid-row: 1; grid-column: 1 / -1` (spans all columns)
- Proportions maintained: 20% | 55% | 25%

**Responsive behavior:**
- On smaller screens (future): columns may stack or hide left panel
- For current implementation: assume desktop viewport (1400px+)

---

### 2. Header Toolbar

**Structure:** Flexbox row with space-between alignment

**Left section:**
- Gmail Email Assistant logo + icon (📧)
- Search input field (placeholder: "Search threads...") with icon

**Center section:**
- (Empty, for visual balance)

**Right section:**
- Account info display (user's email address)
- Last refresh timestamp (e.g., "Refreshed: 2 min ago" or "Never")
- 🔄 Refresh Emails button (triggers fetch and list update)
- ⚙️ Settings dropdown menu with options:
  - View Settings
  - Logout
- 🚪 Quick logout button (optional, can be in dropdown)

**Styling:**
- Background: `--color-neutral-50` (light gray)
- Border-bottom: 1px solid `--color-neutral-200`
- Height: 60px
- Sticky positioning: `position: sticky; top: 0; z-index: 100`
- Padding: `--spacing-md` (16px)
- Typography: `--font-size-sm` (14px)

---

### 3. Left Column: Email List (20%)

**Container properties:**
- Width: 20% of viewport
- Background: `--color-neutral-100` (slightly darker gray)
- Overflow: `auto` (scrollable)
- Padding: `--spacing-md` (16px)
- Gap between items: `--spacing-sm` (8px)

**Email Thread Card (each item):**

```
┌──────────────────────────────┐
│ Sarah Chen                   │
│ Q1 Budget Approval - Sign... │
│ We've compiled the Q1 budg.. │
│ Apr 10, 2:30 PM              │
└──────────────────────────────┘
```

**Card Content:**
- Line 1: Sender name - **bold**, `--font-weight-bold`, `--font-size-base`
- Line 2: Subject line - `--font-weight-semibold`, truncate at 2 lines
- Line 3: Preview text - `--color-neutral-600`, truncate at 2 lines, `--font-size-sm`
- Line 4: Timestamp - `--color-neutral-400`, `--font-size-xs`

**Card Styling:**
- Background: white
- Border: 1px solid `--color-neutral-200`
- Border-radius: `--border-radius-md` (8px)
- Padding: `--spacing-md` (16px)
- Margin-bottom: `--spacing-sm` (8px)
- Cursor: pointer
- Transition: all 150ms ease
- Hover: box-shadow `--shadow-md`, background slightly lighter
- **Selected state:** border-left 4px solid `--color-primary`, background `--color-primary-light`

**List behavior:**
- Show latest 20 threads (from fetch_all_emails)
- Sorted newest to oldest
- Click to select → triggers center and right updates
- No drag/reorder for now

---

### 4. Center Column: Email Thread Viewer (55%)

**Container properties:**
- Width: 55% of viewport
- Background: white
- Overflow: `auto` (scrollable)
- Padding: `--spacing-lg` (24px)
- Border-left/right: 1px solid `--color-neutral-200`

**Thread Header (sticky within column):**
- Subject line: `--font-size-xl`, `--font-weight-bold`
- Metadata: "{N} messages from {date_range}"
- Participants: "From: alice@..., bob@..., ..."
- Divider line below header

**Message Container (repeats for each message):**

```
Sarah Chen <sarah@company.com>
Apr 10, 2:30 PM

[Full message body text wrapping naturally]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Per-message layout:**
- Sender name: `--font-weight-bold`, `--font-size-base`
- Sender email: `--color-neutral-600`, `--font-size-sm`
- Timestamp: `--color-neutral-400`, `--font-size-sm`
- Message body: `--font-size-base`, `--line-height-relaxed`, left-aligned
- Divider: light gray line, margin `--spacing-lg` top/bottom

**Message styling:**
- Padding: `--spacing-lg` (24px) bottom
- Margin: `--spacing-md` (16px) between messages
- Text wrapping: word-break, handle long emails/URLs

**Scroll behavior:**
- Internal scroll (doesn't affect sidebar)
- Messages chronological: oldest at top, newest at bottom

---

### 5. Right Column: Assistant Sidebar (25%)

**Container properties:**
- Width: 25% of viewport
- Background: `--color-neutral-50` (light gray, slightly different from list)
- Overflow: hidden (tabs + content handle scroll internally)
- Padding: `--spacing-md` (16px)
- Border-left: 1px solid `--color-neutral-200`

**Thread Context Indicator (top):**
```
📧 Analyzing: Q1 Budget Approval
```
- Small badge-style display
- Sender + subject preview
- `--font-size-sm`, `--color-neutral-600`
- Updates automatically when thread is selected

**Tab Interface:**

Three tabs:
1. **💬 Ask** - Q&A about the thread
2. **📝 Summarize** - Summary/synthesis of thread
3. **✉️ Draft** - Generate reply draft

**Tab styling:**
- Tab bar: flex row, gap `--spacing-md`
- Each tab: padding `--spacing-md`, border-bottom 2px
- Active tab: border-color `--color-primary`, text bold
- Inactive tabs: border-color transparent, cursor pointer
- Transition: 150ms

**Tab Content Areas (one visible at a time):**

**Ask Tab:**
- Input field: textarea, placeholder "Ask about this email thread..."
- Submit button: "Ask"
- Response area: display AI response, scrollable
- Chat history: list of previous Q&A exchanges (scrollable)
- Styling: white background cards for each exchange

**Summarize Tab:**
- Action button: "Generate Summary"
- Response area: display summary text, scrollable
- Copy button to copy summary

**Draft Tab:**
- Intent input: textarea, placeholder "What do you want to say? (e.g., 'Approve the budget')"
- Tone selector: dropdown (Professional, Collaborative, Assertive, Empathetic)
- Submit button: "Generate Draft"
- Response area: display draft reply, scrollable
- Copy/edit options

**Common styling for all tabs:**
- Input fields: standard form styling
- Buttons: `--color-primary` background, white text
- Response text: `--font-size-sm`, `--line-height-relaxed`
- Scrollable content area: max-height with internal scroll

---

### 6. Color Palette & Tokens

**Existing design tokens (reused):**
```
Primary: #2563EB
Primary Dark: #1D4ED8
Primary Light: #DBEAFE

Success: #10B981
Warning: #F59E0B
Error: #EF4444

Neutral 50: #F9FAFB
Neutral 100: #F3F4F6
Neutral 200: #E5E7EB
Neutral 400: #9CA3AF
Neutral 600: #4B5563
Neutral 900: #111827
```

**Usage in new layout:**
- Headers: `--color-neutral-900`
- Backgrounds: `--color-neutral-50` or `--color-neutral-100`
- Borders: `--color-neutral-200`
- Secondary text: `--color-neutral-600`
- Interactive elements: `--color-primary`
- Hover/active: `--color-primary-light` backgrounds

---

### 7. User Interactions & Flows

**Primary workflow:**
1. User opens app → authenticated? No → login flow
2. If authenticated:
   - Header loads
   - Email list loads with 20 latest threads
   - First thread auto-selected
   - Center column displays that thread
   - Right sidebar shows "Analyzing: [subject]"
   - Ask tab is default active
3. User reads thread in center
4. User asks question in sidebar → response appears
5. User clicks different thread → center/right auto-update
6. User can switch tabs (Ask → Summarize → Draft) anytime

**Search flow:**
- User types in header search
- Email list filters in real-time (sender or subject match)
- Selection clears (or maintains if it matches filter)

**Refresh flow:**
- User clicks "Refresh Emails" button
- Spinner shows in button
- Fetches latest 20 from Gmail
- Updates list, resets selection to first
- Timestamp updates in header

**Logout flow:**
- User clicks settings → logout
- Session clears
- Redirects to login screen

---

### 8. State Management

**Session state variables:**
```python
st.session_state.authenticated: bool          # Is user logged in?
st.session_state.email_threads: List[EmailThread]  # Cached threads
st.session_state.selected_thread_idx: int     # Currently selected thread (0-indexed)
st.session_state.assistant_tab: str           # "ask", "summarize", or "draft"
st.session_state.chat_history: List[dict]     # Q&A exchanges for Ask tab
st.session_state.search_query: str            # Email list search filter
st.session_state.last_refresh: str            # Timestamp of last refresh
```

**When thread is selected:**
- `selected_thread_idx` updates
- Center column re-renders with that thread
- Right sidebar analyzes that thread (context updates)
- Chat history clears (new thread = fresh conversation)

**When tab is switched:**
- `assistant_tab` updates
- Right sidebar content changes to show Ask/Summarize/Draft

---

### 9. Technical Implementation Strategy

**File changes:**
- `app/main.py` - Complete redesign of layout (major refactor)
- `services/email_renderer.py` (new) - Helper functions to render email threads as HTML
- CSS in `st.markdown()` blocks - Grid layout, component styling

**Key technical decisions:**
- Use HTML/CSS grid via `st.markdown()` with custom `<div>` structures
- Separate containers for left/center/right using div styling
- Thread selection via Streamlit button interactions in left column
- Assistant responses in right column via `st.write()` / `st.markdown()`
- State management via `st.session_state` (already in use)

**Component hierarchy:**
```
app/main.py
├── Header Toolbar (HTML div + buttons)
├── 3-Column Grid (HTML div)
│   ├── Left: Email List (loop through email_threads, render cards)
│   ├── Center: Thread Viewer (render selected thread as linear messages)
│   └── Right: Assistant Sidebar (tabbed interface with forms)
```

---

### 10. Edge Cases & Error Handling

**No emails:**
- Email list shows: "No emails found. Click 'Refresh Emails' to get started."

**No thread selected:**
- Center shows: "Select an email thread to view"
- Right sidebar disabled until thread selected

**API errors:**
- Refresh fails: "Error fetching emails. Try again?"
- Q&A fails: "Failed to generate response. Try again?"

**Performance:**
- Max 20 threads displayed (limit from fetch_all_emails)
- Lazy rendering in list (no pre-loading all previews)

---

## Success Criteria

✅ 3-column layout displays correctly (20/55/25 split)  
✅ Email list shows 20 threads with Gmail-style previews  
✅ Click thread → center and right update automatically  
✅ Thread displays as linear conversation  
✅ Assistant tabs (Ask/Summarize/Draft) all functional  
✅ Header toolbar fully operational  
✅ Professional appearance matching design system  
✅ Responsive scrolling (columns scroll independently)  
✅ State management works seamlessly  
✅ All features (Q&A, summarization, drafts) work with selected thread  

---

## Next Steps

1. User reviews and approves this spec
2. Implementation plan created
3. Build in phases:
   - Phase 1: Layout structure (grid, columns)
   - Phase 2: Email list rendering
   - Phase 3: Thread viewer
   - Phase 4: Assistant sidebar
   - Phase 5: Styling and polish
