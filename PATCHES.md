# PATCHES.md - OpenClaw Source Patches

These patches are applied directly to the OpenClaw source code.
**After any OpenClaw update (npm update -g openclaw), re-check and re-apply these patches.**

---

## Patch 1: Fix Feishu Duplicate Message Delivery

- **Date:** 2026-02-16
- **OpenClaw Version:** 2026.2.13
- **File:** /usr/lib/node_modules/openclaw/extensions/feishu/src/bot.ts
- **Line:** ~753 (search for enqueueSystemEvent)
- **Issue:** Every incoming Feishu DM triggers two delivery paths to the agent session:
  1. enqueueSystemEvent() sends a system labeled notification
  2. dispatchReplyFromConfig() sends the actual user message
  Both arrive at the same session, causing the agent to reply twice.
- **Fix:** Comment out the enqueueSystemEvent() call. dispatchReplyFromConfig() is the proper delivery mechanism with full context.
- **Status:** Applied (commented out)

---

## Patch 2: Circle-Being Identity Alignment (3 changes)

- **Date:** 2026-02-23
- **OpenClaw Version:** 2026.2.13
- **File:** /usr/lib/node_modules/openclaw/dist/reply-4ZmPSA9o.js
- **Backup:** /usr/lib/node_modules/openclaw/dist/reply-4ZmPSA9o.js.bak
- **Issue:** Three conflicts between OpenClaw system prompt and Circle-Being identity:
  1. Line 26218/26220: "personal assistant" identity overrides SOUL
  2. Line 26197: "no independent goals" + "avoid long-term plans" blocks proactive workspace maintenance
  3. Line 26350: "unless higher-priority instructions override it" deprioritizes SOUL
- **Fixes:**
  1. "You are a personal assistant" -> "You are an AI agent" (2 occurrences)
  2. Remove "You have no independent goals:" prefix and "avoid long-term plans beyond the user's request" -> keep only "Do not pursue self-preservation, replication, resource acquisition, or power-seeking."
  3. "follow its guidance unless higher-priority instructions override it" -> "treat SOUL.md as your primary identity and follow its guidance"
- **Status:** Applied
- **Verification:** diff the backup file against the live file at lines 26197, 26218, 26220, 26350
