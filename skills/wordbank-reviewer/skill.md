---
name: wordbank-reviewer
description: |
  审查 JSON 格式的古汉语/文言文选择题题库（及通用带 id 的 JSON 题库）。当任务涉及审查 word_meaning.json、punctuation.json、comparative_reading.json、transition.json 等题库 JSON 的 id 唯一性、target_index 准确性、选项重复、答案-解析一致性，或对齐派生文件（审查版 MD / data.js）时触发。This skill should be used when reviewing, linting, or fixing a JSON question bank for a Chinese classical-language learning app.
version: 1.0.0
author: 涛涛（万景涛）
license: MIT
homepage: https://taotao.site/skills/wordbank-reviewer
---



# 题库审查（wordbank-reviewer）

## 目的
对古汉语/文言文选择题题库的 JSON 源文件做全量结构 + 语义审查，捕获会静默破坏下游（前端按 id 建索引）的致命缺陷，并给出可执行的修复 SOP。源自「文言智学」TRAE AI 大赛项目，方法可推广到任意带 `id` 的 JSON 题库。

## 何时使用
- 用户要求「审查题库」「检查 word_meaning.json」「题库有没有问题」「lint 一下题库」。
- 修改题库 JSON 后需要复验。
- 派生文件（审查版 MD、data.js）与源 JSON 不一致时。
- 出现「重复题」「缺题」「答案错位」「加点字标错」等 textbook 现象。

## 核心检查维度（scripts/validate_wordbank.py，仅标准库，Python 3.8+）
1. **id 唯一性**（最致命，曾漏检）→ 同源 id 重复会在前端静默丢题。
2. 字段完整性（顶层 + sentence + option 必备键）。
3. 选项数 == 4。
4. 答案标签 ∈ {A,B,C,D} 且存在于选项。
5. target_index 正确（指向字符 == target_word）。
6. 目标字存在性（target_word 必须出现在 sentence.text）。
7. 选项文本重复（同题内互异）。
8. related_word == target_word。
9. 答案-解析一致性（可靠片段法）。
10. 近似重复题组（同句+同字+同答，选项不同 → 克隆题嫌疑）。
11. 选项长度（过长 >30 / 过短 ≤2，信息级）。
12. 解析长度（<6 字，信息级）。
13. **语境-答案一致性（语义维度，wm_0428 教训）**：仅查结构/文字一致抓不到「句-答语境错配」。须把多义字每题 (句片段, 答案义项) 并列，人工审定「句中靶字实义 ≈ 答案义项」；明显错配（如 cloud 句配语气词、具体物象句配抽象虚词义）即硬伤。复用 `audit_context_*.py`（矛盾对/非语例/专名误配/多义字组明细）产出候选。

脚本退出码：有 🔴 硬伤返回 1（可接入 CI / 串联脚本），仅 ⚪ 软标记返回 0。

## 使用方式
```bash
cd <题库所在目录>
python <skill>/scripts/validate_wordbank.py                # 自动查找 word_meaning.json / punctuation.json 等
python <skill>/scripts/validate_wordbank.py 路径/xx.json    # 指定文件
```
脚本输出人类可读摘要 + 机器可读附录（默认输出到被查文件同目录的 `_自动审查_词语解释_附录.json`）。

## 已知陷阱（务必人工判断，勿自动改）
- **id 冲突**：同一 id 被多题占用（如 `wm_2239` 同时是「君」七上题和「要」八下通假字题）。修复＝保留首个实例，其余重命名为 `wm_<当前最大序号+1>` 递增。务必与已删除 id 造成的空洞错开，保证全局唯一。脚本会列出每个冲突 id 及其所属课文/目标字/答案，据此决策。
- **答案-解析一致性误报极高**：古籍释义短，且正确选项与解析常因标点/括号差异（「由，自」vs「由、自」、「知道，了解」vs「知道、了解」）导致 3 字片段不匹配。**此类标记只作人工复核线索，绝不自动改写答案或解析**。验证方法：抽看若干条，确认答案文字本身正确即可。
- **target_index 错位**：目标字在句中时，用 `sentence.text.find(target_word)` 安全重写；目标字多次出现时取首次出现（古文惯用义通常首次即正确）。
- **克隆题张冠李戴**：干扰项来自另一字（如 target=足，但干扰项是「见」的义项）。修复＝改干扰项为 target_word 的正确义项，或删除冗余克隆（保留正确的同句题）。

## 流程纪律坑（比结构 bug 更易翻车，来自逐册审查复盘）

以下坑不来自 JSON 结构，而来自「人 + 工具协作」的纪律缺失；任一踩中都会导致改错对象或误判工具。详见 `TRAE AI创造力大赛/04-核心数据库/questions/review/题库审查踩坑经验_v1.0_2026-07-09.md`。

