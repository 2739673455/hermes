# Hermes Agent
- https://hermes-agent.nousresearch.com/docs

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [快速上手](#2-快速上手)
3. [配置文件与配置管理](#3-配置文件与配置管理)
4. [会话管理](#4-会话管理)
5. [Dashboard](#5-dashboard)
6. [Toolsets](#6-toolsets)
7. [MCP 服务器集成](#7-mcp-服务器集成)
8. [Skill](#8-skill)
9. [持久记忆（Memory）](#9-持久记忆memory)
10. [子Agent与任务委派（Delegation）](#10-子Agent与任务委派delegation)
11. [多终端协调与后台任务](#11-多终端协调与后台任务)
12. [消息平台集成（Gateway）](#12-消息平台集成gateway)
13. [定时任务（Cron）](#13-定时任务cron)
14. [Profile（配置文件集）](#14-profile配置文件集)
15. [附录：会话架构设计](#附录会话架构设计)

# 1. Hermes Agent 是什么
Hermes Agent 是由 Nous Research 开发的开源 AI Agent 框架。它运行在终端、消息平台（Telegram、Discord、Slack 等）和 IDE 中，能够自主调用工具完成任务。

Hermes 的独特优势：
- **技能自进化** — Hermes 能从经验中学习。解决复杂问题后，会保存可复用的流程为 Skill，下次遇到类似任务直接加载。
- **跨会话持久记忆** — 记住用户身份与偏好、环境细节和经验教训。
- **多平台网关** — 同一个Agent在 Telegram、Discord、Slack 等 10+ 平台上运行，且拥有完整的工具访问权限。
- **Profile** — 运行多个互相隔离的 Hermes 实例，各有独立的配置、会话、技能和记忆。
- **可扩展** — 插件系统、MCP 服务器、自定义工具、Webhook 触发、定时任务。

# 2. 快速上手
## 2.1 安装
- https://hermes-agent.nousresearch.com/docs/getting-started/installation
- 安装前请确认 git 可用

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

## 2.3 安装后检查
```bash
hermes doctor
```

`hermes doctor` 会检查依赖项和配置是否完整，如发现缺失会给出修复建议。加上 `--fix` 参数可尝试自动修复：

```bash
hermes doctor --fix
```

## 2.4 交互式对话
```bash
# 启动交互式对话
hermes

# 启动交互式对话，使用 TUI
hermes --tui
```

## 2.5 单次对话（非交互式）
```bash
hermes chat -q "查看系统资源占用情况"
```

适合脚本调用或一次性任务。

## 2.6 常用快捷键
| 快捷键         | 功能                                         |
| -------------- | -------------------------------------------- |
| `Alt + V`      | 从剪贴板粘贴图像                             |
| `Ctrl + C`     | 中断当前操作                                 |
| `Ctrl + D`     | 退出会话                                     |
| `Ctrl + Z`     | 暂停并挂起到后台，`fg` 恢复                  |
| `Ctrl + Enter` | 输入多行文本（Windows 需用此代替 Alt+Enter） |

## 2.7 更新
- https://hermes-agent.nousresearch.com/docs/getting-started/updating

```bash
hermes update
```

## 2.8 卸载
- https://hermes-agent.nousresearch.com/docs/getting-started/updating#uninstalling

```bash
hermes uninstall
```

### 2.8.1 手动清理
如果需要完全清理所有数据：

```bash
rm -rf ~/.hermes
```

# 3. 配置文件与配置管理
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration

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
hermes config                        # 查看当前配置
hermes config edit                   # 用 $EDITOR 打开 config.yaml 编辑
hermes config set section.key value  # 直接设置某个配置项
```

会话内也可以通过斜杠命令调整配置：
- https://hermes-agent.nousresearch.com/docs/reference/slash-commands#configuration

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
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration#smart-approvals

```yaml
approvals:
  mode: manual  # manual | smart | off
# manual    — 每次高危操作都询问（默认）
# smart     — 用辅助模型自动判断风险，低风险直接执行
# off       — 跳过所有确认（等同于 --yolo）
```

### 3.3.2 上下文压缩
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration#context-compression

```yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 压缩触发阈值
  target_ratio: 0.20  # 触发压缩的消息中多少比例的消息保留不压缩
  protect_last_n: 20  # 最少保留不压缩的最近消息数
```

### 3.3.3 记忆配置
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration#memory-configuration

```yaml
memory:
  memory_enabled: true        # 启用持久记忆
  user_profile_enabled: true  # 启用用户档案
  memory_char_limit: 2200     # 记忆字符上限（约 800 tokens）
  user_char_limit: 1375       # 用户档案字符上限（约 500 tokens）
```

### 3.3.4 子Agent行为
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration#delegation

```yaml
delegation:
  max_concurrent_children: 3  # 每个批次并行运行的最大子Agent数量
  max_spawn_depth: 1          # 最大子Agent嵌套深度
  orchestrator_enabled: true  # 可否生成 Orchestrator 子Agent，为 false 时只能生成叶子Agent
```

# 4. 会话管理
- https://hermes-agent.nousresearch.com/docs/user-guide/sessions

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
- https://hermes-agent.nousresearch.com/docs/reference/slash-commands

会话控制：

| 命令                    | 功能                                                             |
| ----------------------- | ---------------------------------------------------------------- |
| `/new`                  | 开始新会话                                                       |
| `/clear`                | 清屏并开始新会话                                                 |
| `/undo`                 | 撤销上一次用户/Agent交互记录                                     |
| `/title <session_name>` | 为当前会话命名                                                   |
| `/history`              | 显示对话历史                                                     |
| `/sessions`             | 查看和管理会话                                                   |
| `/compress`             | 手动压缩上下文                                                   |
| `/stop`                 | 停止后台进程                                                     |
| `/background <prompt>`  | 在后台运行任务                                                   |
| `/goal <text>`          | 设置持续性目标。一个评判模型会检查目标是否完成，未完成则自动继续 |

# 5. Dashboard
- https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard

Hermes 提供了一个基于浏览器的 Web 管理界面，替代手动编辑 YAML 和 CLI 命令，用于配置管理、API 密钥设置和会话监控。

## 5.1 启动与配置
```bash
hermes dashboard              # 启动，自动打开浏览器 http://127.0.0.1:9119
hermes dashboard --port 8080  # 自定义端口
hermes dashboard --tui        # 开启 Chat 标签页
```

# 6. Toolsets
- https://hermes-agent.nousresearch.com/docs/user-guide/features/tools

工具（Tools）是 Hermes 调用外部能力的基本单元——搜索网页、执行命令、读写文件、控制浏览器等。工具按功能分组为「工具集」（Toolsets），可以按平台按需启用或禁用，从而精确控制Agent的能力范围。

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

| 类别             | 包含工具                                                 | 用途                                     |
| ---------------- | -------------------------------------------------------- | ---------------------------------------- |
| **Web**          | `web_search`, `web_extract`                              | 搜索网页、提取页面内容                   |
| **终端与文件**   | `terminal`, `process`, `read_file`, `patch`              | 执行命令、读写文件                       |
| **浏览器**       | `browser_navigate`, `browser_snapshot`, `browser_vision` | 交互式浏览器自动化，支持文本与视觉       |
| **媒体**         | `vision_analyze`, `image_generate`, `text_to_speech`     | 多模态分析与内容生成                     |
| **编排**         | `todo`, `clarify`, `execute_code`, `delegate_task`       | 任务规划、澄清需求、代码执行、委托子Agent |
| **记忆与召回**   | `memory`, `session_search`                               | 持久化记忆、搜索历史会话                 |
| **自动化与推送** | `cronjob`, `send_message`                                | 定时任务、消息推送                       |
| **集成**         | `ha_*`, MCP 工具, `rl_*`                                 | Home Assistant、MCP 服务器、RL 训练等    |

## 6.3 终端后端
终端工具支持 7 种后端，适应不同的安全隔离和运行环境需求：

| 后端             | 说明                   | 适用场景                                 |
| ---------------- | ---------------------- | ---------------------------------------- |
| `local`          | 在本机直接执行（默认） | 本地开发、可信任务                       |
| `docker`         | 隔离容器中执行         | 安全隔离、可复现环境                     |
| `ssh`            | 远程服务器执行         | 沙箱化，防止Agent修改自身代码             |
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
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference

MCP（Model Context Protocol）可以把外部工具服务器接入 Hermes。

## 7.1 添加 MCP 服务器
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

## 7.3 工具暴露与安全
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

# 8. Skill
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- 已安装的技能会以斜杠命令的形式提供

## 8.1 基本操作
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands#hermes-skills

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

## 8.5 Curator
- https://hermes-agent.nousresearch.com/docs/user-guide/features/curator

Curator 是 Hermes 的技能维护系统，专门管理由 Agent 创建或用户手写的技能。它会跟踪技能的查看、使用和修改频率，把长期不用的技能从 `active` 推进到 `stale`，再归档到 `~/.hermes/skills/.archive/`。

Curator 的存在是为了防止通过自我提升循环产生的技能无限累积。每次 Agent 解决一个新问题并保存一项技能时，该技能都会被添加到 `~/.hermes/skills/` 目录中。如果不进行维护，最终会导致数十个功能相近但范围狭窄的重复技能，这些技能不仅会污染目录，还会浪费 token。

### 8.5.1 运行机制
Curator 不是 cron 守护进程，而是在 Hermes 启动或 Gateway 后台 tick 时检查是否满足运行条件：

- 距离上次运行已经超过 `interval_hours`，默认 168 小时（7天）
- Agent 已经空闲超过 `min_idle_hours`，默认 2 小时

运行分两阶段：

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
每次真实 Curator 运行前，Hermes 会把 `~/.hermes/skills/` 打包备份到：

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
Curator 只处理「非内置、非 Hub 安装」的技能。也就是说，不在这些记录里的技能都可能被维护：

- `~/.hermes/skills/.bundled_manifest`
- `~/.hermes/skills/.hub/lock.json`

这包括：

- Agent 通过 `skill_manage(action="create")` 创建的技能
- 用户手写的 `SKILL.md`
- 外部技能目录中暴露给 Hermes 的技能

如果某个手写技能很重要，建议先执行：

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

`REPORT.md` 适合快速审计某次运行做了什么：哪些技能发生状态迁移、LLM reviewer 给了什么意见、哪些技能被 patch。这样不用去 `agent.log` 里手动 grep。

# 9. 持久记忆（Memory）
Hermes 能跨会话记住你的个人信息、偏好和重要事实。

## 9.1 查看与管理记忆
```bash
hermes memory status    # 查看记忆状态
hermes memory setup     # 配置记忆提供商
```

## 9.2 记忆存储的内容
- **用户信息**：你的名字、角色、工作习惯（例如「用户是后端开发者，偏好 Python」）
- **环境事实**：项目结构、常用工具、操作系统细节
- **偏好**：「回复要简洁」「用中文回复」「优先使用 pytest」

## 9.3 记忆与传统 Chat 的对比
|          | Hermes 记忆      | ChatGPT / Claude 聊天历史 |
| -------- | ---------------- | ------------------------- |
| **粒度** | 结构化事实       | 完整对话                  |
| **检索** | 自动注入系统提示 | 需手动翻阅                |
| **更新** | 自动修改         | 无更新机制                |
| **控制** | `/reset` 后保留  | 新会话不保留              |

## 9.4 不存储在记忆中的内容
- 动态任务进度（如「PR #42 已提交」— 这些信息过几天就过期了）
- 完整的对话内容
- 临时 TODO 状态

# 10. 子Agent与任务委派（Delegation）
Hermes 可以创建子Agent来处理独立的任务。子Agent有自己的对话和终端环境，互不干扰。

## 10.1 什么时候用委派？
- **并行独立任务** — 同时处理多个互不依赖的任务
- **需要隔离环境** — 子Agent运行在独立工作目录
- **减少上下文干扰** — 子Agent的详细输出不会污染主会话的上下文

## 10.2 使用方式
通过 `delegate_task` 工具创建子Agent。支持两种模式：

**单任务模式：**

提供一个目标和上下文，子Agent执行后返回摘要。

**批量并行模式（最多 3 个子Agent并行）：**

同时派发多个任务，所有子Agent并行执行，结果一并返回。

## 10.3 委派 vs 独立进程
|          | delegate_task          | 独立 hermes 进程 |
| -------- | ---------------------- | ---------------- |
| 隔离性   | 独立对话，共享进程     | 完全独立进程     |
| 持续时间 | 分钟级（受限于父循环） | 小时/天级        |
| 工具访问 | 父进程的子集           | 完整工具权限     |
| 交互性   | 无                     | 有（PTY 模式）   |
| 适用场景 | 快速并行子任务         | 长期自主任务     |

# 11. 多终端协调与后台任务
## 11.1 后台任务
长时间运行的任务可以通过 `terminal(background=True)` 在后台运行，并在完成后收到通知：

```bash
# 启动后台任务（Hermes Agent 自动完成，无需手动 shell）
terminal(command="pytest tests/ -v", background=true, notify_on_complete=true)
```

支持两种模式：
- **notify_on_complete** — 任务完成后自动通知你
- **watch_patterns** — 在输出中匹配特定字符串时通知（如 "Application startup complete"）

## 11.2 多Agent协调（tmux 模式）
对于需要多个 Hermes 实例长时间并行工作的场景，可以用 tmux 启动多个独立实例：

```bash
# 启动Agent A：后端开发
tmux new-session -d -s backend -x 120 -y 40 'hermes -w'
sleep 8 && tmux send-keys -t backend '构建用户管理 REST API' Enter

# 启动Agent B：前端开发
tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'
sleep 8 && tmux send-keys -t frontend '构建 React 仪表盘' Enter

# 查看Agent A 的进度
tmux capture-pane -t backend -p | tail -30

# 将Agent A 的结果传达给Agent B
tmux send-keys -t frontend '后端 API 结构是：...' Enter
```

`-w` 参数（worktree 模式）为每个Agent创建独立的 git worktree，避免并发编辑时的 git 冲突。

# 12. 消息平台集成（Gateway）
Hermes 可以通过 Gateway 运行在消息平台上，让你在 Telegram、Discord、Slack 等日常聊天工具中使用它。

## 12.1 配置 Gateway
```bash
# 交互式配置消息平台
hermes gateway setup

# 启动 Gateway（前台）
hermes gateway run

# 安装为系统服务（后台自动启动）
hermes gateway install

# 控制服务
hermes gateway start
hermes gateway stop
hermes gateway restart
hermes gateway status
```

## 12.2 支持的平台
Telegram、Discord、Slack、WhatsApp、Signal、Email、SMS、Matrix、Mattermost、Home Assistant、DingTalk（钉钉）、Feishu（飞书）、WeCom（企业微信）、BlueBubbles（iMessage）、Weixin（微信）、API Server、Webhooks

## 12.3 Gateway 专用命令
在消息平台中，除了常规的对话外，还有以下专用功能：

- `/approve` / `/deny` — 批准/拒绝高危命令
- `/sethome` — 将当前聊天设为本机频道
- `/platforms` — 查看所有平台的连接状态
- `/topic` — 在 Telegram 中创建话题子会话
- `/restart` — 重启 Gateway

## 12.4 Gateway 日志
```bash
# 查看最近错误
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

## 12.5 Gateway 常见问题
- **SSH 登出后 Gateway 死亡**：启用 linger：`sudo loginctl enable-linger $USER`
- **WSL2 关闭后死亡**：确保 `/etc/wsl.conf` 中有 `systemd=true`；否则使用 `nohup`
- **Discord Bot 不响应**：必须在 Discord 开发者后台启用 Message Content Intent
- **Slack Bot 只响应私信**：必须订阅 `message.channels` 事件

# 13. 定时任务（Cron）
Hermes 内置了定时任务系统，让Agent在指定时间自动执行任务。

## 13.1 创建任务
```bash
# 每 30 分钟执行一次
hermes cron create "30m" --prompt "检查我的服务器状态并报告"

# 每天早 9 点
hermes cron create "0 9 * * *" --prompt "生成每日报告"

# 指定时间（ISO 格式）
hermes cron create "2025-03-01T09:00:00" --prompt "..."
```

## 13.2 管理任务
```bash
hermes cron list          # 列出任务（--all 包含已禁用的）
hermes cron pause ID      # 暂停任务
hermes cron resume ID     # 恢复任务
hermes cron edit ID       # 编辑任务的调度、提示、投递方式
hermes cron run ID        # 立即触发
hermes cron remove ID     # 删除任务
hermes cron status        # 调度器状态
```

## 13.3 投递方式
任务的执行结果可以投递到指定平台：

```bash
# 默认投递到当前会话
# 投递到 Telegram
hermes cron create "30m" --prompt "..." --deliver "telegram:-1001234567890"
# 投递到所有已连接的平台
hermes cron create "30m" --prompt "..." --deliver "all"
```

## 13.4 高级用法
- **指定技能加载**：`hermes cron create "30m" -s "web,github-issues" --prompt "..."`
- **指定模型**：`hermes cron create "30m" --model "anthropic/claude-sonnet-4" --prompt "..."`
- **自定义脚本**：`hermes cron create "30m" --script "~/monitor.sh"`

# 14. Profile（配置文件集）
Profile 让你运行多个完全独立的 Hermes 实例，各有独立的配置、会话、技能和记忆。

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

# 附录：会话架构设计
https://hermes-agent.nousresearch.com/docs/user-guide/sessions#session-search-tool

## 存储架构
Hermes 采用双层存储架构：

**SQLite 数据库（`~/.hermes/state.db`）**——结构化存储主体：

| 表             | 内容                                                                          |
| -------------- | ----------------------------------------------------------------------------- |
| `sessions`     | 会话元数据：ID、来源平台、标题、模型、token 统计、时间戳、父会话 ID（压缩链） |
| `messages`     | 完整消息历史：角色、内容、工具调用、工具名称、token 数                        |
| `messages_fts` | FTS5 全文索引虚拟表，覆盖 `content`、`tool_name`、`tool_calls`                |
| `state_meta`   | 键值元数据（如上次清理时间）                                                  |

数据库使用 WAL 模式，支持「一写多读」并发，适合多平台 Gateway 场景。

**JSONL 转录文件（`~/.hermes/sessions/`）**——原始对话副本：

- 每个会话一个 `.jsonl` 文件，每行一条 JSON 记录
- `sessions.json` 索引文件，映射 `session_key` → 会话 ID
- 写操作双写（SQLite + JSONL），读操作优先选内容更丰富的一方

会话 ID 格式：`YYYYMMDD_HHMMSS_<8位随机>`（如 `20260512_085232_54041b`）。

## 索引构建
**FTS5 全文索引**是搜索的核心。Hermes 创建两个 FTS5 虚拟表：

1. **`messages_fts`**（unicode61 分词器）——处理英文/拉丁语系文本
2. **`messages_fts_trigram`**（trigram 分词器）——处理 CJK（中日韩）文本的子串搜索

两个表均索引 `content || tool_name || tool_calls` 的拼接内容，通过 INSERT/DELETE/UPDATE 触发器与 `messages` 表保持实时同步。

数据库典型大小为「数百个会话 10-15 MB」。

## 检索机制
**搜索流程（`session_search` 工具）：**

1. **查询路由**：检测是否包含 CJK 字符（≥3 个则走 trigram 表，否则走标准 FTS5）
2. **FTS5 搜索**：执行全文匹配，返回带 `snippet()` 高亮的片段及前后各 1 条消息作为上下文
3. **按会话分组**：取匹配度最高的前 N 个唯一会话（默认 3）
4. **智能截断**：将会话截断至约 10 万字符，以匹配位置为中心
5. **摘要生成**：由快速辅助模型生成聚焦摘要
6. **返回结果**：每个匹配会话附带摘要、元数据和上下文片段

**支持的查询语法：**

| 语法       | 示例                                      |
| ---------- | ----------------------------------------- |
| 简单关键词 | `docker deployment`                       |
| 精确短语   | `"exact phrase"`                          |
| 布尔运算   | `docker OR kubernetes`、`python NOT java` |
| 前缀匹配   | `deploy*`                                 |

**自动触发**：Agent 被提示在「用户提及过往对话内容或怀疑存在相关历史上下文」时自动调用 `session_search`，无需用户手动搜索。

**会话键机制（Gateway 多平台）：**

在消息平台上，会话通过确定性键管理：

```
agent:main:<平台>:<聊天类型>:<标识符>
```

- Telegram/Discord 私信：按 chat ID 键控
- 群聊：默认按 `group:<chat_id>:<user_id>` 键控（每人独立会话，互不污染上下文窗口）
- 群聊话题/线程：默认按 `group:<chat_id>:<thread_id>` 键控（参与者共享）

## 清理与维护
- 默认不自动清理
- 开启 `auto_prune` 后，已结束且超过 `retention_days`（默认 90 天）的会话在启动时清理
- `VACUUM` 在清理后自动执行，回收磁盘空间（SQLite 不会在 DELETE 后自动缩小文件）
- 手动清理：`hermes sessions prune --older-than <天数>`
