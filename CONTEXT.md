# Domain Glossary（taotao-skills）

> 本项目领域词汇表。所有 agent 在讨论、编码、写文档时必须使用这些术语，保持语言一致。

## 架构

- **Skill** — WorkBuddy 技能，由 SKILL.md + references/ + scripts/ 组成
- **SKILL.md** — 技能定义文件（大写），含 frontmatter + 能力描述 + 流程
- **References** — 技能的数据/知识/模板目录，技能自包含的知识库
- **Scripts** — 技能的可执行脚本目录（Python/Shell/JS）
- **L0 编排层** — Orchestration，teacher-workflow 元技能 + 场景包
- **L1 能力层** — Capabilities，按工作流环节分 4 域的具体技能
- **L2 数据底座** — Foundation，单一数据源（文言词库 / 品牌规范 / 模板库 / 教材版本库）

## 工作流环节（4 域）

- **备课设计** — 备课助手(k12)、整本书阅读、跨学科设计、配图规划、课件生成(规划)
- **文言古汉语** — 文言词典(guwen-cidian)、王力视角、吕叔湘视角、古诗文鉴赏
- **评价考情** — 江西中考备考、中考分析(通用)、文本词频、作文批改(规划)
- **教研写作** — 教研写作、文稿审核(doc-review)、学生自学卡(规划)

## 元数据

- **Frontmatter** — SKILL.md 顶部的 YAML 元数据块
- **Name** — 英文技能 ID，格式 `<动词>-<对象>`
- **Display-name** — 中文显示名，用于 README 与入口
- **Category** — 技能所属域（备课设计/文言古汉语/评价考情/教研写作）
- **Depends-on** — 技能声明的数据/能力依赖（如 guwen-cidian）
- **Version** — 语义化版本（如 2.0.0）
- **License** — MIT 或 Apache-2.0

## 质量规范（借鉴 Matt Pocock）

- **Completion Criterion** — 步骤的完成检查标准，必须可检查、可判定
- **Leading Word** — 主导词，紧凑概念锚定行为（如"速查"、"actionable释义"）
- **Context Pointer** — 上下文指针，引用外部文件（如 `references/字词卡片模板.md`）
- **Progressive Disclosure** — 渐进披露，信息分层：步骤 → 同文件参考 → 外部参考
- **User-invoked** — 用户触发（disable-model-invocation: true），如视角技能
- **Model-invoked** — 模型自动触发（默认），如查词/审核技能
- **Router Skill** — 路由技能，统一入口分发到具体技能
- **Single Source of Truth** — 单一数据源，共享知识只存一份，禁止复制

## 输出格式

- **字词卡片** — 锁死格式：读音/词性/义项/语境判定/中考频度/易错提醒
- **串讲卡** — 锁死格式：逐词标注/特殊用法/整句翻译
- **审核报告** — 锁死格式：🔴🟡🟢⚪ 四色标记
- **鉴赏卡** — 锁死格式：八栏（作者/朝代/体裁/主题/手法/意象/情感/定评与商榷）
