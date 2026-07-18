# Day4 测试与验收记录

> 本文件只记录实际执行结果。当前状态：功能、全量数据与提交审计 PASS。

## 环境

- 日期：2026-07-15（Asia/Shanghai）
- macOS arm64
- 系统 Python：3.9.6，缺少 pandas/matplotlib/scikit-learn/pytest，未用于验收
- 项目环境：`.venv`，Python 3.12.13，依赖按 `requirements.txt` 安装成功

## 用例记录

| ID | 输入 | 预期 | 实际 | 结果 |
|---|---|---|---|---|
| ENV-1 | `.venv/bin/python -m pip install -r requirements.txt` | 依赖安装完成 | pandas 2.3.1、matplotlib 3.10.3、scikit-learn 1.7.1、pytest 8.4.1 安装完成 | PASS |
| UT-1a | P1/P2 首次联合 pytest | 应完成收集并执行全部用例 | 收集阶段失败：两个非包测试目录的 `test_integration.py` 顶层模块重名；尚未执行断言 | FAIL |
| UT-1b | 两个 tests 目录增加 `__init__.py` 后复测 | 同名测试模块隔离，全部用例执行 | 仍在收集阶段失败：两个目录的包名都为 `tests`，根因是默认 prepend 导入模式而不只是缺少 `__init__.py` | FAIL |
| UT-1c | 配置 pytest `--import-mode=importlib` 后复测 | 按文件位置隔离同名模块，执行全部用例 | 成功收集 19 个用例并开始执行；后续暴露业务/Expected 问题 | PASS（收集问题已修复） |
| UT-1d | 首次完成断言执行 | 业务断言全部通过 | 17 PASS / 1 FAIL；失败用例把 `FREE!!! Pay $100 NOW` 的大写率误算为大于 0.8，人工逐字母复算应恰为 0.8；同时发现父项目未成包可能造成同名测试解析歧义 | FAIL（测试 Expected Result 错误） |
| UT-1e | 修正精确 Expected Result、隔离项目包后复测 | 19 个用例通过 | 18 PASS / 1 FAIL：NB 的 `min_df=2` 在 4 条 Smoke Test 中剪枝后无词可用；这是小样本行为缺陷，不是测试错误 | FAIL |
| UT-1f | 将受 `max_features` 约束的 Vectorizer 改为 `min_df=1` 后复测 | 小样本训练和全部回归通过 | 19 passed；后续最终复测仍为 19 passed | PASS |
| E2E-1 | Apache.tar.gz 全量入口 | 生成 5 个 CSV、3 张图、报告 | parsed=52,004、invalid=4,478、error=38,081；全部指定产物非空 | PASS |
| E2E-2 | 六个邮件包全量入口 | 生成 cleaned CSV、4 张图、报告与可复现指标 | total=7,449、train=5,959、test=1,490；NB=0.9564/0.9885/0.9120/0.9487 | PASS |
| DATA-1 | 独立读取 P1 输出复算 | 级别、状态码、模块率与报告一致 | error=38,081、notice=13,755、warn=168、error state=4,349、workerEnv=4,349/10,057=43.24% | PASS |
| DATA-2 | 独立读取 cleaned_data.csv | 样本、标签、切分、来源一致 | 7,449；ham=4,153、spam=3,296；六来源计数与数据说明一致；raw 空 49、cleaned 空 160 | PASS |
| VIS-1 | 人工查看模块图、指标对比图、NB 混淆矩阵 | 中文不乱码、坐标与数字可读 | 三图均可读；NB 矩阵显示 [[824,7],[58,601]] | PASS |
| REV-1 | 模块 Error 率反例 | 修改前失败、修改后通过 | 前：LDAP=0.5/mod_jk=0.5；后：LDAP=1.0/mod_jk=0.5；产品 diff 仅 2 文件 | PASS |
| AUDIT-1 | 文件清单与 Skill 审计 | 无 BLOCKED | 初次因题目必交文档在项目根目录而 BLOCKED；改为 docs 唯一正文 + 题目路径符号链接后通过；最终回归曾因 pytest 重建 `.pytest_cache/README.md` 再次触发路径 BLOCKED，禁用 cacheprovider 后复审 39 PASS / 0 WARNING / 0 BLOCKED | PASS |
| GIT-1 | 小米 GitLab 私有 `day4-submission` 项目 | main 推送成功且远端 commit 等于本地 HEAD | 在 Day2 同一命名空间创建私有项目；`git push -u origin main` 成功；最终用 `git ls-remote origin refs/heads/main` 与 `git rev-parse HEAD` 比对 | PASS |

## 非阻断告警

pytest 最终产生 48 条第三方弃用告警，来自 matplotlib/pyparsing 与 NumPy timedelta 兼容路径；没有测试失败，也没有本项目 CJK 缺字告警。该风险不影响当前结果，但升级 matplotlib/NumPy 后应回归图表生成。
