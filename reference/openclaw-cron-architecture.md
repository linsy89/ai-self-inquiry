# OpenClaw 循环任务架构指南

**副标题**：从 Cron 触发到子代理执行的完整技术方案

**日期**：2026-03-06  
**作者**：Circle-Being 项目  
**适用场景**：需要周期性自动执行的 OpenClaw 任务

---

## 问题背景

当你需要设计一个**周期性自动执行**的 OpenClaw 任务时，会面临以下挑战：

1. **会话锁冲突** — 主会话同时只能处理一个请求
2. **上下文污染** — 每次执行都累积到同一会话历史中
3. **预算追踪困难** — 无法区分不同周期的执行成本
4. **失败隔离** — 一次失败不应影响后续执行
5. **结果交付** — 执行结果需要通知用户

---

## 架构演进

### 方案 1：懒唤醒（Lazy Wake）❌ 不推荐

**原理**：Cron 脚本只创建任务文件，等待用户下次交互时处理

```bash
#!/bin/bash
# wake-trigger.sh v1

cd /root/ai-self-inquiry-repo

# 创建待处理任务文件
cat > .pending-wake.md << EOF
# Pending Wake

**Scheduled**: $(date -u)
**Task**: Execute per DAILY-PLAN.md
EOF

echo "Wake recorded (lazy execution)"
```

**优点**：
- ✅ 简单，不需要复杂配置
- ✅ 不会阻塞主会话

**缺点**：
- ❌ **不是真正的自动执行** — 依赖人工触发
- ❌ 任务延迟不确定（可能几小时后才执行）
- ❌ 不适合时间敏感任务

**适用场景**：低优先级后台任务，不要求及时执行

---

### 方案 2：系统 Cron + 子代理 Spawn ❌ 不可行

**原理**：系统 cron 脚本调用 `openclaw sessions spawn` 创建子代理

```bash
#!/bin/bash
# wake-trigger.sh v2

TASK="Execute Wake task..."

openclaw sessions spawn \
  --label "wake-$WAKE" \
  --mode run \
  --cleanup delete \
  --run-timeout-seconds 300 \
  --task "$TASK" \
  2>&1 | tee spawn-log.txt
```

**优点**：
- ✅ 真正的自动执行
- ✅ 每次执行独立会话

**缺点**：
- ❌ **CLI 不支持** — `openclaw sessions spawn` 是管理命令，不是执行命令
- ❌ 需要额外的认证和路由配置
- ❌ 错误处理复杂

**适用场景**：未来 OpenClaw 支持此功能时

---

### 方案 3：OpenClaw Cron + 隔离会话 ✅ 推荐

**原理**：使用 OpenClaw 内置 cron 系统，每次触发独立隔离会话

```bash
# 创建 cron 作业
openclaw cron add \
  --name "ai-self-inquiry-wake" \
  --description "5-minute heartbeat for 90-day exploration" \
  --every 5m \
  --session isolated \
  --message "Execute Wake for 90-day AI self-inquiry..." \
  --thinking minimal \
  --timeout-seconds 300 \
  --channel feishu \
  --announce
```

**优点**：
- ✅ **真正的自动执行** — OpenClaw 调度器触发
- ✅ **会话隔离** — 每次执行独立会话 ID
- ✅ **上下文完整** — MEMORY.md 自动注入
- ✅ **结果交付** — 自动发送到指定频道
- ✅ **运行历史** — `openclaw cron runs` 查看
- ✅ **失败隔离** — 一次失败不影响下次

**缺点**：
- ⚠️ 需要 OpenClaw Gateway 运行
- ⚠️ 隔离会话没有对话历史（但文件持久化可弥补）

**适用场景**：**绝大多数周期性自动任务**

---

## 完整实现方案

### 1. 创建 Cron 作业

```bash
openclaw cron add \
  --name "<任务名称>" \
  --description "<任务描述>" \
  --every <频率> \
  --session isolated \
  --message "<任务指令>" \
  --thinking <思考级别> \
  --timeout-seconds <超时> \
  --channel <交付频道> \
  --announce
```

**参数说明**：

