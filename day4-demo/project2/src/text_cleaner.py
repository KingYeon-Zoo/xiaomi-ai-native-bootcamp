"""
文本清洗模块

提供邮件解析和文本清洗功能
"""

import re
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser


# 简化版停用词列表
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
    'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
    'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o',
    're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn',
    'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn',
    'weren', 'won', 'wouldn'
}


class HTMLTextExtractor(HTMLParser):
    """HTML文本提取器"""

    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        return ''.join(self.result)


def parse_email(filepath: str) -> dict:
    """
    从文件路径解析邮件（用于测试）

    Args:
        filepath: 邮件文件路径

    Returns:
        dict：
        - from: 发件人
        - subject: 主题
        - body: 正文
        - content_type: 内容类型
    """
    try:
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        # 提取邮件头
        from_addr = msg['From'] or ''
        subject = msg['Subject'] or ''

        # 提取正文
        body = ''
        content_type = 'text/plain'

        # 尝试获取纯文本正文
        text_body = msg.get_body(preferencelist=('plain',))
        if text_body:
            body = text_body.get_content()
            content_type = 'text/plain'
        else:
            # 尝试获取HTML正文
            html_body = msg.get_body(preferencelist=('html',))
            if html_body:
                html_content = html_body.get_content()
                body = html_to_text(html_content)
                content_type = 'text/html'

        return {
            'from': from_addr,
            'subject': subject,
            'body': body,
            'content_type': content_type
        }
    except Exception as e:
        return {
            'from': '',
            'subject': '',
            'body': '',
            'content_type': 'error'
        }


def parse_email_from_raw(raw_email: str) -> str:
    """
    从原始邮件内容提取正文（用于数据流）

    Args:
        raw_email: 原始邮件内容（含邮件头）

    Returns:
        str: 邮件正文
    """
    try:
        # 将字符串转换为字节
        raw_bytes = raw_email.encode('utf-8', errors='ignore')
        msg = BytesParser(policy=policy.default).parsebytes(raw_bytes)

        # 尝试获取纯文本正文
        text_body = msg.get_body(preferencelist=('plain',))
        if text_body:
            return text_body.get_content()

        # 尝试获取HTML正文
        html_body = msg.get_body(preferencelist=('html',))
        if html_body:
            html_content = html_body.get_content()
            return html_to_text(html_content)

        return ''
    except Exception as e:
        return ''


def html_to_text(html_content: str) -> str:
    """
    将HTML转换为纯文本

    Args:
        html_content: HTML内容

    Returns:
        str: 纯文本
    """
    extractor = HTMLTextExtractor()
    try:
        extractor.feed(html_content)
        return extractor.get_text()
    except Exception:
        # 如果解析失败，使用正则去除HTML标签
        clean_text = re.sub(r'<[^>]+>', ' ', html_content)
        return clean_text


def clean_text(text: str) -> str:
    """
    清洗文本（9步）

    Args:
        text: 原始文本

    Returns:
        str: 清洗后的文本
    """
    if not text:
        return ''

    # 1. 转小写
    text = text.lower()

    # 2. 去除HTML标签
    text = re.sub(r'<[^>]+>', ' ', text)

    # 3. 去除URL链接
    text = re.sub(r'http[s]?://\S+', ' ', text)
    text = re.sub(r'www\.\S+', ' ', text)

    # 4. 去除邮箱地址
    text = re.sub(r'\S+@\S+', ' ', text)

    # 5. 去除电话号码
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', ' ', text)
    text = re.sub(r'\b\d{10,}\b', ' ', text)

    # 6. 去除特殊符号和标点
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # 7. 去除多余空格
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    # 8. 去除停用词
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS]
    text = ' '.join(words)

    # 9. 过滤空消息
    if not text:
        return ''

    return text
