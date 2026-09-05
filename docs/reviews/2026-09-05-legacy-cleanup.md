# 历史源码清理记录

按仓库所有者指示，删除以下不再维护的历史源码副本及相关执行脚本。未重写 Git 历史，其他对象保持不变。

删除前提交：`bd27a279f5febe4e09b7d99c50defcba471269a0`。

- `day3-demo/tripSplit`
- `day3-submission/backend`
- `day3-submission/frontend`
- `day3-submission/check-submission.sh`
- `day4-demo/project2`
- `day4-submission/project1`
- `day4-submission/project2`
- `day4-submission/requirements.txt`
- `day4-submission/pytest.ini`
- `day4-submission/check-submission.sh`
- `day5-submission-Loops Aget/src`
- `day5-submission-Loops Aget/ppt_build`
- `day5-submission-Loops Aget/start.sh`

验证：逐层比对 Git 树，除上述路径、首页说明和本记录外，其他文件的对象哈希必须一致。此操作移除当前分支上的旧实现，不宣称修复了历史提交里的依赖。
