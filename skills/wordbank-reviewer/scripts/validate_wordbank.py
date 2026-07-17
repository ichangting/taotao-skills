# -*- coding: utf-8 -*-
"""
JSON 题库审查脚本（wordbank-reviewer skill）
============================================
对带 id 的 JSON 选择题题库做全量结构 + 语义检查，输出人类可读摘要与机器可读附录。

核心检查维度（含初版遗漏的「id 唯一性」）：
  1. id 唯一性        —— 同一 id 被多题占用是致命缺陷（曾漏检导致 wm_2239 冲突静默丢题）
  2. 字段完整性       —— 必备键是否存在
  3. 选项数 == 4      —— 单选题标准
  4. 答案标签有效     —— answer ∈ {A,B,C,D} 且存在于选项
  5. target_index 正确 —— 指向字符必须等于 target_word
  6. 目标字存在性     —— target_word 必须出现在 sentence.text
  7. 选项文本重复     —— 同题内选项互异
  8. related_word 一致 —— 应等于 target_word
  9. 答案-解析一致性  —— 用「正确选项≥3字片段是否出现在解析」可靠判定（误报远低于字符重合度）
  10. 近似重复题组    —— 同句+同字+同答 但选项不同的克隆题
  11. 选项长度        —— 过长(>30)/过短(≤2) 信息级提示
  12. 解析质量        —— 过短(<6字) 信息级提示

用法：
  python validate_wordbank.py                       # 自动探测 CWD 下的 word_meaning.json 等
  python validate_wordbank.py /path/to/xxx.json     # 检查任意题库
  python validate_wordbank.py --appendix out.json   # 指定附录输出路径

退出码：有 🔴 硬伤返回 1（可接入 CI），仅 ⚪ 软标记返回 0。
依赖：Python 3.8+，仅标准库。
"""
import json
import re
import os
import sys
import argparse
from collections import Counter, defaultdict

PUNCT = set(
    list("，。、；：？！“”‘’（）《》〈〉「」『』—…·.,;:?!")
    + ['"', "'", "(", ")", "[", "]", "{", "}", "<", ">", "—", "-", "　", "\t", "\n"]
)


def chars(s):
    """去标点/空白后的有意义字符"""
    return [c for c in (s or "") if c not in PUNCT and not c.isspace()]


def norm(s):
    return re.sub(r"\s+", "", s or "")


def grams(s, n=3):
    s = norm(s)
    return {s[i:i+n] for i in range(len(s)-n+1)} if len(s) >= n else {s}


REQUIRED_TOP = {"id", "type", "difficulty", "sentence", "options", "answer", "explanation", "source", "tags"}
REQUIRED_SENT = {"text", "target_word", "target_index"}
REQUIRED_OPT = {"label", "text"}
VALID_LABELS = {"A", "B", "C", "D"}

COMMON_NAMES = ["word_meaning.json", "punctuation.json", "comparative_reading.json", "transition.json"]


