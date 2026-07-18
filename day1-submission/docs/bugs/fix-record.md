# task-manager 最小修复与回归

## 修复 A：统一优先级类型

- 在 `add_task()` 中先尝试 `int(priority)`。
- 对 `high/medium/low` 使用 `5/3/1` 别名映射；无法识别时回退为 `0`。
- 不修改排序、列表复制或过滤逻辑，避免无关回归。

## 修复 B：拒绝空标题

- `title.strip()` 后立即检查非空。
- 为空时抛出 `ValueError('title must not be empty')`。
- 不增加长度、字符白名单或转义规则，因为不属于课程复现范围。

## 回归结果

执行：

```bash
python3 bug-fix-lab/test.py
```

实际：7 条断言通过、0 条失败；正常排序、空字符串、纯空格、字符串优先级、列表副本和优先级过滤均覆盖。完整执行环境和结果见 `docs/test-record.md`。
