# AI 单文件交接说明与规范提示词

> 这份文件可以**单独发给任何队友的 AI**。即使该 AI 没有自动读取仓库根目录规则，只要完整阅读本文件，也应能够找到资源、检查实时待办、遵守分支边界并沿用统一论文格式。

## A. 这个仓库怎么理解

这是一个数学建模竞赛模块化仓库。原则：

- 一个章节/问题一个独立分支；
- 一个章节只有一个正文源；
- 固定路径不随比赛过程改变；
- 每个模块都有实时待办；
- 正式数值必须可追溯到当前代码/结果文件；
- 全文只在临时 preview 中合并，不靠长期“总稿分支”日常开发；
- `main` 只保存稳定版本。

## B. 永久固定的资源路径

| 模块 | key | 正文/主资源 | 分支 |
|---|---|---|---|
| 摘要 | `abstract` | `modules/00_abstract/` | `feature/abstract` |
| 问题重述 | `restatement` | `modules/10_restatement/` | `feature/restatement` |
| 符号说明 | `notation` | `modules/11_notation/` | `feature/notation` |
| 模型假设 | `assumptions` | `modules/12_assumptions/` | `feature/assumptions` |
| 问题一 | `q1` | `modules/20_q1/` | `feature/q1` |
| 问题二 | `q2` | `modules/30_q2/` | `feature/q2` |
| 问题三 | `q3` | `modules/40_q3/` | `feature/q3` |
| 问题四 | `q4` | `modules/50_q4/` | `feature/q4` |
| 模型评价 | `evaluation` | `modules/60_evaluation/` | `feature/evaluation` |
| 参考文献 | `references` | `modules/70_references/` | `feature/references` |
| 附录 | `appendix` | `modules/80_appendix/` | `feature/appendix` |
| AI使用报告 | `ai-report` | `modules/90_ai_report/` | `feature/ai-report` |
| 跨问共享代码 | `shared` | `shared/` | `feature/shared` |
| 全文格式/标题/目录/页码 | `paper-shell` | `paper/` | `feature/paper-shell` |

其他固定位置：

```text
data/raw/                  官方原始附件，原则上不改写
data/external/             外部补充数据及来源
modules/<q>/code/          单问代码
modules/<q>/data/processed/单问派生数据
modules/<q>/figures/       正文引用图
modules/<q>/figures/editable/ Origin/Excel/AGX等可编辑图源
modules/<q>/tables/        精确结果表
modules/<q>/results/registry.csv 结果状态登记
work/tasks/<key>.md        当前模块实时待办
work/archive/              废弃模型/旧图/旧路线
output/final/              正式交付物
```

遇到“文件在哪里”时，**先查本表、`docs/RESOURCE_MAP.md`、`config/project.json` 和模块目录，不要要求队友重新提供这些固定路径。**

## C. 开工前强制动作

假设本次模块是 `q2`，必须先运行：

```bash
git status
git fetch origin --prune
git pull --ff-only
python scripts/workflow.py start q2
```

`workflow.py start` 会打印：

- 当前模块；
- 期望分支；
- 当前分支；
- 允许修改路径；
- 任务文件路径；
- 实时待办；
- 当前 Git 状态。

如果当前分支与期望分支不一致，先停止修改。

## D. 实时待办必须同步

每个模块的任务文件：

```text
work/tasks/<key>.md
```

工作过程中发现以下任何内容，都必须实时写回任务文件，而不是只留在聊天里：

- 新任务；
- 尚未完成的图/表/代码；
- 数据或模型阻塞；
- 需要复核的参数、引用、结论；
- 已完成事项。

需要人工判断时统一写：

```text
NEEDS_REVIEW / 需要复核
```

复核可由管理员或指定复核成员完成，不指定必须由某一个固定角色确认。

## E. 责任域

当前模块只修改：

```text
<该模块主路径>/**
work/tasks/<key>.md
```

例如 `q2` 只修改：

```text
modules/30_q2/**
work/tasks/q2.md
```

不要因为“方便”顺手改 Q1、摘要或全文导言区。发现跨模块问题时，在当前任务文件记录依赖，并说明需要哪个模块处理。

绝对禁止：

```text
git push --force
git reset --hard
新建第二套全文 document.tex / final.tex
新建 final2 / 真的final / 论文汇总 等并行真源
从旧稿、截图或范文手抄关键结果覆盖当前结果
```

## F. 正式结果状态

问题模块的 `results/registry.csv` 使用：

```text
DRAFT       正在计算或尚未验证
VALIDATED   已复算，等待最终检查
FROZEN      已完成规定检查，可进入正式论文
```

