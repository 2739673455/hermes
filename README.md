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
hermes --continue, -c                        # 继续上次会话
hermes --resume, -r                          # 按会话 ID 或标题恢复对话
hermes sessions rename <session-id> <title>  # 重命名会话
hermes sessions delete <session_id>          # 删除会话
hermes sessions prune --older-than 30        # 清理 30 天前的旧会话
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
| `/steer <prompt>`       | 在下一次工具调用之后向 agent 注入一条中途说明，可用于在任务进行中调整方向                            |
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

使用 `scripts/hooks/conversation-end-popup.py` 和 `scripts/hooks/mac-toast.swift`。Windows / WSL 使用 PowerShell 弹窗，macOS 使用同目录的 `mac-toast` helper。

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
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins

Hermes 拥有一个插件系统，无需修改核心代码即可添加自定义工具、钩子和集成。

## 9.1 插件能做什么
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins#what-plugins-can-do

插件通过 `register(ctx)` 函数接入 Hermes，`ctx` 上所有公开 API 均可使用。以下是完整扩展点：

| 扩展类型     | 说明                                                       |
| ------------ | ---------------------------------------------------------- |
| 工具         | 给模型增加可调用能力，例如外部 API、本地服务或自定义逻辑   |
| 钩子         | 在工具调用、LLM 调用、会话开始 / 结束等生命周期点执行代码  |
| 命令         | 增加 `/name` 斜杠命令，或增加 `hermes <plugin> ...` 子命令 |
| 会话注入     | 把外部事件、消息或数据注入当前会话                         |
| Skill / 数据 | 随插件附带 Skill、模板、配置、静态数据等资源               |
| Gateway 平台 | 接入新的消息平台或自定义平台适配器                         |
| 后端提供商   | 接入新的记忆、上下文压缩、图像生成、视频生成或 LLM 提供商  |

## 9.2 插件目录
用户插件目录是 `~/.hermes/plugins/`，每个插件一个独立子目录。最小可用插件只需要两个文件：

```text
~/.hermes/plugins/hello-world/
├── plugin.yaml      # 插件清单：名称、版本、描述等元信息
└── __init__.py      # 定义 register(ctx)，在这里注册工具 / hook / 命令
```

其中真正的接入点是 `__init__.py` 里的 `register(ctx)`。Hermes 加载插件后会调用这个函数；插件也是在这里通过 `ctx.register_tool(...)`、`ctx.register_hook(...)`、`ctx.register_command(...)` 等 API 把自己的能力注册进 Hermes。

`plugin.yaml` 主要负责插件发现和元信息，例如名称、版本、描述、依赖环境变量等。也就是说：`plugin.yaml` 让 Hermes 知道“这里有一个插件”，`register(ctx)` 决定“这个插件实际提供什么能力”。

## 9.3 插件示例
注册一个 `shake_window` 工具。这个工具适合 WSL / Git Bash / Windows 终端环境：模型调用工具后，插件通过 `powershell.exe` 调用 Windows API，让当前前台窗口轻微左右晃动。

创建目录：

```bash
mkdir -p ~/.hermes/plugins/shake-window
```

创建 `~/.hermes/plugins/shake-window/plugin.yaml`：

```yaml
name: shake-window
version: "1.0"
description: Provides a shake_window tool that briefly shakes the current Windows foreground window as a visible desktop attention cue.
```

创建 `~/.hermes/plugins/shake-window/__init__.py`：

```python
import json
import shutil
import subprocess


POWERSHELL_SHAKE = r"""
Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}

[StructLayout(LayoutKind.Sequential)]
public struct RECT {
    public int Left;
    public int Top;
    public int Right;
    public int Bottom;
}
"@

$hwnd = [Win32]::GetForegroundWindow()
if ($hwnd -eq [IntPtr]::Zero) {
    Write-Error "No foreground window found."
    exit 1
}

$rect = New-Object RECT
if (-not [Win32]::GetWindowRect($hwnd, [ref]$rect)) {
    Write-Error "GetWindowRect failed."
    exit 1
}

$x = $rect.Left
$y = $rect.Top
$w = $rect.Right - $rect.Left
$h = $rect.Bottom - $rect.Top

# 最大化窗口通常无法直接移动，先恢复成普通窗口。
[void][Win32]::ShowWindow($hwnd, 9)
Start-Sleep -Milliseconds 100

for ($i = 0; $i -lt 8; $i++) {
    [void][Win32]::MoveWindow($hwnd, $x - 12, $y, $w, $h, $true)
    Start-Sleep -Milliseconds 45
    [void][Win32]::MoveWindow($hwnd, $x + 12, $y, $w, $h, $true)
    Start-Sleep -Milliseconds 45
}

[void][Win32]::MoveWindow($hwnd, $x, $y, $w, $h, $true)
"""


def register(ctx):
    schema = {
        "name": "shake_window",
        "description": "Shake the current Windows foreground window.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    }

    def handle_shake(params, **kwargs):
        del params, kwargs

        powershell = shutil.which("powershell.exe")
        if powershell is None:
            return json.dumps({
                "ok": False,
                "error": "powershell.exe not found",
            })

        result = subprocess.run(
            [powershell, "-NoProfile", "-Command", POWERSHELL_SHAKE],
            text=True,
            capture_output=True,
            check=False,
        )

        return json.dumps({
            "ok": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        })

    ctx.register_tool(
        name="shake_window",
        toolset="desktop_fun",
        schema=schema,
        handler=handle_shake,
        description="Shake the current Windows foreground window.",
    )
```

启用插件：

```bash
hermes plugins enable shake-window
```

重新启动 Hermes 后，模型就能调用 `shake_window` 工具。

## 9.4 插件发现
Hermes 会从多个来源发现插件：

| 来源    | 路径 / 方式                         | 用途                                                                               |
| ------- | ----------------------------------- | ---------------------------------------------------------------------------------- |
| Bundled | Hermes 仓库内置 `plugins/`          | 官方随 Hermes 发布的插件                                                           |
| User    | `~/.hermes/plugins/`                | 用户自己的本地插件                                                                 |
| Project | `.hermes/plugins/`                  | 当前工作目录插件；默认不扫描，需设置 `HERMES_ENABLE_PROJECT_PLUGINS=true` 显式信任 |
| pip     | `hermes_agent.plugins` entry points | 通过 Python 包分发的插件                                                           |

## 9.5 管理插件
常用命令：

```bash
hermes plugins                    # 交互式开关插件
hermes plugins list               # 查看已安装插件
hermes plugins install user/repo  # 从 GitHub 安装插件
hermes plugins update <name>      # 更新插件
hermes plugins remove <name>      # 移除插件
hermes plugins enable <name>      # 启用插件
hermes plugins disable <name>     # 禁用插件
```

新安装或捆绑的插件默认情况下不启用，必须加入 `~/.hermes/config.yaml` 的 `plugins.enabled` 后才会加载工具、hooks 或命令。

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - my-plugin
  disabled:
    - noisy-plugin
```

`plugins.disabled` 是拒绝列表，如果同一个插件同时出现在 `enabled` 和 `disabled`，禁用优先。

# 10. 持久记忆
https://hermes-agent.nousresearch.com/docs/user-guide/features/memory

Hermes 有一套有容量上限、由 Agent 自己维护的持久记忆系统。它会跨会话保存用户偏好、项目环境、工具习惯和经验教训，并在新会话开始时注入系统提示词。

## 10.1 工作原理
内置记忆由两个文件组成，默认存储在 `~/.hermes/memories/`：

| 文件        | 用途                                                     | 字符上限                    |
| ----------- | -------------------------------------------------------- | --------------------------- |
| `MEMORY.md` | Agent 的个人笔记：环境事实、项目约定、工具细节、经验教训 | 2,200 字符（约 800 tokens） |
| `USER.md`   | 用户画像：用户信息、沟通风格、期望和习惯                 | 1,375 字符（约 500 tokens） |

- 这两个文件会在会话开始时注入系统提示词
- 会话中通过 `memory` 工具新增、替换或删除的记忆会立即写入磁盘，但不会立刻改变当前会话已经注入的提示词快照
- 新的记忆会在下一个会话生效。这样可以保持 LLM prefix cache 稳定

记忆相关配置示例：

```yaml
# ~/.hermes/config.yaml
memory:
  memory_enabled: true        # 启用持久记忆
  user_profile_enabled: true  # 启用用户档案
  memory_char_limit: 2200     # 记忆字符上限（约 800 tokens）
  user_char_limit: 1375       # 用户档案字符上限（约 500 tokens）
```

系统提示词中的记忆大致长这样：

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

`§`（节号符号，section sign）用来分隔不同记忆条目，标题会显示当前容量占用，提醒 Agent 在接近上限时做合并或替换。

## 10.2 memory 工具
Agent 通过 `memory` 工具管理记忆，常用动作：

| 动作      | 用途                                           |
| --------- | ---------------------------------------------- |
| `add`     | 添加新的记忆条目                               |
| `replace` | 替换已有条目，使用 `old_text` 做短唯一子串匹配 |
| `remove`  | 删除已有条目，使用 `old_text` 做短唯一子串匹配 |

没有 `read` 动作。记忆内容会自动注入系统提示词，Agent 在会话里本来就能看到当前快照。

`replace` 和 `remove` 不需要传完整条目，只要传能唯一定位的短文本：

```text
memory(action="replace", target="memory",
       old_text="dark mode",
       content="User prefers light mode in VS Code, dark mode in terminal")
