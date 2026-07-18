# Peer Review — 课堂现有小红书文案生成器

- **评审对象**：`day2-workflow/3-learningDemo`（工作区提供的同桌/课堂现有 Demo）
- **复核日期**：2026-07-13
- **评审方法**：实际安装并运行测试，结合 README、源码和 AI 日志证据；不复用目录内已有评语作为结论。

## 1. 能运行

执行：

```bash
.venv/bin/python -m pip install -r day2-workflow/3-learningDemo/requirements.txt
cd day2-workflow/3-learningDemo
../../day2-submission/.venv/bin/python -m pytest src/test_main.py -v
```

实际：macOS、Python 3.9.6，收集 17 条用例，`17 passed in 1.54s`。Prompt、退出命令、字段收集和 mock LLM 调用均通过。

问题：没有真实 API Key，因此未执行一次真实生成；README 第 147–149 行已诚实说明模型输出和真实 API 未被测试。

## 2. README 完整

证据：README 第 12–50 行有虚拟环境、依赖、API Key 和运行命令；第 77–89 行有测试；第 91–107 行有目录结构；第 126–149 行有支持、不支持和已知限制。

发现的问题：README 声明 Python 3.12+（第 112 行），但 requirements 未固定上限或 Python marker。本次在 Python 3.9.6 仍能安装并跑完测试，说明“3.12+”更像开发环境说明而非经验证的最低版本，建议改成“已验证 3.9.6/3.12.x”或用项目元数据明确限制。

## 3. 边界诚实

### 边界问题 A：超长产品名

- 证据：`src/collector.py:22-40` 对输入只做 `strip()` 和空值判断，没有长度限制；17 条测试也没有超长输入。
- 结果：200 字产品名会原样进入 Prompt，可能破坏 README 声明的标题字数目标。
- 建议：在 Spec 明确“接受任意长度”或增加合理长度限制与边界测试。

### 边界问题 B：API Key 缺失

- 证据：`src/main.py:29-36` 在生成阶段捕获异常并提示检查 `.env`，不会直接退出主循环。
- 结果：用户得到人类可读提示，但 `except Exception` 也会把网络、解析、代码错误都误报为 Key 错误。
- 建议：分别捕获配置错误和模型调用错误，保留不同修复动作。

## 4. AI 依赖可解释

证据：`docs/ai-log.md` 每条有目的、输入、建议、人工判断、验证；例如第 24–32 行拒绝五字段输入，第 78–86 行拒绝额外的 uv 工具，第 102–120 行基于新版导入路径和 RunnableSequence 做技术取舍。

优点：不是聊天截图，明确记录采纳、修改和拒绝理由。问题：部分“验证”写“生成成功”而未给命令或实际输出路径，证据强度低于 test-record 的表格。

## 评审结论

**WARNING**。项目测试可运行，README 和边界说明较完整，AI 决策可解释；但真实 API 端到端未验证、Python 版本声明不够精确、超长输入无边界、广义异常被统一归因于 API Key。以上不阻塞学习 Demo 的 mock 验收，但需要在宣称真实可用前修正。

## 优点与建议

- 优点：17 条自动测试覆盖核心交互；README 明确不支持历史、Web UI、合规检测和联网热点；AI 日志有真实拒绝记录。
- 建议：补一条可选的真实 API smoke test、增加输入长度测试、细分异常类型，并把实际验证过的 Python 版本写准确。
