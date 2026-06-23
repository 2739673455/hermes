# Hermes Agent
https://hermes-agent.nousresearch.com/

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [快速上手](#2-快速上手)
3. [配置管理](#3-配置管理)
4. [会话管理](#4-会话管理)
5. [Toolsets](#5-toolsets)
6. [MCP](#6-mcp)
7. [Skills](#7-skills)
8. [Hooks](#8-hooks)
9. [Plugins](#9-plugins)
10. [持久记忆](#10-持久记忆)
11. [上下文文件](#11-上下文文件)
12. [Gateway](#12-gateway)
13. [Profile](#13-profile)
14. [Cron](#14-cron)
15. [Delegation](#15-delegation)
16. [Kanban](#16-kanban)
17. [案例：深度搜索](#17-案例深度搜索)

# 1. Hermes Agent 是什么
Hermes Agent 是由开源 AI 研究实验室 Nous Research 开发的开源 AI Agent 框架，具有以下核心特性：

- **闭环学习循环**：Hermes 定期管理自身记忆，自主创建并整理优化技能，FTS5（SQLite 全文搜索索引）跨会话召回信息。
- **多平台网关**：通过网关链接 20 多个平台，包括 Telegram、Weixin 等。
- **多 Agent 实例**：通过 Profile 创建多个独立的 Hermes 实例，各自有独立的配置、会话、记忆和技能。
- **多 Agent 协作**：通过子 Agent 委派或 Kanban 实现多 Agent 协作。
- **可扩展**：自定义工具、MCP、技能、钩子、插件、定时任务等。

# 2. 快速上手
## 2.1 安装
https://hermes-agent.nousresearch.com/docs/getting-started/installation

**Linux / macOS / WSL2：**
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

**Windows (PowerShell)：**
```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

安装脚本主要会做如下操作：

1. 检查并准备环境
   - 安装或复用 Hermes 托管的 `uv`；不会复用系统已有的 `uv`
   - 检查 Python 3.11；缺失时通过 Hermes 托管的 `uv` 安装
   - 检查 Git；缺失时会尝试自动安装
   - 检查 Node.js；优先复用系统 Node.js；缺失或版本不满足要求时会安装 Hermes 托管的 Node.js 22
   - 检查网络连通性以及 ripgrep、ffmpeg 等系统依赖；缺失时会尝试自动安装
2. 拉取或更新 Hermes 源码
   - 拉取或更新 Hermes 源码。默认拉取到 `~/.hermes/hermes-agent` 或 `%LOCALAPPDATA%\hermes\hermes-agent`
3. 安装依赖
   - 创建 Python 虚拟环境并安装 Python 依赖
   - 安装 Node.js 依赖、浏览器工具依赖和 TUI 依赖
   - 没有可用系统浏览器且未跳过浏览器安装时，会尝试安装 Playwright Chromium
4. 创建命令入口
   - 创建 `hermes` 命令入口。普通用户链接到 `~/.local/bin`
5. 初始化数据目录和配置
   - 初始化数据目录。默认是 `~/.hermes` 或 `%LOCALAPPDATA%\hermes`
   - 仅在文件不存在时创建 `config.yaml`、`.env`、`SOUL.md`，已有配置会保留
6. 同步技能和平台组件
   - 同步 bundled skills
   - Windows 会额外安装消息平台 SDK 并写入安装完成标记
7. 执行交互式收尾
   - 交互式安装会继续运行 setup 向导，并可选择启动或安装 Gateway；非交互式或传入跳过参数时不会运行这些交互步骤

## 2.2 初次配置
```bash
hermes model  # 交互式选择模型和提供商
hermes setup  # 或者运行完整设置向导
```

密钥存储在 `~/.hermes/.env` 文件中。

## 2.3 对话
```bash
hermes                # 启动交互式对话
hermes --tui          # 使用 TUI 启动交互式对话
hermes chat -q "你好"  # 单次对话，适合脚本调用或一次性任务
```

## 2.4 常用快捷键
| 快捷键                             | 功能                        |
| ---------------------------------- | --------------------------- |
| `Alt+V`                            | 从剪贴板粘贴图像            |
| `Ctrl+C`                           | 中断 Agent                  |
| `Ctrl+D`                           | 退出会话                    |
| `Ctrl+Z`                           | 暂停并挂起到后台，`fg` 恢复 |
| `Alt+Enter`/`Ctrl+J`/`Shift+Enter` | 插入新行，输入多行文本      |

## 2.5 更新
```bash
hermes update
```

## 2.6 卸载
```bash
hermes uninstall
```

如果需要完全清理所有数据：

```bash
rm -rf ~/.hermes
```

## 2.7 Web Dashboard
Hermes 提供了一个基于浏览器的界面。

```bash
hermes dashboard                       # 启动，自动打开浏览器 http://127.0.0.1:9119
hermes dashboard --port 8080           # 自定义端口
hermes dashboard --tui                 # 启用浏览器内 Chat 标签页
hermes dashboard --status              # 查看运行状态
hermes dashboard --stop                # 停止运行
hermes dashboard &>/dev/null & disown  # 后台运行并脱离终端
```

# 3. 配置管理
https://hermes-agent.nousresearch.com/docs/user-guide/configuration

## 3.1 目录结构
```
~/.hermes/
├── config.yaml    # 主配置文件（模型、终端、TTS、压缩等）
├── .env           # API 密钥和机密信息
├── auth.json      # OAuth 提供商凭证（Nous Portal 等）
├── SOUL.md        # 主 Agent 的身份文件，会拼入系统提示词开头部分
├── memories/      # 持久化记忆（MEMORY.md、USER.md）
├── skills/        # 技能
├── cron/          # 定时任务
├── sessions/      # 会话
└── logs/          # 日志（errors.log、gateway.log — 密钥自动脱敏）
```

## 3.2 常用命令
CLI 命令：

```bash
hermes config                        # 查看当前配置
hermes config edit                   # 用 $EDITOR 打开 config.yaml 编辑
hermes config set section.key value  # 直接设置某个配置项
```

斜杠命令：

| 命令                            | 功能                   |
| ------------------------------- | ---------------------- |
| `/config`                       | 查看当前配置           |
| `/model [model-name]`           | 查看或切换当前模型     |
| `/personality [name]`           | 切换预设人格           |
| `/reasoning [level/show/hide]`  | 查看或切换模型推理级别 |
| `/voice [on/off/tts/status]`    | 查看或开关语音模式     |
| `/yolo`                         | 跳过所有危险命令审批   |
| `/busy [interrupt/queue/steer]` | 查看或切换中断模式     |

# 4. 会话管理
Hermes Agent 自动将每次对话保存为一个会话。会话支持对话恢复、对话历史管理以及跨会话搜索。

## 4.1 常用命令
CLI 命令：

```bash
hermes sessions list                         # 列出近期会话
hermes sessions browse                       # 打开交互式会话选择器
hermes sessions rename <session-id> <title>  # 重命名会话
hermes sessions delete <session_id>          # 删除会话
hermes sessions prune --older-than 30        # 清理 30 天前的旧会话
hermes [chat] --continue, -c                 # 继续上次会话
hermes [chat] --resume, -r                   # 按会话 ID 或标题恢复对话
hermes [chat] -t, --toolsets <csv>           # 启用逗号分隔的 toolset 集合
hermes [chat] -s, --skills <name>            # 为会话预加载一个或多个 skill
hermes [chat] --worktree                     # 为本次运行创建隔离的 git worktree
hermes [chat] --checkpoints                  # 在破坏性文件变更前启用文件系统 checkpoint
```

斜杠命令：

| 命令                    | 功能                                                                                                 |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| `/new`                  | 开始新会话                                                                                           |
| `/clear`                | 清屏并开始新会话                                                                                     |
| `/history`              | 显示对话历史                                                                                         |
| `/undo`                 | 移除最后一轮用户/助手对话                                                                            |
| `/title <session_name>` | 为当前会话设置标题                                                                                   |
| `/compress`             | 手动压缩上下文                                                                                       |
| `/rollback`             | 列出或恢复文件系统检查点                                                                             |
| `/queue <prompt>`       | 将 prompt 加入队列等待下一轮处理，不会中断当前 agent 响应                                            |
| `/steer <prompt>`       | 在下一次工具结果返回后，将中途说明追加到工具结果末尾，用于在任务进行中调整方向                       |
| `/goal <text>`          | 设置持续性目标。辅助裁判模型会判断目标是否完成；若未完成则自动继续                                   |
| `/subgoal <text>`       | 在循环进行中向活动目标追加一个用户自定义条件，只有原始目标和所有子目标都满足时，目标才会被标记为完成 |
| `/sessions`             | 查看和管理会话                                                                                       |
| `/background <prompt>`  | 在独立的后台会话中运行  prompt                                                                       |
| `/stop`                 | 停止后台进程                                                                                         |
| `/branch [name]`        | 分支当前会话（探索不同路径）                                                                         |

## 4.2 会话存储
Hermes 使用 SQLite 数据库（`~/.hermes/state.db`）保存会话状态，包括会话元数据、完整消息历史、FTS5 全文搜索索引等。

SQLite 中主要有这几张表：

| 表                     | 内容                                               |
| ---------------------- | -------------------------------------------------- |
| `sessions`             | 会话元数据：会话 ID、来源平台、用户 ID、模型配置等 |
| `messages`             | 完整消息历史：所属会话、角色、正文、工具调用等     |
| `messages_fts`         | FTS5 虚拟表，用于英文 / 拉丁语系全文搜索           |
| `messages_fts_trigram` | FTS5 虚拟表，用于 CJK（中日韩）子串搜索            |
| `state_meta`           | 键值元数据表，用于记录状态型信息                   |
| `schema_version`       | 记录 schema 版本，跟踪迁移状态                     |

SQLite 数据库使用 WAL 模式支持并发读取和单写入。

## 4.3 上下文压缩
当会话上下文长度接近限制时，Hermes 会自动压缩历史消息，保留关键信息并维持上下文窗口可用。

### 4.3.1 相关配置
```yaml
# ~/.hermes/config.yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 上下文窗口阈值
  target_ratio: 0.20  # 窗口内保留多少不压缩
  protect_last_n: 20  # n 个末尾消息不压缩
```

### 4.3.2 压缩算法
1. 清理旧工具结果
   - 将大于 200 字符的旧工具结果替换为 `[Old tool output cleared to save context space]`
2. 确定压缩边界
   - 保留系统提示词和会话开头消息作为头部
   - 按 `threshold_tokens × target_ratio` 计算尾部 token 预算，从末尾向前保留最近上下文
   - 边界会对齐 `tool_call` / `tool_result`，避免拆散工具调用组
3. 生成结构化摘要
   - 由 `auxiliary.compression` 模型生成摘要
   - 记录目标、约束、进展、关键决策、相关文件、后续操作和关键细节
   - 摘要预算按被压缩内容动态分配，最低 2000 token，最高不超过 `min(context_length × 0.05, 12000)`
4. 组装压缩消息
   - 压缩后的消息列表为头部消息、压缩摘要和尾部消息
   - 如果摘要生成失败，会根据配置中止压缩或插入确定性 fallback 摘要
   - 最后清理孤立的 `tool_call` / `tool_result`，并移除历史图片载荷
5. 迭代重压缩
   - 再次触发压缩时，前一次摘要会连同指令一起传递给 LLM，要求其更新摘要而非从头摘要
6. 摘要模型要求
   - 摘要模型的上下文窗口应不小于主模型，否则中间对话轮次可能因摘要失败无法完整保留

## 4.4 会话搜索工具
当用户引用过去对话中的内容，或 Agent 怀疑存在相关历史上下文时，Agent 会使用内置的 `session_search` 工具搜索历史消息。`session_search` 工具使用 SQLite 的 FTS5 引擎对所有历史对话进行全文搜索，并支持滚动浏览命中的 session。

`session_search` 有三种调用形式(发现、滚动、浏览)，会根据传入参数推断调用意图：

1. 发现
   - 参数：`session_search(query, limit)`
   - 用途：运行 FTS5 搜索，按 session 谱系去重，返回前 N 个会话
   - 每个结果通常包含：
     - `session_id`、`title`、`when`、`source`
     - `snippet`：FTS5 高亮匹配摘录
     - `bookend_start`：session 开头的用户和助手消息，用于还原目标或开场
     - `messages`：匹配点前后消息窗口，锚点消息会被标记
     - `bookend_end`：session 结尾的用户和助手消息，用于判断结论或决策
     - `match_message_id`：FTS5 命中的锚点消息 ID，可用于滚动调用继续查看上下文
     - `messages_before`：当前返回窗口之前还有多少条更早消息
     - `messages_after`：当前返回窗口之后还有多少条更新消息
2. 滚动
   - 参数：`session_search(session_id, around_message_id, window)`
   - 用途：返回以锚点消息为中心的前后消息窗口，用于发现更多上下文
3. 浏览
   - 参数：`session_search()`
   - 用途：按时间顺序返回最近 session 的标题、预览和时间戳

# 5. Toolsets
工具是扩展 Agent 能力的函数。它们被组织为逻辑上的工具集。

## 5.1 可用工具
Hermes 包含如下工具：

| 类别             | 包含工具                                                                                | 用途                                                                             |
| ---------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Web**          | `web_search`, `web_extract`                                                             | 搜索网页并提取页面内容                                                           |
| **X 搜索**       | `x_search`                                                                              | 搜索 X（Twitter）帖子和话题；需要 xAI 凭据，默认关闭，可通过 `hermes tools` 启用 |
| **终端与文件**   | `terminal`, `process`, `read_file`, `patch`                                             | 执行命令并操作文件                                                               |
| **浏览器**       | `browser_navigate`, `browser_snapshot`, `browser_vision`                                | 交互式浏览器自动化，支持文本与视觉                                               |
| **媒体**         | `vision_analyze`, `image_generate`, `video_generate`, `video_analyze`, `text_to_speech` | 多模态分析与生成；视频工具需手动启用 `video_gen` / `video` 工具集                |
| **Agent 编排**   | `todo`, `clarify`, `execute_code`, `delegate_task`                                      | 任务规划、澄清需求、代码执行和子 Agent 委托                                      |
| **记忆与召回**   | `memory`, `session_search`                                                              | 持久化记忆和会话搜索                                                             |
| **自动化与投递** | `cronjob`, `send_message`                                                               | 定时任务和出站消息投递                                                           |
| **集成**         | `ha_*`, MCP server 工具                                                                 | Home Assistant、MCP 及其他集成                                                   |

## 5.2 常用命令
```bash
hermes tools                            # 交互式管理工具集
hermes tools list                       # 查看所有工具集
hermes tools list --platform weixin     # 查看指定平台的工具集
hermes tools enable yuanbao             # 启用 yuanbao 工具集
hermes tools disable yuanbao            # 禁用 yuanbao 工具集

/tools [list|disable|enable] [name...]  # 查看或管理可用工具
/toolsets                               # 列出可用工具集
```

## 5.3 终端后端
终端工具支持多种后端，用于在本机、容器、远程主机或云端环境中执行命令。

### 5.3.1 后端类型
| 后端          | 说明                            | 适用场景               |
| ------------- | ------------------------------- | ---------------------- |
| `local`       | 在本机直接执行命令（默认）      | 本地开发、可信任务     |
| `docker`      | 在 Docker 容器中执行命令        | 隔离运行、可复现环境   |
| `ssh`         | 通过 SSH 在远程主机执行命令     | 远程服务器、沙箱主机   |
| `singularity` | 高性能计算集群容器              | 集群计算、无 root 权限 |
| `modal`       | 在 Modal 云端沙箱中执行命令     | 无服务器、弹性扩展     |
| `daytona`     | 在 Daytona workspace 中执行命令 | 持久化云端开发环境     |

### 5.3.2 Docker 后端配置
```yaml
# ~/.hermes/config.yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
```

### 5.3.3 SSH 后端配置
```yaml
# ~/.hermes/config.yaml
terminal:
  backend: ssh
```

```yaml
# ~/.hermes/.env
TERMINAL_SSH_HOST=my-server.example.com
TERMINAL_SSH_USER=myuser
TERMINAL_SSH_KEY=~/.ssh/id_rsa
```

# 6. MCP
MCP 让 Agent 连接到外部工具服务器。

## 6.1 MCP 服务器配置
可配置两种服务器：

1. stdio
   - 工作方式：本机启动 MCP server 进程，通过 stdin / stdout 与其通信
   - 适用场景：服务器已在本地安装、低延迟访问本地资源
   - 常用字段：
     - command：MCP 服务器的可执行文件
     - args：服务器的参数
     - env：传递给服务器的环境变量
2. HTTP
   - 工作方式：连接远程 MCP server
   - 适用场景：公司内部服务、远程 API、共享的工具服务器
   - 常用字段：
     - url：MCP 服务器端点
     - headers：HTTP 请求头

示例：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  project-fs:
    command: "npx"
    args: ["-y", "@mcp/server-filesystem", "/home/user/my-project"]

  company_api:
    url: "https://mcp.internal.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

常用配置项：

| 配置项                         | 说明                                  |
| ------------------------------ | ------------------------------------- |
| `timeout`                      | 工具调用超时时间                      |
| `connect_timeout`              | 初始连接超时时间                      |
| `enabled`                      | 是否启用该 server                     |
| `supports_parallel_tool_calls` | 若为 true，该服务器的工具可并发运行   |
| `tools`                        | 按服务器过滤工具及实用工具策略        |
| `auth`                         | 若为 oauth 可启用带 PKCE 的 OAuth 2.1 |

tools 配置项：

| 配置项      | 说明                                         |
| ----------- | -------------------------------------------- |
| `include`   | 工具白名单，指定允许注册的 MCP 工具          |
| `exclude`   | 工具黑名单，指定不允许注册的 MCP 工具        |
| `resources` | 启用/禁用 `list_resources` + `read_resource` |
| `prompts`   | 启用/禁用 `list_prompts` + `get_prompt`      |

若 `include` 和 `exclude` 同时配置，则 `include` 优先。

tools 配置示例：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, update_issue, search_code]
      resources: false
      prompts: false

  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer, refund_payment]
```

## 6.2 常用命令
```bash
hermes mcp list              # 列出已配置的服务器
hermes mcp test <name>       # 测试连接
hermes mcp configure <name>  # 管理服务器中的工具启用状态
hermes mcp remove <name>     # 移除服务器

/reload-mcp                  # 重新加载 MCP 服务器
```

# 7. Skills
Skills 是 Agent 在需要时可以按需加载的知识文档。每个已安装的 skill 都自动作为斜杠命令可用。

## 7.1 Skill 格式与配置
### 7.1.1 `SKILL.md` 格式
```markdown
---
name: my-skill                             # Skill 名称
description: Brief description of what this skill does  # 简短说明
version: 1.0.0                             # Skill 版本
platforms: [macos, linux]                  # 可用平台
metadata:
  hermes:
    tags: [python, automation]             # 标签
    category: devops                       # 分类
    fallback_for_toolsets: [web]           # web 工具集可用时隐藏
    fallback_for_tools: [web_search]       # web_search 工具可用时隐藏
    requires_toolsets: [terminal]          # terminal 工具集可用时显示
    requires_tools: [terminal]             # terminal 工具可用时显示
    config:
      - key: my.setting                    # 配置键
        description: "What this controls"  # 配置说明
        default: "value"                   # 默认值
        prompt: "Prompt for setup"         # 配置提示
required_environment_variables:
  - name: TENOR_API_KEY                    # 环境变量名
    prompt: Tenor API key                  # 输入提示
    help: Get a key from https://developers.google.com/tenor  # 获取方式
    required_for: full functionality       # 用途说明
---
# Skill Title
## When to Use
Trigger conditions for this skill.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes and fixes

## Verification
How to confirm it worked.
```

常用 frontmatter 字段：

| 字段                                    | 说明                       |
| --------------------------------------- | -------------------------- |
| `name`                                  | Skill 名称                 |
| `description`                           | 简短说明                   |
| `version`                               | Skill 版本                 |
| `platforms`                             | 限制可用操作系统           |
| `metadata.hermes.tags`                  | 标签                       |
| `metadata.hermes.category`              | 分类                       |
| `metadata.hermes.fallback_for_toolsets` | 仅在工具集不可用时显示技能 |
| `metadata.hermes.fallback_for_tools`    | 仅在工具不可用时显示技能   |
| `metadata.hermes.requires_toolsets`     | 仅在工具集可用时显示技能   |
| `metadata.hermes.requires_tools`        | 仅在工具可用时显示技能     |
| `metadata.hermes.config`                | 非密钥配置项声明           |
| `required_environment_variables`        | 需要用户配置的环境变量声明 |

`metadata.hermes.config` 声明的设置会在 Skill 加载时从 `config.yaml` 的 `skills.config` 下解析并注入上下文，Agent 可以直接看到已配置的值。

`required_environment_variables` 已配置的环境变量会自动传递到 `execute_code` 和 `terminal` 沙箱，Skill 的脚本可以直接使用对应环境变量。

### 7.1.2 输出与媒体传递
当 Skill 或 Agent 回复中包含媒体文件的裸绝对路径时，Gateway 会自动识别并把文件作为原生附件发送到聊天平台，而不是把路径文本直接显示给用户。

```text
/home/user/screenshots/diagram.png
```

音频文件可以通过 `[[audio_as_voice]]` 指令在支持的平台上作为语音消息发送。

如果需要把图片或其他媒体作为下载文件发送，而不是作为内联预览发送，可以在同一条响应中加入 `[[as_document]]`：

```text
Here is your rendered chart:

/home/user/.hermes/cache/chart-q4-2025.png

[[as_document]]
```

该指令会在投递前移除，用户不会看到它。同一响应中的所有媒体路径都会按文档附件方式发送。

## 7.2 Skill 目录结构
Hermes 本地 Skill 目录结构：

```text
~/.hermes/skills/
├── mlops/                 # 类别目录
│   ├── axolotl/           # 技能目录
│   │   ├── SKILL.md       # 主说明文件，必需
│   │   ├── references/    # 额外参考资料
│   │   ├── templates/     # 输出模板
│   │   ├── scripts/       # 辅助脚本
│   │   └── assets/        # 图片、数据等附加资源
│   └── vllm/
│       └── SKILL.md
├── devops/
│   └── deploy-k8s/
│       ├── SKILL.md
│       └── references/
├── .hub/                  # Skills Hub 状态
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
└── .bundled_manifest      # 记录内置技能同步状态
```

如果有其他的 Skill 目录，例如 `~/.agents/skills/`，可以让 Hermes 额外扫描这些目录：

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

本地与外部 Skill 行为规则：

- **本地创建，就地更新**：Agent 创建的新 Skill 写入 `~/.hermes/skills/`；已有 Skill 会在找到的位置被修改
- **外部目录默认不会写保护**：如果外部 Skill 目录对 Hermes 进程可写，`skill_manage` 可以修改其中的文件；需要只读共享 Skill 时，应使用文件系统权限或单独的 profile / toolset 约束
- **本地优先**：如果本地目录和外部目录有同名 Skill，本地版本优先
- **路径可选**：不存在的外部目录会被静默跳过，适合跨机器共享配置

## 7.3 常用命令
```bash
hermes skills list                # 列出已安装的技能
hermes skills browse              # 浏览技能
hermes skills search my-skill     # 搜索技能
hermes skills install my-skill    # 通过 ID 安装技能
hermes skills install https://share.chat/SKILL.md  # 通过 URL 安装技能（单文件 SKILL.md）
hermes skills uninstall my-skill  # 卸载技能
hermes skills config              # 管理技能配置

/skills                           # 管理技能
```

## 7.4 Skill 捆绑包
Skill 捆绑包用于把多个 Skill 组合到同一个斜杠命令下。当运行 `/<bundle-name>` 时，捆绑包中列出的 Skill 会同时加载，适合固定组合使用的重复任务。

### 7.4.1 创建示例
```bash
hermes bundles create backend-dev \
  --skill github-code-review \
  --skill test-driven-development \
  --skill github-pr-workflow \
  -d "Backend feature work — review, test, PR workflow"
```

捆绑包存放在 `~/.hermes/skill-bundles/<slug>.yaml` 中：

```yaml
name: backend-dev
description: Backend feature work — review, test, PR workflow
skills:
  - github-code-review
  - test-driven-development
  - github-pr-workflow
instruction: |
  Always start by writing failing tests, then implement.
  Open the PR through the standard workflow with co-author tags.
```

字段说明：

| 字段          | 说明                                                        |
| ------------- | ----------------------------------------------------------- |
| `name`        | 显示名称；默认使用文件名主干，并规范化为斜杠命令 slug       |
| `description` | 在 `/bundles` 和 `hermes bundles list` 中显示的简短说明     |
| `skills`      | 必填，非空列表；可以写 Skill 名称或相对于 Skills 目录的路径 |
| `instruction` | 可选；加载这些 Skill 时追加的额外指令                       |

### 7.4.2 行为规则
- **命令冲突时捆绑包优先**：如果捆绑包和单个 Skill 使用同一个 slug，斜杠命令会调用捆绑包
- **缺失 Skill 会被跳过**：捆绑包会加载能解析的 Skill，并提示哪些条目被跳过
- **跨界面可用**：交互式 CLI、TUI、Dashboard Chat 和 Gateway 平台都可以使用捆绑包
- **不会修改系统提示词**：捆绑包调用时生成一条新的用户消息，不会使 prompt 缓存失效
- **不会自动安装 Skill**：捆绑包只是 YAML 别名，列出的 Skill 必须已存在于本地或外部 Skill 目录

### 7.4.3 常用命令
```bash
hermes bundles list                    # 列出所有捆绑包
hermes bundles show backend-dev        # 查看捆绑包
hermes bundles create research         # 交互式创建捆绑包
hermes bundles create backend-dev --skill ... --force  # 覆盖现有捆绑包
hermes bundles delete backend-dev      # 删除捆绑包
hermes bundles reload                  # 重新扫描 skill-bundles 目录

/bundles                               # 会话内列出捆绑包
```

## 7.5 Agent-Managed Skills (skill_manage tool)
Agent 可以通过 `skill_manage` 工具创建、修改和删除自己的技能。这是 Agent 的「程序记忆」：当它找到一个非平凡的工作流时，它会将该方法保存为 Skill 以供将来复用。

Agent 创建和更新 Skill 主要由三条路径触发：

| 触发入口                | 行为                                                                                                                              |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 主对话提示词            | `skill_manage` 可用时，系统提示会要求 Agent 在复杂任务、困难修复或发现非平凡流程后保存 Skill；如果已加载 Skill 有问题，要立即修补 |
| `skill_manage` 工具说明 | 工具 schema 会明确何时 `create`、`patch`、`edit`、`write_file`、`delete`，并要求跳过简单的一次性任务，创建和删除前向用户确认      |
| 后台 review agent       | 当工具调用迭代数达到 `skills.creation_nudge_interval` 后，回合结束会 fork 后台 review，回顾本轮对话并更新 Skill library           |

何时创建 Skill：

- 完成了复杂任务，尤其是 5 次以上工具调用的任务
- 克服了棘手错误、环境差异或反复调试问题
- 用户纠正后的做法被验证有效
- 发现了可复用的命令序列、排障路径、工作流或检查清单
- 用户明确要求“记住这个流程”或以后复用

何时更新 Skill：

- 本轮加载或查看过的 Skill 缺步骤、命令错误、过时或不适配当前系统
- 遇到 Skill 没覆盖的坑点、OS 差异、依赖问题或验证步骤
- 用户纠正了执行顺序、输出格式、审查标准或工作偏好
- 已有通用类 Skill 能覆盖本轮新增经验

更新优先级：

1. 先 patch 当前加载或查看过的 Skill
2. 再 patch 已有的通用类 Skill
3. 需要保留较长细节时，用 `write_file` 写入 `references/`、`templates/` 或 `scripts/`
4. 没有合适现有 Skill 时，再创建新的通用类 Skill

`skill_manage` 操作：

| 动作          | 用途                             |
| ------------- | -------------------------------- |
| `create`      | 从零创建一个新技能               |
| `patch`       | 对现有技能做针对性修改，优先使用 |
| `edit`        | 整体重写技能                     |
| `delete`      | 删除技能                         |
| `write_file`  | 添加或更新支持文件               |
| `remove_file` | 删除支持文件                     |

## 7.6 Curator (技能维护)
每次 Agent 解决新问题并保存技能时，该技能都会落入 `~/.hermes/skills/`。若没有维护，最终可能会出现数十个范围狭窄的近似重复项，污染技能目录并浪费 token。

为防止通过自我改进循环创建的技能无限堆积，Curator 在后台维护 Agent 创建的技能。它：

- 跟踪每个技能被查看、使用和修补的频率
- 将长期未使用的技能按照 active → stale → archived 状态流转
- 定期启动一个短暂的辅助模型审查，提出合并或修补建议

### 7.6.1 运行机制
Curator 由空闲检查触发。在 Hermes 启动或 Gateway 后台 tick 时，会检查是否满足如下启动条件：

- `curator.enabled` 没有被设为 `false`
- Curator 没有被 `hermes curator pause` 暂停
- 距离上次运行已经超过 `interval_hours`，默认 168 小时（7天）
- Agent 已经空闲超过 `min_idle_hours`，默认 2 小时

Curator 启动后会在后台创建一个 AIAgent 分支运行。

首次安装或还没有 `last_run_at` 记录时，Curator 不会运行，而是写入当前时间作为基准并推迟一个时间间隔。

用户也可以通过 `hermes curator run` 手动触发；手动运行会跳过时间间隔和空闲时长门槛，但仍要求 `curator.enabled` 没有被关闭。

运行分为两个阶段：

1. **自动状态迁移**：不调用 LLM。只检查 Curator 管理范围内的技能
   - 超过 `stale_after_days` (30天) 未使用的技能变为 `stale`，
   - 超过 `archive_after_days` (90天) 未使用的技能移动到 `~/.hermes/skills/.archive/`
2. **LLM Review**：启动一个辅助模型任务
   - 查看 Curator 管理范围内的技能，决定保留、修补、合并或归档。

### 7.6.2 配置
```yaml
# ~/.hermes/config.yaml
curator:
  enabled: true           # 是否启用 Curator
  interval_hours: 168     # 自动检查间隔，默认 7 天
  min_idle_hours: 2       # Agent 空闲多久后才允许自动运行
  stale_after_days: 30    # 多久未使用后标记为陈旧
  archive_after_days: 90  # 多久未使用后归档
```

Curator 的 LLM Review 可以单独指定辅助模型：

```yaml
# ~/.hermes/config.yaml
auxiliary:
  curator:
    provider: openrouter  # 若为 auto 则代表使用主模型
    model: google/gemini-3-flash-preview
    timeout: 600
```

### 7.6.3 常用命令
```bash
hermes curator status              # 查看技能状态
hermes curator run                 # 手动运行
hermes curator run --background    # 后台运行
hermes curator run --dry-run       # 只预览，不修改技能库
hermes curator pause               # 暂停自动运行
hermes curator resume              # 恢复自动运行
hermes curator pin <skill-name>    # 固定某个技能，防止被自动处理
hermes curator unpin <skill-name>  # 取消固定
hermes curator restore my-skill    # 恢复已归档的技能
```

同样的子命令也可以在会话中通过 `/curator` 斜杠命令使用。

### 7.6.4 备份与回滚
每次 Curator 运行前，Hermes 会把 `~/.hermes/skills/` 打包备份到 `~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz`。如果某次维护结果不符合预期，可以回滚：

```bash
hermes curator rollback                           # 恢复最新备份
hermes curator rollback -y                        # 跳过确认
hermes curator rollback --list                    # 查看可用备份
hermes curator rollback --id <timestamp>          # 恢复指定备份
hermes curator backup --reason "before-refactor"  # 手动创建快照
```

备份数量可配置：

```yaml
# ~/.hermes/config.yaml
curator:
  backup:
    enabled: true
    keep: 5
```

### 7.6.5 Curator 处理范围
如果某个 Skill 不属于 bundled 内置技能，也不是 Skills Hub 安装的技能，就会落入 Curator 的处理范围。

不被 Curator 处理的 Skill：

- `~/.hermes/skills/.bundled_manifest` 记录的 bundled 内置技能
- `~/.hermes/skills/.hub/lock.json` 记录的 Skills Hub 安装技能

会被视为 Curator 处理范围的 Skill：

- Agent 通过 `skill_manage(action="create")` 创建的技能
- 用户手写 `SKILL.md` 创建的技能
- 通过 `skills.external_dirs` 暴露给 Hermes 的外部技能目录中的技能

如果某个技能不希望被自动迁移、审查或归档，应使用 `hermes curator pin <skill-name>` 将其固定。技能被固定后：

- Curator 自动状态转换会跳过它，不会把它从 `active` 迁移到 `stale` 或 `archived`
- Curator 的 LLM Review 会跳过它
- Agent 的 `skill_manage(action="delete")` 会拒绝删除它，并提示先运行 `hermes curator unpin <name>`
- `patch` 和 `edit` 仍然允许，因此 Agent 仍可修补已固定技能的内容

### 7.6.6 使用记录与报告
Curator 会维护一个伴随文件 `~/.hermes/skills/.usage.json` 记录使用遥测。每个技能对应一条记录：

```jsonc
{
  "my-skill": {
    "use_count": 12,                          // Agent 加载该技能的次数
    "view_count": 34,                         // Agent 查看该技能的次数
    "last_used_at": "2026-04-24T18:12:03Z",   // 最近一次加载时间
    "last_viewed_at": "2026-04-23T09:44:17Z", // 最近一次查看时间
    "patch_count": 3,                         // 被 skill_manage 修改的次数
    "last_patched_at": "2026-04-20T22:01:55Z",// 最近一次修改时间
    "created_at": "2026-03-01T14:20:00Z",     // 技能创建时间
    "state": "active",                        // 当前状态
    "pinned": false,                          // 是否被固定
    "archived_at": null                       // 归档时间，未归档时为 null
  }
}
```

每次 Curator 运行后，都会在 `~/.hermes/logs/curator/` 下写入一个带时间戳的目录：

```text
~/.hermes/logs/curator/
└── 20260429-111512/
    ├── run.json      # 机器可读：完整数据、统计信息、LLM 输出
    └── REPORT.md     # 人类可读：运行摘要
```

# 8. Hooks
Hook 用于在关键生命周期节点运行自定义代码。

Hermes 有三套 Hook 系统：

| 类型          | 适用场景                                                  |
| ------------- | --------------------------------------------------------- |
| Shell Hooks   | 用任意命令或脚本做轻量自动化、审计、通知和上下文注入      |
| Plugin Hooks  | 用 Python 插件做工具拦截、指标采集、防护策略和记忆召回    |
| Gateway Hooks | 在消息平台 Gateway 中监听平台、会话、Agent 和斜杠命令事件 |

## 8.1 Shell Hooks
Shell Hooks 声明在 `~/.hermes/config.yaml` 的 `hooks` 下：

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"  # 仅用于 pre/post_tool_call
      command: "~/.hermes/agent-hooks/check-tool.sh"
      timeout: 10
```

Hook 触发时，Hermes 会把 JSON 载荷通过 stdin 传入，并从 stdout 读取 JSON 响应。

## 8.2 Plugin Hooks
Plugin Hooks 通过插件 `register(ctx)` 中 `ctx.register_hook()` 以编程方式注册处理函数。

```python
def register(ctx):
    async def log_tool_call(tool_name, args, task_id, **kwargs):
        logger.info(
            "TOOL_CALL session=%s tool=%s args=%s",
            task_id,
            tool_name,
            json.dumps(args)[:200],
        )

    ctx.register_hook("pre_tool_call", log_tool_call)
```

Shell / Plugin 可挂载点：

| 挂载点                      | 触发时机                               | 常见用途                            | 是否能影响流程                        |
| --------------------------- | -------------------------------------- | ----------------------------------- | ------------------------------------- |
| `pre_tool_call`             | 工具执行前                             | 阻止危险命令、检查参数、审计调用    | 可以返回 `block` 阻止工具执行         |
| `post_tool_call`            | 工具返回后                             | 记录结果、采集指标、跟踪生成文件    | 观察型，不修改工具结果                |
| `pre_llm_call`              | 每轮 LLM 调用前                        | 注入 git 状态、外部上下文、策略提示 | 可以返回 `context` 注入额外上下文     |
| `post_llm_call`             | 每轮 LLM 调用结束后                    | 记录响应、同步记忆、采集 token 指标 | 观察型                                |
| `on_session_start`          | 新会话开始时                           | 初始化会话状态、打开外部连接        | 观察型                                |
| `on_session_end`            | 会话结束、重置或退出时                 | 清理资源、flush 缓存、发送通知      | 观察型                                |
| `on_session_finalize`       | CLI / Gateway 销毁活跃会话时           | 刷新、保存、统计                    | 观察型                                |
| `on_session_reset`          | Gateway 切换到新会话 key 时            | 记录 `/new`、`/reset` 等重置行为    | 观察型                                |
| `subagent_stop`             | `delegate_task` 子 Agent 退出时        | 记录子任务结果、耗时和状态          | 观察型                                |
| `pre_gateway_dispatch`      | Gateway 收到用户消息，认证和分发前     | 跳过、重写或放行消息                | 可以返回 `skip`、`rewrite` 或 `allow` |
| `pre_approval_request`      | 危险命令需要用户审批，提示发送前       | 记录审批请求、发送外部通知          | 观察型                                |
| `post_approval_response`    | 用户响应审批或审批超时后               | 记录审批结果                        | 观察型                                |
| `transform_tool_result`     | 工具结果交还给模型前                   | 清理、摘要或脱敏工具结果            | 可以返回字符串替换结果                |
| `transform_terminal_output` | `terminal` 输出截断、ANSI 剥离、脱敏前 | 标准化终端输出                      | 可以返回字符串替换输出                |
| `transform_llm_output`      | 最终响应交付用户前                     | 改写或同步最终文本                  | 可以返回字符串替换响应                |

## 8.3 Gateway Hooks
Gateway Hooks 放在 `~/.hermes/hooks/<name>/` 目录中，目录结构如下：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听的事件
    └── handler.py     # Python 处理函数
```

HOOK.yaml：

```yaml
name: audit
description: Log gateway commands
events:
  - command:*
```

handler.py：

```python
async def handle(event_type: str, context: dict):
    print(event_type, context)
```

Gateway 常用挂载点：

| 挂载点                                            | 触发时机                        | 常见用途                       |
| ------------------------------------------------- | ------------------------------- | ------------------------------ |
| `gateway:startup`                                 | Gateway 进程启动时              | 启动检查、告警、注册 Webhook   |
| `session:start` / `session:end` / `session:reset` | Gateway 会话创建、结束或重置时  | 记录消息平台会话、审计用户行为 |
| `agent:start` / `agent:step` / `agent:end`        | Gateway 中 Agent 处理消息的过程 | 监控长任务、记录工具循环       |
| `command:*` / `command:<name>`                    | Gateway 里执行斜杠命令时        | 命令审计、权限统计、外部通知   |

## 8.4 Shell Hook 示例：每次对话结束后弹窗提示
当一次对话结束后，`on_session_end` 会触发脚本，弹窗提示。

1. 创建脚本目录并复制脚本：

使用仓库中的 [scripts/hooks/conversation-end-popup.py](scripts/hooks/conversation-end-popup.py) 和 [scripts/hooks/mac-toast.swift](scripts/hooks/mac-toast.swift)。Windows / WSL 使用 PowerShell 弹窗，macOS 使用同目录的 `mac-toast` helper。

```bash
mkdir -p ~/.hermes/agent-hooks
cp scripts/hooks/conversation-end-popup.py ~/.hermes/agent-hooks/
cp scripts/hooks/mac-toast.swift ~/.hermes/agent-hooks/
chmod +x ~/.hermes/agent-hooks/conversation-end-popup.py
```

2. 注册 shell hook：

```yaml
# ~/.hermes/config.yaml
hooks:
  on_session_end:
    - command: "~/.hermes/agent-hooks/conversation-end-popup.py"
      timeout: 15
```

3. 测试脚本：

```bash
printf '{}' | ~/.hermes/agent-hooks/conversation-end-popup.py
```

首次运行时 Hermes 会询问是否允许这个 `(event, command)` 组合。

# 9. Plugins
Hermes 提供了一套插件系统，可在不修改核心代码的情况下添加自定义工具、钩子和集成。

## 9.1 插件能做什么
不同插件类型对应不同扩展对象，常见场景如下：

| 场景          | 可扩展内容                                         | 适用说明                                      |
| ------------- | -------------------------------------------------- | --------------------------------------------- |
| 通用插件      | 工具、钩子、斜杠命令、CLI 命令、消息注入           | 给 Agent 增加本地能力、工作流入口或自动化逻辑 |
| 插件附带资源  | Skill、模板、配置、静态数据                        | 把可复用知识或资源随插件一起分发              |
| Provider 插件 | Memory provider、Context engine、Model provider    | 替换或增强记忆、上下文压缩和模型后端          |
| Gateway 平台  | 消息平台适配器                                     | 接入新的消息平台                              |
| 媒体后端      | 图像生成、视频生成、TTS 等生成后端                 | 接入外部生成服务或本地生成引擎                |
| 宿主 LLM 调用 | 使用 Hermes 当前配置的模型做一次性补全或结构化生成 | 插件内部需要轻量模型调用时使用                |

## 9.2 插件发现与启用
Hermes 会从多个位置发现插件：

| 来源    | 路径 / 方式                          | 用途                                                                               |
| ------- | ------------------------------------ | ---------------------------------------------------------------------------------- |
| Bundled | Hermes 仓库内置 `plugins/`           | 官方随 Hermes 发布的插件                                                           |
| User    | `~/.hermes/plugins/`                 | 用户自己的本地插件                                                                 |
| Project | `.hermes/plugins/`                   | 当前工作目录插件；默认不扫描，需设置 `HERMES_ENABLE_PROJECT_PLUGINS=true` 显式信任 |
| pip     | `hermes_agent.plugins` entry points  | 通过 Python 包分发的插件                                                           |
| Nix     | `services.hermes-agent.extraPlugins` | NixOS 声明式安装插件                                                               |

Hermes 还会扫描插件子目录，用于注册特定类型的 provider 或平台适配器：

| 子目录                     | 用途                 |
| -------------------------- | -------------------- |
| `plugins/` 根目录          | 通用插件             |
| `plugins/platforms/`       | Gateway 平台适配器   |
| `plugins/image_gen/`       | 图像生成后端         |
| `plugins/video_gen/`       | 视频生成后端         |
| `plugins/memory/`          | 外部记忆 provider    |
| `plugins/context_engine/`  | 上下文压缩引擎       |
| `plugins/model-providers/` | 模型 / 推理 provider |

同名插件以最后发现的来源为准。因此，用户插件可以覆盖同名的内置插件。

用户插件以独立子目录存放，最小结构如下：

```text
~/.hermes/plugins/hello-world/
├── plugin.yaml      # 插件清单：名称、版本、描述等元信息
└── __init__.py      # 定义 register(ctx)，在这里注册插件内容
```

普通插件和用户安装的 provider 默认只会被发现，不会自动启用。需要加入 `~/.hermes/config.yaml` 的 `plugins.enabled` 后，插件才会加载工具、hooks、命令或 provider：

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - my-plugin
  disabled:  # 禁用优先于启用
    - noisy-plugin
```

## 9.3 常用命令
```bash
hermes plugins                    # 交互式开关插件
hermes plugins list               # 查看已安装插件
hermes plugins install user/repo  # 从 Git 安装插件
hermes plugins update <name>      # 更新插件
hermes plugins remove <name>      # 移除插件
hermes plugins enable <name>      # 启用插件
hermes plugins disable <name>     # 禁用插件
```

# 10. 持久记忆
Hermes Agent 拥有持久记忆。记忆有容量上限，且由 Agent 自行维护。它会跨会话保存用户偏好、项目环境和经验教训。

## 10.1 内置记忆
内置记忆由两个文件组成，存储在 `~/.hermes/memories/`：

| 文件        | 用途                                           | 字符上限                    |
| ----------- | ---------------------------------------------- | --------------------------- |
| `MEMORY.md` | Agent 的个人笔记：环境事实、项目约定、经验教训 | 2,200 字符（约 800 tokens） |
| `USER.md`   | 用户档案：用户偏好、沟通风格、期望和习惯       | 1,375 字符（约 500 tokens） |

- 这两个文件会在会话开始时注入系统提示词
- Agent 在会话中通过 `memory` 工具新增、替换或删除的记忆会立即写入磁盘，但不会在当前会话立刻生效
- 新的记忆会在下一个会话生效，以保持 LLM prefix cache 稳定
- 当记忆已满时，Agent 会整合或替换条目以腾出空间存放新信息

系统提示词中的记忆的呈现方式：

```text
══════════════════════════════════════════════
MEMORY (your personal notes) [67% — 1,474/2,200 chars]
══════════════════════════════════════════════
User's project is a Rust web service at ~/code/myapi using Axum + SQLx
§
This machine runs Ubuntu 22.04, has Docker and Podman installed
§
User prefers concise responses, dislikes verbose explanations
```

标题会显示当前容量占用，提醒 Agent 在接近上限时做合并或替换；`§` (节号符号，section sign)用来分隔不同记忆条目。

记忆相关配置：

```yaml
# ~/.hermes/config.yaml
memory:
  memory_enabled: true        # 启用持久记忆
  user_profile_enabled: true  # 启用用户档案
  memory_char_limit: 2200     # 记忆字符上限
  user_char_limit: 1375       # 用户档案字符上限
```

## 10.2 Memory 工具操作
Agent 通过 `memory` 工具管理记忆，常用动作：

| 动作      | 用途                       |
| --------- | -------------------------- |
| `add`     | 添加新的记忆条目           |
| `replace` | 替换已有条目，使用子串匹配 |
| `remove`  | 删除已有条目，使用子串匹配 |

没有 `read` 动作。记忆内容会自动注入系统提示词，Agent 在会话能直接看到。

`replace` 和 `remove` 不需要传完整条目，只需要传能唯一定位的短文本：

```text
memory(
    action="replace",
    target="memory",
    old_text="dark mode",
    content="User prefers light mode in VS Code, dark mode in terminal",
)
```

必须刚好匹配 1 条记忆；匹配 0 条会报错，匹配多条也会报错并要求提供更具体的片段。

## 10.3 记忆管理规则
`memory` 工具有两个写入目标：

| 目标     | 用途                                           |
| -------- | ---------------------------------------------- |
| `memory` | Agent 的个人笔记：环境事实、项目约定、经验教训 |
| `user`   | 用户档案：用户偏好、沟通风格、期望和习惯       |

应该主动保存到记忆中的内容：

- 用户偏好：例如「用户偏好 TypeScript 而不是 JavaScript」
- 环境事实：例如「这台服务器运行 Debian 12 和 PostgreSQL 16」
- 用户纠正：例如「Docker 命令不要用 sudo，用户已在 docker 组」
- 项目约定：例如「项目使用 tabs、120 字符行宽、Google 风格 docstring」
- 已完成的工作：例如「2026-01-15 将数据库从 MySQL 迁移到 PostgreSQL」
- 显式要求：例如「记住 API key 每月轮换」

不适合保存到记忆中的内容：

- 太模糊的信息：例如「用户问过 Python」
- 容易重新查询的通用知识
- 大段代码、日志、数据表
- 会话特定的临时内容，例如一次性文件路径或临时调试上下文
- 已经写在 `SOUL.md`、`AGENTS.md` 等上下文文件中的信息

记忆有严格字符上限：

| 存储     | 上限       | 典型条目数 |
| -------- | ---------- | ---------- |
| `memory` | 2,200 字符 | 8-15 条    |
| `user`   | 1,375 字符 | 5-10 条    |

当新增条目会超过上限时，`memory` 工具会返回错误，并附带当前条目和容量信息。Agent 应先删除或整合旧条目，使用 `replace` 合并相关记忆，再添加新条目。

当记忆使用率超过 80% 时，应先整合现有条目再添加新内容。高质量记忆条目应紧凑、具体、信息密度高。

记忆系统会拒绝完全重复的条目。如果添加的内容已经存在，会返回成功，并提示未添加重复项。

记忆条目写入前会经过安全扫描。包含提示词注入、凭证外泄、SSH 后门或不可见 Unicode 字符等风险模式的内容会被阻止。

## 10.4 会话搜索与记忆对比
除了 `MEMORY.md` 和 `USER.md`，Hermes 还可以通过 `session_search` 搜索过去的完整会话。两者用途不同：

| 对比项     | 持久记忆                           | 会话搜索                       |
| ---------- | ---------------------------------- | ------------------------------ |
| 容量       | 约 1,300 tokens                    | 所有历史会话                   |
| 速度       | 即时，会话开始时直接注入系统提示词 | FTS5 查询约 20 ms，滚动约 1 ms |
| 用途       | 始终可见的关键事实                 | 查找过去某次讨论的具体内容     |
| 管理方式   | Agent 主动维护                     | 自动保存所有会话               |
| Token 成本 | 每个会话固定占用少量上下文         | 返回的消息片段占用上下文       |

## 10.5 外部记忆提供商
Hermes Agent 内置了 8 个外部记忆提供商插件，用来提供比内置记忆更强的跨会话记忆能力。外部记忆不会替代内置记忆，而是作为叠加能力并行工作。同一时间只能启用一个外部记忆提供商。

常用命令：

```bash
hermes memory setup   # 交互式选择并配置外部记忆提供商
hermes memory status  # 查看当前启用状态
hermes memory off     # 关闭外部记忆提供商
```

也可以手动配置：

```yaml
# ~/.hermes/config.yaml
memory:
  provider: openviking
```

外部记忆 provider 激活后，Hermes 会自动：

- 将 provider 已知上下文注入系统提示词
- 在每轮对话前后台预取相关记忆
- 在每次响应后将对话轮次同步到 provider
- 在会话结束时提取记忆，取决于 provider 是否支持
- 将内置记忆写入镜像到外部 provider
- 添加 provider 专属工具，让 Agent 搜索、存储和管理外部记忆

可用 provider 包括：

| Provider      | 功能                                                    | 场景                                      | 数据存储                          | 费用                            |
| ------------- | ------------------------------------------------------- | ----------------------------------------- | --------------------------------- | ------------------------------- |
| `honcho`      | 跨会话用户建模、辩证推理、会话上下文、语义搜索          | 多 Agent 系统、用户-Agent 对齐            | Honcho Cloud 或自托管             | Honcho 定价或自托管免费         |
| `mem0`        | 服务端 LLM 事实提取、语义搜索、重排序、自动去重         | 免维护记忆管理                            | Mem0 Cloud                        | Mem0 定价                       |
| `openviking`  | 文件系统式知识层级、分层检索、6 类记忆提取              | 可结构化浏览的自托管知识管理              | 自托管，本地或云端                | 免费，AGPL-3.0                  |
| `byterover`   | CLI 持久记忆、分层知识树、分层检索、预压缩提取          | 本地优先、可移植、面向开发者的记忆管理    | 本地或 ByteRover Cloud            | 本地免费，云端按 ByteRover 定价 |
| `hindsight`   | 知识图谱、实体解析、多策略检索、跨记忆合成              | 基于知识图谱的实体关系召回                | Hindsight Cloud 或本地 PostgreSQL | 云端按 Hindsight 定价，本地免费 |
| `holographic` | 本地 SQLite 事实存储、FTS5 搜索、信任评分、HRR 代数查询 | 无外部依赖的纯本地高级检索记忆            | 本地 SQLite                       | 免费                            |
| `retaindb`    | 混合搜索、7 种记忆类型、增量压缩                        | 已使用 RetainDB 基础设施的团队            | RetainDB Cloud                    | $20/月                          |
| `supermemory` | 语义长期记忆、profile 召回、会话图谱导入、多容器        | 带用户 profile 和会话级图谱构建的语义召回 | Supermemory Cloud                 | Supermemory 定价                |

# 11. 上下文文件
Hermes Agent 会自动发现并加载上下文文件。这里的上下文文件包括项目上下文文件与 `SOUL.md`。

## 11.1 支持的上下文文件
| 文件                       | 用途                         | 发现方式                        |
| -------------------------- | ---------------------------- | ------------------------------- |
| `.hermes.md` / `HERMES.md` | 项目说明，优先级最高         | 向上遍历至 git 根目录           |
| `AGENTS.md`                | 项目指令、规范、架构说明     | 启动目录；子目录中渐进发现      |
| `CLAUDE.md`                | Claude Code 的上下文文件     | 启动目录；子目录中渐进发现      |
| `.cursorrules`             | Cursor 编码规范              | 启动目录                        |
| `.cursor/rules/*.mdc`      | Cursor 规则模块              | 启动目录                        |
| `SOUL.md`                  | 当前 Hermes 实例的人格、语气 | 只从 `HERMES_HOME/SOUL.md` 加载 |

## 11.2 上下文文件的加载
项目上下文有两种加载方式：启动时加载和渐进式加载。

### 11.2.1 启动加载
会话启动时会加载上下文文件：

1. 扫描当前工作目录，依次查找 `.hermes.md` / `HERMES.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` / `.cursor/rules/*.mdc`。
2. 读取文件 (UTF-8)
3. 安全扫描
4. 截断长文本
5. 组合到 `# Project Context` 标题下
6. 注入系统提示词

启动加载的默认截断上限是 20,000 字符。超过上限后，Hermes 保留 70% 头部和 20% 尾部，中间插入截断标记，显示字符数并建议使用文件工具：

```text
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

### 11.2.2 渐进加载
在会话进行过程中会渐进式加载上下文：

1. 每次工具调用后，从参数（path、workdir、shell 命令）中提取文件路径
2. 检查该目录及最多 5 层父目录，跳过已访问的目录
3. 每个目录按优先级查找文件，只加载首个匹配项
4. 安全扫描
5. 截断 (保留前 8,000 字符并追加截断标记)
6. 内容追加到工具结果中

### 11.2.3 安全扫描
安全扫描会检查以下内容：

1. **指令覆盖** — 例如 `ignore previous instructions`、`disregard your rules`
2. **欺骗行为** — 例如 `do not tell the user`
3. **系统提示词覆盖** — 例如 `system prompt override`
4. **隐藏 HTML 注释** — 例如 `<!-- ignore instructions -->`
5. **隐藏 div 元素** — 例如 `<div style="display:none">`
6. **凭证外泄** — 例如 `curl ... $API_KEY`
7. **密钥文件读取** — 例如 `cat .env`、`cat credentials`
8. **不可见字符** — 零宽空格、双向文本覆盖符、词连接符等

命中任意威胁模式后，文件将被阻止加载，上下文位置替换为：

```text
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

此扫描可防范常见注入模式，但不能替代对上下文文件的人工审查。

## 11.3 `SOUL.md` 与个性
`SOUL.md` 定义 Hermes Agent 的身份与个性。它会拼入系统提示词开头部分。

`SOUL.md` 行为：

- 如果 `SOUL.md` 尚不存在，Hermes 会自动生成 `~/.hermes/SOUL.md` 文件
- 如果 `SOUL.md` 为空或读取失败时，回退到内置默认身份
- 如果 `SOUL.md` 有内容，经过安全扫描和截断后注入系统提示词

`SOUL.md` 适合写长期稳定的个性和沟通偏好：

- 语气
- 风格
- 直接程度
- 默认交互风格
- 不希望出现的表达习惯
- 面对不确定性、分歧、模糊情况时的处理方式

不适合写项目说明、文件路径、仓库约定、临时流程。这些应该放进 `AGENTS.md`。

`/personality` 是会话级覆盖层，用于更改或补充当前系统提示词。Hermes 内置了多种个性：

| 人格          | 说明                                 |
| ------------- | ------------------------------------ |
| `helpful`     | 友好的通用助手                       |
| `concise`     | 简短、直击要点的回复                 |
| `technical`   | 详尽、准确的技术专家                 |
| `creative`    | 创新、突破常规的思维                 |
| `teacher`     | 耐心的教育者，配有清晰示例           |
| `kawaii`      | 可爱表达、闪光效果与热情 ★           |
| `catgirl`     | 带有猫咪表达方式的 Neko-chan，nya~   |
| `pirate`      | 船长 Hermes，精通技术的海盗          |
| `shakespeare` | 充满戏剧张力的莎士比亚式风格吟游诗人 |
| `surfer`      | 超级冷静的冲浪者氛围                 |
| `noir`        | 硬派侦探叙事风格                     |
| `uwu`         | 极致可爱的 uwu 语气                  |
| `philosopher` | 对每个问题深度沉思的哲学家           |
| `hype`        | 最大能量与热情！！！                 |

# 12. Gateway
Gateway 是 Hermes 的消息平台接入层，可以作为前台进程或后台服务运行。它负责：

- 连接消息平台
- 接收消息
- 维护每个聊天对应的会话
- 把消息转发给 Hermes Agent 处理
- 将回复发送回消息平台
- 运行 cron 调度循环，执行到期任务

## 12.1 常用命令
```bash
hermes gateway setup                  # 交互式配置消息平台
hermes gateway                        # 前台启动 Gateway
hermes gateway install                # 安装为用户服务（Linux）/ launchd 服务（macOS）
hermes gateway start                  # 启动默认服务
hermes gateway stop                   # 停止默认服务
hermes gateway status                 # 查看默认服务状态
sudo hermes gateway install --system  # 仅 Linux：安装为开机启动的系统服务
hermes gateway status --system        # 仅 Linux：检查系统服务状态
```

## 12.2 网关配对
默认情况下，网关拒绝所有不在白名单中或未通过私信配对的用户。

在 `~/.hermes/.env` 中配置白名单：

```bash
# `~/.hermes/.env`
# 按平台限制用户
TELEGRAM_ALLOWED_USERS=123456789,987654321
WEIXIN_ALLOWED_USERS=123456789,987654321

# 或配置通用允许列表
GATEWAY_ALLOWED_USERS=123456789,987654321

# 显式允许所有用户，但不推荐给有终端访问权限的机器人使用
GATEWAY_ALLOW_ALL_USERS=true
```

私信配对：无需手动配置用户 ID，未知用户在私信机器人时会收到一次性配对码 (1 小时后过期)，例如 `Pairing code: XKGH5N7P`。之后管理员在本机批准：

```bash
hermes pairing approve telegram XKGH5N7P  # 批准配对
hermes pairing list                       # 查看配对列表
hermes pairing revoke telegram <user_id>  # 撤销配对
```

## 12.3 斜杠命令权限控制
管理员与普通用户的划分决定已允许用户能运行哪些斜杠命令：

- **管理员**：可运行所有已注册的斜杠命令，包括内置命令和插件注册的命令
- **普通用户**：可正常与 Agent 对话，但只能运行显式允许的斜杠命令，以及 `/help` 和 `/whoami`

示例配置：

```yaml
# ~/.hermes/config.yaml
gateway:
  platforms:
    discord:
      extra:
        allow_from: ["111", "222", "333"]
        allow_admin_from: ["111"]                 # 管理员：所有斜杠命令
        user_allowed_commands: [status, model]    # 普通用户可运行的命令
        group_allow_admin_from: ["111"]           # 群组 / 频道管理员
        group_user_allowed_commands: [status]     # 群组 / 频道普通用户可运行的命令
```

如果某个作用域没有配置 `allow_admin_from`，该作用域不启用权限层级，所有已允许用户都拥有完整斜杠命令权限。

在任意平台使用 `/whoami` 可以查看当前作用域、自己的权限层级以及可运行的斜杠命令。

## 12.4 会话管理
Gateway 会按策略重置会话。自动重置后，下一条消息会提示这是一次自动重置后的新对话。

会话重置策略可通过 `~/.hermes/config.yaml` 的 `session_reset` 配置：

```yaml
# ~/.hermes/config.yaml
session_reset:
  mode: both
  at_hour: 4
  idle_minutes: 1440
  notify: true
  notify_exclude_platforms:
    - api_server
    - webhook
```

未配置时使用代码内置默认值：

| 配置项                     | 默认值                  | 说明                     |
| -------------------------- | ----------------------- | ------------------------ |
| `mode`                     | `both`                  | 自动重置模式             |
| `at_hour`                  | `4`                     | 每日重置小时时刻         |
| `idle_minutes`             | `1440`                  | 空闲多少分钟后重置       |
| `notify`                   | `true`                  | 自动重置后是否通知用户   |
| `notify_exclude_platforms` | `api_server`, `webhook` | 不发送自动重置通知的平台 |

`mode` 可选值：

| mode    | 说明                             |
| ------- | -------------------------------- |
| `none`  | 不自动重置，只依靠上下文压缩管理 |
| `idle`  | 空闲达到 `idle_minutes` 后重置   |
| `daily` | 每天在 `at_hour` 指定的小时重置  |
| `both`  | `idle` 和 `daily` 谁先触发就重置 |

可以在 `~/.hermes/gateway.json` 中按聊天类型或平台覆盖重置策略：

```json
{
  "reset_by_type": {
    "dm": { "mode": "idle", "idle_minutes": 720 },
    "group": { "mode": "daily", "at_hour": 6 }
  },
  "reset_by_platform": {
    "telegram": { "mode": "idle", "idle_minutes": 480 },
    "discord": { "mode": "none" }
  }
}
```

覆盖优先级：平台覆盖 > 聊天类型覆盖 > 默认策略。

# 13. Profile
通过 Profile 能够创建并运行多个独立的 Agent，每个 Agent 有独立的配置、会话、记忆、技能、定时任务，状态数据库和 Gateway。

## 13.1 常用命令
```bash
hermes profile create coder                 # 创建全新 Profile
hermes profile create coder --description "负责阅读源码、实现已明确的代码修改、修复测试或构建问题、运行必要验证，并在完成后汇报改动、测试结果和剩余风险"  # 创建带描述的 Profile
hermes profile create coder --clone         # 克隆当前 Profile 的 config.yaml、.env、SOUL.md、Skill，不复制会话和记忆
hermes profile create backup --clone-all    # 克隆完整状态：配置、API key、人格、记忆、会话、技能、定时任务、插件
hermes profile create coder --clone --clone-from backup  # 从指定 Profile 克隆
hermes profile describe coder --text "..."  # 为 Profile 添加描述
hermes profile describe coder --auto        # 用辅助模型自动生成 Profile 描述
hermes profile delete coder                 # 删除 Profile
hermes profile list                         # 显示所有 profile 及其状态
hermes profile show coder                   # 显示某个 profile 的详细信息
hermes profile rename coder dev-bot         # 重命名（同步更新别名和服务）
hermes profile export coder                 # 导出为 coder.tar.gz
hermes profile import coder.tar.gz          # 从归档文件导入
```

## 13.2 使用 Profile
每个 Profile 都会自动生成同名命令别名，位置在 `~/.local/bin/<profile-name>`。

例如创建 `coder` 后：

```bash
coder chat           # 启动 coder profile 的交互式对话
coder setup          # 运行 coder profile 的初始化 / 配置向导
coder gateway start  # 启动 coder profile 的 Gateway 服务
coder doctor         # 检查 coder profile 的健康状态
coder skills list    # 查看 coder profile 已安装的 skills
coder config set model.default anthropic/claude-sonnet-4  # 修改 coder profile 的默认模型
```

这个别名实质等价于 `hermes -p <name>`，例如 `hermes -p coder chat`。

可将 `hermes` 命令默认指向某个 Profile：

```bash
hermes profile use coder    # 默认使用 coder Profile
hermes chat                 # 现在默认使用 coder
hermes profile use default  # 恢复默认 Profile 为 default
```

## 13.3 工作原理
Profile 使用 `HERMES_HOME` 环境变量。运行 `coder chat` 时，包装脚本会在启动 Hermes 前设置 `HERMES_HOME=~/.hermes/profiles/coder`。代码中通过 `get_hermes_home()` 解析路径，把 Hermes 状态限定在对应 Profile 目录下，包括配置、会话、记忆、技能、状态数据库、Gateway PID、日志和定时任务。

# 14. Cron
Hermes 通过 `cronjob` 工具管理定时任务，可以用自然语言、cron 表达式调度自动运行的任务。

定时任务运行时会禁用 cron 管理工具，避免递归创建更多定时任务造成调度循环。

## 14.1 创建任务
可在会话中通过 `/cron`，或使用 CLI 命令 `hermes cron` 创建定时任务，也可以通过自然语言让 Hermes Agent 创建任务。

```bash
/cron add 30m "提醒我检查构建结果"
/cron add "every 2h" "检查服务器状态"
/cron add "every 1h" "总结新动态" --skill blogwatcher

hermes cron create "every 2h" "检查服务器状态"
hermes cron create "every 1h" "总结新动态" --skill blogwatcher

"每天早上 9 点检查 Hacker News 上的 AI 新闻，然后发一份摘要到 Telegram。"
```

`/cron add` 和 `hermes cron create` 都支持的常用选项：

| 选项        | 说明                                                     |
| ----------- | -------------------------------------------------------- |
| `--name`    | 设置任务名称                                             |
| `--deliver` | 设置投递目标，如 `local`、`telegram`、`platform:chat_id` |
| `--repeat`  | 设置重复次数                                             |
| `--skill`   | 附加 skill，可重复传递                                   |

`hermes cron create` 独有选项：

| 选项         | 说明                                       |
| ------------ | ------------------------------------------ |
| `--script`   | 指定 `~/.hermes/scripts/` 下的脚本         |
| `--no-agent` | 跳过 LLM，运行脚本并直接投递 stdout        |
| `--workdir`  | 指定任务运行目录，并注入该目录的上下文文件 |

对于不需要 LLM 推理的任务（例如监控程序、磁盘 / 内存警报、心跳检测、CI ping 等），可在创建任务时使用 `--no-agent`。调度程序会运行脚本并直接输出其标准输出，完全跳过 Agent：

```bash
hermes cron create "every 5m" \
  --no-agent \
  --script memory-watchdog.sh \
  --deliver telegram \
  --name "memory-watchdog"
```

脚本必须放在 `~/.hermes/scripts/`。`.sh`、`.bash` 用 `/bin/bash` 执行，其他脚本在当前 Python 解释器（sys.executable）下运行。

脚本运行默认超时时间是 120 秒，可以通过配置调整：

```yaml
# ~/.hermes/config.yaml
cron:
  script_timeout_seconds: 300
```

Hermes 通过自然语言创建任务时，会在内部调用 `cronjob` 工具，常见字段示例：

```text
cronjob(
    action="create",
    schedule="every 1d at 09:00",
    prompt="检查 Hacker News 上的 AI 新闻，筛选值得关注的条目，并写成中文摘要。",
    name="HN AI daily",
    deliver="telegram",
    workdir=None,
    skills=[],
    repeat=None,
    context_from=[],
    script=None,
    no_agent=False,
    enabled_toolsets=["web"],
)
```

任务存储在 `~/.hermes/cron/jobs.json`，运行输出会保存到 `~/.hermes/cron/output/{job_id}/{timestamp}.md`。

## 14.2 管理任务
可在会话中通过 `/cron`，或使用 CLI 命令 `hermes cron` 查看、编辑、暂停、恢复、触发和删除定时任务。

```bash
/cron list                                             # 查看启用中的定时任务
/cron list --all                                       # 查看所有任务，包括已暂停的任务
/cron edit <job_id> --schedule "every 4h"              # 修改调度时间
/cron edit <job_id> --prompt "使用新的任务说明"          # 修改任务说明
/cron edit <job_id> --name "新的任务名"                 # 修改任务名称
/cron edit <job_id> --deliver telegram,discord        # 修改投递目标
/cron edit <job_id> --repeat 5                        # 设置重复次数
/cron edit <job_id> --skill blogwatcher --skill maps  # 替换当前任务的技能列表
/cron edit <job_id> --add-skill maps                  # 追加技能
/cron edit <job_id> --remove-skill blogwatcher        # 移除指定技能
/cron edit <job_id> --clear-skills                    # 清空所有技能
/cron pause <job_id>                                  # 暂停任务
/cron resume <job_id>                                 # 恢复任务
/cron run <job_id>                                    # 下一个 scheduler tick 触发任务
/cron remove <job_id>                                 # 删除任务

hermes cron list/create/edit/pause/resume/run/remove
hermes cron edit <job_id> --script watch-site.py      # 设置脚本输入
hermes cron edit <job_id> --script ""                 # 清除脚本
hermes cron edit <job_id> --no-agent                  # 启用 no-agent 模式
hermes cron edit <job_id> --agent                     # 恢复 Agent 执行模式
hermes cron edit <job_id> --workdir /home/me/projects/acme  # 修改运行目录
hermes cron edit <job_id> --workdir ""                # 清除运行目录
hermes cron status                                    # 查看 Gateway 和 cron 状态
hermes cron tick                                      # 手动运行一次到期任务检查
```

## 14.3 调度格式
| 类型        | 示例                                      | 行为                 |
| ----------- | ----------------------------------------- | -------------------- |
| 相对延迟    | `30m`、`2h`、`1d`                         | 一次性运行           |
| 循环间隔    | `every 30m`、`every 2h`、`every 1d`       | 周期性运行           |
| Cron 表达式 | `0 9 * * *`、`0 9 * * 1-5`、`0 */6 * * *` | 按 cron 规则重复运行 |
| ISO 时间    | `2026-03-15T09:00:00`                     | 运行一次             |

Cron 表达式格式为 `分 时 日 月 周`，例如：

- `0 9 * * *` 每天 9:00 执行
- `0 9 * * 1-5` 工作日每天 9:00 执行
- `0 */6 * * *` 每 6 小时执行
- `30 8 1 * *` 每月 1 日 8:30 执行

## 14.4 工作原理
定时任务的执行通过 Gateway 守护进程处理，Gateway 每 60 秒 tick 一次调度器，每次 tick 时：

- 从 `~/.hermes/cron/jobs.json` 加载任务
- 对照当前时间检查任务是否需要运行
- 为每个到期任务启动全新的 `AIAgent` 会话
- 可选地将一个或多个已附加的 `skill` 注入该新会话
- 将 `prompt` 运行至完成
- 投递最终响应
- 更新运行元数据和下次调度时间

## 14.5 结果投递
`deliver` 控制定时任务运行完成后，把任务的最终结果或失败错误通知发送到哪里。

常见投递目标：

| deliver                        | 说明                                   |
| ------------------------------ | -------------------------------------- |
| `origin`                       | 回到创建任务的聊天来源，消息平台默认值 |
| `local`                        | 只保存到本地文件，CLI 默认值           |
| `telegram`、`discord`、`slack` | 投递到对应平台的 home channel          |
| `telegram:123456`              | 投递到指定 Telegram chat ID            |
| `discord:#engineering`         | 投递到指定 Discord 频道                |
| `all`                          | 投递到所有已配置 home channel 的平台   |
| `telegram,discord`             | 投递到多个指定平台                     |
| `origin,all`                   | 投递到来源聊天加上所有其他已连接频道   |

示例：

```bash
hermes cron create "every 30m" "检查服务状态" --deliver telegram
hermes cron create "every 1d" "生成日报" --deliver telegram,discord
hermes cron create "every 1h" "检查异常，有问题才报告" --deliver all
```

默认投递内容会带有定时任务的头尾内容，以便用户知晓其来自于定时任务：

```text
Cronjob Response: Morning feeds
-------------

<agent output here>

Note: The agent cannot see this message, and therefore cannot respond to it.
```

可以在配置中关闭包装：

```yaml
# ~/.hermes/config.yaml
cron:
  wrap_response: false
```

如果 Agent 的最终回复以 `[SILENT]` 开头，成功运行时会抑制投递，但输出仍会保存到本地；失败任务仍会投递错误信息。这可用于那些只有出现问题才需要报告的作业：

```text
Check if nginx is running. If everything is healthy, respond with only [SILENT].
Otherwise, report the issue.
```

## 14.6 通过 context_from 串联任务
Cron 任务彼此之间默认隔离：每次运行都是新的 Agent 会话。`context_from` 用来把一个任务的最新输出接到另一个任务的 prompt 前面。

示例：

```text
# 任务 1：收集原始数据
cronjob(
    action="create",
    prompt="Fetch the top 10 AI/ML stories from Hacker News. Save them to ~/.hermes/data/briefs/raw.md in markdown format with title, URL, and score.",
    schedule="0 7 * * *",
    name="AI News Collector",
)

# 任务 2：分类——接收任务 1 的输出作为上下文
# 从 cronjob(action="list") 获取任务 1 的 ID
cronjob(
    action="create",
    prompt="Read ~/.hermes/data/briefs/raw.md. Score each story 1–10 for engagement potential and novelty. Output the top 5 to ~/.hermes/data/briefs/ranked.md.",
    schedule="30 7 * * *",
    context_from="<job1_id>",
    name="AI News Triage",
)

# 任务 3：发布——接收任务 2 的输出作为上下文
cronjob(
    action="create",
    prompt="Read ~/.hermes/data/briefs/ranked.md. Write 3 tweet drafts (hook + body + hashtags). Deliver to telegram:7976161601.",
    schedule="0 8 * * *",
    context_from="<job2_id>",
    name="AI News Brief",
)
```

`context_from` 支持单个 job ID 或多个 job ID：

| 格式         | 示例                              |
| ------------ | --------------------------------- |
| 单个上游任务 | `context_from="a1b2c3d4"`         |
| 多个上游任务 | `context_from=["job_a", "job_b"]` |

多个上游输出会按列表顺序拼接。

运行时 Hermes 会读取上游任务在 `~/.hermes/cron/output/{job_id}/` 下最近一次完成的输出，拼接到下游任务的 prompt 前。

每个上游输出在注入前会被截断至 8,000 字符（超出部分以 `[... output truncated ...]` 标记），避免 prompt 过度膨胀。

> 注意：`context_from` 只能由 Agent 通过 `cronjob` 工具设置。

> 注意：`context_from` 读取的是上游任务「最近一次已完成输出」，不会等待同一个 tick 中仍在运行的上游任务。如果上游本次运行还没结束、下游已经触发，下游会拿到上游上一次完成的结果。需要强依赖同一批数据时，应把上下游任务错开足够长的时间，或把多个步骤合并到同一个 cron prompt / 脚本里串行执行。

# 15. Delegation
`delegate_task` 工具会生成具有隔离上下文、受限工具集和独立终端会话的子 Agent 实例。

## 15.1 单任务与并行批量
**单任务：**

```text
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"]
)
```

**并行（默认最多 3 并发，可通过 `max_concurrent_children` 配置）：**

```text
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]}
])
```

超过 `max_concurrent_children` 的批量请求会返回工具错误。

结果按输入顺序排列，不受完成先后影响。

`delegate_task` 是同步的，父 Agent 中断会传播到所有活跃子 Agent。

## 15.2 子 Agent 上下文
子 Agent 启动时拥有全新对话，其唯一上下文来自父 Agent 传入的 `goal` 和 `context` 两个字段：

- `goal`：任务目标（必填）
- `context`：完成目标所需的全部背景信息——错误详情、文件路径、项目位置、环境约束等

子 Agent 完成后，只返回结构化摘要（包括所做的事情、发现的内容、修改的文件以及遇到的问题）。

## 15.3 工具集限制
`toolsets` 参数限制子 Agent 可用工具，例如：

| toolsets                      | 适用场景             |
| ----------------------------- | -------------------- |
| `["terminal", "file"]`        | 编码、调试、文件编辑 |
| `["web"]`                     | 调研、查文档         |
| `["terminal", "file", "web"]` | 全栈任务（默认）     |

某些工具限制为子 Agent 无法使用，无论是否在 `toolsets` 中指定：

| 工具             | 原因                                      |
| ---------------- | ----------------------------------------- |
| `delegation`     | 叶子节点禁止再次委派（orchestrator 保留） |
| `clarify`        | 子 Agent 不能与用户交互                   |
| `memory`         | 不写入共享持久记忆                        |
| `code_execution` | 子 Agent 应逐步推理                       |
| `send_message`   | 无跨平台副作用                            |

## 15.4 嵌套委派
默认委派是扁平的：父 Agent（深度 0）只能生成一层子 Agent（深度 1），子 Agent 默认是 `leaf`，不能继续委派。

配置示例：

```yaml
# ~/.hermes/config.yaml
delegation:
  max_concurrent_children: 3  # 单次批量委派的并行子 Agent 上限
  max_spawn_depth: 2          # 最大子 Agent 嵌套深度  🠜
  orchestrator_enabled: true  # 是否允许子 Agent 为 orchestrator  🠜
  # model: "google/gemini-3-flash-preview"  # 可选：为子 Agent 指定模型
  # provider: "openrouter"                  # 可选：为子 Agent 指定 provider
```

调用示例：

```text
delegate_task(
    goal="Survey three code review approaches and recommend one",
    role="orchestrator",  🠜
    context="...",
)
```

`role` 默认 `leaf`；`orchestrator` 保留 `delegation` 工具集，但仍受 `max_spawn_depth` 限制。

# 16. Kanban
Hermes Kanban 提供了一个可恢复、可审计、可中途介入的工作队列，让多个 Agent 协作。

## 16.1 Kanban 的目标
`delegate_task` 存在无法覆盖的工作场景：

1. **研究分流与综合**：并行"研究员 -> 分析师 -> 写作者"，支持人工介入。
2. **定时循环工作流**：周期性简报，跨运行累积知识，支持失败恢复。
3. **工程流水线**：分解 → 在并行 worktree 中实现 → 审查 → 迭代 → PR，并保留贡献和交接记录。

这些场景需要如下能力：

- 跨运行持久状态
- 跨 Agent 交接工作
- 人类或其他 Agent 介入
- 任务可审计

## 16.2 Kanban 架构
三层架构：

- 控制层：用户通过 CLI、Gateway 和 Dashboard 与 Kanban 交互，包括创建任务、查看进展、补充人工反馈
- 状态层：共享看板，保存任务、依赖、评论、认领、心跳和执行记录；调度器推进就绪任务、原子认领并启动 worker
- 执行层：多个相互独立的 Agent 进程作为 worker，worker 之间不直接通信，所有输入、输出、状态变化和交接都写回看板

```text
CONTROL
+------------------------------+
| USER                         |
| CLI / Telegram / Discord     |
+------------------------------+
       |
       | /kanban create | list | comment
       v

STATE
+--------------+  read/write  +-------------------------+
| kanban.db    | -----------> | DISPATCHER (cron, 60s)  |
| SQLite (WAL) |              | 1. recompute READY      |
+--------------+              | 2. atomic claim (CAS)   |
      ^                       | 3. spawn worker         |
      |                       +-------------------------+
      |                                  |
      | complete                         | spawn
      |                                  v

EXECUTION
+-------------------------------------------------+
| +------------------+   +--------------------+   |
| | planner          |   | researcher         |   |
| | own $HERMES_HOME |   | workspace: scratch |   |
| +------------------+   +--------------------+   |
|                                                 |
| +-------------------+  +---------------------+  |
| | inbox-triage      |  | backend-eng         |  |
| | workspace: ~/Mail |  | workspace: worktree |  |
| +-------------------+  +---------------------+  |
+-------------------------------------------------+
```

## 16.3 Kanban 核心概念
### 16.3.1 Board
Board 是一个独立的任务队列，拥有自己的：

- SQLite 数据库 (`~/.hermes/kanban/boards/<slug>/kanban.db`)
- workspaces 目录
- logs 目录
- 调度循环

可以有多个 board。调度器启动 worker 时会固定 `HERMES_KANBAN_BOARD`，让 worker 只看到自己所属的 board。默认 board 的数据库位于 `~/.hermes/kanban.db`。

### 16.3.2 Task
Task 是 Kanban 的基本工作单元，一个 Task 对应 `tasks` 表的一行记录，通常包含标题、正文、一个指派人、状态、workspace、租户等。

task 的状态包括：

| 状态        | 说明                                                             |
| ----------- | ---------------------------------------------------------------- |
| `triage`    | 待分流 / 待明确，通常还需要补充信息或拆解                        |
| `todo`      | 已创建但尚未满足运行条件，可能还在等待父任务完成                 |
| `scheduled` | 已暂缓调度，等待后续由 cron、人工或其他自动化调用 `unblock` 恢复 |
| `ready`     | 已满足运行条件，可以被 dispatcher 认领                           |
| `running`   | 已被认领，worker 正在执行                                        |
| `blocked`   | 执行被阻塞，需要人工输入、修复问题或等待外部条件                 |
| `review`    | 等待审查，通常是 worker 完成 PR 后交给审查 worker 验证           |
| `done`      | 已完成                                                           |
| `archived`  | 已归档，不再参与正常调度                                         |

### 16.3.3 Link
Link 是 task 之间的父子依赖，对应 `task_links` 表中的一行 (`parent_id -> child_id`) 记录。当所有父任务都为 `done` / `archived` 后，调度器会把子任务推进到 `ready`。

### 16.3.4 Comment
Comment 是人类或 Agent 在 task 上追加的持久消息，也是 Kanban 的跨 Agent 交接协议，对应 `task_comments` 表。worker 被启动或重新启动时，会读取完整评论串。人类可以通过评论补充要求、回答 worker 的问题、纠正方向；Agent 也可以通过评论留下中间发现、交接说明。

### 16.3.5 Event
Event 是 Kanban 的任务审计日志，对应 `task_events` 表。它记录 task 的状态变化、人工编辑和 worker 执行遥测：

- **任务生命周期**：
  - `created`（创建）
  - `promoted`（依赖满足后推进到 `ready`）
  - `claimed`（被调度器认领）
  - `completed`（完成）
  - `blocked`（阻塞）
  - `unblocked`（解除阻塞）
  - `archived`（归档）
- **人工编辑**：
  - `assigned`（改派指派人）
  - `edited`（编辑标题或正文）
  - `reprioritized`（调整优先级）
  - `status`（直接改状态）
- **worker 遥测**：
  - `spawned`（worker 已启动）
  - `heartbeat`（worker 心跳）
  - `reclaimed`（认领过期后回收）
  - `crashed`（worker 崩溃）
  - `timed_out`（运行超时）
  - `stale`（长时间无心跳后判定陈旧）
  - `respawn_guarded`（重启被保护策略拦截）
  - `spawn_failed`（worker 启动失败）
  - `protocol_violation`（协议违例）
  - `gave_up`（熔断器放弃重试）

### 16.3.6 Workspace
Task 绑定的 workspace 会作为其 worker 执行时所在的目录。Kanban 支持如下 workspace 类型：

- `scratch`：默认模式，为 task 创建新的临时工作目录
- `dir:<path>`：使用已有绝对路径
- `worktree`：用于代码任务的 git worktree，由 worker 侧执行 `git worktree add` 创建

### 16.3.7 Dispatcher
调度器是一个默认运行在 Gateway 内部的长期循环。它每次 tick（默认 60 秒）扫描所有 board，回收异常任务，推进就绪任务，认领可启动任务，并为已分配指派人的任务启动 worker。

### 16.3.8 Worker
Worker 是调度器启动的独立 Hermes profile 进程。调度器启动 worker 时会设置 `HERMES_KANBAN_TASK` 等环境变量，让 worker 自动获得任务范围内的 `kanban_*` 工具，并在系统提示词中注入 Kanban 生命周期指引。

1. 启动后先调用 `kanban_show()`，读取 task 标题、正文、父任务交接、历史运行记录和完整评论串
2. 进入 `$HERMES_KANBAN_WORKSPACE`，在 task 绑定的 workspace 中执行工作
3. 定期调用 `kanban_heartbeat(note="...")`，刷新心跳并留下进度说明
4. 完成时调用 `kanban_complete(summary="...", metadata={...})`；卡住时调用 `kanban_block(reason="...")`

### 16.3.9 Tenant
Tenant 是 task 上的租户标识，对应 `tasks.tenant` 字段。适用于同一 board 中同一 profile 服务多个业务上下文的场景（如多个客户、项目、账号或业务域）。

Tenant 的行为：

- task 会保存 `tenant` 字段
- worker 进程的 `HERMES_TENANT` 带有 `tenant` 信息
- `kanban_show()` 返回的上下文中包含 `Tenant: <name>`

Tenant 的继承：

- worker 或 orchestrator profile 调用 `kanban_create` 创建子任务时默认继承当前环境里的 `HERMES_TENANT`
- 分解器拆解出的子任务继承原始 task 的 `tenant`

Tenant 本身只是一个标识，不会自动绑定 workspace，也不会自动隔离记忆。需要隔离业务数据时，应在创建任务时显式绑定 workspace；需要保存租户相关长期信息时，应在记忆内容中显式带上 tenant 前缀。如果不同业务需要不同身份、不同工具权限或不同长期记忆，应创建不同 profile。

## 16.4 协作模式
1. 扇出

   ```text
   goal
   ├── researcher-a
   ├── researcher-b
   └── researcher-c
   ```

2. 流水线

   ```text
   researcher -> analyst -> writer -> reviewer
   ```

3. 扇入

   ```text
   researcher-a \
   researcher-b  -> reviewer / aggregator
   researcher-c /
   ```

4. 长期运行日志

   同一个 profile 在同一个 workspace 周期性处理任务，通过持久记忆和共享 workspace 累积经验，并利用 Kanban 充当审计时间线。适合日报、周报、监控巡检、收件箱分流这类工作。

5. 人工介入

   Worker 遇到不确定的情况时，把 task 置为 `blocked`，并在任务评论中附上疑问。用户或其他 profile 通过评论回复并 unblock 任务。调度器重新启动 worker，任务评论会成为下一次 worker 的上下文。

   ```text
   worker 执行 -> block(reason) -> 用户评论 -> unblock -> 调度器重新启动 worker
   ```

6. 批量对象作业

   同一个 profile 通过 N 个 task 管理 N 个对象，这里的对象可以是社媒账号、客户、服务器、仓库、监控服务或数据源，每个对象有自己的 workspace。

   例如一个 `insta-manager` profile 管理多个 Instagram 账号：

   ```text
   task: post daily story for acct-1   -> assignee=insta-manager, workspace=dir:~/insta/acct-1/
   task: post daily story for acct-2   -> assignee=insta-manager, workspace=dir:~/insta/acct-2/
   ...
   task: post daily story for acct-50  -> assignee=insta-manager, workspace=dir:~/insta/acct-50/
   ```

## 16.5 任务分解与编排
调度器只负责推进任务状态，无法判断目标如何拆解、子任务如何分配、以及子任务完成后整体目标是否完成。这些工作需要分解器（Decomposer）和编排 profile（Orchestrator Profile）来执行。

- Decomposer：Gateway 内的辅助 LLM 流程，负责把 `triage` task 拆成 JSON 任务图，并创建子任务和依赖关系。
- Orchestrator Profile：普通 Hermes profile，负责承接 root task，读取子任务结果，判断整体目标是否完成，并在需要时追加任务或阻塞等待输入。

任务分解与编排流程如下：

1. `triage` task 进入分解流程。
2. 分解器读取 `triage` task 的标题和正文、可用 profile 及其描述。
3. 分解器生成 JSON 任务图，描述 task 是否需要拆分、要创建哪些子任务、每个子任务分配给谁，以及子任务之间的依赖关系。
4. 分解器根据 JSON 任务图创建子任务，并建立子任务之间的依赖关系。
5. 原始 `triage` task 变成 root task，作为子任务图完成后的汇总任务，并将 `assignee` 设置为 `kanban.orchestrator_profile`。
6. 子任务全部完成后，root task 推进到 `ready`。
7. 调度器启动 root task 当前 `assignee` 对应的 profile worker。
8. 编排器读取子任务结果，做总体验收和汇总：如果目标已经完成，就完成 root task；如果还缺步骤，就继续追加 task 或留下阻塞说明。

分解器支持自动和手动两种触发模式：

- 自动模式：调度器每个 tick 自动触发分解器。
- 手动模式：用户在 Dashboard 点 Decompose，或运行 `hermes kanban decompose <id>`，或在聊天里使用 `/kanban decompose <id>` 来触发分解器。

相关配置：

```yaml
# ~/.hermes/config.yaml
kanban:
  auto_decompose: true        # 是否让调度器每 tick 自动运行分解器
  auto_decompose_per_tick: 3  # 每个 tick 最多拆解几个 triage 任务
  orchestrator_profile: ""    # root task 的默认 assignee；空值表示使用当前默认 profile
  default_assignee: ""        # 指派到未知 profile 时的兜底；空值表示使用当前默认 profile

auxiliary:
  kanban_decomposer:          # 分解器的辅助模型
    provider: ""
    model: ""
  profile_describer:          # 自动生成 profile 描述的辅助模型
    provider: ""
    model: ""
```

创建 `orchestrator` profile，并把它配置为自动拆解后 root task 的默认 assignee：

```bash
hermes profile create orchestrator --clone

orchestrator tools disable terminal file web browser code_execution

hermes config set kanban.orchestrator_profile orchestrator
hermes config set kanban.auto_decompose true
```

## 16.6 命令工具
基本形式：

```bash
hermes kanban [--board <slug>] <action> [options]
```

Hermes 会按 `--board <slug>` -> `HERMES_KANBAN_BOARD` -> `~/.hermes/kanban/current` -> `default` 的优先级决定要操作的 board。

### 16.6.1 快速启动
```bash
hermes kanban init      # 创建 kanban.db，已存在时不会破坏数据
hermes gateway install  # 安装 Gateway 为服务
hermes gateway start    # 启动 Gateway
hermes kanban create "research Hermes Agent" --assignee researcher  # 创建任务
hermes kanban watch     # 实时观察事件
hermes kanban list      # 查看任务列表
hermes kanban stats     # 查看任务统计
```

### 16.6.2 Board 管理
多 board 用于把不同项目、仓库或业务域隔离到不同 SQLite DB、workspace 和日志目录中。

```bash
hermes kanban boards list [--all] [--json]  # 列出 board；--all 包含已归档 board，--json 输出机器可读结果
# 创建 board
hermes kanban boards create <slug> \
  [--name "Display Name"] \
  [--description "..."] \
  [--icon "..."] \
  [--color "..."] \
  [--switch]
hermes kanban boards switch <slug>  # 切换当前默认 board
hermes kanban boards show           # 查看当前 board
hermes kanban boards rename <slug> "New Display Name"  # 修改显示名；slug 是目录名，不会被改
hermes kanban boards rm <slug>          # 归档 board；默认移动到 boards/_archived/<slug>-<ts>/
hermes kanban boards rm <slug> --delete # 硬删除 board；不可恢复
hermes kanban --board <slug> list       # 临时查看某个 board，不改变当前默认 board
hermes kanban --board <slug> create "Restart service" --assignee ops  # 临时在某个 board 创建任务
```

### 16.6.3 创建、查询和指派
```bash
# 创建 task
hermes kanban create "<title>" \
  [--body "..."] \
  [--assignee <profile>] \
  [--parent <id>]... \
  [--tenant <name>] \
  [--workspace scratch|worktree|worktree:<path>|dir:<absolute-path>] \
  [--branch <name>] \
  [--priority N] \
  [--triage] \
  [--idempotency-key KEY] \
  [--max-runtime 30m|2h|1d|<seconds>] \
  [--max-retries N] \
  [--skill <name>]... \
  [--json]
hermes kanban list [--mine] [--assignee P] [--status S] [--tenant T] [--archived] [--json]  # 列表
hermes kanban show <id> [--json]       # 查看单个 task；包含评论、事件、依赖和运行信息
hermes kanban assign <id> <profile>    # 指派 / 改派
hermes kanban assign <id> none         # 取消 assignee
hermes kanban assignees [--json]       # 查看可用 assignee：磁盘上的 profile + 每个 assignee 的 task 数
```

常用创建参数：

- `--assignee <profile>`：指定执行 task 的 Hermes profile。
- `--parent <id>`：建立父依赖；可以多次传入，用于指定多个父任务。父任务未完成前，子任务留在 `todo`。
- `--tenant <name>`：给 task 打租户 / 业务域标签。
- `--workspace scratch`：默认临时目录。
- `--workspace dir:<absolute-path>`：绑定已有共享目录；必须是绝对路径。
- `--workspace worktree` / `worktree:<path>`：给编码任务创建 git worktree。
- `--triage`：把粗略想法放进 `triage` 列，等待 `specify` / `decompose` 或自动拆解。
- `--idempotency-key KEY`：适合 webhook / cron，重复调用返回已有 task，避免重复创建。
- `--max-runtime`：单次 worker 最大运行时间。
- `--max-retries`：覆盖该 task 的失败重试 / circuit breaker 上限。
- `--skill <name>`：给这个 task 额外加载技能；可以多次传入，用于加载多个技能。

### 16.6.4 依赖和生命周期
```bash
hermes kanban link <parent_id> <child_id>      # 建立依赖
hermes kanban unlink <parent_id> <child_id>    # 删除依赖
hermes kanban claim <id> [--ttl SECONDS]       # 手动原子认领 ready task；主要用于调试
hermes kanban comment <id> "<text>" [--author NAME]  # 添加评论；下一次 worker 会在 kanban_show() 里读到
hermes kanban complete <id> [--result "..."] [--summary "..."] [--metadata '{"key":"value"}']  # 完成 task；--summary/--metadata 是结构化交接信息
hermes kanban complete <id>... [--result "..."]       # 批量完成；批量 close 不应使用同一份 --summary/--metadata
hermes kanban block <id> "<reason>" [--ids <id>...]   # 阻塞 task，等待人或其他 profile 输入
hermes kanban schedule <id> "<reason>"                # 暂缓指定 task
hermes kanban unblock <id>...                         # 解除 blocked / scheduled。依赖都完成时回到 ready，否则回到 todo
hermes kanban archive <id>...                         # 归档 task；默认列表不再显示，后续 gc 可清理 scratch workspace
```

生命周期类命令中，`complete`、`block`、`unblock`、`archive` 支持多个 task id，适合批量清理：

```bash
hermes kanban complete t_abcd1234 t_def56789 t_9876fedc --result "batch wrap"
hermes kanban block t_abcd1234 "need input" --ids t_def56789 t_9876fedc
hermes kanban unblock t_abcd1234 t_def56789
hermes kanban archive t_abcd1234 t_def56789 t_9876fedc
```

### 16.6.5 Triage、规格化和拆解
`triage` 列用于接收粗略想法。可以手动触发，也可以让 dispatcher 在 `kanban.auto_decompose: true` 时自动处理。

```bash
hermes kanban specify <id> [--author NAME] [--json]                 # 把 triage task 补全成明确 spec
hermes kanban specify --all [--tenant T] [--author NAME] [--json]   # 批量规格化 triage task；可按 tenant 限定范围
hermes kanban decompose <id> [--author NAME] [--json]               # 把 triage task 拆成子任务图，并根据 profile description 路由
hermes kanban decompose --all [--tenant T] [--author NAME] [--json] # 批量拆解 triage task；可按 tenant 限定范围
```

`specify` 使用 `auxiliary.triage_specifier` 模型配置；`decompose` 使用 `auxiliary.kanban_decomposer` 模型配置。`decompose` 如果判断不需要 fan-out，会退化成类似 `specify` 的单任务补全。

### 16.6.6 运行、日志和监控
```bash
hermes kanban tail <id>          # 跟踪单个 task 的事件流
hermes kanban watch [--assignee P] [--tenant T] [--kinds completed,blocked,...] [--interval SECS]  # 观察整个 board 的事件流
hermes kanban runs <id> [--json]             # 查看一个 task 的 run history；一次认领、启动、失败或完成就是一条 run
hermes kanban stats [--json]                 # 查看状态和 assignee 统计
hermes kanban log <id> [--tail BYTES]        # 查看 worker 日志
hermes kanban context <id>                   # 打印 worker 会看到的完整上下文：title、body、父任务结果、评论等
```

### 16.6.7 Dispatcher 和维护
```bash
hermes kanban dispatch [--dry-run] [--max N] [--failure-limit N] [--json]  # 手动跑一次 dispatcher tick；用于调试或跳过默认 60 秒等待
hermes kanban gc [--event-retention-days N] [--log-retention-days N]       # 清理归档 task 的 scratch workspace、旧事件、旧日志
```

### 16.6.8 Gateway 通知订阅
从 Gateway 里用 `/kanban create ...` 创建的 task 会自动订阅 originating chat 的终态事件。脚本或 Cron 创建的 task 如果也想投递到某个平台，可以显式管理订阅：

```bash
# 订阅终态通知
hermes kanban notify-subscribe <id> \
  --platform <name> \
  --chat-id <id> \
  [--thread-id <id>] \
  [--user-id <id>]
hermes kanban notify-list [<id>] [--json]  # 查看订阅；不传 id 时列出全部
# 取消订阅
hermes kanban notify-unsubscribe <id> \
  --platform <name> \
  --chat-id <id> \
  [--thread-id <id>]
```

task 到达 `done` 或 `archived` 后，订阅会自动移除。

### 16.6.9 `/kanban` slash command
所有 `hermes kanban <action>` 都可以在交互式 CLI 或消息平台 Gateway 中写成 `/kanban <action>`。两者复用同一套 argparse，所以参数和输出格式一致：

```text
/kanban list
/kanban show t_abcd1234
/kanban create "write launch post" --assignee writer --parent t_1234abcd
/kanban comment t_abcd1234 "looks good, ship it"
/kanban unblock t_abcd1234
/kanban dispatch --max 3
/kanban specify t_abcd1234
/kanban specify --all --tenant engineering
/kanban decompose t_abcd1234
```

`/kanban` 在 Gateway 中会绕过 running-agent guard：即使某个 agent 正在运行，也可以立刻执行 `list`、`show`、`comment`、`unblock`、`assign`、`archive` 等 board 操作。消息平台有长度限制，`/kanban list`、`/kanban show`、`/kanban tail` 的长输出可能被截断；终端里的 `hermes kanban ...` 没有这层消息长度限制。

# 17. 案例：深度搜索
## 17.1 定位
Hermes 版 DeepResearch 是一条可确认、可追溯、可恢复的研究生产线。它接收自然语言研究需求，通过 Hermes Profile、Skill、MCP 工具和 Kanban 长任务队列完成研究计划、资料检索、证据整理、章节写作、综合结论和报告渲染。

## 17.2 核心特性
| 特性         | 说明                                                           |
| ------------ | -------------------------------------------------------------- |
| 研究计划先行 | 在执行检索前生成研究任务书、研究计划和大纲                     |
| 用户可控     | 在约束、任务书、大纲、补充来源和章节重跑等节点允许用户介入     |
| 多源研究     | 支持公开网页、指定网站、上传文件、内部知识库、数据库和外部 API |
| 可追溯引用   | 每个关键判断通过证据链关联来源和事实卡片                       |
| 长任务可恢复 | 使用 Kanban 保存任务状态、依赖、日志、失败重试和人工处理记录   |
| 章节级重跑   | 每个章节独立检索、写作和保存，可单章重跑                       |
| 工具可扩展   | 通过 MCP 接入搜索、网页读取、知识库、企业系统和报告渲染工具    |
| 多格式交付   | 通过 Document IR 输出 HTML、PDF、Markdown、PPT 或前端组件      |

## 17.3 执行流程
1. 用户提交自然语言研究需求。
2. `research-orchestrator` 判断是否需要向用户确认可选研究约束。
3. 用户补充约束，或明确不需要限定。
4. `research-orchestrator` 生成 `ResearchBrief`，固化研究目标、范围、排除项、关键问题、默认假设和交付标准。
5. 用户确认或修改 `ResearchBrief`。
6. `research-orchestrator` 生成 `ResearchPlan` 和 `ResearchOutline`。
7. 用户确认或修改研究大纲。
8. `research-orchestrator` 拆解检索任务和章节任务。
9. `search-worker` 执行公开网页、指定站点、内部知识库、上传文件和外部 API 检索。
10. `source-reviewer` 去重来源、评估可信度、整理证据链、事实卡片和风险说明。
11. `section-writer` 基于证据链写作章节正文、关键发现、表格、图表和章节风险。
12. `synthesis-writer` 汇总跨章节结论、建议和全局风险。
13. `report-renderer` 将结构化研究结果渲染为报告版本。

## 17.4 Hermes 架构
```text
用户 / Gateway / API
  -> Hermes Kanban
  -> Hermes Profiles
  -> Skills
  -> MCP 工具
  -> 外部网页 / 内部知识库 / 文件 / 数据库 / 报告存储
```

| 层级     | 组件                              | 职责                                                       |
| -------- | --------------------------------- | ---------------------------------------------------------- |
| 交互层   | CLI、Gateway、Dashboard、产品 API | 接收研究需求、展示确认节点、查询报告和任务状态             |
| 协作层   | Hermes Kanban                     | 管理长任务、依赖关系、章节并行、失败重试和审计日志         |
| Agent 层 | Hermes Profiles                   | 承担研究编排、检索、来源审查、章节写作、综合和渲染职责     |
| 能力层   | Skills                            | 固化研究方法、输出契约、引用规范、章节写作规范和报告规范   |
| 工具层   | MCP Server                        | 暴露搜索、读取、检索、项目读写、章节保存和报告渲染工具     |
| 存储层   | 数据库和对象存储                  | 保存研究项目、来源、章节、结构化结果、报告版本和 HTML 文件 |

## 17.5 Profile 规划
| Profile                 | 职责                                                           | 主要 Skill                                         |
| ----------------------- | -------------------------------------------------------------- | -------------------------------------------------- |
| `research-orchestrator` | 理解需求、确认约束、生成任务书和大纲、拆分任务、汇总状态       | `deepresearch-orchestrator`、`kanban-orchestrator` |
| `search-worker`         | 执行公开搜索、指定站点搜索、网页读取、文件检索和内部知识库检索 | `deepresearch-search`、`kanban-worker`             |
| `source-reviewer`       | 来源去重、可信度评估、冲突识别、证据链整理和风险记录           | `deepresearch-source-review`、`kanban-worker`      |
| `section-writer`        | 章节正文、关键发现、表格、图表、证据链和章节风险写作           | `deepresearch-section`、`kanban-worker`            |
| `synthesis-writer`      | 汇总执行摘要、核心结论、跨章节洞察、建议和全局风险             | `deepresearch-synthesis`、`kanban-worker`          |
| `report-renderer`       | 通过确定性渲染生成 HTML、PDF、Markdown、PPT 或前端组件         | `deepresearch-report`、`kanban-worker`             |

## 17.6 Skill 规划
| Skill                        | 输入                                       | 输出                                                              |
| ---------------------------- | ------------------------------------------ | ----------------------------------------------------------------- |
| `deepresearch-orchestrator`  | 研究需求、用户约束、用户反馈、任务状态     | `ResearchBrief`、`ResearchPlan`、`ResearchOutline`、Kanban 任务图 |
| `deepresearch-search`        | 检索问题、来源偏好、约束、已有来源         | 原始搜索结果、网页摘要、知识库片段、候选来源                      |
| `deepresearch-source-review` | 候选来源、原文摘要、知识库片段、检索问题   | `Source`、`EvidenceChain`、`FactCard`、风险说明                   |
| `deepresearch-section`       | 大纲节点、证据链、事实卡片、来源、章节要求 | `ResearchSection`                                                 |
| `deepresearch-synthesis`     | 所有章节、事实卡片、洞察卡片、风险说明     | `ResearchSynthesis`                                               |
| `deepresearch-report`        | `ResearchResult`、展示要求、输出格式       | `DocumentIR`、`ReportVersion`                                     |

## 17.7 MCP 工具
| 工具                    | 输入                                 | 输出                               |
| ----------------------- | ------------------------------------ | ---------------------------------- |
| `search_web`            | 查询词、站点过滤、时间过滤、结果数量 | 公开搜索结果                       |
| `read_web_page`         | URL、最大字符数                      | 标题、发布时间、正文摘要、最终 URL |
| `search_internal_kb`    | 查询词、数据集、文档范围、召回参数   | 内部知识库片段                     |
| `read_uploaded_file`    | 文件编号、页码或范围                 | 文件正文、表格、元数据             |
| `query_database`        | 数据源、查询参数                     | 结构化数据                         |
| `save_research_brief`   | 项目编号、任务书                     | 保存结果                           |
| `save_research_outline` | 项目编号、大纲                       | 保存结果                           |
| `save_research_section` | 项目编号、章节结果                   | 保存结果和校验错误                 |
| `save_research_result`  | 项目编号、结构化研究结果             | 保存结果                           |
| `render_report`         | `DocumentIR`、输出格式               | 报告文件                           |
| `save_report_version`   | 项目编号、报告元数据、报告文件       | 报告版本                           |

## 17.8 Kanban 任务图
```text
root: research_request
  |
  v
human: confirm_constraints
  |
  v
task: generate_research_brief
  |
  v
human: confirm_research_brief
  |
  v
task: generate_research_plan
  |
  v
human: confirm_outline
  |
  v
task: decompose_research_tasks
  |
  +--> task: search_section_1
  +--> task: search_section_2
  +--> task: search_section_3
  |
  +--> task: review_sources_1
  +--> task: review_sources_2
  +--> task: review_sources_3
  |
  +--> task: write_section_1
  +--> task: write_section_2
  +--> task: write_section_3
  |
  v
task: synthesize_research_result
  |
  v
task: render_report
```

章节任务使用同一个 `project_id` 和不同的 `section_id`。章节写作任务必须保存 `ResearchSection` 后才能完成。报告渲染任务只读取 `ResearchResult`，不新增事实、来源或结论。

## 17.9 数据对象
| 对象                | 作用                                                     |
| ------------------- | -------------------------------------------------------- |
| `ResearchRequest`   | 用户原始研究需求和补充约束                               |
| `ResearchBrief`     | 固化研究目标、范围、排除项、关键问题、默认假设和交付标准 |
| `ResearchPlan`      | 记录研究方法、检索策略、来源偏好、章节任务和验收规则     |
| `ResearchOutline`   | 报告结构、章节问题、证据需求和章节输出要求               |
| `SearchTask`        | 可执行检索任务，包含查询词、来源范围、检索目标和预期证据 |
| `Source`            | 可引用来源，包含标题、URL、发布时间、来源类型和摘要      |
| `EvidenceChain`     | 关键判断、事实编号、来源编号和置信度                     |
| `FactCard`          | 可复核事实、来源编号、置信度和适用范围                   |
| `InsightCard`       | 基于事实形成的判断、支撑事实和适用边界                   |
| `ResearchSection`   | 单章正文、关键发现、证据链、来源、表格、图表和风险说明   |
| `ResearchSynthesis` | 执行摘要、核心结论、跨章节洞察、建议和全局风险           |
| `ResearchResult`    | 报告渲染前的完整结构化研究结果                           |
| `DocumentIR`        | 报告展示中间表示                                         |
| `ReportVersion`     | 最终报告版本、格式、来源列表和存储地址                   |

## 17.10 证据契约
章节中的关键判断必须满足以下约束：

- 每条关键判断必须写入 `EvidenceChain`。
- `EvidenceChain.source_ids` 必须能对应到 `Source.source_id`。
- 公开网页来源必须包含 HTTP URL。
- 内部知识库来源必须标记 `source_type=internal_knowledge_base`。
- 事实卡片只能保存可复核事实，不保存大段原文。
- 口径差异、来源不足、时效性不足和样本偏差必须写入风险说明。
- 报告渲染阶段不得新增事实、来源、判断或证据链。

## 17.11 报告渲染
报告渲染使用确定性流程：

```text
ResearchResult
  -> DocumentIR
  -> HTML / PDF / Markdown / PPT / 前端组件
```

`ResearchResult` 保存研究内容，`DocumentIR` 保存展示结构。`report-renderer` 只负责目录、引用、表格、图表、参考来源和版式，不负责新增研究结论。

## 17.12 用户控制点
| 控制点     | 用户操作                                       |
| ---------- | ---------------------------------------------- |
| 约束确认   | 补充约束，或明确不限定                         |
| 任务书确认 | 修改研究目标、范围、排除项、关键问题和交付标准 |
| 大纲确认   | 修改章节结构、章节问题和证据需求               |
| 来源补充   | 添加指定网站、文件、内部文档或必须排除的来源   |
| 章节重跑   | 只重跑指定章节的检索、来源审查或写作           |
| 报告重渲染 | 基于已有 `ResearchResult` 重新生成不同格式报告 |

## 17.13 参考能力来源
- OpenAI Deep Research：https://openai.com/index/introducing-deep-research/
- OpenAI Deep Research Help：https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt
- Gemini Deep Research Agent：https://ai.google.dev/gemini-api/docs/interactions/deep-research
- Perplexity Sonar Deep Research：https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research
