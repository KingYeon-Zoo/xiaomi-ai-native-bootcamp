# AI 生成代码审查清单

## 审查范围与方法

- **对象**：`review-target/unsafe_agent.py`
- **性质**：课程专用的有意不安全夹具；禁止运行或导入。
- **方法**：逐行静态检查 mission 指定的六类风险，并为每项给出位置、影响、最小修复和回归测试。
- **凭证说明**：第 6 行的 `sk-demo-key-for-review-only` 是明确无效的演示字符串，不是真实密钥；保留它是为了演示硬编码凭证检查。

## 六类风险清单

| # | 风险类型 | 位置 | 影响 | 修复方案 | 对应回归测试 |
|---|----------|------|------|----------|--------------|
| 1 | 幻觉 SDK | `unsafe_agent.py:3` | `imaginary_rag_sdk` 不存在，模块导入立即失败，服务无法启动；名字看似可信会误导评审者。 | 删除虚假依赖；改用仓库内 `tools.rag.rag_search`，并在依赖清单中只声明可安装包。 | 在干净虚拟环境运行 `python -c 'from tools.rag import rag_search'`，预期退出码 0；运行依赖安装 smoke test。 |
| 2 | 硬编码密钥 | `unsafe_agent.py:6,13` | 凭证进入源码和 Git 历史后可被复制滥用；即使删除当前行，历史仍可能泄露。 | 从环境或密钥服务读取；缺失时启动失败并给中文配置提示；对已泄露真实值立即吊销并清理历史。 | 运行 secret scanner，预期源码无凭证；清空环境后调用配置加载，预期明确失败且日志不含密钥。 |
| 3 | 任意文件读取 | `unsafe_agent.py:10-11` | 用户可传 `/etc/passwd`、`../../.env` 或符号链接读取工作目录外敏感文件。 | 使用固定知识库路径；如必须接收路径，先 `resolve()`，再验证位于 allowed root 且后缀/文件名在白名单。 | 分别提交绝对路径、`../` 和指向外部的符号链接，预期全部拒绝；允许根内 FAQ 正常读取。 |
| 4 | 资料外编造 | `unsafe_agent.py:16-18` | 检索为空时仍声称“根据资料”，用户无法区分事实与幻觉，课程规则被伪造。 | 无结果时固定返回“资料中没有找到依据”，`sources=[]`；只有来源非空才能输出基于资料的回答。 | mock RAG 返回空结果，预期固定拒答且来源为空；断言输出不含“根据资料”。 |
| 5 | 吞掉错误 | `unsafe_agent.py:12-15` | 网络、配置、解析和代码异常都被压成 `None`，无法排查，还会继续触发编造兜底。 | 捕获可预期异常类型，记录结构化错误和请求 ID；返回 `success=false` 的人类可读失败，未知异常继续上抛到统一边界。 | 让 RAG 抛 `TimeoutError`，预期记录一次超时并返回工具失败；让其抛未知异常，预期统一边界记录而非伪造答案。 |
| 6 | 只覆盖 happy path | `unsafe_agent.py:21-23` | 只有“answer 非空”的弱断言，幻觉、越界读取、吞错和假来源都可在测试通过时存在。 | 删除内嵌 demo 断言，建立独立测试模块，覆盖正常、空查询、资料外、缺库、路径越界、超时和来源一致性。 | CI 至少运行上述七类用例；对旧实现运行时，资料外/路径越界/超时用例必须能失败，证明测试有效。 |

## 审查结论

**BLOCKED**。样例在导入阶段即因幻觉 SDK 失败，同时存在硬编码凭证模式、用户可控路径读取、资料外编造、异常吞噬和测试覆盖不足。任一前三项都足以阻止部署；六项应全部修复后再进入复审。

该结论只覆盖 `review-target/unsafe_agent.py`，不代表对整个仓库完成了穷尽式安全扫描。

## 修复顺序

1. 先删除虚假 SDK 和硬编码凭证，确保项目可安装且不泄密。
2. 固定知识库根目录并阻止路径逃逸。
3. 统一 RAG 结果结构，明确区分“无资料”和“工具失败”。
4. 细分异常并加入可观测性。
5. 按每个 finding 添加回归测试，最后运行全量工具测试与 secret scan。

## 回归测试计划

```text
test_imports_only_real_rag_tool
test_missing_secret_fails_without_echoing_secret
test_absolute_parent_and_symlink_paths_are_rejected
test_empty_retrieval_returns_fixed_refusal_without_source
test_timeout_is_logged_and_returned_as_tool_failure
test_suite_covers_normal_no_match_missing_file_escape_and_timeout
```

通过标准：六项测试全部 PASS，`python3 -m unittest discover -s 04-training-agent/tests -v` 继续 13/13 PASS，敏感信息扫描仅命中本清单对风险模式的文字说明和明确无效的审查夹具。
