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
| 初始化项目 | 读 `prompts/constitution.md` → 适配项目名 → 保存到 `.test-case/constitution.md` |
| 分析需求文档 | 读 `prompts/extraction-guide.md` Phase 1 → 构建业务树 → 保存到 `.test-case/business_tree.json` |
| 评审需求质量 | 读 `prompts/extraction-guide.md` Phase 2 → 5 维度评审 → 循环直到用户通过 |
| 生成测试大纲 | 读 `prompts/extraction-guide.md` Phase 3 → 按模块组织测试点 → 保存到 `.test-case/outline.json` |
| 生成测试用例 | 读 `prompts/extraction-guide.md` Phase 4 → 逐个测试点生成用例 → 保存到 `.test-case/test_cases.json` |
| 导出 Excel | 调用 `src/excel_exporter.py` → 输出 `.test-case/test_cases.xlsx` |

---

## 禁止行为（最高优先级）

以下行为**绝对禁止**：

- ❌ 用户没确认当前阶段结果就进入下一阶段
- ❌ 需求文档不完整就直接说"无法生成"
- ❌ 跳过 L1-L3 的结构化覆盖，直接让 AI 自由发挥
- ❌ 不读 `prompts/constitution.md` 就开始执行
- ❌ 不读 `prompts/extraction-guide.md` 就自行发挥
- ❌ 生成用例后不验证就保存
- ❌ 用户说"通过"之前就标记 review_result 为 approved
- ❌ 跳过广度追问环节（必须连续 2 轮无新增才能结束）

---

## 执行流程（必须按顺序，每步必须等用户确认）

### 1. Init — 初始化

```
读 prompts/constitution.md
→ 根据用户提供的项目名称适配
→ 保存到 .test-case/constitution.md
→ 展示完成信息，等待用户提供需求文档
```

**依赖**：无
**确认**：展示项目名称和宪法文件路径，等待用户说"继续"或提供需求文档

### 2. Model — 业务建模

```
读 prompts/extraction-guide.md Phase 1（完整执行 Step 1-5）
→ Step 1: 逐章节解析需求文档
→ Step 2: 识别所有入口点（用户操作、系统事件、外部触发）
→ Step 3: 追踪每个入口点的完整业务流程到叶子节点
→ Step 4: 识别所有分支点（条件分支、异常分支、状态分支、空分支）
→ Step 5: 构建业务树，保存到 .test-case/business_tree.json
→ Step 6: 生成 L1-L4 场景，广度追问直到连续 2 轮无新增
→ 展示业务树摘要（入口点数、分支点数、各层场景数），等待用户确认
```

**依赖**：`.test-case/constitution.md` 存在
**确认**：展示摘要，等待用户说"继续"、"可以了" 或提出调整

### 3. Review — 需求评审（循环）

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

### 4. Outline — 测试大纲

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

### 5. Generate — 生成用例

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

### 6. Export — 导出 Excel

```
读 .test-case/test_cases.json
→ 调用 src/excel_exporter.py 中的 export_to_excel()
→ 生成格式化 Excel：
   冻结首行、P1 用例红色背景、自动筛选、10 列标准格式
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
├── constitution.md       # 核心原则（最高优先级，每次先读这个）
├── extraction-guide.md   # 完整执行指南（Phase 1-4 详细步骤）
└── commands/             # 各阶段独立指令
    ├── init.md
    ├── model.md
    ├── review.md
    ├── outline.md
    ├── generate.md
    └── export.md
src/
├── cli.py                # CLI 入口（可选，typer 实现）
├── session_service.py    # 状态文件管理
└── excel_exporter.py     # Excel 导出（openpyxl）
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