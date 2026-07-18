"""
测试数据加载工具
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_emails


def test_load_emails():
    """测试邮件加载功能"""
    df = load_emails('data')

    # 检查数据数量
    assert len(df) == 6052, f"期望6052条记录，实际{len(df)}条"

    # 检查列名
    assert 'label' in df.columns, "缺少label列"
    assert 'raw_email' in df.columns, "缺少raw_email列"
    assert 'source' in df.columns, "缺少source列"

    # 检查标签值
    valid_labels = {'ham', 'spam'}
    actual_labels = set(df['label'].unique())
    assert actual_labels.issubset(valid_labels), f"标签值不正确: {actual_labels}"

    # 检查ham和spam数量
    ham_count = len(df[df['label'] == 'ham'])
    spam_count = len(df[df['label'] == 'spam'])
    assert ham_count == 4153, f"期望4153条ham，实际{ham_count}条"
    assert spam_count == 1899, f"期望1899条spam，实际{spam_count}条"


def test_load_emails_content():
    """测试邮件内容加载"""
    df = load_emails('data')

    # 检查raw_email不为空
    empty_count = (df['raw_email'] == '').sum()
    assert empty_count == 0, f"有{empty_count}条空邮件"

    # 检查每条邮件都有内容
    for idx, row in df.head(10).iterrows():
        assert len(row['raw_email']) > 0, f"第{idx}条邮件为空"