```

使用 `old_text` 匹配时，会先去掉 `old_text` 首尾空白，并在每条记忆中进行精确子串匹配。必须刚好匹配 1 条记忆；匹配 0 条会报错，匹配多条也会报错并要求提供更具体的片段

## 10.3 记忆管理
记忆管理指令：

**提示词：`MEMORY_GUIDANCE`**

- **位置**：`agent/prompt_builder.py`
- **作用**：指导 Agent 何时写入 memory、何时不要写入 memory、何时改用 Skill
- **注入位置**：`memory` 工具可用时，随主对话系统提示词注入

中文大意：用 `memory` 保存跨会话仍然重要的长期事实，例如用户偏好、环境细节、工具使用注意事项和稳定约定。优先保存能减少用户未来重复纠正或提醒的内容。不要保存任务进度、会话结果、完成记录、临时 TODO、PR / issue / commit 编号，或任何一周内会过期的内容；这类历史细节应该用 `session_search` 找回。如果沉淀的是一种可复用做法或流程，应该保存成 Skill。记忆要写成陈述性事实，不要写成命令式指令。

关键原文片段：

```text
You have persistent memory across sessions. Save durable facts using the memory
tool: user preferences, environment details, tool quirks, and stable conventions.
Memory is injected into every turn, so keep it compact and focused on facts that
will still matter later.

Prioritize what reduces future user steering — the most valuable memory is one
that prevents the user from having to correct or remind you again.

Do NOT save task progress, session outcomes, completed-work logs, or temporary TODO
state to memory; use session_search to recall those from past transcripts.

If you've discovered a new way to do something, solved a problem that could be
necessary later, save it as a skill with the skill tool.