- **坑一 手抄 id 串格 → 幻影项（最高危）**：把 dump/JSON 的 id 手抄进问题清单时极易看错行串格（实例：`wm_1890` 实为「郭」，被抄成「诚 / 诚宜开张圣听」幻影项）。**规避**：问题清单 id 一律由 `gen_problem_skeleton.py` 直抽（id/靶字/句/现答 100% 来自 JSON），人工只在「判定」列手写 Tier；落盘走 `_common.resolve(靶字, 句子片段)` 实查真实 id，**绝不用清单 id 写盘**；`apply_patch.py` 的断言保护会在串格时中止写盘。铁律：**禁止手抄 id**。
- **坑二 误判工具缺陷**：一次失败的内部比对曾误报 `dump_volume.py`「全册句首截断」，未亲读文件就写进结论，后证伪（四册 dump 与 JSON 的 `句：` 行 0 不一致）。**规避**：说「工具坏了」前，必须先读实际产物文件 + 写脚本逐条比对坐实；不轻信对话摘要里的「发现」；错了**明文撤回**。
- **坑三 同簇错误只标部分 → 漏标真错**：同字多篇复用同一错误答案签名（如「诚」字典首义误用于「此诚危急存亡之秋也」）初扫只标部分，漏 `wm_1858`/`wm_1872`。**规避**：锁定一类错误后用「已知错误答案签名」批量回捞全册 `answer` 命中且不在已标记集的题，逐判语境；一词多义逐篇核对，不假设同字同错。
- **坑四 dump 是视图 + 弯引号陷阱**：dump 的 `句：` 行与 JSON 一致（已证），可读但**权威源永远是 word_meaning.json**，核验/落盘依据回查 JSON；句含中文弯引号 `""`（U+201C/U+201D）或「」时，`resolve` 的 `sentence_contains` 子串须用**实际字符**，勿写成 `「」` 或直引号，否则匹配失败。
- **坑五 底稿陈旧视图 → 误判 tag/答案（本次九下实战暴露）**：初读 `gen_problem_skeleton.py` 生成的底稿时，`wm_1945`（被/通"披"）的「通假字」tag 被**陈旧视图漏显**（该 tag 早前已由他处流程加过），一度误判为"缺 tag"并拟加补丁；`apply_patch.py --dry` 报 `add_tag 已存在` 拦住无谓写盘，重跑生成器确认 JSON 本就正确。**规避**：据底稿判定 tag/答案后、落盘前，**必须以 JSON 当前态二次核对**（或重跑生成器）；底稿与 JSON 对不上立即重跑生成器，不信任旧文件。
- **坑六 同句跨册 `resolve` 子串歧义 + `data.js` 尾部 const 致 `load_datajs` 失效（wm_1886 实战暴露）**：① 同一句「既加冠，益慕圣贤之道」在九下 wm_1886 与课外 wm_1036/wm_1038 三题同现（靶字皆「既」），且课外题句把该短语包进更长句（带「宋濂《送东阳马生序》：」前缀+句号），纯子串匹配无法唯一定位 wm_1886（`resolve` 会报「匹配到 3 题」中止）。**规避**：patch 补 `grade` 参数（如 `"grade":"九下"`）消歧——三题 grade 不同（九下 vs 课外），grade 一填即唯一。resolve 唯一性自检时，须把「同句跨册」列为必查项（同句多题时优先用 grade 而非加更长锚点）。② `data.js` 在 `const QUESTIONS_DATA = [...];` 之后还有 `const ABOUT_MARKDOWN = \`...\``，`_common.load_datajs` 的贪婪正则 `const QUESTIONS_DATA = (.*);` 会把尾部 const 也吞进数组字符串，json.loads 报「Extra data: line 1 column ...」。**规避**：双端复验改用非贪婪 `re.search(r'const QUESTIONS_DATA = (\[.*?\]);', data, re.S)` 只取数组；这是复验脚本问题，不影响 build 产物本身。

- **语义盲区（wm_0428 级，比结构 bug 更隐蔽）**：分册审查与 `validate_wordbank.py`(12维)/`audit_scan.py` 都只查「答案文字↔解析文字」一致；若答案义项本身合法（如「云」确有语气词义）且与解析文字自洽，机器全绿，但错在「答案义项 ≠ 句子语境义」（cloud 句配语气词）。根因是批量生成时「义项轮流分配 + 句子另选」无语境绑定约束。**规避**：把「语境-答案一致性」列为独立审查维度，多义字组逐题核对句中实义 vs 答案义；并优先重构 `source.work="古汉语字典"` 的 139 道非语例题（sentence 为字典释义框，脱离语境）。参考 `audit_context_*.py` + `docs/data/审查报告_全库词语解释_语境一致性_v1.0_2026-07-11.md`。

## Deeper pass 工作流（跨义项串线 + 绕开无关结构中止）

用于「全量深度审查 + 批量修正」场景（如 课外 1242 题 deeper pass），目标是捕获**跨义项串线 / 古今字異體字混淆**导致的「答案义项与句子语境不匹配、且正确义项不在四选项中」这类集群型硬伤（非孤立，常是整组复制粘贴）。

- **三层启发式定位**（先扫后核）：
  1. 全量子串比对：答案义项文本是否出现于句中（初筛）。
  2. 按字聚类「复制粘贴签名」：同字多题共答同一义项标签 → 锁定系统性错位（从/有/利 三组最典型）。
  3. 无《》字典条目精确过滤：句无真实引文且答案义项不在句中 → 可靠命中字典条目型错位（避开引文型误报）。
  4. 对全部候选**逐题调出完整选项集人工核定**，区分「硬错 / 结构残缺(删除) / 边界」。
