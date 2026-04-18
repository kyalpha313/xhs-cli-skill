# Capability Boundary

这份文档定义 `xhs-cli-skill` 当前阶段承诺的真实能力边界。

核心原则只有一句话：

只包装稳定 CLI 能力，不把隐藏命令和已知失败命令误暴露给 Agent。

## 一、默认支持

以下能力已经进入 `xhs` 当前默认命令面，可作为 skill MVP 的正式输入面。

### 认证与会话

- `xhs login`
- `xhs login --qrcode-http`
- `xhs status`
- `xhs whoami`
- `xhs auth doctor`
- `xhs auth inspect`
- `xhs auth import --file`
- `xhs auth import-fields --interactive`
- `xhs logout`

### 只读发现与阅读

- `xhs search`
- `xhs search-user`
- `xhs topics`
- `xhs feed`
- `xhs hot`
- `xhs read`
- `xhs comments`
- `xhs my-notes`
- `xhs unread`
- `xhs board`

### 互动与社交

- `xhs like`
- `xhs like --undo`
- `xhs favorite`
- `xhs unfavorite`
- `xhs comment`
- `xhs reply`
- `xhs delete-comment`
- `xhs follow`
- `xhs unfollow`

## 二、默认隐藏但仍保留

这些命令暂时不进入 skill MVP 默认路由：

- `xhs post`
- `xhs login --browser`
- `xhs login --qrcode`

处理规则：

- 不主动暴露
- 不写入默认命令映射
- 不作为主 skill 的默认建议

## 三、隐藏且已知失败

这些命令当前不应接入 skill：

- `xhs delete`
- `xhs sub-comments`
- `xhs user`
- `xhs user-posts`
- `xhs favorites`
- `xhs likes`
- `xhs notifications`

处理规则：

- 主 skill 必须拦截
- 不允许静默尝试
- 优先返回替代路线或边界说明

## 四、替代路线

当用户触发未承诺能力时，优先使用下面的稳定替代路径：

| 用户需求 | 不要走 | 推荐替代 |
| --- | --- | --- |
| 查看收藏列表 | `favorites` | `board <board_id_or_url>` |
| 检查是否有新消息 | `notifications` | `unread` |
| 查看用户主页和发帖 | `user` / `user-posts` | 说明当前不承诺 |
| 删除自己发布的内容 | `delete` | 说明当前不承诺 |

## 五、路由含义

skill 侧应显式识别三种状态：

- `supported`：已支持，可直接路由
- `hidden`：保留但不默认使用
- `blocked`：已知失败或明确不承诺

## 六、MVP 内外边界

### MVP 内

- 登录检查
- 登录失败排障
- 搜索与发现
- 读取详情与评论
- 读取 board
- 查看未读
- 评论、回复、点赞、收藏、关注
- 搜索后的摘要整理

### MVP 外

- 发布
- 删除
- 用户主页能力承诺
- 收藏列表 API
- notifications 能力承诺
- sub-comments 能力承诺

## 七、文档同步规则

每次 CLI 发布面变化时，需要同步更新：

1. 本文档
2. `references/cli-command-map.md`
3. `SKILL.md`
4. 相关子 skill 文档
