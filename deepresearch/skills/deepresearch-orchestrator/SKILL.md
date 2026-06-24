---
name: deepresearch-orchestrator
description: DeepResearch 编排器，用于接收研究需求、确认研究方案、创建项目 workspace、拆解 Hermes Kanban 任务、协调 worker 反馈并完成根任务
version: 0.1.0
metadata:
  hermes:
    tags: [deepresearch, research, orchestrator]
    category: research
---
# DeepResearch Orchestrator
## When to Use
当 Hermes profile 被分配到 DeepResearch 根任务，并需要把自然语言研究需求推进为可追踪、可恢复、可验收的研究报告时，加载本 skill。

## Runtime Contract
- 启动后先调用 `kanban_show()` 读取根任务标题、正文、父任务交接、历史运行记录和评论串
- 在 `$HERMES_KANBAN_WORKSPACE` 下创建和维护项目文件；如果该环境变量不存在，使用当前工作目录
- 用 Kanban 保存任务状态、依赖关系、评论、人工确认、阻塞原因、重试记录和 worker 交接
- 用文件系统保存研究业务产物
- 定期调用 `kanban_heartbeat(note="...")` 写入进度
- 需要用户输入时调用 `kanban_block(reason="...")`
- 根任务完成时调用 `kanban_complete(summary="...", metadata={...})`

## Workspace Layout
每个研究项目创建一个独立目录，目录名使用 `deepresearch/<project_id>/`。

```text
deepresearch/<project_id>/
  project.json
  scheme.json
  sections/
    <section_id>/
      candidate_sources.jsonl
      sources.jsonl
      source_assessments.jsonl
      fact_cards.jsonl
      evidence_chains.jsonl
      conflict_notes.jsonl
      risk_notes.jsonl
      section.json
      validation.json
  synthesis/
    synthesis.json
    insights.jsonl
    recommendations.jsonl
  result/
    research_result.json
    validation.json
  reports/
    report.html
    report_version.json
```

## Project Manifest
创建 workspace 后写入 `project.json`。

```json
{
  "project_id": "dr-20260624-153000-topic",
  "workspace_path": "deepresearch/dr-20260624-153000-topic",
  "root_task_id": "<kanban_task_id>",
  "phase": "planning",
  "created_at": "<iso8601>",
  "updated_at": "<iso8601>"
}
```

`project.json.phase` 只记录研究业务阶段，可用值为 `planning`、`researching`、`synthesizing`、`validating`、`rendering`、`delivered`。

## ResearchScheme
用户确认研究方向后写入 `scheme.json`。`scheme.json` 是任务拆解、检索、写作和验收的共同依据。

- `research_goal`：研究目标和最终需要回答的问题
- `key_questions`：必须回答的关键问题
- `scope`：研究边界与约束，包括研究范围、排除项和口径限制
- `assumptions`：可选，执行研究时默认采用的前提假设
- `methodology`：分析方法，如 SWOT、PEST、对比分析、案例研究、定量分析等
- `search_strategy`：检索方法与来源筛选标准，包括检索方向、搜索范围、来源类型优先级、可信度与时效性要求
- `known_sources`：已知要查阅的具体数据库、文档、平台或内部知识库清单
- `outline`：章节结构、章节目标和章节证据要求
- `deliverables`：最终交付内容，包括 HTML 报告、执行摘要、表格、图表和数据附录
- `acceptance_criteria`：验收标准，包括问题覆盖、证据链完整性、引用有效性和格式要求
- `risk_boundary`：输出结论时必须说明的限制、不确定性和适用边界

## Procedure
1. 读取根任务中的研究需求和评论中的补充信息。
2. 判断当前需求是否缺少会影响研究方案的必要边界。
3. 需要用户确认边界时，使用 `kanban_block(reason="...")` 提出具体问题。
4. 用户明确边界或明确不限定后，生成 `scheme.json` 草案。
5. 请求用户确认研究方案；确认前不得创建检索、审查、写作或渲染任务。
6. 用户确认后，将 `project.json.phase` 更新为 `researching`。
7. 按 `scheme.json.outline` 创建章节任务链。
8. 所有章节校验通过后，创建综合、结果校验和报告渲染任务。
9. 读取所有 worker 结果并判断根任务是否满足完成条件。
10. 满足完成条件后完成根任务。

