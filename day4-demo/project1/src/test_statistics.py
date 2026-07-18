"""statistics 模块测试"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
import pandas as pd
from statistics import daily_stats, type_stats, module_stats

# 项目根目录（Apache.log 所在位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, 'Apache.log')


class TestDailyStats:
    """daily_stats 单元测试"""

    def test_total_days(self):
        """测试天数在合理范围内（有 error 的天数）"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        daily = daily_stats(error_df)
        assert 200 < len(daily) < 250  # 实际 230 天，留余量

    def test_columns(self):
        """测试包含 date 和 count 列"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file(LOG_FILE)
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
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        types = type_stats(error_df)
        assert types['count'].sum() == 38081

    def test_type_count(self):
        """测试 12 种错误类型"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        types = type_stats(error_df)
        assert len(types) == 12


class TestModuleStats:
    """module_stats 单元测试"""

    def test_module_count(self):
        """测试 4 个模块"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        modules = module_stats(error_df)
        assert len(modules) == 4

    def test_total_count(self):
        """测试各模块数量之和 = 38,081"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        modules = module_stats(error_df)
        assert modules['count'].sum() == 38081
