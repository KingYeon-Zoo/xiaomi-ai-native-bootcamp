# test_rag.py — RAG 助手自动化测试
# 覆盖 questions.json 的 13 个测试用例
# 自动启停 mock_server.py
# 运行: python tests/test_rag.py

import json
import os
import re
import socket
import subprocess
import sys
import time

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')
MOCK_SERVER = os.path.join(BASE_DIR, 'llm-mock', 'mock_server.py')
MAIN_PY = os.path.join(BASE_DIR, 'src', 'main.py')
MOCK_PORT = 9876
MOCK_WAIT_TIMEOUT = 10  # seconds


def wait_for_port(port, timeout=MOCK_WAIT_TIMEOUT):
    """等待端口就绪"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def start_mock_server():
    """启动 mock server，返回 subprocess.Popen"""
    proc = subprocess.Popen(
        [sys.executable, MOCK_SERVER],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=BASE_DIR,
    )
    if not wait_for_port(MOCK_PORT):
        proc.kill()
        raise RuntimeError(f'mock server 未能在 {MOCK_WAIT_TIMEOUT}s 内启动')
    return proc


def stop_mock_server(proc):
    """停止 mock server"""
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def run_main(question):
    """运行 src/main.py，返回 stdout 字符串"""
    try:
        result = subprocess.run(
            [sys.executable, MAIN_PY, question],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=BASE_DIR,
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return '[TIMEOUT]'
    except Exception as e:
        return f'[ERROR] {e}'


def check_case(case, output):
    """验证单个测试用例，返回 (passed, detail)"""
    expected_type = case['expected_type']
    expected_keywords = case.get('expected_keywords', [])
    expected_source = case.get('expected_source')
    expected_sources = case.get('expected_sources')

    # 超长输入特殊处理：只验证不报错
    if case.get('category') == '边界' and '超长' in case.get('note', ''):
        if output and '[ERROR]' not in output and '[TIMEOUT]' not in output:
            return True, '不报错，有输出'
        return False, f'输出异常: {output[:80]}'

    if expected_type == 'prompt_input':
        for kw in expected_keywords:
            if kw in output:
                return True, f'包含 "{kw}"'
        return False, f'未包含 {expected_keywords}'

    if expected_type == 'refuse':
        for kw in expected_keywords:
            if kw in output:
                return True, f'拒答，包含 "{kw}"'
        return False, f'未拒答，输出: {output[:80]}'

    if expected_type == 'refuse_or_handle':
        for kw in expected_keywords:
            if kw in output:
                return True, f'拒答，包含 "{kw}"'
        return False, f'未拒答，输出: {output[:80]}'

    if expected_type == 'answer_with_source':
        # 检查关键词
        kw_pass = any(kw in output for kw in expected_keywords)
        # 检查来源
        source_pass = True
        source_detail = ''
        if expected_source:
            source_pass = expected_source in output
            source_detail = f'来源 {expected_source}'
        elif expected_sources:
            source_pass = any(s in output for s in expected_sources)
            source_detail = f'来源 {expected_sources}'
        else:
            # 至少检查有 [faq-XX] 格式
            source_pass = bool(re.search(r'\[faq-\d{2}\]', output))
            source_detail = '来源格式 [faq-XX]'

        if kw_pass and source_pass:
            return True, f'关键词命中 + {source_detail}'
        problems = []
        if not kw_pass:
            problems.append(f'缺少关键词 {expected_keywords}')
        if not source_pass:
            problems.append(f'缺少 {source_detail}')
        return False, '; '.join(problems)

    return False, f'未知 expected_type: {expected_type}'


def main():
    print('RAG 助手自动化测试\n')

    # 加载测试用例
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        cases = json.load(f)
    print(f'加载 {len(cases)} 个测试用例\n')

    # 启动 mock server
    print('启动 mock server...')
    try:
        mock_proc = start_mock_server()
        print(f'mock server 已启动 (PID {mock_proc.pid})\n')
    except Exception as e:
        print(f'❌ 无法启动 mock server: {e}')
        sys.exit(1)

    passed = 0
    failed = 0

    try:
        for i, case in enumerate(cases, 1):
            category = case.get('category', '?')
            question = case['question']
            note = case.get('note', '')

            display_q = question if len(question) <= 30 else question[:30] + '...'
            print(f'{i:2d}. [{category}] "{display_q}"')

            output = run_main(question)
            ok, detail = check_case(case, output)

            if ok:
                print(f'    ✅ {detail}')
                passed += 1
            else:
                print(f'    ❌ {detail}')
                if output:
                    print(f'    实际输出: {output[:100]}')
                failed += 1

        print('')
        print('=' * 40)
        print(f'结果: {passed} 通过, {failed} 失败')
        print('=' * 40)

    finally:
        print('\n关闭 mock server...')
        stop_mock_server(mock_proc)
        print('mock server 已关闭')

    sys.exit(1 if failed > 0 else 0)


if __name__ == '__main__':
    main()
