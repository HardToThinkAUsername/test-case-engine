---
name: test-case-engine
description: "Use this skill any time a requirement document is involved — as input, being discussed, or being reviewed. This includes: generating test cases from PRD, user stories, or functional specs; reviewing requirements for completeness, consistency, clarity, boundary, and exception handling; building test outlines; exporting test cases to Excel. Trigger whenever the user mentions \"测试用例\", \"test case\", \"需求\", \"requirement\", \"PRD\", \"需求文档\", \"需求评审\", \"测试大纲\", \"生成用例\", \"导出Excel\", or references a requirement document. If test cases need to be created, reviewed, outlined, or exported, use this skill."
triggers:
  - 用户上传/提及需求文档
  - 用户说"生成测试用例"
  - 用户说"评审需求"
  - 用户说"测试大纲"
  - 用户说"导出用例"
  - 用户给了PRD/功能说明/用户故事
  - 用户问"怎么测试这个需求"
  - 用户说"帮我写用例"
---

# Test Case Engine

## Quick Reference

| 用户想做什么 | AI 执行什么 |
|-------------|-----------|
| 初始化项目 | 读 `prompts/constitution.md` → 适配项目名 → 保存到 `.test-case/constitution.md` → 自动继续 |
| 分析需求文档 | 读 `prompts/extraction-guide.md` Phase 1 → 构建业务树 → 新开 Agent 追问评审 → 循环直到收敛 → 保存到 `.test-case/business_tree.json` |
| 确认业务树 | 展示业务树摘要 → **等待用户确认** → 支持用户修改（自然语言/JSON/3D交互） |
| 评审需求质量 | 读 `prompts/extraction-guide.md` Phase 2 → 5 维度评审 → 循环直到用户通过 |
| 生成测试大纲 | 读 `prompts/extraction-guide.md` Phase 3 → 按模块组织测试点 → 保存到 `.test-case/outline.json` |
| 生成测试用例 | 读 `prompts/extraction-guide.md` Phase 4 → 逐个测试点生成用例 → 保存到 `.test-case/test_cases.json` |
| 导出 Excel | 调用 `src/excel_exporter.py` → 输出 `.test-case/test_cases.xlsx` |

---

## 禁止行为（最高优先级）

以下行为**绝对禁止**：

- ❌ 业务树构建完成前要求用户确认
- ❌ 需求文档不完整就直接说"无法生成"
- ❌ 跳过 L1-L3 的结构化覆盖，直接让 AI 自由发挥
- ❌ 不读 `prompts/constitution.md` 就开始执行
- ❌ 不读 `prompts/extraction-guide.md` 就自行发挥
- ❌ 生成用例后不验证就保存
- ❌ 用户说"通过"之前就标记 review_result 为 approved
- ❌ 跳过广度追问环节（必须连续 2 轮无新增才能结束）
- ❌ 跳过业务树追问评审（必须新开 agent 追问到无法优化为止）

---

## 执行流程（必须按顺序）

### 1. Init — 初始化（自动执行，无需确认）

```
读 prompts/constitution.md
→ 根据用户提供的项目名称适配
→ 保存到 .test-case/constitution.md
→ 自动进入 Phase 2 业务建模
```

**依赖**：无
**确认**：**不需要用户确认**，自动继续

### 2. Model — 业务建模（自动执行，无需确认）

```
读 prompts/extraction-guide.md Phase 1（完整执行 Step 1-5）
→ Step 1: 逐章节解析需求文档
→ Step 2: 识别所有入口点（用户操作、系统事件、外部触发）
→ Step 3: 追踪每个入口点的完整业务流程到叶子节点
→ Step 4: 识别所有分支点（条件分支、异常分支、状态分支、空分支）
→ Step 5: 构建业务树，保存到 .test-case/business_tree.json
→ Step 6: 生成 L1-L4 场景，广度追问直到连续 2 轮无新增
→ 自动进入 Phase 2.5 业务树追问评审
```

**依赖**：`.test-case/constitution.md` 存在
**确认**：**不需要用户确认**，自动继续

### 2.5. Interrogate — 业务树追问评审（自动执行，必须新开 Agent）

