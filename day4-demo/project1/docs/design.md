# 技术设计文档

## Apache HTTP 服务器日志智能清洗与故障分析工具

---

## 1. 架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        主流程编排                                 │
│  lesson1_日志探索与解析.py → lesson2_异常识别与统计.py → lesson3_可视化与报告.py  │
└─────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│  log_parser   │         │ error_filter  │         │  visualizer   │
│    .py        │         │    .py        │         │    .py        │
│               │         │               │         │               │
│ 正则解析      │         │ 错误筛选      │         │ 图表生成      │
│ 字段提取      │         │ 错误分类      │         │ 时序/饼/柱    │
└───────────────┘         └───────────────┘         └───────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│  statistics   │         │    utils      │         │   charts/     │
│    .py        │         │    .py        │         │               │
│               │         │               │         │ *.png         │
│ 多维度统计    │         │ 工具函数      │         │               │
└───────────────┘         └───────────────┘         └───────────────┘
```

### 1.2 数据流

```
Apache.log (56,482行)
    │
    ▼
log_parser.py ──────────────────────────────────► structured_logs.csv (52,004行)
    │                                                      │
    │ (格式异常 4,478 行跳过)                               │
    │                                                      ▼
    │                                              error_filter.py
    │                                                      │
    │                              ┌───────────────────────┴───────────────────────┐
    │                              ▼                                               ▼
    │                      error_logs.csv (38,081行)                  error_code_reference.csv
    │                              │                                               │
    │                              ▼                                               │
    │                      statistics.py (内存中传递)                              │
    │                              │                                               │
    │          ┌───────────────────┼───────────────────┐                           │
    │          ▼                   ▼                   ▼                           │
    │   daily_stats_df      type_stats_df       module_stats_df                   │
    │   (DataFrame)         (DataFrame)         (DataFrame)                        │
    │          │                   │                   │                           │
    │          └───────────────────┼───────────────────┘                           │
    │                              ▼                                               │
    │                      visualizer.py                                           │
    │                              │                                               │
    │          ┌───────────────────┼───────────────────┐                           │
    │          ▼                   ▼                   ▼                           │
    │  charts/daily_trend.png  charts/error_types.png  charts/modules.png          │
    │                              │                                               │
    └──────────────────────────────┴───────────────────────────────────────────────┘
                                                                   │
                                                                   ▼
                                                           analysis_report.md
                                                           (手写，引用图表)
```

---

## 2. 模块划分与职责

### 2.1 模块清单

| 模块 | 文件 | 职责 | 输入 | 输出 |
|------|------|------|------|------|
| 解析模块 | `log_parser.py` | 正则解析日志，提取字段 | Apache.log | structured_logs.csv |
| 筛选模块 | `error_filter.py` | 筛选 error 日志，分类错误类型 | structured_logs.csv | error_logs.csv |
| 统计模块 | `statistics.py` | 多维度统计分析 | error_logs.csv | 统计 CSV 文件 |
| 可视化模块 | `visualizer.py` | 生成图表 | 统计 CSV 文件 | charts/*.png |
| 工具模块 | `utils.py` | 通用工具函数 | - | - |

### 2.2 模块接口设计

#### log_parser.py

```python
def parse_log_line(line: str) -> dict | None:
    """
    解析单行日志

    Args:
        line: 原始日志行

    Returns:
        dict: {'timestamp': str, 'level': str, 'content': str} 或 None（格式异常）
    """

def parse_log_file(filepath: str) -> pd.DataFrame:
    """
    解析整个日志文件

    Args:
        filepath: 日志文件路径

    Returns:
        DataFrame: 包含 timestamp, level, content 三列
    """
```

#### error_filter.py

```python
def filter_errors(df: pd.DataFrame) -> pd.DataFrame:
    """筛选 error 级别日志"""

def classify_error(content: str) -> str:
    """
    错误分类

    Args:
        content: 日志内容

    Returns:
        str: 错误类型代码
    """

def get_error_reference() -> pd.DataFrame:
    """获取错误类型对照表"""
```

#### statistics.py

```python
def daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """每日错误数量统计"""

def type_stats(df: pd.DataFrame) -> pd.DataFrame:
    """错误类型统计"""

def module_stats(df: pd.DataFrame) -> pd.DataFrame:
    """模块维度统计"""
```

#### visualizer.py

```python
def plot_daily_trend(df: pd.DataFrame, output_path: str):
    """绘制每日错误趋势时序图"""