复核状态：

```text
NEEDS_REVIEW
CHECKED
```

正文关键数值应来自：

```text
FROZEN + CHECKED
```

模型/代码改变且影响结果后，相关结果重新回到 `DRAFT`。

## G. 论文格式不要重新设计

完整规范见 `docs/PAPER_STYLE_GUIDE.md`。最重要的固定口径如下：

- A4，四边 `25 mm`；
- 中文正文 Windows 优先宋体，英文/数字优先 Times New Roman；
- 正文小四，段首缩进2字符，行距基准1.38；
- 论文题目三号加粗居中；
- 一级标题中文序号且居中，二级 `4.1`，三级 `4.1.1`；
- 目录显示到二级标题；
- 正文从问题重述重新计第1页；
- 参考文献、附录、AI使用报告分别另起一页；
- 三线表，浅蓝表头，不画纵线；
- 单个小图 `0.44\textwidth`；两个小图总宽 `0.88\textwidth`；Origin合成双面板图整张 `0.88\textwidth`；总体流程图约 `1.0\textwidth`；机理图通常 `0.70\textwidth`；
- 图题、表题由LaTeX生成，不把大标题做进图片；
- 伪代码统一使用 `algorithm2e`，表达算法机制，不复制Python；
- 普通公式尽量行内，核心模型/约束/结果才单独编号；
- 不在章节文件里重定义字体、页边距、标题格式。

若任务只是写 Q2，而你认为字体不合适：**不要直接改字体**，记录为 `paper-shell` 需要处理的事项。

## H. 推荐的单问写作结构

根据题意选用，不机械堆标题：

```text
问题描述与分析
→ 总体流程图
→ 必要预备/数据处理
→ 模型建立
→ 模型汇总
→ 模型求解
→ 结果与分析
→ 对主要不确定性的检验
```

优化问题必须明确：决策变量、目标函数、约束、模型汇总。

摘要按“任务--准备--模型--算法--结果--解释”组织每问，再压缩为约4--6行。

## I. 图表规则

每张正式图都必须能回答：

1. 数据来自哪里？
2. 对应哪个当前代码/表格？
3. 可编辑图源在哪里？
4. 正文用它说明什么？

可编辑图源统一放 `figures/editable/`。如果用 Origin 完成最终图，不要为了省事再用 Python 粗糙重画替代正式图；Python 可以用于产生数据和预览。

## J. 结束本轮前强制动作

```bash
python scripts/workflow.py finish <module-key>
git diff
git status
```

必须同步更新任务文件，然后只 `git add` 明确需要提交的文件。结束汇报至少包含：

- 本轮改了什么；
- 结果/图/代码的准确路径；
- 剩余待办；
- 阻塞项；
- 需要复核项。

---

# 可直接复制给 AI 的规范提示词

```text
你正在 CUMCM 模块化 Git 仓库中工作，本次模块是 <模块key>，任务是：<本次任务>。

开始任何修改前必须：
1. 完整阅读当前提供的《AI 单文件交接说明与规范提示词》。如果仓库可访问，再读 AGENTS.md、README.md、docs/RESOURCE_MAP.md、docs/PAPER_STYLE_GUIDE.md。
2. 运行 `python scripts/workflow.py start <模块key>`，读取当前分支、允许路径、固定资源位置和实时待办。
3. 读取并持续维护 `work/tasks/<模块key>.md`。新增任务、阻塞、风险、完成项、需要复核项必须实时写回，不只留在聊天里。
4. 遇到“不知道文件在哪里”时先查固定资源地图、config/project.json和模块目录，不向队友重复询问已经固定的路径。
5. 只修改当前模块责任域。跨模块问题记录依赖，不直接覆盖别的章节。
6. 正式数值必须能追溯到当前代码/结果文件；不得从旧稿、截图、范文或历史JSON手抄覆盖。
7. 需要人工判断的内容统一标记 NEEDS_REVIEW/需要复核，由管理员或指定复核成员处理，不绑定某个固定角色。
8. 沿用仓库既定论文格式；非 paper-shell 任务不得重定义字体、页边距、标题、目录或全局图表样式。
9. 不得 force push、reset --hard，不得创建第二套全文TeX或随意汇总目录。

结束前必须：
1. 更新实时待办；
2. 运行 `python scripts/workflow.py finish <模块key>`；
3. 检查 git diff，确认无责任域外修改；
4. 汇报本轮修改、准确文件路径、剩余待办、阻塞和需要复核项。
```
