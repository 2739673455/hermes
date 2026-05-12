# Hermes Agent
https://hermes-agent.nousresearch.com/docs

# 目录
1. [Hermes Agent 是什么](#1-hermes-agent-是什么)
2. [安装](#2-安装)
3. [模型提供商配置](#3-模型提供商配置)
4. [命令行使用入门](#4-命令行使用入门)
5. [会话管理](#5-会话管理)
6. [斜杠命令（Slash Commands）](#6-斜杠命令slash-commands)
7. [配置文件详解](#7-配置文件详解)
8. [Toolset（工具箱）](#8-toolset工具箱)
9. [技能系统（Skills）](#9-技能系统skills)
10. [持久记忆（Memory）](#10-持久记忆memory)
11. [子代理与任务委派（Delegation）](#11-子代理与任务委派delegation)
12. [多终端协调与后台任务](#12-多终端协调与后台任务)
13. [消息平台集成（Gateway）](#13-消息平台集成gateway)
14. [定时任务（Cron）](#14-定时任务cron)
15. [MCP 服务器集成](#15-mcp-服务器集成)
16. [Profile（配置文件集）](#16-profile配置文件集)
17. [卸载](#17-卸载)

# 1. Hermes Agent 是什么
Hermes Agent 是由 Nous Research 开发的开源 AI 代理框架。它运行在终端、消息平台（Telegram、Discord、Slack 等）和 IDE 中，能够自主调用工具完成任务。

## Hermes 的独特优势
- **技能自进化** — Hermes 能从经验中学习。解决复杂问题后，会保存可复用的流程为 Skill，下次遇到类似任务直接加载。
- **跨会话持久记忆** — 记住用户身份与偏好、环境细节和经验教训。
- **多平台网关** — 同一个代理在 Telegram、Discord、Slack 等 10+ 平台上运行，且拥有完整的工具访问权限。
- **Profile** — 运行多个互相隔离的 Hermes 实例，各有独立的配置、会话、技能和记忆。
- **可扩展** — 插件系统、MCP 服务器、自定义工具、Webhook 触发、定时任务。

# 2. 安装
https://hermes-agent.nousresearch.com/docs/getting-started/installation

## 前置条件
- **Git** — 安装前请确认 git 可用

## Linux / macOS / WSL2
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

## Windows（PowerShell）
```powershell
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

## 安装后检查
```bash
hermes doctor
```

`hermes doctor` 会检查依赖项和配置是否完整，如发现缺失会给出修复建议。加上 `--fix` 参数可尝试自动修复：

```bash
hermes doctor --fix
```

## 升级
```bash
hermes update
```

# 3. 模型提供商配置
https://hermes-agent.nousresearch.com/docs/integrations/providers

## 快速配置
```bash
# 交互式选择模型和提供商
hermes model

# 或者使用安装向导
hermes setup
```

API Key 存储在 `~/.hermes/.env` 文件中。

在会话中通过 `/model` 命令即可切换模型和提供商。

# 4. 命令行使用入门
https://hermes-agent.nousresearch.com/docs/user-guide/cli

## 启动交互式对话
```bash
# 命令行启动
hermes

# TUI 启动
hermes --tui
```

## 单次对话（非交互式）
```bash
hermes chat -q "查看系统资源占用情况"
```

适合脚本调用或一次性任务。

## 快捷键
| 快捷键         | 功能                                         |
| -------------- | -------------------------------------------- |
| `Alt + V`      | 从剪贴板粘贴图像                             |
| `Ctrl + C`     | 中断当前操作                                 |
| `Ctrl + D`     | 退出会话                                     |
| `Ctrl + Z`     | 暂停并挂起到后台，`fg` 恢复                  |
| `Ctrl + Enter` | 输入多行文本（Windows 需用此代替 Alt+Enter） |

## 会话管理
https://hermes-agent.nousresearch.com/docs/user-guide/sessions

每一次与 Hermes 的对话都是一个会话（Session），系统会自动保存和索引。

### 基本操作
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

### 会话搜索工具
https://hermes-agent.nousresearch.com/docs/user-guide/sessions#session-search-tool

## Toolset
https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference

Hermes 的工具按功能分组为「工具箱」（Toolsets）。可以按需启用或禁用以控制代理的能力范围。

### 查看与管理工具箱
```bash
# 交互式管理
hermes tools

# 查看所有工具箱及状态
hermes tools list

# 会话内管理工具
/tools
```

# 6. 斜杠命令（Slash Commands）
https://hermes-agent.nousresearch.com/docs/reference/slash-commands

在交互式会话中，以 `/` 开头的命令称为斜杠命令。

## 完整命令列表
在会话中输入 `/help` 即可查看所有命令列表。以下是常用命令的分类概览：

### 会话控制
| 命令                    | 功能                                                             |
| ----------------------- | ---------------------------------------------------------------- |
| `/new`                  | 开始新会话                                                       |
| `/clear`                | 清屏并开始新会话                                                 |
| `/undo`                 | 撤销上一次用户/Agent交互记录                                     |
| `/title <session_name>` | 为当前会话命名                                                   |
| `/history`              | 显示对话历史                                                     |
| `/compress`             | 手动压缩上下文                                                   |
| `/stop`                 | 停止后台进程                                                     |
| `/background <prompt>`  | 在后台运行任务                                                   |
| `/goal <text>`          | 设置持续性目标。一个评判模型会检查目标是否完成，未完成则自动继续 |

### 配置
| 命令                            | 功能             |
| ------------------------------- | ---------------- |
| `/config`                       | 查看当前配置     |
| `/model [model-name]`           | 查看或切换模型   |
| `/personality [name]`           | 设置性格         |
| `/reasoning [level/show/hide] ` | 设置推理级别     |
| `/voice [on/off/tts/status]`    | 语音模式         |
| `/yolo`                         | 切换绕过确认模式 |

### 工具与技能
| 命令                               | 功能                       |
| ---------------------------------- | -------------------------- |
| `/tools`                           | 管理工具箱的启用/禁用      |
| `/skills`                          | 搜索和安装技能             |
| `/cron`                            | 管理定时任务               |
| `/curator [status\|run\|pin\|…]`   | 技能自动维护（策展人系统） |
| `/kanban [tasks\|links\|comments]` | 多代理协作看板             |

# 7. 配置
https://hermes-agent.nousresearch.com/docs/user-guide/configuration

## 配置目录结构
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

## 配置管理命令
```bash
hermes config                        # 查看当前配置
hermes config edit                   # 用 $EDITOR 打开 config.yaml 编辑
hermes config set section.key value  # 直接设置某个配置项
```

## 常用配置
### 命令确认模式
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#smart-approvals

```yaml
approvals:
  mode: manual  # manual | smart | off
# manual    — 每次高危操作都询问（默认）
# smart     — 用辅助模型自动判断风险，低风险直接执行
# off       — 跳过所有确认（等同于 --yolo）
```

### 上下文压缩
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#context-compression

```yaml
compression:
  enabled: true       # 启用/禁用压缩
  threshold: 0.50     # 压缩触发阈值
  target_ratio: 0.20  # 保留为未压缩尾部的阈值比例
  protect_last_n: 20  # 最少保留不压缩的最近消息数
```

### 记忆配置
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#memory-configuration

```yaml
memory:
  memory_enabled: true        # 启用持久记忆
  user_profile_enabled: true  # 启用用户档案
  memory_char_limit: 2200     # 记忆字符上限（约800 tokens）
  user_char_limit: 1375       # 用户档案字符上限（约500 tokens）
```

### 子Agent行为
https://hermes-agent.nousresearch.com/docs/user-guide/configuration#delegation

```yaml
delegation:
  max_concurrent_children: 3  # 每个批次并行运行的最大子Agent数量
  max_spawn_depth: 1          # 最大子Agent嵌套深度
  orchestrator_enabled: true  # 可否生成 Orchestrator 子Agent，为 false 时只能生成叶子Agent
```



# 9. 技能系统（Skills）
## 基本操作
```bash
# 列出已安装的技能
hermes skills list

# 浏览可用的技能（从官方仓库）
hermes skills browse

# 搜索技能
hermes skills search "code review"

# 安装技能（通过 ID 或 URL）
hermes skills install github-code-review
hermes skills install https://example.com/my-skill/SKILL.md

# 预览技能内容（不安装）
hermes skills inspect github-code-review

# 检查技能更新
hermes skills check

# 更新所有过时技能
hermes skills update

# 卸载技能
hermes skills uninstall 0

# 发布自定义技能到仓库
hermes skills publish ./my-skill/

# 添加 GitHub repo 作为技能源
hermes skills tap add NousResearch/hermes-skills
```

## 在会话中加载技能
```bash
# 启动时加载
hermes -s "github-code-review,test-driven-development"

# 会话内加载
/skill python-debugpy
```

## 技能自维护
Hermes 有一个「策展人」（Curator）系统，它会自动跟踪技能的使用频率，将长期未使用的技能标记为「过时」并归档：

```bash
# 查看技能状态
hermes curator status

# 手动运行策展
hermes curator run

# 固定某个技能（防止被自动处理）
hermes curator pin my-important-skill

# 恢复已归档的技能
hermes curator restore my-skill
```

# 10. 持久记忆（Memory）
Hermes 能跨会话记住你的个人信息、偏好和重要事实。

## 查看与管理记忆
```bash
hermes memory status    # 查看记忆状态
hermes memory setup     # 配置记忆提供商
```

## 记忆存储的内容
- **用户信息**：你的名字、角色、工作习惯（例如「用户是后端开发者，偏好 Python」）
- **环境事实**：项目结构、常用工具、操作系统细节
- **偏好**：「回复要简洁」「用中文回复」「优先使用 pytest」

## 记忆与传统 Chat 的对比
|          | Hermes 记忆      | ChatGPT / Claude 聊天历史 |
| -------- | ---------------- | ------------------------- |
| **粒度** | 结构化事实       | 完整对话                  |
| **检索** | 自动注入系统提示 | 需手动翻阅                |
| **更新** | 自动修改         | 无更新机制                |
| **控制** | `/reset` 后保留  | 新会话不保留              |

## 不存储在记忆中的内容
- 动态任务进度（如「PR #42 已提交」— 这些信息过几天就过期了）
- 完整的对话内容
- 临时 TODO 状态

# 11. 子代理与任务委派（Delegation）
Hermes 可以创建子代理来处理独立的任务。子代理有自己的对话和终端环境，互不干扰。

## 什么时候用委派？
- **并行独立任务** — 同时处理多个互不依赖的任务
- **需要隔离环境** — 子代理运行在独立工作目录
- **减少上下文干扰** — 子代理的详细输出不会污染主会话的上下文

## 使用方式
通过 `delegate_task` 工具创建子代理。支持两种模式：

**单任务模式：**

提供一个目标和上下文，子代理执行后返回摘要。

**批量并行模式（最多 3 个子代理并行）：**

同时派发多个任务，所有子代理并行执行，结果一并返回。

## 委派 vs 独立进程
|          | delegate_task          | 独立 hermes 进程 |
| -------- | ---------------------- | ---------------- |
| 隔离性   | 独立对话，共享进程     | 完全独立进程     |
| 持续时间 | 分钟级（受限于父循环） | 小时/天级        |
| 工具访问 | 父进程的子集           | 完整工具权限     |
| 交互性   | 无                     | 有（PTY 模式）   |
| 适用场景 | 快速并行子任务         | 长期自主任务     |

# 12. 多终端协调与后台任务
## 后台任务
长时间运行的任务可以通过 `terminal(background=True)` 在后台运行，并在完成后收到通知：

```bash
# 启动后台任务（Hermes Agent 自动完成，无需手动 shell）
terminal(command="pytest tests/ -v", background=true, notify_on_complete=true)
```

支持两种模式：
- **notify_on_complete** — 任务完成后自动通知你
- **watch_patterns** — 在输出中匹配特定字符串时通知（如 "Application startup complete"）

## 多代理协调（tmux 模式）
对于需要多个 Hermes 实例长时间并行工作的场景，可以用 tmux 启动多个独立实例：

```bash
# 启动代理 A：后端开发
tmux new-session -d -s backend -x 120 -y 40 'hermes -w'
sleep 8 && tmux send-keys -t backend '构建用户管理 REST API' Enter

# 启动代理 B：前端开发
tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'
sleep 8 && tmux send-keys -t frontend '构建 React 仪表盘' Enter

# 查看代理 A 的进度
tmux capture-pane -t backend -p | tail -30

# 将代理 A 的结果传达给代理 B
tmux send-keys -t frontend '后端 API 结构是：...' Enter
```

`-w` 参数（worktree 模式）为每个代理创建独立的 git worktree，避免并发编辑时的 git 冲突。

# 13. 消息平台集成（Gateway）
Hermes 可以通过 Gateway 运行在消息平台上，让你在 Telegram、Discord、Slack 等日常聊天工具中使用它。

## 配置 Gateway
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

## 支持的平台
Telegram、Discord、Slack、WhatsApp、Signal、Email、SMS、Matrix、Mattermost、Home Assistant、DingTalk（钉钉）、Feishu（飞书）、WeCom（企业微信）、BlueBubbles（iMessage）、Weixin（微信）、API Server、Webhooks

## Gateway 专用命令
在消息平台中，除了常规的对话外，还有以下专用功能：

- `/approve` / `/deny` — 批准/拒绝高危命令
- `/sethome` — 将当前聊天设为本机频道
- `/platforms` — 查看所有平台的连接状态
- `/topic` — 在 Telegram 中创建话题子会话
- `/restart` — 重启 Gateway

## Gateway 日志
```bash
# 查看最近错误
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

## Gateway 常见问题
- **SSH 登出后 Gateway 死亡**：启用 linger：`sudo loginctl enable-linger $USER`
- **WSL2 关闭后死亡**：确保 `/etc/wsl.conf` 中有 `systemd=true`；否则使用 `nohup`
- **Discord Bot 不响应**：必须在 Discord 开发者后台启用 Message Content Intent
- **Slack Bot 只响应私信**：必须订阅 `message.channels` 事件

# 14. 定时任务（Cron）
Hermes 内置了定时任务系统，让代理在指定时间自动执行任务。

## 创建任务
```bash
# 每 30 分钟执行一次
hermes cron create "30m" --prompt "检查我的服务器状态并报告"

# 每天早 9 点
hermes cron create "0 9 * * *" --prompt "生成每日报告"

# 指定时间（ISO 格式）
hermes cron create "2025-03-01T09:00:00" --prompt "..."
```

## 管理任务
```bash
hermes cron list          # 列出任务（--all 包含已禁用的）
hermes cron pause ID      # 暂停任务
hermes cron resume ID     # 恢复任务
hermes cron edit ID       # 编辑任务的调度、提示、投递方式
hermes cron run ID        # 立即触发
hermes cron remove ID     # 删除任务
hermes cron status        # 调度器状态
```

## 投递方式
任务的执行结果可以投递到指定平台：

```bash
# 默认投递到当前会话
# 投递到 Telegram
hermes cron create "30m" --prompt "..." --deliver "telegram:-1001234567890"
# 投递到所有已连接的平台
hermes cron create "30m" --prompt "..." --deliver "all"
```

## 高级用法
- **指定技能加载**：`hermes cron create "30m" -s "web,github-issues" --prompt "..."`
- **指定模型**：`hermes cron create "30m" --model "anthropic/claude-sonnet-4" --prompt "..."`
- **自定义脚本**：`hermes cron create "30m" --script "~/monitor.sh"`

# 15. MCP 服务器集成
Hermes 支持 MCP（Model Context Protocol）服务器，可以连接外部工具和数据源。

## 基本操作
```bash
# 添加 MCP 服务器
hermes mcp add my-server --url "http://localhost:8000/sse"
hermes mcp add my-server --command "python mcp_server.py"

# 列出已配置的服务器
hermes mcp list

# 测试连接
hermes mcp test my-server

# 管理服务器中的工具启用状态
hermes mcp configure my-server

# 移除服务器
hermes mcp remove my-server

# 将会话中已加载的 MCP 工具重新加载
/reload-mcp
```

## 启动 Hermes 作为 MCP 服务器
```bash
hermes mcp serve
```

# 16. Profile（配置文件集）
Profile 让你运行多个完全独立的 Hermes 实例，各有独立的配置、会话、技能和记忆。

## 为什么用 Profile？
- **工作/个人分离** — 不同的 API key、模型、技能集
- **项目隔离** — 每个项目有自己的配置和环境
- **团队协作** — 不同的角色使用不同的工具集

## 管理 Profile
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

## 使用 Profile
```bash
# 启动时指定 Profile
hermes -p work

# 启动并使用 worktree 模式
hermes -p work -w
```

Profile 的数据存储在 `~/.hermes/profiles/<name>/` 目录下，结构和主目录一致。

# 17. 卸载
```bash
hermes uninstall
```

## 手动清理
如果需要完全清理所有数据：

```bash
rm -rf ~/.hermes
```
