# Plan：Day2 学习任务清单助手

## 模块划分

| 模块 | 入口 | 职责 |
|------|------|------|
| CLI 路由 | `main(argv)` | 解析 today/submit/check，打印结果并返回退出码 |
| 状态存储 | `load_status()` / `save_status()` | 初始化、校验、重建和持久化 JSON |
| 任务服务 | `submit_task()` / `remaining_tasks()` | 执行任务规则，不负责参数解析 |
| 自动测试 | `tests/test_cli.py` | 用隔离临时状态验证正常、边界和失败路径 |

## 数据结构

```python
TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志",
}

# status.json
{"spec.md": false, "plan.md": false, "tasks.md": false,
 "README.md": false, "ai-log.md": false}
```

`false` 表示未提交，`true` 表示已提交。生产默认路径与 `cli.py` 同目录；测试通过 `DAY2_STATUS_FILE` 指向临时文件。

## 数据流

```text
argv → argparse → 命令服务 → load_status → 规则判断 → save_status → 中文输出/退出码
```

## 风险与应对

| 风险 | 影响 | 应对 | 验证 |
|------|------|------|------|
| JSON 被手动破坏 | 命令崩溃或状态不可信 | 校验键集合和值类型，不合法即重建 | 损坏与字段不完整用例 |
| README 大小写差异 | 合法任务被拒绝 | 小写比较、保留规范名称输出 | `readme.MD` 用例 |
| 测试污染真实状态 | 作业进度被重置 | 环境变量覆盖到临时目录 | 每条测试独立 setUp/tearDown |
| 未知文件修改状态 | 清单出现非法键 | 校验后再加载和保存 | `fake.txt` 用例 |
