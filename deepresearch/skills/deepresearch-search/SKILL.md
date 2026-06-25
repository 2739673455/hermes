---
name: deepresearch-search
description: 深度研究章节检索、来源评估、事实抽取和证据链整理
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, search, evidence]
    category: deepresearch
    requires_toolsets: [web, browser, file]
---
# DeepResearch Search
## When to Use
- 执行章节搜索与证据整理任务
- 为单个 `section_id` 生成 `sections/<section_id>/research.json`

## Inputs and Outputs
- 输入：`scheme.json`、`section_id`、`workspace_path`
- 输出：`sections/<section_id>/research.json`

## Procedure
1. 读取 `scheme.json` 的 `outline` 中对应章节
2. 读取 `scope`、`search_strategy`、`known_sources` 和章节证据要求
3. 生成章节搜索计划
4. 执行公开网页、指定站点、上传文件、内部知识库、数据库和外部 API 检索
5. 记录候选来源
6. 评估可引用来源
7. 抽取可复核事实
8. 整理证据链、冲突信息、风险说明和证据缺口
9. 保存 `sections/<section_id>/research.json`
10. 检索或证据不足时通过 Kanban 评论反馈缺口

## Rules
- 章节目标和证据要求通过 `section_id` 从 `scheme.json` 的 `outline` 读取
- 搜索计划必须遵守 `scheme.json` 的 `scope`、`search_strategy`、`known_sources` 和章节证据要求
- 候选来源必须记录检索渠道、原始标题、URL 或文档编号、摘要片段和召回信息
- 公开网页候选来源必须记录最终 URL
- 内部知识库候选来源必须记录数据集和片段定位
- 可引用来源必须包含项目内唯一来源编号、标题、URL 或文档编号、发布时间、来源类型和摘要
- 来源评估必须记录可信度、相关性、时效性、偏差风险和可用事实
- 可复核事实不保存大段原文
- 不得用低可信来源填补关键证据缺口

## File Contract
- `section_id`：章节编号，格式为 `sNNN`
- `search_plan`：`queries`、`source_types`、`constraints`
- `candidate_sources`：`candidate_source_id`、`retrieval_channel`、`title`、`url`、`document_id`、`locator`、`snippet`、`retrieved_at`
- `sources`：`source_id`、`title`、`url`、`document_id`、`locator`、`published_at`、`source_type`、`summary`
- `source_evaluations`：`source_id`、`credibility`、`relevance`、`recency`、`bias_risk`、`usable_fact_ids`
- `facts`：`fact_id`、`text`、`source_ids`、`evidence_chain_ids`
- `evidence_chains`：`evidence_chain_id`、`claim`、`fact_ids`、`source_ids`
- `conflicts`：`conflict_id`、`description`、`source_ids`
- `risks`：`risk_id`、`description`、`applies_to`
- `gaps`：`gap_id`、`description`、`required_evidence`

## Verification
- `sources.source_id` 使用 `src-NNNN`
- `facts.fact_id` 使用 `fact-<section_id>-NNN`
- `evidence_chains.evidence_chain_id` 使用 `ev-<section_id>-NNN`
- 证据链引用的 `fact_ids` 和 `source_ids` 存在
- 公开来源包含 HTTP URL
- 内部知识库、上传文件、数据库和 API 来源包含 `document_id` 与 `locator`
