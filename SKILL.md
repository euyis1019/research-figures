---
name: research-figures
description: Publication-quality matplotlib figures for ML papers and technical blogs, in one fixed house style (tinted panels, white grid, Computer Modern, red/blue semantic families, strict row alignment). Use when drawing any data figure (training curves, ablations, loss landscapes, theory-vs-simulation, heatmaps, leaderboards, schedules) or a schematic for a paper or blog post, or when restyling existing figures. 画论文 / 博客配图、重画论文里的数字、统一图风格时使用。
---

# research-figures：论文与技术博客配图

数据图一律用 matplotlib 加本 skill 的 `figkit/style.py`，不用 seaborn 或 plotly，也不手调 rcParams。本文与通用 dataviz 建议冲突时，以本文为准。

风格参照两篇论文正文里的图：Hägele et al. 2024（arXiv 2405.18392）和 Song et al. 2025（arXiv 2507.09846），即浅色底、白网格、黑色全框、Computer Modern 字体、红蓝两个语义色族。`templates/figs/gallery.png` 是全部模板的效果图。

本 skill 目录下的文件：

| 路径 | 内容 |
|---|---|
| `figkit/style.py` | 样式模块，用时复制到项目里 |
| `templates/t0_skeleton.py` | `make_figs.py` 骨架 |
| `templates/t1…t13_*.py` | 13 类图的完整可运行示例，用合成数据，可直接跑 |
| `templates/make_gallery.py` | 跑全部模板并拼出 gallery |
| `references/diagrams.md` | 框图（架构、流程）的做法：matplotlib / TikZ / Mermaid / Gemini 提示词 |

## 0. 两条路：数据图还是示意图

- **有数值坐标轴 → 数据图**，按第 1–9 节做。
- **有框、有箭头 → 示意图**。简单的分层、状态、调度示意，用 matplotlib 画（T7、T8），风格与数据图一致。复杂的架构图或流程图，读 `references/diagrams.md`，按“TikZ → Mermaid 草图 → Gemini 生成”的顺序选工具。

## 1. 先从上下文里抽内容

用户给的通常不是现成的规格，而是一段正文、一张结果表、一个 CSV，或一句“给这节配张图”。动手前先回答下面几个问题，写成两三行注释放在 `fig_*()` 开头。

1. **这张图要读者看出什么？** 用一句话写下来；后面的图注第一句、面板标题、高亮色都服务于这句话。
2. **比较的是什么？** 方法、配置、阶段放类别轴或分色；指标放数值轴；有步数或时间就用折线。
3. **哪个是主角？** 本文的方法或结论用 `BLUE`，基线和对照用 `REDS` 或 `GRAY`。全图只留一个最饱和的蓝。
4. **数字从哪来？** 论文表格、实验日志还是 toy 模拟；图注最后要写明来源。数字必须和正文一致（见 §6）。
5. **几个面板？** 一个面板只回答一个问题。两到三个问题就并排放，用 (a)(b)(c) 标出。

## 2. 选图：数据形状 → 模板

| 数据形状 | 图 | 模板 |
|---|---|---|
| 随步数变化的噪声量加均值，或几个随旋钮变化的曲线 | 1×3 曲线行：噪声轨迹 + 滑动均值 + 事件线；最优点 + 直接标注；log-log + 参考线 | T1 |
| 两个模型之间插值的 loss，与端点连线比较 | 插值面板：曲线在连线下方填蓝（收益），上方填红（barrier） | T2 |
| 2-D loss 地形上的一条轨迹 | 地形图 + 普通轴同行（等比例） | T3 |
| 一批对象在处理前后各有一个值 | 斜率图 + 排斥标签 | T4 |
| 重画论文表格：少量类别各一个值；分数随某个数变化 | 柱状（家族浅→深）+ 带基线的折线 | T5 |
| 少量有序类别各一个值，旁边是距离很远的两组点 | 棒棒糖 + 断轴点图，跨面板两行文字对齐 | T6 |
| 学习率调度、窗口、分叉 | 调度示意，共享 y | T7 |
| 若干层结论各自的证据状态 | 分层 / 状态条 | T8 |
| 跨好几个数量级的类别值，分两区 | 对数类别点图 + 分区 | T9 |
| 闭式解与模拟对照 | 理论虚线 + 模拟点（带误差棒）+ 极限参考线 | T10 |
| 阶梯 / 分段函数，旁边是几种方法随 K 的对比 | 阶梯图 + log-log 方法对比，右侧 y 轴 | T11 |
| N 个方法 × M 个基准；单指标排行 | 分组柱 + 横向排行榜，“ours” 用蓝 | T12 |
| 矩阵（层 × 设置、混淆矩阵、注意力）；两个连续量的相关 | 标注热力图（有符号用发散色）+ 散点拟合 | T13 |

没有对应模板时按下面的优先级选：有步数轴 → 折线；N 方法 × M 基准 → 分组柱；单一排名 → 横向条；两个连续量 → 散点；方阵 → 热力图；构成比例 → 堆叠横条（不用饼图）；分布 → 箱线或小提琴，配色按 §4。

