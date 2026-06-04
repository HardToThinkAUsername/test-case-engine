---
description: 将测试用例导出为Excel文档
handoffs: []
---

# /test-case.export

## Goal

将测试用例导出为格式化的Excel文档，便于测试团队使用。

## Operating Constraints

- **格式规范**：遵循标准测试用例Excel格式
- **内容完整**：所有字段必须完整
- **可读性**：列宽、颜色、冻结行等便于阅读

## Pre-Execution Checks

1. 检查`.test-case/test_cases.json`是否存在

## User Input

```text
$ARGUMENTS
```

参数：
- `--output`: 输出Excel文件路径（默认`.test-case/test_cases.xlsx`）

## Execution Steps

### Step 1: 加载测试用例

读取`.test-case/test_cases.json`。

### Step 2: 创建Excel工作簿

使用openpyxl创建Excel工作簿。

### Step 3: 写入表头

标准表头：

| 列 | 字段 | 宽度 |
|----|------|------|
| A | 用例编号 | 12 |
| B | 用例标题 | 40 |
| C | 优先级 | 8 |
| D | 用例类型 | 10 |
| E | 所属模块 | 15 |
| F | 来源 | 20 |
| G | 前置条件 | 30 |
| H | 操作步骤 | 50 |
| I | 预期结果 | 40 |
| J | 关联需求 | 20 |

### Step 4: 写入用例数据

逐行写入每个测试用例。

### Step 5: 格式化

- 冻结首行
- 设置列宽
- P1用例标红背景
- 自动筛选

### Step 6: 保存文件

保存到指定路径。

## Completion Report

```
## Excel导出完成

**文件路径**: {output_path}
**用例总数**: {total}

**优先级分布**:
  P1: {count}个
  P2: {count}个
  P3: {count}个

**文件已就绪，可以分享给测试团队。**
```

## Done When

- [ ] Excel文件已生成
- [ ] 表头完整（10列）
- [ ] 所有用例已写入
- [ ] 格式化已完成（冻结行、列宽、颜色）
- [ ] Completion Report 已展示给用户