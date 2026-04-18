Xiaohongshu Agent Stack 项目设计文档 v0.2

**这份文档现在不再只是 CLI 早期设计稿，而是 `xhs-cli-headless` 完成 `0.8.5` 首个稳定发布后的阶段总结与下一阶段规划。它的主要用途，是为即将新开的 skill 仓库提供一份可直接延续的设计基线。**

## 1. 文档目的

这份文档回答三件事：

1. `xhs-cli-headless` 到今天为止已经做成了什么。
2. 新 skill 项目应该建立在怎样的真实 CLI 能力边界上。
3. 接下来两个仓库应该如何分工、协同和演进。

一句话总结：

- CLI 已经从“可行性探索”进入“首个稳定发行物”阶段。
- skill 项目现在可以正式独立启动。
- skill 不应该再基于最初设想去“完整覆盖所有 CLI 能力”，而应该只包装已经验证并纳入发布面的稳定命令。

## 2. 当前项目状态

截至 `0.8.5`，CLI 项目已经完成：

- 基于 `jackwener/xiaohongshu-cli` 的 fork 改造与持续维护。
- 面向无 GUI / 服务器 / Agent 场景的登录路径收敛。
- `auth doctor`、`auth inspect`、`auth import`、`auth import-fields` 等认证工具链补齐。
- 默认命令面的重新收缩，只公开当前已验证、适合承诺的能力。
- GitHub Release 与 PyPI 发布链路打通。

当前结论可以概括为：

- `xhs-cli-headless` 已是一个可安装、可发布、可维护的 CLI 产品。
- 新 skill 项目不需要再承担 CLI 探路工作，而应该把重心放在 Agent 适配、路由、规则与用户体验。

## 3. 项目总目标

整体仍然是构建一套面向 Hermes / Agent 的小红书能力栈，但现在要拆成两个阶段看：

### A. 已落地部分：CLI 产品

项目名：

- `xhs-cli-headless`

目标：

- 在无 GUI 环境中提供可安装、可验证、可脚本化的小红书 CLI。
- 以结构化输出形式暴露稳定能力。
- 为 Agent 提供一个可依赖的命令后端。

### B. 即将启动部分：独立 skill 项目

工作目标：

- 新建一个与 CLI 分离的 skill 仓库。
- 让 Agent 以自然语言调用当前稳定 CLI 能力。
- 提供路由、策略、确认、摘要和安全边界。
- 不重新实现小红书业务逻辑，只适配 CLI。

## 4. 非目标

新 skill 项目当前阶段不追求：

- 覆盖 CLI 源码中仍然隐藏或已知失败的全部能力。
- 直接绕过 CLI 去重写一套 API 调用层。
- 一开始就支持所有写操作自动化。
- 一开始就做成重型平台化系统。
- 为了“统一感”而过早做 monorepo 或大规模仓库重构。

换句话说：

当前阶段追求的是“稳定适配已发布 CLI”，不是“重新发明一整套小红书 Agent 平台”。

## 5. 总体架构

推荐架构如下：

用户 / Agent
-> Hermes Skill
-> Wrapper / command policy / confirmation rules
-> `xhs` CLI
-> Reverse-engineered XHS APIs / HTML fallback
-> local auth artifacts (`cookies.json`, session fields, diagnostics)

### A. CLI 层职责

- 与小红书交互。
- 管理登录态与 cookies。
- 提供结构化命令输出。
- 隐藏复杂逆向细节。
- 维护真实可用的默认命令面。

### B. Skill 层职责

- 把自然语言意图映射为稳定 CLI 命令。
- 控制风险边界与默认策略。
- 在写操作前进行确认。
- 对 CLI 输出做摘要、整理和二次表达。
- 给出登录失败、能力不可用、替代路径等用户友好提示。

### 设计原则

- CLI 和 skill 分仓维护。
- CLI 负责“能力实现”，skill 负责“能力编排”。
- skill 只依赖已发布口径，不依赖源码里是否还留着某个隐藏命令。
- skill 侧必须显式感知“支持 / 隐藏 / 已知失败”这三个状态。

## 6. 为什么继续采用 CLI + Skill 双仓库

这个判断在今天比项目初期更成立。

### 原因 1：CLI 已经成为独立产品

现在的 `xhs-cli-headless` 已经具备：

