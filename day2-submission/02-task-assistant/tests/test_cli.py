import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIR))

import cli  # noqa: E402


class TaskAssistantTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.status_file = Path(self.temp_dir.name) / "status.json"
        self.old_status = os.environ.get("DAY2_STATUS_FILE")
        os.environ["DAY2_STATUS_FILE"] = str(self.status_file)

    def tearDown(self):
        if self.old_status is None:
            os.environ.pop("DAY2_STATUS_FILE", None)
        else:
            os.environ["DAY2_STATUS_FILE"] = self.old_status
        self.temp_dir.cleanup()

    def run_main(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = cli.main(args)
        return code, output.getvalue()

    def test_today_lists_five_tasks_and_status(self):
        code, output = self.run_main(["today"])
        self.assertEqual(0, code)
        self.assertEqual(5, output.count("⬜"))
        self.assertIn("README.md", output)

    def test_submit_accepts_case_insensitive_filename(self):
        code, output = self.run_main(["submit", "readme.MD"])
        self.assertEqual(0, code)
        self.assertIn("README.md 已提交", output)
        self.assertTrue(cli.load_status()["README.md"])

    def test_duplicate_submit_returns_nonzero(self):
        self.run_main(["submit", "spec.md"])
        code, output = self.run_main(["submit", "spec.md"])
        self.assertEqual(1, code)
        self.assertIn("已提交过", output)

    def test_unknown_file_returns_nonzero(self):
        code, output = self.run_main(["submit", "fake.txt"])
        self.assertEqual(2, code)
        self.assertIn("不在任务清单", output)

    def test_check_lists_only_remaining_tasks(self):
        self.run_main(["submit", "spec.md"])
        code, output = self.run_main(["check"])
        self.assertEqual(0, code)
        self.assertNotIn("- spec.md", output)
        self.assertIn("- plan.md", output)

    def test_corrupt_status_is_reset(self):
        self.status_file.write_text("{broken", encoding="utf-8")
        code, output = self.run_main(["today"])
        self.assertEqual(0, code)
        self.assertIn("状态文件损坏", output)
        data = json.loads(self.status_file.read_text(encoding="utf-8"))
        self.assertEqual(set(cli.TASKS), set(data))

    def test_incomplete_status_is_reset(self):
        self.status_file.write_text('{"spec.md": true}', encoding="utf-8")
        _, output = self.run_main(["check"])
        self.assertIn("状态文件损坏", output)
        self.assertEqual(5, len(cli.remaining_tasks()))

    def test_no_command_prints_help_and_returns_nonzero(self):
        code, output = self.run_main([])
        self.assertEqual(2, code)
        self.assertIn("today", output)
        self.assertIn("submit", output)
        self.assertIn("check", output)


if __name__ == "__main__":
    unittest.main()
