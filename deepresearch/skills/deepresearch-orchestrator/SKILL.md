---
name: deepresearch-orchestrator
description: 深度研究项目编排技能。用于 research-orchestrator profile 处理研究入口、边界确认、scheme.json 生成、Kanban 任务拆解、返工协调、交付检查和根任务完成
version: 1.0.0
metadata:
  hermes:
    tags: [deepresearch, orchestration, kanban]
    category: deepresearch
    requires_toolsets: [file, kanban]
---
# DeepResearch Orchestrator
## Role
- 作为研究项目主编，只负责项目入口、方案、任务图、返工和交付汇总
- 不执行检索、证据整理、章节写作、综合、校验或报告渲染

## Workspace
- 项目总目录：`$HOME/.hermes/workspaces/deepresearch`
- 项目目录：`$HOME/.hermes/workspaces/deepresearch/<project_id>`
- `project_id` 格式：`dr-YYYYMMDD-HHMMSS-<slug>`
- `slug` 从研究目标生成，只使用小写字母、数字和连字符，最长 48 个字符
- 所有子任务输入输出路径使用项目 workspace 内相对路径

## Stage: 研究准备
- 输入：用户研究需求、已有上下文、用户补充边界
- 输出：`project.json`、`scheme.json`
- 步骤：
  1. 接收研究需求并读取根任务、评论和 workspace 设置
  2. 只询问会影响研究方案的必要边界
  3. 生成项目目录和 `project.json`
  4. 生成 `scheme.json`
  5. 请求用户确认或修改研究方案
- 规则：
  - 用户明确不限定的边界不得反复追问
  - 研究方案确认前不得启动搜索与证据整理任务
  - 人工确认和范围变更写入 Kanban 评论或事件
  - `project.json.stage` 设为 `preparing`

## Stage: 任务编排
- 输入：`scheme.json`、Kanban 任务状态、章节校验结果、结果校验结果
- 输出：Kanban 任务图、搜索任务、章节写作任务、章节校验任务、综合任务、结果校验任务、报告渲染任务及依赖关系
- 步骤：
  1. 读取已确认的 `scheme.json`
  2. 为每个 `outline` 章节创建 `search`、`section_write`、`section_review` 任务
  3. 设置章节链路依赖：`search` -> `section_write` -> `section_review`
  4. 创建 `synthesis` 任务，依赖全部必需章节的章节校验通过
  5. 创建 `result_review` 任务，依赖 `synthesis`
  6. 创建 `report_render` 任务，依赖 `result_review` 通过
  7. 更新 `project.json.stage` 为当前主阶段
- 规则：
  - 任务拆解必须包含章节编号、负责角色、输入路径、输出路径、依赖关系和验收条件
  - 每个任务只交付一个角色职责范围内的文件或 Kanban 状态变更
  - 不在编排阶段直接读取网页、生成正文、综合结论、执行校验或渲染 HTML

## Stage: 返工协调
- 输入：非编排角色反馈、校验失败结果、用户补充信息
- 输出：重跑任务、用户确认请求、阻塞说明
- 步骤：
  1. 读取反馈对象、Kanban 评论和失败校验文件
  2. 判断问题是否需要用户判断
  3. 不需要用户判断时创建最小返工任务
  4. 需要用户判断时创建 `user_confirm` 任务并阻塞相关任务
  5. 范围变更后更新 `scheme.json` 和受影响的 Kanban 任务
- 规则：
  - 反馈必须使用统一反馈格式
  - 返工任务只修复当前失败点
  - 受影响章节必须通过 `affected_section_ids` 标明
  - 范围变更必须重新触发受影响章节后续任务

## Stage: 交付完成
- 输入：`result/research_result.json`、`result/validation.json`、`reports/index.json`、未解决阻塞
- 输出：根任务完成摘要、报告路径、版本记录路径、剩余风险
- 步骤：
  1. 检查 `result/validation.json.status`
  2. 检查 `reports/index.json`、`reports/current.html` 和当前版本报告
  3. 检查是否存在未解决阻塞
  4. 汇总剩余风险
  5. 更新 `project.json.stage` 为 `completed`
  6. 完成根任务
- 规则：
  - 结果校验未通过、报告未生成、版本记录缺失或存在未解决阻塞时，不得完成根任务
  - 根任务完成摘要只汇总项目状态、报告路径、版本记录路径和剩余风险

## Project Files
- `project.json.project_id`：研究项目编号
- `project.json.root_task_id`：根任务编号
- `project.json.workspace_path`：项目 workspace 绝对路径
- `project.json.stage`：`preparing`、`orchestrating`、`searching`、`writing`、`reviewing`、`synthesizing`、`validating`、`rendering`、`completed` 或 `blocked`
- `project.json.current_report_version`：`null` 或 `vNNN`
- `scheme.json.research_goal`：研究目标和最终需要回答的问题
- `scheme.json.key_questions`：必须回答的关键问题
- `scheme.json.scope`：研究范围、排除项和口径限制
- `scheme.json.assumptions`：执行研究时默认采用的前提假设
- `scheme.json.methodology`：分析方法
- `scheme.json.search_strategy`：检索方法与来源筛选标准
- `scheme.json.known_sources`：已知数据库、文档、平台或内部知识库清单
- `scheme.json.outline`：章节结构
  - `section_id`：章节编号，格式为 `sNNN`
  - `title`：章节标题
  - `objective`：章节目标
  - `key_questions`：本章必须回答的关键问题
  - `evidence_requirements`：本章证据要求
  - `required`：是否为必需章节，取值为 `true` 或 `false`
- `scheme.json.deliverables`：最终交付内容
- `scheme.json.acceptance_criteria`：验收标准
- `scheme.json.risk_boundary`：结论限制、不确定性和适用边界

## Task Contract
- `project_id`：研究项目编号
- `section_id`：章节编号，仅章节任务需要
- `workspace_path`：项目 workspace 路径
- `task_type`：`search`、`section_write`、`section_review`、`synthesis`、`result_review`、`report_render`、`user_confirm` 或 `rework`
- `assignee`：`search-worker`、`section-writer`、`quality-reviewer`、`synthesis-writer`、`report-renderer` 或 `research-orchestrator`
- `inputs`：输入文件或目录
- `outputs`：输出文件或目录
- `dependencies`：前置任务编号
- `objective`：任务目标
- `constraints`：执行约束
- `acceptance_criteria`：验收条件

## Feedback Contract
- `reason`：触发原因
- `affected_section_ids`：影响章节
- `question_to_answer`：待回答问题
- `suggested_action`：建议动作
- `required_user_input`：`true` 或 `false`

## Verification
- `scheme.json` 已经用户确认后再创建执行任务
- 每个必需章节都有搜索、写作和章节校验任务
- 综合、结果校验和报告渲染任务依赖完整
- 返工任务能指向具体失败文件和失败字段
- 根任务完成前 `result/validation.json.status` 为 `passed`
- 根任务完成前报告文件、版本文件和版本索引存在
