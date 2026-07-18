"""error_filter 模块测试"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
import pandas as pd
from error_filter import classify_error, filter_errors, get_error_reference

# 项目根目录（Apache.log 所在位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, 'Apache.log')


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
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        assert len(error_df) == 38081

    def test_columns(self):
        """测试包含必要列"""
        from log_parser import parse_log_file
        df = parse_log_file(LOG_FILE)
        error_df = filter_errors(df)
        assert 'error_type' in error_df.columns
        assert 'module' in error_df.columns

    def test_error_type_coverage(self):
        """测试覆盖 12 种错误类型"""
        from log_parser import parse_log_file
        df = parse_log_file(LOG_FILE)
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
