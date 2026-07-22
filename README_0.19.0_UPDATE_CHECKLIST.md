# README.md 适配 Hermes Agent 0.19.0 更新清单
本文列出将当前 `README.md` 更新到 Hermes Agent 0.19.0 时需要处理的章节和内容。目标版本为 `0.19.0`，对应标签 `v2026.7.20`。

## 处理概览
| 级别 | 范围 |
| --- | --- |
| 必须修改 | 密钥存储表述、Gateway 会话重置默认值、MCP 工具命名、`hermes serve` 定义 |
| 重点补充 | 智能审批、会话导出、子 Agent 实时转录与持久化结果、跨 Profile 消息路由 |
| 常用功能补充 | Nous 订阅管理、临时模型切换、推理强度、配置命令、技能叠加调用 |
| 客户端补充 | 桌面端、Web Dashboard、消息平台交互能力 |
| 运维补充 | Cron 审计、用量文件、安全模式、密码管理器、投递账本 |

## 必须修改的现有内容
### `3.1 目录结构`
- 保留 `state.db` 作为会话、消息和运行状态的主存储
- 将 Gateway 路由索引说明统一到 `state.db`
- 将 `sessions.json` 标记为可选的旧版兼容镜像，不再作为主索引介绍

### `7. MCP`
- 增加 MCP 工具命名格式 `mcp__<server>__<tool>`
- 按新命名格式更新涉及 MCP 工具名的 Hook、白名单、黑名单和权限示例

### `13.3 会话管理`
- 将 Gateway 会话自动重置的默认值改为 `mode: none`
- 将现有 `mode: both` 配置标记为主动启用自动重置的示例
- 说明 `idle`、`daily` 和 `both` 都属于显式启用项
- 说明存在活动后台进程的会话不会自动重置

### `2.6 Web Dashboard` 与 `13.4 API 服务器`
- 区分 `hermes dashboard`、`hermes serve` 和 OpenAI 兼容 API Server
- 将 `hermes dashboard` 定义为带浏览器管理界面的服务
- 将 `hermes serve` 定义为供桌面端或远程客户端连接的无头 JSON-RPC/WebSocket 后端
- 保留 API Server 作为向 Open WebUI 等客户端提供 Agent Chat Completions 的 OpenAI 兼容端点

## 按现有章节补充的内容
### `2.1 安装`
- 增加 Windows 和 macOS 的 Hermes Desktop 安装入口
- 保留 Linux、macOS、WSL2 和 Windows 的命令行安装脚本
- 将现有快捷键标题改为“CLI/TUI 常用快捷键”，避免与可重新绑定的桌面端快捷键混用

### `2.3 对话`
- 增加故障排查命令 `hermes chat --safe-mode`
- 增加单轮临时模型切换 `/model --once <model>`
- 增加 `/compact`，并标注其为 `/compress` 的别名
- 增加 `max` 和 `ultra` 推理强度
- 增加默认开启推理过程显示的说明

### `2.5 更新与卸载`
- 增加 `hermes update --check`，仅检查可用更新
- 增加更新前快速状态快照、完整备份和关闭备份的配置项
- 按 0.19.0 CLI 帮助更新卸载参数列表
- 保留 `hermes update` 作为普通升级命令

### `2.6 Web Dashboard`
- 增加 Capabilities 页面，统一说明 Skills、Tools、MCP 和 Hub
- 增加记忆提供商切换、安全会话导入、WhatsApp 配对和 Discord 工具集编辑
- 增加终端保活与重连、聊天图片粘贴或拖放、移动端 OAuth 登录
- 增加 Gateway 拓扑、Profile 状态和运行维护入口

### `3.2 常用命令`
- 增加 `hermes config get <key>`
- 增加 `hermes config unset <key>`
- 增加 `hermes config check`
- 增加 `hermes config migrate`
- 增加未知顶层配置项和已弃用配置项的检查说明
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
- 增加提供商 `enabled: false` 和 `excluded_providers`
- 增加按模型设置 `reasoning_effort`
- 将模型清单标记为随版本变化的速查内容，并链接官方模型配置文档

### `4. Mixture of Agents (MoA)`
- 保留现有 `reference_max_tokens` 说明
- 在参考模型和聚合模型配置中增加 `reasoning_effort`
- 列出有效值 `none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max` 和 `ultra`
- 增加按用户轮次运行一次参考模型的扇出频率配置
- 说明参考模型 token 上限不限制聚合模型输出

### `5.1 常用命令`
- 增加 `hermes sessions export`
- 增加 `hermes sessions archive`
- 增加 `hermes sessions stats`
- 增加 `/sessions search <query>`
- 增加按工作区筛选会话和恢复会话工作目录

### 在 `5. 会话管理` 下新增“会话导出与归档”
- 列出 `jsonl`、`md`、`qmd`、`html` 和 `trace` 导出格式
- 增加 `--only user-prompts`
- 增加 `--redact` 和 trace 默认脱敏行为
- 增加 `--lineage logical`，把压缩后的会话谱系导出为一个逻辑会话
- 增加 Hugging Face trace 上传参数 `--upload`、`--public` 和 `--no-redact`
- 增加时间、平台、工作区、模型、提供商、消息数、token、成本和工具调用筛选项
- 说明 `archive` 只隐藏会话，不删除消息和搜索数据

### `5.3 上下文压缩`
- 增加 `/compact` 别名
- 增加压缩时保留用户意图、持久交接信息和多模态句柄
- 增加会话谱系导出与压缩续接关系