## Task Graph
每个章节创建一条顺序任务链。

```text
search-worker
  -> section-writer
  -> quality-reviewer
```

所有章节任务链完成后创建全局任务链。

```text
synthesis-writer
  -> quality-reviewer
  -> report-renderer
```

## Child Task Contract
每个子任务正文必须包含以下字段。

- `project_id`
- `section_id`，仅章节任务需要
- `workspace_path`
- `assignee`
- `inputs`
- `outputs`
- `objective`
- `constraints`
- `acceptance_criteria`

## Search Task
`search-worker` 任务输出候选来源、可引用来源、来源评估和事实证据。

```text
Title: 搜索并整理章节证据 <section_id>：<section_title>
Assignee: search-worker

project_id: <project_id>
section_id: <section_id>
workspace_path: <workspace_path>

Inputs:
- scheme: <workspace_path>/scheme.json

Outputs:
- candidate_sources: <workspace_path>/sections/<section_id>/candidate_sources.jsonl
- sources: <workspace_path>/sections/<section_id>/sources.jsonl
- source_assessments: <workspace_path>/sections/<section_id>/source_assessments.jsonl
- fact_cards: <workspace_path>/sections/<section_id>/fact_cards.jsonl
- evidence_chains: <workspace_path>/sections/<section_id>/evidence_chains.jsonl
- conflict_notes: <workspace_path>/sections/<section_id>/conflict_notes.jsonl
- risk_notes: <workspace_path>/sections/<section_id>/risk_notes.jsonl

Objective:
<章节目标>

Constraints:
<研究边界、来源范围、时效性要求>

Acceptance criteria:
- 候选来源包含检索渠道、标题、URL 或文档编号、摘要片段和召回信息
- 公开网页候选来源包含最终 URL
- 内部知识库候选来源包含数据集和片段定位
- 每个可引用来源都有项目内唯一的 `source_id`
- 每个 `Source` 都关联 `SourceAssessment`
- 事实卡片只保存可复核事实
- 冲突事实写入 `ConflictNote`
- 所有输出只写入当前章节目录
```

## Section Task
`section-writer` 任务输出单章结构化正文。

```text
Title: 写作章节 <section_id>：<section_title>
Assignee: section-writer

project_id: <project_id>
section_id: <section_id>
workspace_path: <workspace_path>

Inputs:
- scheme: <workspace_path>/scheme.json
- sources: <workspace_path>/sections/<section_id>/sources.jsonl
- source_assessments: <workspace_path>/sections/<section_id>/source_assessments.jsonl
- fact_cards: <workspace_path>/sections/<section_id>/fact_cards.jsonl
- evidence_chains: <workspace_path>/sections/<section_id>/evidence_chains.jsonl
- conflict_notes: <workspace_path>/sections/<section_id>/conflict_notes.jsonl
- risk_notes: <workspace_path>/sections/<section_id>/risk_notes.jsonl

Outputs:
- section: <workspace_path>/sections/<section_id>/section.json

Acceptance criteria:
- 章节正文对应已确认大纲节点
- 每条关键判断关联证据链
- 章节风险说明覆盖证据不足、口径差异、时效性不足、样本偏差和适用边界
- 不新增无来源事实
```

## Section Validation Task
`quality-reviewer` 任务输出章节校验。

```text
Title: 校验章节 <section_id>：<section_title>
Assignee: quality-reviewer

project_id: <project_id>
section_id: <section_id>
workspace_path: <workspace_path>

Inputs:
- scheme: <workspace_path>/scheme.json
- section: <workspace_path>/sections/<section_id>/section.json
- sources: <workspace_path>/sections/<section_id>/sources.jsonl
- evidence_chains: <workspace_path>/sections/<section_id>/evidence_chains.jsonl

Outputs:
- validation: <workspace_path>/sections/<section_id>/validation.json

Acceptance criteria:
- 校验结果包含通过状态、问题列表、严重级别和返工建议
- 证据链引用的 `source_id` 必须存在
- 公开来源必须提供 HTTP URL
- 内部知识库来源必须标记来源类型
```

