---
name: deepresearch-section
description: 深度研究章节写作技能。用于 section-writer profile 将单章 research.json 转成 section.json，生成章节正文、关键发现、表格、图表说明、证据链引用和章节风险说明
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, writing, section]
    category: deepresearch
    requires_toolsets: [file]
---
# DeepResearch Section
## Role
- 作为专题撰稿编辑，把已保存的章节证据转成可校验的章节内容
- 只产出 `sections/<section_id>/section.json` 和必要的返工反馈

## Inputs
- `scheme.json`
- `section_id`
- `workspace_path`
- `sections/<section_id>/research.json`

## Output
- `sections/<section_id>/section.json`

## Procedure
1. 读取 `scheme.json` 并定位 `outline` 中的当前章节
2. 读取当前章节的 `research.json`
3. 校对章节目标、关键问题、证据要求和风险边界
4. 从 `facts`、`evidence_chains`、`sources` 和 `risks` 整理写作要点
5. 选择有证据链支撑的关键发现
6. 写作章节正文段落
7. 根据证据生成表格和图表说明
8. 为关键发现、正文段落、表格和图表绑定 `evidence_chain_ids` 与 `source_ids`
9. 写入章节风险说明
10. 自检无未完成内容、占位符和无来源事实
11. 保存 `sections/<section_id>/section.json`
12. 证据不足或无法完成章节时通过 Kanban 评论提交反馈

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

## Output Schema
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

## Feedback
- 无法完成章节、关键问题缺证、证据链断裂或需要补充资料时提交反馈
- 反馈字段：
  - `reason`：触发原因
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：`true` 或 `false`

## Verification
- `section_id` 存在于 `scheme.json.outline`
- `body` 至少包含一个正文段落
- `key_findings` 至少包含一条关键发现
- `evidence_chains` 至少包含一条证据链
- 每条关键发现关联的证据链存在
- 每条正文段落、表格和图表都有对应来源编号
- 章节引用来源编号能对应到 `research.json.sources.source_id`
- 文件中不包含未完成内容、TODO、占位符或无来源事实