## 3. 规格速查

| 项目 | 取值 |
|---|---|
| 字体 | Computer Modern（cmr10 + mathtext cm），STIX 补缺字；不开 usetex |
| 字号 | 正文 / 轴标签 9，标题 9.5，刻度 8，图例 7.5（拥挤时 6.3–6.8），面板内标注 ≥ 6.3（按最终印刷尺寸） |
| 坐标区 | warm 底 `#eee7dd`（默认）/ cool `#eaeaf2`；白网格；四边黑框 0.9 pt |
| 标题 | 居中、不加粗、前缀 (a)(b)(c)；单图不加前缀 |
| 尺寸（博客） | `FULL_W=7.0` / `HALF_W=3.4` in；行高 2.35–2.6 in；单幅图按内容定（如 4.8×3.2） |
| 尺寸（论文） | `style.VENUE_W[venue] = (单栏, 通栏)`：NeurIPS / ICLR 5.5；ICML 3.25 / 6.75；ACL / EMNLP 3.3 / 6.8；AAAI 3.3 / 7.0；CVPR 3.25 / 6.875 |
| 输出 | `style.save()` 同时写 300 dpi PNG 和 PDF（TrueType 内嵌，`pdf.fonttype 42`）；LaTeX 里用 PDF |
| 线型常量 | `DASH=(0,(4,2.5))` 端点连线 / 理论线；`DASH_S=(0,(3,2))` 事件线 / 基线 / 极限值；`DOT=(0,(1,1.5))` 次要解析项 |

按论文尺寸画时，`figsize` 宽度直接取 `VENUE_W`，不要画大了再在 LaTeX 里缩小，否则字号会跟着缩。

## 4. 颜色语义（不可混用）

| 名称 | 色值 | 含义 |
|---|---|---|
| `REDS` | `#f5957f #d83611 #711c09` | 基线、失败、barrier、早期、“之前” |
| `BLUES` | `#91b4ee #3879e0 #154084` | 本文方法、有效、收益、后期、“之后” |
| `INK` / `INK2` | `#262626` / `#5a5650` | 文字与零线 / 次要文字、理论线、参考线 |
| `GRAY` | `#8c8780` | 弱化系列、排行榜里的其他模型、“按构造成立” |
| `THEME["dark"]` α0.55 | 浅米色 | “证据不足”“未知” |
| `tint_cmap()` | 底色 → 深米色 | 无符号的连续量（地形图、非负矩阵） |
| `diverging_cmap()` | 深红 ← 底色 → 深蓝 | 有符号的量，配 `TwoSlopeNorm(0, -lim, lim)` |

- 同家族内浅→深 = 先→后 / 小→大。噪声轨迹用 `[0]`，均值或结论用 `[2]`，常规系列用 `[1]`。
- 中性的单个点用 `BLUES[0]` 填充 + `INK` 描边；平均点或汇总点用同家族 `[2]` 色菱形 + 白边。
- 高亮点一律白边：`**style.dot(color)`（`mec="white", mew=0.9`）。
- 背景分区：`axvspan` 用 `THEME["legend_face"]`（更浅），或 `BLUES[0]` α0.35（表示“作用窗口”）。
- 颜色只表达角色。同一概念全文同色：一篇文章里方法 X 一旦是蓝，就一直是蓝。
- 不用 jet / rainbow，不用纯红配纯绿，不用荧光色。

## 5. 对齐硬规则

同一行面板会被读者当成一组比较，任何高低不齐都会被看成错误。

1. **坐标框对齐**：同一行坐标框上下边同高。等比例面板（地形图、热力图）与普通轴同行时，普通轴 `set_box_aspect(1)`；colorbar 用 `ax.inset_axes([1.04, 0, 0.05, 1])`，不用 `fig.colorbar(ax=...)`（它会挤小坐标框）。
2. **下方文字行要么都有、要么都没有**：一个面板有 x-label，其余面板也要有一行有信息的下方文字（地形图写 `window: steps 20–180`），不写占位符。
3. **同一基线**：`style.align_xlabels(fig, axes)`。一侧是“刻度 + x-label”两行、另一侧是类别标签时，类别标签也凑成两行（名称 / 分组），第二行放在对侧 x-label 的基线上（见 T6）。
4. **类别标签不旋转、不重叠**：先缩短或分组（≤ 3 行），再缩字号（≥ 6.3）或加宽面板；旋转是最后手段，旋转后要重查基线。
5. **保存前**调用 `style.check_row(fig, axes)`，把返回值写进 `STATS`。手工对齐时也打印实测错位。应为 0（容差 1 pt）。
6. **渲染后逐张看 PNG**：标签重叠、标注压线、图例遮挡数据。

## 6. 其他固定做法

