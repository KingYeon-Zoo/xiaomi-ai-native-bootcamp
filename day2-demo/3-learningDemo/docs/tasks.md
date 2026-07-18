# Tasks — 小红书文案生成器

> 用于指导 AI 完成项目的任务清单

---

## Task 1: 环境准备

**目标**：项目可运行

- [x] 创建 `requirements.txt`（langchain、langchain-openai、pytest、python-dotenv）
- [x] 创建 `.env.example`（OPENAI_API_KEY 配置说明）
- [ ] 创建 `.env`（用户自行填写真实 API key）
- [x] 创建 `.gitignore`（排除 .env、.venv、__pycache__）
- [x] 创建 `.venv` 虚拟环境

**环境方案**：.venv + pip（不依赖 uv 等额外工具，方便他人验证）

**验证**：
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Task 2: 核心模块实现

**目标**：代码可运行，能生成文案

- [x] `src/prompt.py` — PromptTemplate 定义 + 建议备选项常量
- [x] `src/collector.py` — 信息收集逻辑（必填校验、建议显示）
- [x] `src/generator.py` — LLMChain 调用，生成文案（从 .env 读取 API key）
- [x] `src/main.py` — 主入口，while True 循环 + quit 退出

**API 配置**：通过 `python-dotenv` 读取 `.env` 中的 `OPENAI_API_KEY`

**验证**：配置 .env 后，`python src/main.py` 输入信息后生成文案

---

## Task 3: 自动测试

**目标**：测试可运行，全部通过（不消耗 API 额度）

- [x] `src/test_main.py` — pytest 测试，**全部 mock**
- [x] mock LLM 调用，验证 PromptTemplate 填充和调用参数
- [x] 测试用例覆盖：正常流程 + 必填为空异常 + 可选字段跳过
- [x] 测试用例匹配 PRD 验收标准

**测试策略**：全部 mock，不真实调用 API，确保测试可重复运行

**验证**：`pytest src/test_main.py` 全部 PASS（无需配置 API key）

---

## Task 4: 文档更新

**目标**：交付物完整

- [x] `learning-record.md` — 补充"我不知道"的实际学习结果
- [x] `test-record.md` — 填写测试结果（命令+期望+实际+PASS/FAIL）
- [x] `ai-log.md` — 补充实现阶段的决策记录

**验证**：文档内容完整，符合任务要求

---

## Task 5: 最终提交

**目标**：代码和文档全部提交

- [x] 检查所有文件是否已 git add
- [x] 撰写清晰的 commit message
- [x] 确认文件结构完整

**验证**：`git log` 可见完整提交历史