```
目标：用独立视角评审业务树，找出所有遗漏和可优化点

执行方式：
→ 新开一个独立的 Agent（隔离上下文，不受主流程影响）
→ 该 Agent 读取 .test-case/business_tree.json
→ 从以下角度逐项追问：

  1. 入口点是否完整？对比需求文档逐段检查，有没有漏掉的功能入口？
  2. 分支覆盖是否完整？每个入口点的每个分支走向是否都覆盖了？
  3. 异常场景是否充分？L3 的 10 类异常模板是否在每个节点都匹配了？
  4. 隐含逻辑是否挖掘？数据来源、配置依赖、外部系统交互是否都明确了？
  5. 边界条件是否定义？每个参数的边界值、空值、超长值是否覆盖？
  6. 业务规则是否完整？跨模块的约束、状态流转、权限控制是否都体现？

→ 输出问题列表，每项标注：严重程度（高/中/低）、具体位置、改进建议
→ 主流程根据问题列表自动更新业务树
→ 更新后再次新开 Agent 追问
→ 循环直到 Agent 明确回答"无法继续优化"或"未发现新问题"
→ 至少执行 2 轮追问
```

**依赖**：`.test-case/business_tree.json` 存在
**确认**：**不需要用户确认**，追问收敛后自动进入 Phase 3 用户确认

### 3. Confirm — 业务树确认（首次用户交互）

```
展示业务树摘要：
  - 入口点数量及列表
  - 分支点数量
  - L1-L4 各层场景数
  - 追问评审轮数及解决的问题数

展示业务树详情（建议用 3D 可视化或结构化文本）
→ 等待用户确认

用户可能的操作：
  ├─ "通过"/"继续" → 进入 Phase 4 需求评审
  ├─ 提出修改意见 → 理解意图 → 更新业务树 → 重新展示
  └─ 用户手动编辑 business_tree.json → 重新加载 → 重新展示

支持用户修改的方式：
  - 自然语言描述修改（如"增加XX入口点"、"删除YY分支"）
  - 直接编辑 JSON 文件
  - 在 3D 业务树上点击节点增删改
```

**依赖**：`.test-case/business_tree.json` 存在且追问已收敛
**确认**：**首次需要用户确认**，支持反复修改直到用户满意

### 4. Review — 需求评审（循环）

```
读 .test-case/business_tree.json
→ 5 维度逐项评审：
   维度1 - 完整性：是否有遗漏的业务分支？
   维度2 - 一致性：需求之间是否有矛盾？
   维度3 - 清晰性：是否有模糊描述（"等"、"适当"、"必要时"）？
   维度4 - 边界性：每个参数的边界值是否定义？
   维度5 - 异常性：每个操作失败时的处理是否描述？
→ 输出问题列表
→ 保存到 .test-case/review_result.json（status: pending）
→ 等待用户反馈
  │
  ├─ 用户有调整 → 理解意图 → 更新业务树 → 重新评审 → 重复
  └─ 用户明确说"通过"/"可以了"/"继续" → 更新 status 为 approved → 进入下一阶段
```

**依赖**：`.test-case/business_tree.json` 存在
**确认**：每次评审后展示问题列表，等待用户反馈。**用户说"通过"之前绝不标记为 approved**

### 5. Outline — 测试大纲

```
读 .test-case/business_tree.json + .test-case/review_result.json
→ 按模块/功能分组
→ 每个分支生成测试点，标注：
   来源层级：L1 / L2 / L3 / L4
   优先级：P1（核心流程）/ P2（重要分支/异常）/ P3（边界/想象力）
→ 保存到 .test-case/outline.json
→ 展示大纲摘要（模块数、测试点数、按优先级和来源的分布），等待用户确认
```

**依赖**：`review_result.json` 存在且 status 为 approved
**确认**：展示摘要，等待用户确认

### 6. Generate — 生成用例

```
读 .test-case/outline.json + .test-case/business_tree.json
→ 逐个测试点生成完整用例，每个用例必须包含：
   编号(id)、标题(title)、优先级(priority)、类型(type)、
   模块(module)、来源(source)、前置条件(preconditions)、
   操作步骤(steps)、预期结果(expected_result)、关联需求(related_requirement)
→ 广度追问：从用户误操作、系统故障、并发冲突等角度追问是否遗漏
→ 去重验证：检查是否有重复或高度相似的用例
→ 保存到 .test-case/test_cases.json
→ 展示覆盖率报告，等待用户确认
```

**依赖**：`.test-case/outline.json` 存在
**确认**：展示覆盖率报告，等待用户确认

### 7. Export — 导出 Excel

