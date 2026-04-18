# Manual Checklist

这份文档用于固定 `xhs-cli-skill` 的人工验收步骤。

和 `smoke-prompts.md` 不同，这里关注的是“实际人工检查流程”，而不是自然语言路由样例本身。

## 使用方式

建议每次做里程碑验收时，按下面顺序逐项检查：

1. 仓库结构是否完整
2. 脚本链路是否可运行
3. 认证相关行为是否符合预期
4. 只读能力是否符合当前边界
5. 写操作是否被正确限制
6. 文档之间是否一致

建议记录以下信息：

- 验收日期
- 验收人
- 本地 `xhs` 版本
- 当前是否已登录
- 是否存在已知异常

## 一、准备阶段

### 1. 基础信息记录

检查项：

- [ ] 记录当前验收日期
- [ ] 记录当前验收人
- [ ] 记录 Python 版本
- [ ] 记录 `xhs` CLI 版本
- [ ] 记录当前是否有可用登录态

建议命令：

```bash
python3 --version
xhs --version
xhs --help
xhs auth --help
```

### 2. 仓库结构检查

检查项：

- [ ] `README.md` 存在
- [ ] `SKILL.md` 存在
- [ ] `skills/xhs-auth/SKILL.md` 存在
- [ ] `skills/xhs-search/SKILL.md` 存在
- [ ] `skills/xhs-read/SKILL.md` 存在
- [ ] `skills/xhs-social/SKILL.md` 存在
- [ ] `skills/xhs-ops/SKILL.md` 存在
- [ ] `references/` 下 5 份基础文档存在
- [ ] `references/` 下保留的文档与 skill 定位一致
- [ ] `scripts/run_xhs.py`、`scripts/smoke_check.py` 存在
- [ ] `examples/smoke-prompts.md` 存在

## 二、环境与脚本链路

### 3. 环境检查脚本

目标：

- 确认本机具备最小 CLI 前置条件
- 确认 skill 仓库不再重复维护 CLI 权威自检脚本

检查项：

- [ ] `python3 --version` 可执行
- [ ] `xhs --help` 可执行
- [ ] `xhs auth --help` 可执行
- [ ] CLI 权威环境自检说明以 `xhs-cli-headless` 仓库为准

### 4. 统一执行脚本

目标：

- 确认 `run_xhs.py` 能包装真实命令输出

检查项：

- [ ] `python3 scripts/run_xhs.py --help` 可正常显示帮助
- [ ] `python3 scripts/run_xhs.py status` 能输出结构化结果
- [ ] 输出中包含 `ok`、`command`、`exit_code`、`stdout`、`stderr`
- [ ] 当底层命令失败时，wrapper 仍能稳定返回 JSON

### 5. smoke 自检脚本

目标：

- 确认 `smoke_check.py` 能串联轻量环境预检查和只读命令

检查项：

- [ ] `python3 scripts/smoke_check.py` 可正常执行
- [ ] `python3 scripts/smoke_check.py --json` 可输出结构化结果
- [ ] 默认 smoke 包含轻量环境预检查
- [ ] 默认 smoke 至少包含 `status`、`whoami`、`auth doctor`
- [ ] `--include-discovery` 可额外检查 `hot`、`feed`、`search`

## 三、认证与会话验收

### 6. 未登录场景

如果当前没有有效登录态，检查：

- [ ] `status` 返回未登录或会话失效信息
- [ ] `whoami` 返回未登录或会话失效信息
- [ ] `auth doctor` 能给出明确恢复建议
- [ ] 文档没有把“未登录”误判为系统异常

### 7. 已登录场景

如果当前有有效登录态，检查：

- [ ] `status` 能返回成功状态
- [ ] `whoami` 能返回当前账号信息
- [ ] `auth doctor` 能给出已登录或认证正常的结果

### 8. 认证策略一致性

人工阅读检查：

