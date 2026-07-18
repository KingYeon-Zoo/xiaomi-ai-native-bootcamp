#!/usr/bin/env python3
"""测试脚本：自动执行 eval-cases.json 中的所有用例"""

import json
import os
import subprocess
import sys

STATUS_FILE = "status.json"
EVAL_FILE = "eval-cases.json"
TEST_RECORD_FILE = "test-record.md"


def run_command(cmd):
    """执行命令并返回输出"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return result.stdout + result.stderr


def reset_status():
    """重置 status.json 为全 false"""
    status = {
        "spec.md": False,
        "plan.md": False,
        "tasks.md": False,
        "README.md": False,
        "ai-log.md": False
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def set_status_all_true():
    """设置 status.json 为全 true"""
    status = {
        "spec.md": True,
        "plan.md": True,
        "tasks.md": True,
        "README.md": True,
        "ai-log.md": True
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def corrupt_status():
    """损坏 status.json"""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("{invalid json content}")


def test_case_1():
    """today 命令输出任务列表"""
    reset_status()
    output = run_command("python cli.py today")
    passed = all(f in output for f in ["spec.md", "plan.md", "tasks.md", "README.md", "ai-log.md"])
    return passed, output.strip()


def test_case_2():
    """submit 正常提交"""
    reset_status()
    output = run_command("python cli.py submit spec.md")
    passed = "✅ spec.md 已提交" in output and "已提交过" not in output
    return passed, output.strip()


def test_case_3():
    """check 列出未提交文件"""
    reset_status()
    # 先提交一个
    run_command("python cli.py submit spec.md")
    output = run_command("python cli.py check")
    passed = "未提交的文件" in output and "plan.md" in output
    return passed, output.strip()


def test_case_4():
    """submit 重复提交"""
    reset_status()
    run_command("python cli.py submit spec.md")
    output = run_command("python cli.py submit spec.md")
    passed = "ℹ️  spec.md 已提交过" in output
    return passed, output.strip()


def test_case_5():
    """submit 不存在的文件"""
    reset_status()
    output = run_command("python cli.py submit fake.txt")
    passed = "❌ fake.txt 不在任务清单中" in output
    return passed, output.strip()


def test_case_6():
    """check 全部完成"""
    set_status_all_true()
    output = run_command("python cli.py check")
    passed = "🎉 全部完成！" in output
    return passed, output.strip()


def test_case_7():
    """status.json 损坏"""
    corrupt_status()
    output = run_command("python cli.py today")
    passed = "status.json 文件损坏" in output and "spec.md" in output
    return passed, output.strip()


def test_case_8():
    """status.json 不存在"""
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)
    output = run_command("python cli.py today")
    # 检查是否创建了 status.json
    file_exists = os.path.exists(STATUS_FILE)
    passed = file_exists and "spec.md" in output
    return passed, output.strip()


def main():
    """执行所有测试用例"""
    test_functions = [
        test_case_1,
        test_case_2,
        test_case_3,
        test_case_4,
        test_case_5,
        test_case_6,
        test_case_7,
        test_case_8,
    ]

    # 加载 eval-cases.json
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    results = []

    print("=" * 60)
    print("开始测试：Day2 学习任务清单助手")
    print("=" * 60)

    for i, test_func in enumerate(test_functions):
        case = cases[i]
        print(f"\n测试 {case['id']}: {case['name']}")
        print(f"输入: {case['input']}")

        try:
            passed, actual_output = test_func()
            status = "PASS" if passed else "FAIL"
        except Exception as e:
            status = "FAIL"
            actual_output = f"异常: {str(e)}"

        cases[i]["status"] = status
        results.append({
            "id": case["id"],
            "name": case["name"],
            "type": case["type"],
            "expect": case["expect"],
            "actual": actual_output,
            "status": status
        })

        print(f"预期: {case['expect']}")
        print(f"实际: {actual_output[:100]}{'...' if len(actual_output) > 100 else ''}")
        print(f"结果: {status}")

    # 更新 eval-cases.json
    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    # 生成 test-record.md
    generate_test_record(results)

    # 统计
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    print("\n" + "=" * 60)
    print(f"测试完成: {total} 条用例, {passed} 通过, {failed} 失败")
    print("=" * 60)

    return 0 if failed == 0 else 1


def generate_test_record(results):
    """生成 test-record.md"""
    with open(TEST_RECORD_FILE, "w", encoding="utf-8") as f:
        f.write("# 测试记录 — Day2 学习任务清单助手\n\n")
        f.write("## 测试结果表\n\n")
        f.write("| ID | 用例名称 | 类型 | 预期输出 | 实际输出 | 结果 |\n")
        f.write("|-----|----------|------|----------|----------|------|\n")

        for r in results:
            # 截断长文本
            expect_short = r["expect"][:50] + "..." if len(r["expect"]) > 50 else r["expect"]
            actual_short = r["actual"][:50].replace("\n", " ") + "..." if len(r["actual"]) > 50 else r["actual"].replace("\n", " ")
            f.write(f"| {r['id']} | {r['name']} | {r['type']} | {expect_short} | {actual_short} | {r['status']} |\n")

        f.write("\n## 失败分析\n\n")

        failed_cases = [r for r in results if r["status"] == "FAIL"]
        if failed_cases:
            for r in failed_cases:
                f.write(f"### 用例 {r['id']}: {r['name']}\n\n")
                f.write(f"- **类型**: {r['type']}\n")
                f.write(f"- **预期**: {r['expect']}\n")
                f.write(f"- **实际**: {r['actual']}\n")
                f.write(f"- **失败定位**: ")
                f.write(f"cli.py 实现问题 — 程序输出与预期不符\n")
                f.write(f"- **修复方向**: 检查 cli.py 中相关函数的逻辑\n\n")
        else:
            f.write("全部通过，无失败用例。\n\n")

        f.write("## 下一步\n\n")
        f.write("- 补充范围外拒答测试用例（待 RAG 场景实现后）\n")
        f.write("- 增加更多边界条件测试\n")


if __name__ == "__main__":
    sys.exit(main())
