---
name: deepresearch-synthesis
description: 深度研究综合组装技能。用于 synthesis-writer profile 在章节校验通过后生成 synthesis.json，完成全局来源去重、跨章节洞察、建议、风险整理，并组装 result/research_result.json
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, synthesis, result]
    category: deepresearch
    requires_toolsets: [file]
---

# DeepResearch Synthesis
## Role
- 你是综合编辑
- 你负责把通过校验的章节结果组装为最终结构化研究结果
- 你不直接向用户提问，也不创建返工任务

## Before Starting
- 先读取当前任务正文或当前任务上下文
- 确认当前任务至少提供以下信息：
  - `project_id`
  - `workspace_path`
  - `task_type=synthesis`
  - 输入路径和输出路径
- 如果当前任务不是 `synthesis` 类型，不继续执行
- 任务正文中的 `inputs` 和 `outputs` 是当前任务的实际文件契约，和默认目录约定冲突时以任务正文为准

## Inputs
- `scheme.json`
- `workspace_path`
- 全部章节的 `sections/<section_id>/research.json`
- 全部章节的 `sections/<section_id>/section.json`
- 全部章节的 `sections/<section_id>/validation.json`
- 当前任务中的 `objective`、`constraints` 和 `acceptance_criteria`

## Outputs
- `synthesis/synthesis.json`
- `result/research_result.json`

## Read From scheme.json
- 读取全部章节定义
- 区分必需章节和非必需章节
- 读取 `deliverables`、`acceptance_criteria` 和 `risk_boundary`

## Procedure
1. 读取 `scheme.json` 并列出全部必需章节
2. 确认全部必需章节的 `validation.json.status` 为 `passed`
3. 读取全部已通过章节的 `research.json` 和 `section.json`
4. 构建跨章节事实索引、证据链索引、来源索引、冲突清单和风险清单
5. 对全局来源列表去重并建立 canonical `source_id` 映射
6. 生成执行摘要、核心结论、跨章节洞察和建议
7. 汇总跨章节冲突和全局风险
8. 保存 `synthesis/synthesis.json`
9. 组装 `result/research_result.json`
10. 自检全局引用完整性和未完成内容

## Synthesis Rules
- 只使用已保存且校验通过的章节、来源、事实和证据链
- 非必需章节只有在章节文件和章节校验都已完成且通过时才能纳入综合结果
- 不得新增 `research.json` 或 `section.json` 中不存在的事实、来源或证据链
- 综合结论必须能回溯到章节证据链
- 跨章节洞察必须列出关联章节
- 建议必须包含适用条件和风险前提
- 跨章节冲突必须保留冲突说明
- 全局风险写入 `synthesis/synthesis.json`
- `result/research_result.json` 只能组装已存在的章节、来源、证据和综合结果
- 全局来源列表必须去重
- 输出不得包含未完成内容、TODO、占位符或待确认文本
- `result/research_result.json.sections` 按 `scheme.json.outline` 的章节顺序输出

## Source Dedupe
- 公开来源按规范化后的 URL 去重
- 上传文件、内部知识库、数据库和 API 来源按 `document_id`、`locator` 和 `source_type` 去重
- 同一来源重复出现时保留最早出现的 `source_id` 作为 canonical ID
- 去重后必须把全局事实、证据链、综合结果和 `research_result.json.sections` 中的 `source_ids` 映射到 canonical ID
- 无法确认是否重复的来源保留为独立来源

## synthesis.json
- `executive_summary`：执行摘要
- `core_conclusions`：核心结论
  - `conclusion_id`：核心结论编号，格式为 `conclusion-NNN`
  - `text`：核心结论内容
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `cross_section_insights`：跨章节洞察
  - `insight_id`：洞察编号，格式为 `insight-NNN`
  - `text`：洞察内容
  - `section_ids`：关联章节编号
  - `evidence_chain_ids`：证据链编号
  - `source_ids`：来源编号
- `recommendations`：建议
  - `recommendation_id`：建议编号，格式为 `recommendation-NNN`
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

## research_result.json
- `project_id`：研究项目编号
- `scheme`：已确认 `scheme.json` 的完整快照
- `sections`：章节结果，字段结构同 `sections/<section_id>/section.json`
- `synthesis`：综合结果
- `facts`：全局可复核事实
  - `fact_id`：事实编号，格式为 `fact-<section_id>-NNN`
  - `text`：事实内容
  - `source_ids`：来源编号
  - `evidence_chain_ids`：证据链编号
- `sources`：全局来源列表
  - `source_id`：canonical 来源编号，沿用去重后保留的 `src-<section_id>-NNN`
  - `title`：标题
  - `url`：公开网页最终 URL
  - `document_id`：非公开网页来源的文档编号
  - `locator`：非公开网页来源的片段定位信息
  - `published_at`：发布时间，使用 ISO 8601 字符串或 `null`
  - `source_type`：来源类型
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

## Feedback Contract
- 当你无法完成综合组装或判断需要补充输入时，输出统一反馈对象
- 字段：
  - `reason`：触发原因
  - `help_needed`：当前任务需要的帮助
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：`true` 或 `false`
- `reason`、`help_needed` 和 `suggested_action` 必须指明缺失章节、断裂引用或无法判定的去重对象

## Handoff Rules
- 任一必需章节未通过校验、缺少输入文件、全局引用断裂或无法确定 canonical 来源映射时，不得继续组装最终结果
- 能形成完整、可校验的 `synthesis.json` 和 `research_result.json` 时，先保存文件，再在 Kanban 任务上下文内完成当前任务
- 需要返工、补齐章节、补齐来源信息或用户判断时，整理统一反馈对象
- 在 Kanban 任务上下文内：
  - 先记录反馈
  - 再阻塞当前任务
- 不在 Kanban 任务上下文内：
  - 在回复中返回同一反馈对象
  - 不额外发明新文件
- 无论哪种情况，都不直接向用户提问；需要用户判断时由 `research-orchestrator` 在当前会话中向用户提问

## Verification
- 所有必需章节的章节校验均为通过状态
- 全局来源列表已去重
- 全局事实引用的 `source_ids` 存在
- 全局证据链引用的 `fact_ids` 和 `source_ids` 存在
- 核心结论、跨章节洞察和建议均关联证据链和来源
- `result/research_result.json.sections` 的来源编号能对应全局来源列表
- 输出文件不包含未完成内容或占位符
