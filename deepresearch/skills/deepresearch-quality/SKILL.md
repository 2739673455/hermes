---
name: deepresearch-quality
description: 深度研究质量校验技能。用于 quality-reviewer profile 执行章节校验、研究结果校验、证据引用检查、未完成内容检查，生成 validation.json 和可执行返工反馈
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, validation, review]
    category: deepresearch
    requires_toolsets: [file]
---
# DeepResearch Quality
## Role
- 作为事实核查编辑，校验章节结果和最终研究结果
- 只产出 `sections/<section_id>/validation.json` 或 `result/validation.json`，并在失败时提交返工反馈

## Section Review Inputs
- `scheme.json`
- `section_id`
- `workspace_path`
- `sections/<section_id>/research.json`
- `sections/<section_id>/section.json`

## Section Review Output
- `sections/<section_id>/validation.json`

## Section Review Procedure
1. 读取 `scheme.json` 并确认 `section_id` 属于已确认大纲
2. 读取当前章节的 `research.json` 和 `section.json`
3. 检查章节正文、关键发现和证据链完整性
4. 检查 `source_id` 引用是否存在
5. 检查公开来源 URL 是否为 HTTP URL
6. 检查内部知识库、上传文件、数据库和 API 来源是否包含类型、文档编号和定位信息
7. 检查章节正文、表格和图表是否包含未完成内容或占位符
8. 写入校验项、问题列表、缺失内容和返工反馈
9. 保存 `sections/<section_id>/validation.json`
10. 校验失败时通过 Kanban 评论记录返工反馈

## Section Review Rules
- 章节正文不能为空
- 每章至少包含一条关键发现和一条证据链
- 证据链引用的 `fact_id` 必须存在于 `research.json.facts`
- 证据链引用的 `source_id` 必须存在于 `research.json.sources`
- 公开来源必须提供 HTTP URL
- 内部知识库来源必须标记来源类型
- 校验失败时 `issues` 至少包含一个问题
- 返工反馈必须能指向具体失败点

## Result Review Inputs
- `scheme.json`
- `workspace_path`
- 全部章节校验结果
- `synthesis/synthesis.json`
- `result/research_result.json`
- 全局来源列表
- 全局证据链

## Result Review Output
- `result/validation.json`

## Result Review Procedure
1. 读取 `scheme.json` 并列出全部必需章节
2. 读取全部 `sections/<section_id>/validation.json`
3. 读取 `synthesis/synthesis.json`
4. 读取 `result/research_result.json`
5. 检查所有必需章节是否已保存正文并通过章节校验
6. 检查全局来源列表是否去重
7. 检查全局事实、证据链、核心结论、洞察、建议和风险是否能回溯到章节证据链
8. 检查报告渲染输入是否包含未完成内容或占位符
9. 写入校验项、问题列表、受影响章节和返工反馈
10. 保存 `result/validation.json`
11. 校验失败时通过 Kanban 评论记录返工反馈

## Result Review Rules
- 所有需要正文的章节都已保存
- 所有必需章节校验已通过
- 全局来源列表不得包含重复来源
- 报告渲染输入不得包含未完成内容或占位符
- `result/validation.json.status` 只有在全部必需检查通过时才能为 `passed`
- 校验失败时 `issues` 至少包含一个问题
- 返工反馈必须能指向具体失败点

## Output Schema
- `status`：校验状态，取值为 `passed`、`failed` 或 `blocked`
- `checks`：校验项结果
  - `name`：校验项名称
  - `status`：校验项状态，取值为 `passed`、`failed` 或 `skipped`
  - `message`：校验说明
- `issues`：问题列表
  - `issue_id`：问题编号，格式为 `issue-NNNN`
  - `severity`：严重程度，取值为 `info`、`warning`、`error` 或 `blocker`
  - `path`：问题位置
  - `message`：问题说明
- `missing_items`：缺失内容，仅章节校验需要
- `affected_section_ids`：受影响章节编号，仅结果校验需要
- `feedback`：返工反馈
  - `reason`：触发原因
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：`true` 或 `false`
- `required_user_input`：`true` 或 `false`

## Status Rules
- `passed`：所有必需校验项通过
- `failed`：存在可通过返工修复的问题
- `blocked`：缺少必要输入、需要用户判断或无法确定校验结论
- `required_user_input` 为 `true` 时，`feedback.question_to_answer` 必须填写
- 不需要用户判断时，`feedback.suggested_action` 必须指向可执行返工动作

## Verification
- 输出文件路径与任务类型一致
- 每个失败检查都有对应 `issues` 记录
- 每个 `issues.path` 指向具体文件字段
- 返工反馈使用统一反馈格式
- 校验失败或阻塞时已通过 Kanban 评论同步给 `research-orchestrator`
