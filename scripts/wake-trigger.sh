#!/bin/bash
# Auto-Inquiry Wake Trigger
# Runs every 5 minutes to trigger agent exploration

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

# Agent reads these files each wake:
# 1. AGENT-OPERATING-GUIDE.md — 90-day project overview (this is the master context)
# 2. DAILY-PLAN.md — Today's specific tasks
# 3. ACTIVE-INQUIRY.md — Question status tracker
# 4. TASK-SCHEDULE.md — Work stream allocation
