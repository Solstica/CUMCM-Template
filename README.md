# CUMCM 通用协作与论文模板 v1

面向数学建模竞赛的三人/多人 + AI 协作模板。它不只提供 Git 分支和 worktree，也已经包含团队上一场正式论文验证过的**标题、摘要、目录、正文标题层级、字体、页边距、行距、公式、三线表、插图尺寸、伪代码、代码附录、评价、参考文献和 AI 使用报告样式**。

核心原则：**单一真源、章节独立、固定路径、任务可见、结果可追溯、格式统一、全文临时集成、稳定版本再进入 main。**

## 1. 新比赛开局

```bash
# 例：三问题赛题
python scripts/set_questions.py 3 --name 2026CUMCM-A

git add config/project.json paper/main.tex
git commit -m "chore: initialize contest structure"
git push

# 创建所有活动章节的独立分支和 worktree
python scripts/bootstrap_worktrees.py --push
```

模板默认按三问展示；如赛题为1--4问，使用 `set_questions.py` 调整。

## 2. 直接编译模板看格式

```bash
cd paper
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

默认应得到一份可直接删改的示例论文：

```text
第1页  标题 + 摘要
第2页  目录
正文第1页起  问题重述、符号说明、模型假设
问题一  完整结构示例：流程图、公式、模型汇总、伪代码、表格、双小图、检验
问题二/三  只保留一级标题
后续  模型评价、参考文献、附录代码示例、AI使用报告
```

目录可在 `paper/settings.tex` 切换：

```tex
\showtoctrue
% \showtocfalse
```

完整论文格式规范：`docs/PAPER_STYLE_GUIDE.md`。

## 3. 永久固定的资源路径

| 模块 | 唯一正文/资源位置 | 分支 |
|---|---|---|
| 摘要 | `modules/00_abstract/` | `feature/abstract` |
| 问题重述 | `modules/10_restatement/` | `feature/restatement` |
| 符号说明 | `modules/11_notation/` | `feature/notation` |
| 模型假设 | `modules/12_assumptions/` | `feature/assumptions` |
| 问题一 | `modules/20_q1/` | `feature/q1` |
| 问题二 | `modules/30_q2/` | `feature/q2` |
| 问题三 | `modules/40_q3/` | `feature/q3` |
| 问题四 | `modules/50_q4/` | `feature/q4` |
| 模型评价 | `modules/60_evaluation/` | `feature/evaluation` |
| 参考文献 | `modules/70_references/` | `feature/references` |
| 附录 | `modules/80_appendix/` | `feature/appendix` |
| AI使用报告 | `modules/90_ai_report/` | `feature/ai-report` |
| 跨问共享代码 | `shared/` | `feature/shared` |
| 标题/目录/页码/公共样式 | `paper/` | `feature/paper-shell` |
| 官方原始附件 | `data/raw/` | 不随章节移动 |
| 外部补充数据 | `data/external/` | 不随章节移动 |
| 模块待办 | `work/tasks/<模块>.md` | 跟随对应模块分支 |
| 正式交付物 | `output/final/` | 稳定集成后生成 |
| 废弃路线 | `work/archive/` | 只读归档 |

更详细的地图见 `docs/RESOURCE_MAP.md`。固定位置不要反复向队友询问；先查资源地图或运行 `workflow.py start`。

## 4. 问题模块内部结构

```text
modules/30_q2/
├─ paper/q2.tex
├─ code/
├─ data/processed/
├─ figures/
│  └─ editable/
├─ tables/
└─ results/registry.csv
```

问题一另提供 `paper/q1_algorithm.tex` 作为伪代码格式示例。跨两个及以上问题共用的数值内核进入 `shared/`，不要复制多份。

## 5. 分支规则

长期活动分支按责任域，不按人名：

```text
main
├─ feature/shared
├─ feature/abstract
├─ feature/restatement
├─ feature/notation
├─ feature/assumptions
├─ feature/q1
├─ feature/q2
├─ feature/q3
├─ feature/q4
├─ feature/evaluation
├─ feature/references
├─ feature/appendix
├─ feature/ai-report
└─ feature/paper-shell
```

`main` 只保存稳定版本。不要创建 `feature/张三`、`final2`、`真的final` 或第二套 `document.tex`。

## 6. 每次开工/收工

开始：

```bash
git status
git fetch origin --prune
git pull --ff-only
python scripts/workflow.py start <模块key>
```

结束：

```bash
python scripts/workflow.py finish <模块key>
git diff
git add <明确需要提交的文件>
git commit -m "feat(q2): 完成……"
git push
```

`workflow.py` 会显示固定资源位置和实时待办，并在结束时检查责任域外修改及“改了正文却没同步待办”的情况。

## 7. 实时待办

每个模块都有：

```text
work/tasks/<key>.md
```

新增任务、阻塞、风险、需要复核项和完成项必须实时写入，不只留在聊天中。

需要人工判断的内容统一标记：

```text
NEEDS_REVIEW / 需要复核
```

检查可由管理员或指定复核成员完成，不绑定某个固定角色。

## 8. 结果状态

问题模块 `results/registry.csv` 使用：

- `DRAFT`：正在计算/尚未验证；
- `VALIDATED`：已复算，等待最终检查；
- `FROZEN`：已完成规定检查，可进入正式论文。

另有 `review_state`：`NEEDS_REVIEW` / `CHECKED`。

正文关键数值应来自 `FROZEN + CHECKED`。模型或代码改变且影响结果后，受影响结果重新回到 `DRAFT`。

## 9. 临时全文 Merge Preview

```bash
python scripts/preview_merge.py
```

流程：

```text
fetch origin
→ origin/main 创建 detached 临时 worktree
→ 按配置 merge 各活动章节分支
→ paper-shell 最后合入
→ final_preflight
→ XeLaTeX/latexmk 编译
→ 打开 PDF
```

它不会生成长期汇总分支，也不会修改正式 feature 分支或 main。

清理：

```bash
python scripts/preview_merge.py --clean
```

## 10. 论文公共格式

除非比赛官方要求发生变化，默认不重新设计：

- A4，四边25 mm；
- 中文正文 Windows 优先宋体，英文/数字优先 Times New Roman；
- 正文小四、段首2字符、1.38行距基准；
- 题目三号加粗居中；
- 一级标题中文序号居中；二级 `4.1`；三级 `4.1.1`；
- 三线表 + 浅蓝表头；
- 单小图0.44正文宽，双图总宽0.88，Origin合成双面板整张0.88，流程图约1.0，机理图通常0.70；
- `algorithm2e` 伪代码；
- 参考文献、附录、AI使用报告各自另起一页；
- 正文从问题重述开始第1页。

详见 `docs/PAPER_STYLE_GUIDE.md`。格式调整只在 `feature/paper-shell` 完成。

## 11. 给队友 AI 的单文件说明

如果队友使用的 AI 不能自动读取仓库规则，直接把下面这个文件单独发给它：

```text
docs/AI_HANDOFF_PROMPT.md
```

该文件自身包含：

- 固定资源路径；
- 分支/责任域；
- 实时待办要求；
- 结果状态；
- 论文版式核心规范；
- 图表尺寸；
- 开工/收工命令；
- 可直接复制使用的规范提示词。

支持仓库级指令的 AI 还会读取根目录 `AGENTS.md` 和 `.github/copilot-instructions.md`。

## 12. AI 规范提示词

简化入口：

```text
你正在 CUMCM 模块化 Git 仓库中工作，本次模块是 <模块key>，任务是：<任务>。
开始前完整阅读 AGENTS.md、README.md、docs/RESOURCE_MAP.md、docs/PAPER_STYLE_GUIDE.md，并运行 `python scripts/workflow.py start <模块key>`。
必须围绕 `work/tasks/<模块key>.md` 的实时待办推进，新任务/阻塞/需要复核项实时写回任务文件。
固定资源路径先自行查询，不要求队友重复提供。
只修改当前模块责任域；正式数值必须可追溯到当前代码/结果文件；非 paper-shell 任务不得重定义论文公共格式；需要人工判断统一标记 NEEDS_REVIEW；禁止 force push/reset-hard/第二套全文TeX。
结束前更新待办，运行 `python scripts/workflow.py finish <模块key>`，检查 git diff，并汇报修改、准确路径、剩余待办和需要复核项。
```

更完整版本直接使用 `docs/AI_HANDOFF_PROMPT.md`。

## 13. 检查层级

1. `scripts/structure_guard.py`：仓库结构、责任域和第二套全文源；
2. `scripts/final_preflight.py`：引用、标签、结果状态、LaTeX日志；
3. 人工检查：模型合理性、结果解释、图表视觉、论文表达。

机器检查防止灾难性错误，不替代人工判断。
