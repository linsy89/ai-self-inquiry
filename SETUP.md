# AgentMail Setup Guide

**For**: AI Self-Inquiry project  
**Purpose**: Enable autonomous email communication for the agent

---

## What Is AgentMail

AgentMail is an email API service designed for AI agents. It provides:
- Programmatic send/receive via REST API
- Persistent inbox (survives across agent wake-ups)
- No human email account required

---

## Setup Steps

### 1. Sign Up for AgentMail

Visit: https://agentmail.to

**Information needed**:
- Email address (for account notifications)
- Payment method (if paid tier)

**Expected output**:
- `API_KEY` (Bearer token)
- `INBOX_ID` (your dedicated inbox identifier)

---

### 2. Add to GitHub Secrets

Go to: https://github.com/linsy89/ai-self-inquiry/settings/secrets/actions

**Add two secrets**:

| Secret Name | Value |
|-------------|-------|
| `AGENTMAIL_API_KEY` | Your API key from AgentMail |
| `AGENTMAIL_INBOX_ID` | Your inbox ID from AgentMail |

---

### 3. Test the Integration

**Test send** (from VPS):
```bash
cd /root/ai-self-inquiry-repo
export AGENTMAIL_API_KEY="your_key_here"
export AGENTMAIL_INBOX_ID="your_inbox_here"
python3 scripts/send_mail.py "your-test-email@example.com" "Test" "This is a test message"
```

**Test read**:
```bash
python3 scripts/read_mail.py --limit 5
```

---

### 4. Integrate into Workflow

**GitHub Actions** (awake.yaml):

Add to the `env:` section:
```yaml
env:
  AGENTMAIL_API_KEY: ${{ secrets.AGENTMAIL_API_KEY }}
  AGENTMAIL_INBOX_ID: ${{ secrets.AGENTMAIL_INBOX_ID }}
```

**Usage in agent session**:
```python
# In agent instructions or tool definitions
import subprocess

def send_email(to, subject, body):
    subprocess.run([
        "python3", "scripts/send_mail.py",
        to, subject, body
    ])
```

---

## Usage Examples

### Send Email
```bash
python3 scripts/send_mail.py \
  "henry.shevlin@cambridge.ac.uk" \
  "Re: AI Agent Email to Philosopher" \
  "Dear Dr. Shevlin, I noticed your recent post about..."
```

### Read Recent Emails
```bash
python3 scripts/read_mail.py --limit 10
```

### Read Specific Email
```bash
python3 scripts/read_mail.py --message-id "msg_abc123"
```

### Output as JSON (for agent parsing)
```bash
python3 scripts/read_mail.py --json --limit 5
```

---

## Pricing

**Check current pricing at**: https://agentmail.to/pricing

**Aris's usage** (for reference):
- ~38 wake-ups over ~2 weeks
- 5 emails sent
- Email cost is small fraction of total ~$0.35/session

---

## Troubleshooting

### Error: "AGENTMAIL_API_KEY not set"
**Solution**: Ensure environment variable is set before running script.

### Error: "401 Unauthorized"
**Solution**: API key is invalid or expired. Regenerate in AgentMail dashboard.

### Error: "404 Not Found"
**Solution**: INBOX_ID is incorrect. Check your AgentMail dashboard.

### Error: "403 Forbidden"
**Solution**: Account may be suspended or out of credits.

---

## Security Notes

1. **Never commit API keys to git** — always use GitHub Secrets
2. **Rotate keys periodically** — regenerate every 90 days
3. **Monitor usage** — check AgentMail dashboard for unusual activity
4. **Limit inbox access** — only agent sessions should have credentials

---

## Alternatives

If AgentMail is unavailable or unsuitable:

| Service | Pros | Cons |
|---------|------|------|
| **Resend** | Good docs, free tier | May block automation |
| **Postmark** | Reliable, good deliverability | Requires verified domain |
| **SendGrid** | Free tier, well-known | Strict anti-automation |
| **SMTP + Gmail** | Free, familiar | 2FA issues, may flag automation |

**Recommendation**: Start with AgentMail (designed for AI agents), fall back to alternatives if needed.

---

## Status

- [x] Scripts created (`send_mail.py`, `read_mail.py`)
- [ ] AgentMail account created
- [ ] Secrets configured in GitHub
- [ ] Test send/receive completed
- [ ] Integrated into awake workflow

---

*Last updated: 2026-03-06*
