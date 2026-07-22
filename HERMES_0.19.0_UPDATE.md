# Hermes Agent 0.19.0 更新摘要
本文记录 Hermes Agent 0.19.0 相比 0.18.0 的主要更新。0.19.0 对应发布标签 `v2026.7.20`，包含 0.18.1 和 0.18.2 的全部更新。

## 版本概览
| 项目 | 内容 |
| --- | --- |
| 发布日期 | 2026 年 7 月 20 日 |
| 对比范围 | `v2026.7.1...v2026.7.20` |
| 提交数量 | 约 2,245 个 |
| 合并 PR | 约 1,065 个 |
| 变更文件 | 约 2,465 个 |
| 关闭 Issue | 约 3,300 个 |
| 参与贡献者 | 450 多人 |

## 性能与交互速度
- 将首次对话从提交到分发的耗时从约 4.3 秒降至约 0.9 秒，覆盖 CLI、Gateway、TUI、桌面端和 Cron
- 默认实时显示推理过程，并按 token 刷新回复框
- 增加提示词构建缓存、时区解析缓存、模型元数据探测缓存和技能发现缓存
- 支持混合工具调用批次并发执行，减少请求体大小估算中的重复序列化
- 支持 TUI 按 Markdown 块增量渲染流式内容
- 将桌面端流式 Markdown 分割器的 CPU 开销降低约 14 倍
- 支持桌面端虚拟化渲染大型 Diff，优化长会话切换、侧边栏更新、工具调用渲染和文件树刷新
- 在 Node 清单未变化时跳过 `hermes update` 中的 npm 安装

## Agent、推理与委派
- 默认启用智能审批，由独立模型审核需要审批的单条命令
- 支持用户自定义拒绝规则，拒绝规则在 yolo 模式下仍然生效
- 新增 `/deny <reason>`，向 Agent 传递拒绝原因
- 新增 `max` 和 `ultra` 推理强度，覆盖 CLI、TUI、桌面端和模型路由
- 支持按模型设置 `reasoning_effort`，并支持为辅助任务和 MoA 各槽位分别设置推理强度
- 支持通过 `reference_max_tokens` 限制 MoA 参考模型输出
- 支持按用户轮次控制 MoA 扇出频率
- 为 `delegate_task` 返回可实时查看的子 Agent 转录文件
- 持久化后台委派结果，进程重启后继续恢复和投递完成结果
- 统一委派并发上限，并弃用 `max_async_children`
- 增强 Codex app-server 运行时的工具卡片、过程消息、上下文压缩、截断恢复和用量重置

## 模型与提供商
- 新增 Fireworks AI、DeepInfra 和 Upstage Solar 提供商
- 新增 GPT-5.6 Sol、Terra、Luna 及 Pro 变体
- 新增 grok-4.5、moonshotai/kimi-k3、claude-fable-5、claude-sonnet-5 和 tencent/hy3
- 支持 LM Studio 按需加载本地模型
- 支持 Kimi 系列 Anthropic 端点的自适应推理
- 支持 GLM-5.2 原生 `reasoning_effort`
- 支持为 LLM API 请求配置额外 HTTP 头
- 支持 API Server 按客户端选择模型路由
- 支持通过提供商配置中的 `enabled: false` 或 `excluded_providers` 隐藏不使用的提供商
- 增强 Bedrock 实时上下文窗口探测、地理前缀、价格和新模型目录
- 优化桌面端和 TUI 的提供商分组与模型选择器

## 密钥、配置与用量
- 新增可扩展的 `SecretSource` 接口
- 支持从 Bitwarden 和 1Password 读取密钥
- 支持同时启用多个密码库，并显示密钥来源、优先级和冲突警告
- 新增 `hermes config get` 和 `hermes config unset`
- 对未知的顶层配置项发出警告，并通过 doctor 报告已弃用配置项
- 新增 `display.timestamp_format`
- 按辅助任务记录模型用量，并在辅助模型、MoA 和委派调用中记录 Nous Portal 会话标签
- 为 `hermes -z` 新增 `--usage-file`，输出 JSON 格式的成本、token 和会话用量

## 会话与数据管理
- 新增 `hermes sessions export`，支持导出 Markdown、Quarto、HTML、仅提示词和 Hugging Face trace 格式
- 支持按时间、工作区和平台筛选导出内容
- 支持使用 `--redact` 清理导出内容中的密钥
- 支持关联经过上下文压缩的会话分支，生成完整逻辑会话导出
- 扩展会话 prune 筛选条件，并支持批量归档
- 新增 `/sessions search <query>`
- 在恢复会话时恢复对应工作目录
- 将 Gateway 会话元数据和路由索引统一存入 `state.db`
- 将 `sessions.json` 调整为可选的旧版镜像
- 通过 `api_content` 旁路数据保存原始 API 内容
- 增强上下文压缩中的用户意图、任务交接、多模态内容和提示词缓存保留

## Gateway、Profile 与投递可靠性
- 新增持久化投递账本，在 Gateway 重启后重新投递尚未确认送达的最终回复
- 支持单个 Gateway 按服务器、频道或线程把消息路由到不同 Profile
- 保持不同 Profile 的配置、技能、记忆和密钥相互隔离
- 新增 `GATEWAY_MULTIPLEX_PROFILES` 多 Profile 覆盖配置
- 支持按频道覆盖模型和系统提示词
- 持久化每个会话的 `/model` 覆盖配置
- 默认关闭会话自动重置
- 增加会话级轮次租约、统一重置边界和运行时就绪检查
- 支持 Webhook 负载筛选、路由脚本和平台 HTTP 事件回调
- 支持配置长任务状态提示语
- 为 Relay 新增通用 OIDC 客户端凭证配置
- 增强 Nous 登录状态检查和 Docker 启动时的会话自修复

