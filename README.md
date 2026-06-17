# Hermes Agent
https://hermes-agent.nousresearch.com/

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [快速上手](#2-快速上手)
3. [配置文件与配置管理](#3-配置文件与配置管理)
4. [会话管理](#4-会话管理)
5. [Dashboard](#5-dashboard)
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

# 1. Hermes Agent 是什么
Hermes Agent 是由开源 AI 研究实验室 Nous Research 开发的开源 AI Agent 框架，可以运行在终端或消息平台（Telegram、Weixin 等）。

Hermes 的核心功能：
- **技能自进化** — Hermes 能从经验中学习。解决复杂问题后，会保存可复用的流程为 Skill，下次遇到类似任务直接加载。
- **跨会话持久记忆** — 记住用户身份与偏好、环境细节和经验教训。
- **多平台网关** — 同一个 Agent 在 Telegram、Discord、Slack 等 10+ 平台上运行，且拥有完整的工具访问权限。
- **Profile** — 运行多个互相隔离的 Hermes 实例，各有独立的配置、会话、技能和记忆。
- **可扩展** — 插件系统、MCP 服务器、自定义工具、Webhook 触发、定时任务。

# 2. 快速上手
## 2.1 安装
https://hermes-agent.nousresearch.com/docs/getting-started/installation

安装前请确认 git 可用。

安装脚本主要会做这些事：

- 拉取或更新 Hermes 源码。普通 Linux / macOS / WSL2 用户默认安装到 `~/.hermes/hermes-agent`；Windows 默认安装到 `%LOCALAPPDATA%\hermes\hermes-agent`
- 创建 Python 虚拟环境并安装依赖；必要时会安装 `uv`、Node.js、浏览器工具相关依赖
- 创建 `hermes` 命令入口，并提示把它所在目录加入 `PATH`
- 初始化数据目录。Linux / macOS / WSL2 默认是 `~/.hermes`；Windows 默认是 `%LOCALAPPDATA%\hermes`
- 仅在文件不存在时创建 `config.yaml`、`.env`、`SOUL.md`，已有配置会保留
- 交互式终端中会继续运行 setup 向导

### 2.1.1 Linux / macOS / WSL2
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 2.1.2 Windows（PowerShell）
```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

## 2.2 初次配置
```bash
hermes model  # 交互式选择模型和提供商
hermes setup  # 或者运行完整设置向导
```

API Key 存储在 `~/.hermes/.env` 文件中。

## 2.3 交互式对话
```bash
hermes        # 启动交互式对话
hermes --tui  # 使用 TUI 启动交互式对话
```

## 2.4 单次对话（非交互式）
```bash
hermes chat -q "查看系统资源占用情况"
```

适合脚本调用或一次性任务。

## 2.5 常用快捷键
| 快捷键          | 功能                             |
| --------------- | -------------------------------- |
| `Alt + V`       | 从剪贴板粘贴图像                 |
| `Ctrl + C`      | 中断当前操作                     |
| `Ctrl + D`      | 退出会话                         |
| `Ctrl + Z`      | 暂停并挂起到后台，`fg` 恢复      |
| `Alt + Enter`   | 插入新行，输入多行文本           |
| `Ctrl + J`      | 插入新行，输入多行文本           |
| `Shift + Enter` | 插入新行，需终端支持独立按键序列 |

## 2.6 更新
https://hermes-agent.nousresearch.com/docs/getting-started/updating

```bash
hermes update
```

## 2.7 卸载
https://hermes-agent.nousresearch.com/docs/getting-started/updating#uninstalling

```bash
hermes uninstall
```

### 2.7.1 手动清理
如果需要完全清理所有数据：

```bash
rm -rf ~/.hermes
```

# 3. 配置文件与配置管理
https://hermes-agent.nousresearch.com/docs/user-guide/configuration

## 3.1 配置目录结构
```
~/.hermes/
├── config.yaml     # 主配置文件（模型、终端、TTS、压缩等）
├── .env            # API 密钥和机密信息
├── auth.json       # OAuth 提供商凭证（Nous Portal 等）
├── SOUL.md         # 主 Agent 的身份 / 人格文件，会拼入系统提示词开头部分
├── memories/       # 持久化记忆（MEMORY.md、USER.md）
├── skills/         # 技能
├── cron/           # 定时任务
├── sessions/       # 会话
└── logs/           # 日志（errors.log、gateway.log — 密钥自动脱敏）
```

## 3.2 配置管理命令
```bash
hermes config                 # 查看当前配置
hermes config edit            # 用 $EDITOR 打开 config.yaml 编辑
hermes config set section.key value  # 直接设置某个配置项
```

会话内也可以通过斜杠命令调整部分配置：
https://hermes-agent.nousresearch.com/docs/reference/slash-commands#configuration

| 命令                           | 功能                                                                 |
| ------------------------------ | -------------------------------------------------------------------- |
| `/config`                      | 查看当前配置                                                         |
| `/model [model-name]`          | 查看或切换当前会话使用的模型                                         |
| `/personality [name]`          | 切换预设交互风格 / 人格，例如更简洁、更解释型或某个自定义风格        |
| `/reasoning [level/show/hide]` | 调整或查看模型推理级别；`show` / `hide` 控制是否显示推理相关信息     |
| `/voice [on/off/tts/status]`   | 开启、关闭或查看语音输入 / TTS 输出状态                              |
| `/yolo`                        | 切换绕过确认模式，减少工具执行确认；只建议在可信环境和低风险任务使用 |

# 4. 会话管理
https://hermes-agent.nousresearch.com/docs/user-guide/sessions

每一次与 Hermes 的对话都是一个会话（Session），系统会自动保存和索引。

## 4.1 基本操作
```bash
hermes sessions list                                    # 列出近期会话
hermes sessions browse                                  # 打开交互式会话选择器
hermes --continue                                       # 继续上次会话
hermes -c                                               # 继续上次会话的短参数
hermes --resume 20250225_143052_a1b2c3                  # 按会话 ID 恢复
hermes -r "我的项目设置"                                  # 按标题恢复
hermes sessions rename 20250225_143052_a1b2c3 "后端 API 开发"  # 重命名会话
hermes sessions delete session_id                       # 删除会话
hermes sessions prune --older-than 30                   # 清理 30 天前的旧会话
```

## 4.2 斜杠命令
https://hermes-agent.nousresearch.com/docs/reference/slash-commands#session

会话控制：

| 命令                    | 功能                                                           |
| ----------------------- | -------------------------------------------------------------- |
| `/new`                  | 开始新会话                                                     |
| `/clear`                | 清屏并开始新会话                                               |
| `/undo`                 | 撤销上一次用户/Agent 交互记录                                  |
| `/title <session_name>` | 为当前会话命名                                                 |
| `/history`              | 显示对话历史                                                   |
| `/sessions`             | 查看和管理会话                                                 |
| `/compress`             | 手动压缩上下文                                                 |
| `/stop`                 | 停止后台进程                                                   |
| `/background <prompt>`  | 在后台运行任务                                                 |
| `/goal <text>`          | 设置持续性目标。辅助评判模型检查目标是否完成，未完成则自动继续 |

## 4.3 会话存储
https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage

Hermes 主要使用 SQLite 数据库（`~/.hermes/state.db`）保存会话状态：会话元数据、完整消息历史、模型配置、token / 费用统计，以及用于跨会话搜索的 FTS5 索引。数据库采用 WAL（预写日志）模式，支持并发读取和单个写入。

早期版本使用 `~/.hermes/sessions/` 下的 JSONL 文件保存逐会话转录；当前 `state.db` 是会话查询、恢复和搜索的主要存储。

SQLite 中主要有这几张表：

| 表               | 内容                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------ |
| `sessions`       | 会话元数据：会话 ID、来源平台、用户 ID、模型配置、系统提示词、会话标题等             |
| `messages`       | 完整消息历史：所属会话、角色、正文、工具调用、工具名称、时间戳、结束原因、推理内容等 |
| `state_meta`     | 键值元数据表，用于记录状态型信息                                                     |
| `schema_version` | 数据库 schema 版本号，用于迁移判断                                                   |

Hermes 还会维护 FTS5 搜索索引表：`messages_fts` 用于英文 / 拉丁语系全文搜索，`messages_fts_trigram` 用于 CJK（中日韩）子串搜索。SQLite 中还包括 `messages_fts_data`、`messages_fts_idx`、`messages_fts_content`、`messages_fts_docsize`、`messages_fts_config` 等影子表，以及对应的 `messages_fts_trigram_*` 表。这些是 SQLite FTS5 为全文索引自动维护的内部结构，用来保存倒排索引、文档大小、配置和原始内容映射。

## 4.4 上下文压缩
当会话上下文接近模型限制时，Hermes 会自动压缩历史消息，保留关键信息并维持上下文窗口可用。

```yaml
# ~/.hermes/config.yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 当 prompt tokens 达到模型上下文窗口的 50% 时触发压缩
  target_ratio: 0.20  # 最近消息保留预算：threshold_tokens 的 20%，即默认保留约 10% 总上下文不压缩
  protect_last_n: 20  # 最少保留不压缩的最近消息数
```

也可通过 `/compress` 斜杠命令手动触发压缩。

## 4.5 会话搜索工具
https://hermes-agent.nousresearch.com/docs/user-guide/sessions#session-search-tool

Agent 内置 `session_search` 工具，用 SQLite FTS5 在过去所有会话中做全文搜索。它解决的是“我之前是不是和 Hermes 说过这件事”的问题。

Agent 被提示在用户提到过去对话，或者怀疑历史会话里有相关上下文时，先调用 `session_search` 回忆历史，而不是直接要求用户重复信息。

借助这个工具 Agent 可以先搜索命中的会话，再沿着同一个会话向前或向后翻看更多上下文。

`session_search` 没有显式 `mode` 参数，而是根据传入参数自动判断调用形态：

| 调用形态  | 参数                               | 用途                                                    |
| --------- | ---------------------------------- | ------------------------------------------------------- |
| Discovery | `query`                            | 按关键词搜索历史会话，返回最相关的若干会话              |
| Scroll    | `session_id` + `around_message_id` | 在某个命中的会话里，以指定消息为中心继续向前 / 向后翻看 |
| Browse    | 无参数                             | 按时间列出最近会话，适合用户只问“我之前在做什么”        |

Discovery 搜索结果通常包含：

- `session_id`、标题、时间、来源平台
- FTS5 命中的高亮片段
- 会话开头几条用户 / assistant 消息，用来还原任务开始时的目标
- 命中消息前后的一小段上下文
- 会话结尾几条用户 / assistant 消息，用来判断最后结论或决策
- 命中的 `message_id`，后续可用它继续 Scroll

Agent 调用 `session_search` 时，`query` 参数支持常见 FTS5 查询语法：

```text
docker deployment        # 多关键词，默认 AND
"exact phrase"           # 精确短语
docker OR kubernetes     # 布尔 OR
python NOT java          # 排除关键词
deploy*                  # 前缀匹配
```

`session_search` 常用可选输入参数：

| 参数          | 说明                                                                     |
| ------------- | ------------------------------------------------------------------------ |
| `limit`       | Discovery 返回的会话数量                                                 |
| `window`      | Scroll 时围绕锚点消息返回前后多少条消息                                  |
| `sort`        | `newest` / `oldest`，在相关性之外按时间排序                              |
| `role_filter` | 限制搜索角色；默认搜索 `user,assistant`，需要调试工具输出时可包含 `tool` |

# 5. Dashboard
https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard

Hermes 提供了一个基于浏览器的 Web 管理界面，替代手动编辑 YAML 和 CLI 命令，用于配置管理、API 密钥设置和会话监控。

## 5.1 启动与配置
```bash
hermes dashboard                       # 启动，自动打开浏览器 http://127.0.0.1:9119
hermes dashboard --port 8080           # 自定义端口
hermes dashboard --tui                 # 启用浏览器内 Chat 标签页
hermes dashboard --status              # 查看运行状态
hermes dashboard --stop                # 停止运行
hermes dashboard &>/dev/null &         # 后台运行
hermes dashboard &>/dev/null & disown  # 后台运行并脱离终端
```

# 6. Toolsets
https://hermes-agent.nousresearch.com/docs/user-guide/features/tools

工具（Tools）是 Hermes 调用外部能力的基本单元——搜索网页、执行命令、读写文件、控制浏览器等。工具按功能分组为「工具集」（Toolsets），可以按平台按需启用或禁用，从而精确控制 Agent 的能力范围。

## 6.1 基本操作
```bash
hermes tools                  # 交互式管理工具集
hermes tools list             # 查看所有工具集
hermes tools list --platform weixin  # 查看指定平台的工具集
hermes tools enable yuanbao   # 启用 yuanbao 工具集
hermes tools disable yuanbao  # 禁用 yuanbao 工具集

/tools    # 会话内查看 / 管理可用工具
/verbose  # 切换工具执行展示模式（all → verbose → off → new）
```

`/verbose` 控制工具执行过程在会话里显示多少信息：

| 模式      | 含义                                             |
| --------- | ------------------------------------------------ |
| `off`     | 只显示最终回复，不展示工具调用、日志或推理信息   |
| `new`     | 工具调用发生时显示简短的一行进度                 |
| `all`     | 显示所有工具活动，包括工具结果                   |
| `verbose` | 显示最完整细节，包括工具参数和输出，适合调试问题 |

## 6.2 工具分类
Hermes 内置的工具按用途分为以下几类：

| 类别             | 包含工具                                                 | 用途                                       |
| ---------------- | -------------------------------------------------------- | ------------------------------------------ |
| **Web**          | `web_search`, `web_extract`                              | 搜索网页、提取页面内容                     |
| **终端与文件**   | `terminal`, `process`, `read_file`, `patch`              | 执行命令、读写文件                         |
| **浏览器**       | `browser_navigate`, `browser_snapshot`, `browser_vision` | 交互式浏览器自动化，支持文本与视觉         |
| **媒体**         | `vision_analyze`, `image_generate`, `text_to_speech`     | 多模态分析与内容生成                       |
| **编排**         | `todo`, `clarify`, `execute_code`, `delegate_task`       | 任务规划、澄清需求、代码执行、委托子 Agent |
| **记忆与召回**   | `memory`, `session_search`                               | 持久化记忆、搜索历史会话                   |
| **自动化与推送** | `cronjob`, `send_message`                                | 定时任务、消息推送                         |
| **集成**         | `ha_*`, MCP 工具, `rl_*`                                 | Home Assistant、MCP 服务器、RL 训练等      |

## 6.3 终端后端
终端工具支持 7 种后端，适应不同的安全隔离和运行环境需求：

| 后端             | 说明                   | 适用场景                        |
| ---------------- | ---------------------- | ------------------------------- |
| `local`          | 在本机直接执行（默认） | 本地开发、可信任务              |
| `docker`         | 隔离容器中执行         | 安全隔离、可复现环境            |
| `ssh`            | 远程服务器执行         | 沙箱化，防止 Agent 修改自身代码 |
| `singularity`    | HPC 容器（Apptainer）  | 集群计算、无 root 环境          |
| `modal`          | 云端无服务器执行       | 弹性伸缩                        |
| `daytona`        | 云端沙箱工作区         | 持久化远程开发环境              |
| `vercel_sandbox` | Vercel 云端微虚拟机    | 部署与长期运行进程              |

选择建议：

- 默认先用 `local`，适合本机开发和可信任务
- 不信任任务内容、担心误改本机文件时，用 `docker`
- 目标环境在远程服务器上时，用 `ssh`
- HPC / 集群环境优先考虑 `singularity`
- 需要云端隔离或弹性资源时，考虑 `modal`、`daytona`、`vercel_sandbox`

切换后端：
```bash
hermes config set terminal.backend docker
```

当命令需要 sudo 权限时，终端会提示输入密码（会话内缓存）。也可以在 `~/.hermes/.env` 中设置 `SUDO_PASSWORD` 环境变量。

# 7. MCP
https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

MCP（Model Context Protocol）可以把外部工具服务器接入 Hermes。

## 7.1 添加 MCP 服务器
https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference

配置示例：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  project-fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]

  company_api:
    url: "https://mcp.internal.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

上面两个 server 分别代表两种传输方式：

| 模式  | 配置方式           | 工作方式                                                        | 适用场景                                 |
| ----- | ------------------ | --------------------------------------------------------------- | ---------------------------------------- |
| stdio | `command` + `args` | Hermes 在本机启动 MCP server 进程，通过 stdin / stdout 与其通信 | 本地文件系统、CLI 工具、开发环境里的集成 |
| HTTP  | `url`              | Hermes 连接一个已经运行的 MCP server                            | 公司内部服务、远程 API、共享的工具服务器 |

常用配置项：

| 配置项            | 说明                                        |
| ----------------- | ------------------------------------------- |
| `command`         | 本地 stdio MCP Server 的启动命令            |
| `args`            | 传给启动命令的参数                          |
| `env`             | 传给 stdio server 的环境变量                |
| `url`             | 远程 HTTP MCP Server 地址                   |
| `headers`         | 远程 HTTP 请求头                            |
| `auth: oauth`     | 仅用于 HTTP server，启用 OAuth 2.1 授权流程 |
| `enabled`         | 是否启用该 server                           |
| `timeout`         | 工具调用超时时间                            |
| `connect_timeout` | 初次连接超时时间                            |

`auth: oauth` 通常需要一次浏览器交互式授权。授权完成后，Hermes 会缓存授权结果，后续调用复用已授权 token。

可以在每个 server 下配置 `tools.include` 或 `tools.exclude`，来控制注册工具白名单或黑名单：

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

## 7.2 管理与重载
```bash
hermes mcp list                  # 列出已配置的服务器
hermes mcp test project-fs       # 测试连接
hermes mcp configure project-fs  # 管理服务器中的工具启用状态
hermes mcp remove project-fs     # 移除服务器

/reload-mcp  # 修改配置后，在会话内重载 MCP 工具
```

Hermes 启动时会自动发现 MCP 工具。修改 `mcp_servers` 配置后，用 `/reload-mcp` 重新加载；如果 MCP Server 支持动态工具变更通知，Hermes 可以自动刷新工具列表。

# 8. Skills
https://hermes-agent.nousresearch.com/docs/user-guide/features/skills

已安装的技能会以斜杠命令的形式提供。

## 8.1 基本操作
https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-skills

```bash
hermes skills list                                      # 列出已安装的技能
hermes skills browse                                    # 浏览可用的技能
hermes skills search honcho                             # 搜索技能
hermes skills install honcho                            # 通过 ID 安装技能
hermes skills install https://example.com/my-skill/SKILL.md  # 通过 URL 安装技能
hermes skills uninstall honcho                          # 卸载技能

/skills  # 会话内管理技能
```

## 8.2 技能目录结构
所有技能默认存放在 `~/.hermes/skills/`，这是 Hermes 的主技能目录，也是本地安装、Hub 安装、Agent 创建技能的写入位置。

```text
~/.hermes/skills/
├── mlops/                 # 类别目录
│   ├── axolotl/           # 技能目录
│   │   ├── SKILL.md       # 主说明文件，必需
│   │   ├── references/    # 额外参考资料
│   │   ├── templates/     # 输出模板
│   │   ├── scripts/       # 技能可调用的辅助脚本
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

`SKILL.md` 是每个技能的入口文件。`references/`、`templates/`、`scripts/`、`assets/` 都是可选目录，用来承载较长资料、固定输出格式、辅助脚本和资源文件。

可以把 Skill 粗略分成三种层级：

| 类型                                             | 例子                             | 含义                                                                 |
| ------------------------------------------------ | -------------------------------- | -------------------------------------------------------------------- |
| 普通具体 Skill                                   | `mlops/axolotl`                  | 面向某个具体工具或流程，例如 Axolotl 训练                            |
| 总括型 Skill（umbrella Skill）                   | `mlops/training`                 | 覆盖一组相关流程，把多个具体训练经验组织到一个入口下                 |
| 类别级总括型 Skill（class-level umbrella Skill） | `software-development/debugging` | 抽象到任务类别，例如“调试”这一类工作，而不是某次会话里的某个具体 bug |

`umbrella` 强调“覆盖一组相关流程”；`class-level` 强调“抽象到任务类别”。Curator 和后台 review 更偏好把零散、狭窄、只记录一次问题的 Skill 合并成这类更通用的 Skill。

## 8.3 外部技能目录
如果团队已经有共享技能目录，比如 `~/.agents/skills/` 或公司内部 repo，可以让 Hermes 额外扫描这些目录：

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
```

外部目录支持 `~` 展开和 `${VAR}` 环境变量替换。它们的行为规则：

- **只读扫描**：Hermes 会发现外部技能，但 Agent 创建或修改技能时仍然写入 `~/.hermes/skills/`
- **本地优先**：如果本地目录和外部目录有同名技能，本地版本优先
- **完整集成**：外部技能会出现在技能索引、`skills_list`、`skill_view` 和 `/skill-name` 斜杠命令中
- **路径可选**：不存在的外部目录会被静默跳过，适合跨机器共享配置

## 8.4 Agent-Managed Skills (skill_manage tool)
Hermes 可以通过 `skill_manage` 工具创建、修改和删除自己的技能。这是 Agent 的「程序记忆」：当它解决了一个有复用价值的复杂问题，就可以把流程沉淀成 Skill，下次遇到类似任务时直接加载。

触发策略主要靠提示词驱动，Hermes 会从几个位置共同推动 Agent 创建或更新技能：

| 提示词                                 | 位置                          | 作用                                                           | 注入 / 触发位置                                                                        |
| -------------------------------------- | ----------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `SKILLS_GUIDANCE`                      | `agent/prompt_builder.py`     | 指导 Agent 在复杂任务、错误修复或发现工作流后保存 / 修补 Skill | `skill_manage` 工具可用时，随主对话系统提示词注入                                      |
| Skills 列表注入提示词                  | `agent/prompt_builder.py`     | 要求 Agent 加载相关 Skill，并在发现 Skill 问题时修补           | 构建可用 Skills 列表时注入                                                             |
| `skill_manage` 工具 schema description | `tools/skill_manager_tool.py` | 在工具定义里告诉模型何时 `create`、`patch`、跳过或确认         | `skill_manage` 作为可调用工具暴露给模型时                                              |
| `_SKILL_REVIEW_PROMPT`                 | `run_agent.py`                | 后台回顾本轮对话并更新 Skill library                           | 工具调用迭代数达到 `skills.creation_nudge_interval`，回合结束后 fork 后台 review agent |

整体规则可以概括为：

- 复杂任务成功、克服错误、用户纠正后的方法有效、发现可复用流程，或用户要求记住流程时，可以创建 Skill
- 发现 Skill 过时、缺步骤、命令错误、OS 相关失败或新坑点时，应优先 `patch` 现有 Skill
- 后台 review 会优先更新当前加载的 Skill，其次更新已有 umbrella Skill，再考虑添加支持文件或创建新的 class-level umbrella Skill

`skill_manage` 常见动作：

| 动作          | 用途                                            |
| ------------- | ----------------------------------------------- |
| `create`      | 从零创建一个新技能                              |
| `patch`       | 对现有技能做小范围修改，优先使用                |
| `edit`        | 整体重写技能内容                                |
| `delete`      | 删除技能                                        |
| `write_file`  | 添加或更新 `references/`、`scripts/` 等支持文件 |
| `remove_file` | 删除支持文件                                    |

## 8.5 Curator（技能维护）
https://hermes-agent.nousresearch.com/docs/user-guide/features/curator

Curator 是 Hermes 的技能维护系统，专门管理由后台自我改进 review agent 创建并标记的本地技能。它会跟踪这些技能的查看、使用和修改频率，把长期不用的技能从 `active` 推进到 `stale`，再归档到 `~/.hermes/skills/.archive/`。

Curator 的存在是为了防止通过自我提升循环产生的技能无限累积。后台 review agent 在解决复杂问题后可能会把可复用经验保存成新的本地 Skill，并标记为 Curator 管理对象。如果不进行维护，最终会导致数十个功能相近但范围狭窄的重复技能，这些技能不仅会污染目录，还会浪费 token。

如果某个技能很重要，可以把它 pin 住。Pinned 技能有三层保护：

- Curator 不会把它自动迁移到 `stale` 或 `archived`
- Curator 的 LLM Review 会跳过它
- Agent 的 `skill_manage delete` 也不能删除它，但仍然可以 `patch` / `edit` 改进内容

### 8.5.1 运行机制
Curator 在 Hermes 启动或 Gateway 后台 tick 时检查是否满足运行条件。自动运行需要同时满足以下门槛：

- `curator.enabled` 没有被设为 `false`
- Curator 没有被 `hermes curator pause` 暂停
- 距离上次运行已经超过 `interval_hours`，默认 168 小时（7天）
- Agent 已经空闲超过 `min_idle_hours`，默认 2 小时

首次安装或还没有 `last_run_at` 记录时，Curator 会先写入当前时间作为基准，不会立刻自动运行。后续自动检查只有在上述门槛通过后，才会在后台创建一个 AIAgent 分支运行。用户也可以通过 `hermes curator run` 手动触发；手动运行会跳过时间间隔和空闲时长门槛，但仍要求 `curator.enabled` 没有被关闭。

每次实际运行都会按照两阶段执行：

1. **自动状态迁移**：不调用 LLM。只检查 Curator 管理范围内的技能；超过 `stale_after_days` (30天) 未使用的技能变成 `stale`，超过 `archive_after_days` (90天) 未使用的技能移动到 `.archive/`。
2. **LLM Review**：启动一个辅助模型任务，查看 Curator 管理范围内的技能，决定保留、修补、合并或归档。

**提示词：`CURATOR_REVIEW_PROMPT`**

- **位置**：`agent/curator.py`
- **作用**：指导 Curator 做 Skill 合并、归档和总括型 Skill 整理
- **触发条件**：Curator 满足运行条件并进入 LLM Review 阶段

中文大意：Curator 要整理并构建总括型 Skill 而不只是被动审计或简单找重复项。目标是让技能库成为“类别级指令和经验知识”的库，而不是堆满只记录某次会话具体 bug 的狭窄 Skill。它的候选列表已经过滤为 Curator 管理的本地技能；它不能碰 bundled / Hub 安装的技能，不能删除技能，最多只能归档；pinned 技能完全跳过。整理时会扫描候选列表，识别前缀集群，判断它们共同服务的 umbrella class，然后选择合并到已有 umbrella、创建新的 umbrella，或把窄技能降级成 `references/`、`templates/`、`scripts/` 支持文件。

关键原文片段：

```text
You are running as Hermes' background skill CURATOR. This is an
UMBRELLA-BUILDING consolidation pass, not a passive audit and not a
duplicate-finder.

The goal of the skill collection is a LIBRARY OF CLASS-LEVEL
INSTRUCTIONS AND EXPERIENTIAL KNOWLEDGE.

Hard rules — do not violate:
1. DO NOT touch bundled or hub-installed skills.
2. DO NOT delete any skill. Archiving is the maximum destructive action.
3. DO NOT touch skills shown as pinned=yes. Skip them entirely.

Three ways to consolidate:
  a. MERGE INTO EXISTING UMBRELLA.
  b. CREATE A NEW UMBRELLA SKILL.md.
  c. DEMOTE TO REFERENCES/TEMPLATES/SCRIPTS.
```

### 8.5.2 配置
Curator 配置示例：

```yaml
# ~/.hermes/config.yaml
curator:
  enabled: true
  interval_hours: 168
  min_idle_hours: 2
  stale_after_days: 30
  archive_after_days: 90
```

Curator 的 LLM Review 可以单独指定更便宜的辅助模型进行维护任务：

```yaml
# ~/.hermes/config.yaml
auxiliary:
  curator:
    provider: openrouter  # auto 代表使用主模型
    model: google/gemini-3-flash-preview
    timeout: 600
```

### 8.5.3 常用命令
```bash
hermes curator status                   # 查看技能状态
hermes curator run                      # 手动运行策展
hermes curator run --background         # 后台运行
hermes curator run --dry-run            # 只预览，不修改技能库
hermes curator pause                    # 暂停自动运行
hermes curator resume                   # 恢复自动运行
hermes curator pin my-important-skill   # 固定某个技能，防止被自动处理
hermes curator unpin my-important-skill # 取消固定
hermes curator restore my-skill         # 恢复已归档的技能
```

同样的子命令也可以在会话中通过 `/curator` 斜杠命令使用。

### 8.5.4 备份与回滚
每次 Curator 运行前，Hermes 会把 `~/.hermes/skills/` 打包备份到：

```text
~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz
```

如果某次维护结果不符合预期，可以回滚：

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

### 8.5.5 哪些技能会被处理
Curator 的自动迁移和 LLM Review 只处理同时满足这些条件的技能：

- 位于本地技能目录 `~/.hermes/skills/`
- 不在 `~/.hermes/skills/.bundled_manifest` 记录中，也就是不是 bundled 内置技能
- 不在 `~/.hermes/skills/.hub/lock.json` 记录中，也就是不是 Skills Hub 安装的技能
- 在 `~/.hermes/skills/.usage.json` 中被明确标记为 `created_by: "agent"` 或 `agent_created: true`

通常这指后台自我改进 review agent 通过 `skill_manage(action="create")` 创建的技能。下列技能不会因为只是存在于磁盘上就被 Curator 自动归档或合并：

- 用户手写的 `SKILL.md`
- 用户明确要求前台 Agent 创建的 Skill
- 通过 `skills.external_dirs` 暴露给 Hermes 的外部技能目录中的 Skill
- bundled 内置技能和 Skills Hub 安装的技能

外部技能目录仍会被扫描并出现在技能索引、`skills_list`、`skill_view` 和斜杠命令中，但它们不是 Curator 的归档 / 合并对象；Curator 的归档目录也只在本地 `~/.hermes/skills/.archive/` 下。

如果某个技能很重要，建议先执行：

```bash
hermes curator pin <skill-name>
```

Pinned 技能不会被自动迁移到 `stale` 或 `archived`，Curator 的 LLM Review 会跳过它，Agent 的 `skill_manage delete` 也不能删除它。

### 8.5.6 使用记录与报告
Curator 会维护一个伴随文件 `~/.hermes/skills/.usage.json`，记录非 bundled、非 Hub 技能的使用遥测和 Curator 管理标记。bundled / Hub 技能不会写入这份文件；用户手写或外部目录里的技能可能因为被查看或加载而出现使用计数，但只有带有 `created_by: "agent"` 或 `agent_created: true` 的条目才会进入 Curator 的自动迁移和 LLM Review 候选集。

```jsonc
{
  "my-skill": {
    "created_by": "agent",                  // agent 表示进入 Curator 管理范围；null 表示只记录遥测
    "use_count": 12,                         // 被加载到对话 prompt 的次数
    "view_count": 34,                        // Agent 调用 skill_view 查看该技能的次数
    "last_used_at": "2026-04-24T18:12:03Z",  // 最近一次被加载到对话的时间
    "last_viewed_at": "2026-04-23T09:44:17Z",// 最近一次被 skill_view 查看时间
    "patch_count": 3,                        // 被 skill_manage 修改的次数
    "last_patched_at": "2026-04-20T22:01:55Z",// 最近一次被修改时间
    "created_at": "2026-03-01T14:20:00Z",    // 技能创建时间
    "state": "active",                       // 当前状态：active / stale / archived
    "pinned": false,                         // 是否被固定，固定后不会被自动归档
    "archived_at": null                      // 归档时间，未归档时为 null
  }
}
```

计数器递增规则：

- `view_count`：Agent 对该技能调用 `skill_view`
- `use_count`：该技能被加载到对话 prompt 中
- `patch_count`：`skill_manage patch/edit/write_file/remove_file` 作用于该技能

内置技能和通过 Skills Hub 安装的技能不会写入这份文件，也不参与 Curator 的 stale / archive 判断。Curator 不需要为它们维护使用统计，因为它们由 bundled 同步或 Hub lock 管理，而不是由 Curator 维护生命周期。

每次 Curator 运行后，都会在 `~/.hermes/logs/curator/` 下写入一个带时间戳的目录：

```text
~/.hermes/logs/curator/
└── 20260429-111512/
    ├── run.json      # 机器可读：完整数据、统计信息、LLM 输出
    └── REPORT.md     # 人类可读：本次运行摘要
```

# 9. Hooks
https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks

Hermes 提供了三种钩子系统，允许在关键生命周期点执行自定义代码。所有钩子都是非阻塞设计，错误会被捕获并记录，不会影响 Agent 运行。

三种钩子对比：

| 维度     | Shell Hooks Shell 钩子                  | Plugin Hooks 插件钩子                  | Gateway Hooks 网关钩子             |
| -------- | --------------------------------------- | -------------------------------------- | ---------------------------------- |
| 语言     | 任意（Bash、Python、Go 等）             | 仅 Python                              | 仅 Python                          |
| 运行环境 | CLI + Gateway                           | CLI + Gateway                          | 仅 Gateway                         |
| 事件名   | Agent 内部事件名                        | Agent 内部事件名                       | 带冒号的 Gateway 事件名            |
| 注册位置 | `~/.hermes/config.yaml` 的 `hooks:`     | 插件 `register(ctx)` 中注册            | `~/.hermes/hooks/<name>/HOOK.yaml` |
| 典型用例 | 阻止危险命令、自动格式化、注入 git 状态 | 工具拦截、指标采集、防护措施、记忆召回 | 日志记录、告警通知、Webhook 回调   |

常见钩子：

| 钩子                                              | 适用系统       | 触发时机                        | 常见用途                            | 是否能影响流程                    |
| ------------------------------------------------- | -------------- | ------------------------------- | ----------------------------------- | --------------------------------- |
| `pre_tool_call`                                   | Shell / Plugin | 工具执行前                      | 阻止危险命令、检查参数、审计调用    | 可以返回 `block` 阻止工具执行     |
| `post_tool_call`                                  | Shell / Plugin | 工具返回后                      | 记录结果、采集指标、跟踪生成文件    | 观察型，不修改工具结果            |
| `pre_llm_call`                                    | Shell / Plugin | 每轮 LLM 调用前                 | 注入 git 状态、外部上下文、策略提示 | 可以返回 `context` 注入额外上下文 |
| `post_llm_call`                                   | Shell / Plugin | 每轮 LLM 调用结束后             | 记录响应、同步记忆、采集 token 指标 | 观察型                            |
| `on_session_start`                                | Shell / Plugin | 新会话开始时                    | 初始化会话状态、打开外部连接        | 观察型                            |
| `on_session_end`                                  | Shell / Plugin | 会话结束、重置或退出时          | 清理资源、flush 缓存、发送通知      | 观察型                            |
| `gateway:startup`                                 | Gateway        | Gateway 进程启动时              | 启动检查、告警、注册 Webhook        | 观察型                            |
| `session:start` / `session:end` / `session:reset` | Gateway        | Gateway 会话创建、结束或重置时  | 记录消息平台会话、审计用户行为      | 观察型                            |
| `agent:start` / `agent:step` / `agent:end`        | Gateway        | Gateway 中 Agent 处理消息的过程 | 监控长任务、记录工具循环、统计耗时  | 观察型                            |
| `command:*`                                       | Gateway        | Gateway 里执行任意斜杠命令时    | 命令审计、权限统计、外部通知        | 观察型                            |

## 9.1 Shell Hook 示例：每次对话结束后弹出 Windows 桌面小窗
适合在 WSL / Git Bash / Windows 终端里使用 Hermes：当一次 `run_conversation()` 结束时，`on_session_end` 会触发脚本，通过 `powershell.exe` 创建一个 WinForms 桌面提醒小窗。

1. 注册 shell hook：

```yaml
# ~/.hermes/config.yaml
hooks:
  on_session_end:
    - command: "~/.hermes/agent-hooks/windows-session-end-popup.sh"
      timeout: 15
```

2. 创建脚本目录：

```bash
mkdir -p ~/.hermes/agent-hooks
```

3. 创建脚本 `~/.hermes/agent-hooks/windows-session-end-popup.sh`：

```bash
#!/usr/bin/env bash

# Hermes 会把 hook payload 传到 stdin；这里不需要使用，直接丢弃。
cat - >/dev/null

if command -v powershell.exe >/dev/null 2>&1; then
  # WinForms 自绘小弹窗
  powershell.exe -NoProfile -WindowStyle Hidden -Command '
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $padding = 10
    $gap = 2
    $titleText = "Hermes"
    $bodyText = "Session finished"
    $titleFont = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $bodyFont = New-Object System.Drawing.Font("Segoe UI", 9)
    $titleSize = [System.Windows.Forms.TextRenderer]::MeasureText($titleText, $titleFont)
    $bodySize = [System.Windows.Forms.TextRenderer]::MeasureText($bodyText, $bodyFont)
    $contentWidth = [Math]::Max($titleSize.Width, $bodySize.Width)

    $f = New-Object System.Windows.Forms.Form
    $f.Text = "Hermes"
    $f.Width = $contentWidth + ($padding * 2)
    $f.Height = $titleSize.Height + $bodySize.Height + $gap + ($padding * 2)
    $f.FormBorderStyle = "None"
    $f.StartPosition = "Manual"
    $f.BackColor = [System.Drawing.Color]::FromArgb(32, 32, 32)
    $f.ForeColor = [System.Drawing.Color]::White
    $workArea = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
    $x = $workArea.Left + (($workArea.Width - $f.Width) / 2)
    $y = $workArea.Top + (($workArea.Height - $f.Height) / 2)
    $f.Location = [System.Drawing.Point]::new($x, $y)
    $f.TopMost = $true
    $f.ShowInTaskbar = $false

    # 标题
    $title = New-Object System.Windows.Forms.Label
    $title.Text = $titleText
    $title.Font = $titleFont
    $title.ForeColor = [System.Drawing.Color]::White
    $title.Location = [System.Drawing.Point]::new($padding, $padding)
    $title.Size = [System.Drawing.Size]::new($contentWidth, $titleSize.Height)
    $f.Controls.Add($title)

    # 内容
    $body = New-Object System.Windows.Forms.Label
    $body.Text = $bodyText
    $body.Font = $bodyFont
    $body.ForeColor = [System.Drawing.Color]::FromArgb(180, 180, 180)
    $body.Location = [System.Drawing.Point]::new($padding, $padding + $titleSize.Height + $gap)
    $body.Size = [System.Drawing.Size]::new($contentWidth, $bodySize.Height)
    $f.Controls.Add($body)

    # 3 秒后自动关闭
    $timer = New-Object System.Windows.Forms.Timer
    $timer.Interval = 3000
    $timer.Add_Tick({ $f.Close() })
    $timer.Start()

    $f.ShowDialog()
    $f.Dispose()
  ' >/dev/null 2>&1 &
fi

printf '{}\n'
```

这个脚本适用于常见的 Windows 10 / 11 + WSL / Git Bash / Windows 终端环境。脚本依赖 Windows 自带的 `powershell.exe`，并通过 WinForms 创建一个不走系统通知中心的小弹窗；如果弹窗没有出现，优先检查当前环境是否能调用 `powershell.exe`、Hermes 是否运行在可交互的 Windows 桌面会话中。

4. 赋予执行权限：

```bash
chmod +x ~/.hermes/agent-hooks/windows-session-end-popup.sh
```

首次运行时 Hermes 会询问是否允许这个 `(event, command)` 组合。

# 10. Plugins
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins

Hermes 拥有一个插件系统，无需修改核心代码即可添加自定义工具、钩子和集成。

## 10.1 插件能做什么
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

## 10.2 插件目录
用户插件目录是 `~/.hermes/plugins/`，每个插件一个独立子目录。最小可用插件只需要两个文件：

```text
~/.hermes/plugins/hello-world/
├── plugin.yaml      # 插件清单：名称、版本、描述等元信息
└── __init__.py      # 定义 register(ctx)，在这里注册工具 / hook / 命令
```

其中真正的接入点是 `__init__.py` 里的 `register(ctx)`。Hermes 加载插件后会调用这个函数；插件也是在这里通过 `ctx.register_tool(...)`、`ctx.register_hook(...)`、`ctx.register_command(...)` 等 API 把自己的能力注册进 Hermes。

`plugin.yaml` 主要负责插件发现和元信息，例如名称、版本、描述、依赖环境变量等。也就是说：`plugin.yaml` 让 Hermes 知道“这里有一个插件”，`register(ctx)` 决定“这个插件实际提供什么能力”。

## 10.3 插件示例
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

## 10.4 插件发现
Hermes 会从多个来源发现插件：

| 来源    | 路径 / 方式                         | 用途                                                                               |
| ------- | ----------------------------------- | ---------------------------------------------------------------------------------- |
| Bundled | Hermes 仓库内置 `plugins/`          | 官方随 Hermes 发布的插件                                                           |
| User    | `~/.hermes/plugins/`                | 用户自己的本地插件                                                                 |
| Project | `.hermes/plugins/`                  | 当前工作目录插件；默认不扫描，需设置 `HERMES_ENABLE_PROJECT_PLUGINS=true` 显式信任 |
| pip     | `hermes_agent.plugins` entry points | 通过 Python 包分发的插件                                                           |

## 10.5 管理插件
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

# 11. 持久记忆
https://hermes-agent.nousresearch.com/docs/user-guide/features/memory

Hermes 有一套有容量上限、由 Agent 自己维护的持久记忆系统。它会跨会话保存用户偏好、项目环境、工具习惯和经验教训，并在新会话开始时注入系统提示词。

## 11.1 工作原理
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

## 11.2 memory 工具
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

## 11.3 记忆管理
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

## 11.4 session_search vs memory
除了 `MEMORY.md` 和 `USER.md`，Hermes 还可以通过 `session_search` 搜索过去的完整会话。两者用途不同：

| 对比项     | 持久记忆                     | Session Search             |
| ---------- | ---------------------------- | -------------------------- |
| 容量       | 约 1,300 tokens，总量很小    | 理论上包含所有历史会话     |
| 速度       | 会话开始时直接进入系统提示词 | 需要按需查询数据库         |
| 用途       | 必须一直可见的关键事实       | 查找过去某次讨论的具体内容 |
| 管理方式   | Agent 主动维护、压缩、替换   | 自动保存所有会话           |
| token 成本 | 每个会话固定占用少量上下文   | 返回的消息片段占用上下文   |

memory 保存「以后经常要用的稳定事实」；session_search 用来回答「上次我们讨论过什么」。

## 11.5 外部记忆
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

# 12. 上下文文件
https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files

Hermes Agent 会自动发现并加载上下文文件。这里的“上下文文件”分两类：项目上下文文件用于描述当前仓库或目录规则；`SOUL.md` 用于描述当前 Hermes 实例的人格和沟通风格。

## 12.1 支持的上下文文件
| 文件                       | 用途                                   | 发现方式                        |
| -------------------------- | -------------------------------------- | ------------------------------- |
| `.hermes.md` / `HERMES.md` | Hermes 专用项目说明，优先级最高        | 从当前目录向上查找到 git root   |
| `AGENTS.md`                | 项目说明、架构、约定、注意事项         | 启动目录；子目录中可渐进发现    |
| `CLAUDE.md`                | 兼容 Claude Code 的上下文文件          | 启动目录；子目录中可渐进发现    |
| `.cursorrules`             | 兼容 Cursor 的项目规则                 | 启动目录；子目录中可渐进发现    |
| `.cursor/rules/*.mdc`      | Cursor 规则模块                        | 启动目录                        |
| `SOUL.md`                  | 当前 Hermes 实例的人格、语气和沟通风格 | 只从 `HERMES_HOME/SOUL.md` 加载 |

## 12.2 加载流程与安全处理
项目上下文有两条加载路径：启动加载和渐进加载。启动加载决定会话一开始注入哪份项目说明；渐进加载会在 Agent 访问子目录时补充局部规则。

### 12.2.1 启动加载
启动加载发生在会话开始时。流程如下：

1. 扫描当前工作目录，按优先级查找项目上下文文件
2. 以 UTF-8 文本格式读取
3. 执行安全扫描
4. 超过 20,000 字符时截断，保留头部和尾部
5. 组合到 `# Project Context` 部分并注入系统提示词

启动时的项目上下文只加载一种类型，优先级是：`.hermes.md` / `HERMES.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` / `.cursor/rules/*.mdc`。`SOUL.md` 独立加载，不参与这个优先级竞争。

`.hermes.md` / `HERMES.md` 是 Hermes 专用的项目级说明，只在启动时从当前目录向上查找到 git root。它不参与子目录渐进发现；子目录级规则应写在 `AGENTS.md`、`CLAUDE.md` 或 `.cursorrules` 中。

### 12.2.2 启动加载的截断策略
启动加载的默认截断上限是 20,000 字符。超过上限后，Hermes 保留前 70% 和后 20%，中间插入截断标记。例如：

```text
[...truncated AGENTS.md: kept 14000+4000 of 35620 chars. Use file tools to read the full file.]
```

也就是说，重要规则最好放在文件开头或结尾；如果关键规则只放在超长文件中间，可能只留下截断标记，需要 Agent 之后用文件工具读取全文。

### 12.2.3 渐进加载
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

## 12.3 `SOUL.md` 与 `/personality`
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

# 13. Gateway
https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

Gateway 是 Hermes 的消息平台接入层，可以作为前台进程或后台服务运行。它负责连接 Telegram、Discord、Slack、微信等平台，接收消息，维护每个聊天对应的会话，把消息转发给 Hermes Agent 处理，再把回复发回原平台。

Gateway 和 CLI 模式使用同一套 Hermes 程序、配置、会话、记忆、技能和工具。区别在于：CLI 是终端里的单次交互入口，Gateway 是长期运行的消息平台适配进程。Gateway 还会运行 cron 调度循环，用来触发到期的计划任务。

## 13.1 命令
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

## 13.2 网关配对
默认情况下，网关会拒绝所有不在允许列表中或未通过私信配对的用户。

### 13.2.1 允许列表
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

### 13.2.2 私信配对
无需手动配置用户 ID，未知用户在私信机器人时会收到一次性配对码，例如： `Pairing code: XKGH5N7P`。之后管理员在本机批准：

```bash
hermes pairing approve telegram XKGH5N7P  # 批准配对
hermes pairing list                       # 查看配对列表
hermes pairing revoke telegram <user_id>  # 撤销配对
```

配对码 1 小时后过期，有速率限制，并使用加密随机数生成。

### 13.2.3 斜杠命令权限控制
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

# 14. Profile
https://hermes-agent.nousresearch.com/docs/user-guide/profiles

通过 Profile 运行多个独立的 Hermes Agent，每个 Agent 有独立的配置、会话、技能和记忆。

## 14.1 什么是 Profile
Profile 是一个独立的 Hermes home 目录。其中包含各自的 `config.yaml`、`.env`、`SOUL.md`、记忆、会话、技能、cron 任务、状态数据库和 Gateway 状态。

通过 Profile 可以运行用于不同用途的 Agent 而不会混淆 Hermes 状态。

创建 Profile 后，Hermes 会自动生成同名命令别名。例如创建 `coder` 后，可以直接使用 `coder chat`、`coder setup`、`coder gateway start`，本质上等价于 `hermes -p coder ...`。

## 14.2 创建 Profile
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

## 14.3 使用 Profile
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

## 14.4 工作原理
Profile 使用 `HERMES_HOME` 环境变量。运行 `coder chat` 时，包装脚本会在启动 Hermes 前设置 `HERMES_HOME=~/.hermes/profiles/coder`。代码中通过 `get_hermes_home()` 解析路径，把 Hermes 状态限定在对应 Profile 目录下，包括配置、会话、记忆、技能、状态数据库、Gateway PID、日志和定时任务。

# 15. Cron
https://hermes-agent.nousresearch.com/docs/user-guide/features/cron

Hermes 内置定时任务系统，可以用自然语言、cron 表达式安排任务。

定时任务通过 Gateway daemon 执行：Gateway 每 60 秒 tick 一次，检查到期任务。为每个到期任务启动一个新的 Agent 会话执行 prompt，然后投递最终结果。

Cron 运行时会禁用 cron 管理工具，避免递归创建更多定时任务造成调度循环。

## 15.1 创建任务
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

## 15.2 调度格式
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

## 15.3 管理任务
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

## 15.4 运行结果投递方式
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

## 15.5 No-agent 模式
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

## 15.6 使用 context_from 链接作业
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

# 16. Delegation
https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation

Hermes 可以创建子 Agent 来处理独立的任务。子 Agent 有自己的对话和终端环境，互不干扰。

## 16.1 单任务与并行批量
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

## 16.2 子 Agent 上下文
子 Agent 启动时拥有全新对话，不知道父会话之前的任何内容。子 Agent 的唯一上下文来自接收的 `goal` 和 `context` 两个字段：

- `goal`：任务目标（必填）
- `context`：完成目标所需的全部背景信息——错误详情、文件路径、项目位置、环境约束等，父 Agent 必须在此完整传递

子 Agent 完成后，只有结构化摘要（做了什么、发现了什么、改了什么、遇到的问题）回传到父会话，详细对话过程不保留，以此控制 token 开销。

## 16.3 工具集限制
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

## 16.4 嵌套委派与配置
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

# 17. Kanban
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://github.com/NousResearch/hermes-agent/blob/main/docs/hermes-kanban-v1-spec.pdf

Hermes Kanban 是一个多 Agent 协作层：它是一个可恢复、可审计、可中途介入的工作队列。它把任务、依赖、评论、运行记录和工作目录放进一个持久任务板里，让多个具名 profile 以异步方式协作。

## 17.1 Kanban 的目标
### 17.1.1 从 `delegate_task` 到 Kanban
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

### 17.1.2 其他系统的设计方案
#### 17.1.2.1 Cline Kanban
Cline Kanban 的形态是本地任务板：一个任务是一张卡片，每张卡片对应一个临时 git 工作树，并可以分配给不同命令行 Agent。卡片可以连成依赖链，父任务完成后子任务自动启动。

它的启发是：**任务板 + 依赖链接 + 工作目录** 本身就足以构成一个有效的协调层。它没有账号系统、服务器基础设施、复杂治理，也不强调长期 Agent 身份。这个模型简单有效，但偏代码任务：git 工作树是核心假设，非代码工作和长期身份不是主要目标。

#### 17.1.2.2 Paperclip
Paperclip 把 Agent 建模成公司里的“员工”：有组织结构图、预算、治理、目标任务图、心跳、执行记录和每 Agent 的 API key 轮换。它强调持久 Agent 身份和原子任务认领，Agent 运行时也可以是 OpenClaw、Claude Code、Codex、Cursor、bash 或 HTTP。

它的启发是：长期协作需要持久身份、原子认领和可恢复任务。但它也展示了另一端的复杂度：预算、审批、治理、组织架构对企业场景有价值，但不一定应该进入 Hermes 的协作内核。对多数用户来说，这些更适合做成 profile 约定或插件。

#### 17.1.2.3 NanoClaw Agent Swarms
NanoClaw Agent Swarms 基于 Claude Code 的实验性 agent teams 能力，让主 Agent 在容器中编排多个子 Agent。

它的启发是：不要把协作生命周期完全绑定在外部 SDK 的会话分支、resume 语义或临时子 Agent 生命周期上。协调层必须在 Hermes 自己控制的层里；工作者应该是独立操作系统进程，失败、崩溃、超时或主机重启后都可以通过任务板和认领机制恢复。

#### 17.1.2.4 三者比较分析
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

### 17.1.3 Hermes Kanban 的设计理念
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

## 17.2 架构
![hermes kanban architecture](images/hermes_kanban_architecture.png)

三层架构：

- 控制层是用户交互入口，包括 CLI、Gateway 和 Dashboard
- 状态层是任务板和简易调度器
- 执行层是一组相互独立的 profile 进程，每个进程都有隔离状态

所有协调都通过任务板流转，profile 之间没有直接的进程间通信。

### 17.2.1 Control Plane：CLI / Gateway / Dashboard
控制层是用户与 Kanban 交互的入口。用户通过 CLI、Gateway 或 Dashboard 把工作交给 Kanban，查看当前进展，补充人工反馈，并根据执行结果决定下一步。

控制层关心的是“我要做什么”“现在做到哪里”“是否需要人工介入”，不直接持有 worker 的执行上下文。

### 17.2.2 State Plane：SQLite board + dispatcher
状态层是 Kanban 的唯一事实来源。默认 board 使用 `~/.hermes/kanban.db` 共享 SQLite 数据库，所有 profile 进程都读取和写入它。

dispatcher 根据 board 里的任务状态和依赖关系，决定哪些任务可以运行，并启动对应的 profile worker。

### 17.2.3 Execution Plane：独立 profile worker
执行层由一组独立 profile 进程组成。每个 worker 都是完整的 Hermes 进程，拥有自己的 `HERMES_HOME`、记忆、技能和工作目录。

worker 之间不直接通信，所有输入、输出、状态变化和交接都写回 board。

## 17.3 Kanban 核心概念
### 17.3.1 Board：任务板
Board 是一个独立的任务队列，拥有自己的 SQLite 数据库、workspaces 目录和调度循环。可以有多个 board，例如按项目、仓库或业务域拆分；如果只使用单项目工作流，默认使用 `default` board。

默认 board 的数据库位于 `~/.hermes/kanban.db`。非默认 board 位于 `~/.hermes/kanban/boards/<slug>/` 下，并拥有独立的 `kanban.db`、`workspaces/` 和 `logs/`。dispatcher 启动 worker 时会固定 `HERMES_KANBAN_BOARD`，让 worker 只看到自己所属的 board。

### 17.3.2 Task：任务
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

### 17.3.3 Link：任务的依赖关系
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

### 17.3.4 Comment：任务的评论 / 交接记录
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

### 17.3.5 Event：任务事件
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

### 17.3.6 Workspace：任务的工作目录
Workspace 是 task 绑定的工作目录，也是 worker 执行该 task 时所在的文件系统目录。Task 通过 `workspace_kind` 和 `workspace_path` 记录 workspace 设置；board 提供默认的 `workspaces/` 根目录，用来放置 `scratch` 类型任务目录。Kanban 支持如下 workspace 类型：

- `scratch`：默认模式，为 task 创建新的临时工作目录。默认 board 位于 `~/.hermes/kanban/workspaces/<id>/`；非默认 board 位于 `~/.hermes/kanban/boards/<slug>/workspaces/<id>/`
- `dir:<path>`：使用已有绝对路径
- `worktree`：为代码任务创建 git worktree，目录通常位于 `.worktrees/<id>/`。由 worker 侧执行 `git worktree add` 创建，让并行工程任务互不干扰

### 17.3.7 Dispatcher：调度器
Dispatcher 是一个长期循环，默认运行在 Gateway 内部。它每 N 秒（默认 60 秒）扫描 board，回收异常任务，重新计算 ready 状态，认领可启动任务，并为已分配 assignee 的任务启动对应 profile worker。

这个间隔可通过 `kanban.dispatch_interval_seconds` 调整：

```yaml
# ~/.hermes/config.yaml
kanban:
  dispatch_interval_seconds: 60  # dispatcher tick 间隔，单位秒；默认 60，最小 1
```

### 17.3.8 Worker：执行者
Worker 是 dispatcher 启动的独立 Hermes profile 进程。每个 worker 都是完整的操作系统进程，拥有自己的 `HERMES_HOME`、记忆、技能、工具权限和 workspace。

处理 Kanban task 的 profile 需要加载 `kanban-worker` skill。这个 skill 教会 worker Kanban 工具调用完整生命周期，而不是在终端里执行 `hermes kanban ...` 命令：

1. 启动后先调用 `kanban_show()`，读取 task 标题、正文、父任务交接、历史运行记录和完整评论串
2. 通过 terminal 工具进入 `$HERMES_KANBAN_WORKSPACE`，在 task 绑定的 workspace 中执行工作
3. 长时间运行时定期调用 `kanban_heartbeat(note="...")`，刷新心跳并留下进度说明
4. 完成时调用 `kanban_complete(summary="...", metadata={...})`；卡住时调用 `kanban_block(reason="...")`

`kanban-worker` 是 bundled skill，安装和更新时会同步到每个 profile。dispatcher 启动 worker 时也会自动传入 `--skills kanban-worker`，所以即使某个 profile 的默认 skills 配置里没有它，worker 仍会获得这套工作模式。

worker 不通过 CLI 命令操作任务板，而是通过 `kanban_*` 工具读取和更新 task，例如 `kanban_show`、`kanban_heartbeat`、`kanban_complete`、`kanban_block`、`kanban_comment`。这样做是为了保持后端可移植性：worker 的 terminal 工具可能指向远程执行后端，例如 Docker、SSH。如果 worker 在 terminal 里执行 `hermes kanban complete`，命令实际会运行在远程容器或远程主机中，而远程主机可能没有安装 `hermes`，也没有挂载本机的 `~/.hermes/kanban.db`。`kanban_*` 工具则运行在 Agent 自己的 Python 进程里，可以直接访问当前 Hermes home 下正确的 board 数据库，不受 terminal 后端位置影响。

## 17.4 协作模式
Kanban 可衍生出如下可重用的协作模式。

### 17.4.1 扇出（Fan-out）
把一个目标拆成多个同级 task，并行交给同一类或多类 profile 执行。task 之间没有父子依赖，各自独立产出结果；如果需要综合，再创建一个下游汇总 task。

例如：

```text
goal
├── researcher-a
├── researcher-b
└── researcher-c
```

### 17.4.2 流水线（Pipeline）
上游 task 完成后，下游 task 才进入 `ready`，适合“一个阶段的输出是下一个阶段的输入”的工作。依赖关系用 `task_links` 表达，父任务的摘要和评论会成为下游 worker 的上下文。

例如：

```text
researcher -> analyst -> writer -> reviewer
```

### 17.4.3 扇入（Fan-in）
多个同级 task 先独立产出候选发现、判断或实现方案；聚合 task 依赖它们全部完成后再启动。适合研究综合、方案评审、并行实现后的汇总。

例如：

```text
researcher-a \
researcher-b  -> reviewer / aggregator
researcher-c /
```

### 17.4.4 长期运行日志（Long-running journal）
同一个 profile 在同一个共享 workspace 通过定时任务反复处理周期性任务。profile 通过持久记忆和共享 workspace 累积经验，并利用 Kanban 充当审计时间线。适合日报、周报、监控巡检、收件箱分流这类工作。

### 17.4.5 人工介入分流（Human-in-the-loop triage）
worker 遇到不确定的情况时，把 task 置为 `blocked`，并在任务评论中附上疑问。用户或其他 profile 通过评论回复并 unblock 任务。调度器会重新启动 worker，任务评论会成为下一次 worker 的上下文。

例如：

```text
worker 执行 -> kanban_block(reason) -> user comment -> unblock -> dispatcher 重新启动 worker
```

### 17.4.6 批量对象作业（Fleet farming）
一个 profile 管理 N 个对象：这里的对象可以是社媒账号、客户、服务器、仓库、监控服务或数据源。所有 task 指派给同一个 profile，但每个对象使用自己的 workspace 目录。

例如一个 `insta-manager` profile 管理 50 个 Instagram 账号：

```text
task: post daily story for acct-1   -> assignee=insta-manager, workspace=dir:~/insta/acct-1/
task: post daily story for acct-2   -> assignee=insta-manager, workspace=dir:~/insta/acct-2/
...
task: post daily story for acct-50  -> assignee=insta-manager, workspace=dir:~/insta/acct-50/
```

通过 Cron 按账号定期创建任务，例如每天为每个账号创建一个发布、巡检或分析 task。

## 17.5 Dispatcher：调度器
### 17.5.1 职责与 tick 流程
dispatcher 负责把 board 中已经满足运行条件的 task 交给对应 profile worker，并推进 task 状态。每次 tick 主要执行四类动作：

1. **stale recovery**：先处理异常的 `running` 任务，包括认领过期、worker 进程已经退出、超过最大运行时间等情况。必要时释放 `claim_lock`，把任务恢复到可重新调度的状态，并记录回收、崩溃或超时事件。
2. **recompute ready**：将没有父任务，或所有父任务都已经 `done` / `archived` 的任务推进到 `ready`。
3. **atomic claim**：扫描 `ready`、`claim_lock IS NULL`、`assignee IS NOT NULL` 的任务，通过“比较并交换”（compare-and-swap）式 SQL 更新 `tasks` 表记录。只有更新成功才算认领成功；成功后任务变成 `running`，并写入 `claim_lock` 和 `claim_expires`。
4. **启动 worker**：认领成功后解析 workspace，启动 assignee 对应的 profile worker。worker 启动成功后，dispatcher 把子进程 PID 写入 `worker_pid`，并记录启动事件。

### 17.5.2 并发正确性
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

### 17.5.3 失败与恢复
worker 启动失败、运行超时、进程崩溃，或没有按协议把 task 标记为完成 / 阻塞，都会被记录到任务事件和运行记录中。dispatcher 后续 tick 会尝试恢复这类任务，让它重新进入可调度状态。

为了避免同一个坏任务无限重试，Kanban 会维护连续失败计数。超过重试上限后，任务会自动进入 `blocked`，并保留最近一次错误信息，等待人类或 orchestrator profile 介入。

## 17.6 Orchestrator Profile
### 17.6.1 Decomposer 与 Orchestrator Profile
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

### 17.6.2 Auto Decompose 相关配置
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

### 17.6.3 Orchestrator Profile 的职责与约束
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

### 17.6.4 创建 orchestrator profile
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

## 17.7 Multi-Tenant Context：多租户上下文
Multi-Tenant Context 解决的是“同一个 profile 服务多个业务上下文”的问题。例如同一个 `researcher` profile 可以同时服务 `business-a`、`business-b` 和 `personal`，而不需要为每个业务复制一个 `researcher`。

### 17.7.1 Tenant 的含义和边界
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

### 17.7.2 子任务如何继承 Tenant
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

## 17.8 命令工具
基本形式：

```bash
hermes kanban [--board <slug>] <action> [options]
```

Hermes 会按以下优先级决定要操作的 board：

1. CLI 显式传入的 `--board <slug>`
2. 环境变量 `HERMES_KANBAN_BOARD`
3. `~/.hermes/kanban/current`
4. `default`

### 17.8.1 快速启动
```bash
hermes kanban init      # 幂等创建默认 kanban.db，已存在时不会破坏数据
hermes gateway start    # 启动 Gateway
hermes kanban create "research Hermes Agent" --assignee researcher  # 创建任务
hermes kanban watch     # 实时观察事件
hermes kanban list      # 查看任务列表
hermes kanban stats     # 查看任务统计
```

### 17.8.2 Board 管理
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

### 17.8.3 创建、查询和指派
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

### 17.8.4 依赖和生命周期
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

### 17.8.5 Triage、规格化和拆解
`triage` 列用于接收粗略想法。可以手动触发，也可以让 dispatcher 在 `kanban.auto_decompose: true` 时自动处理。

```bash
hermes kanban specify <id> [--author NAME] [--json]                 # 把 triage task 补全成明确 spec
hermes kanban specify --all [--tenant T] [--author NAME] [--json]   # 批量规格化 triage task；可按 tenant 限定范围
hermes kanban decompose <id> [--author NAME] [--json]               # 把 triage task 拆成子任务图，并根据 profile description 路由
hermes kanban decompose --all [--tenant T] [--author NAME] [--json] # 批量拆解 triage task；可按 tenant 限定范围
```

`specify` 使用 `auxiliary.triage_specifier` 模型配置；`decompose` 使用 `auxiliary.kanban_decomposer` 模型配置。`decompose` 如果判断不需要 fan-out，会退化成类似 `specify` 的单任务补全。

### 17.8.6 运行、日志和监控
```bash
hermes kanban tail <id>          # 跟踪单个 task 的事件流
hermes kanban watch [--assignee P] [--tenant T] [--kinds completed,blocked,...] [--interval SECS]  # 观察整个 board 的事件流
hermes kanban runs <id> [--json]             # 查看一个 task 的 run history；一次认领、启动、失败或完成就是一条 run
hermes kanban stats [--json]                 # 查看状态和 assignee 统计
hermes kanban log <id> [--tail BYTES]        # 查看 worker 日志
hermes kanban context <id>                   # 打印 worker 会看到的完整上下文：title、body、父任务结果、评论等
```

### 17.8.7 Dispatcher 和维护
```bash
hermes kanban dispatch [--dry-run] [--max N] [--failure-limit N] [--json]  # 手动跑一次 dispatcher tick；用于调试或跳过默认 60 秒等待
hermes kanban gc [--event-retention-days N] [--log-retention-days N]       # 清理归档 task 的 scratch workspace、旧事件、旧日志
```

### 17.8.8 Gateway 通知订阅
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

### 17.8.9 `/kanban` slash command
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

## 17.9 示例
### 运营应用
#### 17.9.1 50 个账号的批量作业
场景：用同一个 `insta-manager` profile 管理 50 个账号。每个账号都有独立 workspace、tenant 和任务记录；Cron 周期性创建任务，dispatcher 并行调度这些账号任务。

##### 17.9.1.1 创建 profile
先创建一个专门的 profile。这里用 `--clone` 继承当前默认 profile 的模型和 API 配置，并写入 description，方便 Kanban 后续按 profile 描述分配任务：

```bash
hermes profile create insta-manager --clone \
  --description "负责按账号处理社交媒体日常运营任务：读取账号素材、生成草稿、执行发布或互动动作、记录结果；每次只处理当前 task 指定的 tenant 和 workspace。"
```

这个 profile 会被批量并行启动，建议收窄工具权限：只保留完成账号任务必需的浏览器、记忆和文件访问能力，禁用 `terminal`、`code_execution` 等执行型工具：

```bash
hermes -p insta-manager tools enable browser file memory
hermes -p insta-manager tools disable terminal code_execution
```

##### 17.9.1.2 准备每个账号的 workspace
为每个账号创建一个独立目录。后续每个 task 都会绑定到自己的账号目录：

```bash
for i in $(seq 1 50); do
  mkdir -p ~/insta/acct-$i/{assets,drafts,logs}
done
```

目录含义可以按自己的工作流调整：

- `assets/`：待发布图片、视频或素材
- `drafts/`：文案草稿、候选回复
- `logs/`：每次任务的执行记录

##### 17.9.1.3 创建批量任务脚本
接下来创建一个批量任务脚本。Hermes Cron 的 `--script` 只读取 `~/.hermes/scripts/` 下的相对路径，所以脚本放在 `~/.hermes/scripts/hermes-kanban-create-fleet-tasks.sh`。这个脚本遍历 `~/insta/acct-*` 目录，并为每个账号调用一次 `hermes kanban create`。

创建脚本：

```bash
mkdir -p ~/.hermes/scripts

cat > ~/.hermes/scripts/hermes-kanban-create-fleet-tasks.sh <<'EOF'
#!/usr/bin/env bash
# 严格模式：命令失败、变量未定义或管道失败时立即退出
set -euo pipefail

profile="insta-manager"
root="$HOME/insta"
slot="$(date +%Y%m%d%H)"

for dir in "$root"/acct-*; do
  [ -d "$dir" ] || continue

  acct="$(basename "$dir")"

  hermes kanban create "engage $acct" \
    --assignee "$profile" \
    --tenant "$acct" \
    --workspace "dir:$dir" \
    --idempotency-key "fleet:$acct:$slot" \
    --max-runtime 1800
done
EOF

chmod +x ~/.hermes/scripts/hermes-kanban-create-fleet-tasks.sh
```

这里的关键点：

- `--assignee "$profile"`：所有 task 都交给同一个 `insta-manager` profile
- `--tenant "$acct"`：每个账号作为一个 tenant，方便过滤任务和隔离记忆前缀
- `--workspace "dir:$dir"`：每个账号绑定自己的目录
- `--idempotency-key`：同一小时重复运行脚本时不会重复创建同一账号的任务
- `--max-runtime 1800`：单个账号任务最多运行 30 分钟，避免异常任务长期占用 worker

##### 17.9.1.4 配置周期任务
用 Hermes Cron 每 4 小时运行一次脚本：

```bash
hermes cron create \
  --name "create insta fleet tasks" \
  --script hermes-kanban-create-fleet-tasks.sh \
  --no-agent \
  "0 */4 * * *"
```

Cron job 定时运行脚本，批量创建 Kanban task。Gateway 内置 dispatcher 在后续 tick 中认领这些 ready task，并启动对应的 `insta-manager` worker。

##### 17.9.1.5 worker 执行时看到什么
当 dispatcher 认领 `acct-17` 的任务时，它启动的是 `insta-manager` profile worker。这个 worker 处理的仍然是一个普通 Kanban task，但上下文会指向账号 17：

- `HERMES_TENANT=acct-17`
- workspace 是 `~/insta/acct-17/`
- task body 是 `engage acct-17`
- profile memory 按 tenant 命名空间隔离，也就是账号 17 自己的记忆
- worker 可以把日志写到 `~/insta/acct-17/logs/YYYY-MM-DD.jsonl`
- worker 最后把结果写回 Kanban

完成时，worker 仍然只是完成一个普通 Kanban task：

```bash
hermes kanban complete t_abcd1234 --result "当前账号发布 2 条内容，点赞其他账号内容 18 次，关注 1 个账号"
```

##### 17.9.1.6 查看和处理结果
按 tenant 查看某个账号：

```bash
hermes kanban list --tenant acct-17
hermes kanban tail t_abcd1234
```

某个账号遇到登录、素材缺失或风控问题时，worker 可以把任务标记为 blocked，并在评论里说明原因：

```bash
hermes kanban comment t_abcd1234 "acct-17 缺少今天的素材，等待补充 assets/"
hermes kanban block t_abcd1234
```

用户补齐素材后再恢复任务：

```bash
hermes kanban comment t_abcd1234 "素材已补充到 assets/"
hermes kanban unblock t_abcd1234
```

这个流程体现了 Kanban 的优势：50 个账号共享同一个专职 profile，但每个账号都有独立 workspace、tenant、任务历史和失败恢复；任务可以周期性生成，也可以针对任意单个账号阻塞、恢复和审计。

#### 17.9.2 客服工单分流与知识库沉淀
场景：客服系统每天产生大量工单。外部工单系统把新增工单标准化后 POST 到 Hermes Gateway；Kanban 自动创建 `triage` task，随后分流、查历史解决方案、生成回复草稿、升级产品缺陷，并把高频问题沉淀到知识库。

##### 17.9.2.1 流程使用的 profile
这个流程使用这些 profile：

- `triage-agent`：按产品线、严重程度、客户等级和 SLA 分流工单
- `support-agent`：查历史记录，生成客户回复草稿
- `product-agent`：判断问题属于需求、缺陷、配置问题还是使用误解
- `bug-reporter`：把确认的问题转成工程 task
- `kb-writer`：把高频问题写入知识库
- `reviewer`：审查敏感回复、退款说明和对外承诺

##### 17.9.2.2 自动入口
外部工单系统需要把工单标准化成如下字段：

```json
{
  "ticket_id": "SUP-1024",
  "customer": "acme",
  "priority": "high",
  "product": "billing",
  "summary": "客户反馈发票金额和订单金额不一致。",
  "url": "https://support.example.com/tickets/SUP-1024"
}
```

然后创建 webhook route：

```bash
export SUPPORT_WEBHOOK_SECRET="replace-with-route-hmac-secret"

hermes webhook subscribe support-ticket \
  --description "Create Kanban tasks from support tickets" \
  --secret "$SUPPORT_WEBHOOK_SECRET" \
  --prompt '/kanban create "处理客服工单 {ticket_id}：{product} {priority}" --triage --tenant customer-support --idempotency-key "support:{ticket_id}" --body "客户：{customer}；产品线：{product}；优先级：{priority}；工单链接：{url}；摘要：{summary}。请先分流，再决定是否需要回复客户、升级产品缺陷、补知识库或请求人工判断。"'
```

##### 17.9.2.3 任务图
典型任务图如下：

```text
工单 webhook -> 分流 -> 历史方案检索 -> 回复草稿 -> 回复审查
                         \-> 缺陷确认 -> 工程修复 task
                         \-> 高频问题 -> 知识库更新
```

普通工单可以由 `support-agent` 直接生成草稿；涉及退款、法律、SLA、企业大客户或公开承诺时，应进入审查或人工确认。

##### 17.9.2.4 人工介入和知识库沉淀
遇到需要人工判断的工单，worker 可以阻塞任务：

```bash
hermes kanban comment t_abcd1234 "该客户要求退款，金额超过自动处理阈值，需要人工确认口径。"
hermes kanban block t_abcd1234 "等待客服负责人确认退款方案"
```

人工确认后恢复：

```bash
hermes kanban comment t_abcd1234 "客服负责人确认：先补开发票差额说明，不直接承诺退款。"
hermes kanban unblock t_abcd1234
```

如果同类问题反复出现，可以追加知识库任务：

```bash
hermes kanban create "沉淀知识库：发票金额与订单金额不一致" \
  --assignee kb-writer \
  --tenant customer-support \
  --parent t_abcd1234 \
  --body "整理问题原因、排查步骤、客户回复模板和内部升级条件。"
```

Kanban 的价值在于把工单从“消息流”变成“可恢复工作队列”：普通工单并行处理，敏感工单保留人工卡点，高频问题最终沉淀成知识库，而不是散落在客服聊天记录里。

#### 17.9.3 内容生产流水线
场景：运营团队持续产出文章、视频脚本、社媒短帖或产品发布内容。一个主题通常要经历资料收集、观点提炼、初稿、事实核查、编辑、发布和数据复盘。

##### 17.9.3.1 流程使用的 profile
这个流程使用这些 profile：

- `researcher`：收集资料、链接、用户案例和出处
- `analyst`：提炼观点、受众角度和内容结构
- `writer`：写初稿或脚本
- `fact-checker`：核查事实、链接、数据和引用
- `editor`：统一语气、格式和发布规范
- `publisher`：发布内容，记录发布时间、渠道和数据

##### 17.9.3.2 创建内容 root task
一次性内容项目可以直接创建 root task：

```bash
mkdir -p /home/user/content/product-update-w21

hermes kanban create "制作本周产品更新长文和社媒短帖" \
  --tenant content \
  --workspace dir:/home/user/content/product-update-w21 \
  --triage
```

如果是固定节奏的内容生产，可以用 Cron 定期创建任务：

```bash
mkdir -p ~/.hermes/scripts

cat > ~/.hermes/scripts/create-weekly-content-task.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

week="$(date +%G-W%V)"
workspace="$HOME/content/product-updates/$week"
mkdir -p "$workspace"

hermes kanban create "制作 $week 产品更新内容包" \
  --tenant content \
  --workspace "dir:$workspace" \
  --idempotency-key "content:product-update:$week" \
  --triage
EOF

chmod +x ~/.hermes/scripts/create-weekly-content-task.sh

hermes cron create \
  --name "create weekly content task" \
  --script create-weekly-content-task.sh \
  --no-agent \
  "0 9 * * 1"
```

##### 17.9.3.3 任务图
典型任务图如下：

```text
资料收集 -> 观点提炼 -> 初稿 -> 事实核查 -> 编辑 -> 发布 -> 数据复盘
                 \-> 社媒短帖 ----------------------^
```

下游 task 会读取父任务 summary 和评论。例如 `writer` 启动时能看到 `researcher` 收集的资料；`fact-checker` 启动时能看到初稿和引用来源。

##### 17.9.3.4 审查卡点
涉及客户案例、收入数据、竞品比较或合规表述时，应阻塞发布任务等待确认：

```bash
hermes kanban comment t_9a8b7c6d "文中包含客户名称和收入提升数据，需要市场负责人确认是否可公开。"
hermes kanban block t_9a8b7c6d "等待市场负责人确认客户案例授权"
```

发布完成后，`publisher` 可以把渠道和数据写回任务：

```bash
hermes kanban complete t_9a8b7c6d --result "已发布到官网、公众号和 LinkedIn；首日 PV 3200，注册转化 41。"
```

Kanban 的价值在于流水线交接：每个 profile 只处理自己擅长的阶段，所有素材、审查意见、发布记录和复盘数据都挂在任务链上。

#### 17.9.4 竞品与市场情报周报
场景：每周收集竞品发布、价格变化、融资新闻、社区反馈和客户评论，形成结构化周报，并把值得跟进的机会转成产品或销售 task。

##### 17.9.4.1 流程使用的 profile
这个流程使用这些 profile：

- `web-researcher`：收集官网、博客、新闻和社媒信息
- `community-listener`：整理社区讨论和用户反馈
- `analyst`：提炼趋势、风险和机会
- `writer`：生成周报
- `sales-ops`：把销售机会转成后续跟进 task
- `product-agent`：把产品机会转成需求调研 task

##### 17.9.4.2 定时创建周报任务
用 Cron 每周一创建情报任务：

```bash
mkdir -p ~/.hermes/scripts

cat > ~/.hermes/scripts/create-market-intel-task.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

week="$(date +%G-W%V)"
workspace="$HOME/market-intel/$week"
mkdir -p "$workspace"

hermes kanban create "生成 $week 竞品与市场情报周报" \
  --tenant market-intel \
  --workspace "dir:$workspace" \
  --idempotency-key "market-intel:$week" \
  --triage
EOF

chmod +x ~/.hermes/scripts/create-market-intel-task.sh

hermes cron create \
  --name "create weekly market intel task" \
  --script create-market-intel-task.sh \
  --no-agent \
  "0 8 * * 1"
```

##### 17.9.4.3 任务图
典型任务图如下：

```text
多源信息收集 -> 社区反馈整理 -> 趋势分析 -> 周报撰写 -> 审查
                                   \-> 产品机会 task
                                   \-> 销售跟进 task
```

周报完成后，可以把机会转成后续任务：

```bash
hermes kanban create "跟进竞品降价后的企业客户流失风险" \
  --assignee sales-ops \
  --tenant market-intel \
  --parent t_1111aaaa \
  --body "基于本周情报，整理受影响客户名单、风险等级和建议沟通话术。"

hermes kanban create "调研竞品新工作流功能的产品差距" \
  --assignee product-agent \
  --tenant market-intel \
  --parent t_1111aaaa \
  --body "输出差距分析、用户场景和是否进入 roadmap 的建议。"
```

Kanban 的价值在于长期积累：每周 task 留在 board 上，评论和结果形成可回溯的情报日志；情报不是停在报告里，而是可以继续生成产品、销售和运营任务。

### 开发应用
#### 17.9.5 遗留功能灰度迁移
场景：把一个老后台里的“订单导出 CSV”迁到新架构。这个任务表面很小，实际要梳理历史兼容行为、实现新接口、补回归测试、灰度上线、等待第二天业务数据验证，最后决定是否切流。

##### 17.9.5.1 准备 profile
这个流程至少需要 6 类 profile：

- `researcher`：梳理旧逻辑、历史字段、客户依赖
- `backend-eng`：实现新导出接口
- `qa`：补回归测试和差异校验
- `reviewer`：审查代码、测试覆盖和迁移风险
- `ops`：灰度部署、观察日志
- `orchestrator`：汇总结果，决定完成或追加修复任务

可以先用 description 把每个 profile 的职责写清楚，方便 decomposer 或 orchestrator 路由：

```bash
hermes profile create researcher --clone \
  --description "负责阅读历史代码、文档、提交记录和线上行为，梳理旧逻辑、兼容约束和风险点。"
hermes profile create backend-eng --clone \
  --description "负责实现后端接口、迁移逻辑、数据兼容和必要的代码修改。"
hermes profile create qa --clone \
  --description "负责设计和执行回归测试、差异校验、边界场景验证。"
hermes profile create reviewer --clone \
  --description "负责审查代码变更、测试覆盖、迁移风险和上线前检查项。"
hermes profile create ops --clone \
  --description "负责灰度部署、观察日志、监控指标和回滚预案。"
```

##### 17.9.5.2 创建 root task
把高层目标放进 `triage`，让 decomposer 先做第一轮拆解：

```bash
hermes kanban create "迁移订单导出 CSV 到新架构" \
  --triage \
  --workspace dir:/home/user/project \
  --tenant export-migration
```

这条命令只创建一个粗略目标。后续 decomposer 会根据 profile description 拆出子任务；原始 task 会成为 root task，等子任务完成后再回到 orchestrator 做总体验收。

##### 17.9.5.3 拆解后的任务图
典型任务图如下：

```text
梳理旧导出逻辑 -> 实现新导出接口 -> 补回归测试 -> 代码审查 -> 灰度部署 -> 次日数据校验 -> 总体验收
```

对应到 Kanban task，大致是：

| 阶段           | assignee       | 说明                                       |
| -------------- | -------------- | ------------------------------------------ |
| 梳理旧导出逻辑 | `researcher`   | 找出旧字段、特殊客户逻辑、历史兼容行为     |
| 实现新导出接口 | `backend-eng`  | 在新架构里实现接口，并保留必要兼容         |
| 补回归测试     | `qa`           | 对比新旧导出结果，覆盖边界字段和大数据量   |
| 代码审查       | `reviewer`     | 审查实现、测试覆盖和迁移风险               |
| 灰度部署       | `ops`          | 小流量启用新导出路径，观察日志和错误率     |
| 次日数据校验   | `qa` / `ops`   | 等第二天真实业务数据出来后再做差异校验     |
| 总体验收       | `orchestrator` | 读取所有子任务结果，决定完成或继续追加修复 |

##### 17.9.5.4 人类介入：历史兼容字段
迁移类任务很容易遇到“没人敢删”的历史字段。`researcher` 或 `qa` 发现不确定兼容行为时，可以把任务阻塞，等待用户确认：

```bash
hermes kanban comment t_abcd1234 "旧导出里存在 legacy_customer_code 字段，新系统没有对应来源；需要确认是否继续保留。"
hermes kanban block t_abcd1234 "等待确认 legacy_customer_code 是否仍有客户依赖"
```

用户确认后再恢复：

```bash
hermes kanban comment t_abcd1234 "该字段仍被客户 A 使用，迁移后继续保留，并在新接口中从 customer_metadata 读取。"
hermes kanban unblock t_abcd1234
```

这一步体现的是 Kanban 的人类中途介入能力：不需要重启整条流程，也不需要把上下文塞回某个父 Agent 的对话里。

##### 17.9.5.5 跨天验证：灰度后等待真实数据
灰度部署完成后，通常不能立刻判断迁移成功。`ops` 可以把“次日数据校验”任务暂缓：

```bash
hermes kanban schedule t_ef567890 "等待第二天 09:00 后生成真实业务导出数据，再做新旧结果差异校验"
```

第二天数据就绪后，用户在 CLI 手动补充说明并恢复任务 ：

```bash
hermes kanban comment t_ef567890 "2026-05-23 业务导出数据已生成，可以开始差异校验。"
hermes kanban unblock t_ef567890
```

##### 17.9.5.6 root task 收尾
所有子任务完成后，root task 会从 `todo` 回到 `ready`，dispatcher 启动 root task 当前 `assignee` 对应的 profile worker。通常这个 worker 是 `orchestrator`。

orchestrator 会读取子任务结果，并做三个判断：

1. 新导出接口是否实现完成
2. 新旧导出差异是否在预期范围内
3. 灰度日志、错误率和回滚预案是否满足切流条件

满足条件时，orchestrator 完成 root task：

```bash
hermes kanban complete t_2222bbbb --result "订单导出 CSV 已迁移到新架构；灰度验证通过，保留 legacy_customer_code 兼容字段，后续可按计划切流。"
```

仍有问题时，它可以继续创建修复 task，而不是把 root task 草草结束。

这个案例体现了 Kanban 的核心优势：任务能跨天保留，子任务能并行和串行混合推进，人工确认可以插入中途，失败和阻塞有明确状态，最终由 root task 汇总所有交接信息后再决定是否完成。

#### 17.9.6 GitHub Issue 与 PR 维护队列
场景：开源项目或内部平台每天收到 issue、bug report、feature request 和 PR。GitHub webhook 事件先被标准化成统一 payload，再推到 Hermes Gateway；Kanban 自动创建 `triage` task，随后分流、复现、实现、审查、合并和写 changelog。

##### 17.9.6.1 流程使用的 profile
这个流程使用这些 profile：

- `triager`：阅读 issue / PR，判断类型、优先级和缺失信息
- `reproducer`：复现 bug，补最小复现步骤
- `maintainer`：实现修复或整理 PR 反馈
- `reviewer`：审查代码、测试和兼容性
- `release-note-writer`：整理 changelog 和升级说明

##### 17.9.6.2 webhook 入口
外部 GitHub webhook handler 需要把原始 GitHub event 标准化成如下字段：

```json
{
  "event_type": "issue",
  "repo": "org/project",
  "repo_path": "/home/user/repos/project",
  "number": "1234",
  "title": "导出接口在空订单时返回 500",
  "author": "octocat",
  "url": "https://github.com/org/project/issues/1234",
  "summary": "用户反馈空订单导出时接口返回 500。"
}
```

创建 webhook route：

```bash
export GITHUB_WEBHOOK_SECRET="replace-with-route-hmac-secret"

hermes webhook subscribe github-maintenance \
  --description "Create Kanban tasks from GitHub issues and pull requests" \
  --secret "$GITHUB_WEBHOOK_SECRET" \
  --prompt '/kanban create "处理 GitHub {event_type}：{title}" --triage --tenant github-maintenance --workspace dir:{repo_path} --idempotency-key "github:{repo}:{number}:{event_type}" --body "仓库：{repo}；编号：{number}；作者：{author}；链接：{url}；摘要：{summary}。请先分流，再决定是否需要复现、实现、审查、合并或写 changelog。"'
```

##### 17.9.6.3 任务图
典型任务图如下：

```text
GitHub webhook -> triage -> 复现 / 需求澄清 -> 实现或 PR 反馈 -> review -> 合并 -> changelog
```

缺少复现信息时，可以阻塞 issue task：

```bash
hermes kanban comment t_abcd1234 "当前 issue 缺少请求参数和错误日志，无法复现。"
hermes kanban block t_abcd1234 "等待报告人补充复现步骤和日志"
```

合并后可以追加发布说明任务：

```bash
hermes kanban create "补充 changelog：修复空订单导出 500" \
  --assignee release-note-writer \
  --tenant github-maintenance \
  --parent t_abcd1234 \
  --workspace dir:/home/user/repos/project
```

Kanban 的价值在于把 GitHub 事件流变成可恢复工作队列：每个 issue / PR 都有状态、评论、失败恢复和下游任务；多轮 review 和补充信息不会埋在通知流里。

### 运维应用
#### 17.9.7 安全漏洞响应与补丁发布
场景：GitHub Dependabot、SCA、SIEM 或镜像扫描等外部安全系统产生高危告警后，通过 webhook 自动 POST 到 Hermes Gateway。Gateway 收到告警后创建 Kanban root task，后续由不同 profile 确认影响范围、复现漏洞、实现补丁、补测试、发版、写公告，并跟踪补丁是否部署到所有环境。

##### 17.9.7.1 配置漏洞告警源
Hermes 这一侧提供的是 webhook 接收入口：Gateway 监听指定 HTTP route，收到 POST 后按 route prompt 创建 Kanban task。漏洞发现、扫描和告警生成由外部安全系统负责；这些系统需要把告警标准化成统一 webhook payload，并 POST 到 Hermes Gateway。

本示例使用如下 payload 字段：

```json
{
  "event_type": "vulnerability",
  "id": "CVE-XXXX",
  "source": "github",
  "severity": "critical",
  "package": "example-lib",
  "project": "/home/user/project",
  "summary": "example-lib 存在远程代码执行风险，需要确认影响并修复。"
}
```

##### 17.9.7.2 准备 profile
这个流程使用这些 profile：

- `security`：确认 CVE / advisory 影响范围，复现攻击路径
- `backend-eng`：实现补丁
- `qa`：补安全回归测试
- `ops`：部署补丁并检查生产版本
- `writer`：写内部通报和客户公告
- `reviewer`：审查补丁和公告准确性

```bash
hermes profile create security --clone \
  --description "负责分析安全公告、确认影响范围、复现攻击路径、判断风险等级和修复优先级。"
hermes profile create backend-eng --clone \
  --description "负责实现后端补丁、升级依赖、修复漏洞触发路径并提交代码变更。"
hermes profile create qa --clone \
  --description "负责补安全回归测试、验证漏洞无法复现、确认主要业务路径没有回归。"
hermes profile create ops --clone \
  --description "负责部署补丁、检查生产版本、观察日志和确认补丁覆盖所有环境。"
hermes profile create writer --clone \
  --description "负责撰写内部安全通报、客户公告和发布说明。"
hermes profile create reviewer --clone \
  --description "负责审查补丁、测试覆盖、公告准确性和发布风险。"
```

##### 17.9.7.3 配置 webhook 入口
先启用 webhook platform。也可以用 `hermes gateway setup` 交互式配置；手动配置写法如下：

```yaml
# ~/.hermes/config.yaml
platforms:
  webhook:
    enabled: true
    extra:
      host: "0.0.0.0"
      port: 8644
      secret: "replace-with-global-hmac-secret"
```

然后创建一个动态 webhook route。这个 route 收到 POST 后，会把 payload 渲染成 `/kanban create ...` 命令，由 Gateway 直接创建 `triage` task：

```bash
export SECURITY_WEBHOOK_SECRET="replace-with-route-hmac-secret"

hermes webhook subscribe security-advisory \
  --description "Create Kanban tasks from normalized security advisories" \
  --secret "$SECURITY_WEBHOOK_SECRET" \
  --prompt '/kanban create "响应 {id}：{package} {severity} 漏洞" --triage --tenant security --workspace dir:{project} --idempotency-key "vuln:{source}:{id}:{project}" --body "来源：{source}；严重程度：{severity}；受影响组件：{package}；摘要：{summary}；请确认影响范围、复现条件、修复方案、测试覆盖、发布计划和对外说明。"'
```

`--prompt` 里的 `{id}`、`{package}`、`{severity}`、`{project}`、`{source}`、`{summary}` 是 webhook payload 的同名字段。Gateway 收到 POST 后，会先用 payload 字段替换这些占位符，再把渲染后的文本当作斜杠命令执行。因此 payload 顶层字段名必须和占位符一致；字段缺失时，这条 route 无法生成完整的 Kanban task。

例如 payload 中 `id=CVE-XXXX`、`package=example-lib`、`severity=critical` 时，任务标题会被渲染为：

```text
响应 CVE-XXXX：example-lib critical 漏洞
```

启动 Gateway；已经安装成后台服务时可以用 `restart`：

```bash
hermes gateway run
# 或：hermes gateway restart
```

`hermes webhook subscribe` 会打印 route URL，例如：

```text
http://localhost:8644/webhooks/security-advisory
```

把这个 URL 配到外部安全平台。外部平台需要按 Hermes webhook 的 HMAC 要求签名请求；Gateway 验签通过后才会处理 payload。

##### 17.9.7.4 验证自动触发
用 `hermes webhook test` 模拟一次外部告警：

```bash
hermes webhook test security-advisory --payload '{
  "event_type": "vulnerability",
  "id": "CVE-XXXX",
  "source": "github",
  "severity": "critical",
  "package": "example-lib",
  "project": "/home/user/project",
  "summary": "example-lib 存在远程代码执行风险，需要确认影响并修复。"
}'
```

测试通过后，Kanban board 里会出现一个 `triage` task。随后 decomposer 会把 root task 拆成安全分析、修复、测试、发布、公告等子任务；dispatcher 再启动对应 profile worker。

`--idempotency-key` 会防止同一个漏洞因为 webhook 重试、扫描器重复上报或多个来源同时命中而重复创建 task。

##### 17.9.7.5 拆解后的任务图
典型任务图如下：

```text
漏洞告警 -> 影响评估 -> 复现验证 -> 补丁实现 -> 安全回归 -> 发布部署
                                \-> 公告草稿 -> 公告审查
```

对应到 Kanban task，大致是：

| 阶段     | assignee      | 说明                                 |
| -------- | ------------- | ------------------------------------ |
| 影响评估 | `security`    | 判断受影响版本、暴露面和优先级       |
| 复现验证 | `security`    | 在安全环境中确认漏洞是否可触发       |
| 补丁实现 | `backend-eng` | 升级依赖、修改代码或加防护逻辑       |
| 安全回归 | `qa`          | 验证漏洞已修复，主路径没有回归       |
| 发布部署 | `ops`         | 灰度部署、检查版本、观察日志         |
| 公告草稿 | `writer`      | 写内部通报、客户公告或发布说明       |
| 公告审查 | `reviewer`    | 审查公告是否准确，避免夸大或遗漏风险 |

##### 17.9.7.6 阻塞、发布和审计
安全任务经常需要人工判断。例如 `security` 无法确认某个组件是否暴露给外部用户时，可以阻塞任务：

```bash
hermes kanban comment t_abcd1234 "无法确认 example-lib 是否用于公网导出接口，需要服务 owner 确认调用路径。"
hermes kanban block t_abcd1234 "等待服务 owner 确认外部暴露面"
```

确认后恢复：

```bash
hermes kanban comment t_abcd1234 "服务 owner 确认该依赖仅用于内部批处理，不暴露公网，但仍需升级。"
hermes kanban unblock t_abcd1234
```

补丁发布后，`ops` 完成发布任务时可以写清楚部署范围：

```bash
hermes kanban complete t_3333cccc --result "补丁已部署到 staging 和 production；镜像版本 registry/app:2026-05-22-secfix；24 小时内未见相关错误。"
```

Kanban 的价值在于自动触发、审计和并行：漏洞告警一出现就进入任务板；安全分析、公告草稿和补丁实现可以并行推进；每个 task 的评论、状态变化、结果和失败记录都会留在 board 上，适合事后复盘。

#### 17.9.8 数据报表与 ETL 质量监控
场景：数据团队每天要跑 ETL、检查指标异常、生成日报、分析异常原因，并把确认的问题分派给数据工程或业务负责人。

##### 17.9.8.1 流程使用的 profile
这个流程使用这些 profile：

- `etl-runner`：检查 ETL 运行状态、失败日志和产物时间戳
- `data-checker`：检查数据完整性、重复率、空值和指标波动
- `analyst`：解释异常原因，判断是业务变化还是数据问题
- `data-eng`：修复 pipeline、补回填任务或修 schema
- `report-writer`：生成日报或周报

##### 17.9.8.2 定时创建日报任务
用 Hermes Cron 每天创建一个 Kanban root task：

```bash
mkdir -p ~/.hermes/scripts

cat > ~/.hermes/scripts/create-daily-data-report-task.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

day="$(date +%F)"
workspace="$HOME/data-reports/$day"
mkdir -p "$workspace"

hermes kanban create "生成 $day 经营数据日报并检查异常" \
  --tenant data-daily \
  --workspace "dir:$workspace" \
  --idempotency-key "data-daily:$day" \
  --triage
EOF

chmod +x ~/.hermes/scripts/create-daily-data-report-task.sh

hermes cron create \
  --name "create daily data report task" \
  --script create-daily-data-report-task.sh \
  --no-agent \
  "30 8 * * *"
```

##### 17.9.8.3 任务图
典型任务图如下：

```text
定时创建日报 task -> ETL 检查 -> 指标校验 -> 异常分析 -> 报告生成
                                           \-> pipeline 修复 -> 数据回填
```

数据源延迟时，`etl-runner` 可以把任务暂缓：

```bash
hermes kanban schedule t_abcd1234 "上游订单表 08:30 仍未生成，等待 09:30 后再次检查。"
```

`schedule` 只表示任务暂缓，不会按原因里的时间自动唤醒；后续需要由用户、Cron 脚本或外部自动化在数据就绪后恢复任务。

如果确认是数据质量问题，则先阻塞报告任务，再创建一个独立的修复任务。修复任务完成后，把修复结果补回报告任务，并恢复报告任务继续生成日报。

```bash
hermes kanban comment t_4444dddd "支付成功率较昨日下降 18%，初步确认是 orders 表缺失 02:00-03:00 分区。"
hermes kanban block t_4444dddd "等待 data-eng 修复 orders 分区并回填"

hermes kanban create "修复 orders 表 02:00-03:00 缺失分区并回填" \
  --assignee data-eng \
  --tenant data-daily \
  --body "修复后请在评论里写明回填范围、校验 SQL 和影响指标。"
```

修复任务完成后，再把结果补回报告任务并恢复它：

```bash
hermes kanban comment t_4444dddd "orders 表缺失分区已回填，修复任务结果见 t_1234abcd，可以继续生成日报。"
hermes kanban unblock t_4444dddd
```

Kanban 的价值在于定时和恢复：Cron 负责每天创建任务，dispatcher 负责认领和恢复 worker；数据延迟、质量异常和修复动作都有状态和评论，不会只停留在告警群里。

#### 17.9.9 线上事故复盘与改进项追踪
场景：线上事故结束后，需要收集时间线、日志、告警、变更记录、客户影响、根因分析和改进项，并持续跟踪改进项是否真正完成。

##### 17.9.9.1 流程使用的 profile
这个流程使用这些 profile：

- `incident-scribe`：整理时间线、会议记录和关键事件
- `log-analyst`：分析日志、指标、trace 和告警
- `root-cause-analyst`：做根因分析，区分触发因素和系统性原因
- `owner-router`：把改进项分配给负责人或团队
- `reviewer`：审查复盘是否完整，避免只写表面原因
- `ops`：验证改进项是否上线并持续有效
- `qa`：补回归、压测或演练场景，验证改进项是否覆盖事故路径

##### 17.9.9.2 创建复盘 root task
事故结束后创建 root task：

```bash
mkdir -p /home/user/incidents/2026-05-22-payment-timeout

hermes kanban create "复盘 2026-05-22 支付超时事故并跟踪改进项" \
  --tenant incident-20260522 \
  --workspace dir:/home/user/incidents/2026-05-22-payment-timeout \
  --triage
```

workspace 中可以放置原始材料：

```text
/home/user/incidents/2026-05-22-payment-timeout/
├── alerts/
├── logs/
├── timeline.md
├── customer-impact.md
└── changes/
```

##### 17.9.9.3 任务图
典型任务图如下：

```text
时间线整理 -> 日志分析 -> 根因分析 -> 复盘文档 -> 改进项拆分 -> 完成情况跟踪
```

根因不清楚时，`root-cause-analyst` 可以阻塞任务，要求补材料：

```bash
hermes kanban comment t_5555eeee "目前只有应用日志，缺少数据库连接池指标和发布变更记录，无法判断是否为容量问题。"
hermes kanban block t_5555eeee "等待 SRE 补充数据库指标和发布记录"
```

复盘完成后，把改进项拆成可跟踪 task：

```bash
hermes kanban create "改进项：支付服务连接池耗尽前提前告警" \
  --assignee ops \
  --tenant incident-20260522 \
  --workspace dir:/home/user/incidents/2026-05-22-payment-timeout \
  --parent t_6666ffff \
  --body "新增连接池利用率、排队时间和超时率告警；上线后观察一周并回填验证结果。"

hermes kanban create "改进项：补支付超时压测场景" \
  --assignee qa \
  --tenant incident-20260522 \
  --workspace dir:/home/user/incidents/2026-05-22-payment-timeout \
  --parent t_6666ffff \
  --body "增加连接池耗尽、下游慢响应和重试放大三个压测场景。"
```

需要观察一段时间的改进项可以暂缓：

```bash
hermes kanban schedule t_7777aaaa "告警规则已上线，等待一周观察是否有误报或漏报。"
```

观察期结束后，需要由用户、Cron 脚本或外部自动化恢复任务，再写入验证结果。

Kanban 的价值在于防止复盘停在文档：每个改进项都是可跟踪 task，有 assignee、状态、评论和完成记录；长期未完成的项不会埋在会议纪要里。

### HR 应用
#### 17.9.10 招聘简历筛选与面试安排
场景：团队收到一批候选人简历，需要初筛、岗位匹配、生成面试问题、安排面试、汇总反馈，并把通过者推进到下一轮。最终录用判断仍由招聘负责人和面试官做，Kanban 只负责流程推进和记录交接。

##### 17.9.10.1 流程使用的 profile
这个流程使用这些 profile：

- `resume-screener`：提取简历信息，检查硬性条件
- `role-matcher`：匹配岗位、级别和团队方向
- `interview-planner`：生成面试问题、评分表和关注点
- `scheduler`：协调面试时间，记录候选人可用时间段
- `hiring-reviewer`：汇总反馈，给出是否推进的建议

##### 17.9.10.2 创建候选人任务
每个候选人建议一个 task，tenant 使用招聘批次，workspace 指向候选人材料目录：

```bash
hermes kanban create "筛选候选人：后端工程师 A" \
  --tenant hiring-backend-2026w21 \
  --workspace dir:/home/user/hiring/2026w21/candidate-a \
  --idempotency-key "hiring:backend:2026w21:candidate-a" \
  --triage
```

批量导入时，可以用脚本读取候选人目录并创建 task：

```bash
for dir in /home/user/hiring/2026w21/*; do
  [ -d "$dir" ] || continue
  name="$(basename "$dir")"

  hermes kanban create "筛选候选人：$name" \
    --tenant hiring-backend-2026w21 \
    --workspace "dir:$dir" \
    --idempotency-key "hiring:backend:2026w21:$name" \
    --triage
done
```

##### 17.9.10.3 任务图
典型任务图如下：

```text
候选人 task -> 简历初筛 -> 岗位匹配 -> 面试问题 -> 面试安排 -> 反馈汇总 -> 人工决策
```

如果候选人信息不完整，`resume-screener` 可以阻塞任务：

```bash
hermes kanban comment t_abcd1234 "简历缺少最近两段经历的项目说明，需要 HR 补充材料。"
hermes kanban block t_abcd1234 "等待 HR 补充候选人材料"
```

面试结束后，面试官或 `hiring-reviewer` 可以把反馈写入任务：

```bash
hermes kanban comment t_abcd1234 "一面反馈：系统设计基础扎实，数据库索引和缓存一致性需要二面继续确认。"
hermes kanban complete t_abcd1234 --result "建议进入二面；关注缓存一致性、线上排障经验和跨团队沟通。"
```

Kanban 的价值在于流程透明和可审计：每个候选人的材料、阻塞原因、面试安排、反馈和推进结论都有记录；人工判断仍然保留在流程末端。

### 质检应用
#### 17.9.11 合规审计证据收集
场景：准备 SOC 2、ISO 27001、等保或客户安全审查时，需要从代码仓库、云平台、工单系统、监控系统和制度文档里收集证据，核对缺口，补整改项，并生成审计包。

##### 17.9.11.1 流程使用的 profile
这个流程使用这些 profile：

- `evidence-collector`：按控制项收集截图、导出文件、配置和日志
- `cloud-auditor`：检查 IAM、网络、备份、加密和日志配置
- `policy-writer`：整理制度文档、流程说明和责任人
- `gap-analyst`：识别缺失证据和不满足项
- `ops`：执行整改，例如补监控、补备份、调整权限
- `reviewer`：审查证据包是否完整、可追溯、不过度暴露敏感信息

##### 17.9.11.2 创建审计 root task
审计项目通常是一次性或季度性任务，直接创建 root task：

```bash
mkdir -p /home/user/audit/soc2-q2

hermes kanban create "准备 Q2 SOC 2 审计证据包" \
  --tenant audit-soc2-q2 \
  --workspace dir:/home/user/audit/soc2-q2 \
  --triage
```

审计目录可以按控制项组织：

```text
/home/user/audit/soc2-q2/
├── CC6-access-control/
├── CC7-monitoring/
├── A1-availability/
└── policies/
```

##### 17.9.11.3 任务图
典型任务图如下：

```text
审计范围确认 -> 控制项拆分 -> 证据收集 -> 缺口分析 -> 整改任务 -> 证据包审查
```

如果发现缺口，`gap-analyst` 可以创建整改任务：

```bash
mkdir -p /home/user/audit/soc2-q2/CC7-monitoring

hermes kanban create "整改 CC7：补齐生产告警升级记录" \
  --assignee ops \
  --tenant audit-soc2-q2 \
  --workspace dir:/home/user/audit/soc2-q2/CC7-monitoring \
  --parent t_8888bbbb \
  --body "补充最近 90 天 P1/P2 告警、升级记录、处理人和关闭时间，并生成 evidence-index.md。"
```

等待第三方材料时，可以阻塞对应控制项：

```bash
hermes kanban comment t_9999cccc "缺少 IdP 管理员导出，需要 IT 提供最新用户和角色列表。"
hermes kanban block t_9999cccc "等待 IT 导出 IdP 管理员列表"
```

Kanban 的价值在于证据可追踪：每个控制项都是独立 task，可以记录证据来源、责任人、缺口和整改结果；最终 root task 汇总所有证据和遗留风险，适合交给审计方或客户安全团队。
