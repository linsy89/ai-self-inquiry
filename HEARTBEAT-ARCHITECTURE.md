# 5-Minute Heartbeat — Architecture Fix Needed

## Problem Identified

**Cron triggers, but Agent doesn't auto-execute.**

**Root cause**: OpenClaw uses "request-response" model:
- Agent only responds when user sends message
- Cron can trigger script, but can't force Agent session
- Session lock prevents concurrent access (main session locked when I'm active)

**Current state**:
- ✅ Cron runs every 5 minutes
- ✅ Wake counter increments
- ❌ Agent doesn't auto-execute tasks
- ❌ No output files generated

---

## Solution Options

### Option 1: Lazy Wake (Current Implementation)

**How it works**:
- Cron creates `.pending-wake.md` file
- Next human message triggers Agent
- Agent sees pending file, executes task

**Pros**:
- Simple, no architecture changes
- No session conflicts

**Cons**:
- Not truly automatic
- Depends on human interaction

**Status**: 🔄 Implemented (wake-trigger.sh v4)

---

### Option 2: Sub-Agent Loop (Recommended)

**How it works**:
1. Lin spawns a sub-agent: `sessions_spawn(mode="session", task="Execute wakes every 5 min")`
2. Sub-agent has its own session (no lock conflicts)
3. Sub-agent loops: execute task → sleep 5 min → repeat
4. Sub-agent reports back to main session

**Pros**:
- Truly automatic
- No session conflicts
- Independent execution

**Cons**:
- Requires initial setup (Lin spawns sub-agent)
- Sub-agent consumes budget continuously

**Implementation**:
```javascript
// Lin triggers this once
sessions_spawn({
  mode: "session",
  task: "Auto-Inquiry Wake Executor: Loop every 5 min, execute tasks per DAILY-PLAN.md",
  label: "wake-executor",
  cleanup: "keep"
})
```

---

### Option 3: Local Embedded Agent

**How it works**:
- Use `openclaw agent --local` in cron
- Requires API keys in environment
- Runs embedded model locally

**Pros**:
- Truly automatic
- No session conflicts

**Cons**:
- Requires API key configuration
- May not have same tools/capabilities

**Status**: ❌ Not tested (needs API config)

---

## Current Recommendation

**Use Option 1 (Lazy Wake) for now**:
- Cron records wakes
- Lin interacts every ~30 min
- Agent executes accumulated wakes in batch

**Transition to Option 2 when ready**:
- Lin spawns sub-agent once
- Sub-agent handles automatic execution
- Main session receives periodic reports

---

## Lazy Wake Execution Protocol

**When Agent sees `.pending-wake.md`**:

1. Read the file (shows how many wakes pending)
2. Execute tasks for each pending wake
3. Record outputs (batch commit)
4. Delete `.pending-wake.md`
5. Report: "Executed wakes X-Y, Z tasks completed"

**Example**:
- Cron triggers wakes 024-030 (7 wakes, 35 min)
- Lin sends message at wake 030
- Agent sees `.pending-wake.md`
- Agent executes wakes 024-030 in sequence
- Agent commits all outputs together
- Agent deletes `.pending-wake.md`

---

*This document explains the heartbeat architecture and current workaround.*  
*Last updated: 2026-03-06 15:35 UTC*
