# Context Pack — Day2 学习任务清单助手

> 上下文包，用于让 AI 理解项目背景、约束和期望输出。

---

## ① 目标

开发一个命令行任务管理工具，帮助学生管理 Day2 的学习任务。

**核心功能**：

| 命令 | 输入 | 输出 |
|------|------|------|
| `python cli.py today` | 无 | 返回 Day2 任务列表（5 个文件名 + 简要描述） |
| `python cli.py submit <文件名>` | 文件名（如 README.md） | 确认该文件已标记为已提交 |
| `python cli.py check` | 无 | 返回尚未提交的文件清单 |

**任务清单**（固定 5 个文件）：
- `spec.md` — 需求规格
- `plan.md` — 技术设计
- `tasks.md` — 任务拆解
- `README.md` — 项目说明
- `ai-log.md` — AI 协作日志

---

## ② 非目标

以下内容**明确不做**：

1. **不做 GUI** —— 纯命令行工具，不开发图形界面
2. **不做远程存储** —— 数据存在本地 JSON 文件，不联网、不用数据库
3. **不做任务编辑** —— 任务列表固定，不支持增删改
4. **不做多用户** —— 单用户设计，不支持团队协作
5. **不做历史记录** —— 只显示当前状态，不记录提交历史

---

## ③ 资料

### spec.md 关键内容

**边界条件**：

| 场景 | 处理方式 |
|------|----------|
| `submit` 一个不在任务列表中的文件 | 提示"该文件不在任务清单中" |
| `submit` 一个已经提交过的文件 | 提示"该文件已提交"，不重复标记 |
| `check` 时所有文件都已提交 | 提示"全部完成！" |
| 首次运行（`status.json` 不存在） | 自动初始化，所有文件标记为未提交 |
| `status.json` 文件损坏 | 提示错误并重新初始化 |

**验收标准**：

| # | 命令 | 期望结果 |
|---|------|----------|
| 1 | `python cli.py today` | 输出 5 个文件名及描述 |
| 2 | `python cli.py submit spec.md` | 提示"spec.md 已提交" |
| 3 | `python cli.py check` | 列出剩余 4 个未提交文件 |
| 4 | `python cli.py submit spec.md`（重复） | 提示"spec.md 已提交过" |
| 5 | `python cli.py submit fake.txt` | 提示"fake.txt 不在任务清单中" |
| 6 | 全部提交后 `python cli.py check` | 提示"全部完成！" |

### plan.md 关键内容

**模块划分**（单文件 3 个职责）：

| 模块 | 职责 |
|------|------|
| CLI 入口 | 解析命令行参数，调用对应功能 |
| 任务管理 | 加载任务列表、读写 `status.json` |
| 输出格式化 | 格式化终端输出 |

**数据结构**：

```python
# 任务列表（硬编码）
TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志"
}

# 状态文件 status.json
{
    "spec.md": false,  # false = 未提交，true = 已提交
    "plan.md": false,
    ...
}
```

**风险应对**：

| 风险 | 应对 |
|------|------|
| `status.json` 被手动删除 | 首次运行自动初始化 |
| `status.json` 被篡改为非法格式 | 捕获异常，提示错误并重新初始化 |
| 文件名大小写不一致 | 统一转小写比较 |

---

## ④ 代码

### cli.py 核心结构

