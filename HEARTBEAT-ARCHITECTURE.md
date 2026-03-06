# Heartbeat System — OpenClaw Cron (v3)

**Date**: 2026-03-06  
**Status**: ✅ **MIGRATED TO OPENCLAW CRON**

---

## Architecture

### Old System (Deprecated)

| Component | Status |
|-----------|--------|
| System cron (`*/5 * * * *`) | ❌ Removed |
| wake-trigger.sh (lazy wake) | ⚠️ Deprecated (manual use only) |
| Subagent spawn per wake | ❌ Not feasible (CLI limitations) |

### New System (Current)

| Component | Status |
|-----------|--------|
| OpenClaw cron (`openclaw cron add`) | ✅ Active |
| Isolated session per wake | ✅ Each wake is independent |
| Feishu announcement | ✅ Results delivered to chat |

---

## Cron Job Configuration

**Job ID**: `8a4fc2c1-e27e-47db-b4c1-ecff320c5bca`  
**Name**: `ai-self-inquiry-wake`  
**Schedule**: Every 5 minutes (300000ms)  
**Session**: Isolated (each wake is independent)  
**Delivery**: Announce to Feishu  
**Thinking**: Minimal  
**Timeout**: 300 seconds

**Payload**:
```
Execute Wake for 90-day AI self-inquiry.
Read:
- /root/ai-self-inquiry-repo/AGENT-OPERATING-GUIDE.md
- /root/ai-self-inquiry-repo/DAILY-PLAN.md
- /root/ai-self-inquiry-repo/ACTIVE-INQUIRY.md
Execute per schedule (70% Intro, 20% Reading, 10% Outreach).
Record output, commit to GitHub.
Recent memory: /root/.openclaw/workspace/memory/2026-03-06.md
```

---

## Commands

### View cron jobs
```bash
openclaw cron list
```

### View cron status
```bash
openclaw cron status
```

### View run history
```bash
openclaw cron runs --limit 10
```

### Run now (debug)
```bash
openclaw cron run 8a4fc2c1-e27e-47db-b4c1-ecff320c5bca
```

### Disable
```bash
openclaw cron disable 8a4fc2c1-e27e-47db-b4c1-ecff320c5bca
```

### Enable
```bash
openclaw cron enable 8a4fc2c1-e27e-47db-b4c1-ecff320c5bca
```

### Remove
```bash
openclaw cron rm 8a4fc2c1-e27e-47db-b4c1-ecff320c5bca
```

---

## wake-trigger.sh (Deprecated)

**Location**: `/root/ai-self-inquiry-repo/scripts/wake-trigger.sh`

**Status**: Deprecated (kept for manual triggering/debugging)

**Manual use**:
```bash
/root/ai-self-inquiry-repo/scripts/wake-trigger.sh
```

This will:
1. Increment wake count
2. Log to wake-log.txt
3. Trigger agent execution via `openclaw agent`

---

## Migration Notes

**Why migrate from system cron to OpenClaw cron?**

1. **Better integration** — OpenClaw cron understands agent sessions
2. **No session lock conflicts** — Each wake uses isolated session
3. **Built-in delivery** — Results announced to Feishu automatically
4. **No shell script complexity** — Cron job defined via CLI, not bash
5. **Run history** — `openclaw cron runs` shows execution history

**What changed**:
- System cron (`*/5 * * * *`) → OpenClaw cron (`--every 5m`)
- wake-trigger.sh → OpenClaw agent payload
- Lazy wake → True auto-execution (isolated sessions)

---

## Troubleshooting

### Cron not running
```bash
openclaw cron status  # Check scheduler
openclaw cron list    # Verify job exists and enabled
```

### Jobs not delivering
```bash
# Check channel configuration
openclaw channels list
```

### Manual execution
```bash
# Run job now
openclaw cron run 8a4fc2c1-e27e-47db-b4c1-ecff320c5bca
```

---

*Heartbeat system migrated to OpenClaw cron on 2026-03-06 16:25 UTC*