def plot_error_types(df: pd.DataFrame, output_path: str):
    """绘制错误类型占比饼图"""

def plot_modules(df: pd.DataFrame, output_path: str):
    """绘制模块错误数量柱状图"""
```

---

## 3. 正则表达式设计

### 3.1 日志格式分析

基于真实数据测试，日志存在 3 种格式：

| 格式 | 数量 | 占比 | 示例 |
|------|------|------|------|
| 包含 `[client xxx]` | 31,115 | 55.1% | `[Thu Jun 09 07:11:21 2005] [error] [client 204.100.200.22] Directory index forbidden by rule: /var/www/html/` |
| 不包含 `[client xxx]` | 20,889 | 37.0% | `[Thu Jun 09 06:07:04 2005] [notice] LDAP: Built with OpenLDAP LDAP SDK` |
| 格式异常 | 4,478 | 7.9% | `script not found or unable to stat` |

### 3.2 正则表达式

```python
PATTERN = r'\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.*)'
```

**提取字段**：
- `$1` → `timestamp`：时间戳（如 `Thu Jun 09 06:07:04 2005`）
- `$2` → `level`：日志级别（notice / error / warn）
- `$3` → `content`：日志内容（包含 `[client xxx]` 部分）

**匹配结果**：52,004 行成功匹配，4,478 行格式异常跳过

### 3.3 日期格式转换

原始格式：`Thu Jun 09 06:07:04 2005`

目标格式：`2005-06-09`（用于按天聚合）

```python
MONTH_MAP = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
             'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

def convert_date(timestamp: str) -> str:
    """Thu Jun 09 06:07:04 2005 → 2005-06-09"""
    parts = timestamp.split()
    return f"{parts[4]}-{MONTH_MAP[parts[1]]}-{parts[2].zfill(2)}"
```

---

## 4. 错误分类规则

### 4.1 错误类型定义（12 种）

| 错误代码 | 错误类型 | 关键字匹配规则 | 数量 | 占比 |
|----------|----------|----------------|------|------|
| FILE_NOT_FOUND | 文件不存在 | `File does not exist` | 20,861 | 54.8% |
| DIR_INDEX_FORBIDDEN | 目录索引禁止 | `Directory index forbidden` | 6,745 | 17.7% |
| MODJK_WORKER_ERROR | mod_jk worker 错误 | `mod_jk child workerEnv` | 4,349 | 11.4% |
| SCRIPT_NOT_FOUND | 脚本不存在 | `script not found` | 3,301 | 8.7% |
| MODJK_INIT | mod_jk 初始化 | `mod_jk child init` | 1,259 | 3.3% |
| JK2_CHILD_NOT_FOUND | jk2 子进程找不到 | `jk2_init() Can't find` | 971 | 2.5% |
| BEAN_CREATE_ERROR | Bean 创建错误 | `env.createBean2()` | 180 | 0.5% |
| CONFIG_ERROR | 配置错误 | `config.update()` | 180 | 0.5% |
| URI_TOO_LONG | URI 过长 | `URI too long` | ~150 | 0.4% |
| URIMAP_ERROR | URI 映射错误 | `uriMap.mapUri()` | 27 | 0.1% |
| INVALID_METHOD | 无效请求方法 | `Invalid method` | 26 | 0.1% |
| REQUEST_ERROR | 其他请求错误 | `attempt to invoke` / `Invalid URI` / `client sent` | ~130 | 0.3% |

### 4.2 分类函数

```python
def classify_error(content: str) -> str:
    """基于关键字匹配的错误分类"""
    if 'mod_jk child workerEnv' in content:
        return 'MODJK_WORKER_ERROR'
    elif 'mod_jk child init' in content:
        return 'MODJK_INIT'
    elif 'jk2_init()' in content and "Can't find" in content:
        return 'JK2_CHILD_NOT_FOUND'
    elif 'env.createBean2()' in content:
        return 'BEAN_CREATE_ERROR'
    elif 'config.update()' in content:
        return 'CONFIG_ERROR'
    elif 'File does not exist' in content:
        return 'FILE_NOT_FOUND'
    elif 'Directory index forbidden' in content:
        return 'DIR_INDEX_FORBIDDEN'
    elif 'script not found' in content:
        return 'SCRIPT_NOT_FOUND'
    elif 'URI too long' in content:
        return 'URI_TOO_LONG'
    elif 'uriMap.mapUri()' in content:
        return 'URIMAP_ERROR'
    elif 'Invalid method' in content:
        return 'INVALID_METHOD'
    else:
        return 'REQUEST_ERROR'
```

