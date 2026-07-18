# Bug 复现记录 — task-manager

> 运行 `python3 test.py`，观察哪些测试失败。为每个失败的测试填写一份复现记录。

---

## Bug A：字符串 priority 未转换为数字

### 输入

```python
tasks = []
add_task(tasks, '重要任务', 'high')
add_task(tasks, '普通任务', 'low')
str_types = [(t['title'], type(t['priority']).__name__, repr(t['priority']))
             for t in tasks if isinstance(t['priority'], str)]
```

### 期望输出

```
str_types 为 []（priority 应被转换为 int，不存在字符串类型）
```

### 实际输出

```
str_types = [('普通任务', "str", "'low'"), ('重要任务', "str", "'high'")]
priority 保留原始字符串，未做 int() 转换，导致后续排序/过滤按字符串规则执行
```

### 环境信息

- Python 版本：3.12
- 复现命令：`python test.py`

### 复现步骤

1. 运行 `python test.py`
2. 观察测试 3（异常输入）断言失败，提示 priority 未做 int() 转换
3. 在 `src/task_manager.py` 中确认 `priority` 被原样写入任务字典，未做转换

---

## Bug B：空字符串/纯空格 title 未抛异常

### 输入

```python
add_task([], '', 1)
add_task([], '   ', 1)
```

### 期望输出

```
两次调用都应抛出 ValueError，且错误信息中包含 "title"
```

### 实际输出

```
两次调用都没有抛出异常；空字符串和纯空格字符串被写入任务字典，导致测试 2 断言失败
```

### 环境信息

- Python 版本：3.12
- 复现命令：`python test.py`

### 复现步骤

1. 运行 `python test.py`
2. 观察测试 2（边界输入 — 空 title）两个断言都失败
3. 在 `src/task_manager.py` 中确认 `add_task()` 只对 `title` 做了 `strip()`，没有检查结果是否为空
