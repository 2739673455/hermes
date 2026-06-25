---
name: deepresearch-orchestrator
description: 深度研究编排、方案确认、任务拆解、返工协调和交付汇总
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, orchestration, kanban]
    category: deepresearch
    requires_toolsets: [file, kanban]
---
# DeepResearch Orchestrator
## When to Use
- 处理深度研究根任务、研究方案、任务编排、返工协调和交付完成
- 维护 Kanban 任务图、任务依赖、人工确认、范围变更和阻塞状态

## Inputs and Outputs
- 研究准备输入：用户研究需求、已有上下文、用户补充边界
- 研究准备输出：`project.json`、`scheme.json`
- 任务编排输入：`scheme.json`、Kanban 任务状态、章节校验结果、结果校验结果
- 任务编排输出：Kanban 任务图、搜索与证据整理任务、章节写作任务、章节校验任务、综合任务、结果校验任务、报告渲染任务及依赖关系
- 返工协调输入：非编排角色反馈、校验失败结果、用户补充信息
- 返工协调输出：重跑任务、用户确认请求、阻塞说明
- 交付完成输入：`result/research_result.json`、`result/validation.json`、`reports/index.json`、未解决阻塞
- 交付完成输出：根任务完成摘要、报告路径、版本记录路径、剩余风险

## Procedure
1. 接收研究需求并读取 Kanban 根任务、评论和 workspace 信息
2. 确认影响研究方案的必要边界
3. 创建项目 workspace 并写入 `project.json`
4. 生成 `scheme.json` 并请求用户确认研究方案
5. 方案确认后创建章节搜索与证据整理任务、章节写作任务和章节校验任务
6. 所有章节校验通过后创建综合任务、结果校验任务和报告渲染任务
7. 读取反馈和校验失败结果，创建返工任务或用户确认请求
8. 检查结果校验、报告文件、版本记录和未解决阻塞
9. 满足交付条件后完成根任务

## Rules
- 只确认会影响研究方案的边界
- 用户明确不限定的边界不得反复追问
- 研究方案确认前不得启动搜索与证据整理任务
- 人工确认和范围变更写入 Kanban 评论或事件
- 任务拆解必须包含章节编号、负责角色、输入路径、输出路径、依赖关系和验收条件
- 只创建和维护任务，不直接执行检索、写作、综合、校验或渲染
- 反馈必须使用统一反馈格式
- 需要用户判断时阻塞相关任务
- 不需要用户判断时，只创建能修复当前失败点的返工任务
- 范围变更必须更新 `scheme.json` 和受影响的 Kanban 任务
- 结果校验未通过、报告未生成、版本记录缺失或存在未解决阻塞时，不得完成根任务
- 根任务完成摘要只汇总项目状态、报告路径、版本记录路径和剩余风险

## File Contract
- `project.json`：项目编号、根任务编号、workspace 路径、当前研究业务阶段和当前报告版本
- `scheme.json`：研究目标、关键问题、边界、方法、搜索策略、已知来源、大纲、交付物、验收标准和风险边界
- 子任务正文：`project_id`、`section_id`、`workspace_path`、`task_type`、`assignee`、`inputs`、`outputs`、`dependencies`、`objective`、`constraints`、`acceptance_criteria`
- 反馈格式：`reason`、`affected_section_ids`、`question_to_answer`、`suggested_action`、`required_user_input`

## Verification
- `project.json.stage` 使用规定阶段值
- `scheme.json.outline` 使用 `sNNN` 章节编号
- 所有子任务使用项目 workspace 内相对输入输出路径
- 根任务完成前 `result/validation.json` 为通过状态
- 根任务完成前 `reports/index.json`、`reports/current.html` 和版本报告存在