```
读 .test-case/test_cases.json
→ 调用 src/excel_exporter.py 中的 export_to_excel()
→ 生成格式化 Excel（3 个 Sheet）：
    Sheet 1「测试用例明细」— 全量用例，冻结首行，自动筛选，优先级着色
    Sheet 2「统计汇总」— 优先级/模块/类型/来源分布
    Sheet 3「按模块」— 用例按模块分组展示
→ 输出文件路径
```

**依赖**：`.test-case/test_cases.json` 存在

---

## 场景分层

| 层级 | 覆盖目标 | 要求 | 生成方式 |
|------|---------|------|---------|
| L1 主路径 | 每个入口点的正向流程 | 100% | 结构化提取 |
| L2 分支路径 | 每个分支点的每个走向 | 100% | 结构化提取 |
| L3 异常模板 | 每个节点匹配以下 10 类异常 | 100% | 模板匹配 |
| L4 想象力场景 | 10 种增强技术持续挖掘 | 收敛为止 | 广度追问 |

**L3 异常模板（10 类，必须全部覆盖）**：

| # | 类型 | 模板问题 |
|---|------|---------|
| 1 | 前置条件缺失 | "如果前置条件不满足会发生什么？" |
| 2 | 输入异常 | "如果输入为空/非法/超大会发生什么？" |
| 3 | 资源不足 | "如果资源不足会发生什么？" |
| 4 | 外部依赖失败 | "如果外部依赖失败会发生什么？" |
| 5 | 并发冲突 | "如果并发执行会发生什么？" |
| 6 | 超时 | "如果操作超时会发生什么？" |
| 7 | 权限拒绝 | "如果权限不足会发生什么？" |
| 8 | 数据不存在 | "如果数据不存在会发生什么？" |
| 9 | 状态非法 | "如果状态为非法状态会发生什么？" |
| 10 | 空分支 | "如果走空分支会发生什么？" |

**L4 想象力增强技术（10 种）**：

1. 逆向思考 2. 反模式学习 3. 渐进式假设 4. 多角色视角 5. 数据全生命周期 6. 逐层追问 7. 类比推理 8. 组合交叉 9. 时间和顺序 10. 规模和压力

---

## 核心原则（摘要，完整原则见 `prompts/constitution.md`）

1. **显式引导**：不要假设 AI 会自己想到，每个角度都要明确要求
2. **完整性**：L1-L3 必须 100% 覆盖，零遗漏
3. **先广度再深度**：先列出所有场景，再逐个深入
4. **零冗余**：不得生成重复或高度相似的用例
5. **边界值必须覆盖**：每个参数的边界值都应有对应用例
6. **功能测试与性能测试分离**：不在同一份用例中混合

---

## 输出文件

所有文件存放在 `.test-case/` 目录下：

| 文件 | 阶段 | 内容 |
|------|------|------|
| `constitution.md` | Init | 项目宪法 |
| `business_tree.json` | Model | 入口点、业务流程、分支点、L1-L4 场景 |
| `review_result.json` | Review | 5 维度问题 + status (pending/approved) |
| `outline.json` | Outline | 按模块组织的测试点，标注优先级和来源 |
| `test_cases.json` | Generate | 完整测试用例 + 覆盖率报告 |
| `test_cases.xlsx` | Export | 格式化 Excel |

---

## 校验规则

每步执行后必须检查：

- [ ] 输出文件已保存到 `.test-case/` 目录
- [ ] 前序阶段的状态文件存在且有效
- [ ] L1-L3 覆盖率达到 100%
- [ ] 无重复用例
- [ ] **用户已确认当前阶段结果**（这是硬性约束，不确认不能继续）

---

## 文件索引

```
prompts/
├── constitution.md              # 核心原则（最高优先级，每次先读这个）
└── extraction-guide.md          # 完整执行指南（Phase 1-4 详细步骤）
schemas/
└── test-cases.schema.json       # 测试用例输出 JSON Schema（生成后校验）
src/
└── excel_exporter.py            # Excel 导出（openpyxl）
examples/
├── online-shop-prd.md    # 示例需求文档
├── validation-result.md  # 验证记录
└── output/               # 示例输出
```

## Dependencies

CLI 可选。如需使用 CLI：
- Python >= 3.12
- `typer >= 0.12`
- `openpyxl >= 3.1`
- 安装：`pip install -e .`