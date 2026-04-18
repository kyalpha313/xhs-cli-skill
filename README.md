# xhs-cli-skill

`xhs-cli-skill` 是一个面向 Hermes / Agent 的小红书 skill 仓库。

它不重新实现小红书业务逻辑，而是把已经稳定发布的 `xhs` CLI 能力包装成适合 Agent 调用的 skill、规则和工作流。

一句话说，这里是 `xhs-cli-headless` 的 Agent 适配层，不是新的小红书实现层。

## 主视图

当前仓库只需要先看 4 类内容：

- 唯一入口：`SKILL.md`
- 3 个核心子 skill：`skills/xhs-auth/SKILL.md`、`skills/xhs-search/SKILL.md`、`skills/xhs-read/SKILL.md`
- 3 份核心 references：`references/capability-boundary.md`、`references/cli-command-map.md`、`references/safety-rules.md`
- 其余内容作为补充材料存在，不是第一阅读层

## Related Repos

- `xhs-cli-headless`：<https://github.com/kyalpha313/xhs-cli-headless>
  - 负责 CLI 本体、认证机制、能力口径、结构化输出和安装说明
  - 本仓库将它作为唯一 CLI 依赖与权威事实来源

## 仓库定位

- 底层能力来自 `xhs-cli-headless`
- 本仓库负责自然语言路由、风险控制、输出整理和替代路线
- 本仓库只消费 CLI 已发布、已验证的能力口径
- 未安装 CLI 时，主入口先做依赖引导，不单独拆成子 skill

## 核心范围

当前最值得先打通的是 3 条主链路：

- `xhs-auth`：登录检查、会话恢复、认证排障
- `xhs-search`：搜索笔记、搜索用户、话题、推荐、热榜
- `xhs-read`：读取正文、评论、board、我的笔记、未读

互动和组合工作流仍保留在仓库里，但不是首页主视图重点。

## 核心 references

- `capability-boundary.md`：当前 skill 明确承诺什么，不承诺什么
- `cli-command-map.md`：自然语言意图如何映射到 `xhs` 命令
- `safety-rules.md`：写操作确认、替代路线和风险边界

## Quick Start

下面是一条最小可用路径，用来确认本地已经具备调用 `xhs` CLI 的基础条件。

说明：

- CLI 的认证机制、错误模型和环境自检应以 `xhs-cli-headless` 仓库为准
- 本仓库只保留少量面向 skill 集成的说明与辅助脚本

### 1. 安装 CLI 依赖

你需要：

- 已安装 Python 3.10+
- 已安装并可执行 `xhs`
- `xhs` 已在当前 shell 的 `PATH` 中

如果你还没有安装 `xhs` CLI，请先安装 `xhs-cli-headless`：

```bash
uv tool install git+https://github.com/kyalpha313/xhs-cli-headless
```

或：

```bash
pipx install git+https://github.com/kyalpha313/xhs-cli-headless
```

安装完成后，建议先执行：

```bash
xhs login
xhs status --yaml
```

更完整的安装、认证和能力范围说明，请以 `xhs-cli-headless` 仓库 README 与 `capability-status.md` 为准。

### 2. 先看主入口和核心规则

建议按下面顺序阅读：

1. `SKILL.md`
2. `references/capability-boundary.md`
3. `references/cli-command-map.md`
4. `references/safety-rules.md`
5. `skills/xhs-auth/SKILL.md`
6. `skills/xhs-search/SKILL.md`
7. `skills/xhs-read/SKILL.md`

### 3. 运行一条基础命令

例如检查登录状态：

```bash
python3 scripts/run_xhs.py status
```

例如查看当前账号：

```bash
python3 scripts/run_xhs.py whoami
```

例如先做认证排障：

```bash
python3 scripts/run_xhs.py auth doctor
```

### 4. 运行一条偏结构化的命令

如果底层命令支持 `--json`，可以让 wrapper 自动追加：

```bash
python3 scripts/run_xhs.py --append-json-flag search "AI agent"
```

wrapper 会统一输出：

- `ok`
- `command`
- `exit_code`
- `stdout`
- `stderr`
- `stdout_json`

### 5. 运行一轮 smoke 自检

如果你想一次性确认“环境检查 + 关键只读命令链路”是否正常，可以运行：

```bash
python3 scripts/smoke_check.py
```

默认 smoke 会顺序执行：

- 轻量环境预检查
- `status`
- `whoami`
- `auth doctor`

如果你想拿到结构化报告：

```bash
python3 scripts/smoke_check.py --json
```

如果你还想顺带检查发现类只读命令：

```bash
python3 scripts/smoke_check.py --include-discovery
```

也可以自定义搜索词：

```bash
python3 scripts/smoke_check.py --include-discovery --search-query "AI agent"
```

说明：

- 默认 smoke 会把 `status`、`whoami`、`auth doctor` 的退出码 `0` 和 `1` 都视为可接受
- 这意味着“当前未登录但命令链路正常”不会被误判成 smoke 失败
- 这个设计更适合本地日常自检

## 仓库结构

```text
xhs-cli-skill/
├── README.md
├── SKILL.md
├── skills/
│   ├── xhs-auth/
│   │   └── SKILL.md
│   ├── xhs-read/
│   │   └── SKILL.md
│   ├── xhs-search/
│   │   └── SKILL.md
│   ├── xhs-social/
│   │   └── SKILL.md
│   ├── xhs-ops/
│   │   └── SKILL.md
├── references/
│   ├── capability-boundary.md
│   ├── cli-command-map.md
│   └── safety-rules.md
├── examples/
│   ├── manual-checklist.md
│   └── smoke-prompts.md
└── scripts/
    ├── smoke_check.py
    ├── run_xhs.py
```

## 调用约定

- 统一通过 `xhs` 可执行命令调用
- 优先使用结构化输出，例如 `--json`
- skill 自己负责 JSON 解析、错误分类和摘要整理
- 不直接依赖 CLI 仓库内部 Python 模块
- CLI 安装引导由主入口统一处理，不单独作为子 skill 路由

## 设计原则

- `CLI` 负责能力实现
- `skill` 负责能力编排
- 写操作必须确认
- 登录问题先走 `xhs auth doctor`
- 已知失败能力优先给替代路线
- 默认返回摘要，不直接铺开超长原始输出

## 脚本说明

### `scripts/run_xhs.py`

用于统一执行 `xhs` 命令，并返回结构化结果，便于：

- skill 侧统一处理 `stdout` / `stderr`
- 尝试解析 JSON 输出
- 保留退出码
- 在调用失败时给出统一错误格式

### `scripts/smoke_check.py`

用于串联最小只读自检流程，适合做本地快速验收。

默认会检查：

- 轻量环境预检查是否通过
- `status` 是否可调用
- `whoami` 是否可调用
- `auth doctor` 是否可调用

可选扩展：

- `hot`
- `feed`
- `search <query>`
