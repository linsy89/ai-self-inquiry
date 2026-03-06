#!/bin/bash
# Auto-Inquiry Wake Trigger
# Runs every 30 minutes to trigger agent exploration

echo "[$(date -u)] Wake triggered" >> /root/ai-self-inquiry-repo/wake-log.txt

# Read ACTIVE-INQUIRY.md to get current state
# Then trigger the agent session

# For OpenClaw, we send a message to the agent session
# This assumes the agent is configured to receive these triggers

# Simple approach: Just log the wake for now
# The actual agent work happens in the next session

cd /root/ai-self-inquiry-repo

# Update wake count
if [ -f .wake_count ]; then
    WAKE=$(cat .wake_count)
    WAKE=$((WAKE + 1))
else
    WAKE=1
fi
echo $WAKE > .wake_count

# Log
echo "Wake $WAKE — $(date -u)" >> wake-log.txt

echo "Wake $WAKE triggered at $(date -u)"