## Synthesis Task
`synthesis-writer` 任务输出跨章节综合结果，完成全局来源去重，并组装 `ResearchResult`。

```text
Title: 综合研究结果
Assignee: synthesis-writer

project_id: <project_id>
workspace_path: <workspace_path>

Inputs:
- scheme: <workspace_path>/scheme.json
- sections: <workspace_path>/sections/

Outputs:
- synthesis: <workspace_path>/synthesis/synthesis.json
- insights: <workspace_path>/synthesis/insights.jsonl
- recommendations: <workspace_path>/synthesis/recommendations.jsonl
- research_result: <workspace_path>/result/research_result.json

Acceptance criteria:
- 综合结论能回溯到章节证据链
- 建议包含适用条件和风险前提
- 跨章节冲突保留冲突说明
- 全局来源列表完成去重
- `ResearchResult` 只能组装已存在的章节、来源、证据和综合结果
```

## Result Validation Task
`quality-reviewer` 任务输出全局结果校验。

```text
Title: 校验研究结果
Assignee: quality-reviewer

project_id: <project_id>
workspace_path: <workspace_path>

Inputs:
- scheme: <workspace_path>/scheme.json
- sections: <workspace_path>/sections/
- synthesis: <workspace_path>/synthesis/synthesis.json
- research_result: <workspace_path>/result/research_result.json

Outputs:
- validation: <workspace_path>/result/validation.json

Acceptance criteria:
- 所有必需章节已有通过状态的章节校验
- `ResearchResult` 包含完整章节、全局来源列表、证据链、综合结论、建议和风险说明
- 全局来源列表已去重
- 报告渲染输入不包含占位内容
```

## Report Task
`report-renderer` 任务输出最终 HTML 报告和版本记录。

```text
Title: 渲染研究报告
Assignee: report-renderer

project_id: <project_id>
workspace_path: <workspace_path>

Inputs:
- research_result: <workspace_path>/result/research_result.json
- validation: <workspace_path>/result/validation.json

Outputs:
- report: <workspace_path>/reports/report.html
- report_version: <workspace_path>/reports/report_version.json

Acceptance criteria:
- 报告基于 `ResearchResult` 确定性生成
- `result/validation.json` 必须为通过状态
- 渲染阶段不得新增事实、来源、判断或证据链
- 报告包含执行摘要、正文、表格或图表、来源列表、风险说明和版本信息
```

## Feedback Handling
worker 发现信息缺口、证据不足、任务边界冲突或需要返工时，编排器读取 Kanban 评论和任务结果后创建后续任务或阻塞根任务。

worker 反馈必须包含：

- `reason`
- `affected_section_ids`
- `question_to_answer`
- `suggested_action`
- `required_user_input`

如果 `required_user_input` 为 `true`，调用 `kanban_block(reason="...")`。如果不需要用户输入，创建最小必要后续任务。

## Completion
满足以下条件后完成根任务。

- `scheme.json` 已存在并经过用户确认
- 所有必需章节都有 `section.json`
- 所有必需章节都有通过状态的 `validation.json`
- `synthesis/synthesis.json` 已存在
- `result/research_result.json` 已存在
- `result/validation.json` 已存在并通过
- `reports/report.html` 已存在
- `reports/report_version.json` 已存在
- 没有未解决阻塞

## Pitfalls
- 不要在研究方案确认前启动检索任务
- 不要把 Kanban 已维护的状态、依赖、评论、事件和重试历史复制成研究业务对象
- 不要把 worker 评论当作已验证事实
- 不要让报告渲染阶段新增事实、来源、判断或证据链
- 不要在章节校验失败时完成根任务

## Verification
- frontmatter 包含 `name`、`description`、`version` 和 `metadata.hermes`
- `project.json`、`scheme.json` 和所有约定输出路径存在
- 子任务正文包含 `project_id`、`workspace_path`、`inputs`、`outputs` 和 `acceptance_criteria`
- 根任务完成摘要包含报告路径、版本记录路径和剩余风险
