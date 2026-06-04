---
description: 基于业务树进行需求评审，输出评审结果
handoffs:
  - label: 调整需求后重新评审
    agent: test-case.review
    prompt: 根据用户调整更新业务树并再次评审
  - label: 进入测试大纲
    agent: test-case.outline
    prompt: 需求评审通过，开始构建测试大纲
---

# /test-case.review

## Goal

基于业务树对需求进行评审，发现遗漏、矛盾、模糊点，输出评审结果。

## Operating Constraints

- **只读评审**：不修改需求文档，只输出评审意见
- **基于业务树**：评审必须基于业务树的结构
- **显式引导**：评审维度必须具体

## Pre-Execution Checks

1. 检查`.test-case/business_tree.json`是否存在
2. 加载业务树

## User Input

```text
$ARGUMENTS
```

参数：
- `--adjustment`: 用户的调整描述（可选，用于再评审）

## Execution Steps

### Step 1: 加载业务树

读取`.test-case/business_tree.json`。

### Step 2: 五维度评审

对业务树的每个分支进行评审：

| 维度 | 检查项 | 输出 |
|------|--------|------|
| 完整性 | 是否有遗漏的业务分支？ | 遗漏项列表 |
| 一致性 | 需求之间是否有矛盾？ | 矛盾点列表 |
| 清晰性 | 是否有模糊的描述？ | 模糊点列表 |
| 边界性 | 是否有未定义的边界条件？ | 边界条件列表 |
| 异常性 | 是否有未描述的异常处理？ | 异常处理建议 |

### Step 3: 输出评审结果

生成评审报告，包含所有发现的问题。

### Step 4: 等待用户反馈

如果用户有调整：
- 理解调整意图
- 更新业务树
- 重新评审（回到Step 2）

如果用户满意：
- 标记评审通过
- handoff到outline命令

## Output Format

```json
{
  "review_result": {
    "timestamp": "...",
    "status": "pending/approved",
    "completeness": {
      "missing_items": ["遗漏项1", "遗漏项2"]
    },
    "consistency": {
      "conflicts": ["矛盾点1"]
    },
    "clarity": {
      "vague_points": ["模糊点1"]
    },
    "boundary": {
      "undefined_boundaries": ["边界条件1"]
    },
    "exception": {
      "missing_exception_handling": ["异常处理建议1"]
    },
    "total_issues": 5,
    "resolved_issues": 0
  }
}
```

## Completion Report

```
## 需求评审报告

**评审状态**: {status}

**发现的问题**:
  遗漏项: {count}个
  矛盾点: {count}个
  模糊点: {count}个
  边界条件: {count}个
  异常处理: {count}个

**总计**: {total}个问题

**下一步**:
- 有问题 → 用户调整后重新评审
- 无问题 → 执行 /test-case.outline 构建测试大纲
```

## Done When

- [ ] 五维度评审已执行
- [ ] 评审结果已生成
- [ ] 用户已确认评审结果
- [ ] 如有问题，已根据用户调整更新业务树
- [ ] Completion Report 已展示给用户