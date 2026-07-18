# Day2 学习任务清单助手

使用本地 JSON 保存五个作业文件的提交状态，提供 today、submit、check 三个命令。

## 安装

需要 Python 3.9+，无第三方依赖：

```bash
cd 02-task-assistant
python3 --version
```

## 运行

```bash
python3 cli.py today
python3 cli.py submit README.md
python3 cli.py check
```

状态保存在同目录 `status.json`；该运行产物被 Git 忽略。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

预期为 8 条测试全部 `ok`。

## 文件说明

- `spec.md`：目标、非目标、边界、验收。
- `plan.md`：模块、数据结构和风险。
- `tasks.md`：分步产出与验收。
- `AGENTS.md`：Agent 命令路由、拒答和失败转译。
- `eval-cases.json` / `test-record.md`：三类评估和失败定位。
- `context-pack.md`：供 AI 评审的七层上下文。

## 边界

不支持修改清单、多用户、历史记录、数据库或联网。未知文件不会写入状态；状态损坏时会明确提示并重建。