- 明确的默认命令面。
- 发布版本与版本号。
- GitHub Release 与 PyPI 安装路径。
- 独立 README、状态文档和验证证据。

这意味着 skill 已经有了一个明确后端，不需要继续和 CLI 混写。

### 原因 2：skill 的职责与 CLI 明显不同

skill 需要解决的问题是：

- 自然语言路由。
- 用户确认。
- 风险控制。
- 输出摘要。
- Agent 友好的体验层。

CLI 需要解决的问题是：

- API 调用。
- 登录态维护。
- HTML fallback。
- 结构化输出。
- 真机 / 真实会话验证。

这两类问题的生命周期不同，放在一个仓库里会互相牵扯。

### 原因 3：避免 skill 被过时假设拖累

项目初期曾经把很多命令视为“未来会纳入默认能力”，但经过真实验证后已经发现：

- 有些命令当前确实稳定可用。
- 有些命令当前只能隐藏保留。
- 有些命令在真实会话中已确认失败。

新 skill 仓库必须站在这个现实之上，而不是继续沿用最早那版“理论上都能接”的规划。

## 7. CLI 当前现实边界

下面这一节是整个 skill 项目的设计前提。

### 7.1 默认支持能力

截至 `0.8.5`，以下能力已经纳入默认 `xhs --help` 命令面，可作为 skill 的首批接入对象：

#### 认证与会话

- `xhs login`
- `xhs login --qrcode-http`
- `xhs status`
- `xhs whoami`
- `xhs auth doctor`
- `xhs auth inspect`
- `xhs auth import --file`
- `xhs auth import-fields --interactive`
- `xhs logout`

#### 只读发现与阅读

- `xhs search`
- `xhs search-user`
- `xhs topics`
- `xhs feed`
- `xhs hot`
- `xhs read`
- `xhs comments`
- `xhs my-notes`
- `xhs unread`

#### 互动与社交

- `xhs like`
- `xhs like --undo`
- `xhs favorite`
- `xhs unfavorite`
- `xhs board`
- `xhs comment`
- `xhs reply`
- `xhs delete-comment`
- `xhs follow`
- `xhs unfollow`

### 7.2 默认隐藏但仍保留

这些命令不应进入 skill MVP 默认路由：

- `xhs post`
- `xhs login --browser`
- `xhs login --qrcode`

其中：

- `post` 已真实成功，但因为与 `delete` 仍不构成完整闭环，暂不适合作为默认公开能力。
- `login --browser` / `login --qrcode` 是辅助路径，不应成为服务器 / Agent 默认路径。

### 7.3 隐藏且已知失败

这些命令当前不应接入 skill：

- `xhs delete`
- `xhs sub-comments`
- `xhs user`
- `xhs user-posts`
- `xhs favorites`
- `xhs likes`
- `xhs notifications`

### 7.4 已知替代路线

新 skill 需要内建替代策略，而不是把失败原样暴露给用户：

- 收藏列表相关：优先使用 `xhs board <board_id_or_url>`，不要走 `favorites`
- 通知相关：若用户只是关心是否有新消息，可优先使用 `xhs unread`
- 用户页相关：当前不承诺 `user` / `user-posts`
- creator 删除相关：当前不承诺 `delete`

## 8. 登录与认证策略

skill 项目不需要重新设计登录机制，但必须准确表达 CLI 现有策略。

### 默认主路径

- 推荐入口：`xhs login`
- 默认行为：headless 二维码登录
- 纯 HTTP 二维码仍是主要服务器路径

### 现实保底路径

- `xhs auth import --file cookies.json`
- `xhs auth import-fields --interactive`

这两条路径已经不是“备选构想”，而是已落地、已验证、应被 skill 明确支持的正式路径。

### skill 侧的默认规则

- 遇到登录问题，先建议 `xhs auth doctor`
- 诊断失败，再给出 `login` / `auth import` / `auth import-fields` 三条路径
- skill 不直接要求用户理解 cookie 细节，除非已经进入故障恢复场景

## 9. 新 skill 项目的核心目标

建议把新项目定义为：

**一个面向 Hermes / Agent 的 `xhs` CLI 适配层，而不是一个新的小红书实现层。**

这意味着它要完成的核心工作是：

