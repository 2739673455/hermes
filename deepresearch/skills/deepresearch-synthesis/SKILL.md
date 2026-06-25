---
name: deepresearch-synthesis
description: 深度研究跨章节综合、建议生成、全局风险和结构化结果组装
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, synthesis, result]
    category: deepresearch
    requires_toolsets: [file]
---
# DeepResearch Synthesis
## When to Use
- 所有章节校验通过后执行综合与组装任务
- 生成 `synthesis/synthesis.json` 和 `result/research_result.json`

## Inputs and Outputs
- 输入：`scheme.json`、`workspace_path`、全部章节的 `sections/<section_id>/research.json`、`sections/<section_id>/section.json` 和章节校验结果
- 输出：`synthesis/synthesis.json`、`result/research_result.json`

## Procedure
1. 读取已保存的章节研究文件、章节正文和章节校验结果
2. 构建跨章节事实索引、冲突清单和风险清单
3. 生成执行摘要、核心结论、跨章节洞察和建议
4. 完成全局来源去重
5. 组装全局可复核事实、全局来源、全局证据链和全局风险
6. 保存 `synthesis/synthesis.json`
7. 保存 `result/research_result.json`

## Rules
- 只使用已保存的章节、来源、事实和证据链
- 综合结论必须能回溯到章节证据链
- 建议必须包含适用条件和风险前提
- 跨章节冲突必须保留冲突说明
- 全局风险写入 `synthesis/synthesis.json`
- `result/research_result.json` 只能组装已存在的章节、来源、证据和综合结果
- 全局来源列表必须去重
- 不得新增事实、来源、判断或证据链

## File Contract
- `synthesis/synthesis.json.executive_summary`：执行摘要
- `synthesis/synthesis.json.core_conclusions`：`conclusion_id`、`text`、`evidence_chain_ids`、`source_ids`
- `synthesis/synthesis.json.cross_section_insights`：`insight_id`、`text`、`section_ids`、`evidence_chain_ids`、`source_ids`
- `synthesis/synthesis.json.recommendations`：`recommendation_id`、`text`、`conditions`、`risks`、`evidence_chain_ids`、`source_ids`
- `synthesis/synthesis.json.conflicts`：`conflict_id`、`description`、`source_ids`
- `synthesis/synthesis.json.global_risks`：`risk_id`、`description`、`applies_to`
- `result/research_result.json`：`project_id`、`scheme`、`sections`、`synthesis`、`facts`、`sources`、`evidence_chains`、`risks`、`deliverables`

## Verification
- 所有必需章节的章节校验均为通过状态
- 全局来源列表已去重
- 全局证据链引用的 `fact_ids` 和 `source_ids` 存在
- 核心结论、跨章节洞察和建议均关联证据链
- `result/research_result.json` 不包含未完成内容或占位符
