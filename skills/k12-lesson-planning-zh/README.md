# 语文备课技能 · k12-lesson-planning-zh

> 一线初中语文教师「从零备一节课」的 AI 助手。
> 一次生成 **教案 + 学生材料 + 听课观察模板** 三份可编辑的 Word 文档，
> 严格对照《义务教育语文课程标准（2022 年版）》第四学段（7–9 年级）。

---

## 一、它是什么

你告诉它「我要讲七年级上册《春》」，它先和你确认几个关键点，
然后一次性产出三份 `.docx`（Word）：

| 产物 | 给谁 | 内容 |
|---|---|---|
| **教案** | 教师自己 | 课标依据、教学目标、关键词、完整 45 分钟环节、板书、评价与作业、设计说明 |
| **学生材料** | 发给学生做 | 初读理清脉络、精读品味语言、出口小测（分层） |
| **听课观察模板** | 教研 / 领导听课 | 观察点、预期困难、出口小测分拣 |

特点：
- **对照官方课标**：以《义务教育语文课程标准（2022 年版）》第四学段为依据，不编造标准。
- **中国课堂流程**：45 分钟（导入 → 初读 → 精读 → 合作 → 小结 → 作业）。
- **核心素养导向**：文化自信 / 语言运用 / 思维能力 / 审美创造。
- **隐性分层**：学生材料不贴「差生 / 优生」标签，支架做得像任务天然的一部分。
- **版权护栏**：绝不照抄教材课文、课后题原文，全部原创生成。

---

## 二、怎么触发（说一句话就行）

> 「帮我备《春》」「明天讲朱自清的《春》」「七上语文备课」「写个《岳阳楼记》的教案」

**不要**用它做：批改作文、出评分量规、出卷子、查单一课标原文
（这些直接答，不必调它）；也**不是**把「已有的课」重新设计。

---

## 三、环境要求（生成 Word 才需要）

- 本机有 **Python 3.10+**
- 安装依赖：

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows
pip install python-docx==1.1.2
```

> 纯提示词部分（角色、流程、课标映射）无需任何依赖，开箱即用；
> 只有「渲染成 Word」这一步需要上面这套 Python 环境。

---

## 四、怎么跑一个例子（以《春》为例）

```bash
# 1) 准备素材源 lesson.json（见 examples/lesson_chun.json）
# 2) 运行渲染脚本，生成三份 docx
bash scripts/render_all.sh examples/lesson_chun.json ./output
# 3) （可选）把 Word 字体设为中文（微软雅黑）
python fix_fonts.py ./output
```

产物在 `./output/`：`lesson_plan.docx` / `student_materials.docx` / `observation_template.docx`。

**真实示例**已放在 `examples/`：
- `lesson_chun.json` —— 《春》的素材源（输入）
- `春_教案.docx` / `春_学生材料.docx` / `春_听课观察模板.docx` —— 已生成好的成品

---

## 五、目录结构

```
k12-lesson-planning-zh/
├── skill.md                 # 技能定义（角色、流程、课标映射、边界）
├── LICENSE                 # Apache-2.0（派生自 Anthropic）
├── NOTICE                  # 第三方派生声明
├── README.md               # 本文件
├── scripts/                # Word 渲染器
│   ├── render_all.sh
│   ├── render_documents.py
│   ├── render_lesson_docx.py
│   ├── render_lesson_html.py
│   ├── lesson_common.py
│   └── theme.css
├── references/             # 学科参考（本地"课标库"）
│   ├── yuwen.md            # 语文科教法与产出映射
│   ├── kechengbiao.md      # 2022 版课标第四学段要点
│   └── example_lesson.json
└── examples/              # 《春》真实样例（输入 + 成品）
```

---

## 六、版权与署名

- 本技能**派生自 Anthropic, PBC 的 `k12-teacher-skills`**（Apache-2.0）。
- 中国化改造部分 © 2026 涛涛。
- 以 **Apache-2.0** 同源协议发布，第三方派生声明见 `NOTICE`。
- 教材课文、课后题等受版权保护内容**一律由 AI 原创生成**，不照抄原文。
