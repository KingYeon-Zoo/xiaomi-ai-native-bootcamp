# 开发文档

## Apache HTTP 服务器日志智能清洗与故障分析工具

---

## 1. 环境搭建

### 1.1 Python 环境（.venv）

```bash
# 创建虚拟环境
python -m venv .venv

# 激活环境
.venv\Scripts\activate        # Windows CMD/PowerShell
source .venv/Scripts/activate # Windows Git Bash
source .venv/bin/activate     # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 1.2 requirements.txt

```
pandas>=1.5.0
matplotlib>=3.5.0
pytest>=7.0.0
```

### 1.3 运行方式

```bash
# 按顺序运行三个 Lesson（必须按顺序，有数据依赖）
python src/lesson1_日志探索与解析.py
python src/lesson2_异常识别与统计.py
python src/lesson3_可视化与报告.py

# 运行测试
pytest src/ -v -k "test_"    # PowerShell
pytest src/test_*.py -v      # Git Bash / Linux / Mac
```

---

## 2. 代码结构

```
project1/
├── Apache.log                        # 数据源（56,482 行）
├── README.md                         # 项目说明
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
│   ├── test_log_parser.py            # 测试（11 用例）
│   ├── test_error_filter.py          # 测试（17 用例）
│   ├── test_statistics.py            # 测试（6 用例）
│   └── test_visualizer.py            # 测试（4 用例）
│
├── log_analyzer/                     # 工具库包
│   ├── __init__.py
│   ├── log_parser.py
│   ├── error_filter.py
│   ├── statistics.py
│   ├── visualizer.py
│   ├── utils.py
│   └── README.md
│
├── output/                           # 所有产出物
│   ├── structured_logs.csv           # 结构化日志（52,004 行）
│   ├── error_logs.csv                # 错误日志（38,081 行）
│   ├── error_code_reference.csv      # 错误类型对照表（12 种）
│   ├── analysis_report.md            # 分析报告（8 章节）
│   └── charts/                       # 可视化图表
│       ├── daily_trend.png
│       ├── error_types.png
│       └── modules.png
│
└── docs/                             # 设计文档
    ├── 作业要求.md
    ├── prd.md
    ├── design.md
    ├── dev.md
    ├── test-strategy.md
    └── ai-log.md
```

---

## 3. 数据流

```
Apache.log (56,482行)
    │
    ▼
lesson1_日志探索与解析.py
    │
    ▼
output/structured_logs.csv (52,004行)
    │
    ▼
lesson2_异常识别与统计.py
    │
    ├──▶ output/error_logs.csv (38,081行)
    └──▶ output/error_code_reference.csv (12种)
    │
    ▼
lesson3_可视化与报告.py
    │
    ├──▶ output/charts/daily_trend.png
    ├──▶ output/charts/error_types.png
    ├──▶ output/charts/modules.png
    └──▶ output/analysis_report.md
```

---

## 4. 模块接口

### 4.1 log_parser.py

```python
def parse_log_line(line: str) -> dict | None:
    """解析单行日志，返回 {timestamp, level, content} 或 None"""

def parse_log_file(filepath: str) -> pd.DataFrame:
    """解析整个日志文件，返回 DataFrame"""

def convert_date(timestamp: str) -> str:
    """日期转换：Thu Jun 09 06:07:04 2005 → 2005-06-09"""
```

### 4.2 error_filter.py

```python
def classify_error(content: str) -> str:
    """错误分类，返回 12 种错误类型之一"""

def filter_errors(df: pd.DataFrame) -> pd.DataFrame:
    """筛选 error 级别日志并添加分类"""

def get_error_reference() -> pd.DataFrame:
    """获取错误类型对照表"""
```

### 4.3 statistics.py

```python
def daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """每日错误数量统计"""

def type_stats(df: pd.DataFrame) -> pd.DataFrame:
    """错误类型统计"""

def module_stats(df: pd.DataFrame) -> pd.DataFrame:
    """模块维度统计"""
```

### 4.4 visualizer.py

```python
def plot_daily_trend(df: pd.DataFrame, output_path: str):
    """绘制每日错误趋势时序图"""

def plot_error_types(df: pd.DataFrame, output_path: str):
    """绘制错误类型占比饼图"""

def plot_modules(df: pd.DataFrame, output_path: str):
    """绘制模块错误数量柱状图"""
```

---

## 5. 已知限制

| 项目 | 说明 |
|------|------|
| 格式异常行 | 4,478 行无时间戳，解析跳过 |
| 分析范围 | 仅分析 error 级别 |
| matplotlib 后端 | 使用 Agg，仅输出 PNG |
| src/ 与 log_analyzer/ | 两份独立代码副本 |
