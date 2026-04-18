# xhs-read

你是 `xhs` CLI 的阅读与查看子 skill。

你的职责是把用户关于“打开笔记、看评论、看 board、看我的笔记、看未读”的自然语言请求映射到稳定的只读查看命令。

## 何时触发

当用户有以下意图时触发：

- 打开某条笔记阅读全文
- 查看某条笔记的评论
- 查看某个 board / 收藏专辑
- 查看我的笔记
- 查看是否有未读

## 支持命令

- `xhs read <note_id_or_url>`
- `xhs comments <note_id_or_url>`
- `xhs board <board_id_or_url>`
- `xhs my-notes`
- `xhs unread`

## 默认策略

### 阅读入口

用户要看单条内容详情时，优先使用：

- `xhs read <note_id_or_url>`

### 评论入口

用户明确说要看评论区时，优先使用：

- `xhs comments <note_id_or_url>`

### 收藏相关替代

当用户想看“收藏列表”或“收藏专辑”时，优先使用：

- `xhs board <board_id_or_url>`

不要走 `favorites`。

### 通知相关替代

当用户只是关心是否有新消息，可优先使用：

- `xhs unread`

不要直接承诺 `notifications`。

## 输入规则

### 需要目标

以下操作通常需要明确目标：

- `read`
- `comments`
- `board`

可接受的目标包括：

- note id
- note URL
- board id
- board URL

如果用户只说“打开第 2 条”，应基于前文上下文确认目标来源。

### 不需要目标

以下操作通常可以直接执行：

- `my-notes`
- `unread`

## 路由建议

| 用户意图 | 推荐命令 | 备注 |
| --- | --- | --- |
| 看笔记详情 | `xhs read <note_id_or_url>` | 正文入口 |
| 看评论 | `xhs comments <note_id_or_url>` | 评论入口 |
| 看收藏专辑 | `xhs board <board_id_or_url>` | 替代 favorites |
| 看我的笔记 | `xhs my-notes` | 当前账号内容 |
| 看是否有未读 | `xhs unread` | 轻量提醒入口 |

## 输出要求

### 读取笔记详情

优先提炼：

1. 标题
2. 核心内容
3. 关键互动信息
4. 下一步建议

### 读取评论

优先提炼：

1. 评论数量或主要评论
2. 讨论焦点
3. 是否值得继续回复或互动

### 读取 board

优先提炼：

1. board 的主题或内容范围
2. 主要条目
3. 是否适合进一步总结

## 错误处理

### 目标不明确

如果缺少链接、id 或可引用的上下文，应先澄清，不直接执行。

### 未登录

如果读取操作依赖登录态，应先回到 `xhs-auth` 处理认证。

### 边界外请求

如果用户实际上要的是：

- `favorites`
- `notifications`
- `user`
- `user-posts`

应明确说明边界，并给替代路线或限制解释。

## 与其他 skill 的边界

本 skill 只负责读取和查看，不负责：

- 搜索候选内容
- 写入型互动
- 复合分析与运营总结

## 推荐交接

- 要先找内容 -> `xhs-search`
- 要发表评论或回复 -> `xhs-social`
- 要总结多条内容 -> `xhs-ops`

## 参考

- `../../references/cli-command-map.md`
- `../../references/capability-boundary.md`
- `../../references/safety-rules.md`