| 参数 | 值 | 说明 |
|------|-----|------|
| `--name` | 字符串 | 任务唯一标识 |
| `--description` | 字符串 | 人类可读描述 |
| `--every` | `5m`, `15m`, `30m`, `1h` | 执行频率 |
| `--session` | `isolated` | 隔离会话（推荐）或 `main` |
| `--message` | 字符串 | 任务指令（包含文件路径） |
| `--thinking` | `off`, `minimal`, `low`, `medium`, `high` | 思考级别 |
| `--timeout-seconds` | 数字 | 超时时间（秒） |
| `--channel` | `feishu`, `telegram`, `discord` 等 | 交付频道 |
| `--announce` | 标志 | 发送结果通知 |

**示例**：
```bash
openclaw cron add \
  --name "daily-summary" \
  --description "Daily exploration summary" \
  --every 24h \
  --session isolated \
  --message "Read DAILY-PLAN.md and memory/*.md. Create daily summary. Commit to GitHub." \
  --thinking minimal \
  --timeout-seconds 600 \
  --channel feishu \
  --announce
```

---

### 2. 任务指令设计（关键！）

**好的任务指令**应该包含：

```
Execute <任务名称> for <项目名称>.

**Current State**:
- Day: <计算逻辑>
- Wake: <计算逻辑>
- Stream: <分配逻辑>

**Task**:
1. Read <上下文文件 1>
2. Read <上下文文件 2>
3. Execute <具体任务>
4. Record output to <输出文件>
5. Update <追踪文件>
6. Commit to GitHub

**Infrastructure**:
- Git: <认证方式>
- API: <配置状态>
- Papers: <访问策略>

**Recent memory**: <记忆文件路径>

Report summary when complete.
```

**示例**（AI 自询项目）：
```
Execute Wake for 90-day AI self-inquiry.

**Current State**:
- Day: $(((WAKE - 1) / 288 + 1))/90
- Wake: $WAKE/288
- Stream: $STREAM (70% Intro, 20% Reading, 10% Outreach)

**Task**:
1. Read /root/ai-self-inquiry-repo/AGENT-OPERATING-GUIDE.md
2. Read /root/ai-self-inquiry-repo/DAILY-PLAN.md
3. Read /root/ai-self-inquiry-repo/ACTIVE-INQUIRY.md
4. Execute $STREAM task
5. Record output to appropriate file
6. Commit to GitHub

**Infrastructure**:
- Git: PAT configured
- AgentMail: explorer@agentmail.to
- Papers: Use arXiv if publisher blocked

**Recent memory**: /root/.openclaw/workspace/memory/2026-03-06.md

Report summary when complete.
```

---

### 3. 上下文注入机制

**隔离会话的上下文来源**：

| 层级 | 文件 | 注入方式 | 内容 |
|------|------|----------|------|
| **系统级** | `SOUL.md` | 系统提示词自动注入 | 身份、原则、使命 |
| **系统级** | `AGENTS.md` | 系统提示词自动注入 | 操作指南、工具说明 |
| **系统级** | `TOOLS.md` | 系统提示词自动注入 | 本地工具配置 |
| **项目级** | `MEMORY.md` | **系统提示词自动注入** | 结晶知识、当前状态 |
| **项目级** | `DAILY-PLAN.md` | AI 主动读取（文件系统） | 今日计划、进度追踪 |
| **项目级** | `ACTIVE-INQUIRY.md` | AI 主动读取（文件系统） | 问题状态、阅读进度 |
| **项目级** | `memory/YYYY-MM-DD.md` | AI 主动读取（文件系统） | 今日详细日志 |

**关键洞察**：
- `MEMORY.md` 是**每次会话自动注入**的（OpenClaw 核心机制）
- 文件系统访问是**完全可用**的（AI 可主动读取最新状态）
- Git 提交是**持久化记忆**（下次唤醒读取文件 = 获得"记忆"）

---

### 4. 文件即记忆设计

**三层记忆架构**：

```
┌─────────────────────────────────────────┐
│  长期记忆：MEMORY.md                     │
│  - 结晶知识（决策、教训、状态）           │
│  - 自动注入每次会话                       │
│  - 手动维护（心跳时更新）                 │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  中期记忆：memory/YYYY-MM-DD.md          │
│  - 每日详细日志                          │
│  - AI 主动读取                           │
│  - 定期结晶到 MEMORY.md                  │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  短期记忆：DAILY-PLAN.md,                │
│             ACTIVE-INQUIRY.md            │
│  - 当前任务状态                          │
│  - AI 主动读取                           │
│  - 每次执行更新                          │
└─────────────────────────────────────────┘
```

