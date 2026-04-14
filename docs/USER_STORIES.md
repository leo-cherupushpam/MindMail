# User Stories & Acceptance Criteria
## MailMind - Email Intelligence Platform

**Document Version:** 1.0  
**Last Updated:** April 13, 2026  
**Status:** MVP - Production Ready  

---

## Overview

This document contains agile-formatted user stories with acceptance criteria, ready for implementation in Jira, Linear, or other tracking systems.

---

## Epic: Core Email Management

---

### Story US-01: View Email Inbox

**Type:** Story  
**Status:** Done  
**Priority:** P0 (Blocker)  
**Effort:** 3 points  

**As a** busy professional  
**I want to** see a list of my emails with sender, subject, and preview text  
**So that** I can quickly scan my inbox and understand what needs my attention

**Acceptance Criteria:**
- [ ] Inbox displays list of 14 email threads on left sidebar
- [ ] Each thread shows: sender name, subject, snippet (80 chars), timestamp
- [ ] Unread indicator (blue dot) appears on first 5 threads
- [ ] Clicking a thread loads the full conversation
- [ ] Inbox loads within 2 seconds on page load
- [ ] Threads are clickable with visual hover state
- [ ] List is scrollable if threads exceed viewport height
- [ ] API endpoint GET /api/threads returns proper format

**Acceptance Test Cases:**
```gherkin
Scenario: View inbox on page load
  Given user opens the application
  When the page loads
  Then the inbox displays all 14 threads
  And each thread shows sender, subject, and snippet
  And the page loads within 2 seconds

Scenario: Click thread to view details
  Given the inbox is displayed
  When the user clicks on a thread
  Then the full email conversation loads
  And the email pane updates with all messages
  And the AI panel loads for that thread

Scenario: Unread indicator displays
  Given the inbox is displayed
  When viewing the thread list
  Then the first 5 threads show an unread blue dot
  And other threads do not show the indicator
```

---

### Story US-02: View Email Thread

**Type:** Story  
**Status:** Done  
**Priority:** P0 (Blocker)  
**Effort:** 3 points  

**As a** user managing emails  
**I want to** click on an email and read the full conversation thread  
**So that** I can understand the complete context of the discussion

**Acceptance Criteria:**
- [ ] Clicking inbox thread loads full conversation in main pane
- [ ] Thread header displays subject line clearly
- [ ] All messages display in chronological order
- [ ] Each message shows sender name, timestamp, and body text
- [ ] Thread view is scrollable for long conversations
- [ ] Message body text displays with line breaks preserved
- [ ] No layout shift occurs when changing threads
- [ ] Back/Return button returns to inbox
- [ ] API endpoint GET /api/thread/{idx} returns complete thread

**Acceptance Test Cases:**
```gherkin
Scenario: Open thread from inbox
  Given the inbox is displayed
  When the user clicks on thread #5
  Then the reading pane loads the conversation
  And the subject displays in the header
  And all messages are visible in order

Scenario: Scroll long thread
  Given a long email thread (5+ messages) is open
  When the user scrolls in the reading pane
  Then the messages scroll smoothly
  And no content is cut off
  And the header remains fixed

Scenario: Switch between threads
  Given thread #1 is open
  When the user clicks on thread #3
  Then the reading pane updates to thread #3
  And the previous thread is no longer displayed
  And no layout shift occurs
```

---

## Epic: AI Assistant Features

---

### Story US-03: Ask Questions About Email

**Type:** Story  
**Status:** Done  
**Priority:** P0 (Blocker)  
**Effort:** 5 points  

**As a** busy professional  
**I want to** ask questions about an email thread and get AI-powered answers  
**So that** I can quickly understand context without reading everything

**Acceptance Criteria:**
- [ ] Ask button (💬) displays in AI panel when email is open
- [ ] Clicking Ask shows question input field
- [ ] User can type questions (e.g., "What's the main concern?")
- [ ] Send button or Enter key submits question
- [ ] Loading indicator displays while AI processes
- [ ] Response displays within 15 seconds
- [ ] Response is accurate and references thread content
- [ ] Response addresses implicit needs, not just facts
- [ ] Copy button allows copying response
- [ ] User can ask multiple follow-up questions
- [ ] API endpoint POST /api/ask returns answer

