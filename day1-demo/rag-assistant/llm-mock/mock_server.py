# mock_server.py — LLM API 本地 Mock 服务
# 兼容 OpenAI Chat Completions API 格式
# 启动: python3 mock_server.py
# 默认端口: 9876

import os
import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get('MOCK_PORT', 9876))

# 加载 course-faq.md 的知识
faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'course-faq.md')
knowledge_base = ''

try:
    with open(faq_path, 'r', encoding='utf-8') as f:
        knowledge_base = f.read()
    print(f'已加载 FAQ 文件: {faq_path}')
except Exception as err:
    print(f'警告: 无法加载 FAQ 文件 ({err})，使用内置知识')
    knowledge_base = '''
[faq-01] 可复核交付是指助教不需要看代码，只看提交的证据文件就能独立判断。
[faq-05] RAG是检索增强生成，数据流六环节：资料源→切片→检索→Prompt拼接→来源引用→资料外拒答。
'''


def generate_mock_answer(question):
    """基于 chunk 内容的回答生成"""
    # 提取用户问题部分（answer.py 会拼接 chunk 内容 + 用户问题）
    if '用户问题：' in question:
        question = question.split('用户问题：')[-1].strip()
    lower_q = question.lower()

    # 资料外检测：否定/超出范围模式
    refuse_patterns = ['除了', '没有教', '不在', '不属于', '还有什么', '其他']
    has_refuse_signal = any(p in lower_q for p in refuse_patterns)

    # 课程关键词
    course_keywords = ['day1', '训练营', 'rag', 'faq', 'spec', 'ai-log', '提交',
                       '证据', '工具链', 'bug', '修复', '能力画像', '非目标', '可复核', 'cli',
                       'prompt', '检索', '切片', '拒答', '来源引用', '交付', '测试',
                       'git', 'commit', 'README', 'design']

    is_relevant = any(kw in lower_q for kw in course_keywords)

    # 有否定信号 + 课程关键词 → 资料外（问的是 FAQ 没覆盖的内容）
    if has_refuse_signal and is_relevant:
        return {
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': '资料中没有找到依据。本助手仅能回答 Day1 AI Native 训练营相关问题。',
                },
            }],
        }

    # 无课程关键词 → 资料外
    if not is_relevant:
        return {
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': '资料中没有找到依据。本助手仅能回答 Day1 AI Native 训练营相关问题。',
                },
            }],
        }

    # 根据关键词匹配 FAQ 内容（只匹配有 [faq-XX] 编号的 section）
    faq_sections = re.split(r'\n(?=##\s*\[faq-\d{2}\])', knowledge_base)
    relevant = []
    for section in faq_sections:
        if not re.search(r'\[faq-\d{2}\]', section):
            continue  # 跳过非 FAQ section（文件头部等）
        section_lower = section.lower()
        if any(kw in section_lower and kw in lower_q for kw in course_keywords):
            relevant.append(section)
    relevant = relevant[:3]

    if not relevant:
        return {
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': '资料中没有找到依据。本助手仅能回答 Day1 AI Native 训练营相关问题。',
                },
            }],
        }

    # 提取来源编号和内容摘要
    sources = []
    excerpts = []
    for section in relevant:
        m = re.search(r'\[faq-\d{2}\]', section)
        if m:
            sources.append(m.group(0))
        # 提取正文内容（去掉标题行，取前 200 字符）
        lines = section.strip().split('\n')
        body = '\n'.join(lines[1:]).strip()
        # 去掉 Markdown 表格行，保留纯文本内容
        body_lines = [l for l in body.split('\n') if not l.strip().startswith('|')]
        body_text = '\n'.join(body_lines).strip()
        if body_text:
            excerpts.append(body_text[:200])

    answer = '\n'.join([
        '基于课程资料，以下是相关内容：',
        '',
    ] + excerpts + [
        '',
        f'来源: {", ".join(sources)}',
    ])

    return {
        'choices': [{
            'message': {
                'role': 'assistant',
                'content': answer,
            },
        }],
    }


class MockHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_POST(self):
        # CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if self.path == '/v1/chat/completions':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')

            try:
                data = json.loads(body)
                messages = data.get('messages', [])
                question = messages[-1]['content'] if messages else ''
                print(f'[mock] 收到问题: {question[:50]}...')

                result = generate_mock_answer(question)
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            except Exception as err:
                self.wfile.write(json.dumps({'error': str(err)}, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), MockHandler)
    print(f'LLM Mock Server running at http://localhost:{PORT}')
    print(f'API endpoint: http://localhost:{PORT}/v1/chat/completions')
    print(f'')
    print(f'测试命令:')
    print(f'  curl -X POST http://localhost:{PORT}/v1/chat/completions \\')
    print(f'    -H "Content-Type: application/json" \\')
    print(f'    -d \'{{"model":"mock","messages":[{{"role":"user","content":"什么是RAG？"}}]}}\'')
    server.serve_forever()