def _default_path():
    for c in COMMON_NAMES:
        if os.path.exists(c):
            return c
        p = os.path.join("questions", c)
        if os.path.exists(p):
            return p
    return "word_meaning.json"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check(data):
    qs = data.get("questions", [])
    N = len(qs)
    issues = defaultdict(list)
    summary = Counter()

    # 1) id 唯一性（核心，初版遗漏）
    idc = Counter((q.get("id") for q in qs))
    dup_ids = {k: v for k, v in idc.items() if v > 1}
    if dup_ids:
        for q in qs:
            if q.get("id") in dup_ids:
                s = q.get("sentence", {})
                issues["duplicate_id"].append((q["id"], {
                    "target_word": s.get("target_word"),
                    "work": q.get("source", {}).get("work"),
                    "grade": q.get("source", {}).get("grade"),
                    "answer": q.get("answer"),
                }))
        summary["duplicate_id"] = sum(dup_ids.values())

    for q in qs:
        qid = q.get("id", "<no-id>")
        sent = q.get("sentence", {}) or {}
        text = sent.get("text", "")
        tw = sent.get("target_word", "")
        ti = sent.get("target_index", None)
        opts = q.get("options", []) or []
        labels = [o.get("label", "") for o in opts]
        opt_texts = [o.get("text", "") for o in opts]
        ans = q.get("answer", "")
        expl = q.get("explanation", "")
        rw = q.get("related_word", "")

        # 2) 字段完整性
        miss_top = REQUIRED_TOP - set(q.keys())
        miss_sent = REQUIRED_SENT - set(sent.keys())
        if miss_top or miss_sent:
            issues["missing_fields"].append((qid, f"缺顶层:{sorted(miss_top)} 缺sentence:{sorted(miss_sent)}"))
            summary["missing_fields"] += 1
        for o in opts:
            if REQUIRED_OPT - set(o.keys()):
                issues["option_missing_fields"].append((qid, f"选项{o.get('label')} 缺键:{sorted(REQUIRED_OPT-set(o.keys()))}"))
                summary["option_missing_fields"] += 1

        # 3) 选项数
        if len(opts) != 4:
            issues["option_count_ne_4"].append((qid, f"实际选项数={len(opts)}"))
            summary["option_count_ne_4"] += 1

        # 4) 答案标签有效
        if ans not in VALID_LABELS or ans not in labels:
            issues["answer_invalid"].append((qid, f"answer={ans!r} 标签集={labels}"))
            summary["answer_invalid"] += 1

        # 5) target_index 正确
        if isinstance(ti, int) and tw:
            actual = text[ti:ti+len(tw)] if 0 <= ti < len(text) else ""
            if actual != tw:
                issues["target_index_bad"].append((qid, f"句:{text!r} 目标字:{tw!r} ti={ti} 实际字符:{actual!r}"))
                summary["target_index_bad"] += 1
            positions = [m.start() for m in re.finditer(re.escape(tw), text)]
            if len(positions) > 1 and ti not in positions:
                issues["target_index_ambiguous"].append((qid, f"目标字'{tw}'出现于{positions}，ti={ti}不在其中"))
                summary["target_index_ambiguous"] += 1

        # 6) 目标字存在性
        if tw and tw not in text:
            issues["target_word_absent"].append((qid, f"目标字{tw!r}不在句:{text!r}"))
            summary["target_word_absent"] += 1

        # 7) 选项文本重复（同题内，忽略空白）
        seen = {}
        for i, t in enumerate(opt_texts):
            nt = norm(t)
            if nt in seen:
                issues["option_text_dup"].append((qid, f"选项{labels[i]}={t!r} 与 选项{labels[seen[nt]]} 重复"))
                summary["option_text_dup"] += 1
            else:
                seen[nt] = i

        # 8) related_word 一致
        if rw and tw and rw != tw:
            issues["related_word_mismatch"].append((qid, f"target_word={tw!r} related_word={rw!r}"))
            summary["related_word_mismatch"] += 1

        # 9) 答案-解析一致性（可靠片段法，低误报；仍可能因标点差异误报，仅作复核线索）
        if ans in labels and opt_texts:
            correct = dict(zip(labels, opt_texts))[ans]
            cn = norm(correct)
            en = norm(expl)
            mismatch = False
            if len(cn) >= 3:
                g = grams(correct, 3)
                if g and not any(gr in en for gr in g):
                    mismatch = True
            elif cn and cn not in en:
                mismatch = True
            if mismatch:
                issues["answer_expl_mismatch"].append((qid, f"正确答案{ans}={correct!r} 其片段未在解析出现 | 解析:{expl[:50]!r}"))
                summary["answer_expl_mismatch"] += 1

        # 11) 选项长度（信息级）
        for i, t in enumerate(opt_texts):
            L = len(chars(t))
            if L > 30:
                issues["option_too_long"].append((qid, f"选项{labels[i]} 长度{L}: {t!r}"))
                summary["option_too_long"] += 1
            elif L <= 2:
                issues["option_too_short"].append((qid, f"选项{labels[i]}={t!r}"))
                summary["option_too_short"] += 1

        # 12) 解析质量（信息级）
        if len(chars(expl)) < 6:
            issues["expl_too_short"].append((qid, f"解析={expl!r}"))
            summary["expl_too_short"] += 1

        # 10) 近似重复题组（同句+同字+同答，选项不同）
        key = (text, tw, ans)
        issues["_dupkey"].append((key, qid))

    dup_groups = defaultdict(list)
    for key, qid in issues["_dupkey"]:
        dup_groups[key].append(qid)
    issues["_dupkey"] = None
    dup_groups = {k: v for k, v in dup_groups.items() if len(v) > 1}
    if dup_groups:
        for k, v in dup_groups.items():
            issues["dup_question_group"].append((v[0], {
                "ids": v, "text": k[0][:30], "target_word": k[1], "answer": k[2]
            }))
        summary["dup_question_group"] = len(dup_groups)

    return N, dict(summary), issues, dup_ids


