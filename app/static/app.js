// ── State ─────────────────────────────────────────────────────────────────
const state = {
  view: 'inbox',          // 'inbox' | 'email'
  threads: [],            // cached from GET /api/threads
  selectedIdx: null,      // currently open thread index
  currentThread: null,    // data from GET /api/thread/{idx}
  activeFeature: null,    // 'ask' | 'draft' | 'summarize' | null
};

// ── Avatar helpers ─────────────────────────────────────────────────────────
const AVATAR_COLORS = [
  '#1A73E8','#34A853','#EA4335','#FBBC04',
  '#FF6D00','#9C27B0','#00ACC1','#F06292',
];

function avatarColor(name) {
  const ch = (name || '?').charCodeAt(0);
  return AVATAR_COLORS[ch % AVATAR_COLORS.length];
}

function avatarHtml(name, size = 40) {
  const initial = (name || '?')[0].toUpperCase();
  const color = avatarColor(name);
  return `<div class="gmail-avatar" style="width:${size}px;height:${size}px;background:${color};">${esc(initial)}</div>`;
}

// ── Timestamp formatting ───────────────────────────────────────────────────
function formatTs(ts) {
  if (!ts) return '';
  const dt = new Date(ts);
  const now = new Date();
  const diffDays = (now - dt) / 864e5;
  if (diffDays < 1) return dt.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  if (diffDays < 7) return dt.toLocaleDateString('en-US', { weekday: 'short' });
  return dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// ── XSS-safe escaping ──────────────────────────────────────────────────────
function esc(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ── Left nav ───────────────────────────────────────────────────────────────
function renderLeftNav() {
  document.getElementById('left-nav').innerHTML = `
    <button class="gmail-compose">✏️&nbsp;&nbsp;Compose</button>
    <div class="gmail-nav-item active">
      <span>📥 Inbox</span>
      <span class="gmail-nav-count">${state.threads.length || 14}</span>
    </div>
    <div class="gmail-nav-item"><span>⭐ Starred</span></div>
    <div class="gmail-nav-item"><span>🕐 Snoozed</span></div>
    <div class="gmail-nav-item"><span>📤 Sent</span></div>
    <div class="gmail-nav-item">
      <span>📝 Drafts</span><span class="gmail-nav-count">3</span>
    </div>
    <div class="gmail-nav-item">
      <span>🚫 Spam</span><span class="gmail-nav-count">12</span>
    </div>
    <div class="gmail-nav-item"><span>🗑️ Trash</span></div>
    <div class="gmail-nav-item"><span>▾ More</span></div>
    <div class="gmail-nav-section">LABELS</div>
    <div class="gmail-nav-item"><span>🏷️ Work</span></div>
  `;
}

// ── Inbox view ─────────────────────────────────────────────────────────────
async function loadInbox() {
  const res = await fetch('/api/threads');
  state.threads = await res.json();
  renderLeftNav();
  renderInbox();
}

function renderInbox() {
  state.view = 'inbox';
  state.activeFeature = null;
  document.getElementById('ai-panel').style.display = 'none';

  const rows = state.threads.map(t => {
    const sender = t.sender.split('@')[0].replace(/\./g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
    const rc = t.is_unread ? 'unread' : 'read';
    return `
      <div class="gmail-row ${rc}" data-idx="${t.idx}">
        <span style="color:#5F6368;flex-shrink:0;">☐</span>
        <span style="color:#5F6368;flex-shrink:0;">☆</span>
        <div class="gmail-row-sender ${rc}">${esc(sender)}</div>
        <div class="gmail-row-subject ${rc}">
          ${esc(t.subject)}
          <span class="gmail-row-snippet">&nbsp;– ${esc(t.snippet)}</span>
        </div>
        <div class="gmail-row-time ${rc}">${esc(formatTs(t.timestamp))}</div>
      </div>`;
  }).join('');

  document.getElementById('content-area').innerHTML = `
    <div class="gmail-tabs">
      <div class="gmail-tab active">📥 Primary</div>
      <div class="gmail-tab">🏷️ Promotions</div>
      <div class="gmail-tab">👥 Social</div>
    </div>
    <div>${rows}</div>`;

  document.querySelectorAll('.gmail-row').forEach(row => {
    row.addEventListener('click', () => openThread(Number(row.dataset.idx)));
  });
}

// ── Email (reading pane) view ──────────────────────────────────────────────
async function openThread(idx) {
  document.getElementById('content-area').innerHTML =
    '<div style="padding:32px;color:#5F6368;">Loading…</div>';

  const res = await fetch(`/api/thread/${idx}`);
  state.currentThread = await res.json();
  state.selectedIdx = idx;
  state.view = 'email';
  state.activeFeature = null;

  renderEmailView();
}

function renderEmailView() {
  const t = state.currentThread;

  const messages = t.messages.map(m => `
    <div class="gmail-message">
      <div class="gmail-message-header">
        ${avatarHtml(m.sender)}
        <div>
          <div class="gmail-sender-name">${esc(m.sender.split('@')[0].replace(/\./g,' ').replace(/\b\w/g, l=>l.toUpperCase()))}</div>
          <div class="gmail-sender-email">&lt;${esc(m.sender)}&gt;</div>
        </div>
        <div class="gmail-message-time">${esc(formatTs(m.timestamp))}</div>
      </div>
      <div class="gmail-message-body">${esc(m.body)}</div>
    </div>`).join('');

  document.getElementById('content-area').innerHTML = `
    <div class="gmail-reading-header">
      <button class="gmail-back-btn" id="back-btn">←</button>
      <div class="gmail-reading-subject">${esc(t.subject)}</div>
    </div>
    ${messages}
    <div class="gmail-reply-bar">
      <button class="gmail-reply-btn">↩ Reply</button>
      <button class="gmail-reply-btn">↪ Forward</button>
    </div>`;

  document.getElementById('back-btn').addEventListener('click', backToInbox);

  // Show AI panel
  const panel = document.getElementById('ai-panel');
  panel.style.display = 'flex';
  renderAIPanel();
}

function backToInbox() {
  renderInbox();
}

// ── AI panel ───────────────────────────────────────────────────────────────
function renderAIPanel() {
  document.getElementById('ai-panel').innerHTML = `
    <div class="ai-panel-header">✦ Gmail Assistant</div>
    <div class="ai-feature-btns">
      <button id="btn-ask" onclick="setFeature('ask')">💬 Ask</button>
      <button id="btn-draft" onclick="setFeature('draft')">✏️ Draft</button>
      <button id="btn-summarize" onclick="setFeature('summarize')">📊 Summarize</button>
    </div>
    <div class="ai-feature-area" id="ai-feature-area">
      <p style="color:#5F6368;font-size:13px;">Choose an action above.</p>
    </div>`;
}

function setFeature(feature) {
  state.activeFeature = feature;
  // Update active button style
  ['ask','draft','summarize'].forEach(f => {
    const btn = document.getElementById(`btn-${f}`);
    if (btn) btn.classList.toggle('active', f === feature);
  });

  const area = document.getElementById('ai-feature-area');

  if (feature === 'ask') {
    area.innerHTML = `
      <textarea id="ask-input" rows="3" placeholder="What action do I need to take?"></textarea>
      <button class="ai-submit-btn" onclick="submitAsk()">Ask →</button>
      <div id="ai-result"></div>`;

  } else if (feature === 'draft') {
    area.innerHTML = `
      <textarea id="draft-intent" rows="2" placeholder="e.g. Accept and propose a timeline (optional)"></textarea>
      <select id="draft-tone">
        <option value="professional">Professional</option>
        <option value="collaborative">Collaborative</option>
        <option value="assertive">Assertive</option>
        <option value="empathetic">Empathetic</option>
      </select>
      <button class="ai-submit-btn" onclick="submitDraft()">Generate Draft →</button>
      <div id="ai-result"></div>`;

  } else if (feature === 'summarize') {
    area.innerHTML = `
      <button class="ai-submit-btn" onclick="submitSummarize()">Summarize thread →</button>
      <div id="ai-result"></div>`;
  }
}

// ── AI API calls ───────────────────────────────────────────────────────────
function showLoading() {
  const el = document.getElementById('ai-result');
  if (el) el.innerHTML = '<div class="ai-loading">Thinking…</div>';
}

async function submitAsk() {
  const question = document.getElementById('ask-input').value.trim();
  if (!question) return;
  showLoading();
  const res = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ thread_idx: state.selectedIdx, question }),
  });
  const data = await res.json();
  document.getElementById('ai-result').innerHTML =
    `<div class="ai-output-card">${esc(data.answer)}</div>`;
}

async function submitDraft() {
  const intent = document.getElementById('draft-intent').value.trim();
  const tone = document.getElementById('draft-tone').value;
  showLoading();
  const res = await fetch('/api/draft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ thread_idx: state.selectedIdx, intent: intent || null, tone }),
  });
  const data = await res.json();
  document.getElementById('ai-result').innerHTML =
    `<div class="ai-output-card">${esc(data.draft)}</div>`;
}

async function submitSummarize() {
  showLoading();
  const res = await fetch('/api/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ thread_idx: state.selectedIdx }),
  });
  const data = await res.json();
  document.getElementById('ai-result').innerHTML =
    `<div class="ai-output-card">${esc(data.summary)}</div>`;
}

// ── Init ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', loadInbox);