**Acceptance Test Cases:**
```gherkin
Scenario: Ask contextual question
  Given an email thread is open
  When the user clicks the Ask button
  And types "What action do I need to take?"
  And clicks Send
  Then a loading spinner displays
  And within 15 seconds the AI response appears
  And the response identifies specific action items

Scenario: Ask follow-up question
  Given a response is displayed
  When the user asks another question
  And submits it
  Then the new response appears below the previous one
  And both responses remain visible

Scenario: Handle empty input
  Given the Ask input field is visible
  When the user clicks Send without typing
  Then the Send button is disabled
  And no API call is made
```

---

### Story US-04: Generate Email Draft

**Type:** Story  
**Status:** Done  
**Priority:** P0 (Blocker)  
**Effort:** 5 points  

**As a** email manager  
**I want to** click a button and generate a professional email reply  
**So that** I can respond quickly with appropriate tone and context

**Acceptance Criteria:**
- [ ] Draft button (✏️) displays in AI panel
- [ ] Tone selector dropdown shows 4 options: Professional, Collaborative, Assertive, Empathetic
- [ ] User can optionally enter an intent (e.g., "Provide solution")
- [ ] Clicking Generate starts the draft generation
- [ ] Loading indicator displays while generating
- [ ] Draft appears within 10 seconds
- [ ] Draft is complete with greeting, body, and closing
- [ ] Draft tone matches selected option
- [ ] Draft can be copied to clipboard
- [ ] Copy button successfully copies full draft text
- [ ] User can regenerate with different tone
- [ ] API endpoint POST /api/draft returns draft

**Acceptance Test Cases:**
```gherkin
Scenario: Generate professional draft
  Given an email thread is open
  And Draft button is clicked
  When the user selects "Professional" tone
  And clicks Generate
  Then a loading spinner displays
  And within 10 seconds a draft email appears
  And the draft uses formal, business-appropriate language

Scenario: Generate collaborative draft
  Given a team discussion email
  When the user selects "Collaborative" tone
  And provides intent "Align team on approach"
  And clicks Generate
  Then the draft includes "we", "our", inclusive language

Scenario: Copy draft to clipboard
  Given a draft is displayed
  When the user clicks Copy
  Then the entire draft is copied
  And a success notification shows "Copied!"

Scenario: Regenerate with different tone
  Given a draft is displayed
  When the user changes tone to "Empathetic"
  And clicks Generate again
  Then a new draft appears
  And the new draft uses empathetic language
```

---

### Story US-05: Summarize Email Thread

**Type:** Story  
**Status:** Done  
**Priority:** P0 (Blocker)  
**Effort:** 5 points  

**As a** executive or manager  
**I want to** generate a comprehensive summary of an email thread  
**So that** I can quickly understand the key points, action items, and concerns

**Acceptance Criteria:**
- [ ] Summarize button (📊) displays in AI panel
- [ ] Clicking Summarize starts summary generation
- [ ] Loading indicator displays
- [ ] Summary appears within 10 seconds
- [ ] Summary includes 6 sections:
  - [ ] Surface Facts (explicit information)
  - [ ] Underlying Needs (implicit requests)
  - [ ] Sentiment Arc (tone changes)
  - [ ] Action Items (tasks and deadlines)
  - [ ] Professional Context (roles, dynamics)
  - [ ] Concerns (worries, blockers)
- [ ] Each section uses appropriate icons/formatting
- [ ] Content is organized with bullets or numbering
- [ ] Copy button copies entire summary
- [ ] Summary is grounded in email content (no hallucinations)
- [ ] API endpoint POST /api/summarize returns summary