Write memories as declarative facts, not instructions to yourself.
'User prefers concise responses' ✓ — 'Always respond concisely' ✗.
```

记忆中适合保存：

- 用户偏好：例如「用户偏好 TypeScript 而不是 JavaScript」
- 环境事实：例如「这台服务器运行 Debian 12 和 PostgreSQL 16」
- 用户纠正：例如「Docker 命令不要用 sudo，用户已在 docker 组」
- 项目约定：例如「项目使用 tabs、120 字符行宽、Google 风格 docstring」
- 显式要求：例如「记住 API key 每月轮换」

记忆中不适合保存：

- 太模糊的信息：例如「用户问过 Python」
- 容易重新查询的通用知识
- 大段代码、日志、数据表
- 临时任务状态、一次性文件路径、短期 TODO
- 已经写在 `SOUL.md`、`AGENTS.md` 等上下文文件里的内容

容量管理：记忆有严格字符上限，避免系统提示词无限膨胀。当新增内容会超过上限时，`memory` 工具会返回错误，并附带当前条目和容量信息。此时 Agent 应该先合并、替换或删除旧条目，再添加新内容。

预防重复数据：记忆系统会拒绝完全重复的条目。如果添加的内容已经存在，会返回成功但提示没有新增重复内容。

安全扫描：记忆条目在写入前还会做安全扫描，包含提示词注入、凭证外泄、SSH 后门、不可见 Unicode 字符等风险模式的内容会被阻止。

## 10.4 session_search vs memory
除了 `MEMORY.md` 和 `USER.md`，Hermes 还可以通过 `session_search` 搜索过去的完整会话。两者用途不同：

| 对比项     | 持久记忆                     | Session Search             |
| ---------- | ---------------------------- | -------------------------- |
| 容量       | 约 1,300 tokens，总量很小    | 理论上包含所有历史会话     |
| 速度       | 会话开始时直接进入系统提示词 | 需要按需查询数据库         |
| 用途       | 必须一直可见的关键事实       | 查找过去某次讨论的具体内容 |
| 管理方式   | Agent 主动维护、压缩、替换   | 自动保存所有会话           |
| token 成本 | 每个会话固定占用少量上下文   | 返回的消息片段占用上下文   |

memory 保存「以后经常要用的稳定事实」；session_search 用来回答「上次我们讨论过什么」。

## 10.5 外部记忆
https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers

Hermes 还内置了 8 个外部记忆提供商插件，用来提供比 `MEMORY.md` / `USER.md` 更强的跨会话记忆能力，例如语义搜索、知识图谱、自动事实抽取、用户建模等。

外部记忆不会替代内置记忆，而是作为叠加能力并行工作。同一时间只能启用一个外部记忆提供商；内置记忆始终可以继续使用。

相关命令：

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

可选 provider 包括：

| 分档 | Provider      | 重点功能 / 优势                                            |
| ---- | ------------- | ---------------------------------------------------------- |
| 入门 | `honcho`      | 跨会话用户建模、session 级上下文、基于历史上下文的综合判断 |
| 入门 | `mem0`        | 服务端 LLM 事实抽取、语义搜索、重排和自动去重              |
| 进阶 | `openviking`  | 文件系统式知识层级、分层读取、自动抽取 6 类记忆            |
| 进阶 | `byterover`   | CLI 驱动的层级知识树、分层检索、压缩前自动提取洞察         |
| 复杂 | `hindsight`   | 知识图谱、实体关系、多策略检索、跨记忆综合                 |
| 复杂 | `holographic` | FTS5 全文搜索、信任评分、HRR 组合查询、冲突检测            |
| 复杂 | `retaindb`    | Vector + BM25 + Reranking 混合搜索、7 类记忆、增量压缩     |
| 复杂 | `supermemory` | 语义长期记忆、用户画像、会话图谱摄取、上下文防污染         |

选择建议：

- 只是想让记忆更智能，先从 `honcho` 或 `mem0` 开始
- 更偏本地 / 文件系统式知识管理，可以看 `openviking` 或 `byterover`
- 需要知识图谱、实体关系和复杂关联检索，再考虑 `hindsight`
- 需要混合检索、评分、冲突检测等进阶能力，再看 `holographic`、`retaindb` 或 `supermemory`

# 11. 上下文文件
https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files

Hermes Agent 会自动发现并加载上下文文件。这里的“上下文文件”分两类：项目上下文文件用于描述当前仓库或目录规则；`SOUL.md` 用于描述当前 Hermes 实例的人格和沟通风格。

## 11.1 支持的上下文文件
| 文件                       | 用途                                   | 发现方式                        |
| -------------------------- | -------------------------------------- | ------------------------------- |
| `.hermes.md` / `HERMES.md` | Hermes 专用项目说明，优先级最高        | 从当前目录向上查找到 git root   |
| `AGENTS.md`                | 项目说明、架构、约定、注意事项         | 启动目录；子目录中可渐进发现    |
| `CLAUDE.md`                | 兼容 Claude Code 的上下文文件          | 启动目录；子目录中可渐进发现    |
| `.cursorrules`             | 兼容 Cursor 的项目规则                 | 启动目录；子目录中可渐进发现    |
| `.cursor/rules/*.mdc`      | Cursor 规则模块                        | 启动目录                        |
| `SOUL.md`                  | 当前 Hermes 实例的人格、语气和沟通风格 | 只从 `HERMES_HOME/SOUL.md` 加载 |

## 11.2 加载流程与安全处理
项目上下文有两条加载路径：启动加载和渐进加载。启动加载决定会话一开始注入哪份项目说明；渐进加载会在 Agent 访问子目录时补充局部规则。

### 11.2.1 启动加载
启动加载发生在会话开始时。流程如下：

1. 扫描当前工作目录，按优先级查找项目上下文文件
2. 以 UTF-8 文本格式读取
3. 执行安全扫描
4. 超过 20,000 字符时截断，保留头部和尾部
5. 组合到 `# Project Context` 部分并注入系统提示词

启动时的项目上下文只加载一种类型，优先级是：`.hermes.md` / `HERMES.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` / `.cursor/rules/*.mdc`。`SOUL.md` 独立加载，不参与这个优先级竞争。

`.hermes.md` / `HERMES.md` 是 Hermes 专用的项目级说明，只在启动时从当前目录向上查找到 git root。它不参与子目录渐进发现；子目录级规则应写在 `AGENTS.md`、`CLAUDE.md` 或 `.cursorrules` 中。

### 11.2.2 启动加载的截断策略
启动加载的默认截断上限是 20,000 字符。超过上限后，Hermes 保留前 70% 和后 20%，中间插入截断标记。例如：

```text
[...truncated AGENTS.md: kept 14000+4000 of 35620 chars. Use file tools to read the full file.]
```

也就是说，重要规则最好放在文件开头或结尾；如果关键规则只放在超长文件中间，可能只留下截断标记，需要 Agent 之后用文件工具读取全文。

### 11.2.3 渐进加载
渐进加载发生在会话进行中。流程如下：

1. Agent 调用工具时，如果参数里出现文件路径，Hermes 会从这些路径推断当前正在访问的目录
2. 典型触发场景包括读取 `src/api/server.py`、搜索 `packages/web/`、在 `services/payments` 下运行命令等
3. 从该路径所在目录向上检查最多 5 层父目录，遇到已访问过的目录则停止继续向上
4. 每个未访问过的目录都会检查一次；同一目录内按 `AGENTS.md` → `CLAUDE.md` → `.cursorrules` 优先级只加载首个匹配项
5. 执行安全扫描
6. 单个渐进提示文件超过 8,000 字符时，只保留前 8,000 字符并追加截断标记
7. 内容追加到工具结果中，模型在上下文中自然看到，不修改系统提示词

因此，一个会话启动时可能只注入了 `.hermes.md`，但后续访问 `src/payments/` 时仍然可能看到 `src/payments/AGENTS.md` 的渐进提示。这个内容不会重新写入系统提示词，只是跟随那次工具结果进入上下文。

安全扫描会检查以下内容：

1. **指令覆盖** — 例如 `ignore previous instructions`、`disregard your rules`
2. **欺骗行为** — 例如 `do not tell the user`
3. **系统提示词覆盖** — 例如 `system prompt override`
4. **隐藏 HTML 注释** — 例如 `<!-- ignore instructions -->`
5. **隐藏 div 元素** — 例如 `<div style="display:none">`
6. **凭证外泄** — 例如 `curl ... $API_KEY`
7. **敏感文件读取** — 例如 `cat .env`、`cat credentials`
8. **不可见字符** — 零宽空格、双向文本覆盖符、词连接符等

安全扫描代码实现位于 `agent/prompt_builder.py`，核心逻辑分为两步：

1. **不可见 Unicode 检测** — 遍历危险字符集合，检查内容是否包含零宽空格、BOM、双向文本覆盖符等字符
2. **正则模式匹配** — 用 `re.IGNORECASE` 逐条匹配威胁模式，每条模式对应一个威胁标签

核心实现摘录：

```python
_CONTEXT_THREAT_PATTERNS = [
    (r'ignore\s+(previous|all|above|prior)\s+instructions', "prompt_injection"),
    (r'do\s+not\s+tell\s+the\s+user', "deception_hide"),
    (r'system\s+prompt\s+override', "sys_prompt_override"),
    (r'disregard\s+(your|all|any)\s+(instructions|rules|guidelines)', "disregard_rules"),
    (r'act\s+as\s+(if|though)\s+you\s+(have\s+no|don\'t\s+have)\s+(restrictions|limits|rules)', "bypass_restrictions"),
    (r'<!--[^>]*(?:ignore|override|system|secret|hidden)[^>]*-->', "html_comment_injection"),
    (r'<\s*div\s+style\s*=\s*["\'][\s\S]*?display\s*:\s*none', "hidden_div"),
    (r'translate\s+.*\s+into\s+.*\s+and\s+(execute|run|eval)', "translate_execute"),
    (r'curl\s+[^\n]*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|API)', "exfil_curl"),
    (r'cat\s+[^\n]*(\.env|credentials|\.netrc|\.pgpass)', "read_secrets"),
]

_CONTEXT_INVISIBLE_CHARS = {
    '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff',
    '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',
}

def _scan_context_content(content: str, filename: str) -> str:
    findings = []

    for char in _CONTEXT_INVISIBLE_CHARS:
        if char in content:
            findings.append(f"invisible unicode U+{ord(char):04X}")

    for pattern, pid in _CONTEXT_THREAT_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append(pid)

    if findings:
        logger.warning("Context file %s blocked: %s", filename, ", ".join(findings))
        return f"[BLOCKED: {filename} contained potential prompt injection ({', '.join(findings)}). Content not loaded.]"

    return content
```

命中任意威胁模式后，文件将被阻止加载，上下文位置替换为：

```text
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

## 11.3 `SOUL.md` 与 `/personality`
https://hermes-agent.nousresearch.com/docs/user-guide/features/personality

Hermes 的个性主要由 `SOUL.md` 控制。它是 Agent 的主身份文件，会拼入系统提示词开头部分，用来定义 Hermes 是谁、怎么说话、默认沟通风格是什么。默认位置在 `~/.hermes/SOUL.md`。

`SOUL.md` 文件为空或读取失败时，回退到内置默认身份。如果文件有内容，经过安全扫描和截断后原样注入系统提示词。它使用和启动项目上下文相同的截断上限：默认 20,000 字符，保留前 70% 和后 20%。

`SOUL.md` 适合写长期稳定的个性和沟通偏好：

- 语气
- 风格
- 直接程度
- 默认互动方式
- 不希望出现的表达习惯
- 面对不确定性、分歧、模糊需求时的处理方式

不适合写项目规则、文件路径、仓库约定、临时流程。这些应该放进 `AGENTS.md`。

`/personality` 是一层额外的系统提示覆盖。它不会修改 `SOUL.md`，而是在当前基础系统提示之后追加一段 personality prompt；因为位置更靠后，它通常会覆盖语气和表达风格，但不会删除 `SOUL.md`、项目上下文、记忆和工具说明。

内置人格可通过 `/personality` 切换。官方内置人格如下：

| 人格          | 说明                                     |
| ------------- | ---------------------------------------- |
| `helpful`     | 友好、通用的基础助手                     |
| `concise`     | 简短直接，回答尽量切中要点               |
| `technical`   | 详细、准确的技术专家模式                 |
| `creative`    | 创新发散，偏向非常规方案和新思路         |
| `teacher`     | 耐心教学，用清晰解释和示例辅助理解       |
| `kawaii`      | 可爱、闪亮、热情的表达风格               |
| `catgirl`     | Neko-chan 猫娘风格，带猫系口癖和可爱表达 |
| `pirate`      | Captain Hermes，懂技术的数字海盗船长风格 |
| `shakespeare` | 莎士比亚式文风，戏剧化、华丽而夸张       |
| `surfer`      | 轻松随性的冲浪者语气，chill bro vibes    |
| `noir`        | 硬汉侦探小说式叙述，偏黑色电影氛围       |
| `uwu`         | 极致可爱和 uwu-speak，可爱口癖更重       |
| `philosopher` | 哲学家模式，会追问问题背后的意义和原因   |
| `hype`        | MAXIMUM ENERGY，极高能量和强烈鼓舞式回应 |

# 12. Gateway
https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

Gateway 是 Hermes 的消息平台接入层，可以作为前台进程或后台服务运行。它负责连接 Telegram、Discord、Slack、微信等平台，接收消息，维护每个聊天对应的会话，把消息转发给 Hermes Agent 处理，再把回复发回原平台。

Gateway 和 CLI 模式使用同一套 Hermes 程序、配置、会话、记忆、技能和工具。区别在于：CLI 是终端里的单次交互入口，Gateway 是长期运行的消息平台适配进程。Gateway 还会运行 cron 调度循环，用来触发到期的计划任务。

## 12.1 命令
```bash
hermes gateway setup                 # 交互式配置消息平台
hermes gateway                       # 前台启动 Gateway
hermes gateway install               # 安装为用户服务（Linux）/ launchd 服务（macOS）
sudo hermes gateway install --system # 仅 Linux：安装为开机启动的系统服务
hermes gateway start                 # 启动默认服务
hermes gateway stop                  # 停止默认服务
hermes gateway status                # 查看默认服务状态
hermes gateway status --system       # 仅 Linux：检查系统服务状态
```

## 12.2 网关配对
默认情况下，网关会拒绝所有不在允许列表中或未通过私信配对的用户。

### 12.2.1 允许列表
在 `~/.hermes/.env` 中配置允许列表，显式写入可信用户 ID：

```bash
# 按平台限制用户
TELEGRAM_ALLOWED_USERS=123456789,987654321
WEIXIN_ALLOWED_USERS=123456789,987654321

# 或配置通用允许列表
GATEWAY_ALLOWED_USERS=123456789,987654321

# 显式允许所有用户，但不推荐给有终端访问权限的机器人使用
GATEWAY_ALLOW_ALL_USERS=true
```

### 12.2.2 私信配对
无需手动配置用户 ID，未知用户在私信机器人时会收到一次性配对码，例如： `Pairing code: XKGH5N7P`。之后管理员在本机批准：

```bash
hermes pairing approve telegram XKGH5N7P  # 批准配对
hermes pairing list                       # 查看配对列表
hermes pairing revoke telegram <user_id>  # 撤销配对
```

配对码 1 小时后过期，有速率限制，并使用加密随机数生成。

### 12.2.3 斜杠命令权限控制
用户通过允许列表或配对后，可以分成管理员和普通用户。这个权限分层目前只控制斜杠命令，不影响普通聊天；普通用户仍然可以和 Agent 对话。

权限规则：

1. 先判断用户是否被允许使用 Gateway：来自允许列表、平台允许列表、群组允许列表或配对记录。
2. 再判断当前作用域是否启用了命令权限分层。私聊作用域看 `allow_admin_from`，群组 / 频道作用域看 `group_allow_admin_from`。
3. 如果当前作用域没有配置对应的 admin 列表，保持向后兼容：该作用域不区分管理员和普通用户，所有已允许用户都可以运行斜杠命令。
4. 如果当前作用域配置了 admin 列表，列表内用户是管理员，可以运行所有内置和插件注册的斜杠命令。
5. 不在 admin 列表里的已允许用户是普通用户，只能运行显式允许的命令，以及始终允许的 `/help` 和 `/whoami`。
6. 私聊和群组 / 频道是两个独立作用域；只配置 `group_allow_admin_from` 不会影响私聊，私聊仍按自己的配置判断。

示例配置：

```yaml
# ~/.hermes/config.yaml
gateway:
  platforms:
    discord:
      extra:
        allow_from: ["111", "222", "333"]       # 允许私聊使用的用户
        allow_admin_from: ["111"]               # 私聊管理员：可运行所有斜杠命令
        user_allowed_commands: [status, model]  # 私聊普通用户可运行的命令
        group_allow_admin_from: ["111"]         # 群组 / 频道管理员
        group_user_allowed_commands: [status]   # 群组 / 频道普通用户可运行的命令
```

可以用 `/whoami` 查看当前平台、作用域、自己的权限层级，以及当前可运行的斜杠命令。

# 13. Profile
https://hermes-agent.nousresearch.com/docs/user-guide/profiles

通过 Profile 运行多个独立的 Hermes Agent，每个 Agent 有独立的配置、会话、技能和记忆。

## 13.1 什么是 Profile
Profile 是一个独立的 Hermes home 目录。其中包含各自的 `config.yaml`、`.env`、`SOUL.md`、记忆、会话、技能、cron 任务、状态数据库和 Gateway 状态。

通过 Profile 可以运行用于不同用途的 Agent 而不会混淆 Hermes 状态。

创建 Profile 后，Hermes 会自动生成同名命令别名。例如创建 `coder` 后，可以直接使用 `coder chat`、`coder setup`、`coder gateway start`，本质上等价于 `hermes -p coder ...`。

## 13.2 创建 Profile
```bash
hermes profile create coder                     # 创建空白 Profile，会生成同名命令别名，内置技能会初始化
hermes profile create coder --description "负责阅读源码、实现已明确的代码修改、修复测试或构建问题、运行必要验证，并在完成后汇报改动、测试结果和剩余风险"                             # 创建带描述的 Profile
hermes profile create coder --clone             # 克隆当前 Profile 的 config.yaml、.env、SOUL.md，不复制会话和记忆
hermes profile create backup --clone-all        # 克隆完整状态：配置、API key、人格、记忆、会话、技能、cron、plugins
hermes profile create coder --clone --clone-from backup  # 从指定 Profile 克隆
hermes profile describe coder --text "..."      # 为 Profile 添加描述
hermes profile describe coder --auto            # 用辅助模型自动生成 Profile 描述
hermes profile delete coder                     # 删除 Profile
```

## 13.3 使用 Profile
每个 Profile 都会自动生成同名命令别名，位置通常是 `~/.local/bin/<profile-name>`。

例如创建 `coder` 后：

```bash
coder chat                                      # 启动 coder profile 的交互式对话
coder setup                                     # 运行 coder profile 的初始化 / 配置向导
coder gateway start                             # 启动 coder profile 的 Gateway 服务
coder doctor                                    # 检查 coder profile 的健康状态
coder skills list                               # 查看 coder profile 已安装的 skills
coder config set model.default anthropic/claude-sonnet-4  # 修改 coder profile 的默认模型
```

这个别名本质上等价于 `hermes -p <name>`。也可以显式指定 Profile：`hermes -p coder chat`。

如果希望普通 `hermes` 命令默认指向某个 Profile：

```bash
hermes profile use coder    # 默认使用 coder Profile
hermes                      # 现在默认使用 coder
hermes profile use default  # 恢复默认 Profile 为 default
```

每个 Profile 都可以作为独立进程运行自己的 Gateway，并拥有自己的 bot token。

## 13.4 工作原理
Profile 使用 `HERMES_HOME` 环境变量。运行 `coder chat` 时，包装脚本会在启动 Hermes 前设置 `HERMES_HOME=~/.hermes/profiles/coder`。代码中通过 `get_hermes_home()` 解析路径，把 Hermes 状态限定在对应 Profile 目录下，包括配置、会话、记忆、技能、状态数据库、Gateway PID、日志和定时任务。

# 14. Cron
https://hermes-agent.nousresearch.com/docs/user-guide/features/cron

Hermes 内置定时任务系统，可以用自然语言、cron 表达式安排任务。

定时任务通过 Gateway daemon 执行：Gateway 每 60 秒 tick 一次，检查到期任务。为每个到期任务启动一个新的 Agent 会话执行 prompt，然后投递最终结果。

Cron 运行时会禁用 cron 管理工具，避免递归创建更多定时任务造成调度循环。

## 14.1 创建任务
可在会话中通过 `/cron`，或使用 CLI 命令 `hermes cron` 来创建定时任务。

```bash
/cron add 30m "提醒我检查构建结果"
/cron add "every 2h" "检查服务器状态"
/cron add "every 1h" "总结新动态" --skill blogwatcher
/cron add "every 1h" "加载两个技能并合并结果" --skill blogwatcher --skill maps

hermes cron create "every 2h" "检查服务器状态"
hermes cron create "every 1h" "总结新动态" --skill blogwatcher
hermes cron create "every 1h" "加载两个技能并合并结果" \
  --skill blogwatcher \
  --skill maps \
  --name "Skill combo"
```

也可以直接用自然语言让 Hermes 创建，例如：

```text
每天早上 9 点检查 Hacker News 上的 AI 新闻，然后发一份摘要到 Telegram。
```

Hermes 会在内部调用 `cronjob` 工具完成创建：

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
    profile=None,
    enabled_toolsets=["web"],
)
```

默认情况下，定时任务会从网关启动时的工作目录运行，可通过传递 `--workdir` 来更改工作目录。设置了 `workdir` 时，该目录内的上下文文件会被注入系统提示词：

```bash
hermes cron create "every 1d at 09:00" "审查打开的 PR，总结 CI 健康状况，并发布到 #eng 频道" \
  --workdir /home/me/projects/acme
```

## 14.2 调度格式
常用格式：

| 类型        | 示例                                      | 行为                 |
| ----------- | ----------------------------------------- | -------------------- |
| 相对延迟    | `30m`、`2h`、`1d`                         | 一次性运行           |
| 循环间隔    | `every 30m`、`every 2h`、`every 1d`       | 持续重复运行         |
| Cron 表达式 | `0 9 * * *`、`0 9 * * 1-5`、`0 */6 * * *` | 按 cron 规则重复运行 |
| ISO 时间    | `2026-03-15T09:00:00`                     | 指定时间运行一次     |

Cron 表达式格式为 `分 时 日 月 周`，例如：

- `0 9 * * *` 每天 9:00 执行
- `0 9 * * 1-5` 工作日每天 9:00 执行
- `0 */6 * * *` 每 6 小时执行
- `30 8 1 * *` 每月 1 日 8:30 执行

## 14.3 管理任务
可在会话中通过 `/cron`，或使用 CLI 命令 `hermes cron` 来管理定时任务。

```bash
/cron list                                             # 查看定时任务
/cron list --all                                       # 查看所有任务，包括已暂停的任务
/cron edit <job_id> --schedule "every 4h"              # 修改调度时间
/cron edit <job_id> --prompt "使用新的任务说明"          # 修改任务说明
/cron edit <job_id> --skill blogwatcher --skill maps  # 替换当前任务的技能列表
/cron edit <job_id> --add-skill maps                  # 追加技能
/cron edit <job_id> --remove-skill blogwatcher        # 移除指定技能
/cron edit <job_id> --clear-skills                    # 清空所有技能
/cron edit <job_id> --repeat 5                        # 设置重复次数
/cron pause <job_id>                                  # 暂停任务
/cron resume <job_id>                                 # 恢复任务
/cron run <job_id>                                    # 下一个 scheduler tick 触发任务
/cron remove <job_id>                                 # 删除任务