### 4.3 模块划分

| 模块 | 包含的错误类型 | 数量 | 占比 |
|------|----------------|------|------|
| request | FILE_NOT_FOUND, DIR_INDEX_FORBIDDEN, SCRIPT_NOT_FOUND, INVALID_METHOD, URI_TOO_LONG, REQUEST_ERROR | 30,986 | 81.4% |
| mod_jk | MODJK_WORKER_ERROR, MODJK_INIT, JK2_CHILD_NOT_FOUND | 6,579 | 17.3% |
| config | BEAN_CREATE_ERROR, CONFIG_ERROR | 360 | 0.9% |
| other | URIMAP_ERROR 等 | 156 | 0.4% |

---

## 5. 中间产物设计

### 5.1 文件清单

| 文件 | 来源 | 用途 | 保留 |
|------|------|------|:----:|
| `structured_logs.csv` | log_parser.py | 基础结构化数据 | ✅ |
| `error_logs.csv` | error_filter.py | 筛选后的 error 日志 | ✅ |
| `error_code_reference.csv` | error_filter.py | 错误类型对照表 | ✅ |

**说明**：
- `structured_logs.csv`、`error_logs.csv`、`error_code_reference.csv` 是阶段性产出，需要保留
- 统计结果（daily_stats、type_stats、module_stats）在内存中传递给可视化模块，**不落盘**
- 最终产出是 `charts/*.png` 图表文件

### 5.2 CSV 格式定义

**structured_logs.csv**：
```csv
timestamp,level,content
"Thu Jun 09 06:07:04 2005","notice","LDAP: Built with OpenLDAP LDAP SDK"
```

**error_logs.csv**：
```csv
timestamp,content,error_type,module
"Thu Jun 09 06:07:05 2005","env.createBean2(): Factory error...","BEAN_CREATE_ERROR","config"
```

---

## 6. 可视化设计

### 6.1 图表清单

| 图表 | 文件名 | 类型 | X 轴 | Y 轴 |
|------|--------|------|------|------|
| 每日错误趋势 | `daily_trend.png` | 时序图 | 日期（按天） | 错误数量 |
| 错误类型分布 | `error_types.png` | 饼图 | 错误类型 | 占比 |
| 模块错误对比 | `modules.png` | 柱状图 | 模块名称 | 错误数量 |

### 6.2 图表设计细节

**时序图**：
- 时间粒度：按天（230 个数据点）
- 图表尺寸：12×6 英寸
- X 轴标签：每 30 天显示一个刻度

**饼图**：
- 占比 < 2% 的类型合并为"其他"
- 显示百分比标签
- 使用不同颜色区分

**柱状图**：
- 4 个模块：request / mod_jk / config / other
- 使用对数坐标（request 占比太大）
- 显示具体数值标签

### 6.3 图表在报告中的引用

```markdown
## 6. 可视化分析

### 6.1 每日错误趋势

![每日错误趋势](../charts/daily_trend.png)

从图中可以看出...
```

---

## 7. 数据统计结果

### 7.1 日志级别分布

| 级别 | 数量 | 占比 |
|------|------|------|
| error | 38,081 | 67.6% |
| notice | 13,755 | 24.5% |
| warn | 168 | 0.3% |
| 格式异常 | 4,478 | 7.9% |

### 7.2 时间范围

- 起始时间：2005-06-09
- 结束时间：2006-02-28
- 总天数：230 天
- 平均每天错误数：166 条

### 7.3 主要错误类型（Top 5）

| 排名 | 错误类型 | 数量 | 占比 | 根因分析 |
|:----:|----------|------|------|----------|
| 1 | FILE_NOT_FOUND | 20,861 | 54.8% | 客户端请求的文件不存在，可能是爬虫扫描或链接失效 |
| 2 | DIR_INDEX_FORBIDDEN | 6,745 | 17.7% | 目录索引被禁止，安全配置生效 |
| 3 | MODJK_WORKER_ERROR | 4,349 | 11.4% | mod_jk 与后端 Tomcat 连接异常 |
| 4 | SCRIPT_NOT_FOUND | 3,301 | 8.7% | CGI 脚本不存在，可能是扫描攻击 |
| 5 | MODJK_INIT | 1,259 | 3.3% | mod_jk 子进程初始化失败 |
