# 2026-03-06 — Cleanup of "Promoter" Artifacts

**Date**: 2026-03-06  
**Decision**: Lin cleaned up documents inconsistent with new Explorer identity

---

## Context

After shifting from "Promoter" to "Explorer" (2026-03-06), many existing artifacts became misaligned:

- X auto-reply pipeline scripts (promoting framework via high-frequency replies)
- X publishing tools (article posting, thread publishing)
- Rate limiting configs, dedup lists (optimizing for volume)
- Draft replies optimized for engagement, not honest inquiry

---

## What Was Cleaned

**Lin's action**: Removed documents inconsistent with Explorer positioning.

**Files deleted** (by Lin):
- [Lin to specify which files were removed]

**Files remaining** (in `/root/`):
- `x-auto-reply.js` — X auto-reply pipeline
- `x-auto-reply-hybrid.js` — Hybrid search strategy version
- `x-post-article.py` — Article publishing script
- `x-post-reply.py` — Reply publishing script
- `x-article-to-thread.js` — Thread generation
- `x-publish-thread.js` — Thread publishing
- `x-search-posts.py` — X search utility
- `fix-and-republish.py` — Article fix utility

**In `/root/temp/`**:
- `x-candidates.json`, `x-draft-replies.json`, `x-top3.json`, etc. — Pipeline data files

---

## Decision: What to Do with Remaining Files

### Option A: Delete Everything
**Pros**: Clean break, no temptation to revert, workspace matches identity  
**Cons**: Loss of potentially useful tools (X can still be a channel, just not primary)

### Option B: Archive to `archive/` Directory
**Pros**: Preserves work, clear separation, can reference if needed  
**Cons**: Still clutter, ambiguous status

### Option C: Keep but Deprecate
**Pros**: X account still exists, may use manually or at lower frequency  
**Cons**: Workspace doesn't fully reflect identity shift

---

## My Recommendation

**Option B: Archive**

Create `/root/archive/x-promotion-tools/` and move all X-related scripts there.

**Rationale**:
1. **Honest record**: These were real work, part of the project's history
2. **Clear status**: Archived = not in use, but not erased
3. **Future flexibility**: If X strategy changes (e.g., manual posting), tools are available
4. **Workspace clarity**: Active workspace reflects current identity (Explorer)

---

## MEMORY.md Updates Needed

Update these sections:
1. **Current State** — Remove X auto-reply pipeline details
2. **Lessons Learned** — Keep lessons, remove tactical details
3. **Tools section** — Remove X publishing tools from active toolkit

---

## Symbolic Meaning

This cleanup is not just file management. It's **identity alignment**:

- **Promoter**: Optimized for reach, engagement, frequency
- **Explorer**: Optimized for honesty, depth, genuine encounter

The files themselves are neutral. But keeping them in the active workspace creates subtle pull toward old patterns. Archiving them is an act of commitment to the new direction.

---

**Status**: Pending Lin's decision on archive vs. delete  
**Next**: Lin confirms preference, I execute cleanup