### `6. Toolsets`
- 增加 `display.tool_progress: log`
- 增加 Browser 截断时保存完整快照的行为
- 增加 Codex 图像输入支持
- 保留现有 Toolset 分类与终端后端说明

### `7. MCP`
- 增加 Dashboard 和桌面端托管 OAuth
- 增加 `redirect_uri` 和 `redirect_host`
- 增加 MCP Server 日志进入 `agent.log`
- 增加 Blender MCP 目录项及默认精选工具
- 增加 OAuth 回调端口冲突处理后的配置说明

### `8.3 常用命令` 与 `8.4 Skill 捆绑包`
- 增加连续加载多个技能的写法 `/skill-a /skill-b 执行任务`
- 区分连续技能调用和命名 Skill Bundle
- 增加 `security/unbroker`、`unreal-mcp` 和 `mcp-oauth-remote-gateway` 的索引入口

### `8.6 Curator`
- 增加 `hermes curator usage`
- 标注不使用 `--consolidate` 时只运行无需辅助模型的确定性维护
- 保留 `curator.consolidate: false` 默认配置

### `9.2 Plugin Hooks`
- 为 `pre_tool_call` 增加 `approve` 动作
- 说明插件返回 `approve` 时进入人工审批门
- 增加大型 Hook 注入内容写入磁盘的结果格式

### `10. Plugins`
- 在 Provider 插件类型中增加 Secret Source Provider
- 说明 `hermes plugins list` 同时显示本地插件和 Python entry-point 插件
- 增加 `SecretSource` 注册接口入口

### `11.4 外部记忆提供商`
- 为 mem0 增加自托管 Dashboard 后端、召回参数和设置向导模式
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

### 在 `13. Gateway` 下新增“消息平台变化”
- 增加 Telegram、Discord 和 Matrix 的 `/reasoning`、`/fast` 原生选择按钮
- 增加 WhatsApp 投票、位置消息、入站元数据和 Dashboard 配对
- 增加 Discord 重连漏收消息恢复、自动线程标题、审批提醒和管理员审批限制
- 增加 Slack 实时工具状态
- 增加 Telegram Topic 自由回复白名单
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
- 增加后台委派完成结果持久化和重启恢复
- 保留 `delegation.max_concurrent_children` 作为统一并发上限
- 增加 `max_async_children` 已弃用的迁移提示

### `17. Kanban`
- 增加创建任务弹窗和可编辑 Board 项目目录
- 增加 Done 卡片结果入口和看板拖拽平移
- 增加附件 Toolset 与 CLI
- 增加带 SSRF 防护的 URL 附件抓取
- 说明创建 Board 时保存项目目录

### `18.11 示例`
- 保留 Open WebUI 使用 API Server 的接入方式
- 增加 API Server 按客户端选择模型路由的配置入口
- 核对 Open WebUI 的 Chat Completions 与 Responses 选项名称
- 核对 Langfuse 插件在 `hermes plugins list` 和 `hermes tools post-setup langfuse` 中的当前状态

## 建议新增的速查表
### 常用新增命令
| 命令 | 用途 |
| --- | --- |
| `/subscription` | 查看和变更 Nous 套餐 |
| `/topup` | 充值 Nous 额度 |
| `/model --once <model>` | 仅下一轮使用指定模型 |
| `/deny <reason>` | 拒绝命令并向 Agent 传递原因 |
| `/compact` | 手动压缩上下文 |
| `/sessions search <query>` | 搜索会话 |
| `hermes chat --safe-mode` | 禁用用户配置、规则、插件、Hooks 和 MCP 进行排查 |
| `hermes config get <key>` | 读取解析后的配置值 |
| `hermes config unset <key>` | 删除用户配置值 |
| `hermes sessions export` | 导出会话 |
| `hermes sessions archive` | 批量归档会话 |
| `hermes curator usage` | 查看全部技能用量 |
| `hermes -z --usage-file <path> <prompt>` | 输出脚本调用的 JSON 用量文件 |

### 需要醒目标注的默认值
| 配置 | 0.19.0 默认值 |
| --- | --- |
| `approvals.mode` | `smart` |
| `display.show_reasoning` | 开启 |
| `session_reset.mode` | `none` |
| `curator.consolidate` | `false` |

## 无需大幅改写的章节
- `6.3 终端后端` 的六种后端分类保持有效，只需补充 Docker 网络开关和桌面端后端选择器
- `11.1` 至 `11.3` 的内置记忆、Memory 工具和记忆管理规则保持有效
- `12. 上下文文件` 的文件发现、渐进加载和安全扫描主体保持有效
- `15. Cron` 的调度格式、结果投递和 `context_from` 保持有效
- `18. 案例：深度研究` 的角色、阶段和文件契约保持有效

## 不写入 README 主体的发布细节
- 不展开提交数量、PR 数量、贡献者名单和内部性能基准实现
- 不展开 CI 流程、TypeScript 迁移和内部缓存结构
- 不记录已经在发布窗口内回滚且未随 0.19.0 发布的功能
- 将完整发布统计和内部变更保留在 `HERMES_0.19.0_UPDATE.md`

## 资料来源
- [Hermes Agent 0.19.0 官方发布说明](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20)
- [Hermes Agent 当前官方文档](https://hermes-agent.nousresearch.com/docs/)
- [配置管理](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/)
- [密钥管理](https://hermes-agent.nousresearch.com/docs/user-guide/secrets/)
- [会话管理](https://hermes-agent.nousresearch.com/docs/user-guide/sessions/)
- [Mixture of Agents](https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents/)
- [CLI 命令参考](https://hermes-agent.nousresearch.com/docs/reference/cli-commands/)
