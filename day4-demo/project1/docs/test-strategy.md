# 测试策略文档

## Apache HTTP 服务器日志智能清洗与故障分析工具

---

## 1. 测试策略

### 1.1 测试原则

- **测试驱动**：每个开发任务完成后必须有对应测试验证
- **自动化优先**：能用 pytest 自动化的测试优先自动化
- **真实数据**：使用 Apache.log 真实数据测试（性能测试已验证 < 1 秒）
- **人工兜底**：图表质量、报告可读性等主观指标由人工 E2E 测试

### 1.2 测试层次

| 层次 | 方式 | 覆盖范围 | 执行者 |
|------|------|----------|--------|
| 单元测试 | pytest | 每个函数的输入输出 | 自动化 |
| 集成测试 | pytest | 模块间协作、端到端流程 | 自动化 |
| E2E 测试 | 人工 | 图表质量、报告可读性 | 人工 |

### 1.3 测试执行时间

| 测试类型 | 预估耗时 |
|----------|----------|
| 单元测试（全部） | < 1 秒 |
| 集成测试 | < 2 秒 |
| E2E 人工测试 | 5-10 分钟 |

---

## 2. 测试用例

### 2.1 Lesson 1 测试用例

#### test_log_parser.py

```python
import pytest
import pandas as pd
from log_parser import parse_log_line, parse_log_file, convert_date

class TestParseLogLine:
    """parse_log_line 单元测试"""

    def test_normal_line(self):
        """测试标准格式日志"""
        line = '[Thu Jun 09 06:07:04 2005] [notice] LDAP: Built with OpenLDAP LDAP SDK'
        result = parse_log_line(line)
        assert result is not None
        assert result['timestamp'] == 'Thu Jun 09 06:07:04 2005'
        assert result['level'] == 'notice'
        assert 'LDAP' in result['content']

    def test_line_with_client(self):
        """测试包含 client 的日志"""
        line = '[Thu Jun 09 07:11:21 2005] [error] [client 204.100.200.22] Directory index forbidden by rule: /var/www/html/'
        result = parse_log_line(line)
        assert result is not None
        assert result['level'] == 'error'
        assert '[client 204.100.200.22]' in result['content']

    def test_abnormal_line(self):
        """测试格式异常行"""
        line = 'script not found or unable to stat'
        result = parse_log_line(line)
        assert result is None

    def test_empty_line(self):
        """测试空行"""
        result = parse_log_line('')
        assert result is None

class TestConvertDate:
    """convert_date 单元测试"""

    def test_june(self):
        """测试 6 月日期转换"""
        assert convert_date('Thu Jun 09 06:07:04 2005') == '2005-06-09'

    def test_february(self):
        """测试 2 月日期转换"""
        assert convert_date('Tue Feb 28 03:49:01 2006') == '2006-02-28'

    def test_december(self):
        """测试 12 月日期转换"""
        assert convert_date('Sun Dec 04 04:47:44 2005') == '2005-12-04'

class TestParseLogFile:
    """parse_log_file 集成测试"""

    def test_total_rows(self):
        """测试解析行数 = 52,004"""
        df = parse_log_file('Apache.log')
        assert len(df) == 52004

    def test_columns(self):
        """测试包含三列"""
        df = parse_log_file('Apache.log')
        assert list(df.columns) == ['timestamp', 'level', 'content']

    def test_no_null(self):
        """测试无缺失值"""
        df = parse_log_file('Apache.log')
        assert df.isnull().sum().sum() == 0

    def test_level_distribution(self):
        """测试日志级别分布"""
        df = parse_log_file('Apache.log')
        level_counts = df['level'].value_counts()
        assert level_counts['error'] == 38081
        assert level_counts['notice'] == 13755
        assert level_counts['warn'] == 168
```

#### Lesson 1 集成验证

| 验证项 | 预期结果 | 验证方式 |
|--------|----------|----------|
| structured_logs.csv 行数 | 52,004 | `wc -l` 或 pandas |
| timestamp 列无缺失 | 0 null | `df.isnull().sum()` |
| level 列无缺失 | 0 null | `df.isnull().sum()` |
| content 列无缺失 | 0 null | `df.isnull().sum()` |
| 日志级别分布 | error:38081, notice:13755, warn:168 | `value_counts()` |