def print_report(N, summary, issues, dup_ids, path):
    print("=" * 64)
    print(f"题库审查：{path}")
    print(f"总题数：{N}")
    print("-" * 64)
    order = [
        ("duplicate_id", "🔴 id 冲突（同一 id 被多题占用）"),
        ("missing_fields", "🔴 字段缺失"),
        ("option_missing_fields", "🔴 选项字段缺失"),
        ("option_count_ne_4", "🔴 选项数≠4"),
        ("answer_invalid", "🔴 答案标签无效"),
        ("target_index_bad", "🔴 target_index 指向错字"),
        ("target_index_ambiguous", "🟡 target_index 未命中（目标字多次出现）"),
        ("target_word_absent", "🔴 目标字不在句中"),
        ("option_text_dup", "🔴 选项文本重复"),
        ("related_word_mismatch", "🔴 related_word≠target_word"),
        ("answer_expl_mismatch", "🔴 答案-解析不一致（需人工复核）"),
        ("dup_question_group", "🟡 近似重复题组（同句同字同答）"),
        ("option_too_long", "⚪ 选项过长(>30字)"),
        ("option_too_short", "⚪ 选项过短(≤2字)"),
        ("expl_too_short", "⚪ 解析过短(<6字)"),
    ]
    for key, label in order:
        n = summary.get(key, 0)
        flag = "✅" if n == 0 else "❌"
        print(f"  {flag} {label}: {n}")
    print("=" * 64)

    if "duplicate_id" in issues:
        print("\n【id 冲突详情】同一 id 的题：")
        by_id = defaultdict(list)
        for qid, d in issues["duplicate_id"]:
            by_id[qid].append(d)
        for qid, lst in by_id.items():
            print(f"  {qid} 被 {len(lst)} 题占用：")
            for d in lst:
                print(f"     目标字={d['target_word']!r} 课文={d['work']!r} 册次={d['grade']} 答案={d['answer']}")
        print("  → 建议：保留首个实例，其余实例重命名为 wm_<当前最大序号+1> 递增（确保全局唯一）。")

    for key in ["target_index_bad", "option_text_dup", "answer_invalid", "answer_expl_mismatch", "dup_question_group"]:
        if issues.get(key):
            print(f"\n【{key}】共 {len(issues[key])} 条，前 5：")
            for qid, detail in issues[key][:5]:
                print(f"  {qid}: {detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)}")


def dump_appendix(N, summary, issues, dup_ids):
    out = {
        "total": N,
        "summary": summary,
        "duplicate_ids": dict(dup_ids),
        "issues": {},
    }
    for k, v in issues.items():
        if k is None:
            continue
        if isinstance(v, list):
            out["issues"][k] = [list(x) for x in v]
    return out


def main():
    ap = argparse.ArgumentParser(description="JSON 题库审查（wordbank-reviewer）")
    ap.add_argument("path", nargs="?", default=_default_path(),
                    help="题库 JSON 路径（缺省自动探测 CWD 常见题库名）")
    ap.add_argument("--appendix", default="_自动审查_词语解释_附录.json",
                    help="机器可读附录输出路径")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print(f"文件不存在：{args.path}", file=sys.stderr)
        sys.exit(2)

    data = load(args.path)
    N, summary, issues, dup_ids = check(data)
    print_report(N, summary, issues, dup_ids, args.path)

    appendix = dump_appendix(N, summary, issues, dup_ids)
    with open(args.appendix, "w", encoding="utf-8") as f:
        json.dump(appendix, f, ensure_ascii=False, indent=2)
    print(f"\n机器可读附录已写入：{args.appendix}")

    hard = sum(summary.get(k, 0) for k in [
        "duplicate_id", "missing_fields", "option_missing_fields",
        "option_count_ne_4", "answer_invalid", "target_index_bad",
        "target_word_absent", "option_text_dup", "related_word_mismatch",
    ])
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