1. 把用户意图映射到稳定 CLI 命令。
2. 在调用前做参数整理、上下文选择和风险控制。
3. 在调用后做结构化结果整理、摘要和错误解释。
4. 避免把 CLI 的隐藏能力和已知失败能力误暴露给 Agent。

## 10. skill 项目范围建议

### 10.1 建议项目名

可以继续用工作名：

- `xhs-cli-skill`

也可以考虑更贴近用途的名字：

- `xhs-agent-skill`
- `xiaohongshu-skill`

如果没有更强品牌诉求，建议先使用：

- `xhs-cli-skill`

原因：

- 能清楚表达它依赖 `xhs` CLI。
- 与 `xhs-cli-headless` 的关系一眼可懂。

### 10.2 建议 skill 层级

#### 1. `xiaohongshu`

主路由 skill。

职责：

- 识别用户意图。
- 路由到子 skill。
- 持有全局规则。
- 拦截高风险或超出支持面的请求。

#### 2. `xhs-auth`

职责：

- 登录状态检查。
- 登录执行与失败恢复建议。
- `auth doctor` 解释。
- `auth inspect` / `auth import` / `auth import-fields` 引导。

#### 3. `xhs-search`

职责：

- `search`
- `search-user`
- `topics`
- `feed`
- `hot`

#### 4. `xhs-read`

职责：

- `read`
- `comments`
- `board`
- `my-notes`
- `unread`

说明：

- `board` 应纳入 read 范畴，而不是继续归入“收藏 API”范畴，因为它现在本质上是对 board 页面 / fallback 的稳定读取能力。

#### 5. `xhs-social`

职责：

- `like` / `undo like`
- `favorite` / `unfavorite`
- `comment`
- `reply`
- `delete-comment`
- `follow` / `unfollow`

说明：

- 与早期文档不同，`reply` 现在已经纳入稳定默认命令面，应直接进入 skill MVP。

#### 6. `xhs-ops`

职责：

- 搜索后摘要。
- 主题热点整理。
- 竞品内容阅读与总结。
- 基于 `search` + `read` + `comments` 的组合工作流。

### 10.3 明确延后项

当前不建议进入 MVP：

- `xhs-creator`
- `xhs user`
- `xhs user-posts`
- `xhs favorites`
- `xhs likes`
- `xhs notifications`
- `xhs sub-comments`
- `xhs delete`

如果未来 CLI 状态变化，再考虑纳入。

## 11. skill 全局规则

建议在主 skill 中明确写死以下规则：

### 11.1 能力边界规则

- 只调用 CLI 当前默认支持命令。
- 默认不调用隐藏命令。
- 遇到已知失败命令，优先提供替代路线。

### 11.2 风险规则

- 写操作必须确认。
- 单次只处理用户明确指定的目标，不做批量高频。
- 不主动引导用户做平台高风险行为。

### 11.3 认证规则

- 一切登录问题先走 `xhs auth doctor`。
- 没有有效登录态时，不盲目重试业务命令。
- 诊断失败时优先推荐最短恢复路径。

### 11.4 输出规则

- 优先返回摘要，不直接铺开超长原始输出。
- 保留 CLI 原始 JSON/YAML 能力作为兜底。
- 当结果来自替代路线时，明确标注“当前使用的是 fallback / 替代命令”。

## 12. 建议目录结构

建议继续采用双仓库。

### 仓库 1：CLI

`xhs-cli-headless/`

- `README.md`
- `docs/`
- `xhs_cli/`
- `tests/`

CLI 仓库继续负责：

- 命令实现
- 认证
- API / HTML fallback
- 发布
- 验证证据

### 仓库 2：Skill

`xhs-cli-skill/`

- `SKILL.md`
- `README.md`
- `skills/`
- `references/`
- `scripts/`
- `examples/`

建议进一步细化为：

`skills/`

- `xhs-auth/SKILL.md`
- `xhs-search/SKILL.md`
- `xhs-read/SKILL.md`
- `xhs-social/SKILL.md`
- `xhs-ops/SKILL.md`

根目录：

- `SKILL.md` 作为唯一主入口

`references/`

- `cli-command-map.md`
- `capability-boundary.md`
- `safety-rules.md`

`scripts/`

- `run_xhs.py`
- `smoke_check.py`

