"""错误筛选模块 - 筛选 error 日志，分类错误类型"""

import pandas as pd

# 错误分类规则
ERROR_RULES = [
    ('MODJK_WORKER_ERROR', 'mod_jk child workerEnv'),
    ('MODJK_INIT', 'mod_jk child init'),
    ('JK2_CHILD_NOT_FOUND', "jk2_init() Can't find"),
    ('BEAN_CREATE_ERROR', 'env.createBean2()'),
    ('CONFIG_ERROR', 'config.update()'),
    ('FILE_NOT_FOUND', 'File does not exist'),
    ('DIR_INDEX_FORBIDDEN', 'Directory index forbidden'),
    ('SCRIPT_NOT_FOUND', 'script not found'),
    ('URI_TOO_LONG', 'URI too long'),
    ('URIMAP_ERROR', 'uriMap.mapUri()'),
    ('INVALID_METHOD', 'Invalid method'),
]

# 错误类型对应的模块
MODULE_MAP = {
    'MODJK_WORKER_ERROR': 'mod_jk',
    'MODJK_INIT': 'mod_jk',
    'JK2_CHILD_NOT_FOUND': 'mod_jk',
    'BEAN_CREATE_ERROR': 'config',
    'CONFIG_ERROR': 'config',
    'FILE_NOT_FOUND': 'request',
    'DIR_INDEX_FORBIDDEN': 'request',
    'SCRIPT_NOT_FOUND': 'request',
    'URI_TOO_LONG': 'request',
    'URIMAP_ERROR': 'other',
    'INVALID_METHOD': 'request',
    'REQUEST_ERROR': 'request',
}

# 错误类型描述
ERROR_DESCRIPTIONS = {
    'FILE_NOT_FOUND': '文件不存在 (404)',
    'DIR_INDEX_FORBIDDEN': '目录索引被禁止',
    'MODJK_WORKER_ERROR': 'mod_jk worker 连接后端失败',
    'SCRIPT_NOT_FOUND': 'CGI 脚本不存在',
    'MODJK_INIT': 'mod_jk 子进程初始化失败',
    'JK2_CHILD_NOT_FOUND': 'jk2 子进程找不到',
    'BEAN_CREATE_ERROR': 'Bean 创建错误',
    'CONFIG_ERROR': '配置更新失败',
    'URI_TOO_LONG': 'URI 过长',
    'URIMAP_ERROR': 'URI 映射错误',
    'INVALID_METHOD': '无效请求方法',
    'REQUEST_ERROR': '其他请求错误',
}


def classify_error(content: str) -> str:
    """
    错误分类

    Args:
        content: 日志内容

    Returns:
        str: 错误类型代码
    """
    for error_type, keyword in ERROR_RULES:
        if keyword in content:
            return error_type
    return 'REQUEST_ERROR'


def filter_errors(df: pd.DataFrame) -> pd.DataFrame:
    """
    筛选 error 级别日志并添加分类

    Args:
        df: structured_logs DataFrame (timestamp, level, content)

    Returns:
        DataFrame: 包含 timestamp, content, error_type, module 列
    """
    error_df = df[df['level'] == 'error'].copy()
    error_df['error_type'] = error_df['content'].apply(classify_error)
    error_df['module'] = error_df['error_type'].map(MODULE_MAP)
    return error_df[['timestamp', 'content', 'error_type', 'module']].reset_index(drop=True)


def get_error_reference() -> pd.DataFrame:
    """
    获取错误类型对照表

    Returns:
        DataFrame: 包含 error_code, description, module 列
    """
    data = []
    for error_code, _ in ERROR_RULES:
        data.append({
            'error_code': error_code,
            'description': ERROR_DESCRIPTIONS[error_code],
            'module': MODULE_MAP[error_code]
        })
    # 添加 REQUEST_ERROR (兜底类型)
    data.append({
        'error_code': 'REQUEST_ERROR',
        'description': ERROR_DESCRIPTIONS['REQUEST_ERROR'],
        'module': MODULE_MAP['REQUEST_ERROR']
    })
    return pd.DataFrame(data)
