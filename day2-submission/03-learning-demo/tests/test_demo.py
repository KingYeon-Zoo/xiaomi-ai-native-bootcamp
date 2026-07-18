import sys
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIR))

import demo  # noqa: E402


class LangChainDemoTests(unittest.TestCase):
    def test_prompt_has_context_and_question_variables(self):
        self.assertEqual({"context", "question"}, set(demo.PROMPT.input_variables))

    def test_known_question_returns_answer_and_source(self):
        output = demo.run_demo("什么是可复核交付？")
        self.assertIn("可复核交付", output)
        self.assertIn("[demo-01]", output)

    def test_unknown_question_is_rejected(self):
        output = demo.run_demo("今天北京天气怎么样？")
        self.assertEqual("资料中没有找到依据。", output)

    def test_empty_question_raises_clear_error(self):
        with self.assertRaisesRegex(ValueError, "问题不能为空"):
            demo.run_demo("   ")


if __name__ == "__main__":
    unittest.main()
