# Day2 学习任务清单助手 — 任务拆分

## Task 1：冻结规格与接口

- [x] 写三个命令的输入、输出和退出码。
- [x] 写非目标和五类边界条件。
- [x] 定义 TASKS、状态 JSON 和函数接口。
- **产出**：`spec.md`、`plan.md`。
- **验收**：Spec 有 4 个目标、4 个非目标、5 个边界和 5 个可执行验收标准；Plan 有 4 个模块和 4 个风险。

## Task 2：测试先行与状态存储

- [x] 先写 8 条 unittest 用例。
- [x] 运行并观察 `ModuleNotFoundError`。
- [x] 实现 JSON 初始化、校验、重建和隔离路径。
- **产出**：`tests/test_cli.py`、`cli.py` 状态函数。
- **验收**：损坏 JSON 与字段不完整用例均自动重建，不抛堆栈。

## Task 3：实现三个命令

- [x] 实现 today 列表和状态标记。
- [x] 实现 submit 正常、重复、未知文件路径。
- [x] 实现 check 剩余清单和全部完成提示。
- **产出**：完整 `cli.py`。
- **验收**：today/submit/check 正常路径退出码为 0；未知文件为 2，重复提交为 1。

## Task 4：Eval 与失败定位

- [x] 写正确回答、范围外拒答、工具失败三类 Eval。
- [x] 记录大小写用例修复前 FAIL。
- [x] 最小修复文件名规范化并回归。
- **产出**：`eval-cases.json`、`test-record.md`。
- **验收**：JSON 合法，8 条最终状态均 PASS，测试记录保留修复前 FAIL 的归因与修复方向。

## Task 5：上下文与交付文档

- [x] 写七层 context pack。
- [x] 写 AGENTS 四块规则和 README 运行说明。
- [x] 记录 AI 协作的人工作舍。
- **产出**：`context-pack.md`、`AGENTS.md`、`README.md`、`ai-log.md`。
- **验收**：上下文七层完整；README 命令可复制运行；AI 日志每条五字段齐全。