**Acceptance Test Cases:**
```gherkin
Scenario: Generate summary of complex thread
  Given a 5-message email thread is open
  When the user clicks Summarize
  Then a loading spinner displays
  And within 10 seconds a formatted summary appears
  And the summary includes all 6 required sections

Scenario: Summary includes action items with deadlines
  Given a thread with action items and deadlines
  When the summary is generated
  Then the Action Items section lists:
  - Explicit tasks mentioned
  - Deadlines (if provided)
  - Owner (if mentioned)

Scenario: Summary identifies implicit concerns
  Given a thread with unspoken worries
  When the summary is generated
  Then the Concerns section identifies:
  - Budget worries
  - Timeline pressures
  - Resource constraints
  - Other implied hesitations

Scenario: Copy summary
  Given a summary is displayed
  When the user clicks Copy
  Then the entire summary is copied to clipboard
```

---

## Epic: Email Composition

---

### Story US-06: Compose New Email with Subject

**Type:** Story  
**Status:** Done  
**Priority:** P1 (High)  
**Effort:** 5 points  

**As a** user  
**I want to** click Compose and open a modal to write a new email  
**So that** I can draft new messages with AI assistance

**Acceptance Criteria:**
- [ ] Compose button displays in left sidebar
- [ ] Clicking Compose opens a modal dialog
- [ ] Modal has two panes: Editor (70%) and AI Panel (30%)
- [ ] Editor pane has subject input field
- [ ] Editor pane has body textarea (minimum 300px height)
- [ ] Subject input has placeholder "Email subject"
- [ ] Body textarea has placeholder "Write your message..."
- [ ] Send and Cancel buttons visible at bottom
- [ ] Send button is enabled when subject + body have text
- [ ] Cancel button closes modal
- [ ] Clicking backdrop closes modal
- [ ] Modal is centered on screen with proper sizing
- [ ] Modal has smooth fade-in animation

**Acceptance Test Cases:**
```gherkin
Scenario: Open compose modal
  Given the user is in the inbox
  When the user clicks the Compose button
  Then a modal appears centered on screen
  And the modal has subject and body input fields
  And the right pane shows AI assistant buttons

Scenario: Compose modal closes on cancel
  Given the compose modal is open
  When the user clicks Cancel
  Then the modal closes
  And the user returns to the inbox
  And form data is cleared

Scenario: Modal closes on backdrop click
  Given the compose modal is open
  When the user clicks the semi-transparent backdrop
  Then the modal closes
  And the inbox is displayed again
```

---

### Story US-07: Draft Email from Topic

**Type:** Story  
**Status:** Done  
**Priority:** P1 (High)  
**Effort:** 5 points  

**As a** user composing an email  
**I want to** click "Draft" and have AI generate a complete email from just a subject line  
**So that** I can quickly compose professional emails

**Acceptance Criteria:**
- [ ] Draft button (✏️) displays in compose AI panel
- [ ] Clicking Draft shows input for optional description
- [ ] User enters subject: "Q2 Status Update"
- [ ] Clicking Generate calls API with subject
- [ ] Loading indicator displays during generation
- [ ] Generated draft appears within 10 seconds
- [ ] Draft includes greeting, body paragraphs, and closing
- [ ] Draft tone is professional by default
- [ ] Draft text inserts into body textarea
- [ ] Draft can be edited or regenerated
- [ ] API endpoint POST /api/compose/draft returns draft

**Acceptance Test Cases:**
```gherkin
Scenario: Generate email from subject
  Given the compose modal is open
  And the subject is "Q2 Status Update"
  When the user clicks Draft
  Then a loading spinner displays
  And within 10 seconds a complete email appears in the body
  And the email starts with a greeting
  And the email ends with a professional closing

Scenario: Regenerate draft
  Given a generated draft is in the body
  When the user clicks Draft again
  Then a new draft is generated
  And it replaces the previous text
  And it has slightly different wording but same structure

Scenario: Empty subject
  Given the compose modal is open
  When the subject field is empty
  And the user clicks Draft
  Then an error message shows "Enter subject first"
  And no API call is made
```

---

### Story US-08: Get Writing Advice

**Type:** Story  
**Status:** Done  
**Priority:** P2 (Medium)  
**Effort:** 3 points  

**As a** user composing an email  
**I want to** ask the AI for writing advice  
**So that** I can improve my email before sending

