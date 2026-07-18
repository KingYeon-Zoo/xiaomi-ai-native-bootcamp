# log_analyzer

Apache HTTP 服务器日志分析工具库。

## 模块说明

| 模块 | 功能 |
|------|------|
| `log_parser.py` | 日志解析（正则提取 timestamp/level/content） |
| `error_filter.py` | 错误筛选与分类（12 种错误类型） |
| `statistics.py` | 统计分析（每日/类型/模块） |
| `visualizer.py` | 可视化（时序图/饼图/柱状图） |
| `utils.py` | 工具函数 |

## 使用方式

```python
from log_analyzer import log_parser, error_filter, statistics, visualizer

# 解析日志
df = log_parser.parse_log_file('Apache.log')

# 筛选错误
error_df = error_filter.filter_errors(df)

# 统计分析
daily = statistics.daily_stats(error_df)
types = statistics.type_stats(error_df)
modules = statistics.module_stats(error_df)

# 生成图表
visualizer.plot_daily_trend(daily, 'daily_trend.png')
visualizer.plot_error_types(types, 'error_types.png')
visualizer.plot_modules(modules, 'modules.png')
```
