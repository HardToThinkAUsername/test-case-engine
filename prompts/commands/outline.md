---
description: 基于确认后的业务树构建测试大纲
handoffs:
  - label: 生成测试用例
    agent: test-case.generate
    prompt: 基于测试大纲生成测试用例
---

# /test-case.outline

## Goal

基于确认后的业务树和评审结果，构建结构化的测试大纲。

## Operating Constraints

- **完整性**：业务树的每个分支都必须有对应的测试点
- **分层标注**：每个测试点标注来源层级（L1/L2/L3/L4）
- **优先级标注**：每个测试点标注优先级（P1/P2/P3）

## Pre-Execution Checks

1. 检查`.test-case/business_tree.json`是否存在
2. 检查`.test-case/review_result.json`是否存在且状态为approved

## User Input

```text
$ARGUMENTS
```

参数：无（基于已确认的业务树自动生成）

## Execution Steps

### Step 1: 加载业务树和评审结果

读取`.test-case/business_tree.json`和`.test-case/review_result.json`。

### Step 2: 按模块组织测试点

将业务树按模块/功能分组，每个模块下生成测试点列表：

```
测试大纲
├── 模块A（入口点EP001-EP003）
│   ├── TP-A001: 正常流程（L1）[P1]
│   ├── TP-A002: 条件分支（L2）[P1]
│   ├── TP-A003: 异常处理（L3）[P2]
│   └── TP-A004: 边界场景（L4）[P3]
├── 模块B（入口点EP004-EP005）
│   └── ...
```

### Step 3: 标注优先级

优先级规则：

| 来源 | 默认优先级 | 说明 |
|------|------------|------|
| L1 主路径 | P1 | 核心业务流程，必须测试 |
| L2 分支路径 | P1-P2 | 根据业务重要性判断 |
| L3 异常模板 | P2 | 异常场景，重要但非核心 |
| L4 想象力场景 | P2-P3 | 边界和组合场景 |

### Step 4: 保存测试大纲

保存到`.test-case/outline.json`。

## Output Format

```json
{
  "outline": {
    "modules": [
      {
        "name": "模块A",
        "entry_points": ["EP001", "EP002"],
        "test_points": [
          {
            "id": "TP-A001",
            "name": "正常下单流程",
            "source": "L1主路径",
            "priority": "P1",
            "related_branches": ["BP001", "BP002"],
            "test_focus": "验证正向流程完整性"
          }
        ]
      }
    ]
  },
  "summary": {
    "total_modules": 3,
    "total_test_points": 25,
    "by_priority": { "P1": 10, "P2": 10, "P3": 5 },
    "by_source": { "L1": 3, "L2": 7, "L3": 10, "L4": 5 }
  }
}
```

## Completion Report

```
## 测试大纲构建完成

**模块数**: {modules}
**测试点数**: {test_points}

**按优先级**:
  P1: {count}个
  P2: {count}个
  P3: {count}个

**按来源**:
  L1 主路径: {count}个
  L2 分支路径: {count}个
  L3 异常模板: {count}个
  L4 想象力场景: {count}个

**下一步**: 执行 /test-case.generate 生成测试用例
```

## Done When

- [ ] `.test-case/outline.json` 文件已创建
- [ ] 业务树的每个分支都有对应测试点
- [ ] 每个测试点都有来源层级标注
- [ ] 每个测试点都有优先级标注
- [ ] Completion Report 已展示给用户