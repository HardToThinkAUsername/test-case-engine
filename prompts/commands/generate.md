---
description: 根据测试大纲和业务树逐个生成测试用例
handoffs:
  - label: 导出Excel
    agent: test-case.export
    prompt: 将测试用例导出为Excel文档
---

# /test-case.generate

## Goal

根据测试大纲和业务树，逐个测试点生成完整的测试用例，确保零遗漏、零冗余。

## Operating Constraints

- **完整性**：每个测试点都必须有用例
- **零冗余**：不得生成重复用例
- **格式完整**：每个用例必须包含所有必需字段
- **先广度再深度**：先列出所有用例，再逐一完善

## Pre-Execution Checks

1. 检查`.test-case/outline.json`是否存在
2. 检查`.test-case/business_tree.json`是否存在

## User Input

```text
$ARGUMENTS
```

参数：
- `--module`: 只生成指定模块的用例（可选）

## Execution Steps

详细执行规则参见 `prompts/extraction-guide.md` Phase 4。

### Step 1: 加载测试大纲和业务树

读取`.test-case/outline.json`和`.test-case/business_tree.json`。

### Step 2: 逐个测试点生成用例

对每个测试点：

1. 识别对应的业务分支
2. 分析该分支的完整流程
3. 根据测试点来源生成用例：

| 来源 | 用例生成规则 |
|------|--------------|
| L1 主路径 | 生成正向用例，覆盖完整正常流程 |
| L2 分支路径 | 生成分支用例，覆盖每个条件走向 |
| L3 异常模板 | 生成异常用例，覆盖每种异常情况 |
| L4 想象力场景 | 生成边界/组合用例 |

### Step 3: 广度追问

生成后追问：
- 从用户误操作角度，还有遗漏吗？
- 从系统故障角度，还有遗漏吗？
- 还有其他场景吗？

### Step 4: 去重验证

- 检查是否有重复用例
- 相同测试点的用例合并
- 确保每个用例有唯一ID

### Step 5: 保存测试用例

保存到`.test-case/test_cases.json`。

## Output Format

```json
{
  "test_cases": [
    {
      "id": "TC001",
      "title": "正常下单支付成功",
      "priority": "P1",
      "type": "positive",
      "source": "L1主路径 | TP-A001",
      "module": "模块A",
      "preconditions": ["用户已登录", "商品存在", "库存充足"],
      "steps": [
        "1. 选择商品",
        "2. 点击提交订单",
        "3. 确认支付信息",
        "4. 完成支付"
      ],
      "expected_result": "订单创建成功，状态变为已支付",
      "related_requirement": "需求文档第3.1条"
    }
  ],
  "coverage_report": {
    "L1": { "covered": 3, "total": 3, "rate": "100%" },
    "L2": { "covered": 7, "total": 7, "rate": "100%" },
    "L3": { "covered": 10, "total": 10, "rate": "100%" },
    "L4": { "cases": 5 },
    "total_cases": 25
  }
}
```

## Completion Report

```
## 测试用例生成完成

**用例总数**: {total}
**重复用例**: {duplicates}个（已合并）

**按优先级**:
  P1: {count}个
  P2: {count}个
  P3: {count}个

**按来源**:
  L1 主路径: {count}个
  L2 分支路径: {count}个
  L3 异常模板: {count}个
  L4 想象力场景: {count}个

**覆盖验证**: ✅
**去重验证**: ✅

**下一步**: 请确认测试用例，或者说"继续"导出Excel文档
```

## Done When

- [ ] `.test-case/test_cases.json` 文件已创建
- [ ] 每个测试点都有对应用例
- [ ] L1-L3覆盖率达到100%
- [ ] 广度追问已收敛
- [ ] 无重复用例
- [ ] 每个用例格式完整（id/title/priority/type/source/preconditions/steps/expected_result）
- [ ] Completion Report 已展示给用户