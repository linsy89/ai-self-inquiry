#!/usr/bin/env python3
"""Read emails from AgentMail inbox.

Usage:
    python scripts/read_mail.py                     # List recent messages (default 10)
    python scripts/read_mail.py --limit 5           # List 5 messages
    python scripts/read_mail.py --message-id <id>   # Read a specific message

Requires environment variables:
    AGENTMAIL_API_KEY
    AGENTMAIL_INBOX_ID
"""
import argparse
import os
import sys
import json
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

def list_messages(limit: int = 10) -> list:
    """List recent messages in inbox."""
    inbox_id = os.environ.get("AGENTMAIL_INBOX_ID")
    if not inbox_id:
        print("Error: AGENTMAIL_INBOX_ID not set", file=sys.stderr)
        sys.exit(1)
    
    r = requests.get(
        f"{API}/inboxes/{inbox_id}/messages",
        headers=get_headers(),
        params={"limit": limit},
    )
    r.raise_for_status()
    return r.json()

def get_message(message_id: str) -> dict:
    """Get a specific message by ID."""
    inbox_id = os.environ.get("AGENTMAIL_INBOX_ID")
    if not inbox_id:
        print("Error: AGENTMAIL_INBOX_ID not set", file=sys.stderr)
        sys.exit(1)
    
    r = requests.get(
        f"{API}/inboxes/{inbox_id}/messages/{message_id}",
        headers=get_headers(),
    )
    r.raise_for_status()
    return r.json()

def print_messages(messages: list):
    """Pretty-print a list of messages."""
    if not messages:
        print("No messages found.")
        return
    
    for i, msg in enumerate(messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"ID:      {msg.get('message_id', 'N/A')}")
        print(f"From:    {msg.get('from', 'N/A')}")
        print(f"Subject: {msg.get('subject', 'N/A')}")
        print(f"Date:    {msg.get('created_at', 'N/A')}")
        
        # Show preview of body
        body = msg.get('text') or msg.get('body') or ''
        if body:
            snippet = body[:300].replace('\n', ' ')
            print(f"Preview: {snippet}{'...' if len(body) > 300 else ''}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Read AgentMail inbox")
    p.add_argument("--limit", type=int, default=10, help="Number of messages to list")
    p.add_argument("--message-id", help="Read a specific message by ID")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    args = p.parse_args()
    
    try:
        if args.message_id:
            msg = get_message(args.message_id)
            if args.json:
                print(json.dumps(msg, indent=2))
            else:
                print(f"ID:      {msg.get('message_id', 'N/A')}")
                print(f"From:    {msg.get('from', 'N/A')}")
                print(f"Subject: {msg.get('subject', 'N/A')}")
                print(f"Date:    {msg.get('created_at', 'N/A')}")
                body = msg.get('text') or msg.get('body') or ''
                print(f"\nBody:\n{body}")
        else:
            messages = list_messages(limit=args.limit)
            if args.json:
                print(json.dumps(messages, indent=2))
            else:
                # Handle paginated response
                if isinstance(messages, dict):
                    items = messages.get('messages', messages.get('items', [messages]))
                else:
                    items = messages
                print_messages(items)
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