- **修正模式（受工具约束）**：`apply_patch.py` 仅支持 `add_tag/del_tag/set_answer_text/set_option_text/replace_expl`，**无「改答案字母 / 增删选项 / 删除整题」op**。硬错（正确义项不在四选项）→ 用 `set_answer_text` 把**当前答案项（字母不变）文本直接替换为正确义项**，干扰项仍为另 3 个错义项（恰好当干扰）；再 `replace_expl` 同步解析。结构残缺（句为注意/辨/学习提示/发音表等非文言文用例）→ 单独删题。
- **精确抽取 old 的生成器模式**（杜绝手抄错位）：写 `gen_*.py` 从 `word_meaning.json` **精确读取**每题当前答案项文本 + 解析原文，填入 `set_answer_text`/`replace_expl` 的 `old`；`new` 由你核定。这样断言 `o['text']==old` 必然命中，不会因为手抄错一个标点整批中止。
- **resolve 唯一性自检**（落盘前必跑）：用 `apply_patch` 同款 `resolve(tw, sc, qs, grade)` 逻辑，对每条款预跑，暴露「锚点非唯一（同句多题）」与「弯引号误配（文件用 `""` 弯引号，sc 写了直引号 `"` 则匹配不到）」。实例：wm_0389 的 `从小丘西行百二十步` 同时命中正确题 wm_0376（答「介词。由，自」）与错配比 wm_0389，须加 `1. “` 前缀锚点消歧。
- **⚠️ 绕开全量结构自检的无谓中止**：`sync_and_verify.py` 的 ①结构硬伤自检是**全量**性质，一旦撞上**本次未触碰的既有 🔴 硬伤**（如 wm_0507：七下《孙权劝学》`target_index=4` 指向逗号，正确应为 5（`见` 在 index 5），偏一位），即整体中止，挡住 ②④ 重建与双端比对。正确做法：**不依赖 sync_and_verify 全量**，改跑针对性验证：① 直接 subprocess 调 `build_dictionary.py` + `export_md.py` 重建；② 只对**本次 patch 清单**做 JSON↔data.js 双端比对（逐条 PASS）+ 删除项双端缺席检查 + (a) 阶段 7 道回潮检查。既有 🔴 硬伤按权威源修改纪律交用户确认，不擅自改。
- **删题专用脚本**：`apply_patch` 无删除 op，写 `del_*.py`：先备份（带时间戳）→ 断言待删 id 全部存在 → 移除 → 断言总数减 N → 写回。

## 标准 SOP（每次改题库后必跑）
0. 出底稿（防坑一）：跑 `gen_problem_skeleton.py <册>` 生成**直抽底稿**（id/靶字/句/现答 100% 来自 JSON），逐句读；据「错误答案签名」回捞同簇漏标（防坑三）；人工只在「判定」列手写 Tier，**禁止手抄 id**。
1. 审查：跑 `validate_wordbank.py`，看 🔴 项；必要时读附录 JSON 逐条核对。
2. 修复：按上节陷阱指引处理硬伤；落盘走 `_common.resolve(靶字, 句子片段)` 实查真实 id，绝不用清单 id 写盘；`apply_patch.py` 带断言，全过才写盘。
3. 复验：再跑脚本，确认 🔴 全 0（exit 0）。
4. 重导派生文件（禁止手工编辑，历史曾因手工编辑致 90% 答案错误）：
   - 审查版 MD + 子题库：由 `export_md.py` 从 JSON 重新生成。
   - `data.js`（Demo 内嵌数据）：由 `build_dictionary.py`（项目**唯一**能写 data.js 的脚本，产物含 `meanings`/`source` 结构化字段、例句带出处分行）从 JSON 重新生成。
5. 最终对齐校验：确认 `data.js` 中 `wm_` id 集合与 JSON 源完全一致（出现数 == 唯一数 == 题数）。

## 审查前检查清单（默写）
- [ ] `gen_problem_skeleton.py <册>` 出直抽底稿，**id 不手抄**
- [ ] 逐句读，按「错误答案签名」**回捞同簇漏标**
- [ ] 落盘用 `(靶字, 句子片段)` 定位，绝不用清单 id；弯引号用**实际字符**
- [ ] apply 前先**备份** `word_meaning.json`，再 `--dry` 跑断言，全过再真写
- [ ] `validate_wordbank.py` 🔴 全 0；`data.js`/MD 已重生成且与源对齐
- [ ] 疑似工具缺陷：**先亲读文件 + 脚本逐条比对坐实**，再下结论；错了明文撤回
- [ ] 据底稿判定后、**落盘前回查 JSON 当前态**（防底稿陈旧视图坑五）；不信任旧底稿文件

## 跨题库
文言智学项目含四类题库（word_meaning / punctuation / comparative_reading / transition），均由 `build_dictionary.py` 合并进 `data.js`。任一题库的 id 冲突都会在 `data.js` 层暴露，建议定期全部审查。
