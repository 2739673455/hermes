---
name: deepresearch-report
description: 深度研究 HTML 报告渲染和报告版本记录
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, report, html]
    category: deepresearch
    requires_toolsets: [file]
---
# DeepResearch Report
## When to Use
- 结果校验通过后执行报告渲染任务
- 生成 HTML 报告、版本报告和报告版本索引

## Inputs and Outputs
- 输入：`result/research_result.json`、`result/validation.json`、`workspace_path`
- 输出：`reports/current.html`、`reports/vNNN.html`、`reports/index.json`、更新后的 `project.json.current_report_version`

## Procedure
1. 读取 `result/validation.json`
2. 确认结果校验状态为 `passed`
3. 读取 `result/research_result.json`
4. 生成可渲染报告数据
5. 确定性生成 HTML
6. 写入 `reports/current.html`
7. 写入 `reports/vNNN.html`
8. 写入 `reports/index.json`
9. 更新 `project.json.current_report_version`

## Rules
- 结果校验通过后才能渲染
- 报告数据不得包含未完成内容或占位符
- 报告渲染阶段不得新增事实、来源、判断或证据链
- 正文、表格和图表必须附相关来源链接
- 报告必须包含执行摘要、正文、表格或图表、来源汇总、风险说明和版本信息
- `reports/index.json` 必须记录报告格式、引用来源编号、生成时间和存储地址

## File Contract
- `reports/index.json.current_version`：当前版本编号，格式为 `vNNN`
- `reports/index.json.versions`：报告版本列表
- `versions.version`：版本编号，格式为 `vNNN`
- `versions.file_path`：报告文件路径
- `versions.format`：报告格式，取值为 `html`
- `versions.source_ids`：报告引用来源编号
- `versions.generated_at`：生成时间，使用 ISO 8601 字符串
- `versions.note`：版本说明
- `reports/current.html`：当前 HTML 报告
- `reports/vNNN.html`：版本 HTML 报告

## Verification
- `result/validation.json.status` 为 `passed`
- `reports/current.html` 存在
- `reports/vNNN.html` 存在
- `reports/index.json.current_version` 与 `project.json.current_report_version` 一致
- 正文、表格和图表后的来源链接可追溯到 `result/research_result.json.sources`