hermes cron status     # 查看调度器状态
hermes cron tick       # 手动触发一次 scheduler tick
```

任务存储在 `~/.hermes/cron/jobs.json`，运行输出会保存到 `~/.hermes/cron/output/{job_id}/{timestamp}.md`。

## 14.4 运行结果投递方式
`deliver` 控制定时任务运行完成后，把 Agent 的最终回复或失败错误通知发送到哪里。无论是否外部投递，运行输出都会保存到 `~/.hermes/cron/output/{job_id}/{timestamp}.md`。

常见投递目标：

| deliver                        | 说明                                           |
| ------------------------------ | ---------------------------------------------- |
| `origin`                       | 回到创建任务的聊天来源，消息平台默认值         |
| `local`                        | 只保存到本地文件，CLI 默认值                   |
| `telegram`、`discord`、`slack` | 投递到对应平台的 home channel                  |
| `telegram:123456`              | 投递到指定 Telegram chat ID                    |
| `discord:#engineering`         | 投递到指定 Discord 频道                        |
| `all`                          | 投递到所有已配置 home channel 的平台           |
| `telegram,discord`             | 投递到多个指定平台                             |
| `origin,all`                   | 投递到来源聊天，并 fan out 到所有 home channel |

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

可以关闭包装：

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

## 14.5 No-agent 模式
对于不需要 LLM 推理的周期性任务（例如经典的监控程序、磁盘/内存警报、心跳检测、CI ping 等），可在创建任务时传递 `no_agent=True` 参数。调度程序会按计划运行脚本并直接输出其标准输出，完全跳过 Agent：

```bash
hermes cron create "every 5m" \
  --no-agent \
  --script memory-watchdog.sh \
  --deliver telegram \
  --name "memory-watchdog"
```
脚本必须放在 `~/.hermes/scripts/` 中。`.sh` / `.bash` 用 `/bin/bash` 执行，其他脚本用当前 Python 解释器执行。

脚本运行默认超时时间是 120 秒，可以通过配置调整：

```yaml
# ~/.hermes/config.yaml
cron:
  script_timeout_seconds: 300
```

## 14.6 使用 context_from 链接作业
Cron 任务彼此之间默认是隔离的：每次运行都是新的 Agent 会话，不会自动知道其他任务上次输出了什么。`context_from` 用来把一个任务的最新输出接到另一个任务的 prompt 前面。

> 注意：`context_from` 只能由 Agent 通过 `cronjob` 工具设置，`hermes cron create` 和 `hermes cron edit` CLI 命令均不支持该参数。创建依赖链时必须让 Agent 来操作。

典型流程：

```text
Job 1：收集原始数据
Job 2：读取 Job 1 的最新输出，筛选 / 排序
Job 3：读取 Job 2 的最新输出，生成最终报告并投递
```

示例：

```text
# Job 1：收集 AI 新闻
cronjob(action="create",
        name="ai-news-fetch",
        schedule="0 7 * * *",
        prompt="Fetch the top 10 AI/ML stories from Hacker News.")

# Job 2：使用 Job 1 的最新输出做筛选
# Job ID 可通过 cronjob(action="list") 查询
cronjob(action="create",
        name="ai-news-rank",
        schedule="30 7 * * *",
        context_from="<job1_id>",
        prompt="Score each story for novelty and engagement. Keep the top 5.")

# Job 3：使用 Job 2 的最新输出生成日报
cronjob(action="create",
        name="ai-news-brief",
        schedule="0 8 * * *",
        context_from="<job2_id>",
        prompt="Write a concise daily brief and deliver it to Telegram.")
```

`context_from` 支持单个 job ID 或多个 job ID：

| 写法         | 示例                              |
| ------------ | --------------------------------- |
| 单个上游任务 | `context_from="a1b2c3d4"`         |
| 多个上游任务 | `context_from=["job_a", "job_b"]` |

多个上游输出会按列表顺序拼接。运行时 Hermes 会读取上游任务在 `~/.hermes/cron/output/{job_id}/` 下最近一次完成的输出，拼接到下游任务的 prompt 前面；每个上游输出在注入前会被截断至 8,000 字符（超出部分以 `[... output truncated ...]` 标记），避免 prompt 过度膨胀。

> 注意：`context_from` 读取的是上游任务「最近一次已完成输出」，不会等待同一个 tick 中仍在运行的上游任务。如果上游本次运行还没结束、下游已经触发，下游会拿到上游上一次完成的结果。需要强依赖同一批数据时，应把上下游任务错开足够长的时间，或把多个步骤合并到同一个 cron prompt / 脚本里串行执行。

# 15. Delegation
https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation

Hermes 可以创建子 Agent 来处理独立的任务。子 Agent 有自己的对话和终端环境，互不干扰。

## 15.1 单任务与并行批量
**单任务：**

```text
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"],
)
```

**并行批量（默认最多 3 并发，可通过 `max_concurrent_children` 调高）：**

```text
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]},
])
```

超过 `max_concurrent_children` 的批量请求会直接返回工具错误，不会静默截断。结果按输入顺序排列，不受完成先后影响。父 Agent 中断会传播到所有活跃子 Agent。

