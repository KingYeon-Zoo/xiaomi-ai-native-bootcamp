"""自动测试 - pytest + mock"""

import pytest
from unittest.mock import patch, MagicMock

from prompt import PROMPT_TEMPLATE, SUGGESTIONS
from collector import collect_info, collect_field, is_exit_command


# ============================================================
# Prompt 模板测试
# ============================================================


class TestPromptTemplate:
    """测试 PromptTemplate"""

    def test_template_has_variables(self):
        """模板包含必要变量"""
        assert "product" in PROMPT_TEMPLATE.input_variables
        assert "target_user" in PROMPT_TEMPLATE.input_variables
        assert "style" in PROMPT_TEMPLATE.input_variables

    def test_template_fill(self):
        """模板变量正确填充"""
        result = PROMPT_TEMPLATE.format(
            product="测试产品", target_user="测试用户", style="种草"
        )
        assert "测试产品" in result
        assert "测试用户" in result
        assert "种草" in result

    def test_suggestions_exist(self):
        """建议备选项存在"""
        assert len(SUGGESTIONS["product"]) > 0
        assert len(SUGGESTIONS["target_user"]) > 0
        assert len(SUGGESTIONS["style"]) > 0


# ============================================================
# 退出命令测试
# ============================================================


class TestExitCommand:
    """测试退出命令"""

    def test_quit_command(self):
        """quit 命令识别"""
        assert is_exit_command("quit") is True
        assert is_exit_command("Quit") is True
        assert is_exit_command("QUIT") is True

    def test_exit_command(self):
        """exit 命令识别"""
        assert is_exit_command("exit") is True
        assert is_exit_command("Exit") is True

    def test_normal_text(self):
        """普通文本不是退出命令"""
        assert is_exit_command("小米SU7") is False
        assert is_exit_command("大学生") is False


# ============================================================
# 信息收集测试
# ============================================================


class TestCollectField:
    """测试单字段收集"""

    @patch("builtins.input", return_value="小米SU7")
    def test_normal_input(self, mock_input):
        """正常输入"""
        result = collect_field("product", required=True)
        assert result == "小米SU7"

    @patch("builtins.input", return_value="quit")
    def test_quit_returns_none(self, mock_input):
        """输入 quit 返回 None"""
        result = collect_field("product", required=True)
        assert result is None

    @patch("builtins.input", side_effect=["", "小米SU7"])
    def test_required_empty_then_valid(self, mock_input):
        """必填字段为空后重新输入"""
        result = collect_field("product", required=True)
        assert result == "小米SU7"

    @patch("builtins.input", return_value="")
    def test_optional_empty_returns_default(self, mock_input):
        """可选字段为空返回默认值"""
        result = collect_field("style", required=False)
        assert result == "（无）"


class TestCollectInfo:
    """测试完整信息收集"""

    @patch("builtins.input", side_effect=["小米SU7", "大学生", "种草"])
    def test_collect_all_fields(self, mock_input):
        """收集所有字段"""
        result = collect_info()
        assert result == {
            "product": "小米SU7",
            "target_user": "大学生",
            "style": "种草",
        }

    @patch("builtins.input", side_effect=["小米SU7", "大学生", ""])
    def test_collect_with_optional_empty(self, mock_input):
        """可选字段跳过"""
        result = collect_info()
        assert result == {
            "product": "小米SU7",
            "target_user": "大学生",
            "style": "（无）",
        }

    @patch("builtins.input", side_effect=["quit"])
    def test_quit_on_first_field(self, mock_input):
        """第一个字段输入 quit"""
        result = collect_info()
        assert result is None

    @patch("builtins.input", side_effect=["小米SU7", "quit"])
    def test_quit_on_second_field(self, mock_input):
        """第二个字段输入 quit"""
        result = collect_info()
        assert result is None

    @patch("builtins.input", side_effect=["", "小米SU7", "大学生", "种草"])
    def test_required_empty_retry(self, mock_input):
        """必填字段为空后重试"""
        result = collect_info()
        assert result["product"] == "小米SU7"


# ============================================================
# LLM 调用测试（Mock）
# ============================================================


class TestGenerator:
    """测试文案生成（Mock LLM）"""

    @patch("generator.create_chain")
    def test_generate_calls_chain(self, mock_create_chain):
        """验证 chain 调用"""
        from generator import generate_copywriting

        # Mock chain.invoke
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "测试文案"
        mock_chain.invoke.return_value = mock_response
        mock_create_chain.return_value = mock_chain

        # 调用
        result = generate_copywriting(
            {"product": "小米SU7", "target_user": "大学生", "style": "种草"}
        )

        # 验证调用
        mock_chain.invoke.assert_called_once_with(
            {"product": "小米SU7", "target_user": "大学生", "style": "种草"}
        )
        assert result == "测试文案"

    @patch("generator.create_chain")
    def test_generate_with_default_style(self, mock_create_chain):
        """默认风格（无）也能正常调用"""
        from generator import generate_copywriting

        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "测试文案"
        mock_chain.invoke.return_value = mock_response
        mock_create_chain.return_value = mock_chain

        result = generate_copywriting(
            {"product": "小米SU7", "target_user": "大学生", "style": "（无）"}
        )

        mock_chain.invoke.assert_called_once()
        assert result == "测试文案"