---

### 2.2 Lesson 2 测试用例

#### test_error_filter.py

```python
import pytest
import pandas as pd
from error_filter import classify_error, filter_errors, get_error_reference

class TestClassifyError:
    """classify_error 单元测试"""

    def test_file_not_found(self):
        assert classify_error('File does not exist: /var/www/html/') == 'FILE_NOT_FOUND'

    def test_dir_index_forbidden(self):
        assert classify_error('Directory index forbidden by rule: /var/www/html/') == 'DIR_INDEX_FORBIDDEN'

    def test_modjk_worker_error(self):
        assert classify_error('mod_jk child workerEnv in error state 6') == 'MODJK_WORKER_ERROR'

    def test_modjk_init(self):
        assert classify_error('mod_jk child init 1 -2') == 'MODJK_INIT'

    def test_jk2_child_not_found(self):
        assert classify_error("jk2_init() Can't find child 4057 in scoreboard") == 'JK2_CHILD_NOT_FOUND'

    def test_bean_create_error(self):
        assert classify_error('env.createBean2(): Factory error creating channel.jni:jni') == 'BEAN_CREATE_ERROR'

    def test_config_error(self):
        assert classify_error("config.update(): Can't create channel.jni:jni") == 'CONFIG_ERROR'

    def test_script_not_found(self):
        assert classify_error('script not found or unable to stat: /var/www/cgi-bin/awstats') == 'SCRIPT_NOT_FOUND'

    def test_uri_too_long(self):
        assert classify_error('request failed: URI too long (longer than 8190)') == 'URI_TOO_LONG'

    def test_urimap_error(self):
        assert classify_error('uriMap.mapUri() uri must start with /') == 'URIMAP_ERROR'

    def test_invalid_method(self):
        assert classify_error('Invalid method in request GET /scripts/') == 'INVALID_METHOD'

    def test_request_error(self):
        """测试其他请求错误归为 REQUEST_ERROR"""
        assert classify_error('attempt to invoke directory handler') == 'REQUEST_ERROR'

class TestFilterErrors:
    """filter_errors 集成测试"""

    def test_error_count(self):
        """测试筛选后行数 = 38,081"""
        from log_parser import parse_log_file
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        assert len(error_df) == 38081

    def test_columns(self):
        """测试包含必要列"""
        from log_parser import parse_log_file
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        assert 'error_type' in error_df.columns
        assert 'module' in error_df.columns

    def test_error_type_coverage(self):
        """测试覆盖 12 种错误类型"""
        from log_parser import parse_log_file
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        assert error_df['error_type'].nunique() == 12

class TestGetErrorReference:
    """get_error_reference 单元测试"""

    def test_reference_count(self):
        """测试包含 12 种错误类型"""
        ref = get_error_reference()
        assert len(ref) == 12

    def test_columns(self):
        """测试包含必要列"""
        ref = get_error_reference()
        assert 'error_code' in ref.columns
        assert 'description' in ref.columns
```

#### test_statistics.py

```python
import pytest
import pandas as pd
from statistics import daily_stats, type_stats, module_stats

class TestDailyStats:
    """daily_stats 单元测试"""

    def test_total_days(self):
        """测试天数在合理范围内（有 error 的天数）"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        daily = daily_stats(error_df)
        assert 200 < len(daily) < 250  # 实际 230 天，留余量

    def test_columns(self):
        """测试包含 date 和 count 列"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        daily = daily_stats(error_df)
        assert 'date' in daily.columns
        assert 'count' in daily.columns

class TestTypeStats:
    """type_stats 单元测试"""

    def test_total_count(self):
        """测试各类型数量之和 = 38,081"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        types = type_stats(error_df)
        assert types['count'].sum() == 38081

    def test_type_count(self):
        """测试 12 种错误类型"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        types = type_stats(error_df)
        assert len(types) == 12

class TestModuleStats:
    """module_stats 单元测试"""

    def test_module_count(self):
        """测试 4 个模块"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        modules = module_stats(error_df)
        assert len(modules) == 4

    def test_total_count(self):
        """测试各模块数量之和 = 38,081"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        modules = module_stats(error_df)
        assert modules['count'].sum() == 38081
```