## 13. CLI 与 skill 的接口约定

新 skill 项目应尽量把 CLI 当成稳定接口，而不是直接依赖仓库内部 Python 模块。

建议约定如下：

### 调用方式

- 统一通过 `xhs` 可执行命令调用。
- 优先使用 `--json`。
- skill 内自己处理 JSON 解析、错误分类和结果摘要。

### 依赖假设

- skill 只依赖“已发布命令语义”。
- 不依赖 CLI 内部文件结构。
- 不要求与 CLI 仓库同步发版。

### 失败分类

skill 层至少要区分：

- 未登录或登录失效
- 参数错误
- 已知失败能力
- 平台风控或校验异常
- 临时网络错误

## 14. 当前阶段计划

从现在开始，整个能力栈的规划改为 Phase B / C / D，更符合当前实际。

### Phase B：独立 Skill 仓库 MVP

目标：

- 新建 skill 仓库。
- 完成最小可用 skill 集合。
- 只接稳定 CLI 命令面。

任务：

1. 建仓库与基础目录。
2. 写主 skill 和子 skill 初版。
3. 建立 CLI 命令映射表。
4. 固化全局规则、风险规则与错误表达。
5. 提供最小安装和验证路径。

交付物：

- 独立 skill 仓库。
- 可工作的主 skill 与若干子 skill。
- 与 CLI 对齐的边界文档。

成功标准：

- Agent 默认不会调用已知失败能力。
- 用户可以通过自然语言完成登录检查、搜索、阅读、评论相关操作。
- skill 输出比直接 CLI 更适合 Agent / 用户消费。

### Phase C：统一体验层

目标：

- 让双仓库在体验上更像一个整体产品。

任务：

1. 统一安装说明。
2. 统一认证排障说明。
3. 建立跨仓库链接。
4. 补齐人类与 Agent 的 quick start。

### Phase D：品牌与形态再评估

触发条件：

- CLI 稳定持续发版。
- skill 已有稳定调用面。
- 双仓库协作模型已经跑顺。

再评估：

- 是否继续使用当前命名。
- 是否需要 GitHub org / 聚合首页。
- 是否要做统一安装器或统一文档门户。

## 15. skill MVP 建议验收标准

### 最低验收

Agent 可用自然语言完成：

- 登录状态检查
- 登录失败排障
- 搜索笔记
- 读取指定笔记
- 读取评论
- 读取 board / 收藏专辑
- 发布评论与回复评论
- 对搜索结果做摘要整理

### 边界验收

Agent 不会默认调用：

- `delete`
- `sub-comments`
- `favorites`
- `likes`
- `notifications`
- `user`
- `user-posts`

### 体验验收

- 用户不需要理解 `xhs` 全部参数细节也能完成常见任务。
- 登录问题优先被引导到 `auth doctor` 而不是盲目重试。
- 当 CLI 当前能力有限时，skill 能给出替代路线而不是简单失败。

## 16. 当前拍板建议

我建议正式采用以下路线：

- `xhs-cli-headless` 继续作为稳定 CLI 后端维护。
- 新项目以独立 skill 仓库启动，不回塞到 CLI 仓库。
- skill MVP 只包装默认支持命令。
- `reply` 与 `board` 从第一天就纳入 skill 设计，不再按旧文档视为延后项。
- `post`、`delete`、`sub-comments`、`favorites`、`notifications` 等不稳定能力，不进入 skill MVP。

## 17. 新项目的立即执行顺序

建议你在另一个项目里直接按这个顺序推进：

### Step 1

建 skill 仓库骨架：

- `README.md`
- `SKILL.md`
- `skills/`
- `references/`
- `scripts/`

### Step 2

先写三份基础文档：

- `references/cli-command-map.md`
- `references/capability-boundary.md`
- `references/safety-rules.md`

### Step 3

先做 MVP 子 skill：

- `xiaohongshu`
- `xhs-auth`
- `xhs-search`
- `xhs-read`
- `xhs-social`
- `xhs-ops`

### Step 4

做最小验证闭环：

- 安装 CLI
- 登录
- `auth doctor`
- 搜索
- `read`
- `comments`
- `board`
- `reply`

### Step 5

最后再处理体验层增强：

- 错误消息
- 摘要质量
- 确认策略
- 复合工作流
