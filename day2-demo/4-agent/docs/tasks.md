# Tasks — 训练营助教 AGENT

| Step | 任务 | 产出 | 验收方式 |
|------|------|------|----------|
| 1 | 创建项目骨架，复制 course-faq.md 知识文件 | `tools/__init__.py`、`data/course-faq.md` | 目录结构存在，course-faq.md 包含 10 条 FAQ |
| 2 | 实现 RAG 检索工具 + pytest 测试 | `tools/rag.py`、`tests/test_tools.py`（RAG 部分） | pytest 通过：正常查询返回来源、空查询提示输入、无关查询拒答、超长截断处理 |
| 3 | 实现学习管理工具 + pytest 测试 | `tools/task_manager.py`、`tests/test_tools.py`（学习管理部分） | pytest 通过：today 返回 5 个任务、submit 正常/重复/不在列表、check 列出未提交/全部完成 |
| 4 | 实现提交校验工具 + pytest 测试 | `tools/validator.py`、`tests/test_tools.py`（校验部分） | pytest 通过：缺失文件返回 BLOCKED、完整项目返回 PASS/WARNING |
| 5 | 编写 CLAUDE.md 编排配置 | `CLAUDE.md` | 包含：工具描述 + 结果校验流程 + 范围外拒答 + 失败处理 |
| 6 | 全量 pytest 验证 | 无额外文件 | `pytest tests/` 全部通过 |
