# CLI Command Map

这份文档定义自然语言意图如何映射到当前稳定 `xhs` CLI 命令。

## 设计原则

- 只映射默认支持命令
- 优先使用只读能力
- 写操作必须在 skill 层确认
- 已知失败能力不进入默认路由

## 认证与会话

| 用户意图 | 推荐命令 | 说明 |
| --- | --- | --- |
| 检查是否已登录 | `xhs status` | 首选快速检查 |
| 查看当前是谁登录 | `xhs whoami` | 用于识别当前账号 |
| 登录排障 | `xhs auth doctor` | 所有登录问题的首选入口 |
| 查看认证详情 | `xhs auth inspect` | 用于故障恢复 |
| 重新登录 | `xhs login` | 默认 headless 二维码路径 |
| 通过 cookies 文件恢复 | `xhs auth import --file <file>` | 故障恢复正式路径 |
| 手动输入字段恢复 | `xhs auth import-fields --interactive` | 故障恢复正式路径 |
| 退出登录 | `xhs logout` | 清理会话 |

## 搜索与发现

| 用户意图 | 推荐命令 | 说明 |
| --- | --- | --- |
| 搜索笔记 | `xhs search <query>` | 默认入口 |
| 搜索用户 | `xhs search-user <query>` | 用户发现 |
| 查看话题 | `xhs topics <query>` | 主题发现 |
| 看推荐流 | `xhs feed` | 首页推荐 |
| 看热榜 | `xhs hot` | 热门趋势 |

## 阅读与查看

| 用户意图 | 推荐命令 | 说明 |
| --- | --- | --- |
| 读取笔记详情 | `xhs read <note_id_or_url>` | 详情正文入口 |
| 看评论 | `xhs comments <note_id_or_url>` | 评论入口 |
| 看收藏专辑 / board | `xhs board <board_id_or_url>` | 替代 `favorites` |
| 查看我的笔记 | `xhs my-notes` | 当前登录用户内容 |
| 查看是否有未读 | `xhs unread` | 替代通知类需求 |

## 互动与社交

| 用户意图 | 推荐命令 | 说明 |
| --- | --- | --- |
| 点赞 | `xhs like <target>` | 写操作，必须确认 |
| 取消点赞 | `xhs like --undo <target>` | 写操作，必须确认 |
| 收藏 | `xhs favorite <target>` | 写操作，必须确认 |
| 取消收藏 | `xhs unfavorite <target>` | 写操作，必须确认 |
| 发表评论 | `xhs comment <target>` | 写操作，必须确认 |
| 回复评论 | `xhs reply <target>` | 写操作，必须确认 |
| 删除评论 | `xhs delete-comment <target>` | 写操作，必须确认 |
| 关注用户 | `xhs follow <target>` | 写操作，必须确认 |
| 取消关注 | `xhs unfollow <target>` | 写操作，必须确认 |

## 组合工作流

| 用户意图 | 组合方式 | 说明 |
| --- | --- | --- |
| 搜索后总结热门内容 | `search -> read -> summarize` | 交给 `xhs-ops` |
| 阅读评论后提炼观点 | `read -> comments -> summarize` | 交给 `xhs-ops` |
| 检查未读后给出建议 | `unread -> summarize` | 适合作为轻量提醒 |
| 查看 board 后总结收藏主题 | `board -> summarize` | 替代 favorites 列表 |

## 明确不映射

以下命令当前不应进入默认 skill 路由：

- `xhs post`
- `xhs delete`
- `xhs sub-comments`
- `xhs user`
- `xhs user-posts`
- `xhs favorites`
- `xhs likes`
- `xhs notifications`
- `xhs login --browser`
- `xhs login --qrcode`

## 路由建议

- `xhs-auth`：认证、排障、会话恢复
- `xhs-search`：搜索、话题、推荐、热榜
- `xhs-read`：详情、评论、board、我的笔记、未读
- `xhs-social`：所有互动写操作
- `xhs-ops`：组合摘要、主题整理、阅读总结
