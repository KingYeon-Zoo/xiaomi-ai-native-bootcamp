"""log_parser 模块测试"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
import pandas as pd
from log_parser import parse_log_line, parse_log_file, convert_date

# 项目根目录（Apache.log 所在位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, 'Apache.log')


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
        df = parse_log_file(LOG_FILE)
        assert len(df) == 52004

    def test_columns(self):
        """测试包含三列"""
        df = parse_log_file(LOG_FILE)
        assert list(df.columns) == ['timestamp', 'level', 'content']

    def test_no_null(self):
        """测试无缺失值"""
        df = parse_log_file(LOG_FILE)
        assert df.isnull().sum().sum() == 0

    def test_level_distribution(self):
        """测试日志级别分布"""
        df = parse_log_file(LOG_FILE)
        level_counts = df['level'].value_counts()
        assert level_counts['error'] == 38081
        assert level_counts['notice'] == 13755
        assert level_counts['warn'] == 168
