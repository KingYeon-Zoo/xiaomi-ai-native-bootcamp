# Context Pack — Day2 学习任务清单助手

## ① 目标

评审并实现一个本地 CLI：today 返回五个任务及状态，submit 标记一个文件已提交，check 返回未提交清单；异常必须给中文可操作提示。

## ② 非目标

不做 Web UI、账号、多用户、历史提交、动态清单、数据库或联网。不要为“以后可能需要”添加扩展点。

## ③ 资料

- `spec.md`：唯一行为边界和验收来源。
- `plan.md`：模块、数据结构、风险和测试隔离方式。
- `tasks.md`：实现顺序和每步验收。
- `AGENTS.md`：自然语言意图到命令的路由、拒答和失败转译。

上述文件均为本提交包当前版本，无 Windows 绝对路径、`CLAUDE.md` 旧命名或与现有实现冲突的规则。

## ④ 代码

```python
def submit_task(filename: str, path: Optional[Path] = None) -> CommandResult:
    canonical = next((task for task in TASKS if task.lower() == filename.lower()), None)
```

该接口只接受固定清单，返回消息与退出码；状态读写由独立函数负责。

## ⑤ 日志

修复前 `submit readme.MD` 预期 0、实际 2；根因是 `cli.py` 精确大小写比较。规范化比较后 8 条测试全部通过。完整证据见 `test-record.md`。

## ⑥ 约束

1. 只用 Python 标准库，Python 3.9+。
2. 任务键固定为 `spec.md/plan.md/tasks.md/README.md/ai-log.md`。
3. 用户输出不得显示堆栈；未知文件不得写入 JSON。
4. 状态 JSON 必须恰好含五个布尔字段，否则整体重建。

## ⑦ 输出格式

评审输出必须是：

```json
{
  "status": "PASS|WARNING|BLOCKED",
  "findings": [
    {
      "requirement": "对应的 Spec 条目",
      "evidence": "具体文件、函数或测试",
      "result": "满足或不满足",
      "action": "不满足时的最小修复"
    }
  ]
}
```

## AI 评审结果与人工判断

AI 评审认为 Spec 的三个命令、非目标、边界和验收相互一致，建议增加“提交真实文件前检查文件是否存在”。人工拒绝该建议：本工具管理的是作业进度而非文件系统事实，mission 只要求按文件名标记；强制文件存在会改变 submit 语义并让测试依赖工作目录。现有 8 条测试证明既定范围完整。
