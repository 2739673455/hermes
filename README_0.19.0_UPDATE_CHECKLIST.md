# README.md 适配 Hermes Agent 0.19.0 更新清单
本文列出将当前 `README.md` 更新到 Hermes Agent 0.19.0 时需要处理的章节和内容。目标版本为 `0.19.0`，对应标签 `v2026.7.20`。

## 处理概览
| 级别         | 范围                                                                                  |
| ------------ | ------------------------------------------------------------------------------------- |
| 必须修改     | 会话存储表述、密钥存储表述、Gateway 会话重置默认值、MCP 工具命名、`hermes serve` 定义 |
| 重点补充     | 智能审批、会话导出、子 Agent 实时转录与持久化结果、跨 Profile 消息路由                |
| 常用功能补充 | Nous 订阅管理、临时模型切换、推理强度、配置命令、技能叠加调用                         |
| 客户端补充   | 桌面端、Web Dashboard、消息平台交互能力                                               |
| 运维补充     | Cron 审计、用量文件、安全模式、密码管理器、投递账本                                   |

## 按 README 章节整理
### `2.1 安装`
- 增加 Windows 和 macOS 的 Hermes Desktop 安装入口
- 保留 Linux、macOS、WSL2 和 Windows 的命令行安装脚本
- 将现有快捷键标题改为“CLI/TUI 常用快捷键”，避免与可重新绑定的桌面端快捷键混用

### `2.2 初次配置`
- 将“密钥存储在 `~/.hermes/.env`”改为本地环境变量密钥的存储位置
- 增加 Bitwarden、1Password 和第三方 Secret Source

### `2.3 对话`
- 增加故障排查命令 `hermes chat --safe-mode`
- 增加单轮临时模型切换 `/model <model> --once`
- 增加 `/compact`，并标注其为 `/compress` 的别名
- 增加 `max` 和 `ultra` 推理强度
- 增加默认开启推理过程显示的说明

### `2.5 更新与卸载`
- 增加 `hermes update --check`，仅检查可用更新
- 增加 `updates.pre_update_backup` 的 `quick`、`full` 和 `off` 模式，并标注 `quick` 为默认值
- 增加单次更新使用的 `--backup` 和 `--no-backup`
- 按 0.19.0 CLI 帮助更新卸载参数列表
- 保留 `hermes update` 作为普通升级命令

### `2.6 Web Dashboard`
- 区分 `hermes dashboard`、`hermes serve` 和 OpenAI 兼容 API Server
- 将 `hermes dashboard` 定义为带浏览器管理界面的服务
- 增加记忆提供商切换、安全会话导入、WhatsApp 配对和 Discord 工具集编辑
- 增加终端保活与重连、聊天图片粘贴或拖放、移动端 OAuth 登录
- 增加 Gateway 拓扑、Profile 状态和运行维护入口

### 新增 `2.7 Hermes Desktop`
- 增加 Windows 和 macOS 桌面端的用途与启动入口
- 增加 Capabilities 页面，统一说明 Skills、Tools、MCP 和 Hub
- 增加终端后端、记忆提供商、自定义模型端点、TTS、STT、Cron 模型和 Profile 审批配置入口
- 增加可配置面板、后台任务状态、工具调用分组和大型 Diff 虚拟化界面
- 说明桌面端使用独立的 `hermes serve` 无头后端，不依赖 Web Dashboard

### `3.1 目录结构`
- 将 `~/.hermes/.env` 标记为本地环境变量密钥的存储位置
- 将 `auth.json` 标记为 OAuth 凭证存储
- 将 `state.db` 标记为 CLI、TUI 和 Gateway 会话元数据与完整消息历史的权威存储
- 将 `~/.hermes/sessions/sessions.json` 标记为 Gateway 路由索引
- 将 `~/.hermes/sessions/saved/*.json` 标记为 `/save` 创建的会话快照
- 将旧版 `~/.hermes/sessions/*.jsonl` 标记为不再读写的遗留转录文件

### `3.2 常用命令`
- 增加 `hermes config get <key>`
- 增加 `hermes config unset <key>`
- 增加 `hermes config check`
- 增加 `hermes config migrate`
- 说明 `hermes config check` 检查缺失或过期的配置项
- 说明配置校验会提示错放在顶层的 `base_url`、`api_key` 等 provider 字段
- 说明 `hermes doctor` 会提示已弃用的配置项和环境变量
- 增加 `display.timestamp_format`

### 在 `3. 配置管理` 下新增“密钥来源”
- 说明 `SecretSource`、Bitwarden Secrets Manager 和 1Password
- 说明多个密钥源的顺序、覆盖规则、冲突警告和来源标记
- 增加 `secrets.sources`、`secrets.bitwarden` 和 1Password `op://` 引用示例
- 说明第三方密钥源通过插件注册