#### Lesson 2 集成验证

| 验证项 | 预期结果 | 验证方式 |
|--------|----------|----------|
| error_logs.csv 行数 | 38,081 | pandas |
| error_type 列无缺失 | 0 null | `isnull().sum()` |
| module 列无缺失 | 0 null | `isnull().sum()` |
| 错误类型数量 | 12 种 | `nunique()` |
| 模块数量 | 4 个 | `nunique()` |
| error_code_reference.csv | 12 行 | `len()` |

---

### 2.3 Lesson 3 测试用例

#### test_visualizer.py

```python
import pytest
import os
from visualizer import plot_daily_trend, plot_error_types, plot_modules

class TestPlotDailyTrend:
    """plot_daily_trend 单元测试"""

    def test_file_created(self, tmp_path):
        """测试图表文件生成"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        from statistics import daily_stats
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        daily = daily_stats(error_df)
        output = str(tmp_path / 'daily_trend.png')
        plot_daily_trend(daily, output)
        assert os.path.exists(output)

    def test_file_size(self, tmp_path):
        """测试图表文件大小 > 0"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        from statistics import daily_stats
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        daily = daily_stats(error_df)
        output = str(tmp_path / 'daily_trend.png')
        plot_daily_trend(daily, output)
        assert os.path.getsize(output) > 0

class TestPlotErrorTypes:
    """plot_error_types 单元测试"""

    def test_file_created(self, tmp_path):
        """测试图表文件生成"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        from statistics import type_stats
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        types = type_stats(error_df)
        output = str(tmp_path / 'error_types.png')
        plot_error_types(types, output)
        assert os.path.exists(output)

class TestPlotModules:
    """plot_modules 单元测试"""

    def test_file_created(self, tmp_path):
        """测试图表文件生成"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        from statistics import module_stats
        df = parse_log_file('Apache.log')
        error_df = filter_errors(df)
        modules = module_stats(error_df)
        output = str(tmp_path / 'modules.png')
        plot_modules(modules, output)
        assert os.path.exists(output)
```

#### Lesson 3 集成验证

| 验证项 | 预期结果 | 验证方式 |
|--------|----------|----------|
| charts/daily_trend.png | 文件存在，大小 > 0 | os.path |
| charts/error_types.png | 文件存在，大小 > 0 | os.path |
| charts/modules.png | 文件存在，大小 > 0 | os.path |
| log_analyzer/ 可导入 | import 成功 | import 语句 |
| analysis_report.md | 包含 8 个章节标题 | 文本检查 |

#### E2E 人工测试

| 验证项 | 验证标准 | 验证方式 |
|--------|----------|----------|
| 时序图可读性 | X 轴标签不重叠，趋势清晰 | 人工查看 |
| 饼图可读性 | 切片标签清晰，颜色区分明显 | 人工查看 |
| 柱状图可读性 | 数值标签可见，对数坐标有效 | 人工查看 |
| 报告可读性 | 章节完整，图表正确引用 | 人工阅读 |

---

## 3. 测试执行

### 3.1 运行测试

```bash
# 运行所有测试
# PowerShell:
pytest src/ -v -k "test_"
# Git Bash / Linux / Mac:
pytest src/test_*.py -v

# 运行单个模块测试
pytest src/test_log_parser.py -v
pytest src/test_error_filter.py src/test_statistics.py -v

# 显示详细输出
pytest src/ -v -k "test_" --tb=short
```

### 3.2 测试报告

测试完成后输出：
- 测试用例总数
- 通过/失败数量
- 失败用例详情
- 执行时间

### 3.3 持续集成

每个 Lesson 开发完成后：
1. 运行对应测试文件
2. 确认所有测试通过
3. 进行 E2E 人工测试（如需要）
4. 提交代码
