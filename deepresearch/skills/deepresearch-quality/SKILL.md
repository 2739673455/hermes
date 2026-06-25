---
name: deepresearch-quality
description: 深度研究章节校验、结果校验、证据引用检查和返工反馈
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, validation, review]
    category: deepresearch
    requires_toolsets: [file]
---
# DeepResearch Quality
## When to Use
- 执行章节校验任务
- 执行结果校验任务

## Inputs and Outputs
- 章节校验输入：`scheme.json`、`section_id`、`workspace_path`、`sections/<section_id>/research.json`、`sections/<section_id>/section.json`
- 章节校验输出：`sections/<section_id>/validation.json`
- 结果校验输入：`scheme.json`、`workspace_path`、全部章节校验结果、`synthesis/synthesis.json`、`result/research_result.json`、全局来源列表、全局证据链
- 结果校验输出：`result/validation.json`

## Procedure
1. 章节校验时检查章节是否对应已确认大纲节点
2. 章节校验时检查正文、关键发现和证据链完整性
3. 章节校验时检查 `source_id`、公开来源 URL 和内部知识库来源类型
4. 结果校验时检查所有章节校验是否通过
5. 结果校验时检查全局来源列表是否去重
6. 结果校验时检查事实、洞察、建议和章节风险说明是否与章节证据链一致
7. 结果校验时检查报告渲染输入是否存在未完成内容或占位符
8. 生成校验结果和返工反馈

## Rules
- 章节正文不能为空
- 每章至少包含一条关键发现和一条证据链
- 证据链引用的 `source_id` 必须存在
- 公开来源必须提供 HTTP URL
- 内部知识库来源必须标记来源类型
- 所有需要正文的章节都已保存
- 所有章节校验已通过后，结果校验才能通过
- 报告渲染输入不包含未完成内容或占位符
- 校验失败时通过 Kanban 评论记录返工反馈
- 返工反馈必须能指向具体失败点

## File Contract
- `status`：`passed`、`failed`、`blocked`
- `checks`：`name`、`status`、`message`
- `issues`：`issue_id`、`severity`、`path`、`message`
- `missing_items`：缺失内容，仅章节校验需要
- `affected_section_ids`：受影响章节编号，仅结果校验需要
- `feedback`：`reason`、`affected_section_ids`、`question_to_answer`、`suggested_action`、`required_user_input`
- `required_user_input`：`true` 或 `false`

## Verification
- `checks.status` 使用 `passed`、`failed`、`skipped`
- `issues.severity` 使用 `info`、`warning`、`error`、`blocker`
- 校验失败时至少包含一个 `issues` 元素
- 需要用户判断时 `required_user_input` 为 `true`
- 不需要用户判断时 `feedback.suggested_action` 指向可执行返工动作
