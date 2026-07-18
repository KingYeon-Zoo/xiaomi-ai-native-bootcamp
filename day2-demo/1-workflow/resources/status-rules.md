# 状态规则

状态优先级：

```text
BLOCKED > WARNING > PASS
```

## PASS

条件：

- `project_dir` 存在。
- 所有必需文件存在。
- 所有必跑测试通过。
- README 轻量线索完整。
- ai-log 五字段标签完整。

下一步：

- 可以提交。
- 保留 `.submission-check/final-report.md` 作为检查证据。

## WARNING

条件：

- 没有 `BLOCKED` 条件。
- 但 README 缺少安装、运行、测试任一类线索。
- 或 ai-log 缺少 `目的`、`输入`、`建议`、`人工判断`、`验证` 任一标签。

下一步：

- 建议补充 README 或 ai-log。
- 修复后重新运行检查。

## BLOCKED

条件：

- `project_dir` 不存在。
- 任一必需文件缺失。
- 任一必跑测试失败。
- 任一必跑测试超时。
- 测试命令无法执行。

下一步：

- 必须先修复阻塞项。
- 修复后重新运行检查。
