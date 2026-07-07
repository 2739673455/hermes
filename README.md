# Hermes Agent
https://hermes-agent.nousresearch.com/

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [快速上手](#2-快速上手)
3. [配置管理](#3-配置管理)
4. [Mixture of Agents (MoA)](#4-mixture-of-agents-moa)
5. [会话管理](#5-会话管理)
6. [Toolsets](#6-toolsets)
7. [MCP](#7-mcp)
8. [Skills](#8-skills)
9. [Hooks](#9-hooks)
10. [Plugins](#10-plugins)
11. [持久记忆](#11-持久记忆)
12. [上下文文件](#12-上下文文件)
13. [Gateway](#13-gateway)
14. [Profile](#14-profile)
15. [Cron](#15-cron)
16. [Delegation](#16-delegation)
17. [Kanban](#17-kanban)
18. [案例：深度研究](#18-案例深度研究)

# 1. Hermes Agent 是什么
Hermes Agent 是由开源 AI 研究实验室 Nous Research 开发的开源 AI Agent 框架，用于在本地终端、消息平台和自动化任务中运行可扩展的 Agent。

- **闭环学习**：跨会话保存记忆，沉淀可复用技能，并在后续任务中召回相关信息。
- **多平台接入**：连接 Telegram、Weixin 等消息平台，也可以通过 API 接入外部前端。
- **独立 Agent 实例**：为不同用途创建相互隔离的 Agent，每个实例拥有独立配置、会话、记忆和技能。
- **多 Agent 协作**：把复杂任务拆给子 Agent 或 Kanban 工作队列，支持并行执行、交接和人工介入。
- **多模型协作**：让多个模型先分析同一任务，再由聚合模型生成用户可见回复并调用工具。
- **扩展能力**：通过工具集、MCP、技能、钩子、插件和定时任务扩展 Agent 的能力边界。

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

安装完成后会得到：

1. Hermes 源码与运行依赖
2. `hermes` 命令入口
3. 默认数据目录 `~/.hermes`
4. 初始配置文件、密钥文件、身份文件和内置技能

## 2.2 初次配置
```bash
hermes model  # 交互式选择模型和提供商
hermes setup  # 或者运行完整设置向导
```

密钥存储在 `~/.hermes/.env` 文件中。

## 2.3 对话
```bash
hermes                # 终端交互模式
hermes --tui          # TUI 交互模式
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

## 2.5 更新与卸载
```bash
hermes update

hermes uninstall
```

完全清理所有数据时删除默认数据目录：

```bash
rm -rf ~/.hermes
```

## 2.6 Web Dashboard
Web Dashboard 提供浏览器界面，默认地址为 `http://127.0.0.1:9119`。

```bash
hermes dashboard              # 启动并自动打开浏览器
hermes dashboard --port 9119  # 指定端口
hermes dashboard --status     # 查看运行状态
hermes dashboard --stop       # 停止运行

hermes dashboard &>/dev/null & disown  # 后台运行并脱离终端
```

# 3. 配置管理
https://hermes-agent.nousresearch.com/docs/user-guide/configuration

## 3.1 目录结构
```
~/.hermes/
├── config.yaml     # 主配置文件
├── .env            # API 密钥和机密信息
├── auth.json       # OAuth 凭证
├── SOUL.md         # Agent 身份文件
├── state.db        # 会话、消息和运行状态
├── skills/         # 本地技能
├── plugins/        # 本地插件
├── cron/           # 定时任务定义和输出
└── logs/           # 运行日志
```

## 3.2 常用命令
配置文件命令：

```bash
hermes config                        # 查看配置文件中的当前配置
hermes config edit                   # 用 $EDITOR 打开 config.yaml 编辑
hermes config set section.key value  # 直接设置某个配置项
```

会话内切换命令：

| 命令                           | 功能                       |
| ------------------------------ | -------------------------- |
| `/config`                      | 查看当前会话使用的配置     |
| `/model [model-name]`          | 查看或切换当前模型         |
| `/reasoning [level/show/hide]` | 查看或切换当前模型推理级别 |
| `/yolo`                        | 跳过所有危险命令审批       |
| `/personality [name]`          | 切换当前会话的人格         |

# 4. Mixture of Agents (MoA)
MoA 是 Hermes 的多模型协作能力。它先让多个参考模型分析同一个任务，再把分析结果交给聚合模型生成最终回复。

## 4.1 使用
切换当前会话模型为 MoA：

```bash
/model default --provider moa
```

其中 `default` 是 MoA 预设名。

一次性使用：

```bash
/moa 为这个不稳定的测试集群设计迁移方案
```

`/moa <提示词>` 只对当前提示词使用默认 MoA 预设，执行后恢复原模型。

## 4.2 运行流程
当当前会话使用 MoA 预设时，Hermes 按以下流程生成回复：

1. 参考模型接收裁剪后的会话文本，生成私有分析
2. 聚合模型接收普通 Hermes 上下文、工具定义和私有分析，生成用户可见回复
3. 聚合模型发起工具调用时，Hermes 正常执行工具并写回结果
4. 工具结果需要继续生成回复时，Hermes 按同一流程再运行一轮

MoA 不改写已有历史、系统提示词或工具定义。稳定的会话前缀仍按普通模型调用缓存，主要额外开销来自每轮新增的参考模型调用。

## 4.3 配置
### 4.3.1 命令
```bash
hermes moa list              # 列出 MoA 预设
hermes moa configure         # 配置默认 MoA 预设
hermes moa configure review  # 创建或更新名为 review 的 MoA 预设
hermes moa delete review     # 删除名为 review 的 MoA 预设
```

### 4.3.2 配置文件
```yaml
# ~/.hermes/config.yaml
moa:
  default_preset: default           # /moa 默认使用的预设
  presets:
    default:
      reference_models:             # 先运行的参考模型
        - provider: openai-codex
          model: gpt-5.5
        - provider: openrouter
          model: deepseek/deepseek-v4-pro
      aggregator:                   # 生成最终回复和工具调用的模型
        provider: openrouter
        model: anthropic/claude-opus-4.8
      reference_temperature: 0.6
      aggregator_temperature: 0.4
      max_tokens: 4096              # 聚合模型最大输出 token
      reference_max_tokens: 600     # 参考模型最大输出 token
      enabled: true                 # 是否启用参考模型扇出
```

`enabled: false` 会关闭参考模型扇出，只保留聚合模型作为普通模型运行。`reference_max_tokens` 用于限制参考模型的输出 token。

# 5. 会话管理
Hermes Agent 自动将每次对话保存为会话，支持继续上次对话、按会话恢复、管理历史记录和搜索过去内容。

## 5.1 常用命令
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

| 命令                    | 功能                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------ |
| `/new`                  | 开始新会话                                                                           |
| `/clear`                | 清屏后开始新会话                                                                     |
| `/history`              | 显示对话历史                                                                         |
| `/undo`                 | 移除最后一轮用户/助手对话                                                            |
| `/title <session_name>` | 为当前会话设置标题                                                                   |
| `/compress`             | 手动压缩上下文                                                                       |
| `/rollback`             | 列出或恢复文件系统检查点                                                             |
| `/queue <prompt>`       | 将 prompt 加入队列等待下一轮处理，不会中断当前 agent 响应                            |
| `/steer <prompt>`       | 在下一次工具结果返回后，将中途说明追加到工具结果末尾，用于在任务进行中调整方向       |
| `/goal <text>`          | 设置持续性目标。辅助裁判模型会判断目标是否完成；若未完成则自动继续                   |
| `/subgoal <text>`       | 在循环进行中向活动目标追加一个用户自定义条件；原始目标和所有子目标全部满足后才会完成 |
| `/sessions`             | 查看和管理会话                                                                       |
| `/background <prompt>`  | 在独立的后台会话中运行  prompt                                                       |
| `/stop`                 | 停止后台进程                                                                         |
| `/branch [name]`        | 分支当前会话（探索不同路径）                                                         |

## 5.2 会话存储
Hermes 使用 SQLite 数据库 `~/.hermes/state.db` 保存会话状态。

SQLite 中主要有这几张表：

| 表               | 内容                |
| ---------------- | ------------------- |
| `sessions`       | 会话元数据          |
| `messages`       | 完整消息历史        |
| `messages_fts*`  | 会话搜索索引        |
| `state_meta`     | 状态型键值数据      |
| `schema_version` | schema 版本迁移状态 |

SQLite 数据库使用 WAL 模式支持并发读取和单写入。

## 5.3 上下文压缩
当会话上下文长度接近限制时，Hermes 会自动压缩历史消息，保留关键信息并维持上下文窗口可用。

### 5.3.1 相关配置
```yaml
# ~/.hermes/config.yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 上下文窗口阈值
  target_ratio: 0.20  # 窗口内保留多少不压缩
  protect_last_n: 20  # n 个末尾消息不压缩
```

### 5.3.2 压缩算法
| 阶段     | 处理内容                                                   |
| -------- | ---------------------------------------------------------- |
| 清理     | 清理旧工具结果和历史图片载荷                               |
| 保留     | 保留系统提示词、会话开头消息和最近上下文                   |
| 对齐     | 对齐 `tool_call` / `tool_result` 边界，避免拆散工具调用组  |
| 摘要     | 使用辅助模型生成结构化摘要，记录目标、约束、进展和后续操作 |
| 组装     | 将头部消息、压缩摘要和尾部消息组成新的消息列表             |
| 重压缩   | 再次触发压缩时更新前一次摘要                               |
| 失败处理 | 摘要生成失败时按配置中止压缩，或插入确定性 fallback 摘要   |

## 5.4 会话搜索工具
当用户引用过去对话中的内容，或 Agent 需要查找历史上下文时，Agent 会使用内置的 `session_search` 工具搜索历史消息。

`session_search` 使用 SQLite FTS5 搜索索引，支持三种调用形式：

1. 发现
   - 参数：`session_search(query, limit)`
   - 用途：搜索历史消息，按 session 去重返回
2. 滚动
   - 参数：`session_search(session_id, around_message_id, window)`
   - 用途：围绕命中消息滚动查看上下文
3. 浏览
   - 参数：`session_search()`
   - 用途：浏览最近 session

# 6. Toolsets
工具是扩展 Agent 能力的函数。Hermes 将工具组织为若干个工具集。

## 6.1 可用工具
Hermes 包含如下工具：

| 类别             | 包含工具                                                                                |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Web**          | `web_search`, `web_extract`                                                             |
| **X 搜索**       | `x_search`                                                                              |
| **终端与文件**   | `terminal`, `process`, `read_file`, `patch`                                             |
| **浏览器**       | `browser_navigate`, `browser_snapshot`, `browser_vision`                                |
| **媒体**         | `vision_analyze`, `image_generate`, `video_generate`, `video_analyze`, `text_to_speech` |
| **Agent 编排**   | `todo`, `clarify`, `execute_code`, `delegate_task`                                      |
| **记忆与召回**   | `memory`, `session_search`                                                              |
| **自动化与投递** | `cronjob`, `send_message`                                                               |

## 6.2 常用命令
CLI 命令：

```bash
hermes tools                            # 交互式管理工具集
hermes tools list                       # 查看所有工具集
hermes tools list --platform weixin     # 查看指定平台的工具集
hermes tools enable yuanbao             # 启用 yuanbao 工具集
hermes tools disable yuanbao            # 禁用 yuanbao 工具集
```

斜杠命令：

```bash
/tools [list|disable|enable] [name...]  # 查看或管理可用工具
/toolsets                               # 列出可用工具集
```

## 6.3 终端后端
终端工具支持多种后端，用于在本机、容器、远程主机或云端环境中执行命令。

### 6.3.1 后端类型
| 后端          | 说明                            | 适用场景               |
| ------------- | ------------------------------- | ---------------------- |
| `local`       | 在本机直接执行命令（默认）      | 本地开发、可信任务     |
| `docker`      | 在 Docker 容器中执行命令        | 隔离运行、可复现环境   |
| `ssh`         | 通过 SSH 在远程主机执行命令     | 远程服务器、沙箱主机   |
| `singularity` | 高性能计算集群容器              | 集群计算、无 root 权限 |
| `modal`       | 在 Modal 云端沙箱中执行命令     | 无服务器、弹性扩展     |
| `daytona`     | 在 Daytona workspace 中执行命令 | 持久化云端开发环境     |

### 6.3.2 配置示例
Docker 后端：

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
```

SSH 后端：

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

# 7. MCP
MCP 让 Agent 连接到外部工具服务器。

## 7.1 MCP 服务器配置
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

常用配置项：

| 配置项                         | 说明                                  |
| ------------------------------ | ------------------------------------- |
| `timeout`                      | 工具调用超时时间                      |
| `connect_timeout`              | 初始连接超时时间                      |
| `enabled`                      | 是否启用该 server                     |
| `supports_parallel_tool_calls` | 若为 true，该服务器的工具可并发运行   |
| `tools`                        | 按服务器过滤工具及实用工具策略        |
| `auth`                         | 若为 oauth 可启用带 PKCE 的 OAuth 2.1 |

`tools` 配置项：

| 配置项      | 说明                                         |
| ----------- | -------------------------------------------- |
| `include`   | 工具白名单，指定允许注册的 MCP 工具          |
| `exclude`   | 工具黑名单，指定不允许注册的 MCP 工具        |
| `resources` | 启用/禁用 `list_resources` + `read_resource` |
| `prompts`   | 启用/禁用 `list_prompts` + `get_prompt`      |

若 `include` 和 `exclude` 同时配置，则 `include` 优先。

示例：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  project-fs:
    command: "npx"
    args: ["-y", "@mcp/server-filesystem", "/home/user/my-project"]
    tools:
      include: [read_file, list_directory]
      resources: true
      prompts: false

  company_api:
    url: "https://mcp.internal.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer, refund_payment]
```

## 7.2 常用命令
```bash
hermes mcp list              # 列出已配置的服务器
hermes mcp test <name>       # 测试连接
hermes mcp configure <name>  # 管理服务器中的工具启用状态
hermes mcp remove <name>     # 移除服务器

/reload-mcp                  # 重新加载 MCP 服务器
```

# 8. Skills
Skills 是 Agent 在需要时可以按需加载的知识文档。每个已安装的 skill 都自动作为斜杠命令可用。

## 8.1 Skill 格式与配置
### 8.1.1 `SKILL.md` 格式
`SKILL.md` 由 YAML frontmatter 和 Markdown 正文组成：

frontmatter 字段：

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

frontmatter 示例：

```yaml
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    config:
      - key: my.setting
        description: What this controls
        default: value
        prompt: Prompt for setup
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get a key from https://developers.google.com/tenor
    required_for: full functionality
---
```

Skill 加载时，Hermes 会从 `config.yaml` 的 `skills.config` 下解析 `metadata.hermes.config` 声明的设置并注入上下文，Agent 可以直接看到已配置的值。

`required_environment_variables` 中已配置的环境变量自动传递到 `execute_code` 和 `terminal` 沙箱，Skill 的脚本可以直接使用对应环境变量。

### 8.1.2 附件输出与投递指令
附件输出：

Skill 或 Agent 需要发送图片、音频、视频或文档时，可以在回复里写本地文件路径。Gateway 会识别这些路径，把对应文件作为聊天平台附件发送。

| 写法               | 用法                             |
| ------------------ | -------------------------------- |
| 裸文件路径         | 直接写文件的绝对路径或 `~/` 路径 |
| `MEDIA:<文件路径>` | 明确标记一个需要投递的媒体文件   |

路径需要指向实际存在的文件。路径写在代码块或行内代码中时，Gateway 会保留为普通文本。

媒体投递指令：

| 指令                 | 作用范围               | 投递结果                 |
| -------------------- | ---------------------- | ------------------------ |
| `[[audio_as_voice]]` | 同一条回复中的音频路径 | 支持的平台按语音消息发送 |
| `[[as_document]]`    | 同一条回复中的图片路径 | 将图片按文件附件发送     |

内部投递指令可以放在同一条回复的任意位置，Gateway 会在投递前移除这些指令。

```text
[[audio_as_voice]]
/home/user/.hermes/cache/reply.ogg

[[as_document]]
/home/user/screenshots/diagram.png
```

## 8.2 Skill 目录结构
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
└── devops/
    └── deploy-k8s/
        ├── SKILL.md
        └── references/
```

也可以配置外部 Skill 目录：

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

如果本地目录和外部目录有同名 Skill，本地版本优先。

## 8.3 常用命令
```bash
hermes skills list                # 列出已安装的技能
hermes skills browse              # 浏览技能
hermes skills search my-skill     # 搜索技能
hermes skills install my-skill    # 通过 ID 安装技能
hermes skills install https://share.chat/SKILL.md  # 通过 URL 安装技能（单文件 SKILL.md）
hermes skills uninstall my-skill  # 卸载技能
hermes skills config              # 管理技能配置

/skills                           # 管理技能
/learn <anything>                 # 从目录、URL、文字材料或最近工作流提炼 Skill
```

## 8.4 Skill 捆绑包
Skill 捆绑包用于把多个 Skill 组合到同一个斜杠命令下。当运行 `/<bundle-name>` 时，会同时加载捆绑包中的多个 Skill，适合固定组合使用的重复任务。

捆绑包声明在 `~/.hermes/skill-bundles/<slug>.yaml`。

| 字段          | 说明                                                 |
| ------------- | ---------------------------------------------------- |
| `name`        | 显示名称；默认使用文件名主干                         |
| `description` | 简短说明                                             |
| `skills`      | 必填，非空列表；Skill 名称或相对于 Skills 目录的路径 |
| `instruction` | 可选；加载这些 Skill 时追加的额外指令                |

示例：

```yaml
name: backend-dev
description: Backend feature workflow
skills:
  - github-code-review
  - test-driven-development
instruction: |
  Review changes and run the project test workflow.
```

捆绑包和单个 Skill 重名时，优先使用捆绑包。

常用命令：

```bash
hermes bundles list                    # 列出所有捆绑包
hermes bundles show backend-dev        # 查看捆绑包
hermes bundles create research         # 交互式创建捆绑包
hermes bundles create backend-dev --skill ...          # 创建捆绑包
hermes bundles create backend-dev --skill ... --force  # 覆盖现有捆绑包
hermes bundles delete backend-dev      # 删除捆绑包
hermes bundles reload                  # 重新扫描 skill-bundles 目录

/bundles                               # 会话内列出捆绑包
```

## 8.5 Agent-Managed Skills (skill_manage tool)
Agent 可以通过 `skill_manage` 工具创建、修改和删除自己的技能。

| 动作          | 用途                             |
| ------------- | -------------------------------- |
| `create`      | 从零创建一个新技能               |
| `patch`       | 对现有技能做针对性修改，优先使用 |
| `edit`        | 整体重写技能                     |
| `delete`      | 删除技能                         |
| `write_file`  | 添加或更新支持文件               |
| `remove_file` | 删除支持文件                     |

### 8.5.1 触发条件
Hermes 通过系统提示词和 `skill_manage` 工具说明指导 Agent 何时调用 `skill_manage`。

常见触发条件：

| 场景        | 触发条件                                                               |
| ----------- | ---------------------------------------------------------------------- |
| 创建        | 完成复杂任务、解决棘手错误、发现可复用流程，或用户要求记住某个流程     |
| 更新        | 已加载 Skill 缺步骤、命令错误、过时，或本轮新增经验属于已有 Skill 范围 |
| `/learn`    | 用户使用 `/learn <anything>` 提炼 Skill                                |
| 后台 review | 工具调用迭代数达到 `skills.creation_nudge_interval` 后 fork 后台审查   |

### 8.5.2 写入规则
更新优先级：

1. 先 patch 当前加载或查看过的 Skill
2. 再 patch 已有的宽泛 Skill
3. 需要保留较长细节时，用 `write_file` 写入 `references/`、`templates/` 或 `scripts/`
4. 没有合适现有 Skill 时，再创建覆盖同类任务的宽泛 Skill

写入位置：

- 新 Skill 写入 `~/.hermes/skills/`
- 已有 Skill 在找到的位置就地修改
- 外部 Skill 目录可写时，`skill_manage` 可以修改其中的文件

## 8.6 Curator (技能维护)
Curator 在后台维护 Agent 创建的技能，记录使用频率，迁移长期未使用的技能，并在启用时运行辅助模型审查。

### 8.6.1 运行机制
Curator 由 Hermes 启动或 Gateway 后台 tick 触发，也可以通过 `hermes curator run` 手动触发。

| 触发条件                           | 默认值   |
| ---------------------------------- | -------- |
| `curator.enabled` 为 `true`        | 启用     |
| 未通过 `hermes curator pause` 暂停 | 未暂停   |
| 距离上次运行超过 `interval_hours`  | 168 小时 |
| Agent 空闲超过 `min_idle_hours`    | 2 小时   |

运行阶段：

1. 自动状态迁移
   - 将超过 `stale_after_days` 未使用的技能标记为 `stale`
   - 将超过 `archive_after_days` 未使用的技能移动到 `.archive/`
2. LLM Review
   - 使用辅助模型 `auxiliary.curator` 审查技能
   - 提出保留、修补、合并或归档建议

### 8.6.2 配置
```yaml
# ~/.hermes/config.yaml
curator:
  enabled: true           # 是否启用 Curator
  interval_hours: 168     # 自动检查间隔
  min_idle_hours: 2       # Agent 空闲间隔
  stale_after_days: 30    # 多久未使用后标记为陈旧
  archive_after_days: 90  # 多久未使用后归档
  consolidate: false      # 是否启用 LLM 合并审查，默认关闭
```

### 8.6.3 Curator 常用命令
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

同样的子命令也可以通过 `/curator` 在会话中使用。

### 8.6.4 备份与回滚
Curator 运行前会把 `~/.hermes/skills/` 备份到 `~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz`。如果某次维护结果不符合预期，可以回滚。

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

### 8.6.5 Curator 处理范围
| 范围   | Skill 来源                                            |
| ------ | ----------------------------------------------------- |
| 处理   | Agent 通过 `skill_manage(action="create")` 创建的技能 |
| 处理   | 用户手写 `SKILL.md` 创建的技能                        |
| 处理   | 通过 `skills.external_dirs` 暴露给 Hermes 的外部技能  |
| 不处理 | bundled 内置技能                                      |
| 不处理 | Skills Hub 安装技能                                   |

使用 `hermes curator pin <skill-name>` 可以固定技能。固定后技能保持 `active`，不会被自动迁移、LLM 审查或 `skill_manage(action="delete")` 删除，但仍允许 `patch` 和 `edit`。

### 8.6.6 使用记录与报告
Curator 会维护一个伴随文件 `~/.hermes/skills/.usage.json` 记录每个技能的使用、查看、修补、状态、固定和归档信息：

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

每次 Curator 运行后，Hermes 会在 `~/.hermes/logs/curator/` 下写入运行报告：

```text
~/.hermes/logs/curator/
└── 20260429-111512/
    ├── run.json      # 机器可读：完整数据、统计信息、LLM 输出
    └── REPORT.md     # 人类可读：运行摘要
```

# 9. Hooks
Hook 用于在关键生命周期节点运行自定义代码。

Hermes 有三套 Hook 系统：

| 类型          | 典型用途                                                  |
| ------------- | --------------------------------------------------------- |
| Shell Hooks   | 用任意命令或脚本做轻量自动化、审计、通知和上下文注入      |
| Plugin Hooks  | 用 Python 插件做工具拦截、指标采集、防护策略和记忆召回    |
| Gateway Hooks | 在消息平台 Gateway 中监听平台、会话、Agent 和斜杠命令事件 |

## 9.1 Shell Hooks
声明：

Shell Hooks 声明在 `~/.hermes/config.yaml` 的 `hooks` 下：

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"  # 仅用于 pre/post_tool_call
      command: "~/.hermes/agent-hooks/check-tool.sh"
      timeout: 10
```

处理逻辑：

Hook 触发时，Hermes 会执行 `command` 指向的命令或脚本，把 JSON 载荷通过 stdin 传入，并从 stdout 读取 JSON 响应。

## 9.2 Plugin Hooks
声明：

Plugin Hooks 写在插件目录中，通常位于 `~/.hermes/plugins/<plugin-name>/__init__.py`，并通过插件 `register(ctx)` 中的 `ctx.register_hook()` 注册：

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

处理逻辑：

Hook 触发时，Hermes 会执行注册进去的 Python 函数。

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

## 9.3 Gateway Hooks
声明：

Gateway Hooks 放在 `~/.hermes/hooks/<name>/` 目录中，`HOOK.yaml` 声明要监听的事件：

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

处理逻辑：

Gateway Hook 触发时，Hermes 会执行 `handler.py` 中的 `handle(...)` 函数：

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

## 9.4 Shell Hook 示例：弹窗提示
1. 创建脚本目录并复制脚本：

使用仓库中的 [scripts/hooks/agent-notify.py](scripts/hooks/agent-notify.py) 和 [scripts/hooks/mac-toast.swift](scripts/hooks/mac-toast.swift)。Windows / WSL 使用 PowerShell 弹窗，macOS 使用同目录的 `mac-toast` helper。

```bash
mkdir -p ~/.hermes/agent-hooks
cp scripts/hooks/agent-notify.py ~/.hermes/agent-hooks/
cp scripts/hooks/mac-toast.swift ~/.hermes/agent-hooks/
chmod +x ~/.hermes/agent-hooks/agent-notify.py
```

2. 注册 shell hook：

```yaml
# ~/.hermes/config.yaml
hooks:
  on_session_end:
    - command: "~/.hermes/agent-hooks/agent-notify.py --message 完成"
      timeout: 10
  pre_approval_request:
    - command: "~/.hermes/agent-hooks/agent-notify.py --message 请求批准"
      timeout: 10
  post_tool_call:
    - matcher: "clarify"
      command: "~/.hermes/agent-hooks/agent-notify.py --message 澄清"
      timeout: 10
```

3. 测试脚本：

```bash
printf '{}' | ~/.hermes/agent-hooks/agent-notify.py --message 完成
```

首次运行时 Hermes 会询问是否允许这个 `(event, command)` 组合。

# 10. Plugins
Hermes 提供了一套插件系统，可在不修改核心代码的情况下添加自定义工具、钩子和集成。

## 10.1 插件能做什么
不同插件类型对应不同扩展对象，常见场景如下：

| 场景          | 可扩展内容                                         | 适用说明                                      |
| ------------- | -------------------------------------------------- | --------------------------------------------- |
| 通用插件      | 工具、钩子、斜杠命令、CLI 命令、消息注入           | 给 Agent 增加本地能力、工作流入口或自动化逻辑 |
| 插件附带资源  | Skill、模板、配置、静态数据                        | 把可复用知识或资源随插件一起分发              |
| Provider 插件 | Memory provider、Context engine、Model provider    | 替换或增强记忆、上下文压缩和模型后端          |
| Gateway 平台  | 消息平台适配器                                     | 接入新的消息平台                              |
| 媒体后端      | 图像生成、视频生成、TTS 等生成后端                 | 接入外部生成服务或本地生成引擎                |
| 宿主 LLM 调用 | 使用 Hermes 当前配置的模型做一次性补全或结构化生成 | 插件内部需要轻量模型调用时使用                |

## 10.2 插件发现与启用
### 10.2.1 发现来源
Hermes 会从以下位置发现插件：

| 来源 | 路径 / 方式                          | 用途                                                                               |
| ---- | ------------------------------------ | ---------------------------------------------------------------------------------- |
| 内置 | `~/.hermes/hermes-agent/plugins/`    | 官方随 Hermes 发布的插件                                                           |
| 用户 | `~/.hermes/plugins/`                 | 用户自己的本地插件                                                                 |
| 项目 | `.hermes/plugins/`                   | 当前工作目录插件；默认不扫描，需设置 `HERMES_ENABLE_PROJECT_PLUGINS=true` 显式信任 |
| pip  | `hermes_agent.plugins` entry points  | 通过 Python 包分发的插件                                                           |
| Nix  | `services.hermes-agent.extraPlugins` | NixOS 声明式安装插件                                                               |

用户插件以独立子目录存放，最小结构如下：

```text
~/.hermes/plugins/hello-world/
├── plugin.yaml      # 插件清单：名称、版本、描述等元信息
└── __init__.py      # 定义 register(ctx)，在这里注册插件内容
```

`register(ctx)` 是通用插件的入口，用于注册工具、hooks、命令或 provider。

### 10.2.2 启用配置
Hermes 默认只发现普通插件和用户安装的 provider，不会自动启用。将插件加入 `~/.hermes/config.yaml` 的 `plugins.enabled` 后，Hermes 才会加载工具、hooks、命令或 provider：

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - my-plugin
  disabled:  # 禁用优先于启用
    - noisy-plugin
```

## 10.3 常用命令
```bash
hermes plugins                    # 交互式开关插件
hermes plugins list               # 查看已安装插件
hermes plugins install user/repo  # 从 Git 安装插件
hermes plugins update <name>      # 更新插件
hermes plugins remove <name>      # 移除插件
hermes plugins enable <name>      # 启用插件
hermes plugins disable <name>     # 禁用插件
```

# 11. 持久记忆
Hermes Agent 使用内置记忆和外部记忆 provider 保存跨会话信息。内置记忆由 Agent 通过 `memory` 工具维护，外部 provider 提供额外检索、同步和管理能力。

## 11.1 内置记忆
内置记忆存储在 `~/.hermes/memories/`：

| 文件        | 用途                                           | 字符上限                    |
| ----------- | ---------------------------------------------- | --------------------------- |
| `MEMORY.md` | Agent 的个人笔记：环境事实、项目约定、经验教训 | 2,200 字符（约 800 tokens） |
| `USER.md`   | 用户档案：用户偏好、沟通风格、期望和习惯       | 1,375 字符（约 500 tokens） |

Agent 在会话中通过 `memory` 工具新增、替换或删除记忆后，Hermes 会立即写入磁盘，新记忆从下一个会话开始生效。记忆已满时，Agent 会先整合或替换旧条目。

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

系统提示词中会显示记忆标题、容量占用和条目内容，条目之间用 `§` 节号符号分隔。

记忆相关配置：

```yaml
# ~/.hermes/config.yaml
memory:
  memory_enabled: true        # 启用持久记忆
  user_profile_enabled: true  # 启用用户档案
  memory_char_limit: 2200     # 记忆字符上限
  user_char_limit: 1375       # 用户档案字符上限
```

## 11.2 Memory 工具操作
Agent 通过 `memory` 工具管理记忆，常用动作：

| 动作         | 用途                         |
| ------------ | ---------------------------- |
| `add`        | 添加新的记忆条目             |
| `replace`    | 替换已有条目，使用子串匹配   |
| `remove`     | 删除已有条目，使用子串匹配   |
| `operations` | 批量执行多个新增、替换或删除 |

`memory` 工具没有 `read` 动作。Agent 直接从会话上下文读取已注入的记忆。

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

`/journey` 和 `hermes journey` 用于查看已保存的记忆和已学习的技能；`hermes journey list/edit/delete` 可列出、编辑或删除节点。

## 11.3 记忆管理规则
适合保存到记忆中的内容：

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

新增条目超过上限时，`memory` 工具会返回错误，并附带当前条目和容量信息。Agent 应先删除或整合旧条目，再添加新条目。

记忆系统会拒绝完全重复的条目。如果添加的内容已经存在，会返回成功，并提示未添加重复项。

记忆条目写入前会经过安全扫描。安全扫描会阻止包含提示词注入、凭证外泄、SSH 后门或不可见 Unicode 字符等风险模式的内容。

## 11.4 外部记忆提供商
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

外部记忆 provider 激活后，Hermes 会注入 provider 上下文、预取相关记忆、同步对话轮次，并添加 provider 专属工具。支持提取记忆或镜像内置记忆的 provider 会执行对应动作。

可用 provider 包括：

| Provider      | 功能                                                    | 数据存储                          |
| ------------- | ------------------------------------------------------- | --------------------------------- |
| `honcho`      | 跨会话用户建模、辩证推理、会话上下文、语义搜索          | Honcho Cloud 或自托管             |
| `mem0`        | 服务端 LLM 事实提取、语义搜索、重排序、自动去重         | Mem0 Cloud                        |
| `openviking`  | 文件系统式知识层级、分层检索、6 类记忆提取              | 自托管，本地或云端                |
| `byterover`   | CLI 持久记忆、分层知识树、分层检索、预压缩提取          | 本地或 ByteRover Cloud            |
| `hindsight`   | 知识图谱、实体解析、多策略检索、跨记忆合成              | Hindsight Cloud 或本地 PostgreSQL |
| `holographic` | 本地 SQLite 事实存储、FTS5 搜索、信任评分、HRR 代数查询 | 本地 SQLite                       |
| `retaindb`    | 混合搜索、7 种记忆类型、增量压缩                        | RetainDB Cloud                    |
| `supermemory` | 语义长期记忆、profile 召回、会话图谱导入、多容器        | Supermemory Cloud                 |

# 12. 上下文文件
Hermes Agent 会自动发现并加载项目上下文文件与 `SOUL.md`。

## 12.1 支持的上下文文件
| 文件                       | 用途                         | 发现方式                        |
| -------------------------- | ---------------------------- | ------------------------------- |
| `.hermes.md` / `HERMES.md` | 项目说明，优先级最高         | 向上遍历至 git 根目录           |
| `AGENTS.md`                | 项目指令、规范、架构说明     | 启动目录；子目录中渐进发现      |
| `CLAUDE.md`                | Claude Code 的上下文文件     | 启动目录；子目录中渐进发现      |
| `.cursorrules`             | Cursor 编码规范              | 启动目录                        |
| `.cursor/rules/*.mdc`      | Cursor 规则模块              | 启动目录                        |
| `SOUL.md`                  | 当前 Hermes 实例的人格、语气 | 只从 `HERMES_HOME/SOUL.md` 加载 |

## 12.2 上下文文件的加载
项目上下文有两种加载方式：启动时加载和渐进加载。

### 12.2.1 启动加载
会话启动时会加载上下文文件：

1. 扫描当前工作目录，依次查找 `.hermes.md` / `HERMES.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` / `.cursor/rules/*.mdc`。
2. 读取文件 (UTF-8)
3. 安全扫描
4. 截断长文本
5. 注入系统提示词

启动加载的默认截断上限是 20,000 字符。超过上限后，Hermes 保留 70% 头部和 20% 尾部，中间插入截断标记，显示字符数并建议使用文件工具：

```text
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

### 12.2.2 渐进加载
在会话进行过程中会渐进加载上下文：

1. 每次工具调用后，从参数（path、workdir、shell 命令）中提取文件路径
2. 检查该目录及最多 5 层父目录，跳过已访问的目录
3. 每个目录按优先级查找文件，只加载首个匹配项
4. 安全扫描
5. 截断 (保留前 8,000 字符并追加截断标记)
6. 内容追加到工具结果中

### 12.2.3 安全扫描
安全扫描会检查以下内容：

1. **指令覆盖** — 例如 `ignore previous instructions`、`disregard your rules`
2. **欺骗行为** — 例如 `do not tell the user`
3. **系统提示词覆盖** — 例如 `system prompt override`
4. **隐藏 HTML 注释** — 例如 `<!-- ignore instructions -->`
5. **隐藏 div 元素** — 例如 `<div style="display:none">`
6. **凭证外泄** — 例如 `curl ... $API_KEY`
7. **密钥文件读取** — 例如 `cat .env`、`cat credentials`
8. **不可见字符** — 零宽空格、双向文本覆盖符、词连接符等

命中任意威胁模式后，Hermes 会阻止加载文件，并把上下文位置替换为：

```text
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

此扫描可防范常见注入模式，但不能替代对上下文文件的人工审查。

## 12.3 `SOUL.md` 与个性
`SOUL.md` 定义 Hermes Agent 的身份与个性，存储在 `~/.hermes/SOUL.md`。Hermes 会把它拼接到系统提示词开头部分。

`SOUL.md` 适合写长期稳定的个性和沟通偏好：

- 语气
- 风格
- 直接程度
- 默认交互风格
- 不希望出现的表达习惯
- 面对不确定性、分歧、模糊情况时的处理方式

不适合写项目说明、文件路径、仓库约定、临时流程。这些应该放进 `AGENTS.md`。

`/personality` 是会话级覆盖层，用于更改或补充当前系统提示词。常用预设包括：

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

# 13. Gateway
Gateway 是 Hermes 的消息平台接入层，可以作为前台进程或后台服务运行。它负责：

- 连接消息平台
- 接收消息并转发给 Hermes Agent
- 维护每个聊天对应的会话
- 运行后台调度任务

## 13.1 常用命令
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

## 13.2 访问控制
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

私信配对用于批准未写入白名单的用户。未知用户私信机器人后会收到一次性配对码，管理员在本机执行：

```bash
hermes pairing approve telegram XKGH5N7P  # 批准配对
hermes pairing list                       # 查看配对列表
hermes pairing revoke telegram <user_id>  # 撤销配对
```

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

如果某个作用域没有配置 `allow_admin_from`，则所有用户都拥有完整斜杠命令权限。

在任意平台使用 `/whoami` 可以查看当前作用域、自己的权限层级以及可运行的斜杠命令。

## 13.3 会话管理
Gateway 会按配置文件中的会话重置策略自动重置会话：

```yaml
# ~/.hermes/config.yaml
session_reset:
  mode: both          # none | idle | daily | both
  at_hour: 4          # daily / both 使用
  idle_minutes: 1440  # idle / both 使用
  notify: true
  notify_exclude_platforms:
    - api_server
    - webhook
```

也可以在 `~/.hermes/gateway.json` 中按聊天类型或平台覆盖默认策略：

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

## 13.4 API 服务器
API 服务器把 hermes-agent 暴露为 OpenAI 兼容的 HTTP 端点。任何支持 OpenAI 格式的前端都可以连接到 hermes-agent，并把它作为后端使用。

启用 API 服务器：

```bash
hermes config set API_SERVER_ENABLED true
hermes config set API_SERVER_KEY your-secret-key
```

重启 Gateway：

```bash
hermes gateway restart
```

健康检查：

```bash
curl -s http://127.0.0.1:8642/health
# {"status": "ok", ...}

curl -s -H "Authorization: Bearer your-secret-key" http://127.0.0.1:8642/v1/models
# {"object":"list","data":[{"id":"hermes-agent", ...}]}
```

# 14. Profile
Profile 用于创建并运行多个相互隔离的 Hermes Agent 实例。

## 14.1 常用命令
```bash
hermes profile create coder                 # 创建全新 Profile
hermes profile create coder --description "负责代码修改和验证"  # 创建带描述的 Profile
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

## 14.2 使用 Profile
每个 Profile 都会自动生成同名命令别名，位置在 `~/.local/bin/<profile-name>`。例如创建 `coder` 后：

```bash
coder chat           # 启动交互式对话
coder setup          # 运行初始化 / 配置向导
coder gateway start  # 启动 Gateway 服务
coder doctor         # 检查健康状态
```

这个别名实质等价于 `hermes -p <name>`，例如 `hermes -p coder chat`。

可将 `hermes` 命令默认指向某个 Profile：

```bash
hermes profile use coder    # 默认使用 coder Profile
hermes chat                 # 现在默认使用 coder
hermes profile use default  # 恢复默认 Profile 为 default
```

## 14.3 工作原理
Profile 通过 `HERMES_HOME` 定位数据目录。运行 `coder chat` 时，包装脚本会先设置 `HERMES_HOME=~/.hermes/profiles/coder`，再启动 Hermes。

Hermes 启动后会从该目录读取和写入配置、会话、记忆、技能、状态数据库、Gateway 状态、日志和定时任务。

# 15. Cron
Hermes 通过 `cronjob` 工具管理定时任务。任务可以通过会话命令、CLI 命令或自然语言创建。

运行定时任务时，会禁用 cron 管理工具，避免递归创建定时任务。

## 15.1 创建任务
```bash
/cron add 30m "提醒我检查构建结果"
hermes cron create "every 2h" "检查服务器状态"
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

| 选项         | 说明                                             |
| ------------ | ------------------------------------------------ |
| `--script`   | 指定脚本                                         |
| `--no-agent` | 跳过 LLM，直接运行脚本；必须搭配 `--script` 使用 |
| `--workdir`  | 指定任务运行目录，并注入该目录的上下文文件       |

脚本必须放在 `~/.hermes/scripts/` 下。相对路径按 `~/.hermes/scripts/` 解析；传入绝对路径时，解析结果也必须位于该目录内。

任务存储在 `~/.hermes/cron/jobs.json`。

任务输出保存在 `~/.hermes/cron/output/{job_id}/{timestamp}.md`。

## 15.2 管理任务
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

## 15.3 调度格式
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

## 15.4 任务执行
定时任务到期后，Hermes 会：

- 启动新的 Agent 会话
- 注入任务附加的 skill
- 执行任务 prompt
- 保存任务输出
- 投递最终响应或失败错误
- 更新运行元数据和下次调度时间

## 15.5 结果投递
`deliver` 控制定时任务运行完成后，把任务的最终结果或失败错误通知发送到哪里。

常见投递目标：

| deliver                        | 说明                                   |
| ------------------------------ | -------------------------------------- |
| `origin`                       | 回到创建任务的聊天来源，消息平台默认值 |
| `local`                        | 只保存到本地文件，CLI 默认值           |
| `telegram`, `discord`, `slack` | 投递到对应平台的 home channel          |
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

如果 Agent 的最终回复以 `[SILENT]` 开头，成功运行时会抑制投递，但仍会把输出保存到本地；失败任务仍会投递错误信息。这可用于那些只有出现问题才需要报告的作业：

```text
Check if nginx is running. If everything is healthy, respond with only [SILENT].
Otherwise, report the issue.
```

## 15.6 通过 context_from 串联任务
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

# 任务 2：总结——接收任务 1 的输出作为上下文
# 从 cronjob(action="list") 获取任务 1 的 ID
cronjob(
    action="create",
    prompt="Read the previous task output and write a short Chinese summary of the top stories.",
    schedule="30 7 * * *",
    context_from="<job1_id>",
    name="AI News Summary",
)
```

`context_from` 支持单个 job ID 或多个 job ID：

| 格式         | 示例                              |
| ------------ | --------------------------------- |
| 单个上游任务 | `context_from="a1b2c3d4"`         |
| 多个上游任务 | `context_from=["job_a", "job_b"]` |

Hermes 会按列表顺序拼接多个上游输出。

运行时 Hermes 会读取上游任务最近一次完成的输出结果文件，拼接到下游任务的 prompt 前。拼接前会把每个上游输出截断至 8,000 字符（超出部分以 `[... output truncated ...]` 标记），避免 prompt 过度膨胀。

Agent 可以通过 `cronjob` 工具的 `context_from` 参数设置上游任务；也可以人工在 Dashboard 中设置 `context_from`。

`context_from` 只读取上游任务最近一次已完成输出，不等待正在运行的上游任务。如果下游必须使用上游本次结果，需要错开上下游调度时间，或把多个步骤合并到同一个 cron prompt / 脚本中串行执行。

# 16. Delegation
Hermes 通过 `delegate_task` 工具实现子 Agent 委派。`delegate_task` 用于把明确任务交给子 Agent 执行，子 Agent 使用独立上下文、受限工具集和独立终端会话。

## 16.1 单任务与并行批量
**单任务：**

```text
delegate_task(
    goal="Debug why tests fail",
    toolsets=["terminal", "file"]
)
```

**并行批量（默认最多 3 并发，可通过 `delegation.max_concurrent_children` 配置）：**

```text
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]}
])
```

顶层 Agent 调用 `delegate_task` 时默认后台运行，工具调用会立即返回包含运行状态、`delegation_id` 在内的委派元信息。

子 Agent 完成后会把结构化摘要送回对话；批量任务全部完成后按输入顺序合并返回。

子 Agent 内部再次调用 `delegate_task` 时为同步调用。

## 16.2 子 Agent 上下文
父 Agent 通过以下字段传递任务上下文：

| 字段      | 说明                                 |
| --------- | ------------------------------------ |
| `goal`    | 任务目标，必填                       |
| `context` | 额外背景，可包含错误、路径和环境约束 |

## 16.3 工具集限制
`toolsets` 参数限制子 Agent 可用工具，例如：

| toolsets                      | 适用场景             |
| ----------------------------- | -------------------- |
| `["terminal", "file"]`        | 编码、调试、文件编辑 |
| `["web"]`                     | 调研、查文档         |
| `["terminal", "file", "web"]` | 全栈任务（默认）     |

某些工具限制为子 Agent 无法使用，无论是否在 `toolsets` 中指定：

| 工具             | 限制结果                                |
| ---------------- | --------------------------------------- |
| `delegation`     | leaf 子 Agent 不可用，orchestrator 保留 |
| `clarify`        | 不可向用户提问                          |
| `memory`         | 不可写入共享持久记忆                    |
| `code_execution` | 不可使用                                |
| `send_message`   | 不可发送跨平台消息                      |

## 16.4 嵌套委派
默认委派是扁平的：父 Agent（深度 0）只能生成一层子 Agent（深度 1），子 Agent 默认是 `leaf`，不能继续委派。

配置示例：

```yaml
# ~/.hermes/config.yaml
delegation:
  max_spawn_depth: 2          # 最大子 Agent 嵌套深度
  orchestrator_enabled: true  # 是否允许子 Agent 为 orchestrator
```

调用示例：

```text
delegate_task(
    goal="Compare three review approaches",
    role="orchestrator",
)
```

# 17. Kanban
Hermes Kanban 是面向多 Agent 协作的持久工作队列，用于拆分、调度、交接和审计长期任务。

## 17.1 适用场景与核心能力
适用场景：

| 场景         | 用法                                           |
| ------------ | ---------------------------------------------- |
| 研究分流     | 并行收集信息、分析证据、写作和校验             |
| 周期性工作流 | 跨运行保留任务状态、历史输出和失败恢复信息     |
| 工程流水线   | 拆解、实现、审查、返工、合并和交付复杂工程任务 |

核心能力：

| 能力       | 说明                                     |
| ---------- | ---------------------------------------- |
| 持久状态   | 用 SQLite 保存任务、依赖、评论和执行记录 |
| Agent 交接 | 通过任务评论、依赖和输出传递上下文       |
| 人工介入   | 支持评论、阻塞、解锁和改派               |
| 审计记录   | 保存任务生命周期、worker 心跳和运行结果  |

## 17.2 Kanban 架构
Kanban 由控制层、状态层和执行层组成。用户通过 CLI、Gateway 或 Dashboard 操作看板；状态层保存任务图；worker 读取任务并把结果写回看板。

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
| kanban.db    | -----------> | DISPATCHER              |
| SQLite (WAL) |              | recompute READY         |
+--------------+              | claim and spawn worker  |
      ^                       +-------------------------+
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

## 17.3 Kanban 核心概念
| 概念       | 说明                                             |
| ---------- | ------------------------------------------------ |
| Board      | 独立任务队列，拥有自己的 SQLite 数据库、日志目录 |
| Task       | 基本工作单元，包含标题、正文、状态、指派人等     |
| Link       | Task 之间的依赖关系                              |
| Worker     | 执行 Task 的独立 Hermes profile 进程             |
| Dispatcher | 推进就绪任务、认领任务并启动 worker              |

默认 board 的数据库位于 `~/.hermes/kanban.db`。命名 board 的数据库位于 `~/.hermes/kanban/boards/<slug>/kanban.db`。

Task 状态：

| 状态        | 说明                                                                 |
| ----------- | -------------------------------------------------------------------- |
| `triage`    | 待规格化 / 待拆解，通常还需要补充任务描述、边界或子任务结构          |
| `todo`      | 已创建但尚未满足运行条件，通常在等待父任务完成或归档                 |
| `ready`     | 已满足运行条件，可以被认领；自动调度通常还需要存在有效 `assignee`    |
| `running`   | 已被认领，worker 正在执行                                            |
| `blocked`   | 当前无法继续执行，记录阻塞原因并等待人工输入、问题修复或外部条件变化 |
| `done`      | 已完成，是正常完成终态                                               |
| `archived`  | 已归档，不再参与正常调度；作为父任务时不会阻塞子任务                 |
| `scheduled` | 已暂停调度，后续通过 `unblock` 重新入队                              |
| `review`    | 等待验证，通常是 worker 完成 PR 或结果后交给 review agent 审查       |

Task 常用属性：

| 属性      | 说明                                                        |
| --------- | ----------------------------------------------------------- |
| Comment   | 人或 Agent 追加的持久消息，用于补充要求、答复问题和交接     |
| Event     | 创建、认领、完成、阻塞、归档、改派、编辑、心跳等审计记录    |
| Workspace | worker 执行目录，支持 `scratch`、`dir:<path>` 和 `worktree` |
| Tenant    | 同一 board 内的软分组标识，可用于过滤和继承业务上下文       |

## 17.4 协作模式
**扇出**

```text
goal
├── researcher-a
├── researcher-b
└── researcher-c
```

**流水线**

```text
researcher -> analyst -> writer -> reviewer
```

**扇入**

```text
researcher-a \
researcher-b  -> reviewer / aggregator
researcher-c /
```

**人工介入**

```text
worker -> block(reason) -> 用户评论 -> unblock -> worker
```

**长期运行日志**

```text
profile + workspace -> task run -> comment/event/output -> next run
```

**批量对象作业**

```text
task: object-1 -> assignee=manager, workspace=dir:~/objects/1/
task: object-2 -> assignee=manager, workspace=dir:~/objects/2/
task: object-n -> assignee=manager, workspace=dir:~/objects/n/
```

## 17.5 任务分解与编排
任务分解用于把 `triage` task 拆成可调度的子任务图：

- Decomposer 读取 `triage` task 和可用 profile 描述，创建子任务和依赖关系
- 原始 `triage` task 变成 root task，子任务完成后 root task 进入 `ready`
- root task 指派给 `kanban.orchestrator_profile`，用于汇总、验收或继续追加任务

触发方式：

- 自动：开启 `kanban.auto_decompose` 后自动处理 `triage` task
- 手动：在 Dashboard 点 Decompose，或运行 `hermes kanban decompose <id>`，或在聊天里使用 `/kanban decompose <id>`

相关配置：

```yaml
# ~/.hermes/config.yaml
kanban:
  auto_decompose: true        # 是否自动运行分解器
  auto_decompose_per_tick: 3  # 每轮最多拆解几个 triage 任务
  orchestrator_profile: ""    # root task 的默认 assignee；空值表示使用当前默认 profile
  default_assignee: ""        # 指派到未知 profile 时的兜底；空值表示使用当前默认 profile
```

配置编排 profile：

```bash
hermes profile create orchestrator --clone
hermes config set kanban.orchestrator_profile orchestrator
hermes config set kanban.auto_decompose true
```

在普通对话中让 `orchestrator` profile 主动管理看板时，需要启用 `kanban` toolset：

```bash
orchestrator config set toolsets '["kanban"]'
```

## 17.6 常用命令
https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-kanban

Kanban 启动准备：

```bash
hermes kanban init                     # 创建 kanban.db，已存在时不会破坏数据
hermes gateway install                 # 安装 Gateway 为服务
hermes gateway start                   # 启动 Gateway
hermes dashboard &>/dev/null & disown  # 后台运行 Dashboard 并脱离终端
```

访问 Hermes Web UI → http://127.0.0.1:9119/kanban

# 18. 案例：深度研究
## 18.1 目标与角色
深度研究案例使用多个 Profile 和 Kanban 任务图完成研究方案、检索、写作、校验、综合和报告渲染。

| 目标 | 说明                                                           |
| ---- | -------------------------------------------------------------- |
| 方案 | 接收研究需求，确认研究边界，生成研究方案                       |
| 编排 | 按章节拆解搜索、写作、校验、综合和渲染任务                     |
| 多源 | 支持公开网页、指定来源、上传文件、内部知识库、数据库和外部 API |
| 追溯 | 结构化保存来源、事实、证据链、冲突和风险                       |
| 重跑 | 支持章节级返工和单章重跑                                       |
| 交付 | 基于研究结果生成 HTML 报告                                     |

| Profile         | 职责                                                                       |
| --------------- | -------------------------------------------------------------------------- |
| `research-lead` | 接收需求、确认边界、生成方案、创建任务图、巡检任务、处理 blocked、交付汇总 |
| `searcher`      | 执行检索、来源去重、可信度评估、事实抽取、冲突识别和证据链整理             |
| `writer`        | 写作章节正文、关键发现、表格、图表说明和章节风险                           |
| `reviewer`      | 校验章节和最终结果，检查证据引用、未完成内容和返工建议                     |
| `synthesizer`   | 汇总执行摘要、核心结论、跨章节洞察、建议、全局风险和全局来源               |
| `renderer`      | 基于研究结果生成 HTML 报告和版本记录                                       |

## 18.2 端到端流程
1. 用户向 `research-lead` 提出研究需求
2. `research-lead` 确认必要研究边界，生成研究方案
3. 用户确认或修改研究方案
4. `research-lead` 创建 workspace、完整任务图和任务依赖
5. 每个章节依次执行 `searcher -> writer -> reviewer`
6. 全部章节通过校验后，`synthesizer` 综合章节结果并生成最终研究结果
7. `reviewer` 校验最终研究结果
8. 结果校验通过后，`renderer` 生成 HTML 报告
9. `research-lead` 读取报告产物，向用户交付研究结果

```text
human：提出研究需求
  |
  v
research-lead：确认边界并生成研究方案
  |
  v
human：确认研究方案
  |
  v
research-lead：创建 workspace 和任务图
  |
  +-----------------------------------+
  |                                   |
  v                                   v
searcher：搜索章节 1                  searcher：搜索章节 2
  |                                   |
  v                                   v
writer：写作章节 1                    writer：写作章节 2
  |                                   |
  v                                   v
reviewer：校验章节 1                  reviewer：校验章节 2
  |                                   |
  +-----------------------------------+
  |
  v
synthesizer：综合研究结果
  |
  v
reviewer：校验最终结果
  |
  v
renderer：渲染报告
  |
  v
research-lead：交付汇总
```

worker 遇到问题时，把统一反馈对象写入任务评论，并将当前任务置为 `blocked`。`research-lead` 默认每 180 秒巡检当前项目任务，处理 `blocked` 任务、更新约束、解除阻塞、追加返工任务或调整依赖关系。

## 18.3 workspace 目录
每个研究项目写入 `$HERMES_REAL_HOME/.hermes/workspaces/deepresearch/<project_id>/`，`project_id` 使用 `dr-YYYYMMDD-HHMMSS-<slug>` 格式。

```text
$HERMES_REAL_HOME/.hermes/workspaces/deepresearch/<project_id>/
  project.json                  # 项目状态和报告版本
  scheme.json                   # 研究方案
  sections/
    <section_id>/
      research.json             # 来源、事实、证据链、冲突和风险
      section.json              # 章节正文、关键发现、表格和图表说明
      validation.json           # 章节校验结果
  synthesis/
    synthesis.json              # 综合结论、洞察、建议和全局风险
  result/
    research_result.json        # 报告渲染前的最终研究结果
    validation.json             # 最终结果校验
  reports/
    index.json                  # 报告版本索引
    current.html                # 当前 HTML 报告
    v001.html                   # 第 1 版 HTML 报告
    v002.html                   # 第 2 版 HTML 报告
```

## 18.4 `research-lead`
### 18.4.1 职责
负责研究项目入口、边界确认、方案生成、workspace 管理、Kanban 任务创建、周期巡检、blocked 处理和交付汇总

直接修改范围只包括 `project.json`、`scheme.json`、任务评论、任务约束和任务依赖。

不直接修改 `sections/`、`synthesis/`、`result/` 或 `reports/` 下由 worker 负责生成的业务产物。

### 18.4.2 依赖
- Toolsets：`file`、`kanban`、`terminal`
- Skills：`deepresearch-orchestrator`

### 18.4.3 阶段
- 研究准备
  - 输入：用户研究需求、已有上下文、用户补充边界
  - 输出：`project.json`、`scheme.json`
  - 步骤：
    - 接收研究需求
    - 确认必要研究边界
    - 生成 `project.json`
    - 生成 `scheme.json`
  - 执行规则：
    - 只确认会影响研究方案的边界
    - 用户明确不限定的边界不得反复追问
    - 研究方案确认前不得启动搜索与证据整理任务
    - 用户确认和范围变更同步更新到项目文件和相关任务约束
- 完整任务图创建
  - 输入：`scheme.json`
  - 输出：项目目录、完整任务图、任务依赖关系
  - 步骤：
    - 读取 `scheme.json`
    - 创建项目目录
    - 为每个规划章节创建搜索、章节写作和章节校验任务
    - 创建综合、结果校验和报告渲染任务
    - 建立完整依赖关系
  - 执行规则：
    - 每个任务必须包含 `project_id`、`workspace_path`、`task_type`、`assignee`、`skills`、`inputs`、`outputs`、`objective`、`constraints`、`acceptance_criteria` 和 `attempt`
    - 研究方案确认后一次创建完整任务图
    - 章节任务依赖链固定为 `search -> section_write -> section_review`
    - 综合任务依赖全部章节的 `section_review`
    - 结果校验任务依赖 `synthesis`
    - 报告渲染任务依赖 `result_review`
    - 每个 worker 任务必须在 `kanban_create.skills` 中写入对应 worker profile 的专属 skill
    - 专属 skill 映射固定为：
      - `search` -> `searcher` -> `deepresearch-searcher`
      - `section_write` -> `writer` -> `deepresearch-writer`
      - `section_review` -> `reviewer` -> `deepresearch-reviewer`
      - `synthesis` -> `synthesizer` -> `deepresearch-synthesizer`
      - `result_review` -> `reviewer` -> `deepresearch-reviewer`
      - `report_render` -> `renderer` -> `deepresearch-renderer`
    - 完整任务图创建完成后，`project.json.stage` 更新为 `dispatching`
- 周期巡检
  - 输入：当前项目的 Kanban 任务、状态变化任务评论、状态变化任务产物、用户补充信息
  - 输出：项目进度状态、blocked 任务清单、更新后的项目文件
  - 步骤：
    - 读取 `project.json.monitoring`
    - 查看当前项目的 `done`、`running`、`ready`、`todo` 和 `blocked` 任务
    - 对已通过的章节校验结果登记章节通过状态
    - 检查综合、结果校验和报告渲染任务是否按依赖正常推进
    - 更新 `project.json.stage`
    - 更新 `project.json.monitoring`
  - 执行规则：
    - 默认常规巡检间隔为 180 秒
    - 周期巡检只负责查看和记录任务推进情况，不为正常成功路径创建新任务
    - 周期巡检在当前会话里通过 `sleep 180` 控制两轮之间的等待时间
    - `project.json.stage` 必须与当前主阶段一致
    - 完整任务图创建完成后持续巡检，直到交付完成或用户明确暂停、停止项目
    - 每轮常规巡检最多读取一次任务列表
    - 常规巡检只展开读取状态变化任务、`blocked` 任务和报告交付相关任务的评论与产物
    - 章节校验通过后，将对应 `section_id` 写入 `project.json.monitoring.passed_section_ids`
    - 无状态变化且仍有 `running`、`ready` 或 `todo` 任务时，只更新状态摘要
    - 无状态变化且仍有 `running`、`ready` 或 `todo` 任务时，在当前会话内默认 `sleep 180` 秒，再执行下一轮常规巡检
    - 无状态变化时不得立即进入下一轮常规巡检
    - 无状态变化时不得结束项目监督
    - 发现 `blocked` 任务后立即进入 blocked 处理，不等待用户再次提醒
    - 发现报告已生成且结果满足交付条件后立即进入交付汇总
- blocked 处理
  - 输入：blocked 任务、任务评论、相关产物、用户补充信息
  - 输出：补充约束、返工任务、调整后的依赖关系、解除阻塞动作
  - 步骤：
    - 读取 blocked 任务评论和相关产物
    - 判断问题属于补充输入、约束调整、继续原任务还是上游返工
    - 需要用户回答时，在当前会话中向用户提问并记录答复
    - 只需补充输入或约束时，更新 `scheme.json`、任务约束或项目文件
    - 当前 blocked 任务拿到补充信息后可继续时，优先解除阻塞继续由原 profile 处理
    - 需要新的执行工作时，创建对应 worker 的最小返工任务并调整受影响依赖
  - 执行规则：
    - 反馈必须使用统一反馈格式
    - 只有 worker 任务进入 `blocked`
    - 用户提问只发生在 `research-lead` 当前会话中
    - blocked 处理只做编排和交接，不代替任何 worker 执行业务工作
    - 需要检索、补证、重写、重校验、重综合或重渲染时，必须交回对应 profile
    - 同一个 blocked 任务能继续执行时优先解除阻塞继续
    - 解除阻塞前先把补充信息写入任务评论或任务约束，确保原 profile 有完整上下文
    - 问题来自已完成上游任务的产物时，不直接修改该产物；创建对应阶段的最小返工任务，并使用 `retry_of_task_id` 指向原任务
    - 需要重跑上游阶段时，只创建受影响范围内的最小返工任务，并把下游依赖改挂到返工任务上
    - 返工任务的 `assignee` 和 `skills` 必须继续使用固定映射，不能改由 `research-lead` 自己执行
    - 除 `project.json`、`scheme.json`、任务评论、任务约束和任务依赖外，不直接编辑 worker 产物文件
    - 单个 blocked 任务处理结束后立即回到周期巡检
    - 同一轮中存在多个 blocked 任务时，按影响范围依次处理
- 交付汇总
  - 输入：`result/research_result.json`、`result/validation.json`、`reports/index.json`、`reports/current.html`
  - 输出：交付摘要、报告路径、版本记录路径、剩余风险
  - 步骤：
    - 检查结果校验状态和报告文件
    - 汇总剩余风险
    - 向用户汇总研究结果
    - 更新 `project.json.stage`
  - 执行规则：
    - 结果校验未通过或报告未生成时，不得完成交付
    - `project.json.stage` 只有在交付完成时才能更新为 `completed`
    - 交付摘要只汇总项目状态、报告路径、版本记录路径和剩余风险

### 18.4.4 文件格式
`project.json` 字段：
- `project_id`：研究项目编号，格式为 `dr-YYYYMMDD-HHMMSS-<slug>`
- `workspace_path`：项目 workspace 路径
- `stage`：当前研究业务阶段，取值为 `preparing`、`dispatching`、`searching`、`writing`、`reviewing`、`synthesizing`、`validating`、`rendering`、`delivering`、`completed`
- `current_report_version`：当前报告版本，取值为 `null` 或 `vNNN`
- `monitoring`：巡检状态
  - `passed_section_ids`：已通过章节校验的章节编号列表
  - `last_seen_task_status_digest`：上一轮任务状态摘要

`scheme.json` 字段：
- `research_goal`：研究目标和最终需要回答的问题
- `key_questions`：必须回答的关键问题
- `scope`：研究边界与约束，包括研究范围、排除项和口径限制
- `assumptions`：可选，执行研究时默认采用的前提假设
- `methodology`：可选，分析方法，如 SWOT、PEST、对比分析、案例研究、定量分析等
- `search_strategy`：检索方法与来源筛选标准，包括检索范围、来源类型优先级、可信度与时效性要求
- `known_sources`：已知要查阅的具体数据库、文档、平台或内部知识库清单
- `outline`：章节结构、章节目标和章节证据要求
  - `section_id`：章节编号，格式为 `sNNN`
  - `title`：章节标题
  - `objective`：章节目标
  - `key_questions`：本章必须回答的关键问题
  - `evidence_requirements`：本章证据要求
- `deliverables`：最终交付内容，包括 HTML 报告、执行摘要、表格、图表和数据附录
- `acceptance_criteria`：验收标准，包括问题覆盖、证据链完整性、引用有效性和格式要求
- `risk_boundary`：输出结论时必须说明的限制、不确定性和适用边界

### 18.4.5 子任务契约
- `project_id`：研究项目编号
- `section_id`：章节编号，仅章节任务需要，格式为 `sNNN`
- `workspace_path`：项目 workspace 路径
- `task_type`：任务类型，取值为 `search`、`section_write`、`section_review`、`synthesis`、`result_review`、`report_render`
- `assignee`：负责执行的 profile
- `skills`：当前任务强制加载的 skill 列表，通过 `kanban_create.skills` 写入
- `attempt`：当前任务尝试次数，首轮为 `1`
- `retry_of_task_id`：可选，重跑任务对应的原任务编号
- `inputs`：输入文件或目录，使用项目 workspace 内相对路径
- `outputs`：输出文件或目录，使用项目 workspace 内相对路径
- `dependencies`：前置任务编号
- `objective`：任务目标
- `constraints`：执行约束
- `acceptance_criteria`：验收条件

### 18.4.6 反馈格式
- `reason`：触发原因
- `help_needed`：当前任务需要的帮助
- `affected_section_ids`：影响章节
- `question_to_answer`：待回答问题
- `suggested_action`：建议动作
- `required_user_input`：是否需要用户确认，取值为 `true` 或 `false`

## 18.5 `searcher`
### 18.5.1 职责
负责按章节目标执行公开网页、指定站点、上传文件、内部知识库、数据库和外部 API 检索，并完成来源评估、事实抽取、冲突识别和证据链整理

### 18.5.2 依赖
- Toolsets：`web`、`browser`、`file`
- MCP：可选内部知识库、数据库、外部 API
- Skills：`deepresearch-searcher`

联网搜索工具集配置：

相关环境变量写入 `~/.hermes/.env`。

`web` toolsets：https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search
  - Tavily：https://app.tavily.com/ -> TAVILY_API_KEY
  - Firecrawl：https://www.firecrawl.dev/ -> FIRECRAWL_API_KEY
  - DuckDuckGo：hermes chat -q '帮我配置 DuckDuckGo 搜索后端，并测试是否能正常使用'

`browser` toolsets：https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
  - hermes chat -q '帮我配置 browser 工具集，并测试是否能正常使用'

### 18.5.3 阶段
- 搜索与证据整理
  - 输入：`scheme.json`、`section_id`、`workspace_path`
  - 输出：`sections/<section_id>/research.json`
  - 步骤：
    - 读取 `scheme.json` 的 `outline` 中对应章节
    - 生成章节搜索计划
    - 执行检索和网页读取
    - 评估来源并抽取事实
    - 整理证据链、冲突和风险
    - 必要时反馈证据缺口
  - 执行规则：
    - 章节目标和证据要求通过 `section_id` 从 `scheme.json` 的 `outline` 读取
    - 搜索计划必须遵守 `scheme.json` 的 `scope`、`search_strategy`、`known_sources` 和章节证据要求
    - 来源优先级为官方文件、一手数据、学术论文、行业报告、主流媒体、公司官网、二手转载、社媒内容
    - 内部知识库不伪装成公开来源
    - `sections/<section_id>/research.json` 包含候选来源、可引用来源、来源评估、可复核事实、证据链、冲突信息和风险说明
    - 候选来源必须记录检索渠道、原始标题、URL 或文档编号、摘要片段和召回信息
    - 公开网页候选来源必须记录最终 URL
    - 内部知识库候选来源必须记录文档编号和片段定位
    - 可引用来源必须包含章节内唯一来源编号、标题、URL 或文档编号、发布时间、来源类型和摘要
    - 来源评估必须记录可信度、相关性、时效性、偏差风险和可用事实
    - 可复核事实不保存大段原文
    - 不得用低可信来源填补关键证据缺口
    - 关键问题和证据要求已满足时，当前任务成功时先保存 `sections/<section_id>/research.json`，再完成当前任务
    - 检索或证据不足时，先保存当前已成立的 `sections/<section_id>/research.json`，再使用统一反馈格式记录缺口并阻塞当前任务
    - 需要用户判断时，由 `research-lead` 在当前会话中向用户提问
    - 不创建返工任务或下游任务

### 18.5.4 文件格式
`sections/<section_id>/research.json` 字段：
- `section_id`：章节编号，格式为 `sNNN`
- `search_plan`：章节搜索计划
  - `queries`：检索词
  - `source_types`：目标来源类型，取值同 `sources.source_type`
  - `constraints`：检索约束
- `candidate_sources`：候选来源
  - `candidate_source_id`：候选来源编号，格式为 `cand-<section_id>-NNN`
  - `retrieval_channel`：检索渠道，取值为 `web`、`specified_site`、`uploaded_file`、`internal_knowledge`、`database`、`api`
  - `title`：原始标题
  - `url`：公开网页最终 URL
  - `document_id`：上传文件、内部知识库、数据库或外部 API 文档编号
  - `locator`：上传文件、内部知识库、数据库或外部 API 的片段定位信息
  - `snippet`：摘要片段
  - `retrieved_at`：召回时间，使用 ISO 8601 字符串
- `sources`：可引用来源
  - `source_id`：来源编号，格式为 `src-<section_id>-NNN`
  - `title`：标题
  - `url`：公开网页最终 URL
  - `document_id`：上传文件、内部知识库、数据库或外部 API 文档编号
  - `locator`：上传文件、内部知识库、数据库或外部 API 的片段定位信息
  - `published_at`：发布时间，使用 ISO 8601 字符串或 `null`
  - `source_type`：来源类型，取值为 `official`、`primary_data`、`paper`、`industry_report`、`mainstream_media`、`company_site`、`secondary_repost`、`social_media`、`uploaded_file`、`internal_knowledge`、`database`、`api`
  - `summary`：摘要
- `source_evaluations`：来源评估
  - `source_id`：来源编号
  - `credibility`：可信度，取值为 `high`、`medium`、`low`、`unknown`
  - `relevance`：相关性，取值为 `high`、`medium`、`low`、`unknown`
  - `recency`：时效性，取值为 `high`、`medium`、`low`、`unknown`
  - `bias_risk`：偏差风险，取值为 `high`、`medium`、`low`、`unknown`
  - `usable_fact_ids`：可用事实编号
- `facts`：可复核事实
  - `fact_id`：事实编号，格式为 `fact-<section_id>-NNN`
  - `text`：可复核事实内容
  - `source_ids`：来源编号
  - `evidence_chain_ids`：证据链编号
- `evidence_chains`：证据链
  - `evidence_chain_id`：证据链编号，格式为 `ev-<section_id>-NNN`
  - `claim`：关键判断
  - `fact_ids`：事实编号
  - `source_ids`：来源编号
- `conflicts`：冲突信息
  - `conflict_id`：冲突编号，格式为 `conflict-<section_id>-NNN`
  - `description`：冲突说明
  - `source_ids`：来源编号
- `risks`：风险说明
  - `risk_id`：风险编号，格式为 `risk-<section_id>-NNN`
  - `description`：风险说明
  - `applies_to`：适用对象
- `gaps`：证据缺口
  - `gap_id`：缺口编号，格式为 `gap-<section_id>-NNN`
  - `description`：缺口说明
  - `required_evidence`：所需证据

## 18.6 `writer`
### 18.6.1 职责
负责把章节证据转成章节正文、关键发现、表格、图表说明和章节风险说明

### 18.6.2 依赖
- Toolsets：`file`
- Skills：`deepresearch-writer`

### 18.6.3 阶段
- 章节写作
  - 输入：`scheme.json`、`section_id`、`workspace_path`、当前章节的 `sections/<section_id>/research.json`
  - 输出：`sections/<section_id>/section.json`
  - 步骤：
    - 读取 `scheme.json` 的 `outline` 中对应章节
    - 整理章节写作要点和关键发现候选
    - 写作章节正文、表格、图表说明和章节风险说明
    - 保存 `sections/<section_id>/section.json`
  - 执行规则：
    - 写作要点必须对应已确认大纲节点
    - 不得把未验证信息列为关键发现
    - 每条关键判断必须关联 `evidence_chains`
    - 正文段落、表格和图表必须分别记录 `source_ids`
    - `evidence_chains.source_ids` 必须能对应到 `sources.source_id`
    - 章节正文不得新增无来源事实
    - 章节风险说明必须覆盖证据不足、口径差异、时效性不足、样本偏差和适用边界
    - 未完成内容不得进入 `sections/<section_id>/section.json`
    - 当前任务成功时先保存 `sections/<section_id>/section.json`，再完成当前任务
    - 证据不足、证据链断裂或需要补充资料时，使用统一反馈格式记录问题并阻塞当前任务
    - 需要用户判断时，由 `research-lead` 在当前会话中向用户提问
    - 不创建返工任务或下游任务

### 18.6.4 文件格式
`sections/<section_id>/section.json` 字段：
- `section_id`：章节编号，格式为 `sNNN`
- `title`：章节标题
- `objective`：章节目标
- `key_findings`：关键发现
  - `finding_id`：关键发现编号
  - `text`：关键发现内容
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `body`：章节正文段落
  - `block_id`：正文段落编号
  - `heading`：段落小标题
  - `text`：段落正文
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `tables`：表格
  - `title`：表格标题
  - `columns`：列名
  - `rows`：行数据
  - `source_ids`：来源编号
- `charts`：图表说明
  - `title`：图表标题
  - `chart_type`：图表类型，取值为 `bar`、`line`、`pie`、`scatter`、`area`、`other`
  - `description`：图表说明
  - `data`：图表数据
  - `source_ids`：来源编号
- `evidence_chains`：章节证据链
  - `evidence_chain_id`：证据链编号
  - `claim`：关键判断
  - `fact_ids`：事实编号
  - `source_ids`：来源编号
- `risks`：章节风险说明
  - `risk_id`：风险编号
  - `description`：风险说明
  - `applies_to`：适用对象
- `source_ids`：章节引用来源编号

## 18.7 `reviewer`
### 18.7.1 职责
负责章节校验、研究结果校验、证据引用检查、未完成内容检查和返工建议

### 18.7.2 依赖
- Toolsets：`file`
- Skills：`deepresearch-reviewer`

### 18.7.3 阶段
- 章节校验
  - 输入：`scheme.json`、`section_id`、`workspace_path`、当前章节的 `sections/<section_id>/research.json`、`sections/<section_id>/section.json`
  - 输出：`sections/<section_id>/validation.json`
  - 步骤：
    - 检查章节是否对应已确认大纲节点
    - 检查正文、关键发现和证据链完整性
    - 检查 `source_id`、公开来源 URL 和内部知识库来源类型
    - 生成校验结果和返工反馈
  - 执行规则：
    - 章节正文不能为空
    - 每章至少包含一条关键发现和一条证据链
    - 证据链引用的 `fact_id` 必须存在
    - 证据链引用的 `source_id` 必须存在
    - 公开来源必须提供 HTTP URL
    - 内部知识库来源必须标记来源类型
    - 缺少输入文件、章节数据、引用断裂或内容未完成时，且不需要用户判断，校验状态记为 `failed`
    - 只有需要用户判断或外部授权时，校验状态记为 `blocked`
    - 校验通过时先保存 `sections/<section_id>/validation.json`，再完成当前任务
    - 校验失败时，先保存 `sections/<section_id>/validation.json`，再通过 Kanban 评论记录返工反馈并阻塞当前任务
    - 校验状态为 `blocked` 时，也先保存 `sections/<section_id>/validation.json`，再通过 Kanban 评论记录返工反馈并阻塞当前任务
    - 返工反馈必须能指向具体失败点
- 结果校验
  - 输入：`scheme.json`、`workspace_path`、全部章节校验结果、`synthesis/synthesis.json`、`result/research_result.json`、全局来源列表、全局证据链
  - 输出：`result/validation.json`
  - 步骤：
    - 检查所有章节校验是否通过
    - 检查全局来源列表是否保留章节来源编号
    - 检查事实、洞察、建议和章节风险说明是否与章节证据链一致
    - 检查报告渲染输入是否存在未完成内容或占位符
    - 生成校验结果和返工反馈
  - 执行规则：
    - 所有需要正文的章节都已保存
    - 所有章节校验已通过
    - 报告渲染输入不包含未完成内容或占位符
    - 缺少输入文件、缺少章节校验文件、引用断裂或存在未完成内容时，且不需要用户判断，校验状态记为 `failed`
    - 只有需要用户判断或外部授权时，校验状态记为 `blocked`
    - 校验通过时先保存 `result/validation.json`，再完成当前任务
    - 校验失败时，先保存 `result/validation.json`，再通过 Kanban 评论记录返工反馈并阻塞当前任务
    - 校验状态为 `blocked` 时，也先保存 `result/validation.json`，再通过 Kanban 评论记录返工反馈并阻塞当前任务
    - 返工反馈必须能指向具体失败点

### 18.7.4 文件格式
`sections/<section_id>/validation.json` 字段：
- `section_id`：章节编号，格式为 `sNNN`
- `status`：校验状态，取值为 `passed`、`failed`、`blocked`
- `checks`：校验项结果
  - `name`：校验项名称
  - `status`：校验项状态，取值为 `passed`、`failed`、`skipped`
  - `message`：校验说明
- `issues`：问题列表
  - `issue_id`：问题编号，格式为 `issue-NNNN`
  - `severity`：严重程度，取值为 `info`、`warning`、`error`、`blocker`
  - `path`：问题位置
  - `message`：问题说明
- `missing_items`：缺失内容
- `feedback`：返工反馈
  - `reason`：触发原因
  - `help_needed`：当前任务需要的帮助
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：是否需要用户确认，取值为 `true` 或 `false`
- `required_user_input`：是否需要用户确认，取值为 `true` 或 `false`

`result/validation.json` 字段：
- `status`：校验状态，取值为 `passed`、`failed`、`blocked`
- `checks`：校验项结果
  - `name`：校验项名称
  - `status`：校验项状态，取值为 `passed`、`failed`、`skipped`
  - `message`：校验说明
- `issues`：问题列表
  - `issue_id`：问题编号，格式为 `issue-NNNN`
  - `severity`：严重程度，取值为 `info`、`warning`、`error`、`blocker`
  - `path`：问题位置
  - `message`：问题说明
- `affected_section_ids`：受影响章节编号
- `feedback`：返工反馈
  - `reason`：触发原因
  - `help_needed`：当前任务需要的帮助
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：是否需要用户确认，取值为 `true` 或 `false`
- `required_user_input`：是否需要用户确认，取值为 `true` 或 `false`

## 18.8 `synthesizer`
### 18.8.1 职责
负责跨章节综合，生成执行摘要、核心结论、跨章节洞察、建议和全局风险，合并章节来源，并组装研究结果

### 18.8.2 依赖
- Toolsets：`file`
- Skills：`deepresearch-synthesizer`

### 18.8.3 阶段
- 综合与组装
  - 输入：`scheme.json`、`workspace_path`、全部章节的 `sections/<section_id>/research.json`、`sections/<section_id>/section.json` 和章节校验结果
  - 输出：`synthesis/synthesis.json`、`result/research_result.json`
  - 步骤：
    - 构建跨章节事实索引、冲突清单和风险清单
    - 生成执行摘要、核心结论、跨章节洞察和建议
    - 合并章节来源列表
    - 组装 `result/research_result.json`
  - 执行规则：
    - 只使用已保存的章节、来源、事实和证据链
    - 只使用章节文件和章节校验都已完成且通过的章节
    - 综合结论必须能回溯到章节证据链
    - 建议必须包含适用条件和风险前提
    - 跨章节冲突必须保留冲突说明
    - 全局风险写入 `synthesis/synthesis.json`
    - `result/research_result.json` 只能组装已存在的章节、来源、证据和综合结果
    - 全局来源列表保留章节来源编号，不跨章节去重
    - 不得新增事实、来源、判断或证据链
    - `result/research_result.json.sections` 按 `scheme.json.outline` 的章节顺序输出
    - 当前任务成功时先保存 `synthesis/synthesis.json` 和 `result/research_result.json`，再完成当前任务
    - 任一章节未通过校验、缺少输入文件或全局引用断裂时，使用统一反馈格式记录问题并阻塞当前任务
    - 需要用户判断时，由 `research-lead` 在当前会话中向用户提问

### 18.8.4 文件格式
`synthesis/synthesis.json` 字段：
- `executive_summary`：执行摘要
- `core_conclusions`：核心结论
  - `conclusion_id`：核心结论编号
  - `text`：核心结论内容
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `cross_section_insights`：跨章节洞察
  - `insight_id`：洞察编号
  - `text`：洞察内容
  - `section_ids`：关联章节编号
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `recommendations`：建议
  - `recommendation_id`：建议编号
  - `text`：建议内容
  - `conditions`：适用条件
  - `risks`：风险前提
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `conflicts`：跨章节冲突
  - `conflict_id`：冲突编号
  - `description`：冲突说明
  - `source_ids`：来源编号
- `global_risks`：全局风险
  - `risk_id`：风险编号
  - `description`：风险说明
  - `applies_to`：适用对象

`result/research_result.json` 字段：
- `project_id`：研究项目编号
- `scheme`：已确认 `scheme.json` 的完整快照
- `sections`：章节结果，字段结构同 `sections/<section_id>/section.json`
- `synthesis`：综合结果
- `facts`：全局可复核事实
  - `fact_id`：事实编号，格式为 `fact-<section_id>-NNN`
  - `text`：可复核事实内容
  - `source_ids`：来源编号
  - `evidence_chain_ids`：证据链编号
- `sources`：全局来源列表，由纳入综合结果的章节来源合并而成
  - `source_id`：章节来源编号，格式沿用 `src-<section_id>-NNN`
  - `title`：标题
  - `url`：公开网页最终 URL
  - `document_id`：上传文件、内部知识库、数据库或外部 API 文档编号
  - `locator`：上传文件、内部知识库、数据库或外部 API 的片段定位信息
  - `published_at`：发布时间，使用 ISO 8601 字符串或 `null`
  - `source_type`：来源类型，取值为 `official`、`primary_data`、`paper`、`industry_report`、`mainstream_media`、`company_site`、`secondary_repost`、`social_media`、`uploaded_file`、`internal_knowledge`、`database`、`api`
  - `summary`：摘要
- `evidence_chains`：全局证据链
  - `evidence_chain_id`：证据链编号
  - `claim`：关键判断
  - `fact_ids`：事实编号
  - `source_ids`：来源编号
- `risks`：全局风险
  - `risk_id`：风险编号
  - `description`：风险说明
  - `applies_to`：适用对象
- `deliverables`：交付内容

## 18.9 `renderer`
### 18.9.1 职责
负责基于研究结果确定性生成 HTML 报告和报告版本记录

### 18.9.2 依赖
- Toolsets：`file`
- Skills：`deepresearch-renderer`

### 18.9.3 阶段
- 报告渲染
  - 输入：`project.json`、`result/research_result.json`、`result/validation.json`、`workspace_path`
  - 输出：`reports/current.html`、`reports/vNNN.html`、`reports/index.json`、更新后的 `project.json.current_report_version`
  - 步骤：
    - 读取 `project.json`
    - 检查结果校验状态
    - 确保 `reports/` 目录存在
    - 首次渲染时初始化 `reports/index.json`
    - 生成可渲染报告数据
    - 确定性生成 HTML
    - 写入报告版本记录
    - 更新 `project.json.current_report_version`
  - 执行规则：
    - 结果校验通过后才能渲染
    - 报告数据不得包含未完成内容或占位符
    - 报告渲染阶段不得新增事实、来源、判断或证据链
    - 正文、表格和图表必须附相关来源链接
    - 报告必须包含执行摘要、正文、表格或图表、来源汇总、风险说明和版本信息
    - `reports/index.json` 必须记录报告格式、引用来源编号、生成时间和存储地址
    - 首次渲染时 `reports/index.json` 可以不存在，但必须在本次渲染中创建并生成 `v001`
    - 当前任务成功时先写入 HTML、`reports/index.json` 和 `project.json`，再完成当前任务
    - 结果校验未通过、`project.json` 缺失或渲染输入不完整时，使用统一反馈格式记录问题并阻塞当前任务
    - 需要用户判断时，由 `research-lead` 在当前会话中向用户提问

### 18.9.4 文件格式
`reports/index.json` 字段：
- `current_version`：当前版本编号，格式为 `vNNN`
- `versions`：报告版本列表
  - `version`：版本编号，格式为 `vNNN`
  - `file_path`：报告文件路径
  - `format`：报告格式，取值为 `html`
  - `source_ids`：报告引用来源编号
  - `generated_at`：生成时间，使用 ISO 8601 字符串
  - `note`：版本说明

`reports/current.html` 和 `reports/vNNN.html` 内容：
- 执行摘要
- 正文
- 表格或图表
- 正文、表格和图表后的相关来源链接
- 来源汇总
- 风险说明
- 版本信息

## 18.10 Profile 配置
集中创建角色 Profile，并把 deepresearch 相关 Skills 安装到对应 Profile 目录：

```bash
hermes profile create research-lead --clone --description "研究项目主编：负责深度研究项目入口、边界确认、方案生成、Kanban 任务创建、周期巡检、blocked 处理和交付汇总"
research-lead config set toolsets '["kanban"]'
cp -R deepresearch/skills/deepresearch-orchestrator ~/.hermes/profiles/research-lead/skills/research/

hermes profile create searcher --clone --description "资料研究员：负责按章节目标执行检索、来源评估、事实抽取、冲突识别、证据链整理和风险记录"
cp -R deepresearch/skills/deepresearch-searcher ~/.hermes/profiles/searcher/skills/research/

hermes profile create writer --clone --description "专题撰稿编辑：负责把章节证据转成章节正文、关键发现、表格、图表说明和章节风险说明"
cp -R deepresearch/skills/deepresearch-writer ~/.hermes/profiles/writer/skills/research/

hermes profile create reviewer --clone --description "事实核查编辑：负责章节校验、研究结果校验、证据引用检查、未完成内容检查和返工建议"
cp -R deepresearch/skills/deepresearch-reviewer ~/.hermes/profiles/reviewer/skills/research/

hermes profile create synthesizer --clone --description "综合编辑：负责跨章节综合、全局来源合并、全局风险整理和研究结果组装"
cp -R deepresearch/skills/deepresearch-synthesizer ~/.hermes/profiles/synthesizer/skills/research/

hermes profile create renderer --clone --description "报告制作编辑：负责基于研究结果确定性生成 HTML 报告和报告版本记录"
cp -R deepresearch/skills/deepresearch-renderer ~/.hermes/profiles/renderer/skills/research/
```

## 18.11 示例
```bash
research-lead chat --skills deepresearch-orchestrator

> 深入研究下 2026 年 FIFA 男子世界杯哪支队伍最有可能夺冠，写份报告
```

### 18.11.1 接入 Open-WebUI
https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui

启动 API 服务器：

```bash
research-lead config set API_SERVER_ENABLED true
research-lead config set API_SERVER_KEY 123123123123123123
research-lead config set API_SERVER_PORT 8643
```

启用 API 服务器的 kanban 工具：

```bash
research-lead config edit
```

在配置中加入：

```yaml
platform_toolsets:
  api_server:
    - hermes-api-server
    - kanban
```

启动 Gateway：

```bash
research-lead gateway install
```

验证 API 服务器是否可用：

```bash
curl -s http://127.0.0.1:8643/health
# {"status": "ok", ...}

curl -s -H "Authorization: Bearer 123123123123123123" http://127.0.0.1:8643/v1/models
# {"object":"list","data":[{"id":"hermes-agent", ...}]}
```

启动 Open-WebUI：

```bash
cd docker
docker compose up -d
```

访问 Open-WebUI：

```text
http://localhost:8080
```

可选：在 Open-WebUI 中展示 Hermes 工具调用：

```text
点击右上角用户头像
-> 管理员面板
-> 设置
-> 外部连接
-> http://localhost:8643/v1 右侧配置按钮
-> 接口类型
-> 点击切换 Chat Completions 和 Response
```