**Acceptance Criteria:**
- [ ] Ask button (💬) displays in compose AI panel
- [ ] Clicking Ask shows question input
- [ ] User can ask questions like "Should this sound more urgent?"
- [ ] Optional: user can provide email body as context
- [ ] Clicking Send submits question
- [ ] Response displays within 10 seconds
- [ ] Response provides actionable writing suggestions
- [ ] Response is 1-3 sentences (concise)
- [ ] API endpoint POST /api/compose/ask returns answer

**Acceptance Test Cases:**
```gherkin
Scenario: Ask writing question
  Given the compose modal has body text
  When the user clicks Ask
  And types "Should this sound more urgent?"
  And clicks Send
  Then the AI provides specific writing suggestions
  And the response is concise (1-3 sentences)

Scenario: Ask without email context
  Given the compose modal is open
  When the user asks "How should I close this email?"
  Then the AI provides general advice
  And the response is helpful and specific
```

---

### Story US-09: Refine Email Text

**Type:** Story  
**Status:** Done  
**Priority:** P2 (Medium)  
**Effort:** 3 points  

**As a** user composing an email  
**I want to** ask AI to improve my email (make it shorter, more professional, etc.)  
**So that** I can refine the message before sending

**Acceptance Criteria:**
- [ ] Refine button (✨) displays in compose AI panel
- [ ] Clicking Refine shows input for refinement request
- [ ] User can enter requests like "Make it more concise"
- [ ] Refinement suggestions appear (Make shorter, More professional, etc.)
- [ ] Clicking Submit calls API with refinement request
- [ ] Loading indicator displays
- [ ] Refined text appears within 10 seconds
- [ ] Refined text replaces body textarea
- [ ] Refinement preserves the core message
- [ ] API endpoint POST /api/compose/refine returns refined text

**Acceptance Test Cases:**
```gherkin
Scenario: Make email more concise
  Given a draft email is in the body
  When the user clicks Refine
  And requests "Make it more concise"
  Then the refined version appears
  And the refined version is 30% shorter
  And the main message is preserved

Scenario: Make email more professional
  Given a casual draft is in the body
  When the user requests "Sound more professional"
  Then the refined version uses formal language
  And the tone is business-appropriate

Scenario: Empty body
  Given the body textarea is empty
  When the user clicks Refine
  Then an error shows "Add email text first"
```

---

### Story US-10: Send Composed Email

**Type:** Story  
**Status:** Done  
**Priority:** P1 (High)  
**Effort:** 2 points  

**As a** user  
**I want to** click Send to submit my composed email  
**So that** I can send the message (MVP: logs email, future: sends via Gmail)

**Acceptance Criteria:**
- [ ] Send button displays at bottom of compose modal
- [ ] Send button is enabled when subject + body have content
- [ ] Send button is disabled when fields are empty
- [ ] Clicking Send logs email to console (MVP)
- [ ] Success notification appears briefly
- [ ] Modal closes after Send
- [ ] Inbox is displayed after compose completes
- [ ] Form fields are cleared for next compose
- [ ] Subject and body are validated before sending

**Acceptance Test Cases:**
```gherkin
Scenario: Send email with subject and body
  Given the compose modal is open
  And subject is filled
  And body is filled
  When the user clicks Send
  Then the email is logged (MVP)
  Then a success message appears
  And the modal closes
  And the inbox is displayed

Scenario: Send button disabled when empty
  Given the compose modal is open
  When both subject and body are empty
  Then the Send button is disabled
  And it appears grayed out
```

---

## Epic: Interface Controls

---

### Story US-11: Toggle AI Panel Visibility

**Type:** Story  
**Status:** Done  
**Priority:** P2 (Medium)  
**Effort:** 3 points  

**As a** user reading emails  
**I want to** hide and show the AI panel to control screen space  
**So that** I can maximize the email reading area when needed

**Acceptance Criteria:**
- [ ] Toggle button (✦) displays in top-right of email header
- [ ] Toggle button is blue and visually prominent
- [ ] Clicking toggle hides the AI panel
- [ ] Email pane expands to fill available space
- [ ] Clicking toggle again shows the AI panel
- [ ] Panel reappears in original size
- [ ] Toggle state persists while viewing same email
- [ ] Toggle state resets to open when switching threads
- [ ] Animation is smooth (0.3s transition)
- [ ] No layout shift or jank during toggle