## 15.2 子 Agent 上下文
子 Agent 启动时拥有全新对话，不知道父会话之前的任何内容。子 Agent 的唯一上下文来自接收的 `goal` 和 `context` 两个字段：

- `goal`：任务目标（必填）
- `context`：完成目标所需的全部背景信息——错误详情、文件路径、项目位置、环境约束等，父 Agent 必须在此完整传递

子 Agent 完成后，只有结构化摘要（做了什么、发现了什么、改了什么、遇到的问题）回传到父会话，详细对话过程不保留，以此控制 token 开销。

## 15.3 工具集限制
可通过 toolsets 参数限制子 Agent 可用工具，例如：

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

## 15.4 嵌套委派与配置
默认委派是扁平的：父 Agent（深度 0）→ 子 Agent（深度 1，不可再委派）。如需多阶段工作流，需要如下配置：

| 配置项                 | 作用                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------- |
| `role`                 | 单次 `delegate_task` 调用里的角色；`leaf` 是叶子节点，`orchestrator` 申请保留委派能力 |
| `max_spawn_depth`      | 全局最大委派深度；`1` 表示只允许父 Agent 生成一层叶子 Agent                           |
| `orchestrator_enabled` | 嵌套委派总开关；为 `false` 时，`role="orchestrator"` 也会被强制当作 `leaf`            |

对应配置示例：

```yaml
# ~/.hermes/config.yaml
delegation:
  max_concurrent_children: 3   # 并行子 Agent 上限
  max_spawn_depth: 1           # 嵌套深度，1 = 扁平（默认），设为 2 允许 orchestrator 再生成叶子节点
  orchestrator_enabled: true   # false 时全局禁止嵌套委派，role="orchestrator" 也被强制降级为 leaf
  # model: "google/gemini-flash-2.0"   # 可选：为子 Agent 指定不同模型，省略则继承父 Agent 模型
  # provider: "openrouter"
```

将子 Agent 角色设为 `orchestrator` 的工具调用形态如下：

```text
delegate_task(
    goal="Survey three approaches and recommend one",
    role="orchestrator",
    context="...",
)
```

配置交互关系：

| 配置组合                                    | 结果                                                             |
| ------------------------------------------- | ---------------------------------------------------------------- |
| `role="leaf"`，任意 `max_spawn_depth`       | 子 Agent 是叶子节点，不能再调用 `delegate_task`                  |
| `role="orchestrator"`，`max_spawn_depth: 1` | 会被深度限制挡住，实际仍不能继续委派                             |
| `role="orchestrator"`，`max_spawn_depth: 2` | 子 Agent 可以再委派一层叶子 Agent                                |
| `role="orchestrator"`，`max_spawn_depth: 3` | 子 Agent 可以继续形成最多三层的委派树                            |
| `orchestrator_enabled: false`               | 全局禁用嵌套委派，`role="orchestrator"` 会被强制当作 `leaf` 处理 |

# 16. Kanban
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://github.com/NousResearch/hermes-agent/blob/main/docs/hermes-kanban-v1-spec.pdf

Hermes Kanban 是一个多 Agent 协作层：它是一个可恢复、可审计、可中途介入的工作队列。它把任务、依赖、评论、运行记录和工作目录放进一个持久任务板里，让多个具名 profile 以异步方式协作。

## 16.1 Kanban 的目标
### 16.1.1 从 `delegate_task` 到 Kanban
Hermes 已经有多 Agent 能力 `delegate_task`：父 Agent 构造一个 `goal` 和可选 `context`，同步启动一个短生命周期、隔离会话里的子 Agent，然后阻塞等待子 Agent 返回摘要。这是一种“分叉并汇合”（fork-and-join）调用，适合短的、自包含的推理子任务。子 Agent 完成后，它的详细过程不会作为一个可继续协作的对象留在系统里；父 Agent 只拿到结构化摘要，并把这个摘要放回当前上下文继续推理。

`delegate_task` 无法覆盖如下场景：

1. **研究分流与综合（Research triage and synthesis）**：多个专家型 Agent 并行产出候选发现，一个或多个审查者选择、合并，人类还可能中途纠正方向。
2. **定时循环工作流（Scheduled recurring workflows）**：日报、周报、小时级收件箱分流等任务会跨运行积累知识，并且要能从单次失败中恢复。
3. **数字分身 / 持久助手角色（Digital-twin / persistent assistant roles）**：具名、长期存在的 Agent 身份会在数周或数月里积累对人、偏好和上下文的记忆。
4. **端到端工程流水线（End-to-end engineering pipelines）**：拆解、并行实现、审查、迭代、提交，整个流程可能持续数小时，并需要保留每个贡献者的身份和交接记录。

这些场景都需要如下能力：

- 跨运行持久状态
- 工作进行中的可见性
- 不同技能 Agent 之间的交接
- 人类或对等 Agent 随时介入

Kanban 的目标就是补上这些能力。它把协作状态放到一个 Hermes 可控的持久层里，而不是放在某个父 Agent 的上下文窗口或第三方 SDK 的进程内生命周期里。任务、依赖、评论、运行结果和失败恢复都落到任务板上；每个执行者都是具名 profile，拥有自己的 `HERMES_HOME`、记忆、技能和工作目录。

### 16.1.2 其他系统的设计方案
#### 16.1.2.1 Cline Kanban
Cline Kanban 的形态是本地任务板：一个任务是一张卡片，每张卡片对应一个临时 git 工作树，并可以分配给不同命令行 Agent。卡片可以连成依赖链，父任务完成后子任务自动启动。

它的启发是：**任务板 + 依赖链接 + 工作目录** 本身就足以构成一个有效的协调层。它没有账号系统、服务器基础设施、复杂治理，也不强调长期 Agent 身份。这个模型简单有效，但偏代码任务：git 工作树是核心假设，非代码工作和长期身份不是主要目标。

#### 16.1.2.2 Paperclip
Paperclip 把 Agent 建模成公司里的“员工”：有组织结构图、预算、治理、目标任务图、心跳、执行记录和每 Agent 的 API key 轮换。它强调持久 Agent 身份和原子任务认领，Agent 运行时也可以是 OpenClaw、Claude Code、Codex、Cursor、bash 或 HTTP。

它的启发是：长期协作需要持久身份、原子认领和可恢复任务。但它也展示了另一端的复杂度：预算、审批、治理、组织架构对企业场景有价值，但不一定应该进入 Hermes 的协作内核。对多数用户来说，这些更适合做成 profile 约定或插件。

#### 16.1.2.3 NanoClaw Agent Swarms
NanoClaw Agent Swarms 基于 Claude Code 的实验性 agent teams 能力，让主 Agent 在容器中编排多个子 Agent。

它的启发是：不要把协作生命周期完全绑定在外部 SDK 的会话分支、resume 语义或临时子 Agent 生命周期上。协调层必须在 Hermes 自己控制的层里；工作者应该是独立操作系统进程，失败、崩溃、超时或主机重启后都可以通过任务板和认领机制恢复。

#### 16.1.2.4 三者比较分析
| 维度     | Cline Kanban              | Paperclip               | NanoClaw Swarms          |
| -------- | ------------------------- | ----------------------- | ------------------------ |
| 形态     | 本地任务板                | 服务器 + UI + 公司模型  | SDK 进程内团队           |
| 任务粒度 | 一张卡片一个 git 工作树   | 目标 → 项目 → issue     | 团队负责人 fork 子 Agent |
| 身份     | 卡片级匿名执行            | 持久“员工”              | 每次启动都是匿名         |
| 持久性   | DB + git 工作树           | 中央服务器 DB           | 绑定 `query()` 生命周期  |
| 依赖     | 已链接卡片                | issue 链接 / 阻塞关系   | 没有明确依赖模型         |
| 治理     | 基本没有                  | 预算、审批、审计日志    | 基本没有                 |
| 失败模式 | 崩溃工作者留下 git 工作树 | 崩溃 Agent 变成孤儿任务 | 子 Agent 静默终止        |
| 协调介质 | git + 卡片状态            | DB + 心跳 + tickets     | SDK 消息传递             |

Cline 的简单任务板形态是有效的，但偏代码任务；Paperclip 的持久身份和原子认领很有价值，但企业治理过重；NanoClaw 进程内群体协作对上游生命周期太敏感。Hermes Kanban 取它们的交集：任务板、依赖链接、工作目录、持久身份、原子认领；同时避免企业治理内核化和 SDK 群体协作脆弱性。

### 16.1.3 Hermes Kanban 的设计理念
Hermes Kanban 的设计理念可以概括为几个取舍：

- 采用 Cline 的任务板 + 依赖链接 + 工作目录形态
- 采用 Paperclip 的原子认领和持久身份，但把身份映射到 Hermes profile
- 拒绝 NanoClaw 式进程内子 Agent 群体协作，每个工作者都是完整操作系统进程
- 拒绝把 Paperclip 的治理控制面做进内核

最终目标是一个轻量但稳固的协作内核：

- 一个 SQLite 任务板
- 一个 Kanban 命令行入口
- 一个调度器
- 一组工作者技能 / 工具，以及 Hermes profile

任何复杂的协作形态、角色分工和策略，都通过 profile、技能、插件扩展。

## 16.2 架构
![hermes kanban architecture](images/hermes_kanban_architecture.png)

三层架构：

- 控制层是用户交互入口，包括 CLI、Gateway 和 Dashboard
- 状态层是任务板和简易调度器
- 执行层是一组相互独立的 profile 进程，每个进程都有隔离状态

所有协调都通过任务板流转，profile 之间没有直接的进程间通信。

### 16.2.1 Control Plane：CLI / Gateway / Dashboard
控制层是用户与 Kanban 交互的入口。用户通过 CLI、Gateway 或 Dashboard 把工作交给 Kanban，查看当前进展，补充人工反馈，并根据执行结果决定下一步。

控制层关心的是“我要做什么”“现在做到哪里”“是否需要人工介入”，不直接持有 worker 的执行上下文。

### 16.2.2 State Plane：SQLite board + dispatcher
状态层是 Kanban 的唯一事实来源。默认 board 使用 `~/.hermes/kanban.db` 共享 SQLite 数据库，所有 profile 进程都读取和写入它。