## CLI 与 TUI
- 新增 `/subscription`，查看套餐、剩余额度、套餐变更价格和生效时间，并执行或撤销套餐变更
- 新增 `/topup`，在终端中完成额度充值
- 新增 `/model --once`，仅在下一轮临时切换模型
- 支持连续调用多个技能，例如 `/skill-a /skill-b 执行任务`
- 新增 `--safe-mode` 故障排查模式
- 支持卸载预演
- 新增 `/compact` 别名和上下文压缩预览参数
- 支持刷新 TUI 模型选择器
- 新增 Hermes Console REPL
- 新增 `hermes curator usage` 全技能用量视图
- 在 `hermes plugins list` 中显示入口点插件

## 消息平台
- 在 Telegram、Discord 和 Matrix 中为 `/reasoning`、`/fast` 提供原生选项按钮
- 为 WhatsApp 增加原生投票、位置消息、丰富的入站元数据和 Dashboard 配对流程
- 为 Discord 增加重连期间漏收消息恢复、自动线程标题、交互超时配置、审批提醒和管理员审批限制
- 为 Slack 增加实时工具执行状态
- 为 Telegram 增加按 Topic 配置自由回复白名单
- 使用卡片显示 Google Chat 澄清问题
- 新增 `stt.echo_transcripts`，控制是否回显语音转录文本
- 新增 `display.tool_progress: log`，以日志形式显示工具进度

## 桌面端与 Web Dashboard
- 将桌面端布局升级为可配置的面板、区域和布局树
- 新增 Capabilities 页面，统一管理 Skills、Tools、MCP 和 Hub
- 新增 Hermes Cloud 连接模式和终端执行后端选择器
- 增加快捷键提示与设置、统一 Worktree 对话框和新 Worktree 基础分支选择
- 增加后台任务状态、完成未读标记、工具调用分组和长工具任务自动滚动
- 支持为项目和会话设置颜色
- 增加记忆提供商面板、完整配置窗口、自定义模型端点、TTS/STT 提供商、Cron 模型选择器和 Profile 审批模式
- 增加界面缩放、鼠标滚轮缩放、聊天背景开关和 `/journey` 记忆图入口
- 将桌面端代码完整迁移到 TypeScript
- 在 Web Dashboard 中支持切换记忆提供商、安全导入会话、WhatsApp 配对和编辑 Discord 工具集
- 支持 Dashboard 终端保活与重连、聊天粘贴或拖放图片、移动端 OpenAI OAuth 登录
- 将 `hermes serve` 调整为不构建和挂载 Web UI 的纯无头后端

## 工具、Skills 与 MCP
- 统一使用 `mcp__server__tool` 命名 MCP 工具
- 在 `agent.log` 中显示 MCP Server 日志通知
- 为 Dashboard 和桌面端补全托管 MCP OAuth
- 支持配置 MCP OAuth 的 `redirect_uri` 和 `redirect_host`
- 在 MCP 目录中新增 Blender，并默认提供 4 个精选工具
- 新增 `security/unbroker`、`unreal-mcp` 和可选的 `mcp-oauth-remote-gateway` 技能
- 在 Browser 截断结果时保存完整快照，并将 eval 拒绝列表改为可选配置
- 扩展 Kanban 的任务创建窗口、项目目录编辑、附件工具和 CLI
- 为 Cron 增加持久化执行审计记录
- 为自托管 mem0 增加 Dashboard 后端、召回调节和设置向导模式
- 支持向 Codex 图像生成传递图片输入

## 安全与稳定性
- 将 Vertex 凭证、项目和区域解析限定在 Profile 密钥作用域
- 从子进程环境中移除 Vertex、Google 和 computer-use 敏感变量
- 对媒体、视觉和图像生成的本地文件读取统一应用凭证读取保护
- 为 aiohttp Webhook Server 和 Raft 分块请求增加请求体大小限制
- 为 V2 Webhook 签名增加时间戳约束
- 扩展 Fireworks Token 和 Telegram Bot Token 脱敏
- 使用原子写入和 `0600` 权限保存 OAuth Token
- 隔离 Anthropic 请求客户端和各 Profile 的 OAuth 文件
- 修复 WhatsApp Baileys 依赖安装，改用已发布的 `7.0.0-rc13`
- 增强 Windows 安装器、更新器和 Docker 启动流程

## 默认行为与兼容性变化
| 项目 | 0.19.0 行为 |
| --- | --- |
| 推理过程显示 | `display.show_reasoning` 默认开启 |
| 命令审批 | 智能审批默认开启 |
| 会话自动重置 | 默认关闭 |
| MCP 工具名 | 使用 `mcp__server__tool` 格式 |
| Gateway 会话索引 | 以 `state.db` 为主，`sessions.json` 仅作为可选旧版镜像 |
| 委派并发配置 | 使用统一并发上限，`max_async_children` 已弃用 |
| `hermes serve` | 仅启动无头后端，不构建或挂载 Web UI |

## 更新命令
```bash
hermes update
```

## 资料来源
- [Hermes Agent 0.19.0 官方发布说明](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20)
- [0.18.0 到 0.19.0 完整变更对比](https://github.com/NousResearch/hermes-agent/compare/v2026.7.1...v2026.7.20)
- [Hermes Agent 0.18.1 官方发布说明](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7)
- [Hermes Agent 0.18.2 官方发布说明](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7.2)