**Acceptance Test Cases:**
```gherkin
Scenario: Hide AI panel
  Given an email thread is open with AI panel visible
  When the user clicks the toggle button (✦)
  Then the AI panel hides smoothly
  And the email reading pane expands to full width
  And the toggle button remains visible

Scenario: Show AI panel again
  Given the AI panel is hidden
  When the user clicks the toggle button again
  Then the AI panel reappears
  And the email pane contracts to original size
  And AI features are accessible again

Scenario: Panel state resets on thread switch
  Given panel is hidden while viewing thread #1
  When the user clicks on thread #2
  Then the panel reappears by default
  And the panel is visible for the new thread
```

---

### Story US-12: Close AI Panel from Within

**Type:** Story  
**Status:** Done  
**Priority:** P2 (Medium)  
**Effort:** 2 points  

**As a** user  
**I want to** click a close button within the AI panel to hide it  
**So that** I have quick access to close the panel from within

**Acceptance Criteria:**
- [ ] Close button (✕) displays in top-right of AI panel header
- [ ] Close button is subtle (gray icon, not prominent)
- [ ] Clicking close button hides the AI panel
- [ ] Same effect as toggle button in email header
- [ ] Panel state reflects in toggle button
- [ ] Hovering close button changes color
- [ ] Close button only visible when panel is open

**Acceptance Test Cases:**
```gherkin
Scenario: Close AI panel from within
  Given the AI panel is open
  When the user clicks the close button (✕)
  Then the AI panel hides
  And the email pane expands
  And the toggle button (✦) shows visual change
```

---

## Definition of Done

For all stories, the following must be satisfied:

### Code Quality
- [ ] Code follows project style guide
- [ ] All functions have docstrings
- [ ] Type hints used for clarity
- [ ] No console errors or warnings
- [ ] No unused variables or imports

### Testing
- [ ] Acceptance criteria verified manually
- [ ] Happy path tested in browser
- [ ] Edge cases tested (empty input, timeouts, errors)
- [ ] No regression in other features

### Documentation
- [ ] Code changes documented in comments
- [ ] README updated if user-facing changes
- [ ] API endpoints documented if changed
- [ ] Features section updated if new feature

### Performance
- [ ] Load time within specification
- [ ] No memory leaks on repeated actions
- [ ] Animations smooth (60fps)
- [ ] No blocking operations

### Security
- [ ] User input sanitized (XSS protection)
- [ ] API keys not exposed in frontend
- [ ] No sensitive data in logs
- [ ] CORS properly configured (if applicable)

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Color contrast meets WCAG AA
- [ ] Screen reader compatible

---

## Story Point Estimation Guide

| Points | Complexity | Typical Effort |
|--------|-----------|---|
| **1** | Trivial | < 1 hour |
| **2** | Simple | 1-2 hours |
| **3** | Moderate | 2-4 hours |
| **5** | Complex | 4-8 hours |
| **8** | Very Complex | 8-16 hours |

---

## Appendix: Acceptance Criteria Templates

### API Endpoint Testing
```gherkin
Scenario: API endpoint returns success
  Given the API endpoint is called
  And valid input is provided
  When the request is submitted
  Then the API returns HTTP 200
  And the response contains expected fields
  And the response format is valid JSON

Scenario: API endpoint handles error
  Given the API endpoint is called
  And invalid input is provided
  When the request is submitted
  Then the API returns HTTP 400
  And the error response includes error message
```

### UI Component Testing
```gherkin
Scenario: Button is clickable
  Given the button is visible
  When the user clicks the button
  Then the expected action occurs
  And visual feedback is provided
  And the action is logged/tracked

Scenario: Input validation
  Given an input field is displayed
  When the user enters invalid data
  Then an error message displays
  And the form cannot be submitted
```

---

**Document Approved By:** Product & Engineering Teams  
**Last Updated:** April 13, 2026  
**Next Review Date:** May 13, 2026  
**Contact:** development-team@company.com
