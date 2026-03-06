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

# Create a wake record file that the next agent interaction will process
# This is a "lazy wake" - the task is recorded and executed on next human interaction
cat > /root/ai-self-inquiry-repo/.pending-wake.md << EOF
# Pending Wake $WAKE

**Scheduled**: $(date -u)
**Status**: PENDING (waiting for agent session)

**Task**: Execute per DAILY-PLAN.md and AGENT-OPERATING-GUIDE.md

**Instructions for Agent**:
When you see this file, it means a wake was triggered but the session was locked.
Please execute the pending wake task now:
1. Read AGENT-OPERATING-GUIDE.md (90-day overview)
2. Read DAILY-PLAN.md (current task)
3. Execute task (Introspection/Reading/Outreach)
4. Record output
5. Delete this file when complete
EOF

echo "Wake $WAKE recorded (lazy execution)"
