---
name: deepresearch-section
description: 深度研究章节写作、关键发现、表格、图表说明和章节风险说明
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, writing, section]
    category: deepresearch
    requires_toolsets: [file]
---
# DeepResearch Section
## When to Use
- 执行章节写作任务
- 把章节证据转成 `sections/<section_id>/section.json`

## Inputs and Outputs
- 输入：`scheme.json`、`section_id`、`workspace_path`、`sections/<section_id>/research.json`
- 输出：`sections/<section_id>/section.json`

## Procedure
1. 读取 `scheme.json` 的 `outline` 中对应章节
2. 读取当前章节的 `research.json`
3. 整理章节写作要点和关键发现候选
4. 写作正文段落、关键发现、表格、图表说明和章节风险说明
5. 关联正文段落、表格和图表的 `source_ids`
6. 保存 `sections/<section_id>/section.json`

## Rules
- 写作要点必须对应已确认大纲节点
- 不得把未验证信息列为关键发现
- 每条关键判断必须关联 `evidence_chains`
- 正文段落、表格和图表必须分别记录 `source_ids`
- `evidence_chains.source_ids` 必须能对应到 `sources.source_id`
- 章节正文不得新增无来源事实
- 章节风险说明必须覆盖证据不足、口径差异、时效性不足、样本偏差和适用边界
- 未完成内容不得进入 `sections/<section_id>/section.json`

## File Contract
- `section_id`：章节编号，格式为 `sNNN`
- `title`：章节标题
- `objective`：章节目标
- `key_findings`：`finding_id`、`text`、`evidence_chain_ids`、`source_ids`
- `body`：`block_id`、`heading`、`text`、`evidence_chain_ids`、`source_ids`
- `tables`：`title`、`columns`、`rows`、`source_ids`
- `charts`：`title`、`chart_type`、`description`、`data`、`source_ids`
- `evidence_chains`：`evidence_chain_id`、`claim`、`fact_ids`、`source_ids`
- `risks`：`risk_id`、`description`、`applies_to`
- `source_ids`：章节引用来源编号

## Verification
- 章节正文不为空
- 至少包含一条关键发现和一条证据链
- 每条正文段落、表格和图表都有对应来源编号
- 关键发现关联的证据链存在
- 章节引用来源编号能对应到 `research.json` 的 `sources.source_id`
