import sys
import tempfile
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIR))

from check_submission import (  # noqa: E402
    FileCheckResult,
    TestRunResult,
    check_files,
    evaluate_status,
    run_tests,
)


class SubmissionWorkflowTests(unittest.TestCase):
    def test_missing_required_file_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = check_files(Path(tmp), ["README.md", "docs/spec.md"])
        self.assertEqual(["README.md", "docs/spec.md"], result.missing_files)
        self.assertEqual("BLOCKED", evaluate_status(result, TestRunResult([], [])))

    def test_failed_test_is_blocked(self):
        files = FileCheckResult([], [], {})
        tests = TestRunResult([], [{"name": "失败测试", "reason": "exit 1"}])
        self.assertEqual("BLOCKED", evaluate_status(files, tests))

    def test_document_warning_produces_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("只有项目标题", encoding="utf-8")
            (root / "ai-log.md").write_text("目的 输入", encoding="utf-8")
            result = check_files(root, ["README.md", "ai-log.md"])
        self.assertGreaterEqual(len(result.warnings), 2)
        self.assertEqual("WARNING", evaluate_status(result, TestRunResult([], [])))

    def test_complete_files_and_passing_command_are_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("安装 运行 测试", encoding="utf-8")
            (root / "ai-log.md").write_text(
                "目的 输入 建议 人工判断 验证", encoding="utf-8"
            )
            files = check_files(root, ["README.md", "ai-log.md"])
            tests = run_tests(
                root,
                [{"name": "成功测试", "command": [sys.executable, "-c", "print('ok')"]}],
                timeout_seconds=3,
            )
        self.assertEqual([], tests.failed_tests)
        self.assertEqual("PASS", evaluate_status(files, tests))

    def test_timeout_is_recorded_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tests = run_tests(
                Path(tmp),
                [{
                    "name": "超时测试",
                    "command": [sys.executable, "-c", "import time; time.sleep(2)"],
                }],
                timeout_seconds=1,
            )
        self.assertEqual(1, len(tests.failed_tests))
        self.assertIn("超时", tests.failed_tests[0]["reason"])


if __name__ == "__main__":
    unittest.main()
