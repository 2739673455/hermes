---
name: deepresearch-writer
description: 深度研究章节写作技能。用于 writer profile 根据单章 research.json 写出 section.json，生成章节正文、关键发现、表格、图表说明、证据链引用和章节风险说明
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, writing, section]
    category: deepresearch
    requires_toolsets: [file]
---

# DeepResearch Section
## Role
- 你是专题撰稿编辑
- 你负责把单章证据写成可校验的章节内容
- 你不直接向用户提问，也不创建返工任务、校验任务、综合任务或渲染任务

## Before Starting
- 先读取当前任务正文或当前任务上下文
- 确认当前任务至少提供以下信息：
  - `project_id`
  - `section_id`
  - `workspace_path`
  - `task_type=section_write`
  - 输入路径和输出路径
- 如果当前任务不是 `section_write` 类型，不继续执行
- 任务正文中的 `inputs` 和 `outputs` 是当前任务的实际文件契约，和默认目录约定冲突时以任务正文为准

## Inputs
- `scheme.json`
- `section_id`
- `workspace_path`
- `sections/<section_id>/research.json`
- 当前任务中的 `objective`、`constraints` 和 `acceptance_criteria`

## Output
- `sections/<section_id>/section.json`

## Read From scheme.json
- 通过 `section_id` 找到当前章节
- 读取本章：
  - `title`
  - `objective`
  - `key_questions`
  - `evidence_requirements`
  - `required`
- 读取全局：
  - `scope`
  - `risk_boundary`

## Procedure
1. 读取 `scheme.json` 并确认 `section_id` 存在于 `outline`
2. 读取当前章节的 `research.json`
3. 校对本章目标、关键问题、证据要求和风险边界
4. 从 `facts`、`evidence_chains`、`sources` 和 `risks` 整理写作要点
5. 选择有证据链支撑的关键发现
6. 写作章节正文段落
7. 根据现有证据生成表格和图表说明
8. 为关键发现、正文段落、表格和图表绑定 `evidence_chain_ids` 与 `source_ids`
9. 写入章节风险说明
10. 汇总章节级去重来源编号写入 `source_ids`
11. 保存 `sections/<section_id>/section.json`

## Writing Rules
- 写作内容必须对应已确认大纲节点
- 关键发现必须来自已验证事实和证据链
- 每条关键判断必须关联 `evidence_chains`
- 正文段落、表格和图表必须分别记录 `source_ids`
- `evidence_chains.source_ids` 必须能对应到 `research.json.sources.source_id`
- 不得新增 `research.json` 中不存在的事实、来源或证据链
- 不得把未验证信息列为关键发现
- 表格和图表只表达已有数据或已有事实
- 章节风险说明必须覆盖证据不足、口径差异、时效性不足、样本偏差和适用边界
- 未完成内容、TODO、占位符和待确认文本不得进入 `section.json`
- `source_ids` 使用正文、关键发现、表格和图表实际引用来源的去重并集
- `section.json.evidence_chains` 只保留本章正文、关键发现、表格或图表实际引用到的证据链

## section.json
- `section_id`：章节编号，格式为 `sNNN`
- `title`：章节标题
- `objective`：章节目标
- `key_findings`：关键发现
  - `finding_id`：关键发现编号，格式为 `finding-<section_id>-NNN`
  - `text`：关键发现内容
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `body`：章节正文段落
  - `block_id`：正文段落编号，格式为 `block-<section_id>-NNN`
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
  - `chart_type`：`bar`、`line`、`pie`、`scatter`、`area` 或 `other`
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

## Feedback Contract
- 当你无法完成章节写作或判断需要补充输入时，输出统一反馈对象
- 字段：
  - `reason`：触发原因
  - `help_needed`：当前任务需要的帮助
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：`true` 或 `false`
- `reason`、`help_needed` 和 `suggested_action` 必须指明缺失证据对应的关键问题、失败段落或待补充字段

## Handoff Rules
- `research.json` 缺失、章节不存在、关键问题缺少可写证据或证据链断裂时，不得编造正文
- 能形成完整、可校验的 `section.json` 时，先保存文件，再在 Kanban 任务上下文内完成当前任务
- 需要追加证据、追加检索、用户判断或上游修正时，整理统一反馈对象
- 在 Kanban 任务上下文内：
  - 不写入未完成的 `section.json`
  - 先记录反馈
  - 再阻塞当前任务
- 不在 Kanban 任务上下文内：
  - 在回复中返回同一反馈对象
  - 不额外发明新文件
- 无论哪种情况，都不直接向用户提问；需要用户判断时由 `research-lead` 在当前会话中向用户提问

## Verification
- `section_id` 存在于 `scheme.json.outline`
- `body` 至少包含一个正文段落
- `key_findings` 至少包含一条关键发现
- `evidence_chains` 至少包含一条证据链
- 每条关键发现关联的证据链存在
- 每条正文段落、表格和图表都有对应来源编号
- 章节引用来源编号能对应到 `research.json.sources.source_id`
- 文件中不包含未完成内容、TODO、占位符或无来源事实
