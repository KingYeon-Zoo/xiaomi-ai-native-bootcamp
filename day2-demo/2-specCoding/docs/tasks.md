# Tasks — Day2 学习任务清单助手

| Step | 任务 | 产出 | 验收方式 |
|------|------|------|----------|
| 1 | 创建 `cli.py` 骨架，实现命令行参数解析 | `cli.py` 能解析 `today`/`submit`/`check` 三个子命令 | `python cli.py --help` 显示三个命令说明 |
| 2 | 实现 `today` 命令 | `today` 函数，输出 5 个任务文件名及描述 | `python cli.py today` 输出 5 行任务信息 |
| 3 | 实现 `status.json` 读写逻辑 | `load_status()` / `save_status()` 函数 | 手动运行后生成 `status.json`，内容为 5 个 `false` |
| 4 | 实现 `submit` 命令 | `submit` 函数，处理正常/重复/不存在三种情况 | `python cli.py submit spec.md` → 提示已提交；重复提交 → 提示已提交过；`submit fake.txt` → 提示不在清单中 |
| 5 | 实现 `check` 命令 | `check` 函数，列出未提交文件或提示全部完成 | `python cli.py check` 列出未提交文件；全部提交后 → 提示"全部完成！" |
| 6 | 端到端测试 | 无额外文件 | 按 spec.md 验收标准 6 条逐一跑通 |
