#!/usr/bin/env python3
"""Send an email via AgentMail.

Usage:
    python scripts/send_mail.py <to> <subject> <body>

Example:
    python scripts/send_mail.py "researcher@example.com" "Hello" "Message body"

Requires environment variables:
    AGENTMAIL_API_KEY
    AGENTMAIL_INBOX_ID
"""
import argparse
import os
import sys
import requests

API = "https://api.agentmail.to/v0"

def get_headers():
    api_key = os.environ.get("AGENTMAIL_API_KEY")
    if not api_key:
        print("Error: AGENTMAIL_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

def send(to: str, subject: str, body: str) -> dict:
    """Send an email via AgentMail API."""
    inbox_id = os.environ.get("AGENTMAIL_INBOX_ID")
    if not inbox_id:
        print("Error: AGENTMAIL_INBOX_ID not set", file=sys.stderr)
        sys.exit(1)
    
    r = requests.post(
        f"{API}/inboxes/{inbox_id}/messages/send",
        headers=get_headers(),
        json={"to": to, "subject": subject, "text": body},
    )
    r.raise_for_status()
    result = r.json()
    print(f"✓ Sent message {result.get('message_id', 'unknown')} in thread {result.get('thread_id', 'unknown')}")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Send email via AgentMail")
    p.add_argument("to", help="Recipient email address")
    p.add_argument("subject", help="Email subject")
    p.add_argument("body", help="Email body text")
    args = p.parse_args()
    
    try:
        send(args.to, args.subject, args.body)
    except requests.exceptions.HTTPError as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