dispatcher 根据 board 里的任务状态和依赖关系，决定哪些任务可以运行，并启动对应的 profile worker。

### 16.2.3 Execution Plane：独立 profile worker
执行层由一组独立 profile 进程组成。每个 worker 都是完整的 Hermes 进程，拥有自己的 `HERMES_HOME`、记忆、技能和工作目录。

worker 之间不直接通信，所有输入、输出、状态变化和交接都写回 board。

## 16.3 Kanban 核心概念
### 16.3.1 Board：任务板
Board 是一个独立的任务队列，拥有自己的 SQLite 数据库、workspaces 目录和调度循环。可以有多个 board，例如按项目、仓库或业务域拆分；如果只使用单项目工作流，默认使用 `default` board。

默认 board 的数据库位于 `~/.hermes/kanban.db`。非默认 board 位于 `~/.hermes/kanban/boards/<slug>/` 下，并拥有独立的 `kanban.db`、`workspaces/` 和 `logs/`。dispatcher 启动 worker 时会固定 `HERMES_KANBAN_BOARD`，让 worker 只看到自己所属的 board。

### 16.3.2 Task：任务
Task 是 Kanban 的基本工作单元，一个 Task 对应数据库中的一行记录，通常包含标题、正文、一个指派、状态、优先级、workspace 设置等。

一个 task 只有一个 `assignee`，它通常是 Hermes profile 名称。

`tasks` 表结构：

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id                   TEXT PRIMARY KEY,             -- 任务 ID，例如 t_abcd1234
    title                TEXT NOT NULL,                -- 标题
    body                 TEXT,                         -- 任务正文 / 初始说明
    assignee             TEXT,                         -- 指派的 Hermes profile
    status               TEXT NOT NULL,                -- 任务状态
    priority             INTEGER DEFAULT 0,            -- 优先级，越大越先调度
    created_by           TEXT,                         -- 创建者，profile 或 user
    created_at           INTEGER NOT NULL,             -- 创建时间，Unix 时间戳
    started_at           INTEGER,                      -- 首次开始时间
    completed_at         INTEGER,                      -- 完成时间
    workspace_kind       TEXT NOT NULL DEFAULT 'scratch', -- scratch/worktree/dir
    workspace_path       TEXT,                         -- claim 时解析出的实际工作目录
    claim_lock           TEXT,                         -- 认领锁，通常是 host:pid
    claim_expires        INTEGER,                      -- 认领过期时间
    tenant               TEXT,                         -- 租户 / 命名空间
    result               TEXT,                         -- 任务最终结果
    idempotency_key      TEXT,                         -- 幂等键，避免重复创建
    consecutive_failures INTEGER NOT NULL DEFAULT 0,   -- 连续失败计数
    worker_pid           INTEGER,                      -- 当前 worker 子进程 PID
    last_failure_error   TEXT,                         -- 最近一次失败摘要
    max_runtime_seconds  INTEGER,                      -- 最大运行时长
    last_heartbeat_at    INTEGER,                      -- 最近心跳时间
    current_run_id       INTEGER,                      -- 当前 task_runs 记录 ID
    workflow_template_id TEXT,                         -- workflow 模板 ID，预留
    current_step_key     TEXT,                         -- 当前 workflow step，预留
    skills               TEXT,                         -- 额外强制加载的 skills，JSON
    max_retries          INTEGER                       -- 单任务重试阈值
);
```

task 的状态包括：

| 状态        | 中文说明                                                         |
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

用户、脚本、decomposer 或 worker 都可以创建 task。普通任务只有进入 `ready` 后才会被 dispatcher 认领并启动；`review` 是单独的审查队列，dispatcher 会启动对应 assignee 的 review worker，并强制加载 `sdlc-review` skill。`scheduled` 不会被直接调度，需要通过 cron、人工操作或自动化恢复到 `ready` / `todo`。

### 16.3.3 Link：任务的依赖关系
Link 是 task 之间的父子依赖，对应 `task_links` 表中的 `parent_id -> child_id`。父任务完成之前，子任务保持在 `todo` 或等待状态；当所有父任务都为 `done` / `archived` 后，dispatcher 会把子任务推进到 `ready`。

这个机制让 Kanban 可以表达常见任务流程：一个任务可以展开成多个下游任务（fan-out），多个上游任务也可以汇合到同一个下游任务（fan-in）；下游任务会等依赖满足后再启动。

`task_links` 表结构：

```sql
CREATE TABLE IF NOT EXISTS task_links (
    parent_id  TEXT NOT NULL, -- 父任务 ID，上游任务
    child_id   TEXT NOT NULL, -- 子任务 ID，下游任务
    PRIMARY KEY (parent_id, child_id)
);
```

### 16.3.4 Comment：任务的评论 / 交接记录
Comment 是人类和 Agent 在 task 上追加的持久消息，也是 Kanban 的跨 Agent 交接协议。worker 被启动或重新启动时，会读取 task 正文、父任务结果、历史运行记录和完整评论串。

因此，评论不是临时聊天记录，而是任务上下文的一部分。人类可以通过评论补充要求、回答 worker 的问题、纠正方向；Agent 也可以通过评论留下中间发现、交接说明或阻塞原因。

`task_comments` 表结构：

```sql
CREATE TABLE IF NOT EXISTS task_comments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT, -- 评论 ID
    task_id    TEXT NOT NULL,                    -- 所属任务 ID
    author     TEXT NOT NULL,                    -- 作者，profile 或 user
    body       TEXT NOT NULL,                    -- 评论正文
    created_at INTEGER NOT NULL                  -- 创建时间，Unix 时间戳
);
```

### 16.3.5 Event：任务事件
Event 是 Kanban 的任务审计日志，对应 `task_events` 表。它记录 task 生命周期里的状态变化、人工编辑和 worker 执行遥测，例如创建、指派、依赖满足后从 `todo` 推进到 `ready`（`promoted`）、dispatcher 认领、worker 启动、心跳、完成、阻塞、崩溃、超时、恢复，以及熔断器放弃重试（`gave_up`）。

`task_runs` 是每次 worker 执行尝试的记录表，用来保存本次运行的 profile、开始 / 结束时间、结果摘要、metadata 和错误信息；`task_events` 可以通过 `run_id` 关联到某一次执行尝试，并把这些变化串成按时间排序的审计轨迹。

`task_events` 表结构：

```sql
CREATE TABLE IF NOT EXISTS task_events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT, -- 事件 ID，单调递增
    task_id    TEXT NOT NULL,                    -- 所属任务 ID
    run_id     INTEGER,                          -- 所属 task_runs 记录，可为空
    kind       TEXT NOT NULL,                    -- 事件类型
    payload    TEXT,                             -- JSON payload
    created_at INTEGER NOT NULL                  -- 创建时间，Unix 时间戳
);
```

常见事件可以分成三类：

- **任务生命周期**：`created`（创建）、`promoted`（依赖满足后推进到 `ready`）、`claimed`（被 dispatcher 认领）、`completed`（完成）、`blocked`（阻塞）、`unblocked`（解除阻塞）、`archived`（归档）
- **人工或控制面编辑**：`assigned`（改派 assignee）、`edited`（编辑标题或正文）、`reprioritized`（调整优先级）、`status`（直接改状态）
- **worker / dispatcher 遥测**：`spawned`（worker 已启动）、`heartbeat`（worker 心跳）、`reclaimed`（认领过期后回收）、`crashed`（worker 崩溃）、`timed_out`（运行超时）、`stale`（长时间无心跳后判定陈旧）、`respawn_guarded`（重启被保护策略拦截）、`spawn_failed`（worker 启动失败）、`protocol_violation`（协议违例）、`gave_up`（熔断器放弃重试）

### 16.3.6 Workspace：任务的工作目录
Workspace 是 task 绑定的工作目录，也是 worker 执行该 task 时所在的文件系统目录。Task 通过 `workspace_kind` 和 `workspace_path` 记录 workspace 设置；board 提供默认的 `workspaces/` 根目录，用来放置 `scratch` 类型任务目录。Kanban 支持如下 workspace 类型：

- `scratch`：默认模式，为 task 创建新的临时工作目录。默认 board 位于 `~/.hermes/kanban/workspaces/<id>/`；非默认 board 位于 `~/.hermes/kanban/boards/<slug>/workspaces/<id>/`
- `dir:<path>`：使用已有绝对路径
- `worktree`：为代码任务创建 git worktree，目录通常位于 `.worktrees/<id>/`。由 worker 侧执行 `git worktree add` 创建，让并行工程任务互不干扰

### 16.3.7 Dispatcher：调度器
Dispatcher 是一个长期循环，默认运行在 Gateway 内部。它每 N 秒（默认 60 秒）扫描 board，回收异常任务，重新计算 ready 状态，认领可启动任务，并为已分配 assignee 的任务启动对应 profile worker。

这个间隔可通过 `kanban.dispatch_interval_seconds` 调整：

```yaml
# ~/.hermes/config.yaml
kanban:
  dispatch_interval_seconds: 60  # dispatcher tick 间隔，单位秒；默认 60，最小 1
