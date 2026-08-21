#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def tex_files():
    return list((ROOT / "modules").glob("*/paper/*.tex")) + list((ROOT / "paper").glob("*.tex"))


def read(path: Path):
    return path.read_text(encoding="utf-8", errors="replace")


def prose_length(text: str) -> int:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\(?:textbf|emph|mathrm|operatorname)\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", "", text)
    text = re.sub(r"[$\\{}_^~]", "", text)
    return len(re.sub(r"\s+", "", text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post-build", action="store_true")
    a = ap.parse_args()

    errors = []
    warns = []
    labels = defaultdict(list)
    all_tex = {}

    module_tex = list((ROOT / "modules").glob("*/paper/*.tex"))
    forbidden_global_style = (
        r"\geometry{",
        r"\setmainfont",
        r"\setCJKmainfont",
        r"\renewcommand\section",
        r"\renewcommand{\baselinestretch}",
    )

    for p in tex_files():
        t = read(p)
        all_tex[p] = t
        for marker in CONFLICT_MARKERS:
            if marker in t:
                errors.append(f"{p.relative_to(ROOT)}: 残留 Git 冲突标记 {marker}")
        for token in ("??", "[?]", "TODO", "FIXME"):
            if token in t:
                warns.append(f"{p.relative_to(ROOT)}: 发现 {token}")
        for x in re.findall(r"\\label\{([^}]+)\}", t):
            labels[x].append(p)

        # 竞赛正文中过长的纯文字段落通常意味着信息没有被公式、分点或图表组织。
        if "modules/80_appendix" not in str(p).replace("\\", "/"):
            for idx, para in enumerate(re.split(r"\n\s*\n", t), 1):
                if any(x in para for x in ("\\begin{equation", "\\begin{align", "\\begin{figure", "\\begin{table", "\\begin{algorithm", "\\begin{lstlisting")):
                    continue
                if para.lstrip().startswith(("\\section", "\\subsection", "\\subsubsection", "%")):
                    continue
                n = prose_length(para)
                if n >= 260:
                    warns.append(
                        f"{p.relative_to(ROOT)}: 第 {idx} 个文字段约 {n} 字，建议分点/分段或用公式组织"
                    )

    for p in module_tex:
        t = all_tex[p]
        for token in forbidden_global_style:
            if token in t:
                errors.append(f"{p.relative_to(ROOT)}: 章节正文不得重定义公共样式 {token}")

    for k, ps in labels.items():
        if len(ps) > 1:
            errors.append(f"重复 label {k}: " + ", ".join(str(p.relative_to(ROOT)) for p in ps))

    # 图表放入正文后必须至少有一次文字引用，避免“孤立图表”。
    joined = "\n".join(all_tex.values())
    for label, ps in labels.items():
        if not (label.startswith("fig:") or label.startswith("tab:")):
            continue
        refs = len(re.findall(rf"\\(?:ref|autoref)\{{{re.escape(label)}\}}", joined))
        if refs == 0:
            warns.append(f"{ps[0].relative_to(ROOT)}: {label} 未被正文引用或解释")

    for reg in ROOT.glob("modules/*/results/registry.csv"):
        with reg.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if not row.get("result_id"):
                    continue
                if row.get("used_in_paper", "").strip().lower() in {"yes", "true", "1", "y"}:
                    if row.get("status") != "FROZEN" or row.get("review_state") != "CHECKED":
                        errors.append(
                            f"{reg.relative_to(ROOT)}: {row['result_id']} 已用于正文但不是 FROZEN+CHECKED"
                        )

    maintex = read(ROOT / "paper/main.tex")
    required_main = (
        r"\input{settings.tex}",
        r"\ifshowtoc",
        r"\tableofcontents",
        r"\pagenumbering{arabic}",
        r"\setcounter{page}{1}",
    )
    for token in required_main:
        if token not in maintex:
            errors.append(f"paper/main.tex 缺少公共结构: {token}")

    if maintex.count(r"\clearpage") < 4:
        errors.append("paper/main.tex 分页不足：参考文献、附录、AI使用报告应各自另起一页")

    settings = ROOT / "paper/settings.tex"
    if not settings.exists() or "\\newif\\ifshowtoc" not in read(settings):
        errors.append("paper/settings.tex 缺少目录开关")

    abstract = ROOT / "modules/00_abstract/paper/abstract.tex"
    if abstract.exists() and re.search(r"\\section\*?\{", read(abstract)):
        errors.append("摘要模块不应自行创建 section；摘要标题由公共模板负责")

    appendix = ROOT / "modules/80_appendix/paper/appendix.tex"
    if appendix.exists() and re.search(r"\\subsection\{", read(appendix)):
        errors.append("附录不应使用有编号 subsection，避免目录出现错误章节号")

    if not (ROOT / "modules/20_q1/paper/q1_algorithm.tex").exists():
        errors.append("问题一伪代码示例 q1_algorithm.tex 缺失")

    if a.post_build:
        log = ROOT / "paper/main.log"
        if log.exists():
            log_text = read(log)
            if "Overfull \\hbox" in log_text:
                warns.append("LaTeX 日志存在 Overfull \\hbox")
            if "undefined references" in log_text.lower() or ("citation" in log_text.lower() and "undefined" in log_text.lower()):
                errors.append("LaTeX 日志存在未解析引用或文献引用")

    for w in dict.fromkeys(warns):
        print("[WARN]", w)
    for e in dict.fromkeys(errors):
        print("[FAIL]", e)
    if not errors:
        print("[PASS] final preflight")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