```python
#!/usr/bin/env python3
"""Day2 学习任务清单助手 - 命令行工具"""

import argparse
import json
import os
import sys

# 任务列表（硬编码）
TASKS = {
    "spec.md": "需求规格",
    "plan.md": "技术设计",
    "tasks.md": "任务拆解",
    "README.md": "项目说明",
    "ai-log.md": "AI 协作日志"
}

STATUS_FILE = "status.json"


def load_status():
    """加载提交状态，如果文件不存在或损坏则初始化"""
    if not os.path.exists(STATUS_FILE):
        return init_status()
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = json.load(f)
        if not isinstance(status, dict):
            raise ValueError("status.json 格式错误")
        return status
    except (json.JSONDecodeError, ValueError):
        print("⚠️  status.json 文件损坏，已重新初始化")
        return init_status()


def init_status():
    """初始化状态文件，所有文件标记为未提交"""
    status = {filename: False for filename in TASKS}
    save_status(status)
    return status


def save_status(status):
    """保存提交状态到文件"""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def cmd_today():
    """today 命令：显示任务列表"""
    status = load_status()
    print("Day2 学习任务清单：")
    for filename, desc in TASKS.items():
        print(f"  - {filename}: {desc}")


def cmd_submit(filename):
    """submit 命令：标记文件为已提交"""
    status = load_status()
    if filename not in TASKS:
        print(f"❌ {filename} 不在任务清单中")
        return
    if status[filename]:
        print(f"ℹ️  {filename} 已提交过")
        return
    status[filename] = True
    save_status(status)
    print(f"✅ {filename} 已提交")


def cmd_check():
    """check 命令：查看未提交文件清单"""
    status = load_status()
    unsubmitted = [f for f, submitted in status.items() if not submitted]
    if not unsubmitted:
        print("🎉 全部完成！")
        return
    print("未提交的文件：")
    for filename in unsubmitted:
        print(f"  - {filename}")


def main():
    parser = argparse.ArgumentParser(description="Day2 学习任务清单助手")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    subparsers.add_parser("today", help="查看 Day2 任务列表")
    submit_parser = subparsers.add_parser("submit", help="标记文件为已提交")
    submit_parser.add_argument("filename", help="要提交的文件名")
    subparsers.add_parser("check", help="查看未提交文件清单")
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    if args.command == "today":
        cmd_today()
    elif args.command == "submit":
        cmd_submit(args.filename)
    elif args.command == "check":
        cmd_check()


if __name__ == "__main__":
    main()
```

---

## ⑤ 日志

### 测试结果

**测试统计**：

| 类型 | 用例数 | 通过 | 失败 |
|------|--------|------|------|
| 正确回答 | 6 | 6 | 0 |
| 工具失败 | 2 | 2 | 0 |
| 范围外拒答 | 4 | 4 | 0 |
| **总计** | **12** | **12** | **0** |

**关键测试用例**：

| ID | 用例 | 结果 |
|----|------|------|
| 1 | today 输出任务列表 | PASS |
| 2 | submit 正常提交 | PASS |
| 4 | submit 重复提交 | PASS |
| 5 | submit 不存在文件 | PASS |
| 6 | check 全部完成 | PASS |
| 7 | status.json 损坏 | PASS |
| 9 | 范围外：编辑任务列表 | PASS |
| 12 | 范围外：非 Day2 问题 | PASS |

---

## ⑥ 约束

### 禁止事项

1. **禁止引入第三方依赖** —— 只用 Python 标准库（argparse、json、os、sys），不使用 click、typer 等第三方 CLI 库
2. **禁止拆分多文件** —— 所有代码放在单个 `cli.py` 文件中，通过函数划分职责
3. **禁止使用数据库** —— 不使用 SQLite、MySQL 等数据库，只用 JSON 文件存储状态
4. **禁止联网** —— 所有操作本地完成，不调用远程 API
5. **禁止修改任务列表** —— 5 个任务文件名硬编码，不支持动态配置

### 技术约束

- Python 3.6+（需要 f-string 支持）
- 编码统一使用 UTF-8
- 状态文件固定为 `status.json`

---

## ⑦ 输出格式

### 命令输出格式

**today 命令**：
```
Day2 学习任务清单：
  - spec.md: 需求规格
  - plan.md: 技术设计
  - tasks.md: 任务拆解
  - README.md: 项目说明
  - ai-log.md: AI 协作日志
```

**submit 命令**：
```
✅ spec.md 已提交          # 成功
ℹ️  spec.md 已提交过       # 重复提交
❌ fake.txt 不在任务清单中  # 文件不存在
```

**check 命令**：
```
未提交的文件：             # 有未提交文件
  - plan.md
  - tasks.md
  - README.md
  - ai-log.md

🎉 全部完成！              # 所有文件已提交
```

**错误处理**：
```
⚠️  status.json 文件损坏，已重新初始化  # 状态文件损坏
```

### 状态文件格式

```json
{
  "spec.md": false,
  "plan.md": false,
  "tasks.md": false,
  "README.md": false,
  "ai-log.md": false
}
```

- `false` = 未提交
- `true` = 已提交