### 在 `3. 配置管理` 下新增“审批规则”
- 说明 `approvals.mode` 支持 `smart`、`manual` 和 `off`
- 标注 `smart` 为 0.19.0 默认值
- 说明智能审批只批准当前命令，不创建后续命令的永久许可
- 增加 `approvals.deny` 命令匹配规则
- 说明拒绝规则在 `--yolo`、`/yolo` 和 `mode: off` 下仍然生效
- 增加 `/deny <reason>`

### 在 `3. 配置管理` 下新增“模型与提供商”
- 增加 Fireworks AI、DeepInfra 和 Upstage Solar
- 增加 GPT-5.6、grok-4.5、kimi-k3、Claude Fable 5、Claude Sonnet 5 和 tencent/hy3
- 增加 LM Studio 按需加载模式
- 增加 `providers.<name>.enabled: false` 和 `model_catalog.excluded_providers`
- 增加按模型设置 `reasoning_effort`
- 将模型清单标记为随版本变化的速查内容，并链接官方模型配置文档

### `4. Mixture of Agents (MoA)`
- 保留现有 `reference_max_tokens` 说明
- 在参考模型和聚合模型配置中增加 `reasoning_effort`
- 列出有效值 `none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max` 和 `ultra`
- 增加 `fanout: user_turn`，按用户轮次运行一次参考模型
- 标注 `fanout: per_iteration` 为默认值
- 说明参考模型 token 上限不限制聚合模型输出

### `5.1 常用命令`
- 增加 `hermes sessions export`
- 增加 `hermes sessions archive`
- 增加 `hermes sessions stats`
- 增加 `/sessions search <query>`
- 增加按工作区筛选会话和恢复会话工作目录

### `5.2 会话存储`
- 说明 `sessions.json` 将消息平台会话键映射到活动会话 ID，不包含 CLI 或 TUI 会话列表
- 说明 `state.db` 保存会话元数据与完整消息历史
- 将 `sessions.write_json_snapshots: true` 标记为可选的每会话 JSON 快照兼容开关，不与 `sessions.json` 混用

### `5.3 上下文压缩`
- 增加 `/compact` 别名
- 增加压缩时保留用户意图、持久交接信息和多模态句柄
- 增加会话谱系导出与压缩续接关系

### 在 `5. 会话管理` 下新增“会话导出与归档”
- 列出 `jsonl`、`md`、`qmd`、`html` 和 `trace` 导出格式
- 增加 `--only user-prompts`
- 增加 `--redact` 和 trace 默认脱敏行为
- 增加 `--lineage logical`，把压缩后的会话谱系导出为一个逻辑会话
- 增加 Hugging Face trace 上传参数 `--upload`、`--public` 和 `--no-redact`
- 增加时间、平台、工作区、模型、提供商、消息数、token、成本和工具调用筛选项
- 说明 `archive` 只隐藏会话，不删除消息和搜索数据

### `6. Toolsets`
- 增加 `display.tool_progress: log`
- 增加 Browser 截断时保存完整快照的行为
- 增加 `image_generate` 的 OpenAI-Codex 后端图像输入与图像编辑支持
- 保留现有 Toolset 分类与终端后端说明

### `7. MCP`
- 增加 MCP 工具命名格式 `mcp__<server>__<tool>`
- 按新命名格式更新 Hook、全局权限规则和其他注册后工具名示例
- 保留 `mcp_servers.<name>.tools.include` 与 `tools.exclude` 中的服务器原始工具名，不添加 `mcp__<server>__` 前缀
- 增加 Dashboard 和桌面端托管 OAuth
- 增加 MCP Server 日志进入 `agent.log`
- 增加 Blender MCP 目录项及默认精选工具

### `8.3 常用命令` 与 `8.4 Skill 捆绑包`
- 增加连续加载多个技能的写法 `/skill-a /skill-b 执行任务`
- 区分连续技能调用和命名 Skill Bundle
- 增加 `security/unbroker`、`unreal-mcp` 和 `mcp-oauth-remote-gateway` 的索引入口

### `8.6 Curator`
- 增加 `hermes curator usage`
- 标注不使用 `--consolidate` 时只运行无需辅助模型的确定性维护
- 保留 `curator.consolidate: false` 默认配置
- 增加 `curator.prune_builtins: true` 默认配置
- 说明 bundled 内置技能仅参与过期归档，不参与修补、合并或删除
- 说明受保护的内置技能和 Hub 安装技能不参与 Curator 归档

### `9.2 Plugin Hooks`
- 为 `pre_tool_call` 增加 `approve` 动作
- 说明插件返回 `approve` 时进入人工审批门
- 增加大型 Hook 注入内容写入磁盘的结果格式

### `10. Plugins`
- 在 Provider 插件类型中增加 Secret Source Provider
- 说明 `hermes plugins list` 同时显示本地插件和 Python entry-point 插件
- 增加 `SecretSource` 注册接口入口

