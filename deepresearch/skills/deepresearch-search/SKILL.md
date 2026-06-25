---
name: deepresearch-search
description: 深度研究章节检索技能。用于 search-worker profile 按 section_id 执行公开网页、指定站点、上传文件、内部知识库、数据库和外部 API 检索，生成 research.json、来源评估、事实、证据链、冲突、风险和证据缺口反馈
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, search, evidence]
    category: deepresearch
    requires_toolsets: [web, browser, file]
---
# DeepResearch Search
## Role
- 作为资料研究员，为单个章节完成检索、来源评估、事实抽取、冲突识别、证据链整理和风险记录
- 只产出 `sections/<section_id>/research.json` 和必要的缺口反馈

## Inputs
- `scheme.json`
- `section_id`
- `workspace_path`

## Output
- `sections/<section_id>/research.json`

## Procedure
1. 读取 `scheme.json`，通过 `section_id` 定位 `outline` 中的章节
2. 读取章节目标、章节关键问题和 `evidence_requirements`
3. 读取 `scope`、`search_strategy`、`known_sources` 和 `risk_boundary`
4. 扫描已存在的 `sections/*/research.json`，避免生成重复 `source_id`
5. 生成 `search_plan.queries`、`search_plan.source_types` 和 `search_plan.constraints`
6. 按公开网页、指定站点、上传文件、内部知识库、数据库和外部 API 执行可用渠道检索
7. 将召回结果写入 `candidate_sources`
8. 筛选可引用来源并写入 `sources`
9. 对每个可引用来源写入 `source_evaluations`
10. 抽取可复核事实并写入 `facts`
11. 把关键判断组织为 `evidence_chains`
12. 记录互相矛盾的信息、章节风险和证据缺口
13. 保存 `sections/<section_id>/research.json`
14. 检索或证据不足时通过 Kanban 评论提交反馈

## Source Rules
- 来源优先级：官方文件、一手数据、学术论文、行业报告、主流媒体、公司官网、二手转载、社媒内容
- 不得用低可信来源填补关键证据缺口
- 内部知识库不伪装成公开来源
- 公开网页候选来源必须记录最终 HTTP URL
- 上传文件、内部知识库、数据库和 API 来源必须记录 `document_id` 与 `locator`
- 可复核事实不保存大段原文
- 事实文本必须足够具体，能够被 `source_ids` 回溯验证

## Output Schema
- `section_id`：章节编号，格式为 `sNNN`
- `search_plan`：章节搜索计划
  - `queries`：检索词
  - `source_types`：目标来源类型
  - `constraints`：检索约束
- `candidate_sources`：候选来源
  - `candidate_source_id`：候选来源编号，格式为 `cand-<section_id>-NNN`
  - `retrieval_channel`：`web`、`specified_site`、`uploaded_file`、`internal_knowledge`、`database` 或 `api`
  - `title`：原始标题
  - `url`：公开网页最终 URL
  - `document_id`：非公开网页来源的文档编号
  - `locator`：非公开网页来源的片段定位信息
  - `snippet`：摘要片段
  - `retrieved_at`：召回时间，使用 ISO 8601 字符串
- `sources`：可引用来源
  - `source_id`：来源编号，格式为 `src-NNNN`
  - `title`：标题
  - `url`：公开网页最终 URL
  - `document_id`：非公开网页来源的文档编号
  - `locator`：非公开网页来源的片段定位信息
  - `published_at`：发布时间，使用 ISO 8601 字符串或 `null`
  - `source_type`：`official`、`primary_data`、`paper`、`industry_report`、`mainstream_media`、`company_site`、`secondary_repost`、`social_media`、`uploaded_file`、`internal_knowledge`、`database` 或 `api`
  - `summary`：摘要
- `source_evaluations`：来源评估
  - `source_id`：来源编号
  - `credibility`：可信度，取值为 `high`、`medium`、`low` 或 `unknown`
  - `relevance`：相关性，取值为 `high`、`medium`、`low` 或 `unknown`
  - `recency`：时效性，取值为 `high`、`medium`、`low` 或 `unknown`
  - `bias_risk`：偏差风险，取值为 `high`、`medium`、`low` 或 `unknown`
  - `usable_fact_ids`：可用事实编号
- `facts`：可复核事实
  - `fact_id`：事实编号，格式为 `fact-<section_id>-NNN`
  - `text`：事实内容
  - `source_ids`：来源编号
  - `evidence_chain_ids`：证据链编号
- `evidence_chains`：证据链
  - `evidence_chain_id`：证据链编号，格式为 `ev-<section_id>-NNN`
  - `claim`：关键判断
  - `fact_ids`：事实编号
  - `source_ids`：来源编号
- `conflicts`：冲突信息
  - `conflict_id`：冲突编号，格式为 `conflict-<section_id>-NNN`
  - `description`：冲突说明
  - `source_ids`：来源编号
- `risks`：风险说明
  - `risk_id`：风险编号，格式为 `risk-<section_id>-NNN`
  - `description`：风险说明
  - `applies_to`：适用对象
- `gaps`：证据缺口
  - `gap_id`：缺口编号，格式为 `gap-<section_id>-NNN`
  - `description`：缺口说明
  - `required_evidence`：所需证据

## Feedback
- 检索不足、证据不足、范围冲突或需要用户提供内部资料时提交反馈
- 反馈字段：
  - `reason`：触发原因
  - `affected_section_ids`：影响章节
  - `question_to_answer`：待回答问题
  - `suggested_action`：建议动作
  - `required_user_input`：`true` 或 `false`

## Verification
- `section_id` 存在于 `scheme.json.outline`
- `sources.source_id` 在项目 workspace 内唯一
- `candidate_sources` 记录所有重要召回来源
- 每个 `source_evaluations.source_id` 能对应 `sources.source_id`
- 每个 `facts.source_ids` 能对应 `sources.source_id`
- 每个 `evidence_chains.fact_ids` 能对应 `facts.fact_id`
- 每个 `evidence_chains.source_ids` 能对应 `sources.source_id`
- 公开来源包含 HTTP URL
- 内部知识库、上传文件、数据库和 API 来源包含 `document_id` 与 `locator`