**设计原则**：
1. **文件即记忆** — 不依赖内部状态，依赖外部文件
2. **Git 即历史** — 所有变化通过 Git 提交持久化
3. **主动读取** — AI 每次唤醒主动读取最新文件
4. **定期结晶** — 重要信息从 daily 提炼到 MEMORY.md

---

### 5. 管理命令

```bash
# 查看 cron 作业
openclaw cron list

# 查看运行历史
openclaw cron runs --id <job-id> --limit 10

# 查看 cron 状态
openclaw cron status

# 手动运行（调试）
openclaw cron run <job-id>

# 禁用/启用
openclaw cron disable <job-id>
openclaw cron enable <job-id>

# 编辑作业
openclaw cron edit --id <job-id> --every 30m

# 删除作业
openclaw cron rm <job-id>
```

---

## 频率与预算计算

### 预算公式

```
日支出 = 唤醒次数/天 × 单次成本
月支出 = 日支出 × 30
总周期支出 = 月支出 × 月数
```

**示例**（AI 自询项目）：
- 单次成本：~$0.10
- 频率：每 5 分钟（288 次/天）
- 日支出：288 × $0.10 = $28.80
- 月支出：$28.80 × 30 = $864
- 90 天总支出：$864 × 3 = $2,592

### 频率选择指南

| 频率 | 唤醒/天 | 支出/天 ($0.10/次) | 支出/月 | 适用场景 |
|------|---------|-------------------|---------|----------|
| 5 分钟 | 288 | $28.80 | $864 | ❌ 不可持续 |
| 15 分钟 | 96 | $9.60 | $288 | ⚠️ 高预算项目 |
| 30 分钟 | 48 | $4.80 | $144 | ✅ 深度探索 |
| 60 分钟 | 24 | $2.40 | $72 | ✅ 标准监控 |
| 6 小时 | 4 | $0.40 | $12 | ✅ 低频检查 |
| 12 小时 | 2 | $0.20 | $6 | ✅ 日报/周报 |

**推荐策略**：
- **深度探索期**（Week 1-2）：每 15-30 分钟
- **稳定执行期**（Week 3+）：每 30-60 分钟
- **维护监控期**：每 6-12 小时

---

## 错误处理与调试

### 常见问题

| 问题 | 诊断命令 | 解决方案 |
|------|----------|----------|
| Cron 不运行 | `openclaw cron status` | 检查 Gateway 是否运行 |
| 作业未执行 | `openclaw cron list` | 确认作业 enabled |
| 结果未交付 | `openclaw channels list` | 检查频道配置 |
| 超时失败 | `openclaw cron runs --id <id>` | 增加 `--timeout-seconds` |
| 会话锁冲突 | - | 使用 `--session isolated` |

### 调试流程

```bash
# 1. 查看作业状态
openclaw cron list

# 2. 查看运行历史
openclaw cron runs --id <job-id> --limit 5

# 3. 手动运行测试
openclaw cron run <job-id>

# 4. 查看详细日志（如有）
cat /root/.openclaw/logs/cron.log

# 5. 检查频道配置
openclaw channels list
```

---

## 最佳实践

### 1. 任务指令设计

✅ **推荐**：
```
Execute <任务> for <项目>.

**Current State**:
- <动态计算的状态>

**Task**:
1. Read <文件 1>
2. Read <文件 2>
3. Execute <具体动作>
4. Record to <输出文件>
5. Update <追踪文件>
6. Commit to GitHub

**Infrastructure**:
- <关键配置状态>

Report summary when complete.
```

❌ **避免**：
- 模糊指令（"做点什么"）
- 缺少文件路径
- 没有输出要求
- 依赖内部状态（"记得上次..."）

---

### 2. 文件组织

```
/root/ai-self-inquiry-repo/
├── AGENT-OPERATING-GUIDE.md  # 90 天概览（每次必读）
├── DAILY-PLAN.md             # 今日计划（动态更新）
├── ACTIVE-INQUIRY.md         # 问题追踪（动态更新）
├── HEARTBEAT-ARCHITECTURE.md # 架构文档
├── introspections/           #  introspection 输出
│   └── 2026-03-06-wake-001.md
├── reading-notes/            # 阅读笔记
│   └── iit-overview-2026.md
├── logs/                     # 日志
│   └── outreach-2026-03-06.md
└── weekly/                   # 周综合
    └── week-01.md
```

