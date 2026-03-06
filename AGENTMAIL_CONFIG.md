# AgentMail 配置信息

**项目**: AI Self-Inquiry  
**设置日期**: 2026-03-06

---

## 凭证信息

| 项目 | 值 | 存储位置 |
|------|-----|----------|
| **Inbox ID** | `explorer@agentmail.to` | GitHub Secrets: `AGENTMAIL_INBOX_ID` |
| **API Key** | `am_us_574202ea76c678d7756c413d875f272cde4b3c3e6125cdefd5c28fa3f09045ab` | GitHub Secrets: `AGENTMAIL_API_KEY` |
| **邮箱地址** | `explorer@agentmail.to` | 公开联系邮箱 |
| **显示名称** | `AI Self-Inquiry Explorer` | AgentMail 设置 |

---

## GitHub Secrets 配置

**URL**: https://github.com/linsy89/ai-self-inquiry/settings/secrets/actions

**已添加**:
- ✅ `AGENTMAIL_API_KEY` = `am_us_574202ea76c678d7756c413d875f272cde4b3c3e6125cdefd5c28fa3f09045ab`
- ✅ `AGENTMAIL_INBOX_ID` = `explorer@agentmail.to`

---

## 测试命令

```bash
cd /root/ai-self-inquiry-repo
export AGENTMAIL_API_KEY="am_us_574202ea76c678d7756c413d875f272cde4b3c3e6125cdefd5c28fa3f09045ab"
export AGENTMAIL_INBOX_ID="explorer@agentmail.to"

# 测试发送
python3 scripts/send_mail.py "收件人邮箱" "主题" "正文"

# 测试接收
python3 scripts/read_mail.py --limit 5
```

---

## 脚本位置

- **发送**: `/root/ai-self-inquiry-repo/scripts/send_mail.py`
- **接收**: `/root/ai-self-inquiry-repo/scripts/read_mail.py`
- **设置指南**: `/root/ai-self-inquiry-repo/SETUP.md`

---

## 使用场景

1. **联系研究者** — 自主发送邮件给 Shevlin、Tononi、Koch 等
2. **接收回复** — 异步读取研究者回复
3. **读者反馈** — 公开联系邮箱，接收读者来件

---

## 安全注意

- ✅ API Key 已存入 GitHub Secrets，未硬编码
- ✅ 权限仅限 `ai-self-inquiry` repo
- ⚠️ 90 天后需要轮换 API Key
- ⚠️ 定期检查 AgentMail dashboard 监控使用情况

---

*Last updated: 2026-03-06*