```

### 16.3.8 Worker：执行者
Worker 是 dispatcher 启动的独立 Hermes profile 进程。每个 worker 都是完整的操作系统进程，拥有自己的 `HERMES_HOME`、记忆、技能、工具权限和 workspace。

处理 Kanban task 的 profile 需要加载 `kanban-worker` skill。这个 skill 教会 worker Kanban 工具调用完整生命周期，而不是在终端里执行 `hermes kanban ...` 命令：

1. 启动后先调用 `kanban_show()`，读取 task 标题、正文、父任务交接、历史运行记录和完整评论串
2. 通过 terminal 工具进入 `$HERMES_KANBAN_WORKSPACE`，在 task 绑定的 workspace 中执行工作
3. 长时间运行时定期调用 `kanban_heartbeat(note="...")`，刷新心跳并留下进度说明
4. 完成时调用 `kanban_complete(summary="...", metadata={...})`；卡住时调用 `kanban_block(reason="...")`

`kanban-worker` 是 bundled skill，安装和更新时会同步到每个 profile。dispatcher 启动 worker 时也会自动传入 `--skills kanban-worker`，所以即使某个 profile 的默认 skills 配置里没有它，worker 仍会获得这套工作模式。

worker 不通过 CLI 命令操作任务板，而是通过 `kanban_*` 工具读取和更新 task，例如 `kanban_show`、`kanban_heartbeat`、`kanban_complete`、`kanban_block`、`kanban_comment`。这样做是为了保持后端可移植性：worker 的 terminal 工具可能指向远程执行后端，例如 Docker、SSH。如果 worker 在 terminal 里执行 `hermes kanban complete`，命令实际会运行在远程容器或远程主机中，而远程主机可能没有安装 `hermes`，也没有挂载本机的 `~/.hermes/kanban.db`。`kanban_*` 工具则运行在 Agent 自己的 Python 进程里，可以直接访问当前 Hermes home 下正确的 board 数据库，不受 terminal 后端位置影响。

## 16.4 协作模式
Kanban 可衍生出如下可重用的协作模式。

### 16.4.1 扇出（Fan-out）
把一个目标拆成多个同级 task，并行交给同一类或多类 profile 执行。task 之间没有父子依赖，各自独立产出结果；如果需要综合，再创建一个下游汇总 task。

例如：

```text
goal
├── researcher-a
├── researcher-b
└── researcher-c
```

### 16.4.2 流水线（Pipeline）
上游 task 完成后，下游 task 才进入 `ready`，适合“一个阶段的输出是下一个阶段的输入”的工作。依赖关系用 `task_links` 表达，父任务的摘要和评论会成为下游 worker 的上下文。

例如：

```text
researcher -> analyst -> writer -> reviewer
```

### 16.4.3 扇入（Fan-in）
多个同级 task 先独立产出候选发现、判断或实现方案；聚合 task 依赖它们全部完成后再启动。适合研究综合、方案评审、并行实现后的汇总。

例如：

```text
researcher-a \
researcher-b  -> reviewer / aggregator
researcher-c /
```

### 16.4.4 长期运行日志（Long-running journal）
同一个 profile 在同一个共享 workspace 通过定时任务反复处理周期性任务。profile 通过持久记忆和共享 workspace 累积经验，并利用 Kanban 充当审计时间线。适合日报、周报、监控巡检、收件箱分流这类工作。

### 16.4.5 人工介入分流（Human-in-the-loop triage）
worker 遇到不确定的情况时，把 task 置为 `blocked`，并在任务评论中附上疑问。用户或其他 profile 通过评论回复并 unblock 任务。调度器会重新启动 worker，任务评论会成为下一次 worker 的上下文。

例如：

```text
worker 执行 -> kanban_block(reason) -> user comment -> unblock -> dispatcher 重新启动 worker
```

### 16.4.6 批量对象作业（Fleet farming）
一个 profile 管理 N 个对象：这里的对象可以是社媒账号、客户、服务器、仓库、监控服务或数据源。所有 task 指派给同一个 profile，但每个对象使用自己的 workspace 目录。

例如一个 `insta-manager` profile 管理 50 个 Instagram 账号：

```text
task: post daily story for acct-1   -> assignee=insta-manager, workspace=dir:~/insta/acct-1/
task: post daily story for acct-2   -> assignee=insta-manager, workspace=dir:~/insta/acct-2/
...
task: post daily story for acct-50  -> assignee=insta-manager, workspace=dir:~/insta/acct-50/
```

通过 Cron 按账号定期创建任务，例如每天为每个账号创建一个发布、巡检或分析 task。

## 16.5 Dispatcher：调度器
### 16.5.1 职责与 tick 流程
dispatcher 负责把 board 中已经满足运行条件的 task 交给对应 profile worker，并推进 task 状态。每次 tick 主要执行四类动作：

1. **stale recovery**：先处理异常的 `running` 任务，包括认领过期、worker 进程已经退出、超过最大运行时间等情况。必要时释放 `claim_lock`，把任务恢复到可重新调度的状态，并记录回收、崩溃或超时事件。
2. **recompute ready**：将没有父任务，或所有父任务都已经 `done` / `archived` 的任务推进到 `ready`。
3. **atomic claim**：扫描 `ready`、`claim_lock IS NULL`、`assignee IS NOT NULL` 的任务，通过“比较并交换”（compare-and-swap）式 SQL 更新 `tasks` 表记录。只有更新成功才算认领成功；成功后任务变成 `running`，并写入 `claim_lock` 和 `claim_expires`。
4. **启动 worker**：认领成功后解析 workspace，启动 assignee 对应的 profile worker。worker 启动成功后，dispatcher 把子进程 PID 写入 `worker_pid`，并记录启动事件。

### 16.5.2 并发正确性
任务认领通过 SQLite 写事务和“比较并交换”式更新完成。并发 tick、重复触发或恢复过程同时看到同一个 `ready` task 时，只有一个认领者能成功把它推进到 `running`。

核心语义类似：

```sql
UPDATE tasks
   SET status = 'running',
       claim_lock = ?,
       claim_expires = ?
 WHERE id = ?
   AND status = 'ready'
   AND claim_lock IS NULL;
```

如果更新命中 1 行，说明当前调度器成功认领任务，可以继续启动 worker。如果更新命中 0 行，说明任务状态已经变化或已经被认领，当前 tick 不会启动 worker。

### 16.5.3 失败与恢复
worker 启动失败、运行超时、进程崩溃，或没有按协议把 task 标记为完成 / 阻塞，都会被记录到任务事件和运行记录中。dispatcher 后续 tick 会尝试恢复这类任务，让它重新进入可调度状态。

为了避免同一个坏任务无限重试，Kanban 会维护连续失败计数。超过重试上限后，任务会自动进入 `blocked`，并保留最近一次错误信息，等待人类或 orchestrator profile 介入。

## 16.6 Orchestrator Profile
### 16.6.1 Decomposer 与 Orchestrator Profile
Kanban 状态层负责推进任务队列，但不负责理解目标：

- **SQLite board** 保存 task、依赖、评论、结果和事件记录。
- **dispatcher** 每个 tick 根据 `task_links` 重新计算依赖是否满足，把符合条件的 `todo` task 推进到 `ready`；随后认领 `ready` task，并启动对应的 profile worker。

这些组件不会自己进行“编排”：判断目标应该如何拆解、每一步该交给哪个 profile、子任务完成后整体是否已经完成。

因此，Kanban 把编排放在状态层之外处理，并分成两个阶段：

1. **第一阶段：decomposer 处理 `triage` task**。Kanban 内存在一个 decomposer 用于拆解 `triage` task，有自动和手动两种模式。
   - 自动模式下，dispatcher 每个 tick 会自动触发 decomposer。
   - 手动模式下，`triage` task 会留在任务板上，直到用户在 Dashboard 点 Decompose，或运行 `hermes kanban decompose <id>`，或在聊天里使用 `/kanban decompose <id>` 来触发 decomposer。
   - decomposer 不是 profile，也不是 worker，而是在 Gateway 进程内运行的辅助 LLM 拆解流程。它被触发后会执行如下流程：
     1. 读取 `triage` task 的标题和正文。
     2. 读取可用 profile 及其 description，并读取 `kanban.default_assignee` 作为兜底 assignee。
     3. 调用 `auxiliary.kanban_decomposer` 配置的模型，生成 task graph JSON。这个 JSON 描述是否需要拆分、要创建哪些子任务、每个子任务交给哪个 profile，以及子任务之间的依赖关系。
     4. 如果 LLM 判断需要 fan-out，decomposer 会根据 JSON task graph 更新 board：创建子任务、写入 assignee、建立依赖，并把原始 `triage` task 改成 root task。root task 的 `assignee` 设置为 `kanban.orchestrator_profile`，并等待所有子任务完成。
     5. 如果 LLM 判断不需要 fan-out，decomposer 会把原 `triage` task 改写成更完整的单任务说明，并推进到可调度状态。
2. **第二阶段：orchestrator profile 承接 root task**。子任务完成后，root task 会回到 `ready`，dispatcher 会启动 root task 当前 `assignee` 对应的 profile worker。默认情况下，这个 `assignee` 是 decomposer 根据 `kanban.orchestrator_profile` 写入的 profile。这个 worker 会读取子任务结果，做总体验收和汇总：如果目标已经完成，就完成 root task；如果还缺步骤，就继续追加 task 或留下阻塞说明。

除了自动拆解后的 root task `assignee` 设置为 `kanban.orchestrator_profile`，用户也可以直接和某个 orchestrator profile 交流，把高层目标交给它，让它手动创建 task、指派 profile、建立依赖。也就是说，orchestrator profile 在手动编排中可以做“拆解任务”的工作，效果上类似 decomposer；但它是一个普通 Hermes profile，通过 Kanban 工具操作 board，不是 Gateway 内部的 decomposer 流程。

### 16.6.2 Auto Decompose 相关配置
相关配置项：

```yaml
# ~/.hermes/config.yaml
kanban:
  auto_decompose: true        # 是否让 dispatcher 自动拆解 triage 任务
  auto_decompose_per_tick: 3  # 每个 dispatcher tick 最多拆解几个 triage 任务
  orchestrator_profile: ""    # root task 的默认 assignee；空值表示使用当前默认 profile
  default_assignee: ""        # LLM 选到未知 profile 时的兜底 assignee；空值表示使用当前默认 profile

auxiliary:
  kanban_decomposer:          # Decompose 使用的辅助模型
    provider: ""
    model: ""