### `11.4 外部记忆提供商`
- 为 mem0 增加自托管 Dashboard 后端、`mem0_search` 的 `top_k`/`rerank` 参数和设置向导模式
- 增加桌面端记忆提供商配置面板
- 增加 `/journey` 打开桌面端记忆图的行为

### `13. Gateway`
- 增加最终回复持久化投递账本
- 说明 Gateway 重启后会重投未确认送达的最终回复
- 增加单 Gateway 多 Profile 消息路由
- 增加按服务器、频道和线程选择 Profile
- 说明各 Profile 独立使用配置、技能、记忆和密钥
- 增加 `GATEWAY_MULTIPLEX_PROFILES`
- 增加按频道覆盖模型和系统提示词
- 说明会话级 `/model` 覆盖会跨重启保存
- 增加 Webhook 负载筛选、路由脚本和 HTTP 事件回调

### `13.3 会话管理`
- 将 Gateway 会话自动重置的默认值改为 `mode: none`
- 将现有 `mode: both` 配置标记为主动启用自动重置的示例
- 说明 `idle`、`daily` 和 `both` 都属于显式启用项
- 说明活动后台进程会在 `session_reset.bg_process_max_age_hours` 时间内阻止自动重置，默认上限为 24 小时

### `13.4 API 服务器`
- 将 `hermes serve` 定义为供桌面端或远程客户端连接的无头 JSON-RPC/WebSocket 后端
- 保留 API Server 作为向 Open WebUI 等客户端提供 Chat Completions 的 OpenAI 兼容端点

### 在 `13. Gateway` 下新增“消息平台变化”
- 增加 Telegram、Discord 和 Matrix 的 `/reasoning`、`/fast` 原生选择按钮
- 增加 WhatsApp 投票、位置消息、入站元数据和 Dashboard 配对
- 增加 Discord 重连漏收消息恢复、自动线程标题、审批提醒和管理员审批限制
- 增加 Slack `display.live_status` 实时工具状态
- 增加 Telegram `free_response_topics` 自由回复 Topic 列表和 `ignored_threads` 静默 Topic 列表
- 增加 Google Chat 澄清卡片
- 增加 `stt.echo_transcripts`

### `14. Profile`
- 增加 Profile 路由与现有多 Gateway 模式的区别
- 增加共享 Bot Token 下的服务器、频道和线程路由说明
- 增加错误 Profile 配置不影响其他 Profile 的隔离行为

### `15. Cron`
- 增加持久化执行审计历史
- 增加桌面端按 Cron Job 选择模型
- 增加运行认领 TTL 与 `HERMES_CRON_TIMEOUT` 的关系
- 保留现有调度、投递和 `context_from` 用法

### `16. Delegation`
- 增加 `delegate_task` 返回实时转录文件路径
- 增加 `tail -f <transcript-path>` 查看子 Agent 工具调用、结果和流式回复的示例
- 增加已完成但尚未投递的后台委派结果持久化和重启后投递
- 说明进程重启不会恢复仍在运行的子 Agent
- 保留 `delegation.max_concurrent_children` 作为统一并发上限
- 增加 `max_async_children` 已弃用的迁移提示

### `17. Kanban`
- 增加创建任务弹窗和可编辑 Board 项目目录
- 增加 Done 卡片结果入口和看板拖拽平移
- 增加 Kanban Toolset 的 `kanban_attach`、`kanban_attach_url` 和 `kanban_attachments` 工具
- 增加 `hermes kanban attach`、`hermes kanban attachments` 和 `hermes kanban attach-rm` 命令
- 增加带 SSRF 防护的 URL 附件抓取
- 说明创建 Board 时保存项目目录

### `18.11 示例`
- 保留 Open WebUI 使用 API Server 的接入方式
- 增加 API Server 按客户端选择模型路由的配置入口
- 将 Open WebUI 接口类型写为 `Chat Completions` 和 `Responses (Experimental)`
- 将 Langfuse 插件名写为 `observability/langfuse`
- 说明 `hermes tools post-setup langfuse` 安装 Langfuse SDK 并启用该插件
- 使用 `hermes plugins list` 检查 `observability/langfuse` 的启用状态

## README 速查表
### 常用新增命令
| 命令                        | 用途               |
| --------------------------- | ------------------ |
| `hermes config get <key>`   | 读取解析后的配置值 |
| `hermes config unset <key>` | 删除用户配置值     |
| `hermes sessions archive`   | 批量归档会话       |
| `hermes curator usage`      | 查看全部技能用量   |

### 0.19.0 默认值
| 配置                     | 0.19.0 默认值 |
| ------------------------ | ------------- |
| `approvals.mode`         | `smart`       |
| `display.show_reasoning` | 开启          |
| `session_reset.mode`     | `none`        |
| `curator.consolidate`    | `false`       |
| `curator.prune_builtins` | `true`        |
