# Feature Specifications Document
## MailMind - Email Intelligence Platform

**Document Version:** 1.0  
**Last Updated:** April 13, 2026  
**Status:** MVP - Production Ready  

---

## Overview

This document provides detailed specifications for each feature in MailMind, including user workflows, acceptance criteria, edge cases, and technical requirements.

---

## Feature 1: Email Inbox & Thread Viewing

### 1.1 Feature Description
Users can view a list of emails in their inbox, click to view individual email threads, and navigate between emails. The inbox displays sender information, subject, preview text, timestamp, and unread indicators.

### 1.2 User Workflow

```
1. User loads application → Inbox automatically loads
2. Inbox displays 14 threads in sidebar
3. User reads sender, subject, snippet, timestamp
4. User clicks on a thread → Full conversation loads in main pane
5. User views all messages in thread
6. User can click different threads to switch between emails
7. User clicks back/home button to return to inbox
```

### 1.3 Component Specifications

#### Inbox List Component
**Container:** `.gmail-inbox`  
**Height:** 100% of left pane  
**Scrollable:** Yes (if threads exceed viewport)  

**Thread Row (per email):**
- **Layout:** Horizontal, 4 columns
- **Column 1 - Sender:** 80px wide, truncated with ellipsis
- **Column 2 - Subject:** Flex 1 (expands), font-weight: 600
- **Column 3 - Snippet:** Flex 2, gray text (120px max)
- **Column 4 - Timestamp:** 80px wide, right-aligned
- **Unread Indicator:** Blue dot (8px) next to sender if `is_unread: true`
- **Hover State:** Subtle background change (#F3F3F3)
- **Click State:** Selected state with blue left border

**Timestamp Format:**
- Same day: "2:30 PM"
- Same week: "Mon"
- Same year: "Mar 15"
- Different year: "Mar 15, 2025"

#### Thread View Component
**Container:** `.gmail-reading-pane`  
**Layout:** Vertical stack
**Width:** 100% (inbox width ~20%, reading pane ~50%, AI panel ~30%)

**Thread Header:**
- **Subject:** Large font (24px), bold, dark color
- **Sender Info:** "From: sender@example.com"
- **Timestamp:** Gray text
- **Actions Bar:** 
  - Toggle AI Panel button (✦) - right side, blue
  - Close/Back button - returns to inbox

**Message Container:**
- **Scrollable:** Yes (overflow-y: auto)
- **Per Message:**
  - Sender name in bold
  - Timestamp in gray
  - Message body with line breaks preserved
  - 10px padding around text
  - Light background (#FAFAFA) for visual separation
  - 10px margin between messages

### 1.4 Acceptance Criteria

#### UI/UX
- [ ] Inbox loads within 2 seconds
- [ ] All 14 threads display in inbox list
- [ ] Thread rows are visually distinct and clickable
- [ ] Unread indicator (blue dot) shows for first 5 threads
- [ ] Clicking thread loads full conversation without page reload
- [ ] Thread view shows all messages in chronological order
- [ ] Subject line is clearly visible in thread header
- [ ] Inbox and thread panes are independently scrollable
- [ ] Return to inbox button clearly visible and functional
- [ ] No visual glitches or layout shift on thread selection

#### Functionality
- [ ] GET /api/threads endpoint returns 14 threads
- [ ] Thread data includes: idx, sender, subject, snippet, timestamp, is_unread
- [ ] GET /api/thread/{idx} returns full thread with messages
- [ ] Messages include: sender, timestamp, body
- [ ] Invalid thread index (e.g., /api/thread/100) returns 404
- [ ] Clicking thread updates URL (optional: hash routing)
- [ ] Page refresh maintains current thread view
- [ ] Snippet text truncates at 80 characters with "..."

#### Performance
- [ ] Inbox list renders in < 500ms
- [ ] Thread load (from click to full display) < 1s
- [ ] Scrolling threads smooth (60fps)
- [ ] No memory leaks on rapid thread switching

#### Accessibility
- [ ] Thread rows are keyboard-navigable (arrow keys)
- [ ] Click events accessible via Enter key
- [ ] Screen reader announces sender, subject, timestamp
- [ ] Color contrast meets WCAG AA standards
- [ ] Focus states clearly visible

### 1.5 Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| **Empty thread (no messages)** | Display subject, show "No messages" placeholder |
| **Very long email body** | Scrollable within thread pane |
| **Very long subject line** | Wrap to 2-3 lines, full text visible on hover |
| **Rapid thread clicks** | Debounce API calls, show loading state |
| **Invalid thread index** | Return 404, display error message, return to inbox |
| **Network timeout** | Retry once, show error if timeout persists |
| **Very long snippet (>80 chars)** | Truncate with "..." |

---

## Feature 2: AI Assistant Panel - Ask

### 2.1 Feature Description
Users can ask contextual questions about email threads. The AI understands the thread's implicit needs, concerns, and context to provide actionable answers.

### 2.2 User Workflow

```
1. User opens an email thread
2. AI panel displays on right side
3. User clicks "💬 Ask" button
4. Input field appears with placeholder "Ask a question..."
5. User types question: "What's the main concern?"
6. User clicks "Send" or presses Enter
7. Loading indicator appears (spinner)
8. AI response displays below input
9. User can ask follow-up questions
10. Response can be copied or cleared
```

### 2.3 Component Specifications

#### Ask Input Component
**Container:** `.ai-ask-input`  
**Layout:** Horizontal (flex)

**Elements:**
- **Input Field:** 
  - Placeholder: "Ask a question..."
  - Min-height: 40px
  - Flex: 1 (expands)
  - Padding: 10px
  - Border: 1px solid #E0E0E0
  - Focus: Blue border, no outline
  - Border-radius: 4px

- **Send Button:**
  - Text: "Send" or icon (→)
  - Width: 50px
  - Background: #1A73E8 (blue)
  - Color: white
  - Hover: Darker blue (#1557B0)
  - Disabled: Gray (#CCCCCC) when input empty
  - Click: Submits question

#### Ask Response Component
**Container:** `.ai-ask-response`  
**Background:** #F6F8FC (light blue)  
**Padding:** 12px  
**Border-radius:** 4px  
**Margin-top:** 10px  

**Content:**
- **Response Text:** Left-aligned, full width
- **Markdown Support:** 
  - Bold: **text** → rendered bold
  - Bullet lists: - item → rendered as list
  - Line breaks: Preserved
- **Copy Button:** Top-right corner, gray icon
- **Clear Button:** Optional, removes response

#### Loading State
- **Spinner:** Animated circle (CSS keyframes)
- **Text:** "Analyzing thread..."
- **Duration:** Until API response arrives

### 2.4 Acceptance Criteria

#### UI/UX
- [ ] Ask button visible and accessible in AI panel
- [ ] Input field displays with placeholder text
- [ ] Send button enabled/disabled based on input
- [ ] Loading spinner displays during API call
- [ ] Response displays below input within 15 seconds
- [ ] Response is readable and well-formatted
- [ ] Multiple questions can be asked sequentially
- [ ] Previous responses remain visible
- [ ] Copy button copies response to clipboard
- [ ] Error messages are user-friendly

#### Functionality
- [ ] POST /api/ask endpoint called with thread_idx and question
- [ ] Response includes accurate answer based on thread
- [ ] Response addresses implicit concerns, not just facts
- [ ] Response is grounded in actual email content
- [ ] No hallucinations or made-up information
- [ ] Response length: 150-500 words typically
- [ ] Response references specific emails/participants
- [ ] Tone matches professional context

#### Edge Cases
- [ ] Empty question input → Send button disabled
- [ ] Very long question (500+ chars) → Accepted, processed
- [ ] Question about thread not related to emails → Graceful response
- [ ] Rapid-fire questions → Debounced, prevent race conditions
- [ ] Network timeout → Retry once, show error
- [ ] OpenAI API error → Show "Unable to answer, try again"

### 2.5 Example Questions & Answers

| Question | Expected Answer Focus |
|----------|----------------------|
| "What's the main topic?" | Subject matter, key discussion points |
| "What action do I need to take?" | Next steps, responsibilities, deadlines |
| "What are the implicit concerns?" | Worries, hesitations, unspoken needs |
| "Who are the key players?" | Participant roles, influence, relationships |
| "Is this urgent?" | Time sensitivity, impact, priority |
| "What's the underlying ask?" | Hidden request, real need vs. stated need |

---

## Feature 3: AI Assistant Panel - Draft

### 3.1 Feature Description
Users can generate professional email replies that match the tone and context of the email thread. The draft respects tone preferences and addresses underlying needs.

### 3.2 User Workflow

```
1. User opens email thread
2. User clicks "✏️ Draft" button
3. Tone selection dropdown appears
4. User selects tone: Professional | Collaborative | Assertive | Empathetic
5. Optional: User enters intent: "Provide solution and timeline"
6. User clicks "Generate" button
7. Loading state displays
8. Draft email appears in response area
9. User can copy, edit, or regenerate with different tone
10. User copies to email client to send
```

### 3.3 Component Specifications

#### Draft Controls Component
**Container:** `.ai-draft-controls`  

**Elements:**
- **Tone Selector:**
  - Type: Dropdown menu
  - Default: "Professional"
  - Options: Professional | Collaborative | Assertive | Empathetic
  - Icons: Optional emoji (👔 | 🤝 | 💪 | ❤️)

- **Intent Input (Optional):**
  - Placeholder: "What's your goal? (optional)"
  - Type: Text input
  - Flex: 1
  - Example: "Provide solution and timeline"

- **Generate Button:**
  - Text: "Generate Draft"
  - Background: #1A73E8
  - Color: White
  - Disabled state: Gray when tone not selected

#### Draft Response Component
**Container:** `.ai-draft-response`  
**Background:** White  
**Border:** 1px solid #E0E0E0  
**Padding:** 12px  
**Border-radius:** 4px  

**Content:**
- **Draft Email:** Full, formatted text
  - Greeting: "Dear [Name]" or "Hi [Name]"
  - Body: 3-5 paragraphs
  - Closing: "Best regards" or tone-appropriate closing
  - Signature: Generic (user adds personal)
  
- **Actions:**
  - Copy to clipboard button
  - Regenerate button (keeps tone, generates new version)
  - Edit in compose button (opens compose modal with draft)

#### Tone Descriptions
| Tone | Style | Use Case |
|------|-------|----------|
| **Professional** | Formal, business-appropriate, polished | Default, formal contexts |
| **Collaborative** | Team-focused, inclusive, receptive | Team discussions, brainstorms |
| **Assertive** | Confident, direct, action-oriented | Decision-making, commitments |
| **Empathetic** | Understanding, supportive, warm | Difficult conversations, feedback |

### 3.4 Acceptance Criteria

#### UI/UX
- [ ] Draft button visible in AI panel
- [ ] Tone dropdown clearly labeled
- [ ] All 4 tone options available
- [ ] Intent input field optional (not required)
- [ ] Generate button enabled when tone selected
- [ ] Loading spinner displays during generation
- [ ] Draft displays within 10 seconds
- [ ] Draft is complete and ready to send (minimal edits)
- [ ] Copy button successfully copies full draft
- [ ] Regenerate button creates new draft without page reload

#### Functionality
- [ ] POST /api/draft called with thread_idx, tone, intent
- [ ] Response includes complete email draft
- [ ] Draft starts with greeting (Dear/Hi)
- [ ] Draft ends with closing signature
- [ ] Draft tone matches selected preference
- [ ] Draft addresses thread's main issues
- [ ] Draft respects underlying needs, not just surface request
- [ ] Intent (if provided) reflected in response
- [ ] Draft length: 200-500 words typically

#### Tone Validation
- [ ] Professional: Formal language, proper grammar, "Dear"
- [ ] Collaborative: "we", "our", inclusive language
- [ ] Assertive: Direct statements, action items, confident tone
- [ ] Empathetic: Acknowledges feelings, supportive language

#### Edge Cases
- [ ] No tone selected → Generate button disabled
- [ ] Empty intent field → Draft still generated (uses thread context)
- [ ] Very long intent (500+ chars) → Processed, reflected in draft
- [ ] Rapid regenerate clicks → Debounced, prevent API spam
- [ ] Intent contradicts thread context → AI handles gracefully
- [ ] Network error → Show "Unable to generate, try again"

### 3.5 Example Scenarios

| Thread Context | Professional Tone | Empathetic Tone |
|---|---|---|
| **Delayed project** | "We need to discuss timeline and resources..." | "I understand this is challenging. Let's work together..." |
| **Feature request** | "After review, we can implement this in Q3..." | "Great suggestion! We see the value here and..." |
| **Conflict resolution** | "Let's schedule time to align on priorities..." | "I hear your concerns. Let's find a solution..." |

---

## Feature 4: AI Assistant Panel - Summarize

### 4.1 Feature Description
Users can generate comprehensive multi-perspective summaries of email threads, including surface facts, implicit needs, sentiment trajectory, action items, and concerns.

### 4.2 User Workflow

```
1. User opens email thread
2. User clicks "📊 Summarize" button
3. Loading indicator appears
4. Summary displays with multiple sections
5. User can copy summary or collapse/expand sections
6. User references summary in their own response
```

### 4.3 Component Specifications

#### Summarize Button
**Text:** "📊 Summarize"  
**Width:** 100%  
**Background:** #1A73E8  
**Color:** White  
**Padding:** 10px  
**Border-radius:** 4px  
**Hover:** Darker blue

#### Summary Response Component
**Container:** `.ai-summary-response`  
**Background:** #F6F8FC  
**Padding:** 12px  
**Border-radius:** 4px  
**Border-left:** 4px solid #1A73E8  

**Sections (in order):**

1. **Surface Facts**
   - **Header:** "📌 Surface Facts"
   - **Content:** Explicit statements, decisions made
   - **Format:** Bullet list
   
2. **Underlying Needs**
   - **Header:** "🎯 Underlying Needs"
   - **Content:** What's really being asked, implicit requests
   - **Format:** Bullet list with explanations
   
3. **Sentiment & Tone**
   - **Header:** "📈 Sentiment Arc"
   - **Content:** How tone changes across messages
   - **Format:** Narrative description
   - **Example:** "Started anxious → became problem-solving → ended optimistic"

4. **Action Items**
   - **Header:** "✅ Action Items"
   - **Content:** Explicit and implicit next steps
   - **Format:** Numbered list with deadlines if mentioned
   - **Example:** "1. Schedule Q1 budget review (by Apr 15)"

5. **Professional Context**
   - **Header:** "🏢 Context"
   - **Content:** Power dynamics, org hierarchy, political nuances
   - **Format:** Short narrative
   - **Example:** "VP is stakeholder, team leads implementation"

6. **Concerns & Hesitations**
   - **Header:** "⚠️ Concerns"
   - **Content:** Worries, blockers, unspoken objections
   - **Format:** Bullet list
   - **Example:** "• Budget constraints not yet addressed"

### 4.4 Acceptance Criteria

#### UI/UX
- [ ] Summarize button prominent and accessible
- [ ] Loading spinner displays during generation
- [ ] Summary displays within 10 seconds
- [ ] All 6 sections present and readable
- [ ] Headers clearly labeled with icons
- [ ] Content organized with bullet points/numbering
- [ ] Markdown formatting preserved (bold, lists)
- [ ] Copy button copies entire summary
- [ ] Sections can be collapsed/expanded (optional)
- [ ] Visual hierarchy clear (section headers darker/larger)

#### Functionality
- [ ] POST /api/summarize called with thread_idx
- [ ] Response includes all 6 sections
- [ ] Surface Facts: Only explicit, confirmed information
- [ ] Underlying Needs: Identifies hidden requests
- [ ] Sentiment Arc: Describes tone changes across messages
- [ ] Action Items: Lists tasks with deadlines
- [ ] Context: Explains org dynamics
- [ ] Concerns: Flags potential issues
- [ ] Summary is comprehensive (covers all key points)
- [ ] No information made up (grounded in email content)

#### Content Validation
- [ ] Surface Facts match email content exactly
- [ ] Underlying Needs: Inferences grounded in text
- [ ] Sentiment Arc: Accurate tone assessment
- [ ] Action Items: All explicit requests included
- [ ] Context: Accurate to email relationships
- [ ] Concerns: Real issues, not speculative

#### Edge Cases
- [ ] Single-message thread → Summary still generated
- [ ] Thread with no action items → "None identified" shown
- [ ] Ambiguous sentiment → Appropriately neutral description
- [ ] Conflicting statements → Both perspectives noted
- [ ] Network error → Show "Unable to summarize, try again"

### 4.5 Example Summary Structure

```
📌 **Surface Facts**
• Database performance degraded Monday night
• 15-minute downtime affecting 2,000+ users
• Rollback applied at 11:30 PM

🎯 **Underlying Needs**
• Wants root cause analysis to prevent recurrence
• Needs confidence in production stability
• Seeking process improvements

📈 **Sentiment Arc**
Started with alarm and urgency, shifted to problem-solving
mode after initial mitigation, and ended with cautious
optimism about the post-incident review process.

✅ **Action Items**
1. Complete root cause analysis (by Apr 15)
2. Schedule post-incident review (by Apr 20)
3. Implement monitoring improvements (by Apr 30)

🏢 **Context**
VP of Engineering is directly involved, indicating
executive-level concern. Database team owns implementation,
but impacts broader platform stability.

⚠️ **Concerns**
• Concern about repeating the issue
• Budget constraints for infrastructure improvements
• Team's confidence in stability measures
```

---

## Feature 5: Compose Modal

### 5.1 Feature Description
Users can draft new emails from scratch with AI assistance. The compose modal provides subject and body fields, along with full AI support (Draft, Ask, Refine).

### 5.2 User Workflow

```
1. User clicks "Compose" button in left sidebar
2. Modal opens with two panes
3. Left pane: Subject input, body textarea, Send/Cancel buttons
4. Right pane: AI assistant (Ask, Draft, Refine)
5. User types subject: "Q2 Status Update"
6. User clicks "Draft" → AI generates professional email
7. User reviews and optionally edits
8. User clicks "Send" → Email logged (MVP)
9. Modal closes, returns to inbox
```

### 5.3 Component Specifications

#### Modal Container
**Class:** `.compose-modal`  
**Display:** flex, when open  
**Position:** fixed, z-index: 200  
**Width:** 100vw, height: 100vh  
**Background:** Semi-transparent overlay (rgba)

#### Backdrop
**Class:** `.compose-backdrop`  
**Position:** absolute, full screen  
**Background:** rgba(0, 0, 0, 0.5)  
**Click:** Closes modal

#### Modal Content Container
**Class:** `.compose-container`  
**Width:** 90vw (max 1200px)  
**Height:** 90vh (max 800px)  
**Background:** White  
**Border-radius:** 8px  
**Box-shadow:** Material Design 3 elevation 4  
**Animation:** Fade-in over 200ms

#### Two-Pane Layout
**Container:** `.compose-panes`  
**Layout:** flex, row  
**Padding:** 20px

**Left Pane (Editor):** 70% width
- **Header:** "✏️ Compose Email"
- **Subject Input:**
  - Placeholder: "Email subject"
  - Padding: 10px
  - Border: 1px solid #E0E0E0
  - Font-size: 16px
  - Border-radius: 4px
  
- **Body Textarea:**
  - Placeholder: "Write your message..."
  - Padding: 10px
  - Border: 1px solid #E0E0E0
  - Height: flex 1 (expands)
  - Font-size: 14px
  - Font-family: monospace (optional)
  - Min-height: 300px
  
- **Action Buttons:**
  - Layout: flex, justify-content: space-between
  - "Send" button: Blue (#1A73E8), 100px wide
  - "Cancel" button: Gray (#F0F0F0), 100px wide
  - Both: 40px tall, 4px border-radius

**Right Pane (AI Panel):** 30% width
- **Header:** "🤖 AI Assistant"
- **Close Button:** "✕" in top-right
- **AI Controls:**
  - "✏️ Draft" button: Full width
  - "💬 Ask" button: Full width
  - "✨ Refine" button: Full width
- **Response Area:** Scrollable container below buttons

### 5.4 AI Features in Compose Mode

#### Draft (Generate from Subject)
**Trigger:** User clicks "Draft" button  
**Input:** Takes subject and current body text  
**Behavior:**
- If subject empty → Error: "Enter subject first"
- If subject filled → Generates complete email body
- Can be regenerated multiple times
- Replaces current body content

**Prompt Template:**
```
Write a professional email with subject: "{subject}"
The email should be well-structured, professional, and ready to send.
Keep it concise (200-400 words) unless body text suggests more detail.
```

#### Ask (Writing Question)
**Trigger:** User clicks "Ask" button  
**Input:** Question about writing (optional: email context)  
**Behavior:**
- Input field: "Ask a writing question..."
- Examples shown:
  - "Should this sound more urgent?"
  - "Is the tone appropriate?"
  - "Should I add more detail?"
- Response provides suggestions, not replacement text

**Prompt Template:**
```
User asked: "{question}"
Email context: "{email_body if provided}"
Provide concise writing advice (1-2 sentences).
```

#### Refine (Improve Text)
**Trigger:** User clicks "Refine" button  
**Input:** Refinement request (e.g., "Make it shorter")  
**Behavior:**
- Input field: "How would you like to refine this?"
- Examples shown:
  - "Make it more concise"
  - "Sound more professional"
  - "Add more urgency"
  - "Be more empathetic"
- Replaces body text with refined version

**Prompt Template:**
```
Current email: "{body_text}"
User request: "{refinement_request}"
Improve the email according to the request. Keep it professional.
Return only the refined email text, no explanations.
```

### 5.5 Acceptance Criteria

#### UI/UX
- [ ] Compose button in left sidebar is visible
- [ ] Clicking Compose opens modal with fade-in animation
- [ ] Modal centered on screen with proper sizing
- [ ] Subject input displays with focus state
- [ ] Body textarea is large and prominent (min 300px height)
- [ ] Send and Cancel buttons clearly visible
- [ ] Send button enabled when subject + body have text
- [ ] Cancel button visible and functional
- [ ] Backdrop click closes modal
- [ ] Modal closes after Send, returns to inbox
- [ ] AI panel on right side with all 3 buttons
- [ ] Close button (✕) in AI panel closes panel
- [ ] Two-pane layout responsive on smaller screens

#### Functionality
- [ ] POST /api/compose/draft called with topic
- [ ] Generated draft inserted into body textarea
- [ ] POST /api/compose/ask called with question
- [ ] Answer displays in AI response area
- [ ] POST /api/compose/refine called with refinement
- [ ] Refined text replaces body textarea
- [ ] Send button logs email (console.log in MVP)
- [ ] Modal state resets on close (fields cleared)
- [ ] Subject and body preserve input between AI calls
- [ ] Multiple AI requests possible in single compose session

#### Draft Generation
- [ ] Draft starts with greeting (Dear/Hi [generic])
- [ ] Draft includes body paragraphs
- [ ] Draft ends with professional closing
- [ ] Draft tone matches professional style
- [ ] Draft length appropriate for subject
- [ ] Draft is ready to send (minimal editing needed)

#### Edge Cases
- [ ] Subject empty, Draft clicked → Error message
- [ ] Subject entered, body empty, Send clicked → Error
- [ ] Subject and body filled, Send clicked → Success
- [ ] Rapid AI button clicks → Debounced
- [ ] Very long subject (200+ chars) → Accepted
- [ ] Very long body (5000+ words) → Accepted, scrollable
- [ ] Network timeout during Draft/Ask/Refine → Retry once
- [ ] Backdrop click while AI request pending → Cancel request

### 5.6 Example Workflows

| Workflow | Steps | Result |
|----------|-------|--------|
| **AI-Assisted** | 1. Type subject 2. Click Draft 3. Send | Full email generated and sent |
| **Manual Draft** | 1. Type subject 2. Type body 3. Send | Email sent as typed |
| **Refine & Send** | 1. Type subject 2. Type body 3. Click Refine 4. Send | Email improved and sent |
| **Interactive** | 1. Draft generated 2. Ask "More urgent?" 3. Refine "Make shorter" 4. Send | Iterative improvement |

---

## Feature 6: AI Panel Toggle & Close

### 6.1 Feature Description
Users can hide/show the AI panel to maximize email viewing space. The panel toggle persists while viewing the same email but resets when switching threads.

### 6.2 User Workflow

```
1. User opens email thread → AI panel visible by default
2. User clicks toggle button (✦) in email header → Panel hides
3. Email reading pane expands to fill space
4. User clicks toggle again → Panel reappears
5. User switches to different thread → Panel visible again (default)
6. User clicks close button (✕) in AI panel → Panel hides
```

### 6.3 Component Specifications

#### Toggle Button (✦)
**Location:** Top-right of email header  
**Icon:** ✦ (star/diamond symbol)  
**Position:** Absolute, right: 20px  
**Style:**
- Width: 40px
- Height: 40px
- Background: Transparent
- Border: None
- Color: #1A73E8 (blue)
- Font-size: 20px
- Cursor: pointer
- Hover: Opacity 0.7, lighter background
- Click: Toggles panel visibility

**States:**
- **Open:** ✦ (blue, visible)
- **Closed:** ✦ (gray, indicating panel hidden)

#### Close Button in AI Panel (✕)
**Location:** Top-right of AI panel header  
**Icon:** ✕ (X/close symbol)  
**Style:**
- Width: 30px
- Height: 30px
- Background: Transparent
- Border: None
- Color: #666
- Font-size: 18px
- Cursor: pointer
- Hover: Color #000

**Behavior:**
- Clicking closes/hides AI panel
- Same effect as toggle button
- Only visible when panel is open

#### Panel Visibility States

**Panel Open (Default):**
```
┌─────────────────────────────────────┐
│ Subject [✦]                         │
├──────────────┬──────────────────────┤
│              │ 🤖 Assistant    [✕]  │
│   Email      │                      │
│   Content    │ 💬 Ask               │
│   (60%)      │ ✏️ Draft             │
│              │ 📊 Summarize         │
│              │                      │
│              │ [Response Area]      │
└──────────────┴──────────────────────┘
```

**Panel Closed (Collapsed):**
```
┌──────────────────────────────────────┐
│ Subject [✦]                          │
├──────────────────────────────────────┤
│                                      │
│   Email Content (Full Width - 100%)  │
│                                      │
│                                      │
│                                      │
│                                      │
└──────────────────────────────────────┘
```

### 6.4 Acceptance Criteria

#### UI/UX
- [ ] Toggle button visible in email header (top-right)
- [ ] Toggle button clearly styled (blue, icon visible)
- [ ] Close button visible in AI panel header
- [ ] Clicking toggle hides panel smoothly
- [ ] Clicking toggle again shows panel smoothly
- [ ] Email pane expands when panel hidden
- [ ] Email pane contracts when panel shown
- [ ] No jank or layout shift during toggle
- [ ] Toggle state indicated visually (opacity change)
- [ ] Transitions smooth (0.3s animation)

#### Functionality
- [ ] Toggle button click hides panel (display: none)
- [ ] Toggle button click again shows panel (display: flex)
- [ ] Close button (✕) same effect as toggle
- [ ] Panel state persists while viewing same email
- [ ] Panel resets to open when switching threads
- [ ] Panel state doesn't affect other UI elements
- [ ] AI features still work in closed state (after reopening)

#### Performance
- [ ] Toggle animation smooth (60fps)
- [ ] No memory leaks on repeated toggles
- [ ] No layout thrashing on toggle

#### Accessibility
- [ ] Toggle button keyboard-accessible (Tab, Enter/Space)
- [ ] Close button keyboard-accessible
- [ ] Focus state clearly visible
- [ ] Screen reader announces button purpose

### 6.5 Implementation Details

**CSS Classes:**
```css
.ai-panel-toggle-btn { /* Toggle button */ }
.ai-panel-close-btn { /* Close button */ }
.gmail-assistant-panel.hidden { /* Hidden state */ }
.gmail-reading-pane.expanded { /* Expanded email pane */ }
```

**JavaScript State:**
```javascript
state.aiPanelOpen = true  // Current visibility
```

**Toggle Function:**
```javascript
function toggleAIPanel() {
  state.aiPanelOpen = !state.aiPanelOpen
  render()  // Re-render UI
}
```

---

## Appendix: Validation Rules

### Common Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| **Question Input** | Min 3 chars | "Question too short" |
| **Question Input** | Max 500 chars | "Question too long" |
| **Subject Input** | Min 1 char | "Subject required" |
| **Subject Input** | Max 200 chars | "Subject too long" |
| **Body Textarea** | Max 10,000 chars | "Email too long" |
| **Tone Selection** | Must be one of 4 options | "Invalid tone" |
| **Thread Index** | Must be 0-13 | "Invalid thread" |

### API Response Validation

All responses must include:
- **Success:** `{ key: value }` (no error field)
- **Error:** `{ error: "message" }` with appropriate HTTP status

---

**Document Approved By:** Product Team  
**Last Updated:** April 13, 2026  
**Next Review Date:** May 13, 2026  
**Contact:** development-team@company.com
