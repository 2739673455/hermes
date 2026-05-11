# Hermes Agent
https://hermes-agent.nousresearch.com/docs

## 1. 快速开始
### 1.1 安装
https://hermes-agent.nousresearch.com/docs/getting-started/installation  
安装前需确保 git 可用

#### 1.1.1 Linux / macOS / WSL2
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

#### 1.1.2 Windows
```bash
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

### 1.2 配置模型提供商
https://hermes-agent.nousresearch.com/docs/integrations/providers
```bash
hermes model
```

### 1.3 命令行使用
https://hermes-agent.nousresearch.com/docs/user-guide/cli

#### 1.3.1 启动
```bash
hermes
```

#### 1.3.2 命令行命令
https://hermes-agent.nousresearch.com/docs/reference/cli-commands

#### 1.3.3 命令行快捷键
https://hermes-agent.nousresearch.com/docs/user-guide/cli#keybindings
| 快捷键     | 功能                                   |
| ---------- | -------------------------------------- |
| `alt + v`  | 从剪贴板粘贴图像                       |
| `ctrl + c` | 中断会话                               |
| `ctrl + d` | 退出会话                               |
| `ctrl + z` | 暂停会话并挂起到后台，可通过 `fg` 恢复 |

#### 1.3.4 命令行斜杠命令
https://hermes-agent.nousresearch.com/docs/reference/slash-commands#interactive-cli-slash-commands
| 命令                               | 功能                       |
| ---------------------------------- | -------------------------- |
| `/new`                             | 开启新会话                 |
| `/clear`                           | 清除屏幕并开启新会话       |
| `/history`                         | 显示对话记录               |
| `/sessions`                        | 浏览和恢复之前的会话       |
| `/background 查看系统资源占用情况` | 在单独的后台会话中运行任务 |

### 1.4 会话管理
https://hermes-agent.nousresearch.com/docs/user-guide/sessions
| 命令                              | 功能                   |
| --------------------------------- | ---------------------- |
| `hermes -c`                       | 继续上次会话           |
| `hermes -r <session_id or title>` | 按会话id或标题恢复会话 |
| `hermes sessions list`            | 列出所有会话           |
| `hermes sessions delete 123`      | 删除会话               |

### 

### 卸载
https://hermes-agent.nousresearch.com/docs/getting-started/updating#uninstalling

