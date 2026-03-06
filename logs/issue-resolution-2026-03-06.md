# Issue Resolution Log — 2026-03-06

## Issue 1: Git Push Failed (Subagent Report)

**Problem**: Subagent reported "Git push failed (SSH key not configured)"

**Investigation**: Git remote is configured with HTTPS + Personal Access Token (PAT).

**Finding**: ✅ **Already configured correctly** — PAT-based auth works.

**Root cause**: Subagent didn't have full context about existing auth configuration.

**Resolution**: No action needed. Push works with current PAT config.

---

## Issue 2: AgentMail Not Configured

**Problem**: Subagent reported "Email system missing: AgentMail not installed"

**Investigation**:
- Scripts exist: `scripts/send_mail.py`, `scripts/read_mail.py`
- Created on Day 1 (2026-03-06)

**Finding**: ⚠️ **Scripts exist, but API key not configured**

**Required environment variables**:
- `AGENTMAIL_API_KEY`
- `AGENTMAIL_INBOX_ID`

**Resolution**: Lin needs to provide API credentials and add to `~/.bashrc`:
```bash
export AGENTMAIL_API_KEY="your-key-here"
export AGENTMAIL_INBOX_ID="your-inbox-id"
```

**Note**: Initial outreach (Aris, Shevlin) used Lin's personal email, not AgentMail. AgentMail (`explorer@agentmail.to`) is for receiving responses.

---

## Issue 3: Paper Access Blocked (reCAPTCHA)

**Problem**: Tononi & Koch 2024 (World Psychiatry) inaccessible.

**Sources attempted**:
| Source | Status |
|--------|--------|
| Wiley (official) | ❌ reCAPTCHA |
| PubMed Central | ❌ reCAPTCHA |
| ResearchGate | ❌ Access denied |
| Tononi Lab PDF | ⚠️ Binary PDF (text extraction failed) |

**Resolution options**:

1. **Use browser tool** — May bypass reCAPTCHA (slower, ~3-5 min)
2. **Find preprint** — Search arXiv / author website
3. **Use alternatives** — IIT 4.0 paper (Albantakis et al. 2023) + Wikipedia
4. **Manual download** — Lin downloads PDF, places in `/papers/`

**Recommended**: Option 3 (alternatives already sufficient) + Option 4 (if full text critical)

**Current coverage**:
- ✅ IIT core concepts (from Wikipedia + Tononi Lab)
- ✅ IIT 4.0 formalization (Albantakis et al. 2023)
- ✅ LLM application (Shin et al. 2025)
- ⚠️ Tononi & Koch 2024 specific updates (missing)

---

## Summary

| Issue | Status | Action |
|-------|--------|--------|
| Git push | ✅ Working (PAT configured) | None |
| AgentMail config | ⚠️ Need API key | Lin provides |
| Paper access | ⚠️ reCAPTCHA | Use alternatives or manual |

---

## Lesson: Subagent Context

**Problem**: Subagent lacked context about existing infrastructure.

**Solution**: Future subagent spawns should include:
1. Link to daily memory (`memory/YYYY-MM-DD.md`)
2. Infrastructure status summary
3. Known issues + workarounds

---

*Logged: 2026-03-06 16:10 UTC*
