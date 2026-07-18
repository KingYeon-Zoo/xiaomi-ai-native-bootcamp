"""visualizer 模块测试"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from visualizer import plot_daily_trend, plot_error_types, plot_modules

# 项目根目录（Apache.log 所在位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, 'Apache.log')


class TestPlotDailyTrend:
    """plot_daily_trend 单元测试"""

    def test_file_created(self, tmp_path):
        """测试图表文件生成"""
        from log_parser import parse_log_file
        from error_filter import filter_errors
        from statistics import daily_stats
        df = parse_log_file(LOG_FILE)
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
        df = parse_log_file(LOG_FILE)
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
        df = parse_log_file(LOG_FILE)
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
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        modules = module_stats(error_df)
        output = str(tmp_path / 'modules.png')
        plot_modules(modules, output)
        assert os.path.exists(output)
