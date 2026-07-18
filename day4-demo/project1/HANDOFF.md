# 交接文档 — Apache 日志智能清洗与故障分析工具

> **生成时间**：2026-06-25
> **开发方式**：AI Agent 按 tasks.md 顺序执行 Task 1 ~ Task 6
> **最终状态**：全部完成，38/38 测试通过

---

## 1. 项目概述

从 Apache 错误日志（`Apache.log`，56,482 行）中自动识别故障原因，完成日志解析 → 异常识别 → 统计分析 → 可视化 → 报告输出全流程。

**技术栈**：Python 3.12 / pandas / re / matplotlib / pytest

---

## 2. 开发过程记录

### 2.1 执行顺序与提交历史

| Task | 内容 | 测试 | 提交 |
|------|------|------|------|
| Task 1 | 环境搭建 + `log_parser.py` + 测试 | 11/11 ✅ | `d1841ae` |
| Task 2 | `lesson1_日志探索与解析.py` + CSV 产出 | — | `9bc7790` |
| Task 3 | `error_filter.py` + `statistics.py` + 测试 + lesson2 | 23/23 ✅ | `d169a1f` |
| Task 4 | `visualizer.py` + 测试 + lesson3 | 4/4 ✅ | `62df7fb` |
| Task 5 | `log_analyzer/` 包封装 + `analysis_report.md` | 包导入 ✅ | `d17dc88` |
| Task 6 | 产出物整理到根目录 + 最终验证 | 38/38 ✅ | `1135700` |
| 重构 | 源码移入 `src/` + sys.path 注入 + 回归测试 | 38/38 ✅ | `3546a84` |

### 2.2 关键技术决策

| 决策 | 原因 |
|------|------|
| 正则 `r'\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.*)'` | 匹配 52,004 行，跳过 4,478 行格式异常 |
| 12 种错误类型关键字匹配 | 基于真实数据分布设计，覆盖 100% error 日志 |
| matplotlib 使用 `Agg` 后端 | Windows 环境无 Tk，避免 `_tkinter.TclError` |
| 源码移入 `src/` + sys.path 注入 | 整理根目录，保持 import 和文件路径正常 |
| `log_analyzer/` 包留根目录 | 作为对外 API，内部自包含，与 `src/` 模块独立 |

---

## 3. 最终目录结构

```
project1/
│
├── src/                              # 所有 Python 源码
│   ├── log_parser.py                 # 日志解析模块（正则、字段提取、日期转换）
│   ├── error_filter.py               # 错误筛选模块（12 种类型分类）
│   ├── statistics.py                 # 统计模块（每日/类型/模块）
│   ├── visualizer.py                 # 可视化模块（时序图/饼图/柱状图）
│   ├── lesson1_日志探索与解析.py       # Lesson 1 主脚本
│   ├── lesson2_异常识别与统计.py       # Lesson 2 主脚本
│   ├── lesson3_可视化与报告.py         # Lesson 3 主脚本
│   ├── test_log_parser.py            # 测试（11 用例）
│   ├── test_error_filter.py          # 测试（17 用例）
│   ├── test_statistics.py            # 测试（6 用例）
│   └── test_visualizer.py            # 测试（4 用例）
│
├── log_analyzer/                     # 工具库包（对外 API，独立副本）
│   ├── __init__.py
│   ├── log_parser.py
│   ├── error_filter.py
│   ├── statistics.py
│   ├── visualizer.py
│   ├── utils.py
│   └── README.md
│
├── Apache.log                        # 数据源（56,482 行）
├── requirements.txt                  # 依赖：pandas, matplotlib, pytest
│
├── structured_logs.csv               # ✅ 验收产出（52,004 行）
├── error_logs.csv                    # ✅ 验收产出（38,081 行）
├── error_code_reference.csv          # ✅ 验收产出（12 种错误类型）
├── charts/                           # ✅ 验收产出
│   ├── daily_trend.png               #    每日错误趋势时序图
│   ├── error_types.png               #    错误类型占比饼图
│   └── modules.png                   #    模块错误数量柱状图
├── analysis_report.md                # ✅ 验收产出（8 章节）
│
├── docs/                             # 设计文档
│   ├── prd.md                        #    产品需求文档
│   ├── design.md                     #    技术设计文档
│   ├── dev.md                        #    开发文档
│   ├── test-strategy.md              #    测试策略
│   └── 作业要求.md                     #    原始作业要求
│
├── ai-log/                           # AI 协作日志
├── tasks.md                          # 任务清单
└── .gitignore
```

---

## 4. 验收产出物清单

