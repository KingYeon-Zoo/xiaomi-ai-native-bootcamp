# Tasks 任务清单

> **目标**：完成 Apache 日志智能清洗与故障分析工具的开发
> **技术栈**：Python 3.10+ / pandas / re / matplotlib / pytest
> **数据源**：Apache.log（56,482 行）
> **预计耗时**：2.5 小时

---

## Task 1：环境搭建 + 日志解析模块

**目标**：搭建开发环境，实现核心解析模块并通过测试

### 任务详情

1. **创建虚拟环境**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows Git Bash
   ```

2. **创建 requirements.txt**
   ```
   pandas>=1.5.0
   matplotlib>=3.5.0
   pytest>=7.0.0
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **实现 log_parser.py**
   - `parse_log_line(line: str) -> dict | None`：解析单行日志
   - `parse_log_file(filepath: str) -> pd.DataFrame`：解析整个日志文件
   - `convert_date(timestamp: str) -> str`：日期格式转换
   - 正则表达式：`r'\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.*)'`

5. **编写 test_log_parser.py**
   - 测试 parse_log_line：正常行、含 client 行、格式异常行、空行
   - 测试 convert_date：6 月、2 月、12 月
   - 测试 parse_log_file：总行数 = 52,004、三列、无缺失值、级别分布

### 输入文件
- `Apache.log`（数据源）
- `docs/design.md`（正则设计）
- `docs/dev.md`（接口定义）
- `docs/test-strategy.md`（测试用例）

### 输出文件
- `.venv/`（虚拟环境）
- `requirements.txt`（依赖清单）
- `log_parser.py`（解析模块）
- `test_log_parser.py`（测试文件）

### 验证标准
```bash
# 运行测试，全部通过
pytest test_log_parser.py -v
```

---

## Task 2：Lesson 1 主脚本 + 验证产出物

**目标**：完成日志探索与解析的主脚本，产出结构化 CSV

### 任务详情

1. **实现 lesson1_日志探索与解析.py**
   - 数据探索：输出总行数、各级别数量、时间范围、格式异常行数
   - 调用 log_parser.py 解析日志
   - 保存 structured_logs.csv 到 output/ 目录
   - 创建 output/ 目录（如不存在）

2. **运行脚本**
   ```bash
   python lesson1_日志探索与解析.py
   ```

3. **验证产出物**
   - 检查 output/structured_logs.csv 存在
   - 检查行数 = 52,004
   - 检查包含 timestamp、level、content 三列

### 输入文件
- `Apache.log`（数据源）
- `log_parser.py`（Task 1 产出）

### 输出文件
- `lesson1_日志探索与解析.py`（主脚本）
- `output/structured_logs.csv`（结构化数据）

### 验证标准
```bash
# 检查文件行数
wc -l output/structured_logs.csv  # 应为 52,005（含表头）

# 或用 Python 验证
python -c "import pandas as pd; df = pd.read_csv('output/structured_logs.csv'); print(f'行数: {len(df)}, 列: {list(df.columns)}')"
```

---

## Task 3：异常识别与统计分析模块

**目标**：实现错误筛选、分类、统计功能，完成 Lesson 2

### 任务详情

1. **实现 error_filter.py**
   - `classify_error(content: str) -> str`：错误分类（12 种类型）
   - `filter_errors(df: pd.DataFrame) -> pd.DataFrame`：筛选 error 日志
   - `get_error_reference() -> pd.DataFrame`：错误类型对照表

2. **实现 statistics.py**
   - `daily_stats(df: pd.DataFrame) -> pd.DataFrame`：每日统计
   - `type_stats(df: pd.DataFrame) -> pd.DataFrame`：类型统计
   - `module_stats(df: pd.DataFrame) -> pd.DataFrame`：模块统计

3. **编写测试**
   - `test_error_filter.py`：测试分类规则、筛选结果、对照表
   - `test_statistics.py`：测试三个统计函数

4. **实现 lesson2_异常识别与统计.py**
   - 加载 structured_logs.csv
   - 筛选 error 日志并分类
   - 执行三个维度统计
   - 保存 error_logs.csv 和 error_code_reference.csv 到 output/

### 输入文件
- `output/structured_logs.csv`（Task 2 产出）
- `docs/design.md`（错误分类规则）

### 输出文件
- `error_filter.py`（筛选模块）
- `statistics.py`（统计模块）
- `test_error_filter.py`（测试）
- `test_statistics.py`（测试）
- `lesson2_异常识别与统计.py`（主脚本）
- `output/error_logs.csv`（error 日志，38,081 行）
- `output/error_code_reference.csv`（错误对照表，12 行）

### 验证标准
```bash
# 运行测试
pytest test_error_filter.py test_statistics.py -v

# 运行主脚本
python lesson2_异常识别与统计.py

# 验证产出物
python -c "
import pandas as pd
df = pd.read_csv('output/error_logs.csv')
ref = pd.read_csv('output/error_code_reference.csv')
print(f'error_logs: {len(df)} 行, 错误类型: {df[\"error_type\"].nunique()} 种')
print(f'error_code_reference: {len(ref)} 行')
"
```