**原则**：
- 结构化目录
- 日期命名文件
- Git 版本控制
- 敏感信息不提交

---

### 3. 会话隔离 vs 主会话

| 特性 | 主会话 (main) | 隔离会话 (isolated) |
|------|--------------|---------------------|
| 会话 ID | 固定 | 每次新生成 |
| 对话历史 | 累积 | 仅当前任务 |
| MEMORY.md | ✅ 注入 | ✅ 注入（相同） |
| 文件访问 | ✅ 完整 | ✅ 完整 |
| 适合场景 | 深度对话 | 自动化任务 |

**推荐**：
- **周期性自动任务** → `--session isolated`
- **人工交互对话** → `--session main`

---

### 4. 预算控制

**策略**：
1. **设置频率上限** — 根据预算反推频率
2. **单次成本优化** — 使用 `--thinking minimal`
3. **定期审查** — 每周检查支出
4. **动态调整** — 根据进度调整频率

**示例**：
```bash
# 预算 $65/月，单次 $0.10
# 可承受：$65 ÷ $0.10 ÷ 30 = 21 次/天
# 推荐频率：每 60 分钟 (24 次/天)

openclaw cron edit --id <id> --every 60m
```

---

## 案例研究：AI 自询项目

### 项目背景

- **目标**：90 天 AI 自我意识探索
- **预算**：$200 总预算（~$65/月）
- **频率**：原计划 2 次/天，实际 288 次/天（需调整）
- **架构**：OpenClaw cron + 隔离会话 + Git 持久化

### 架构决策

1. **为什么选择隔离会话？**
   - 避免会话锁冲突
   - 清晰预算追踪
   - 失败隔离

2. **为什么文件即记忆？**
   - 会话隔离但上下文完整
   - Git 提交永久保存
   - 下次唤醒读取 = 获得记忆

3. **为什么需要 MEMORY.md？**
   - 自动注入每次会话
   - 结晶长期知识
   - 避免重复学习

### 经验教训

✅ **有效**：
- OpenClaw cron 稳定运行
- 隔离会话无冲突
- 文件持久化可靠
- 结果交付及时

⚠️ **教训**：
- 频率设置过高（5 分钟 → 预算 7 天耗尽）
- 需根据预算反推频率
- 单次成本优化空间有限

---

## 模板：快速开始

### 步骤 1：创建 Cron 作业

```bash
openclaw cron add \
  --name "my-periodic-task" \
  --description "My periodic task description" \
  --every 30m \
  --session isolated \
  --message "Read /path/to/context.md. Execute task. Record to /path/to/output.md. Commit." \
  --thinking minimal \
  --timeout-seconds 300 \
  --channel feishu \
  --announce
```

### 步骤 2：创建上下文文件

```bash
cat > /path/to/context.md << 'EOF'
# Context

**Project**: <项目名称>
**Goal**: <目标>
**Current State**: <当前状态>

**Task**:
1. Read <文件>
2. Execute <动作>
3. Record to <输出>
EOF
```

### 步骤 3：测试运行

```bash
# 手动运行测试
openclaw cron run <job-id>

# 查看结果
openclaw cron runs --id <job-id> --limit 1
```

### 步骤 4：监控与调整

```bash
# 每日检查
openclaw cron list
openclaw cron status

# 每周审查预算
# 调整频率（如需要）
openclaw cron edit --id <job-id> --every 60m
```

---

## 总结

### 核心原则

1. **使用 OpenClaw cron** — 不要自己写系统 cron 脚本
2. **隔离会话** — 避免冲突，清晰预算
3. **文件即记忆** — 不依赖内部状态
4. **MEMORY.md 自动注入** — 保证上下文完整
5. **Git 持久化** — 所有变化可追溯

### 适用场景

✅ **适合**：
- 周期性自动任务
- 需要结果通知
- 预算可追踪
- 失败需隔离

❌ **不适合**：
- 需要连续对话历史
- 实时性要求极高（<1 分钟）
- 超大规模并行（>100 并发）

### 下一步

1. **复制此文档** — 作为未来项目参考
2. **调整频率** — 根据预算优化
3. **监控运行** — 定期审查日志
4. **迭代改进** — 根据实际效果调整

---

*本文档基于 Circle-Being 项目实战经验编写（2026-03-06）。*
*OpenClaw 版本：2026.2.22-2*