- **图例**：小、带框、放坐标区内真正空的位置，必要时扩 ylim 腾出一条空带；不用图顶横条图例。曲线占满面板时改为**直接标注**：系列色家族的深色 `[2]` 文字 + `bbox=style.bb()`，紧贴曲线（T1b）。
- **注释框**：面板内的说明文字用 `style.bb()`（无边框）；一行读数（如 `r = 0.94`、“average is 0.100 off the path”）用 `style.infobox()`（细边框），放空角。
- **标注**放空白角落，不压曲线、点和箭头。标签相撞用 `style.repel()` + 细引导线（INK2，0.5 pt），不要靠缩字号解决。
- **事件**（LR decay 开始、η 减半）：`axvline(color=INK2, lw=0.8, ls=DASH_S)` + 旁边 `bb()` 文字。**基线**：`axhline(REDS[1], ls=DASH_S)`，右端标 "baseline xx.x"（`REDS[2]`）。
- **y 含义不同的面板**（比如第三个面板，或前面是无刻度的地形图）：把 y 轴放右侧，`ax.yaxis.set_label_position("right"); ax.yaxis.tick_right()`。
- **共享 y 的并排面板**：右侧面板 `tick_params(labelleft=False)`。
- **地形图**：`contourf` 画 `log(L − min L + 1e-3)`，`cmap=style.tint_cmap()`，白色等高线 0.5 pt；谷底黑色虚线；轨迹点用浅色填充加深色描边，平均点用深色菱形；`style.no_grid(ax)`，无刻度，等比例。
- **热力图**：`no_grid`，白色格线 1.2 pt，`tick_params(length=0)`；格内数字浅格用 `INK`、深格用白色；有符号的值写成 `%+.1f`，并加 `+0.0` 清掉 `-0.0`。
- **对数轴**：`minorticks_off()` 或 `set_minor_formatter(NullFormatter())` 去掉次刻度标签；log2 轴手写 ticklabels。对数轴上 x=0 的点画在左端，并在图上注明。
- **柱状 / 棒棒糖 / 横条**：类别轴 `grid(visible=False)`、`tick_params(length=0)`；数值标签用 `style.label_values()`。
- **误差**：误差棒细（0.8 pt）、无帽；置信带 `fill_between` α 约 0.15，与线同色。在图注里写明是标准差还是标准误、几个种子。
- **可读性冗余**：超过两条线时，除颜色外再用线型或 marker 区分；转成灰度后要能分清（同家族浅深本身就有亮度差）。
- **文字**：图内一律英文，中文解释写在正文图注里。方法名照原文写，不擅自简写。
- **数字**：图上数字必须和正文一致。每个 `fig_*()` 把画出的统计量写进 `STATS`，脚本末尾打印，渲染后逐条核对。
- **模拟 / toy 图**：图注写明是 toy，只列与默认值不同的参数；模拟代码集中放在一个模块里（如 `toy.py`），不在各个图函数里各写一份。
- **改版**前把 `figs/` 和脚本备份到 `v<N>_*/`。

## 7. 图注

1. 第一句说图是什么，读者不看正文也能懂。
2. 再逐面板说看什么：“(a) …；(b) …”。
3. 先说元素含义（蓝线是什么、虚线是什么），再说结论。
4. 最后写来源：“数据取自 X”，或“toy model”。
5. 不写“图 3 展示了……”；颜色有含义时，论文里可以加 "Best viewed in color."。

## 8. 目录与运行

```
<project>/
├── figkit/style.py          # 从本 skill 复制
├── figkit/toy.py            # 可选：共享的模拟代码
├── <chapter>/make_figs.py   # 每张图一个函数；python3 make_figs.py [warm|cool]
└── <chapter>/figs/          # 输出（PNG + PDF）
```

骨架见 `templates/t0_skeleton.py`，要点如下：

```python
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "figkit"))
import style
from style import REDS, BLUES, RED, BLUE, INK, INK2, GRAY, FULL_W, HALF_W
style.apply(sys.argv[1] if len(sys.argv) > 1 else "warm")
STATS = {}

def fig_example():
    fig, axes = plt.subplots(1, 3, figsize=(FULL_W, 2.4), gridspec_kw=dict(wspace=0.42))
    ...                                              # 画出的每个数字写进 STATS
    style.align_xlabels(fig, axes)
    STATS["example_row_misalignment_pt"] = style.check_row(fig, axes)
    style.save(fig, "fig1_example", "figs"); plt.close(fig)
```

## 9. 收尾检查清单

1. `python3 make_figs.py` 跑完没有 warning（PDF 字体的 "timestamp seems very low" 可以忽略）。
2. 打印的 `STATS` 与正文数字一致；每个 `*_misalignment_pt` 都是 0。
3. 逐张 Read PNG，检查重叠、压线、遮挡、截断（值标签不能碰到边框）、`-0.0`。
4. 颜色语义符合 §4；同一概念全文同色；全图只有主角是饱和蓝。
5. 灰度下能分清各系列；最终尺寸下最小字号 ≥ 6.3 pt。
6. 图注按 §7 写。

## Credits

`references/diagrams.md` 以及 §1、§2 的选图顺序和 §6 的可读性冗余，改编自 Orchestra Research 的 academic-plotting skill（MIT License），见 `THIRD_PARTY_NOTICES.md`。
