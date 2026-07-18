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
| [wordbank-reviewer](skills/wordbank-reviewer) | 古汉语 / 文言文选择题题库审查（id、答案、解析一致性） | MIT |
| [article-illustration](skills/article-illustration) | 文章配图规划与生成（含小红书配图） | MIT |
| [doc-review](skills/doc-review) | 资深编审级文档审查：文字 / 语法 / 格式 / 内容 / 风格五层 | MIT |
| [interdisciplinary-learning](skills/interdisciplinary-learning) | 语文跨学科学习设计（含小学 + 初中案例、模板、评价标准） | MIT |
| [jiangxi-zhongkao-beikao](skills/jiangxi-zhongkao-beikao) | 江西中考备考：基于 2023–2025 真题的命题规律与备考方案 | MIT |
| [jiaoyan-writing](skills/jiaoyan-writing) | 教研课题 / 论文 / 教学案例辅助撰写（含 PDF 解析、Word 排版） | MIT |
| [whole-book-reading](skills/whole-book-reading) | 整本书阅读与名著导读体系化设计（对标统编 12 部必读名著） | MIT |
| [wordfreq](skills/wordfreq) | 文档词频分析统计（Word / PDF / EPUB / TXT，表格 + 图表） | MIT |
| [zhongkao-analysis](skills/zhongkao-analysis) | 中考真题深度分析与考情研判（框架 + 模板） | MIT |

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