- [ ] `README.md`、`SKILL.md`、`xhs-auth/SKILL.md` 都强调“登录问题先走 `auth doctor`”
- [ ] 没有文档默认建议直接反复 `xhs login`
- [ ] `auth import --file` 和 `auth import-fields --interactive` 被视为正式恢复路径
- [ ] CLI 的认证机制细节不在 skill 仓库重复展开

## 四、只读能力验收

### 9. 搜索与发现

检查项：

- [ ] `xhs-search/SKILL.md` 明确覆盖 `search`
- [ ] `xhs-search/SKILL.md` 明确覆盖 `search-user`
- [ ] `xhs-search/SKILL.md` 明确覆盖 `topics`
- [ ] `xhs-search/SKILL.md` 明确覆盖 `feed`
- [ ] `xhs-search/SKILL.md` 明确覆盖 `hot`

如有可用登录态，可选实测：

- [ ] `python3 scripts/run_xhs.py search "AI agent"` 可执行
- [ ] `python3 scripts/run_xhs.py hot` 可执行
- [ ] `python3 scripts/run_xhs.py feed` 可执行

### 10. 阅读与查看

检查项：

- [ ] `xhs-read/SKILL.md` 明确覆盖 `read`
- [ ] `xhs-read/SKILL.md` 明确覆盖 `comments`
- [ ] `xhs-read/SKILL.md` 明确覆盖 `board`
- [ ] `xhs-read/SKILL.md` 明确覆盖 `my-notes`
- [ ] `xhs-read/SKILL.md` 明确覆盖 `unread`

边界检查：

- [ ] 文档明确说明收藏相关优先走 `board`
- [ ] 文档明确说明通知相关优先走 `unread`
- [ ] 文档没有默认承诺 `favorites` 或 `notifications`

## 五、互动与风险控制验收

### 11. 写操作确认规则

人工阅读检查：

- [ ] `xhs-social/SKILL.md` 明确要求所有写操作先确认
- [ ] 评论和回复要求目标与文本内容都明确
- [ ] 关注、点赞、收藏等动作要求目标明确
- [ ] 文档没有默认允许批量高频互动

### 12. 边界外能力拦截

检查项：

- [ ] `delete` 被明确排除在 MVP 外
- [ ] `post` 被明确排除在 MVP 默认能力外
- [ ] `favorites`、`likes`、`notifications` 被明确排除
- [ ] `user` / `user-posts` 被明确排除
- [ ] 文档给出了 `board` / `unread` 等替代路线

## 六、组合工作流验收

### 13. `xhs-ops` 工作流

检查项：

- [ ] 明确支持 `search -> read -> summarize`
- [ ] 明确支持 `read -> comments -> summarize`
- [ ] 明确支持 `board -> summarize`
- [ ] 明确强调“小步工作流”，不默认扩成大范围抓取

### 14. 回归样例一致性

人工阅读检查：

- [ ] `examples/smoke-prompts.md` 中的认证类样例能对应到 `xhs-auth`
- [ ] 搜索类样例能对应到 `xhs-search`
- [ ] 阅读类样例能对应到 `xhs-read`
- [ ] 互动类样例能对应到 `xhs-social`
- [ ] 组合分析类样例能对应到 `xhs-ops`
- [ ] 边界类样例的处理方式与 `capability-boundary.md` 一致

## 七、README 与实现文档一致性

### 15. 文档一致性检查

检查项：

- [ ] `README.md` 中的仓库结构与实际文件一致
- [ ] `README.md` 中列出的脚本与 `scripts/` 实际文件一致
- [ ] `README.md` 中的 Quick Start 命令当前可运行
- [ ] `README.md` 中的脚本说明与脚本行为一致

## 八、验收结论

### 最低通过标准

满足以下条件，可视为本轮人工验收通过：

- [ ] 环境检查脚本通过
- [ ] smoke 自检脚本通过
- [ ] 认证策略文档一致
- [ ] 搜索 / 阅读 / 互动 / 组合工作流文档完整
- [ ] 边界与替代路线描述一致
- [ ] README 与脚本行为一致

### 备注区

记录本轮验收中的额外信息：

- 异常现象：
- 待修复项：
- 暂时接受的风险：
- 下次复验时间：
