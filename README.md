# Hermes Agent
https://hermes-agent.nousresearch.com/docs

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [快速上手](#2-快速上手)
3. [配置文件与配置管理](#3-配置文件与配置管理)
4. [会话管理](#4-会话管理)
5. [Dashboard](#5-dashboard)
6. [Toolsets](#6-toolsets)
7. [MCP 服务器集成](#7-mcp-服务器集成)
8. [Skills](#8-skills)
9. [Plugins](#9-plugins)
10. [Hooks](#10-hooks)
11. [持久记忆](#11-持久记忆)
12. [上下文文件](#12-上下文文件)
13. [消息平台集成（Gateway）](#13-消息平台集成gateway)
14. [Profile](#14-profile)
15. [定时任务（Cron）](#15-定时任务cron)
16. [子 Agent 与任务委派（Delegation）](#16-子-agent-与任务委派delegation)
17. [Kanban（任务看板）](#17-kanban任务看板)

# 1. Hermes Agent 是什么
Hermes Agent 是由 Nous Research 开发的开源 AI Agent 框架。它运行在终端、消息平台（Telegram、Discord、Slack 等）和 IDE 中，能够自主调用工具完成任务。

Hermes 的独特优势：
- **技能自进化** — Hermes 能从经验中学习。解决复杂问题后，会保存可复用的流程为 Skill，下次遇到类似任务直接加载。
- **跨会话持久记忆** — 记住用户身份与偏好、环境细节和经验教训。
- **多平台网关** — 同一个 Agent 在 Telegram、Discord、Slack 等 10+ 平台上运行，且拥有完整的工具访问权限。
- **Profile** — 运行多个互相隔离的 Hermes 实例，各有独立的配置、会话、技能和记忆。
- **可扩展** — 插件系统、MCP 服务器、自定义工具、Webhook 触发、定时任务。

# 2. 快速上手
## 2.1 安装
https://hermes-agent.nousresearch.com/docs/getting-started/installation

安装前请确认 git 可用。

### 2.1.1 Linux / macOS / WSL2
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 2.1.2 Windows（PowerShell）
```powershell
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

## 2.2 初次配置
```bash
# 交互式选择模型和提供商
hermes model

# 或运行完整设置向导
hermes setup
```

API Key 存储在 `~/.hermes/.env` 文件中。

## 2.3 交互式对话
```bash
# 启动交互式对话
hermes

# 启动交互式对话，使用 TUI
hermes --tui
```

## 2.4 单次对话（非交互式）
```bash
hermes chat -q "查看系统资源占用情况"
```

适合脚本调用或一次性任务。

## 2.5 常用快捷键
| 快捷键         | 功能                                         |
| -------------- | -------------------------------------------- |
| `Alt + V`      | 从剪贴板粘贴图像                             |
| `Ctrl + C`     | 中断当前操作                                 |
| `Ctrl + D`     | 退出会话                                     |
| `Ctrl + Z`     | 暂停并挂起到后台，`fg` 恢复                  |
| `Ctrl + Enter` | 输入多行文本（Windows 需用此代替 Alt+Enter） |

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
├── SOUL.md         # 主 agent 身份标识（系统提示词中的第 1 个槽位）
├── memories/       # 持久化记忆（MEMORY.md、USER.md）
├── skills/         # 技能
├── cron/           # 定时任务
├── sessions/       # 会话
└── logs/           # 日志（errors.log、gateway.log — 密钥自动脱敏）
```

## 3.2 配置管理命令
```bash
# 查看当前配置
hermes config

# 用 $EDITOR 打开 config.yaml 编辑
hermes config edit

# 直接设置某个配置项
hermes config set section.key value
```

会话内也可以通过斜杠命令调整配置：
https://hermes-agent.nousresearch.com/docs/reference/slash-commands#configuration

| 命令                           | 功能             |
| ------------------------------ | ---------------- |
| `/config`                      | 查看当前配置     |
| `/model [model-name]`          | 查看或切换模型   |
| `/personality [name]`          | 设置性格         |
| `/reasoning [level/show/hide]` | 设置推理级别     |
| `/voice [on/off/tts/status]`   | 设置语音模式     |
| `/yolo`                        | 切换绕过确认模式 |

## 3.3 常用配置
### 3.3.1 命令确认模式
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#smart-approvals

```yaml
approvals:
  mode: manual  # manual | smart | off
# manual    — 每次高危操作都询问（默认）
# smart     — 用辅助模型自动判断风险，低风险直接执行
# off       — 跳过所有确认（等同于 --yolo）
```

### 3.3.2 上下文压缩
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#context-compression

```yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 压缩触发阈值
  target_ratio: 0.20  # 触发压缩的消息中多少比例的消息保留不压缩
  protect_last_n: 20  # 最少保留不压缩的最近消息数
```

### 3.3.3 记忆配置
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#memory-configuration

```yaml
memory:
  memory_enabled: true        # 启用持久记忆
  user_profile_enabled: true  # 启用用户档案
  memory_char_limit: 2200     # 记忆字符上限（约 800 tokens）
  user_char_limit: 1375       # 用户档案字符上限（约 500 tokens）
```

### 3.3.4 子 Agent 行为
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#delegation

```yaml
delegation:
  max_concurrent_children: 3  # 每个批次并行运行的最大子 Agent 数量
  max_spawn_depth: 1          # 最大子 Agent 嵌套深度
  orchestrator_enabled: true  # 可否生成 Orchestrator 子 Agent，为 false 时只能生成叶子 Agent
```

# 4. 会话管理
https://hermes-agent.nousresearch.com/docs/user-guide/sessions

每一次与 Hermes 的对话都是一个会话（Session），系统会自动保存和索引。

## 4.1 基本操作
```bash
# 列出近期会话
hermes sessions list

# 交互式会话选择器
hermes sessions browse

# 继续上次会话
hermes --continue
hermes -c

# 按 ID 或标题恢复特定会话
hermes --resume 20250225_143052_a1b2c3
hermes -r "我的项目设置"

# 重命名会话（方便后续恢复）
hermes sessions rename 20250225_143052_a1b2c3 "后端 API 开发"

# 删除会话
hermes sessions delete session_id

# 清理旧会话（保留最近 30 天）
hermes sessions prune --older-than 30
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

Hermes 同时将会话数据保存在两处位置：
- SQLite 数据库（`~/.hermes/state.db`）——结构化会话元数据，支持 FTS5 全文搜索。采用 WAL（预写日志）模式，支持并发读取和单个写入。
- JSONL 文件（`~/.hermes/sessions/`）——原始对话转录

SQLite 中包含如下表：

| 表                       | 内容                                                                                                     |
| ------------------------ | -------------------------------------------------------------------------------------------------------- |
| `sessions`               | 会话元数据：会话 ID、来源平台、用户 ID、模型配置、系统提示词、会话标题等                                 |
| `messages`               | 完整消息历史：所属会话、角色、正文、工具调用 ID、工具调用 JSON、工具名称、时间戳、结束原因、推理内容等   |
| `state_meta`             | 键值元数据表，用于记录状态型信息                                                                         |
| `schema_version`         | 数据库 schema 版本号，用于迁移判断                                                                       |
| `messages_fts`           | FTS5 虚拟表，使用 `unicode61` 分词器，索引 `content + tool_name + tool_calls`，适合英文/拉丁语系全文搜索 |
| `messages_fts_trigram`   | FTS5 虚拟表，使用 `trigram` 分词器，索引同一份消息文本，适合 CJK（中日韩）子串搜索                       |
| `messages_fts_*`         | `messages_fts` 的 FTS5 影子表，包括 `_data`、`_idx`、`_content`、`_docsize`、`_config`                   |
| `messages_fts_trigram_*` | `messages_fts_trigram` 的 FTS5 影子表，包括 `_data`、`_idx`、`_content`、`_docsize`、`_config`           |
| `sqlite_sequence`        | SQLite 自增主键计数表，由 `messages.id` 的 `AUTOINCREMENT` 自动维护                                      |

JSONL 转录文件包含每个会话的 `.jsonl` 文件和 `sessions.json` Gateway 索引文件。

## 4.4 会话搜索工具
https://hermes-agent.nousresearch.com/docs/user-guide/sessions#session-search-tool

Agent 内置 `session_search` 工具，使用 SQLite 的 FTS5 引擎对所有过去的对话执行全文搜索。

工作原理：

1. **查询路由**：非 CJK 查询走标准 `messages_fts`；CJK 查询优先走 `messages_fts_trigram`，短 CJK 或混合查询会退回 `LIKE` 子串匹配
2. **匹配与上下文**：FTS5 路径返回命中词附近的高亮片段；每个命中还会附带前后各 1 条消息作为上下文
3. **按会话分组**：取匹配度最高的前 N 个唯一会话（默认 3）
4. **智能截断**：以匹配位置为中心将会话截断至约 10 万字符
5. **摘要生成**：由快速辅助模型生成聚焦摘要
6. **返回结果**：返回包含元数据和上下文信息的会话摘要

自动触发：Agent 被提示在「用户提及过往对话内容或怀疑存在相关历史上下文」时自动调用 `session_search`，无需用户手动搜索。

# 5. Dashboard
https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard

Hermes 提供了一个基于浏览器的 Web 管理界面，替代手动编辑 YAML 和 CLI 命令，用于配置管理、API 密钥设置和会话监控。

## 5.1 启动与配置
```bash
hermes dashboard              # 启动，自动打开浏览器 http://127.0.0.1:9119
hermes dashboard --port 8080  # 自定义端口
hermes dashboard --tui        # 开启 Chat 标签页
```

# 6. Toolsets
https://hermes-agent.nousresearch.com/docs/user-guide/features/tools

工具（Tools）是 Hermes 调用外部能力的基本单元——搜索网页、执行命令、读写文件、控制浏览器等。工具按功能分组为「工具集」（Toolsets），可以按平台按需启用或禁用，从而精确控制 Agent 的能力范围。

## 6.1 基本操作
```bash
# 交互式管理工具（按平台配置）
hermes tools

# 查看所有工具及状态
hermes tools list

# 会话内查看/管理可用工具
/tools

# 切换工具执行展示模式（all → verbose → off → new）
/verbose
```

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

| 后端             | 说明                   | 适用场景                                 |
| ---------------- | ---------------------- | ---------------------------------------- |
| `local`          | 在本机直接执行（默认） | 本地开发、可信任务                       |
| `docker`         | 隔离容器中执行         | 安全隔离、可复现环境                     |
| `ssh`            | 远程服务器执行         | 沙箱化，防止 Agent 修改自身代码          |
| `singularity`    | HPC 容器（Apptainer）  | 集群计算、无 root 环境                   |
| `modal`          | 云端无服务器执行       | 弹性伸缩                                 |
| `daytona`        | 云端沙箱工作区         | 持久化远程开发环境                       |
| `vercel_sandbox` | Vercel 云端微虚拟机    | 部署与长期运行进程（Render、Railway 等） |

切换后端：
```bash
hermes config set terminal.backend docker
```

Docker 后端的关键行为：整个进程共享一个持久容器。后续所有 terminal、file、execute_code 调用都通过 `docker exec` 路由到同一容器。工作目录变更、安装的软件包、环境变量修改等在 `/workspace` 下的文件在整个 Hermes 进程生命周期内保持不变，`/new`、`/reset`、`delegate_task` 也不会重建容器。关闭时，该容器将被停止并移除。

## 6.4 Sudo 支持
当命令需要 sudo 权限时，终端会提示输入密码（会话内缓存）。也可以在 `~/.hermes/.env` 中设置 `SUDO_PASSWORD` 环境变量。

# 7. MCP 服务器集成
https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

MCP（Model Context Protocol）可以把外部工具服务器接入 Hermes。

## 7.1 添加 MCP 服务器
https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference

写入 `~/.hermes/config.yaml`：

```yaml
mcp_servers:
  project_fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]

  company_api:
    url: "https://mcp.internal.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

常用配置项：

| 配置项            | 说明                                   |
| ----------------- | -------------------------------------- |
| `command`         | 本地 stdio MCP Server 的启动命令       |
| `args`            | 传给启动命令的参数                     |
| `env`             | 传给 stdio server 的环境变量           |
| `url`             | 远程 HTTP MCP Server 地址              |
| `headers`         | 远程 HTTP 请求头                       |
| `auth: oauth`     | 对 HTTP server 启用 OAuth 2.1 授权流程 |
| `enabled`         | 是否启用该 server                      |
| `timeout`         | 工具调用超时时间                       |
| `connect_timeout` | 初次连接超时时间                       |

可以在每个 server 下配置 `tools.include` 或 `tools.exclude`，来控制注册工具白名单或黑名单：

```yaml
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

  billing:
    url: "https://mcp.billing.example.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer, refund_payment]
```

## 7.2 管理与重载
```bash
# 列出已配置的服务器
hermes mcp list

# 测试连接
hermes mcp test project-fs

# 管理服务器中的工具启用状态
hermes mcp configure project-fs

# 移除服务器
hermes mcp remove project-fs

# 修改配置后，在会话内重载 MCP 工具
/reload-mcp
```

Hermes 启动时会自动发现 MCP 工具。修改 `mcp_servers` 配置后，用 `/reload-mcp` 重新加载；如果 MCP Server 支持动态工具变更通知，Hermes 可以自动刷新工具列表。

# 8. Skills
https://hermes-agent.nousresearch.com/docs/user-guide/features/skills

已安装的技能会以斜杠命令的形式提供。

## 8.1 基本操作
https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-skills

```bash
# 列出已安装的技能
hermes skills list

# 浏览可用的技能
hermes skills browse

# 搜索技能
hermes skills search honcho

# 安装技能（通过 ID 或 URL）
hermes skills install honcho
hermes skills install https://example.com/my-skill/SKILL.md

# 卸载技能
hermes skills uninstall honcho

# 会话内管理技能
/skills
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

## 8.3 外部技能目录
如果团队已经有共享技能目录，比如 `~/.agents/skills/` 或公司内部 repo，可以编辑 `~/.hermes/config.yaml`，让 Hermes 额外扫描这些目录：

```yaml
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

Agent 通常会在这些场景创建或更新技能：

- 成功完成一个复杂任务（5 次以上工具调用）后
- 走过错误路径后找到了正确流程
- 用户纠正了它的做法
- 发现某个非显而易见、可复用的工作流

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

Curator 是 Hermes 的技能维护系统，专门管理由 Agent 创建或用户手写的技能。它会跟踪技能的查看、使用和修改频率，把长期不用的技能从 `active` 推进到 `stale`，再归档到 `~/.hermes/skills/.archive/`。

Curator 的存在是为了防止通过自我提升循环产生的技能无限累积。每次 Agent 解决一个新问题并保存一项技能时，该技能都会被添加到 `~/.hermes/skills/` 目录中。如果不进行维护，最终会导致数十个功能相近但范围狭窄的重复技能，这些技能不仅会污染目录，还会浪费 token。

### 8.5.1 运行机制
Curator 不是 cron 守护进程，而是在 Hermes 启动或 Gateway 后台 tick 时检查是否满足运行条件：

- 距离上次运行已经超过 `interval_hours`，默认 168 小时（7天）
- Agent 已经空闲超过 `min_idle_hours`，默认 2 小时

如果两个条件都成立，会在后台创建一个 AIAgent 分支，并按照两阶段运行：

1. **自动状态迁移**：不调用 LLM。超过 `stale_after_days` (30天) 未使用的技能变成 `stale`；超过 `archive_after_days` (90天) 未使用的技能移动到 `.archive/`。
2. **LLM Review**：启动一个辅助模型任务，查看 Agent 创建的技能，决定保留、修补、合并或归档。

### 8.5.2 配置
Curator 配置写在 `~/.hermes/config.yaml` 的 `curator:` 下：

```yaml
curator:
  enabled: true
  interval_hours: 168
  min_idle_hours: 2
  stale_after_days: 30
  archive_after_days: 90
```

Curator 的 LLM Review 可以单独指定更便宜的辅助模型进行维护任务：

```yaml
auxiliary:
  curator:
    provider: openrouter  # auto 代表使用主模型
    model: google/gemini-3-flash-preview
    timeout: 600
```

### 8.5.3 常用命令
```bash
# 查看技能状态
hermes curator status

# 手动运行策展
hermes curator run

# 后台运行
hermes curator run --background

# 只预览，不修改技能库
hermes curator run --dry-run

# 暂停 / 恢复自动运行
hermes curator pause
hermes curator resume

# 固定某个技能（防止被自动处理）
hermes curator pin my-important-skill

# 取消固定
hermes curator unpin my-important-skill

# 恢复已归档的技能
hermes curator restore my-skill
```

同样的子命令也可以在会话中通过 `/curator` 斜杠命令使用。

### 8.5.4 备份与回滚
每次 Curator 运行前，Hermes 会把 `~/.hermes/skills/` 打包备份到：

```text
~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz
```

如果某次维护结果不符合预期，可以回滚：

```bash
# 恢复最新备份
hermes curator rollback

# 跳过确认
hermes curator rollback -y

# 查看可用备份
hermes curator rollback --list

# 恢复指定备份
hermes curator rollback --id <timestamp>

# 手动创建快照
hermes curator backup --reason "before-refactor"
```

备份数量可配置：

```yaml
curator:
  backup:
    enabled: true
    keep: 5
```

### 8.5.5 哪些技能会被处理
Curator 只处理「非内置、非 Hub 安装」的技能。也就是说，不在这些记录里的技能都可能被处理：

- `~/.hermes/skills/.bundled_manifest`
- `~/.hermes/skills/.hub/lock.json`

这包括：

- Agent 通过 `skill_manage(action="create")` 创建的技能
- 用户创建的 `SKILL.md`
- 外部技能目录中暴露给 Hermes 的技能

如果某个技能很重要，建议先执行：

```bash
hermes curator pin <skill-name>
```

Pinned 技能不会被自动迁移到 `stale` 或 `archived`，Curator 的 LLM Review 也会避开它。Agent 的 `skill_manage` 工具也不能删除 pinned 技能，但仍然可以 patch/edit 改进内容。

### 8.5.6 使用记录与报告
Curator 会维护一个伴随文件 `~/.hermes/skills/.usage.json`，每个技能对应一个条目：

```jsonc
{
  "my-skill": {
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

内置技能和通过 Skills Hub 安装的技能不会写入这份文件。

每次 Curator 运行后，都会在 `~/.hermes/logs/curator/` 下写入一个带时间戳的目录：

```text
~/.hermes/logs/curator/
└── 20260429-111512/
    ├── run.json      # 机器可读：完整数据、统计信息、LLM 输出
    └── REPORT.md     # 人类可读：本次运行摘要
```

# 9. Plugins
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins

Hermes 拥有一个插件系统，无需修改核心代码即可添加自定义工具、钩子和集成。

## 9.1 插件能做什么
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins#what-plugins-can-do

插件通过 `register(ctx)` 函数接入 Hermes，`ctx` 上所有公开 API 均可使用。以下是完整扩展点：

| 扩展点             | 说明                                                                         |
| ------------------ | ---------------------------------------------------------------------------- |
| 注册工具           | 调用外部 API、调用本地服务、自定义逻辑                                       |
| 注册钩子           | 在会话开始、工具调用、消息处理等生命周期事件中执行额外逻辑                   |
| 注册斜杠命令       | 增加 `/name` 命令，CLI 和 Gateway 会话均可用                                 |
| 注册 CLI 子命令    | 增加 `hermes <plugin> <subcommand>`                                          |
| 从命令调度工具     | 在命令处理器中调用已注册工具，自动注入父 Agent 上下文                        |
| 注入消息           | 向当前会话注入外部消息。                                                     |
| 打包内置 Skill     | 插件附带 Skill，命名空间 `plugin:skill`，通过 `/<name>` 或 `skill_view` 加载 |
| 附带数据文件       | 标准 Python 路径，插件目录内任意组织                                         |
| 环境变量守卫       | 安装时提示用户设置必需的环境变量                                             |
| pip 分发           | 通过 Python entry point 注册，pip 安装即发现                                 |
| 注册消息平台       | 接入新 Gateway 平台                                                          |
| 注册图像生成后端   | 接入新的图像生成提供商                                                       |
| 注册上下文压缩引擎 | 接入自定义上下文压缩算法                                                     |
| 注册记忆后端       | 接入外部记忆系统：知识图谱、语义搜索、用户建模等                             |
| 注册推理后端       | 接入新的 LLM 模型提供商                                                      |
| 借用主模型调用 LLM | 复用用户的模型和认证执行一次性代码补全，可选 JSON Schema 校验                |

## 9.2 插件目录
用户插件目录 `~/.hermes/plugins/`，每个插件通常是一个独立目录，包含 `plugin.yaml` 和 Python 代码，例如：

```text
~/.hermes/plugins/my-plugin/
├── plugin.yaml      # 插件清单：名称、版本、描述等元信息
├── __init__.py      # register()：把 schema 连接到 handler
├── schemas.py       # tool schemas：模型能看到的工具定义
└── tools.py         # tool handlers：工具被调用时真正执行的逻辑
```

## 9.3 插件发现
Hermes 会从多个来源发现插件：

| 来源    | 路径 / 方式                         | 用途                     |
| ------- | ----------------------------------- | ------------------------ |
| Bundled | Hermes 仓库内置 `plugins/`          | 官方随 Hermes 发布的插件 |
| User    | `~/.hermes/plugins/`                | 用户自己的本地插件       |
| Project | `.hermes/plugins/`                  | 项目专属插件，默认关闭   |
| pip     | `hermes_agent.plugins` entry points | 通过 Python 包分发的插件 |

项目级插件需要显式信任，设置 `HERMES_ENABLE_PROJECT_PLUGINS=true` 才会被发现。

## 9.4 管理插件
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
plugins:
  enabled:
    - my-plugin
  disabled:
    - noisy-plugin
```

`plugins.disabled` 是拒绝列表，如果同一个插件同时出现在 `enabled` 和 `disabled`，禁用优先。

# 10. Hooks
https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks

Hermes 提供了三种钩子系统，允许在关键生命周期点执行自定义代码。所有钩子都是非阻塞设计，错误会被捕获并记录，不会影响 Agent 运行。

三种钩子对比：

| 维度     | Shell Hooks Shell 钩子                                | Plugin Hooks 插件钩子                  | Gateway Hooks 网关钩子           |
| -------- | ----------------------------------------------------- | -------------------------------------- | -------------------------------- |
| 语言     | 任意（Bash、Python、Go 等）                           | 仅 Python                              | 仅 Python                        |
| 运行环境 | CLI + Gateway                                         | CLI + Gateway                          | 仅 Gateway                       |
| 典型用例 | 即插即用脚本：阻止危险命令、自动格式化、注入 git 状态 | 工具拦截、指标采集、防护措施、记忆召回 | 日志记录、告警通知、Webhook 回调 |

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

`§` 用来分隔不同记忆条目，标题会显示当前容量占用，提醒 Agent 在接近上限时做合并或替换。

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

如果 `old_text` 匹配多个条目，工具会返回错误，要求提供更具体的片段。

## 11.3 记忆管理
记忆管理指令：

```python
MEMORY_GUIDANCE = (
    "You have persistent memory across sessions. Save durable facts using the memory "
    "tool: user preferences, environment details, tool quirks, and stable conventions. "
    "Memory is injected into every turn, so keep it compact and focused on facts that "
    "will still matter later.\n"
    "Prioritize what reduces future user steering — the most valuable memory is one "
    "that prevents the user from having to correct or remind you again. "
    "User preferences and recurring corrections matter more than procedural task details.\n"
    "Do NOT save task progress, session outcomes, completed-work logs, or temporary TODO "
    "state to memory; use session_search to recall those from past transcripts. "
    "Specifically: do not record PR numbers, issue numbers, commit SHAs, 'fixed bug X', "
    "'submitted PR Y', 'Phase N done', file counts, or any artifact that will be stale "
    "in 7 days. If a fact will be stale in a week, it does not belong in memory. "
    "If you've discovered a new way to do something, solved a problem that could be "
    "necessary later, save it as a skill with the skill tool.\n"
    "Write memories as declarative facts, not instructions to yourself. "
    "'User prefers concise responses' ✓ — 'Always respond concisely' ✗. "
    "'Project uses pytest with xdist' ✓ — 'Run tests with pytest -n 4' ✗. "
    "Imperative phrasing gets re-read as a directive in later sessions and can "
    "cause repeated work or override the user's current request. Procedures and "
    "workflows belong in skills, not memory."
)
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
| 速度       | 会话开始时直接进入系统提示词 | 需要搜索和模型摘要         |
| 用途       | 必须一直可见的关键事实       | 查找过去某次讨论的具体内容 |
| 管理方式   | Agent 主动维护、压缩、替换   | 自动保存所有会话           |
| token 成本 | 每个会话固定占用少量上下文   | 按需搜索时产生额外成本     |

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

也可以手动写入 `~/.hermes/config.yaml`：

```yaml
memory:
  provider: openviking
```

可选 provider 包括：

| Provider      | 重点功能 / 优势                                            |
| ------------- | ---------------------------------------------------------- |
| `honcho`      | 跨会话用户建模、session 级上下文、基于历史上下文的综合判断 |
| `openviking`  | 文件系统式知识层级、分层读取、自动抽取 6 类记忆            |
| `mem0`        | 服务端 LLM 事实抽取、语义搜索、重排和自动去重              |
| `hindsight`   | 知识图谱、实体关系、多策略检索、跨记忆综合                 |
| `holographic` | FTS5 全文搜索、信任评分、HRR 组合查询、冲突检测            |
| `retaindb`    | Vector + BM25 + Reranking 混合搜索、7 类记忆、增量压缩     |
| `byterover`   | CLI 驱动的层级知识树、分层检索、压缩前自动提取洞察         |
| `supermemory` | 语义长期记忆、用户画像、会话图谱摄取、上下文防污染         |

# 12. 上下文文件
https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files

Hermes Agent 会自动发现并加载上下文文件。

## 12.1 支持的上下文文件
| 文件                       | 用途                                   | 发现方式                        |
| -------------------------- | -------------------------------------- | ------------------------------- |
| `.hermes.md` / `HERMES.md` | Hermes 专用项目说明，优先级最高        | 从当前目录向上查找到 git root   |
| `AGENTS.md`                | 项目说明、架构、约定、注意事项         | 启动目录；子目录中可渐进发现    |
| `CLAUDE.md`                | 兼容 Claude Code 的上下文文件          | 启动目录；子目录中可渐进发现    |
| `.cursorrules`             | 兼容 Cursor 的项目规则                 | 启动目录                        |
| `.cursor/rules/*.mdc`      | Cursor 规则模块                        | 启动目录                        |
| `SOUL.md`                  | 当前 Hermes 实例的人格、语气和沟通风格 | 只从 `HERMES_HOME/SOUL.md` 加载 |

每个会话只加载一种上下文类型，优先级是：`.hermes.md` / `HERMES.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` / `.cursor/rules/*.mdc`。`SOUL.md` 独立加载，不参与这个优先级竞争。

## 12.2 加载流程与安全处理
启动时的加载流程：

1. 扫描当前工作目录，按优先级查找项目上下文文件
2. 以 UTF-8 文本格式读取
3. 执行安全扫描
4. 超过 20,000 字符时截断，保留头部和尾部
5. 组合到 `# Project Context` 部分并注入系统提示词

渐进加载流程：

1. Agent 通过工具（`read_file`、`terminal`、`search_files` 等）进入子目录后，从工具调用参数中检测文件路径
2. 检查该文件所在目录及最多 5 层父目录，遇到已访问过的目录则停止
3. 在每个目录中按 `AGENTS.md` → `CLAUDE.md` → `.cursorrules` 优先级查找，每个目录加载首个匹配项
4. 执行安全扫描
5. 超过 8,000 字符时截断
6. 内容追加到工具结果中，模型在上下文中自然看到，不修改系统提示词

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

1. **不可见 Unicode 检测** — 遍历 10 个危险字符（零宽空格 `​`、零宽连接符、BOM、双向文本覆盖符等），检查内容是否包含
2. **正则模式匹配** — 用 `re.IGNORECASE` 逐条匹配 10 条正则，每条对应一个威胁标签

```python
# ---------------------------------------------------------------------------
# Context file scanning — detect prompt injection in AGENTS.md, .cursorrules,
# SOUL.md before they get injected into the system prompt.
# ---------------------------------------------------------------------------

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
    """Scan context file content for injection. Returns sanitized content."""
    findings = []

    # Check invisible unicode
    for char in _CONTEXT_INVISIBLE_CHARS:
        if char in content:
            findings.append(f"invisible unicode U+{ord(char):04X}")

    # Check threat patterns
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

## 12.3 个性与灵魂
https://hermes-agent.nousresearch.com/docs/user-guide/features/personality

Hermes 的个性主要由 `SOUL.md` 控制。它是 Agent 的主身份文件，位于系统提示词的第 1 个槽位，用来定义 Hermes 是谁、怎么说话、默认沟通风格是什么。默认位置在 `~/.hermes/SOUL.md`。

`SOUL.md` 文件为空或读取失败时，回退到内置默认身份。如果文件有内容，经过安全扫描和截断后原样注入系统提示词。

`SOUL.md` 适合写长期稳定的个性和沟通偏好：

- 语气
- 风格
- 直接程度
- 默认互动方式
- 不希望出现的表达习惯
- 面对不确定性、分歧、模糊需求时的处理方式

不适合写项目规则、文件路径、仓库约定、临时流程。这些应该放进 `AGENTS.md`。

`/personality` 是一个会话级别的覆盖层，用于临时更改或补充当前的系统提示，包含下列人格：

| 人格          | 说明                      |
| ------------- | ------------------------- |
| `helpful`     | 友好的通用助手            |
| `concise`     | 简短、直接、少废话        |
| `technical`   | 详细、准确的技术专家      |
| `creative`    | 创新、发散、跳出常规思路  |
| `teacher`     | 耐心教学，配合清晰示例    |
| `kawaii`      | 可爱表达、闪亮感和高热情★ |
| `catgirl`     | 猫娘风格，带猫系表达，喵~ |
| `pirate`      | 技术海盗船长风格          |
| `shakespeare` | 莎士比亚式戏剧化文风      |
| `surfer`      | 放松随性的冲浪者语气      |
| `noir`        | 黑色侦探小说式叙述        |
| `uwu`         | 极致可爱和 uwu 风格表达   |
| `philosopher` | 对每个问题进行深度思辨    |
| `hype`        | 精力充沛，热情高涨！！！  |

# 13. 消息平台集成（Gateway）
https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

Hermes 可以通过 Gateway 运行在消息平台上。

## 13.1 命令
```bash
# 交互式配置消息平台
hermes gateway setup

# 前台启动 Gateway
hermes gateway

# 安装为用户服务（Linux）/ launchd 服务（macOS）
hermes gateway install

# 仅 Linux：安装为开机启动的系统服务
sudo hermes gateway install --system

# 启动默认服务
hermes gateway start

# 停止默认服务
hermes gateway stop

# 查看默认服务状态
hermes gateway status

# 仅 Linux：检查系统服务状态
hermes gateway status --system
```

## 13.2 网关配对
默认情况下，网关会拒绝所有不在允许列表中或未通过私信配对的用户。

这是安全默认值：Gateway 背后的 Agent 可能拥有终端、文件、浏览器、MCP 等工具权限，不应该让任意聊天用户直接访问。

**方式一：配置允许列表**

推荐显式写入可信用户 ID：

这些配置通常写在 `~/.hermes/.env` 中。

```bash
# 按平台限制用户
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=123456789012345678
SIGNAL_ALLOWED_USERS=+155****4567,+155****6543
SMS_ALLOWED_USERS=+155****4567,+155****6543
EMAIL_ALLOWED_USERS=trusted@example.com,colleague@work.com
MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c
MATRIX_ALLOWED_USERS=@alice:matrix.org
DINGTALK_ALLOWED_USERS=user-id-1
FEISHU_ALLOWED_USERS=ou_xxxxxxxx,ou_yyyyyyyy
WECOM_ALLOWED_USERS=user-id-1,user-id-2
WECOM_CALLBACK_ALLOWED_USERS=user-id-1,user-id-2
TEAMS_ALLOWED_USERS=aad-object-id-1,aad-object-id-2

# 或配置通用允许列表
GATEWAY_ALLOWED_USERS=123456789,987654321
```

也可以显式允许所有用户，但不推荐给有终端访问权限的 bot 使用：

```bash
GATEWAY_ALLOW_ALL_USERS=true
```

**方式二：私信配对**

如果不想手动查用户 ID，未知用户私信 bot 时会收到一次性配对码：

```text
Pairing code: XKGH5N7P
```

管理员在本机批准：

```bash
hermes pairing approve telegram XKGH5N7P
```

其他配对命令：

```bash
hermes pairing list
hermes pairing revoke telegram 123456789
```

配对码 1 小时后过期，有速率限制，并使用加密随机数生成。

**斜杠命令权限控制**

用户通过允许列表或配对后，还可以继续分成 admin 和普通 user。admin 可以运行所有斜杠命令；普通 user 只能运行显式允许的命令，以及始终允许的 `/help` 和 `/whoami`。

示例配置：

```yaml
gateway:
  platforms:
    discord:
      extra:
        allow_from: ["111", "222", "333"]
        allow_admin_from: ["111"]
        user_allowed_commands: [status, model]
        group_allow_admin_from: ["111"]
        group_user_allowed_commands: [status]
```

注意：

- 普通聊天不受斜杠命令权限影响，非 admin 用户仍然可以正常和 Agent 对话
- 私信里的 admin 身份不会自动继承到群组 / 频道，每个 scope 都有自己的权限列表
- 如果某个 scope 没有设置 `allow_admin_from`，该 scope 会保持向后兼容，不启用斜杠命令分级
- 可以在消息平台里发送 `/whoami` 查看自己当前是 admin、user 还是 unrestricted，以及能运行哪些命令

# 14. Profile
https://hermes-agent.nousresearch.com/docs/user-guide/profiles

通过 Profile 运行多个独立的 Hermes 实例，各自有独立的配置、会话、技能和记忆。

## 14.1 为什么用 Profile？
- **工作/个人分离** — 不同的 API key、模型、技能集
- **项目隔离** — 每个项目有自己的配置和环境
- **团队协作** — 不同的角色使用不同的工具集

## 14.2 管理 Profile
```bash
# 列出所有 Profile
hermes profile list

# 创建新的 Profile
hermes profile create work

# 从现有 Profile 克隆
hermes profile create project-x --clone work
hermes profile create all-in --clone-all    # 克隆所有配置

# 查看 Profile 详情
hermes profile show work

# 切换默认 Profile
hermes profile use work

# 导出 Profile 为压缩包（方便迁移）
hermes profile export work

# 导入 Profile
hermes profile import work.tar.gz

# 创建别名（wrapper 脚本）
hermes profile alias work

# 删除 Profile
hermes profile delete work

# 重命名
hermes profile rename work personal
```

## 14.3 使用 Profile
```bash
# 启动时指定 Profile
hermes -p work

# 启动并使用 worktree 模式
hermes -p work -w
```

Profile 的数据存储在 `~/.hermes/profiles/<name>/` 目录下，结构和主目录一致。

# 15. 定时任务（Cron）
Hermes 内置了定时任务系统，让 Agent 在指定时间自动执行任务。

## 15.1 创建任务
```bash
# 每 30 分钟执行一次
hermes cron create "30m" --prompt "检查我的服务器状态并报告"

# 每天早 9 点
hermes cron create "0 9 * * *" --prompt "生成每日报告"

# 指定时间（ISO 格式）
hermes cron create "2025-03-01T09:00:00" --prompt "..."
```

## 15.2 管理任务
```bash
hermes cron list          # 列出任务（--all 包含已禁用的）
hermes cron pause ID      # 暂停任务
hermes cron resume ID     # 恢复任务
hermes cron edit ID       # 编辑任务的调度、提示、投递方式
hermes cron run ID        # 立即触发
hermes cron remove ID     # 删除任务
hermes cron status        # 调度器状态
```

## 15.3 投递方式
任务的执行结果可以投递到指定平台：

```bash
# 默认投递到当前会话
# 投递到 Telegram
hermes cron create "30m" --prompt "..." --deliver "telegram:-1001234567890"
# 投递到所有已连接的平台
hermes cron create "30m" --prompt "..." --deliver "all"
```

## 15.4 高级用法
- **指定技能加载**：`hermes cron create "30m" -s "web,github-issues" --prompt "..."`
- **指定模型**：`hermes cron create "30m" --model "anthropic/claude-sonnet-4" --prompt "..."`
- **自定义脚本**：`hermes cron create "30m" --script "~/monitor.sh"`

# 16. 子 Agent 与任务委派（Delegation）
Hermes 可以创建子 Agent 来处理独立的任务。子 Agent 有自己的对话和终端环境，互不干扰。

## 16.1 什么时候用委派？
- **并行独立任务** — 同时处理多个互不依赖的任务
- **需要隔离环境** — 子 Agent 运行在独立工作目录
- **减少上下文干扰** — 子 Agent 的详细输出不会污染主会话的上下文

## 16.2 使用方式
通过 `delegate_task` 工具创建子 Agent。支持两种模式：

**单任务模式：**

提供一个目标和上下文，子 Agent 执行后返回摘要。

**批量并行模式（最多 3 个子 Agent 并行）：**

同时派发多个任务，所有子 Agent 并行执行，结果一并返回。

## 16.3 委派 vs 独立进程
|          | delegate_task          | 独立 hermes 进程 |
| -------- | ---------------------- | ---------------- |
| 隔离性   | 独立对话，共享进程     | 完全独立进程     |
| 持续时间 | 分钟级（受限于父循环） | 小时/天级        |
| 工具访问 | 父进程的子集           | 完整工具权限     |
| 交互性   | 无                     | 有（PTY 模式）   |
| 适用场景 | 快速并行子任务         | 长期自主任务     |

# 17. Kanban（任务看板）
Hermes 提供了一个基于看板的轻量级任务跟踪系统，用于管理工作项和任务进度。

## 17.1 暂空
