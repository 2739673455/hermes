# Hermes Agent
https://hermes-agent.nousresearch.com/docs

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [快速上手](#2-快速上手)
3. [配置文件与配置管理](#3-配置文件与配置管理)
4. [会话管理](#4-会话管理)
5. [Dashboard](#5-dashboard)
6. [Toolsets](#6-toolsets)
7. [MCP](#7-mcp)
8. [Skills](#8-skills)
9. [Plugins](#9-plugins)
10. [Hooks](#10-hooks)
11. [持久记忆](#11-持久记忆)
12. [上下文文件](#12-上下文文件)
13. [Gateway](#13-gateway)
14. [Profile](#14-profile)
15. [Cron](#15-cron)
16. [Delegation](#16-delegation)
17. [Kanban](#17-kanban)

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

## 4.4 上下文压缩
当会话上下文接近模型限制时，Hermes 会自动压缩历史消息，保留关键信息并维持上下文窗口可用。

```yaml
# ~/.hermes/config.yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 压缩触发阈值
  target_ratio: 0.20  # 触发压缩的消息中多少比例的消息保留不压缩
  protect_last_n: 20  # 最少保留不压缩的最近消息数
```

也可通过 `/compress` 斜杠命令手动触发压缩。

## 4.5 会话搜索工具
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
hermes dashboard                       # 启动，自动打开浏览器 http://127.0.0.1:9119
hermes dashboard --port 8080           # 自定义端口
hermes dashboard --tui                 # 开启 Chat 标签页
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

# 7. MCP
https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

MCP（Model Context Protocol）可以把外部工具服务器接入 Hermes。

## 7.1 添加 MCP 服务器
https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference

配置示例：

```yaml
# ~/.hermes/config.yaml
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

触发策略主要靠提示词驱动，但不是只有一条提示词。Hermes 会从三个地方推动 Agent 创建或更新技能：

1. **主对话系统提示词**：当 `skill_manage` 工具可用时，系统提示词会注入 `SKILLS_GUIDANCE`，要求 Agent 在完成复杂任务、修复棘手错误、发现非平凡工作流后，把做法保存成 Skill；如果加载过的 Skill 有过时、缺步骤或错误，也要立即 `patch`。
2. **工具 schema 提示词**：`skill_manage` 的工具描述本身也会告诉模型什么时候该 `create` 或 `patch`。典型信号包括：复杂任务成功、走过错误路径后找到正确流程、用户纠正后的做法有效、发现可复用工作流、用户要求记住某个流程。
3. **后台 self-improvement review**：运行过程中 Hermes 会统计工具调用迭代数。达到 `skills.creation_nudge_interval` 后，回合结束时会 fork 一个后台 `AIAgent`，用专门的 review prompt 回顾本轮对话，只允许调用 memory/skill 工具，并决定是否 `patch` 现有 Skill、写入 `references/` 等支持文件，或创建新的类别级 Skill（class-level Skill）。

提示词摘要：

**提示词：`SKILLS_GUIDANCE`**

- **位置**：`agent/prompt_builder.py`
- **作用**：指导 Agent 在复杂任务、错误修复或发现工作流后保存/修补 Skill
- **注入位置**：`skill_manage` 工具可用时，随主对话系统提示词注入

原文摘录：

```text
After completing a complex task (5+ tool calls), fixing a tricky error,
or discovering a non-trivial workflow, save the approach as a
skill with skill_manage so you can reuse it next time.

When using a skill and finding it outdated, incomplete, or wrong,
patch it immediately with skill_manage(action='patch') — don't wait to be asked.
Skills that aren't maintained become liabilities.
```

中文对照：完成复杂任务（5 次以上工具调用）、修复棘手错误，或发现非平凡工作流后，用 `skill_manage` 把这个方法保存成 Skill，以便下次复用。使用 Skill 时，如果发现它过时、不完整或错误，立即用 `skill_manage(action='patch')` 修补，不要等用户要求。没有被维护的 Skill 会变成负担。

**提示词：Skills 列表注入提示词**

- **位置**：`agent/prompt_builder.py`
- **作用**：要求 Agent 加载相关 Skill，并在发现 Skill 问题时修补
- **注入位置**：构建可用 Skills 列表时，随系统提示词注入

原文摘录：

```text
If a skill has issues, fix it with skill_manage(action='patch').
After difficult/iterative tasks, offer to save as a skill.
If a skill you loaded was missing steps, had wrong commands, or needed
pitfalls you discovered, update it before finishing.
```

中文对照：如果 Skill 有问题，用 `skill_manage(action='patch')` 修复。困难或迭代型任务后，提出把它保存为 Skill。如果加载过的 Skill 缺少步骤、命令错误，或需要加入你发现的坑点，在结束前更新它。

**提示词：`skill_manage` 工具 schema description**

- **位置**：`tools/skill_manager_tool.py`
- **作用**：在工具定义里告诉模型何时 `create`、`patch`、跳过或确认
- **出现位置**：`skill_manage` 作为可调用工具暴露给模型时

原文摘录：

```text
Create when: complex task succeeded (5+ calls), errors overcome,
user-corrected approach worked, non-trivial workflow discovered,
or user asks you to remember a procedure.

Update when: instructions stale/wrong, OS-specific failures,
missing steps or pitfalls found during use.
If you used a skill and hit issues not covered by it, patch it immediately.

After difficult/iterative tasks, offer to save as a skill.
Skip for simple one-offs. Confirm with user before creating/deleting.
```

中文对照：创建条件：复杂任务成功（5 次以上调用）、克服错误、用户纠正后的方法有效、发现非平凡工作流，或用户要求你记住某个流程。更新条件：说明过时或错误、出现 OS 相关失败、使用中发现缺少步骤或坑点。如果使用某个 Skill 时遇到它没有覆盖的问题，立即修补它。困难或迭代型任务后，提出保存为 Skill。跳过简单的一次性任务。创建或删除前先和用户确认。

**提示词：`_SKILL_REVIEW_PROMPT`**

- **位置**：`run_agent.py`
- **作用**：后台回顾本轮对话并更新 Skill library
- **触发条件**：工具调用迭代数达到 `skills.creation_nudge_interval`，回合结束后 fork 后台 review agent

原文摘录：

```text
Review the conversation above and update the skill library. Be
ACTIVE — most sessions produce at least one skill update, even if
small. A pass that does nothing is a missed learning opportunity,
not a neutral outcome.

Signals to look for (any one of these warrants action):
  • User corrected your style, tone, format, legibility, or verbosity.
  • User corrected your workflow, approach, or sequence of steps.
  • Non-trivial technique, fix, workaround, debugging path, or
    tool-usage pattern emerged that a future session would benefit from.
  • A skill that got loaded or consulted this session turned out
    to be wrong, missing a step, or outdated. Patch it NOW.

Preference order:
  1. UPDATE A CURRENTLY-LOADED SKILL.
  2. UPDATE AN EXISTING UMBRELLA.
  3. ADD A SUPPORT FILE under an existing umbrella.
  4. CREATE A NEW CLASS-LEVEL UMBRELLA SKILL when no existing
     skill covers the class.
```

中文对照：回顾上面的对话并更新技能库。要主动；多数会话至少会产生一个 Skill 更新，即使很小。什么都不做不是中性结果，而是错过学习机会。需要寻找的信号包括：用户纠正了风格、语气、格式、可读性或详细程度；用户纠正了工作流、方法或步骤顺序；出现了未来会话可受益的非平凡技巧、修复、绕过方法、调试路径或工具使用模式；本轮加载或查阅过的 Skill 被发现错误、缺少步骤或过时。优先顺序：更新当前已加载的 Skill；更新已有总括型 Skill（umbrella Skill）；在已有总括型 Skill 下添加支持文件；当没有现有 Skill 覆盖这个类别时，创建新的类别级总括型 Skill（class-level umbrella Skill）。

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

**提示词：`CURATOR_REVIEW_PROMPT`**

- **位置**：`agent/curator.py`
- **作用**：指导 Curator 做 Skill 合并、归档和总括型 Skill 整理
- **触发条件**：Curator 满足运行条件并进入 LLM Review 阶段

原文摘录：

```text
You are running as Hermes' background skill CURATOR. This is an
UMBRELLA-BUILDING consolidation pass, not a passive audit and not a
duplicate-finder.

The goal of the skill collection is a LIBRARY OF CLASS-LEVEL
INSTRUCTIONS AND EXPERIENTIAL KNOWLEDGE. A collection of hundreds of
narrow skills where each one captures one session's specific bug is
a FAILURE of the library — not a feature.

Hard rules — do not violate:
1. DO NOT touch bundled or hub-installed skills.
2. DO NOT delete any skill. Archiving is the maximum destructive action.
3. DO NOT touch skills shown as pinned=yes. Skip them entirely.
4. DO NOT use usage counters as a reason to skip consolidation.

How to work — not optional:
1. Scan the full candidate list. Identify PREFIX CLUSTERS.
2. For each cluster with 2+ members, ask what the UMBRELLA CLASS is.
3. Three ways to consolidate:
   a. MERGE INTO EXISTING UMBRELLA.
   b. CREATE A NEW UMBRELLA SKILL.md.
   c. DEMOTE TO REFERENCES/TEMPLATES/SCRIPTS.

'keep' is a legitimate decision ONLY when the skill is already a
class-level umbrella and none of the proposed merges would improve
discoverability.
```

中文对照：你正在作为 Hermes 的后台 Skill Curator（技能维护器）运行。这是一次构建总括型 Skill 的合并整理过程（umbrella-building consolidation pass），不是被动审计，也不是重复项查找。技能集合的目标是一个由类别级（class-level）指令和经验知识组成的库；如果有数百个狭窄 Skill，每个只记录某次会话里的具体 bug，那是技能库的失败，不是特性。硬性规则：不要触碰内置或 Hub 安装的 Skills；不要删除任何 Skill，归档是最大破坏性动作；不要触碰 `pinned=yes`（已固定）的 Skills，完全跳过；不要用使用计数（usage counters）作为跳过合并整理的理由。工作方式：扫描完整候选列表，识别前缀集群（PREFIX CLUSTERS）；对每个有 2 个以上成员的集群，询问它们共同服务的总括类别（umbrella class）是什么；三种合并方式是合并进现有总括型 Skill、创建新的总括型 `SKILL.md`、降级为 `references/`、`templates/` 或 `scripts/`。只有当 Skill 已经是类别级总括型 Skill（class-level umbrella），且任何拟议合并都不能改善可发现性时，`keep` 才是合法决定。

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
# ~/.hermes/config.yaml
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
# ~/.hermes/config.yaml
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

## 10.1 Shell Hook 示例：每次对话结束后弹出 Windows Toast 提醒
适合在 WSL / Git Bash / Windows 终端里使用 Hermes：当一次 `run_conversation()` 结束时，`on_session_end` 会触发脚本，通过 `powershell.exe` 弹出 Windows toast 通知。

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

# WSL / Git Bash / Windows 终端中通常可以直接调用 powershell.exe。
if command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -NoProfile -WindowStyle Hidden -Command '
    $appId = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

    $doc = [Windows.Data.Xml.Dom.XmlDocument]::new()
    $doc.LoadXml("<toast><visual><binding template=`"ToastGeneric`"><text>Hermes</text><text>Finished</text></binding></visual></toast>")
    $toast = [Windows.UI.Notifications.ToastNotification]::new($doc)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show($toast)
  ' >/dev/null 2>&1 &
fi

# 返回空 JSON，表示这个 hook 不修改 Hermes 的正常流程。
printf '{}\n'
```

这个脚本适用于常见的 Windows 10 / 11 + WSL / Git Bash / Windows 终端环境。脚本依赖 Windows 自带的 `powershell.exe` 和 Windows PowerShell 的系统 AppID 来发送 toast；如果通知没有出现，优先检查 Windows 的通知权限、请勿打扰 / 专注助手，以及 `Windows PowerShell` 的通知是否被关闭。

4. 赋予执行权限：

```bash
chmod +x ~/.hermes/agent-hooks/windows-session-end-popup.sh
```

首次运行时 Hermes 会询问是否允许这个 `(event, command)` 组合。

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

**提示词：`MEMORY_GUIDANCE`**

- **位置**：`agent/prompt_builder.py`
- **作用**：指导 Agent 何时写入 memory、何时不要写入 memory、何时改用 Skill
- **注入位置**：`memory` 工具可用时，随主对话系统提示词注入

原文摘录：

```text
You have persistent memory across sessions. Save durable facts using the memory
tool: user preferences, environment details, tool quirks, and stable conventions.
Memory is injected into every turn, so keep it compact and focused on facts that
will still matter later.

Prioritize what reduces future user steering — the most valuable memory is one
that prevents the user from having to correct or remind you again.
User preferences and recurring corrections matter more than procedural task details.

Do NOT save task progress, session outcomes, completed-work logs, or temporary TODO
state to memory; use session_search to recall those from past transcripts.
Specifically: do not record PR numbers, issue numbers, commit SHAs, 'fixed bug X',
'submitted PR Y', 'Phase N done', file counts, or any artifact that will be stale
in 7 days. If a fact will be stale in a week, it does not belong in memory.
If you've discovered a new way to do something, solved a problem that could be
necessary later, save it as a skill with the skill tool.

Write memories as declarative facts, not instructions to yourself.
'User prefers concise responses' ✓ — 'Always respond concisely' ✗.
'Project uses pytest with xdist' ✓ — 'Run tests with pytest -n 4' ✗.
Imperative phrasing gets re-read as a directive in later sessions and can
cause repeated work or override the user's current request. Procedures and
workflows belong in skills, not memory.
```

中文对照：你有跨会话持久记忆。用 `memory` 工具保存长期有效的事实：用户偏好、环境细节、工具使用习惯和稳定约定。记忆会注入每一轮，所以要保持紧凑，只保存以后仍然重要的事实。优先保存能减少用户未来重复纠正或提醒你的内容；用户偏好和反复纠正比流程性任务细节更重要。不要把任务进度、会话结果、完成记录或临时 TODO 状态保存到记忆里；这些应该用 `session_search` 从历史对话找回。不要记录 PR 编号、issue 编号、commit SHA、“修好了某 bug”、“提交了某 PR”、“第 N 阶段完成”、文件数量，或任何 7 天内会过期的东西。如果一个事实一周后会过期，它不属于记忆。如果发现了新的做法，或解决了以后可能还会需要的问题，把它保存成 Skill。记忆要写成陈述性事实，不要写成给自己的命令。命令式写法会在后续会话里被重新读成指令，导致重复工作或覆盖用户当前请求。流程和工作流属于 Skills，不属于 memory。

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

也可以手动配置：

```yaml
# ~/.hermes/config.yaml
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

# 13. Gateway
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
# 批准配对
hermes pairing approve telegram XKGH5N7P

# 查看配对列表
hermes pairing list

# 撤销配对
hermes pairing revoke telegram <user_id>
```

配对码 1 小时后过期，有速率限制，并使用加密随机数生成。

### 13.2.3 斜杠命令权限控制
用户通过允许列表或配对后，可以分成管理员和普通用户；如果当前平台/作用域未配置 `allow_admin_from`（包括没有对应的 gateway 平台配置），则默认不区分，所有已允许用户都可以运行斜杠命令。配置后，管理员可以运行所有斜杠命令；普通用户只能运行显式允许的命令，以及始终允许的 `/help` 和 `/whoami`。

示例配置：

```yaml
# ~/.hermes/config.yaml
gateway:
  platforms:
    discord:
      extra:
        allow_from: ["111", "222", "333"]       # 允许使用的用户
        allow_admin_from: ["111"]               # 管理员用户
        user_allowed_commands: [status, model]  # 非管理员可运行的命令
        group_allow_admin_from: ["111"]
        group_user_allowed_commands: [status]
```

# 14. Profile
https://hermes-agent.nousresearch.com/docs/user-guide/profiles

通过 Profile 运行多个独立的 Hermes Agent，每个 Agent 有独立的配置、会话、技能和记忆。

## 14.1 什么是 Profile
Profile 是一个独立的 Hermes home 目录。其中包含各自的 `config.yaml`、`.env`、`SOUL.md`、记忆、会话、技能、cron 任务、状态数据库和 Gateway 状态。

通过 Profile 可以运行用于不同用途的 Agent 而不会混淆 Hermes 状态。

创建 Profile 后，Hermes 会自动生成同名命令别名。例如创建 `coder` 后，可以直接使用 `coder chat`、`coder setup`、`coder gateway start`，本质上等价于 `hermes -p coder ...`。

## 14.2 创建 Profile
```bash
# 创建空白 Profile，会生成同名命令别名，内置技能会初始化
hermes profile create coder

# 克隆当前 Profile 的 config.yaml、.env、SOUL.md，不复制会话和记忆
hermes profile create coder --clone

# 克隆完整状态：配置、API key、人格、记忆、会话、技能、cron、plugins
hermes profile create backup --clone-all

# 从指定 Profile 克隆配置
hermes profile create coder --clone --clone-from backup

# 删除 Profile
hermes profile delete coder
```

## 14.3 使用 Profile
每个 Profile 都会自动生成同名命令别名，位置通常是 `~/.local/bin/<profile-name>`。

例如创建 `coder` 后：

```bash
coder chat
coder setup
coder gateway start
```

这个别名本质上等价于 `hermes -p <name>`。也可以显式指定 Profile：`hermes -p coder chat`。

如果希望普通 `hermes` 命令默认指向某个 Profile：

```bash
hermes profile use coder    # 默认使用 coder Profile
hermes                      # 现在默认使用 coder
hermes profile use default
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

Hermes 会在内部调用 `cronjob` 工具完成创建。

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
# 查看定时任务
/cron list
/cron list --all  # 查看所有任务，包括已暂停的任务

# 编辑定时任务
/cron edit <job_id> --schedule "every 4h"
/cron edit <job_id> --prompt "使用新的任务说明"
/cron edit <job_id> --skill blogwatcher --skill maps  # 替换当前任务的技能列表
/cron edit <job_id> --add-skill maps                  # 追加技能
/cron edit <job_id> --remove-skill blogwatcher        # 移除指定技能
/cron edit <job_id> --clear-skills                    # 清空所有技能
/cron edit <job_id> --repeat 5                        # 设置重复次数

# 任务生命周期
/cron pause <job_id>   # 暂停任务
/cron resume <job_id>  # 恢复任务
/cron run <job_id>     # 下一个 scheduler tick 触发任务
/cron remove <job_id>  # 删除任务

hermes cron status     # 查看调度器状态
hermes cron tick       # 手动触发一次 scheduler tick
```

任务存储在 `~/.hermes/cron/jobs.json`，运行输出会保存到 `~/.hermes/cron/output/{job_id}/{timestamp}.md`。

## 15.4 投递方式
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

如果 Agent 的最终回复以 `[SILENT]` 开头，成功运行时会抑制投递，但输出仍会保存到本地；失败任务仍会投递错误信息。这可用于哪些只有出现问题才需要报告的作业：

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

> 注意：`context_from` 读取的是上游任务「最近一次已完成输出」，不会等待同一个 tick 中仍在运行的上游任务。

# 16. Delegation
https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation

Hermes 可以创建子 Agent 来处理独立的任务。子 Agent 有自己的对话和终端环境，互不干扰。

## 16.1 单任务与并行批量
**单任务：**

```python
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"],
)
```

**并行批量（默认最多 3 并发，可通过 `max_concurrent_children` 调高）：**

```python
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]},
])
```

超过 `max_concurrent_children` 的批量请求会直接返回工具错误，不会静默截断。结果按输入顺序排列，不受完成先后影响。父 Agent 中断会传播到所有活跃子 Agent。

## 16.2 上下文模型
子 Agent 启动时拥有全新对话，不知道父会话之前的任何内容。子 Agent 的唯一上下文来自接收的 `goal` 和 `context` 两个字段：

- `goal`：任务目标（必填）
- `context`：完成目标所需的全部背景信息——错误详情、文件路径、项目位置、环境约束等，父 Agent 必须在此完整传递

子 Agent 完成后，只有结构化摘要（做了什么、发现了什么、改了什么、遇到的问题）回传到父会话，详细对话过程不保留，以此控制 token 开销。

## 16.3 工具集限制
可通过 toolsets 参数限制子 Agent 可用工具：

| toolsets                      | 适用场景             |
| ----------------------------- | -------------------- |
| `["terminal", "file"]`        | 编码、调试、文件编辑 |
| `["web"]`                     | 调研、查文档         |
| `["terminal", "file", "web"]` | 全栈任务（默认）     |
| `["file"]`                    | 只读分析、代码审查   |
| `["terminal"]`                | 系统管理、进程操作   |

某些工具子 Agent 无法使用（不受 `toolsets` 参数影响）：

| 工具             | 原因                                      |
| ---------------- | ----------------------------------------- |
| `delegation`     | 叶子节点禁止再次委派（orchestrator 保留） |
| `clarify`        | 子 Agent 不能与用户交互                   |
| `memory`         | 不写入共享持久记忆                        |
| `code_execution` | 子 Agent 应逐步推理                       |
| `send_message`   | 无跨平台副作用                            |

## 16.4 嵌套委派（Orchestrator）
默认委派是扁平的：父 Agent（深度 0）→ 子 Agent（深度 1，不可再委派）。如需多阶段工作流，可将子 Agent 角色设为 `orchestrator`：

```python
delegate_task(
    goal="Survey three approaches and recommend one",
    role="orchestrator",
    context="...",
)
```

- `role="leaf"`（默认）：不能再委派
- `role="orchestrator"`：保留 `delegation` 工具，由 `max_spawn_depth` 控制层级
- `max_spawn_depth: 1` → 扁平；设为 2 → orchestrator 可生成叶子孙子；设为 3 → 三层

## 16.5 配置
```yaml
# ~/.hermes/config.yaml
delegation:
  max_concurrent_children: 3   # 并行子 Agent 上限
  max_spawn_depth: 1           # 嵌套深度，1 = 扁平（默认），设为 2 允许 orchestrator 再生成叶子节点
  orchestrator_enabled: true   # false 时全局禁止嵌套委派，role="orchestrator" 也被强制降级为 leaf
  child_timeout_seconds: 600   # 子 Agent 静默超时（秒），超时无 API/工具调用即终止
  max_iterations: 50           # 子 Agent 最大工具调用轮次
  # model: "google/gemini-flash-2.0"   # 可选：为子 Agent 指定不同模型，省略则继承父 Agent 模型
  # provider: "openrouter"
```

# 17. Kanban
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://github.com/NousResearch/hermes-agent/blob/main/docs/hermes-kanban-v1-spec.pdf

Hermes Kanban 是一个多 Agent 协作层：它是一个可恢复、可审计、可中途介入的工作队列。它把任务、依赖、评论、运行记录和工作目录放进一个持久任务板里，让多个具名 profile 以异步方式协作。

## 17.1 为什么需要 Kanban
Hermes 已经有多 Agent 能力，但原有核心原语是 `delegate_task`：父 Agent 同步启动一个短生命周期子 Agent，等待它返回结果。这种模型适合短的、自包含的推理子任务；但当工作需要跨时间、跨角色、跨重启，或者需要人类中途插手时，`delegate_task` 的函数调用模型就不够了。

Kanban 的设计出发点是：把协作状态放到一个 Hermes 可控的持久层里，而不是放在某个父 Agent 的上下文窗口或第三方 SDK 的进程内生命周期里。任务、依赖、评论、运行结果和失败恢复都落到任务板上；每个执行者都是具名 profile，拥有自己的 `HERMES_HOME`、记忆、技能和工作目录。

### 17.1.1 `delegate_task` 的短板
#### 17.1.1.1 `delegate_task` 的当前实现
`delegate_task` 是同步“分叉并汇合”（fork-and-join）调用。父 Agent 构造一个 `goal` 和可选 `context`，启动一个隔离会话里的子 Agent，然后阻塞等待子 Agent 返回摘要。子 Agent 完成后，它的详细过程不会作为一个可继续协作的对象留在系统里；父 Agent 只拿到结构化摘要，并把这个摘要放回当前上下文继续推理。

这对“父 Agent 现在需要一个短答案才能继续”的场景是够用的。例如：

- 并行查几个资料点，然后汇总给父 Agent
- 检查一段代码变更是否有明显风险
- 跑一组局部验证命令并返回结果
- 对一个独立问题做短时间分析

这些任务的共同点是：

- 结果只需要回到父 Agent
- 不需要人类中途评论
- 失败时由父 Agent 重新发起
- 任务本身不需要成为长期可见、可恢复、可审计的对象

#### 17.1.1.2 `delegate_task` 无法覆盖的场景
`delegate_task` 无法覆盖如下场景：

1. **研究分流与综合（Research triage and synthesis）**：多个专家型 Agent 并行产出候选发现，一个或多个审查者选择、合并，人类还可能中途纠正方向。
2. **定时循环工作流（Scheduled recurring workflows）**：日报、周报、小时级收件箱分流等任务会跨运行积累知识，并且要能从单次失败中恢复。
3. **数字分身 / 持久助手角色（Digital-twin / persistent assistant roles）**：具名、长期存在的 Agent 身份会在数周或数月里积累对人、偏好和上下文的记忆。
4. **端到端工程流水线（End-to-end engineering pipelines）**：拆解、并行实现、审查、迭代、提交，整个流程可能持续数小时，并需要保留每个贡献者的身份和交接记录。

这些场景都需要同几类能力：

- 跨运行持久状态
- 工作进行中的可见性
- 不同技能 Agent 之间的交接
- 人类或对等 Agent 随时介入
 
### 17.1.2 其他系统的设计方案
#### 17.1.2.1 Cline Kanban
Cline Kanban 的形态是本地任务板：一个任务是一张卡片，每张卡片对应一个临时 git 工作树，并可以分配给不同命令行 Agent。卡片可以连成依赖链，父任务完成后子任务自动启动。

它的启发是：**任务板 + 依赖链接 + 工作目录** 本身就足以构成一个很有用的协调层。它没有账号系统、服务器基础设施、复杂治理，也不强调长期 Agent 身份。这个模型简单有效，但偏代码任务：git 工作树是核心假设，非代码工作和长期身份不是主要目标。

#### 17.1.2.2 Paperclip
Paperclip 把 Agent 建模成公司里的“员工”：有组织结构图、预算、治理、目标任务图、心跳、执行记录和每 Agent 的 API key 轮换。它强调持久 Agent 身份和原子任务认领，Agent 运行时也可以是 OpenClaw、Claude Code、Codex、Cursor、bash 或 HTTP。

它的启发是：长期协作需要持久身份、原子认领和可恢复任务。但它也展示了另一端的复杂度：预算、审批、治理、组织架构对企业场景有价值，但不一定应该进入 Hermes 的协作内核。对多数本地用户来说，这些更适合做成 profile 约定或插件。

#### 17.1.2.3 NanoClaw Agent Swarms
NanoClaw Agent Swarms 试图基于 Claude Agent SDK 的进程内子 Agent 团队做协作，但在非交互式 SDK / 容器模式下，子 Agent 会随着团队负责人的回合结束而被静默终止，表面看起来成功，实际没有产出文件。

它给 Hermes Kanban 的教训很直接：不要把协作生命周期绑定在外部 SDK 的进程内子 Agent 语义上。协调层必须在 Hermes 自己控制的层里；工作者应该是操作系统进程，失败、崩溃或主机重启后可以通过任务板和认领机制恢复。

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

Cline 的简单任务板形态是有效的，但偏代码任务；Paperclip 的持久身份和原子认领很有价值，但企业治理过重；NanoClaw 说明进程内群体协作对上游生命周期太敏感。Hermes Kanban 取它们的交集：任务板、依赖链接、工作目录、持久身份、原子认领；同时避免企业治理内核化和 SDK 群体协作脆弱性。

#### 17.1.2.5 Google Gemini Enterprise
Google 把 Agent Designer、子 Agent 定义、调度、连接器、治理控制面等能力放在一个更完整的平台里。Gemini CLI 的子 Agent 可以用 Markdown + YAML 定义并放进代码库，用户可以通过 `@agent-name` 显式调用，也可以让编排者自动路由。

对 Hermes 来说，有两点值得吸收：

- profile / 子 Agent 应该能以文件或模板形式版本化、共享、安装
- `@name` 这种显式跨 Agent 委派语法有很好的交互潜力

### 17.1.3 Hermes Kanban 的设计理念
Hermes Kanban 的设计理念可以概括为几个取舍：

- 采用 Cline 的任务板 + 依赖链接 + 工作目录形态
- 采用 Paperclip 的原子认领和持久身份，但把身份映射到 Hermes profile
- 拒绝 NanoClaw 式进程内子 Agent 群体协作，每个工作者都是完整操作系统进程
- 吸收 Gemini 的可移植 profile 工件和 `@name` 委派思路
- 拒绝把 Paperclip / Gemini 的治理控制面做进内核

最终目标是一个最小但稳固的协作内核：一个 SQLite 任务板、一个 Kanban 命令行入口、一个调度器、一组工作者技能 / 工具，以及 Hermes profile。任何复杂的协作形态、角色分工和策略，都通过 profile、技能、插件扩展，而不是让内核变成“公司管理系统”。

这也是 Kanban 和 `delegate_task` 的根本边界：`delegate_task` 是函数调用；Kanban 是持久工作队列。只要一次交接需要活过单个 API loop，并且需要被其他 profile 或人类看到、评论、恢复或审计，就应该进入任务板。

## 17.2 架构

### 17.2.1 Control Plane：CLI / Gateway / Dashboard

### 17.2.2 State Plane：SQLite board + dispatcher

### 17.2.3 Execution Plane：独立 profile worker

### 17.2.4 Critical invariant：不做进程内 subagent swarm

## 17.3 Data Model：数据模型

### 17.3.1 `tasks`

### 17.3.2 `task_links`

### 17.3.3 `task_comments`

### 17.3.4 `task_events` / `task_runs`

### 17.3.5 Status 状态机

### 17.3.6 Workspace kinds

## 17.4 Collaboration Patterns：协作模式

### 17.4.1 P1 Fan-out

### 17.4.2 P2 Pipeline

### 17.4.3 P3 Voting / Quorum

### 17.4.4 P4 Long-running journal

### 17.4.5 P5 Human-in-the-loop triage

### 17.4.6 P6 @mention delegation

### 17.4.7 P7 Thread-scoped workspace

### 17.4.8 P8 Fleet farming

## 17.5 The Orchestrator Profile：编排者 profile

### 17.5.1 Orchestrator 是 control room，不是 worker

### 17.5.2 三个属性：禁用执行工具、加载 skill、遵守 specialist roster

### 17.5.3 为什么 orchestrator 不是 kernel role

### 17.5.4 当前使用方式：直接聊天或作为 Kanban 总任务 assignee

## 17.6 Multi-Tenant Context：多租户上下文

### 17.6.1 `tenant` 是 namespace，不是新实体

### 17.6.2 workspace、memory、board view、audit 的隔离方式

### 17.6.3 一个 specialist fleet 服务多个业务上下文

### 17.6.4 不做 tenant 级 ACL、跨 tenant 依赖、tenant-scoped profiles

## 17.7 Worked Example：50-account social media fleet

### 17.7.1 Setup：一个 specialist profile + 多个 workspace

### 17.7.2 Per-tick task generation

### 17.7.3 Dispatcher 并行 claim 和 spawn

### 17.7.4 为什么这个模型干净

## 17.8 User Stories：典型故事

### 17.8.1 Research triage and synthesis

### 17.8.2 Scheduled recurring workflow

### 17.8.3 Digital-twin / persistent assistant role

### 17.8.4 Coding pipeline

### 17.8.5 这些故事共同需要什么

## 17.9 Kanban vs `delegate_task`

### 17.9.1 一句话区别

### 17.9.2 维度对比

### 17.9.3 何时用 `delegate_task`

### 17.9.4 何时用 Kanban

### 17.9.5 两者如何共存

## 17.10 Assignment Semantics：任务归属语义

### 17.10.1 一个 task 只有一个 assignee

### 17.10.2 谁可以创建任务

### 17.10.3 planner / router 只是约定，不是结构角色

### 17.10.4 worker 能看到什么上下文

### 17.10.5 v1 不支持什么

## 17.11 Dispatcher Design：调度器设计

### 17.11.1 Dispatcher 故意很笨

### 17.11.2 四个动作：recompute ready、atomic claim、spawn worker、stale recovery

### 17.11.3 SQLite 并发正确性

### 17.11.4 当前实现：Gateway 内置 dispatcher

### 17.11.5 失败、重试和 circuit breaker

## 17.12 CLI / Gateway / Dashboard：当前操作入口

### 17.12.1 CLI command surface

### 17.12.2 `/kanban` Slash command

### 17.12.3 Dashboard Kanban tab

### 17.12.4 自动化：cron、webhook、idempotency key

## 17.13 Worker Tool Surface：当前 `kanban_*` 工具

### 17.13.1 为什么 worker 不用 CLI

### 17.13.2 worker 启动环境变量

### 17.13.3 lifecycle 工具：show / heartbeat / complete / block / comment

### 17.13.4 orchestrator 工具：list / create / link / unblock

### 17.13.5 结构化 handoff：summary + metadata

## 17.14 Scope Boundaries：什么不属于 kernel

### 17.14.1 Smart routing / auto-assignment

### 17.14.2 Org chart / hierarchy

### 17.14.3 Budgets、approval gates、governance control plane

### 17.14.4 Fleet management dashboard

## 17.15 Risks / Tradeoffs / Open Questions

### 17.15.1 SQLite cross-process contention

### 17.15.2 Stale workspace buildup

### 17.15.3 Profile misconfiguration

### 17.15.4 Polling over events

### 17.15.5 Cron 与 Kanban 的边界

## 17.16 Current Implementation Notes：PDF 与当前实现的差异

### 17.16.1 PDF 是设计稿，当前实现已经加入 toolset

### 17.16.2 当前实现已有 multi-board、runs、Dashboard、specifier

### 17.16.3 当前仍需以官方文档和源码为准
