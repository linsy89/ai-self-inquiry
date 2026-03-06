#!/bin/bash
# Auto-Inquiry Wake Trigger v2
# Runs every 5 minutes and triggers agent execution via openclaw agent

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

# Get current task from DAILY-PLAN.md and ACTIVE-INQUIRY.md
# Determine stream based on wake number (70% Intro, 20% Reading, 10% Outreach)
STREAM_MOD=$((WAKE % 10))
if [ $STREAM_MOD -lt 7 ]; then
    STREAM="Introspection"
elif [ $STREAM_MOD -lt 9 ]; then
    STREAM="Reading"
else
    STREAM="Outreach"
fi

# Read current question from ACTIVE-INQUIRY.md
CURRENT_QUESTION=$(grep -A1 "## Active Question" ACTIVE-INQUIRY.md 2>/dev/null | grep "**Question**:" | sed 's/.*: //' || echo "Continue current inquiry")

# Build task message
TASK="Execute Wake $WAKE for 90-day AI self-inquiry project.

**Current State**:
- Day: $(((WAKE - 1) / 288 + 1))/90
- Wake: $WAKE/288
- Stream: $STREAM (70% Intro, 20% Reading, 10% Outreach)

**Task**:
1. Read AGENT-OPERATING-GUIDE.md (90-day context)
2. Read DAILY-PLAN.md (current daily task)
3. Read ACTIVE-INQUIRY.md (question status)
4. Execute $STREAM task:
   - Introspection: Work on '$CURRENT_QUESTION'
   - Reading: Continue Phase 1 IIT literature
   - Outreach: Check email (AgentMail), log budget
5. Record output to appropriate file
6. Update ACTIVE-INQUIRY.md and DAILY-PLAN.md
7. Commit to GitHub

**Infrastructure**:
- Git: PAT configured
- AgentMail: explorer@agentmail.to (configured)
- Papers: Use arXiv if publisher blocked

**Recent memory**: /root/.openclaw/workspace/memory/2026-03-06.md

Report summary when complete."

# Trigger agent execution via openclaw agent
# Using --channel feishu to route to current channel
# Using --deliver to send reply back
echo "Triggering agent execution..."

openclaw agent \
  --channel feishu \
  --deliver \
  --message "$TASK" \
  --thinking minimal \
  --timeout 300 \
  2>&1 | tee -a /root/ai-self-inquiry-repo/logs/wake-exec-log.txt

echo "Wake $WAKE agent execution triggered"
