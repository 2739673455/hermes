# README 审阅
审阅对象：`README.md`

## 13. Gateway
- 重复描述：Gateway 职责中的会话维护、cron 调度，与会话管理、Cron 章节重复
- 重复描述：白名单、配对、权限控制都在说明访问控制，可合并为网关访问控制
- 重复描述：API 服务器说明与深度研究案例中的 Open-WebUI 接入步骤存在重复
- 可精简描述：职责列表可压缩为平台连接、消息转发、会话维护、后台调度四项
- 可精简描述：配对示例可只保留 approve、list、revoke 三条命令
- 可精简描述：API 服务器可保留启用、重启、健康检查三步，Open-WebUI 专项接入放到案例章节

## 14. Profile
- 重复描述：章节开头的独立配置、会话、记忆、技能、定时任务、Gateway，与配置管理、会话管理、记忆、Skills、Cron、Gateway 章节重复
- 重复描述：别名命令与 `hermes -p <name>` 示例都在表达同一运行方式
- 可精简描述：常用命令中的长描述 profile 示例可缩短，保留 `create --description` 的用法即可
- 可精简描述：工作原理可压缩为 `HERMES_HOME` 定位和状态隔离两句

## 15. Cron
- 重复描述：创建任务中 `/cron add` 与 `hermes cron create` 示例重复
- 重复描述：管理任务中 `/cron` 和 `hermes cron` 命令覆盖相同动作
- 重复描述：任务输出路径在创建任务和 context_from 串联中重复出现
- 重复描述：Gateway 调度循环与 Gateway 章节职责重复
- 可精简描述：创建任务示例可分别保留会话命令、CLI 命令、自然语言三类各一条
- 可精简描述：管理任务可用动作表替代长命令列表
- 可精简描述：context_from 示例可保留两段任务串联，三段完整 cronjob 示例偏长

## 16. Delegation
- 重复描述：子 Agent 隔离上下文在章节开头和子 Agent 上下文小节重复
- 重复描述：后台运行、结果回传和批量结果合并都在描述委派结果返回
- 重复描述：嵌套委派中的 `max_concurrent_children` 与并行批量小节重复
- 可精简描述：单任务与批量示例可保留最小字段，减少 context 长文本
- 可精简描述：工具限制表可保留工具和限制结果，原因列可压缩

## 17. Kanban
- 重复描述：章节开头、目标、架构都在描述可恢复、可审计、多 Agent 协作
- 重复描述：Task、Comment、Event、Worker 多处重复说明任务状态、评论交接、执行记录
- 重复描述：Dispatcher 的 60 秒 tick 与 Cron、Gateway 调度说明重复
- 重复描述：任务分解与编排中的 Orchestrator Profile，与 Delegation 和 Profile 章节的子 Agent、Profile 能力重复
- 可精简描述：Kanban 目标可合并为适用场景和核心能力两张表
- 可精简描述：架构图可保留，三层架构文字可压缩为图前导语
- 可精简描述：核心概念可只保留 Board、Task、Link、Worker、Dispatcher，Comment、Event、Workspace、Tenant 可合并到 Task 属性
- 可精简描述：协作模式可保留名称和图示，删除长段解释

## 18. 案例：深度研究
- 重复描述：功能、角色规划、流程与任务图、各 profile 职责多次重复研究方案、搜索、写作、校验、综合、渲染链路
- 重复描述：`research-lead` 的周期巡检在流程第 11 步、流程图后说明、18.5.3 周期巡检中重复出现
- 重复描述：blocked 处理规则在流程第 5 步、流程图后说明、research-lead blocked 处理、各 worker 阶段规则中重复出现
- 重复描述：统一反馈格式在 18.5.6、reviewer validation 字段、多个 worker 执行规则中重复出现
- 重复描述：`section_id`、`workspace_path`、`source_ids`、`evidence_chain_ids`、`required_user_input` 等字段在多个文件格式中重复定义
- 重复描述：Profile 配置命令在每个角色小节重复出现
- 重复描述：API 服务器和 Open-WebUI 接入步骤与 Gateway API 服务器章节重复
- 可精简描述：18.1-18.3 可合并为目标、角色、端到端流程三块
- 可精简描述：18.5 的阶段说明可保留输入、输出、关键规则，删除步骤中与规则重复的动作
- 可精简描述：各 worker 小节可统一模板为职责、依赖、输入、输出、成功条件、阻塞条件、产物 schema
- 可精简描述：文件格式可抽成公共字段、章节产物、全局产物、报告产物四组
- 可精简描述：Profile 配置可集中到一个“角色配置命令”小节，避免每个角色重复 `profile create` 和 `cp -R`
- 可精简描述：Open-WebUI 接入可引用 Gateway API 服务器配置，只保留 research-lead 的端口和 kanban toolset 差异
