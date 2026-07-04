## 当前文档不一致项
- 最新版本：Hermes Agent `v0.18.0`，发布标签 `v2026.7.1`
- 当前对照文档：`README.md`

### 6. Gateway Fleet 与 Drain 能力
- README 位置：`README.md:1271-1290`
- 最新版内容：Gateway 支持 scale-to-zero、dormant-quiesce、external drain coordination、safe lifecycle busy/idle readout、relay wake 与 passthrough_forward
- 当前文档状态：Gateway 章节只列连接、收发、会话、投递和 cron 调度，未包含 fleet/relay/scale-to-zero/drain 能力

### 7. API Server 并发上限
- README 位置：`README.md:1397-1418`
- 最新版内容：API server 支持 configurable concurrent-run cap
- 当前文档状态：API 服务器章节只包含启用、重启、health 和 models 验证命令，未包含并发运行上限配置

### 8. Provider 更新
- README 位置：`README.md:71-77`、`README.md:127-130`
- 最新版内容：Google Vertex AI 是一等 provider；Krea、Z.AI、Ollama Cloud reasoning_effort 有新增 provider 能力；`google-gemini-cli` 和 `google-antigravity` OAuth provider 被移除
- 当前文档状态：初次配置和配置目录未包含 provider 清单、Vertex AI、provider 移除项

### 9. Cron Continuations 与工具集
- README 位置：`README.md:1471-1704`
- 最新版内容：Cron 支持续接会话投递、Slack in-channel continuable delivery、Gateway 未运行提示、per-job MCP toolsets
- 当前文档状态：Cron 章节未包含 v0.18.0 的 continuations、Slack 投递和每任务 MCP 工具集

### 10. MCP、Skills、Kanban 与 Plugins
- README 位置：`README.md:339-423`、`README.md:625-667`、`README.md:1791-2057`
- 最新版内容：Blank Slate setup mode、`cloudflare-temporary-deploy` optional skill、creative-ideation v2.1.0、Kanban lifecycle plugin hooks、typed block reasons、unblock-loop breaker、插件 `ctx.profile_name` 是 v0.18.0 更新项
- 当前文档状态：MCP、Skills、Kanban、Plugins 章节未包含这些新增能力
