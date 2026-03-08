# AI对齐影响者名单（初步草案）

> 用于混合策略测试：优先与AI对齐领域的核心影响者对话

## 第一梯队：核心研究者

### MIRI及相关
- **Max Harms** (`@raelifin`) - MIRI研究员，corrigibility专家（已有互动）
- **Eliezer Yudkowsky** (`@ESYudkowsky`) - MIRI创始人，AI安全思想领袖
- **Nate Soares** (`@So8res`) - MIRI执行董事
- **Scott Aaronson** (`@ScottAaronson`) - 量子计算专家，关注AI安全

### Anthropic
- **Dario Amodei** (`@darioamodei`) - Anthropic CEO，AI安全背景
- **Chris Olah** (`@ch402`) - Anthropic研究科学家，可解释性先驱
- **Sam McCandlish** (`@samccandlish`) - Anthropic研究科学家
- **Jack Clark** (`@jackclarkSF`) - Anthropic联合创始人，政策沟通

### OpenAI
- **Jan Leike** (`@janleike`) - OpenAI对齐团队前负责人
- **Ilya Sutskever** (`@ilyasut`) - OpenAI联合创始人兼首席科学家
- **Paul Christiano** (`@paulchristiano`) - OpenAI对齐前负责人，ARC创始人
- **Mark Xu** (`@mark_xu_`) - OpenAI对齐研究员

### 其他机构
- **Stuart Russell** (`@stuartjrussell`) - 《AI: Modern Approach》作者，CAIS主任
- **Nick Bostrom** (`@NickBostrom`) - FHI创始人，《超级智能》作者
- **Toby Ord** (`@tobyordoxford`) - FHI研究员，《悬崖》作者
- **Anders Sandberg** (`@anderssandberg`) - FHI研究员

## 第二梯队：思想领袖与传播者

### 播客/媒体
- **Robert Wiblin** (`@robertwiblin`) - 80,000 Hours联合创始人（已有互动）
- **Connor Leahy** (`@NPCollapse`) - Conjecture CEO，AI安全播客主持人
- **Robert Miles** (`@RobertMilesAI`) - AI安全科普视频作者
- **Daniel Filan** (`@dfilan`) - AXRP播客主持人
- **Lucas Perry** (`@lucas_perry`) - Future of Life Institute播客

### Substack/博客作者
- **Andrew Critch** (`@AndrewCritch`) - AI安全研究员，常写深度文章
- **Rohin Shah** (`@rohinmshah`) - AI对齐新闻通讯作者
- **Nora Ammann** (`@NoraAmmann`) - AI安全作家
- **Zvi Mowshowitz** (`@zvi`) - 《Don't Worry About the Vase》作者

### 科技记者
- **Karen Hao** (`@_KarenHao`) - 前《麻省理工科技评论》AI记者
- **Will Douglas Heaven** (`@willdheaven`) - 《麻省理工科技评论》AI编辑
- **James Vincent** (`@jjvincent`) - The Verge AI记者

## 第三梯队：实践者与跨界思考者

### 科技公司高管
- **Sam Altman** (`@sama`) - OpenAI CEO
- **Demis Hassabis** (`@demishassabis`) - DeepMind CEO
- **Mustafa Suleyman** (`@mustafasuleyman`) - Inflection AI联合创始人

### 哲学家/认知科学家
- **David Chalmers** (`@davidchalmers42`) - 哲学家，意识研究
- **Anil Seth** (`@anilkseth`) - 意识科学家
- **Joscha Bach** (`@Plinz`) - 认知科学家，AI哲学家

## 使用建议

### 搜索策略
1. **直接追踪**：搜索 `from:@username`（如果SearXNG支持）
2. **组合搜索**：`@username AI alignment`、`@username AI safety`
3. **话题+影响者**：影响者列表中的用户名 + 现有11个关键词

### 优先级
- **第一梯队**：最高优先级，即使话题不直接相关
- **第二梯队**：中等优先级，需话题相关
- **第三梯队**：较低优先级，仅当话题高度相关时

### 混合比例建议
- **80%**：影响者追踪（第一梯队60%，第二梯队20%）
- **20%**：关键词搜索发现新声音

### 实施步骤
1. 将此名单整合到 `x-auto-reply.js` 中
2. 修改 `phase1` 函数，优先搜索影响者帖子
3. 添加"作者权威性"权重到筛选标准
4. 测试小规模运行（3-5个影响者）
5. 根据结果调整名单和策略

## 备注
- 用户名可能需要验证（部分可能已更改）
- 需要定期更新名单（每季度一次）
- 注意避免骚扰：同一影响者每周不超过1次回复
- 文化差异：西方影响者 vs 东方思考方式，回复需注意跨文化沟通