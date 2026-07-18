# Apache HTTP 服务器日志智能清洗与故障分析工具

> 从 Apache 错误日志中自动识别故障原因，完成日志解析 → 异常识别 → 统计分析 → 可视化 → 报告输出全流程。

---

## 项目概述

**角色**：运维工程师

**目标**：Web 服务器报错时，快速分析 Apache 错误日志，定位故障根因。

**技术栈**：Python 3.10+ / pandas / re / matplotlib / pytest

**数据源**：`Apache.log`（56,482 行错误日志，2005-06-09 ~ 2006-02-28）

---

## 快速开始

### 1. 环境搭建

```bash
# 创建虚拟环境
python -m venv .venv

# 激活环境
source .venv/Scripts/activate   # Windows Git Bash
# .venv\Scripts\activate        # Windows CMD/PowerShell

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行分析

```bash
# 按顺序运行三个 Lesson
python src/lesson1_日志探索与解析.py
python src/lesson2_异常识别与统计.py
python src/lesson3_可视化与报告.py
```

### 3. 运行测试

```bash
# Git Bash / Linux / Mac
pytest src/test_*.py -v

# PowerShell
pytest src/ -v -k "test_"
```

---

## 项目结构

```
project1/
├── Apache.log                        # 数据源
├── README.md                         # 本文件
├── requirements.txt                  # 依赖清单
├── .venv/                            # 虚拟环境
│
├── src/                              # 源码
│   ├── log_parser.py                 # 日志解析模块
│   ├── error_filter.py               # 错误筛选模块
│   ├── statistics.py                 # 统计分析模块
│   ├── visualizer.py                 # 可视化模块
│   ├── lesson1_日志探索与解析.py       # Lesson 1 主脚本
│   ├── lesson2_异常识别与统计.py       # Lesson 2 主脚本
│   ├── lesson3_可视化与报告.py         # Lesson 3 主脚本
│   ├── test_log_parser.py            # 测试
│   ├── test_error_filter.py          # 测试
│   ├── test_statistics.py            # 测试
│   └── test_visualizer.py            # 测试
│
├── log_analyzer/                     # 工具库包（对外 API）
│   ├── __init__.py
│   ├── log_parser.py
│   ├── error_filter.py
│   ├── statistics.py
│   ├── visualizer.py
│   └── utils.py
│
├── output/                           # 所有产出物
│   ├── structured_logs.csv           # 结构化日志（52,004 行）
│   ├── error_logs.csv                # 错误日志（38,081 行）
│   ├── error_code_reference.csv      # 错误类型对照表（12 种）
│   ├── charts/                       # 可视化图表
│   │   ├── daily_trend.png           #   每日错误趋势
│   │   ├── error_types.png           #   错误类型占比
│   │   └── modules.png               #   模块错误对比
│   └── analysis_report.md            # 分析报告
│
└── docs/                             # 设计文档
    ├── 作业要求.md
    ├── prd.md                        # 产品需求文档
    ├── design.md                     # 技术设计文档
    ├── dev.md                        # 开发文档
    ├── test-strategy.md              # 测试策略
    └── ai-log.md                     # AI 协作日志
```

---

## 产出物说明

所有产出物位于 `output/` 目录：

| 文件 | 说明 | 行数/大小 |
|------|------|-----------|
| `structured_logs.csv` | 解析后的结构化日志 | 52,004 行 |
| `error_logs.csv` | 筛选的 error 日志（含错误分类） | 38,081 行 |
| `error_code_reference.csv` | 错误类型含义对照表 | 12 种类型 |
| `charts/daily_trend.png` | 每日错误数量趋势图 | ~134 KB |
| `charts/error_types.png` | 错误类型占比饼图 | ~73 KB |
| `charts/modules.png` | 模块错误数量柱状图 | ~34 KB |
| `analysis_report.md` | 故障根因分析报告 | 8 个章节 |

---

## 错误类型说明

本项目识别 12 种 Apache 错误类型：

| 错误代码 | 说明 | 所属模块 |
|----------|------|----------|
| FILE_NOT_FOUND | 文件不存在 (404) | request |
| DIR_INDEX_FORBIDDEN | 目录索引被禁止 | request |
| MODJK_WORKER_ERROR | mod_jk worker 连接后端失败 | mod_jk |
| SCRIPT_NOT_FOUND | CGI 脚本不存在 | request |
| MODJK_INIT | mod_jk 子进程初始化失败 | mod_jk |
| JK2_CHILD_NOT_FOUND | jk2 子进程找不到 | mod_jk |
| BEAN_CREATE_ERROR | Bean 创建错误 | config |
| CONFIG_ERROR | 配置更新失败 | config |
| URI_TOO_LONG | URI 过长 | request |
| URIMAP_ERROR | URI 映射错误 | other |
| INVALID_METHOD | 无效请求方法 | request |
| REQUEST_ERROR | 其他请求错误 | request |

---

## 技术设计

详见 `docs/` 目录：

- **prd.md** — 项目背景、目标/非目标、功能需求、验收标准
- **design.md** — 架构设计、正则表达式、错误分类规则、数据流
- **dev.md** — 环境搭建、模块接口定义、开发计划
- **test-strategy.md** — 测试用例、验证标准

---

## 测试覆盖

```bash
# 运行全部测试（38 个用例）
# Git Bash / Linux / Mac:
pytest src/test_*.py -v

# PowerShell:
pytest src/ -v -k "test_"
```

**测试分布**：
- `test_log_parser.py`: 11 用例
- `test_error_filter.py`: 17 用例
- `test_statistics.py`: 6 用例
- `test_visualizer.py`: 4 用例

---

## 已知限制

| 项目 | 说明 |
|------|------|
| 格式异常行 | 4,478 行（`script not found or unable to stat`）无时间戳，解析跳过 |
| 分析范围 | 仅分析 error 级别，notice/warn 不在范围内 |
| matplotlib 后端 | 使用 `Agg`（非交互式），仅输出 PNG 文件 |
