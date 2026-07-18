import os
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIR))

from tools.rag import rag_search  # noqa: E402
from tools.task_manager import task_check, task_submit, task_today  # noqa: E402
from tools.validator import validate_submission  # noqa: E402


class RagToolTests(unittest.TestCase):
    def setUp(self):
        self.faq = MODULE_DIR / "data" / "course-faq.md"

    def test_known_question_returns_source(self):
        result = rag_search("什么是可复核交付？", self.faq)
        self.assertTrue(result["success"])
        self.assertIn("可复核交付", result["answer"])
        self.assertIn("faq-01", result["sources"])

    def test_unrelated_question_is_rejected(self):
        result = rag_search("奖学金怎么申请？", self.faq)
        self.assertTrue(result["success"])
        self.assertEqual("资料中没有找到依据", result["answer"])
        self.assertEqual([], result["sources"])

    def test_missing_knowledge_base_is_tool_failure(self):
        result = rag_search("提交什么", Path("/不存在/course-faq.md"))
        self.assertFalse(result["success"])
        self.assertIn("加载失败", result["answer"])

    def test_empty_query_is_rejected(self):
        result = rag_search("   ", self.faq)
        self.assertFalse(result["success"])
        self.assertIn("请输入", result["answer"])


class TaskToolTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_status = os.environ.get("AGENT_STATUS_FILE")
        os.environ["AGENT_STATUS_FILE"] = str(Path(self.temp_dir.name) / "status.json")

    def tearDown(self):
        if self.old_status is None:
            os.environ.pop("AGENT_STATUS_FILE", None)
        else:
            os.environ["AGENT_STATUS_FILE"] = self.old_status
        self.temp_dir.cleanup()

    def test_today_returns_five_tasks(self):
        self.assertEqual(5, len(task_today()["tasks"]))

    def test_submit_and_check(self):
        self.assertTrue(task_submit("spec.md")["success"])
        self.assertNotIn("spec.md", task_check()["remaining"])

    def test_duplicate_submit_is_not_success(self):
        task_submit("spec.md")
        result = task_submit("spec.md")
        self.assertFalse(result["success"])
        self.assertIn("已提交过", result["message"])

    def test_unknown_file_is_not_success(self):
        result = task_submit("secret.txt")
        self.assertFalse(result["success"])
        self.assertIn("不在任务清单", result["message"])


class ValidatorTests(unittest.TestCase):
    def test_missing_directory_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = validate_submission(Path(tmp) / "missing", Path(tmp))
        self.assertEqual("BLOCKED", result["status"])

    def test_path_outside_allowed_root_is_blocked(self):
        with tempfile.TemporaryDirectory() as allowed, tempfile.TemporaryDirectory() as outside:
            result = validate_submission(Path(outside), Path(allowed))
        self.assertEqual("BLOCKED", result["status"])
        self.assertIn("允许范围", result["details"]["project_dir"])

    def test_complete_submission_is_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            (project / "tests").mkdir(parents=True)
            (project / "README.md").write_text("安装 运行 测试", encoding="utf-8")
            (project / "agent-design.md").write_text("数据流 工具定义 校验规则 测试用例", encoding="utf-8")
            (project / "ai-log.md").write_text("目的 输入 建议 人工判断 验证", encoding="utf-8")
            (project / "tests" / "test_tools.py").write_text("测试", encoding="utf-8")
            result = validate_submission(project, root)
        self.assertEqual("PASS", result["status"])

    def test_missing_file_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            result = validate_submission(project, root)
        self.assertEqual("BLOCKED", result["status"])
        self.assertIn("README.md", result["missing_files"])

    def test_incomplete_readme_is_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            (project / "tests").mkdir(parents=True)
            (project / "README.md").write_text("项目标题", encoding="utf-8")
            (project / "agent-design.md").write_text("数据流 工具定义 校验规则 测试用例", encoding="utf-8")
            (project / "ai-log.md").write_text("目的 输入 建议 人工判断 验证", encoding="utf-8")
            (project / "tests" / "test_tools.py").write_text("测试", encoding="utf-8")
            result = validate_submission(project, root)
        self.assertEqual("WARNING", result["status"])


if __name__ == "__main__":
    unittest.main()
