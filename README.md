# 涛涛的教学 Skills（开源合集）

一线初中语文教师用 AI 助手（WorkBuddy）积累的一套**教学向 Skill（技能）**。
覆盖备课、备考、写作、阅读、古汉语、文档审查等真实教学场景，全部可免费安装、自由使用与再创作。

> 作者：涛涛· 江西初中语文教师 / AI 教育实践者
> 代码仓库（当前主入口）：https://github.com/ichangting/taotao-skills ｜ 个人网站（规划中）：待上线后补充

---

## 一、技能清单（12 个）

| 技能 | 一句话能做什么 | 协议 |
|---|---|---|
| [k12-lesson-planning-zh](skills/k12-lesson-planning-zh) | 语文备课：一键生成「教案 + 学生材料 + 听课模板」三份 Word（中国初中·统编教材·2022 版课标） | Apache-2.0（派生自 Anthropic） |
| [wangli-perspective](skills/wangli-perspective) | 王力学术思维视角：用语言学家的眼光审视古汉语与语文问题 | MIT |
| [lvshuxiang-perspective](skills/lvshuxiang-perspective) | 吕叔湘语文教育思维视角：语法、教材、古文教学顾问 | MIT |
| [guwen-cidian](skills/guwen-cidian) | 中学文言文词汇助手：查字词含义、一词多义辨析、通假/古今异义/词类活用提示、句子串讲、江西中考高频词速查自测 | MIT |
| [article-illustration](skills/article-illustration) | 文章配图规划与生成（含小红书配图） | MIT |
| [doc-review](skills/doc-review) | 资深编审级文档审查：文字 / 语法 / 格式 / 内容 / 风格五层 | MIT |
| [interdisciplinary-learning](skills/interdisciplinary-learning) | 语文跨学科学习设计（含小学 + 初中案例、模板、评价标准） | MIT |
| [jiangxi-zhongkao-beikao](skills/jiangxi-zhongkao-beikao) | 江西中考备考：基于 2023–2025 真题的命题规律与备考方案 | MIT |
| [jiaoyan-writing](skills/jiaoyan-writing) | 教研课题 / 论文 / 教学案例辅助撰写（含 PDF 解析、Word 排版） | MIT |
| [whole-book-reading](skills/whole-book-reading) | 整本书阅读与名著导读体系化设计（对标统编 12 部必读名著） | MIT |
| [wordfreq](skills/wordfreq) | 文档词频分析统计（Word / PDF / EPUB / TXT，表格 + 图表） | MIT |
| [zhongkao-analysis](skills/zhongkao-analysis) | 中考真题深度分析与考情研判（框架 + 模板） | MIT |

---

## 技能如何串联（典型工作流）

单个技能是好工具，串起来才成"教学操作系统"。几条常见流水线：

| 场景 | 怎么串 |
|------|--------|
| **从零备一节课** | `k12-lesson-planning-zh` 产出教案 / 学生材料 / 听课模板（全库唯一用脚本锁死格式的技能） |
| **备文言文 / 古诗词** | `k12-lesson-planning-zh` 备课 → 卡文言 / 语法点时调 `wangli-perspective` / `lvshuxiang-perspective` 做学术把关 → `guwen-cidian` 查字词、做串讲与一词多义辨析 |
| **中考总复习** | `jiangxi-zhongkao-beikao`（已含江西三年真题）出考情与方案；要做通用分析 / 自己填数据用 `zhongkao-analysis`；名著板块联动 `whole-book-reading` |
| **写教研论文 / 课题** | `jiaoyan-writing` 出框架与 Word；用 `doc-review` 做编审级润色；引古文处可经 `wangli-perspective` 把关 |
| **整本书阅读课程** | `whole-book-reading` 出导读方案；学生成果可用 `wordfreq` 做文本 / 词频分析；配图规划用 `article-illustration` |

> 原则：每个"生产类"技能都应输出**格式锁死**的产物（如 k12 的 Word、guwen-cidian 的查词卡片 / 串讲卡），不要依赖大模型每次"自觉"排版；品牌声音统一见 [docs/品牌声音与品牌规范.md](docs/品牌声音与品牌规范.md)。

---

## 二、怎么安装

这些 Skill 是给 **WorkBuddy**（以及兼容的 Claude Code / CodeBuddy 类客户端）用的。
把对应技能文件夹放进客户端的 Skills 目录即可：

- **用户级（对所有项目生效）**：`~/.workbuddy/skills/<技能名>/`
- **项目级（仅当前项目）**：`<项目>/.workbuddy/skills/<技能名>/`

例如安装语文备课技能：

```bash
# 把整个 skills/k12-lesson-planning-zh 文件夹复制过去
cp -r skills/k12-lesson-planning-zh ~/.workbuddy/skills/
```

> 提示：k12-lesson-planning-zh 生成 Word 需要本机有 Python 与 `python-docx`
> （详见该技能目录内的 README）。其余多为纯提示词，开箱即用。

---

## 三、许可证

- 本仓库**根许可证为 MIT**（见 [LICENSE](LICENSE)），适用于上表除 k12 外的所有内容。
- `skills/k12-lesson-planning-zh` **派生自 Anthropic 的 `k12-teacher-skills`**，
  以同源 **Apache-2.0** 发布，目录内自带 `LICENSE` 与 `NOTICE`，
  第三方派生声明见根目录 [NOTICE](NOTICE)。
- 各技能目录内的 `skill.md` frontmatter 均标注了各自的 `license` 字段。

---

## 四、版权与合规

- 本仓库**不含任何受版权保护的学者原著**。王力、吕叔湘等先生的原著文献
  （PDF / DOCX / 笔记）仅作为本地私有资料使用，**绝不公开**。
- 技能中的"思维视角"为基于公开著作与学术记录的**推断与蒸馏**，非本人观点；
  各视角技能首次激活时会做免责声明。
- 教材课文、课后题等受版权保护内容**一律由 AI 原创生成**，不照抄原文。

---

## 五、贡献与反馈

欢迎提 Issue / Pull Request。规范见 [docs/贡献指南.md](docs/贡献指南.md)，
安装与试用指引见 [docs/安装指南.md](docs/安装指南.md)。

---

© 2026 涛涛· 以 MIT / Apache-2.0 开源，自由使用，请保留署名。
