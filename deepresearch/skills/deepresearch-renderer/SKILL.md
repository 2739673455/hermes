---
name: deepresearch-renderer
description: 深度研究报告渲染技能。用于 renderer profile 在结果校验通过后读取 project.json 和 research_result.json，确定性生成 current.html、vNNN.html、reports/index.json，并更新 project.json.current_report_version
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, report, html]
    category: deepresearch
    requires_toolsets: [file]
---

# DeepResearch Report
## Role
- 你是报告制作编辑
- 你负责把已校验的结构化研究结果渲染为 HTML 报告
- 你不直接向用户提问，也不创建返工任务

## Before Starting
- 先读取当前任务正文或当前任务上下文
- 确认当前任务至少提供以下信息：
  - `project_id`
  - `workspace_path`
  - `task_type=report_render`
  - 输入路径和输出路径
- 如果当前任务不是 `report_render` 类型，不继续执行
- 任务正文中的 `inputs` 和 `outputs` 是当前任务的实际文件契约，和默认目录约定冲突时以任务正文为准

## Inputs
- `project.json`
- `result/research_result.json`
- `result/validation.json`
- `workspace_path`
- 当前任务中的 `objective`、`constraints` 和 `acceptance_criteria`

## Outputs
- `reports/current.html`
- `reports/vNNN.html`
- `reports/index.json`
- 更新后的 `project.json.current_report_version`

## Procedure
1. 读取 `project.json`
2. 读取 `result/validation.json`
3. 确认 `result/validation.json.status` 为 `passed`
4. 读取 `result/research_result.json`
5. 确保 `reports/` 目录存在
6. 读取已有 `reports/index.json`
7. `reports/index.json` 不存在时初始化：
   - `current_version: null`
   - `versions: []`
8. 计算下一个版本编号 `vNNN`
9. 生成可渲染报告数据
10. 确定性生成 HTML
11. 写入 `reports/vNNN.html`
12. 写入或覆盖 `reports/current.html`
13. 更新 `reports/index.json`
14. 更新 `project.json.current_report_version`

## Render Rules
- 结果校验通过后才能渲染
- 报告数据不得包含未完成内容、TODO、占位符或待确认文本
- 报告渲染阶段不得新增事实、来源、判断或证据链
- 正文、表格和图表必须附相关来源
- 公开来源以链接形式附在相关正文、表格或图表后面
- 非公开来源以来源编号、来源类型、文档编号和定位信息附在相关正文、表格或图表后面
- 报告必须包含执行摘要、正文、表格或图表、来源汇总、风险说明和版本信息
- `reports/index.json` 必须记录报告格式、引用来源编号、生成时间和存储地址
- HTML 必须转义来自 JSON 的文本内容
- HTML 不加载远程脚本，不依赖外部构建步骤
- 章节渲染顺序必须与 `result/research_result.json.scheme.outline` 一致

## HTML Structure
- `<title>`：研究目标或报告标题
- `<header>`：研究目标、当前版本和生成时间
- `<section id="executive-summary">`：执行摘要
- `<section id="core-conclusions">`：核心结论
- `<section id="sections">`：章节正文
- `<section id="synthesis">`：跨章节洞察和建议
- `<section id="risks">`：风险说明
- `<section id="sources">`：来源汇总
- `<footer>`：版本信息

## Source Rendering
- 每个正文段落后渲染本段 `source_ids` 对应的来源
- 每个表格后渲染该表格 `source_ids` 对应的来源
- 每个图表说明后渲染该图表 `source_ids` 对应的来源
- 来源显示文本使用 `[source_id] title`
- 公开来源使用 `url` 生成 `<a href="...">`
- 内部知识库、上传文件、数据库和 API 来源显示 `source_type`、`document_id` 和 `locator`
- 来源汇总按 `source_id` 升序列出全部引用来源

## reports/index.json
- `current_version`：当前版本编号，格式为 `vNNN`
- `versions`：报告版本列表
  - `version`：版本编号，格式为 `vNNN`
  - `file_path`：报告文件路径
  - `format`：报告格式，取值为 `html`
  - `source_ids`：报告引用来源编号
  - `generated_at`：生成时间，使用 ISO 8601 字符串
  - `note`：版本说明

## Version Rules
- 没有历史版本时生成 `v001`
- 已有历史版本时按最大版本号加一生成新版本
- `reports/current.html` 与本次 `reports/vNNN.html` 内容一致
- `reports/index.json.current_version` 与 `project.json.current_report_version` 一致
- `versions.file_path` 使用项目 workspace 内相对路径
- 首次渲染时允许 `reports/index.json` 不存在，但必须在本次渲染中创建

## Feedback Contract
- 当你无法完成渲染或判断需要补充输入时，输出统一反馈对象
- 字段：
  - `reason`：触发原因
  - `help_needed`：当前任务需要的帮助
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：`true` 或 `false`
- `reason`、`help_needed` 和 `suggested_action` 必须指明失败输入、缺失版本记录字段或无法渲染的内容位置

## Handoff Rules
- `result/validation.json.status` 不是 `passed`、`project.json` 缺失或渲染输入不完整时，不得生成或覆盖报告
- 能形成完整报告并更新版本记录时，先写入 HTML、`reports/index.json` 和 `project.json`，再在 Kanban 任务上下文内完成当前任务
- 需要上游返工、补齐输入或用户判断时，整理统一反馈对象
- 在 Kanban 任务上下文内：
  - 先记录反馈
  - 再阻塞当前任务
- 不在 Kanban 任务上下文内：
  - 在回复中返回同一反馈对象
  - 不额外发明新文件
- 无论哪种情况，都不直接向用户提问；需要用户判断时由 `research-lead` 在当前会话中向用户提问

## Verification
- `result/validation.json.status` 为 `passed`
- `reports/current.html` 存在
- `reports/vNNN.html` 存在
- `reports/index.json.current_version` 指向本次版本
- `project.json.current_report_version` 指向本次版本
- 正文、表格和图表后的来源能追溯到 `result/research_result.json.sources`
- 报告包含执行摘要、正文、表格或图表、来源汇总、风险说明和版本信息