---

## Task 4：可视化模块 + Lesson 3 主脚本

**目标**：实现可视化功能，生成三种图表

### 任务详情

1. **实现 visualizer.py**
   - `plot_daily_trend(df, output_path)`：时序图（按天，X 轴每 30 天刻度）
   - `plot_error_types(df, output_path)`：饼图（占比 <2% 合并为"其他"）
   - `plot_modules(df, output_path)`：柱状图（对数坐标）

2. **编写 test_visualizer.py**
   - 测试三个绘图函数：文件生成、文件大小 > 0

3. **实现 lesson3_可视化与报告.py**
   - 加载统计数据
   - 调用 visualizer.py 生成图表到 output/charts/
   - 暂时不实现报告部分（Task 5 完成）

### 输入文件
- `output/error_logs.csv`（Task 3 产出）
- `error_filter.py`（Task 3 产出）
- `statistics.py`（Task 3 产出）
- `docs/design.md`（可视化设计）

### 输出文件
- `visualizer.py`（可视化模块）
- `test_visualizer.py`（测试）
- `lesson3_可视化与报告.py`（主脚本）
- `output/charts/daily_trend.png`（时序图）
- `output/charts/error_types.png`（饼图）
- `output/charts/modules.png`（柱状图）

### 验证标准
```bash
# 运行测试
pytest test_visualizer.py -v

# 运行主脚本
python lesson3_可视化与报告.py

# 验证图表生成
ls -la output/charts/
# 应有 3 个 PNG 文件，大小 > 0
```

---

## Task 5：工具库封装 + 分析报告

**目标**：封装 log_analyzer 包，撰写分析报告

### 任务详情

1. **创建 log_analyzer/ 包**
   ```
   log_analyzer/
   ├── __init__.py
   ├── log_parser.py       # 从根目录复制
   ├── error_filter.py     # 从根目录复制
   ├── statistics.py       # 从根目录复制
   ├── visualizer.py       # 从根目录复制
   ├── utils.py            # 新建（工具函数）
   └── README.md           # 包说明
   ```

2. **修改 lesson3 主脚本**
   - 改为从 log_analyzer 包导入

3. **撰写 analysis_report.md**
   - 项目概述
   - 数据探索
   - 日志解析方法
   - 异常识别结果
   - 统计分析结果
   - 可视化分析（引用 output/charts/ 图片）
   - 故障根因分析
   - 总结与优化建议

### 输入文件
- `log_parser.py`、`error_filter.py`、`statistics.py`、`visualizer.py`（Task 1-4 产出）
- `output/error_logs.csv`（统计数据源）
- `output/charts/*.png`（图表）
- `docs/design.md`（故障根因分析参考）

### 输出文件
- `log_analyzer/`（工具库包）
- `analysis_report.md`（分析报告）

### 验证标准
```bash
# 验证包可导入
python -c "from log_analyzer import log_parser, error_filter, statistics, visualizer; print('导入成功')"

# 验证报告存在
ls analysis_report.md

# 检查报告包含 8 个章节
grep "^## " analysis_report.md | wc -l  # 应为 8
```

---

## Task 6：产出物整理 + 最终验证 + 提交

**目标**：整理验收文件，E2E 测试，最终提交

### 任务详情

1. **复制产出物到根目录**（验收要求）
   ```bash
   cp output/structured_logs.csv .
   cp output/error_logs.csv .
   cp output/error_code_reference.csv .
   cp -r output/charts .
   ```

2. **E2E 人工测试**
   - 打开 charts/daily_trend.png，检查趋势清晰
   - 打开 charts/error_types.png，检查饼图标签清晰
   - 打开 charts/modules.png，检查柱状图数值可见
   - 阅读 analysis_report.md，检查 8 个章节完整

3. **运行全部测试**
   ```bash
   pytest test_*.py -v
   ```

4. **更新 ai-log.md**
   - 记录开发过程中的关键决策

5. **最终提交**
   ```bash
   git add -A
   git commit -m "feat: 完成 Apache 日志分析工具全部功能"
   ```

### 输入文件
- `output/`（所有产出物）
- `log_analyzer/`（工具库）

### 输出文件
- `structured_logs.csv`（根目录）
- `error_logs.csv`（根目录）
- `error_code_reference.csv`（根目录）
- `charts/`（根目录）
- `analysis_report.md`（根目录）

### 验证标准
```bash
# 验证文件存在
ls structured_logs.csv error_logs.csv error_code_reference.csv
ls charts/*.png
ls analysis_report.md log_analyzer/

# 验证测试通过
pytest test_*.py -v

# 验证 git 状态
git status  # 应为 clean
git log --oneline  # 检查提交历史
```

---

## 执行顺序

```
Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6
  │        │        │        │        │        │
  ▼        ▼        ▼        ▼        ▼        ▼
环境     CSV     统计     图表     包封装    最终
搭建    产出    分析     生成     报告     验证
```

**注意**：每个 Task 依赖前一个 Task 的产出物，必须按顺序执行。
