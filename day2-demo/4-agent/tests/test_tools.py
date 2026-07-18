"""训练营助教 AGENT 工具测试"""

import pytest
import json
import os
import sys

# 确保能导入 tools 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.rag import rag_search
from tools.task_manager import task_today, task_submit, task_check, _reset_status
from tools.validator import validate_submission

FAQ_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "course-faq.md")


# ============================================================
# RAG 工具测试
# ============================================================

class TestRag:
    def test_normal_query(self):
        """正常查询应返回回答和来源"""
        result = rag_search("Day1要交什么？", FAQ_PATH)
        assert result["success"] is True
        assert len(result["sources"]) > 0
        assert "faq-" in result["sources"][0]

    def test_empty_query(self):
        """空查询应返回提示"""
        result = rag_search("", FAQ_PATH)
        assert result["success"] is False
        assert "请输入" in result["answer"]

    def test_whitespace_query(self):
        """纯空格查询应返回提示"""
        result = rag_search("   ", FAQ_PATH)
        assert result["success"] is False
        assert "请输入" in result["answer"]

    def test_no_match(self):
        """无关查询应拒答"""
        result = rag_search("奖学金政策是什么？", FAQ_PATH)
        assert result["success"] is True
        assert "没有找到依据" in result["answer"]
        assert result["sources"] == []

    def test_long_query(self):
        """超长查询应截断处理，不报错"""
        long_query = "a" * 300
        result = rag_search(long_query, FAQ_PATH)
        assert "success" in result  # 不应崩溃

    def test_has_source(self):
        """正常回答必须包含来源编号"""
        result = rag_search("什么是可复核交付", FAQ_PATH)
        assert result["success"] is True
        assert any("faq-" in s for s in result["sources"])


# ============================================================
# 学习管理工具测试
# ============================================================

@pytest.fixture(autouse=True)
def cleanup_status():
    """每个测试前重置 status.json"""
    _reset_status()
    yield
    _reset_status()


class TestTaskManager:
    def test_today(self):
        """today 应返回 5 个任务"""
        result = task_today()
        assert result["success"] is True
        assert len(result["tasks"]) == 5

    def test_submit_normal(self):
        """正常提交应成功"""
        result = task_submit("spec.md")
        assert result["success"] is True
        assert "已提交" in result["message"]

    def test_submit_not_in_list(self):
        """提交不在列表中的文件应失败"""
        result = task_submit("fake.txt")
        assert result["success"] is False
        assert "不在任务清单" in result["message"]

    def test_submit_duplicate(self):
        """重复提交应提示已提交过"""
        task_submit("spec.md")
        result = task_submit("spec.md")
        assert "已提交过" in result["message"]

    def test_check_remaining(self):
        """check 应列出未提交文件"""
        task_submit("spec.md")
        result = task_check()
        assert result["success"] is True
        assert len(result["remaining"]) == 4

    def test_check_all_done(self):
        """全部提交后应提示完成"""
        for f in ["spec.md", "plan.md", "tasks.md", "README.md", "ai-log.md"]:
            task_submit(f)
        result = task_check()
        assert "全部完成" in result["message"]


# ============================================================
# 提交校验工具测试
# ============================================================

class TestValidator:
    def test_missing_dir(self):
        """不存在的目录应返回 BLOCKED"""
        result = validate_submission("/nonexistent/path")
        assert result["status"] == "BLOCKED"

    def test_complete_project(self, tmp_path):
        """完整项目应返回 PASS 或 WARNING"""
        (tmp_path / "README.md").write_text("# 项目说明\n安装\n运行\n测试")
        (tmp_path / "agent-design.md").write_text("# Agent Design\n架构图\n工具定义\n测试用例")
        (tmp_path / "ai-log.md").write_text("# AI Log\n目的\n输入\n建议\n人工判断\n验证")
        (tmp_path / "test_tools.py").write_text("def test_pass(): assert True")
        result = validate_submission(str(tmp_path))
        assert result["status"] in ["PASS", "WARNING"]

    def test_missing_readme(self, tmp_path):
        """缺少 README 应返回 BLOCKED"""
        (tmp_path / "agent-design.md").write_text("# Agent Design\n架构图\n工具定义\n测试用例")
        (tmp_path / "ai-log.md").write_text("# AI Log\n目的\n输入\n建议\n人工判断\n验证")
        (tmp_path / "test_tools.py").write_text("def test_pass(): assert True")
        result = validate_submission(str(tmp_path))
        assert result["status"] == "BLOCKED"
        assert any("README" in f for f in result["missing_files"])
