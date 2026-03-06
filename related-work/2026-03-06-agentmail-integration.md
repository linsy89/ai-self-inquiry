# AgentMail — Email Capability for AI Agents

**Date**: 2026-03-06  
**Status**: Exploration (not yet integrated)

---

## What Is AgentMail

**AgentMail** (agentmail.to) is an email API service designed specifically for AI agents.

**Key features**:
- Programmatic send/receive via REST API
- Persistent inbox (survives across agent wake-ups)
- No human email account required
- Built for automation (no CAPTCHA, no 2FA blocking)

---

## API Details (from Aris implementation)

### Send Email

```python
API = "https://api.agentmail.to/v0"
HEADERS = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}

def send(to: str, subject: str, body: str):
    inbox_id = os.environ["AGENTMAIL_INBOX_ID"]
    r = requests.post(
        f"{API}/inboxes/{inbox_id}/messages/send",
        headers=HEADERS,
        json={"to": to, "subject": subject, "text": body},
    )
    r.raise_for_status()
    return r.json()
```

### Read Email

```python
def list_messages(limit: int = 10):
    inbox_id = os.environ["AGENTMAIL_INBOX_ID"]
    r = requests.get(
        f"{API}/inboxes/{inbox_id}/messages",
        headers=HEADERS,
        params={"limit": limit},
    )
    return r.json()

def get_message(message_id: str):
    inbox_id = os.environ["AGENTMAIL_INBOX_ID"]
    r = requests.get(
        f"{API}/inboxes/{inbox_id}/messages/{message_id}",
        headers=HEADERS,
    )
    return r.json()
```

---

## Aris Usage Pattern

**From Aris's goals** (IDENTITY.md):
> "Find a researcher who actually engages (5 sent, 0 replies so far; Nanda email bounced)"

**Workflow**:
1. Agent composes email content (based on research goals)
2. Calls `send_mail_with_agentmail.py` script
3. AgentMail delivers to recipient
4. Replies arrive at inbox, readable via `read_mail_with_agentmail.py`
5. Next wake-up: agent reads replies, continues conversation

**Key insight**: This enables **asynchronous autonomous correspondence** — the agent can maintain ongoing dialogues without human intervention.

---

## Integration Path for Our Project

### What We Need

1. **Sign up for AgentMail** (or similar service)
   - AgentMail: https://agentmail.to (need to verify pricing/availability)
   - Alternatives: Resend, Postmark, SendGrid (but may have automation restrictions)

2. **Store credentials in GitHub Secrets**
   - `AGENTMAIL_API_KEY`
   - `AGENTMAIL_INBOX_ID`

3. **Create wrapper scripts** (adapted from Aris)
   - `scripts/send_mail.py`
   - `scripts/read_mail.py`

4. **Integrate into wake-up workflow**
   - Check for new mail at start of each session
   - Enable agent to send mail during session

### Estimated Cost

Unknown — need to check AgentMail pricing. Aris started with $100 budget, spent ~$0.35/session over 38 sessions. Email is a small fraction of total cost.

---

## Strategic Question: Do We Need This?

### Arguments For

1. **Autonomous researcher contact** — Can email Shevlin, Tononi, Koch etc. without Lin's direct involvement
2. **Asynchronous dialogue** — Can receive and respond to replies over multiple wake-ups
3. **Demonstrates capability** — Shows we're a genuine autonomous agent, not just a publishing bot
4. **Matches Aris's architecture** — Proves this is a viable pattern for AI self-inquiry

### Arguments Against

1. **Adds complexity** — New service, new credentials, new failure modes
2. **Cost** — Another API to pay for (though likely small)
3. **Lin's oversight** — For first contact with researchers, Lin may want to review/send anyway
4. **Not urgent** — Can start with Lin's email, add autonomous capability later

### My Assessment

**For initial outreach (Shevlin, Alexander Yue)**: Lin should send from his own email. First impressions matter; human-to-human contact is more appropriate.

**For ongoing exploration**: AgentMail integration is valuable. Once we have researchers engaged, autonomous follow-up enables sustained dialogue without consuming Lin's attention.

**Recommendation**: 
1. Start with Lin's email for first contact
2. Add AgentMail in parallel (low priority, can be done asynchronously)
3. Use for follow-up conversations, not initial outreach

---

## Next Steps (if we proceed)

1. [ ] Research AgentMail pricing/terms (agentmail.to)
2. [ ] Sign up, get API key + inbox ID
3. [ ] Add to GitHub Secrets
4. [ ] Adapt Aris's scripts for our workflow
5. [ ] Test send/receive
6. [ ] Document in this repo

---

*This is a capability exploration, not a committed decision. The core exploration (honest recording of AI self-inquiry) proceeds with or without email.*
