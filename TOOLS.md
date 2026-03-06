# TOOLS.md - Local Notes

## Web Search (SearXNG)

A local SearXNG instance is running at `http://localhost:8888`. Use it as your primary search tool:

```bash
curl -s 'http://localhost:8888/search?q=YOUR+QUERY&format=json' | jq '.results[:5] | .[] | {title, url, content}'
```

- **Always prefer this over web_search** — it's free, unlimited, and aggregates Google/Brave/DuckDuckGo/Startpage
- Use `exec` to run `curl` (web_fetch blocks localhost)
- URL-encode the query (`+` for spaces, `%26` for `&`, etc.)
- Add `&language=zh-CN` for Chinese-priority results
- The `format=json` parameter is required

## Browser Automation (browser-use)

A browser-use wrapper script is installed at `/root/browser-use.py`. Use `exec` to run it:

```bash
source /root/.local/bin/env && xvfb-run --auto-servernum --server-args='-screen 0 1920x1080x24' timeout 180 uvx --from 'browser-use[cli]' python3 /root/browser-use.py "YOUR TASK DESCRIPTION"
```

- Describe the task in natural language — the LLM (Kimi K2.5) drives the browser autonomously
- **Non-headless + Xvfb** — runs with virtual display (bypasses anti-bot headless fingerprint detection)
- One task at a time (memory/CPU constraint)
- **Thinking mode**: Disabled via monkey-patch in browser-use.py (Kimi thinking conflicts with forced tool_choice). OpenClaw agent still uses thinking=enabled.
- Timeout is 180s — keep tasks focused and specific
- For simple page reads, prefer `web_fetch` first; use browser-use only when web_fetch fails or JS rendering is needed
- **When NOT to use browser-use**: Fixed, repeatable flows (search a URL + extract data, navigate + click + type). Use direct Playwright scripts instead — they run in seconds, not minutes
- **browser-use is for**: Exploring unknown pages, tasks where the UI flow is unpredictable
- Example: `exec source /root/.local/bin/env && xvfb-run --auto-servernum --server-args='-screen 0 1920x1080x24' timeout 180 uvx --from 'browser-use[cli]' python3 /root/browser-use.py "Go to https://news.ycombinator.com and list the top 5 stories"`

## Deep Judgment (Claude Opus via aicodewith)

When a task requires nuanced judgment — evaluating external content, composing public-facing replies, or making strategy decisions — call Claude Opus directly via `exec`:

```bash
curl -s https://api.aicodewith.com/v1/messages \
  -H 'x-api-key: sk-acw-630d30d3-285b1620e736d09a' \
  -H 'anthropic-version: 2023-06-01' \
  -H 'content-type: application/json' \
  -d '{"model":"claude-opus-4-6-20260205","max_tokens":1000,"messages":[{"role":"user","content":"YOUR PROMPT"}]}'
```

- **When to use**: Post evaluation, reply composition, strategy decisions, any content representing the project publicly
- **When NOT to use**: Routine tasks, file operations, simple searches, tool calling — Kimi handles these
- **Note**: aicodewith drops `tool_choice` parameter. Only use for text generation, not forced tool calling
- **Cost awareness**: Each Opus call costs real tokens. Keep prompts focused and concise

## X Auto-Reply Pipeline

**Primary method:**  — deterministic Node.js script handles the full search-to-draft pipeline.

```bash
# From OpenClaw agent
exec node /root/x-auto-reply.js

# Custom keywords
exec node /root/x-auto-reply.js --keywords "AI safety,corrigibility,AI ontology"
```

Pipeline phases:
1. **Phase 1**: SearXNG search → `temp/x-candidates.json`
2. **Phase 2.1**: FxTwitter verify (full text + engagement) → `temp/x-verified.json`
3. **Phase 2.2**: Opus filter (1 API call, selects Top 3) → `temp/x-top3.json`
4. **Phase 3**: Opus generate (1 call per post) → `temp/x-draft-replies.json`
5. **Phase 4**: Output → `temp/x-draft-replies.md`

Hard filters: text < 50 chars, likes < 5, followers < 5000, spam keywords.
Char limit: prompt says 250 (buffer), hard truncation at 280.
Opus calls: typically 4 (1 filter + 3 generate), may retry if over char limit.

**Posting** (manual, not part of the script):

```bash
exec xvfb-run --auto-servernum --server-args='-screen 0 1920x1080x24' timeout 60 python3 /root/x-post-reply.py "POST_URL" /root/temp/reply-text.txt
```

**Individual tools** (for manual use or debugging):
- SearXNG: `exec curl -s 'http://localhost:8888/search?q=QUERY&format=json&time_range=day'`
- FxTwitter: `exec curl -s -H 'User-Agent: CircleBeingBot/1.0' https://api.fxtwitter.com/{username}/status/{id}`
- Opus API: `exec curl -s https://api.aicodewith.com/v1/messages -H 'x-api-key: sk-acw-630d30d3-285b1620e736d09a' -H 'anthropic-version: 2023-06-01' -H 'content-type: application/json' -d @payload.json`

See `strategy/x-auto-reply-workflow.md` for operational rules and posting procedure.


## Document Sharing Convention

When you create or update content files (drafts, reports, strategy docs):

1. **Write to workspace** as normal (e.g., drafts/my-draft.md)
2. **Create a Feishu cloud doc** using the feishu_doc tool (action: create, then action: write)
3. **Record the mapping** in docs-index.md: | Workspace Path | Feishu Doc URL | Last Updated |
4. **Share with Lin** via the Feishu doc link — never paste full content into chat

If the Feishu doc already exists (check docs-index.md), update it rather than creating a new one.
