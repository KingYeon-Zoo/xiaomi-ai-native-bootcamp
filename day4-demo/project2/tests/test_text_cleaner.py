"""
测试文本清洗模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.text_cleaner import parse_email, parse_email_from_raw, clean_text, html_to_text


def test_parse_email():
    """测试邮件解析功能"""
    # 测试easy_ham目录中的一封邮件
    test_files = os.listdir('data/easy_ham')
    if test_files:
        filepath = os.path.join('data/easy_ham', test_files[0])
        result = parse_email(filepath)

        assert 'from' in result, "缺少from字段"
        assert 'subject' in result, "缺少subject字段"
        assert 'body' in result, "缺少body字段"
        assert 'content_type' in result, "缺少content_type字段"


def test_parse_email_from_raw():
    """测试从原始内容解析邮件"""
    # 构造测试邮件
    raw_email = """From: test@example.com
Subject: Test Email

This is a test email body."""

    body = parse_email_from_raw(raw_email)
    assert 'test email body' in body.lower(), "未能正确提取正文"


def test_clean_text():
    """测试文本清洗功能"""
    # 测试转小写
    result = clean_text('Hello WORLD')
    assert result == 'hello world', f"转小写失败: {result}"

    # 测试去除HTML标签
    result = clean_text('<p>Hello</p> <b>World</b>')
    assert '<' not in result, "HTML标签未去除"
    assert 'hello' in result, "内容丢失"

    # 测试去除URL
    result = clean_text('Visit http://example.com for more')
    assert 'http' not in result, "URL未去除"

    # 测试去除邮箱
    result = clean_text('Contact me@test.com for info')
    assert '@' not in result, "邮箱未去除"

    # 测试去除特殊符号
    result = clean_text('Hello! How are you?')
    assert '!' not in result, "感叹号未去除"
    assert '?' not in result, "问号未去除"

    # 测试去除停用词
    result = clean_text('This is a test')
    assert 'this' not in result, "停用词未去除"
    assert 'is' not in result, "停用词未去除"
    assert 'test' in result, "实词被误删"


def test_clean_text_empty():
    """测试空文本清洗"""
    result = clean_text('')
    assert result == '', "空文本应返回空字符串"

    result = clean_text(None)
    assert result == '', "None应返回空字符串"


def test_html_to_text():
    """测试HTML转文本"""
    html = '<html><body><p>Hello</p><p>World</p></body></html>'
    result = html_to_text(html)
    assert 'Hello' in result, "HTML内容丢失"
    assert 'World' in result, "HTML内容丢失"
    assert '<' not in result, "HTML标签未去除"