| 文件 | 预期 | 实际 | 状态 |
|------|------|------|:----:|
| `structured_logs.csv` | 52,004 行，3 列（timestamp/level/content） | 52,004 行 | ✅ |
| `error_logs.csv` | 38,081 行，4 列（timestamp/content/error_type/module） | 38,081 行 | ✅ |
| `error_code_reference.csv` | 12 行（12 种错误类型对照） | 12 行 | ✅ |
| `charts/daily_trend.png` | 存在，大小 > 0 | 134 KB | ✅ |
| `charts/error_types.png` | 存在，大小 > 0 | 73 KB | ✅ |
| `charts/modules.png` | 存在，大小 > 0 | 34 KB | ✅ |
| `analysis_report.md` | 包含 8 个 `##` 章节 | 8 章节 | ✅ |
| `log_analyzer/` | 可导入 4 个子模块 | 导入成功 | ✅ |

---

## 5. 测试覆盖

### 5.1 测试用例明细（38 个）

**test_log_parser.py（11 用例）**
- `TestParseLogLine`：正常行、含 client 行、格式异常行、空行
- `TestConvertDate`：6 月、2 月、12 月日期转换
- `TestParseLogFile`：总行数=52004、三列、无缺失值、级别分布（error=38081/notice=13755/warn=168）

**test_error_filter.py（17 用例）**
- `TestClassifyError`：12 种错误类型各 1 个 + REQUEST_ERROR 兜底
- `TestFilterErrors`：筛选后行数=38081、包含 error_type/module 列、覆盖 12 种类型
- `TestGetErrorReference`：12 行、包含 error_code/description 列

**test_statistics.py（6 用例）**
- `TestDailyStats`：天数 200~250、包含 date/count 列
- `TestTypeStats`：数量之和=38081、12 种类型
- `TestModuleStats`：4 个模块、数量之和=38081

**test_visualizer.py（4 用例）**
- `TestPlotDailyTrend`：文件生成、文件大小 > 0
- `TestPlotErrorTypes`：文件生成
- `TestPlotModules`：文件生成

### 5.2 运行测试

```bash
# 激活虚拟环境
source .venv/Scripts/activate   # Windows Git Bash
# .venv\Scripts\activate        # Windows CMD/PowerShell

# 运行全部测试
pytest src/test_*.py -v

# 运行单个模块测试
pytest src/test_log_parser.py -v
pytest src/test_error_filter.py test_statistics.py -v
pytest src/test_visualizer.py -v
```

---

## 6. 运行方式

```bash
# 按顺序运行三个 Lesson
python src/lesson1_日志探索与解析.py    # → output/structured_logs.csv
python src/lesson2_异常识别与统计.py    # → output/error_logs.csv, error_code_reference.csv
python src/lesson3_可视化与报告.py      # → output/charts/*.png
```

**注意**：lesson 脚本通过 `PROJECT_ROOT` 常量定位 `Apache.log` 和 `output/`，无论从哪个目录运行都能正确找到文件。

---

## 7. 已知限制与注意事项

| 项目 | 说明 |
|------|------|
| 格式异常行 | 4,478 行（`script not found or unable to stat`）无时间戳，解析跳过 |
| notice/warn | 本次分析仅处理 error 级别，notice 和 warn 不在分析范围内 |
| matplotlib 后端 | 使用 `Agg`（非交互式），不支持 `plt.show()`，仅输出 PNG 文件 |
| `src/` 与 `log_analyzer/` | 两份独立代码副本，`log_analyzer/` 是对外 API，`src/` 是开发用模块 |
| 输出路径 | CSV 和图表输出到 `output/` 目录，根目录的副本是验收用的静态拷贝 |

---

## 8. 快速验收 Checklist

```bash
# 1. 文件存在性
ls structured_logs.csv error_logs.csv error_code_reference.csv
ls charts/daily_trend.png charts/error_types.png charts/modules.png
ls analysis_report.md
ls log_analyzer/

# 2. CSV 行数
python -c "import pandas as pd; df=pd.read_csv('structured_logs.csv'); print(f'structured_logs: {len(df)}')"
python -c "import pandas as pd; df=pd.read_csv('error_logs.csv'); print(f'error_logs: {len(df)}')"
python -c "import pandas as pd; df=pd.read_csv('error_code_reference.csv'); print(f'error_code_reference: {len(df)}')"

# 3. 报告章节
grep "^## " analysis_report.md | wc -l   # 应为 8

# 4. 包导入
python -c "from log_analyzer import log_parser, error_filter, statistics, visualizer; print('OK')"

# 5. 全部测试
pytest src/test_*.py -v
```