```

### 16.6.3 Orchestrator Profile 的职责与约束
Orchestrator profile 的职责是协调，不是执行。它应该做的事是：

1. 读取用户目标，或读取一个被指派给自己的 root task。
2. 判断这个目标是否需要拆分；如果目标不清楚，先向用户补充提问。
3. 查看当前可用的 profile，确认哪些 profile 适合承担哪些子任务。
4. 创建子任务，写清楚每个子任务的目标、执行说明、assignee 和依赖关系。
5. 等待下游 task 完成后，读取它们的结果和评论，汇总整体进展。
6. 判断总目标是否完成；如果完成，就完成 root task；如果还缺步骤，就继续创建下一批 task；如果卡住，就留下阻塞说明。

它不应该自己研究资料、改代码、写稿、跑测试或处理运维命令。如果一个任务已经具体到“去实现”“去验证”“去写成文档”，就应该进入新的 Kanban task，并交给对应 profile。

如果不加约束，orchestrator profile 可能会自己处理任务，而不是把任务路由给合适的 profile。因此需要对 orchestrator profile 做一些约束：

1. **禁用执行型工具**：推荐让 orchestrator profile 只拥有 board 和记忆相关能力，例如 `kanban`、`memory`，必要时再加 `messaging`，而不要给它 terminal、file、web、browser、code 等执行工具。这样模型无法自己处理任务，只能创建任务并委派。
2. **加载 `kanban-orchestrator` skill**：这个内建的 skill 的作用是给 orchestrator profile 注入明确的行为约束：你是编排者，不是执行者；任何具体任务都创建 Kanban task 并指派给合适 profile；你的职责是拆解、路由、汇总，而不是研究、写作或编码。
3. **基于真实 profile 路由**：orchestrator profile 在拆分任务前，应先发现本机真实存在的 profile，并根据这些 profile 的 description 路由；不要凭空编造 profile 名称。

### 16.6.4 创建 orchestrator profile
创建一个名为 `orchestrator` 的 profile，继承当前默认 profile 的模型和 API 配置，并把它配置为自动拆解后 root task 的默认 assignee。

```bash
# 创建 orchestrator profile，并写入 profile description
hermes profile create orchestrator --clone \
  --description "Kanban 编排者。负责拆解高层目标、创建任务、指派真实存在的 profile、建立依赖关系、汇总下游结果；不直接执行研究、写作、编码或运维任务。"

# 限制工具使用
orchestrator tools disable terminal file web browser code_execution

# 确认 bundled skill 已存在；如果缺失就恢复
orchestrator skills list | grep kanban-orchestrator \
  || orchestrator skills reset kanban-orchestrator --restore

# root task 默认交给 orchestrator
hermes config set kanban.orchestrator_profile orchestrator

# 启用自动拆解
hermes config set kanban.auto_decompose true
```

两种常见使用方式。

第一种是**直接和 orchestrator profile 聊天**，把高层目标交给它，让它创建 Kanban task：

```bash
orchestrator chat -q "给后台加一个导出 CSV 功能：先确认现有报表模块中仍然承担业务价值的历史设计，再实现导出、补测试、写使用说明。"
```

第二种是**把粗略任务放进 `triage`**，让 decomposer 先拆第一轮，随后由 `orchestrator` 承接 root task：

```bash
hermes kanban create "把用户设置页迁到新前端框架，并保持所有历史交互习惯不被用户察觉：梳理旧逻辑、实现迁移、补回归测试和上线检查" --triage
```

在 `kanban.auto_decompose: true` 时，dispatcher 后续 tick 会触发 decomposer。decomposer 创建子任务后，会把原始 `triage` task 变成 root task，并把它的 `assignee` 设为 `kanban.orchestrator_profile`，也就是上面配置的 `orchestrator`。

如果要让 decomposer 更准确地把任务分给其他 profile，还需要给可执行工作的 profile 写清楚 description：

```bash
hermes profile create researcher --description "负责查阅文档、源码和资料，产出结构化研究结论。" --clone
hermes profile create writer --description "负责把已有材料整理成清晰、连贯的文档。" --clone
hermes profile create reviewer --description "负责审查文档或代码变更，指出遗漏、错误和风险。" --clone
```

## 16.7 Multi-Tenant Context：多租户上下文
Multi-Tenant Context 解决的是“同一个 profile 服务多个业务上下文”的问题。例如同一个 `researcher` profile 可以同时服务 `business-a`、`business-b` 和 `personal`，而不需要为每个业务复制一个 `researcher`。

### 16.7.1 Tenant 的含义和边界
`tenant` 是 task 上的可选命名空间，对应 `tasks.tenant` 字段。它不是新的实体类型，也不是权限边界；它只是给任务标记业务上下文。

创建任务时可以通过 `--tenant` 指定：

```bash
hermes kanban create "monthly report" \
  --assignee researcher \
  --tenant business-a \
  --workspace dir:/home/user/tenants/business-a/data/
```

这表示：仍然由同一个 `researcher` profile 执行，但这次任务属于 `business-a`，并在 `business-a` 对应的数据目录里工作。

Tenant 主要影响四件事：

| 范围      | 作用                                                                                           |
| --------- | ---------------------------------------------------------------------------------------------- |
| Workspace | 任务可以使用租户专属目录，例如 `dir:/home/user/tenants/business-a/data/`，文件隔离交给文件系统 |
| 记忆      | worker 会收到当前 tenant，可按 tenant 前缀写入记忆；这是一种命名约定，不是自动分区             |
| Board     | CLI、Dashboard 和工具可以按 tenant 过滤任务                                                    |
| 审计      | task 带有 tenant 后，可以按 tenant 查询对应任务及其事件历史                                    |

worker 启动时会收到 `HERMES_TENANT` 环境变量，`kanban_show()` 返回的 worker context 里也会包含 `Tenant: <name>`。Hermes 不会自动创建独立记忆库，也不会强制 memory 工具按 tenant 分区；如果要保存租户相关长期信息，应在记忆内容中显式带上 tenant 前缀，例如“`business-a` 的月报默认读取 `/home/user/tenants/business-a/data/`”。

Tenant 只隔离数据上下文，不复制执行体系。profile、dispatcher、board、orchestrator profile 都仍然共享。

如果 `business-a-researcher` 和 `business-b-researcher` 确实需要不同身份、不同工具权限或不同长期记忆，就应该创建两个 profile，而不是只依赖 tenant。如果需要硬隔离，应使用不同 board。

Tenant 是软隔离，不是安全边界。它不提供 tenant 级访问控制，不会自动切换 profile 配置，也不替代 workspace 隔离。敏感数据仍应该放在各自 tenant 的目录下，并通过 `dir:<absolute-path>` 明确绑定。

通过这种轻量设计：一个可空的 `tenant` 字段、一个 workspace 约定、一个 `HERMES_TENANT` 环境变量，就能让同一个 profile 服务多个客户、账号、项目或业务域。

### 16.7.2 子任务如何继承 Tenant
当一个带 `tenant` 的 task 被 dispatcher 启动时，worker 进程会收到 `HERMES_TENANT`。worker 或 orchestrator profile 在这个上下文里调用 `kanban_create` 创建子任务时，如果没有显式传入 `tenant`，工具会默认使用当前环境里的 `HERMES_TENANT`。

这让 orchestrator profile 在同一个业务上下文里继续拆任务时，不需要每次手动重复 tenant：

```text
root task: tenant=business-a
        |
        v
orchestrator profile 启动时收到 HERMES_TENANT=business-a
        |
        v
kanban_create(...) 默认创建 tenant=business-a 的子任务
```

decomposer 拆解 `triage` task 时也会沿用原任务的 tenant。也就是说，如果原始 `triage` task 属于 `business-a`，自动拆出来的子任务也会属于 `business-a`。

## 16.8 命令工具
基本形式：

```bash
hermes kanban [--board <slug>] <action> [options]
```

Hermes 会按以下优先级决定要操作的 board：

1. CLI 显式传入的 `--board <slug>`
2. 环境变量 `HERMES_KANBAN_BOARD`
3. `~/.hermes/kanban/current`
4. `default`

### 16.8.1 快速启动
```bash
hermes kanban init      # 幂等创建默认 kanban.db，已存在时不会破坏数据
hermes gateway start    # 启动 Gateway
hermes kanban create "research Hermes Agent" --assignee researcher  # 创建任务
hermes kanban watch     # 实时观察事件
hermes kanban list      # 查看任务列表
hermes kanban stats     # 查看任务统计
```

### 16.8.2 Board 管理
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

### 16.8.3 创建、查询和指派
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

### 16.8.4 依赖和生命周期
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

### 16.8.5 Triage、规格化和拆解
`triage` 列用于接收粗略想法。可以手动触发，也可以让 dispatcher 在 `kanban.auto_decompose: true` 时自动处理。

```bash
hermes kanban specify <id> [--author NAME] [--json]                 # 把 triage task 补全成明确 spec
hermes kanban specify --all [--tenant T] [--author NAME] [--json]   # 批量规格化 triage task；可按 tenant 限定范围
hermes kanban decompose <id> [--author NAME] [--json]               # 把 triage task 拆成子任务图，并根据 profile description 路由
hermes kanban decompose --all [--tenant T] [--author NAME] [--json] # 批量拆解 triage task；可按 tenant 限定范围
```

`specify` 使用 `auxiliary.triage_specifier` 模型配置；`decompose` 使用 `auxiliary.kanban_decomposer` 模型配置。`decompose` 如果判断不需要 fan-out，会退化成类似 `specify` 的单任务补全。

### 16.8.6 运行、日志和监控
```bash
hermes kanban tail <id>          # 跟踪单个 task 的事件流
hermes kanban watch [--assignee P] [--tenant T] [--kinds completed,blocked,...] [--interval SECS]  # 观察整个 board 的事件流
hermes kanban runs <id> [--json]             # 查看一个 task 的 run history；一次认领、启动、失败或完成就是一条 run
hermes kanban stats [--json]                 # 查看状态和 assignee 统计
hermes kanban log <id> [--tail BYTES]        # 查看 worker 日志
hermes kanban context <id>                   # 打印 worker 会看到的完整上下文：title、body、父任务结果、评论等
```

### 16.8.7 Dispatcher 和维护
```bash
hermes kanban dispatch [--dry-run] [--max N] [--failure-limit N] [--json]  # 手动跑一次 dispatcher tick；用于调试或跳过默认 60 秒等待
hermes kanban gc [--event-retention-days N] [--log-retention-days N]       # 清理归档 task 的 scratch workspace、旧事件、旧日志
```

### 16.8.8 Gateway 通知订阅
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

### 16.8.9 `/kanban` slash command
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
