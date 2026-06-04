---
description: 基于需求文档进行业务建模，构建业务树
handoffs:
  - label: 进行需求评审
    agent: test-case.review
    prompt: 基于业务树进行需求评审
---

# /test-case.model

## Goal

基于需求文档进行业务建模，构建完整的业务树，通过L1-L4分层覆盖所有场景。

## Operating Constraints

- **显式引导**：每个要求必须具体明确
- **完整性**：零遗漏
- **先广度再深度**

## Pre-Execution Checks

1. 检查`.test-case/constitution.md`是否存在
2. 加载宪法文件
3. 确认需求文档路径

## User Input

```text
$ARGUMENTS
```

参数：
- `--document`: 需求文档路径（必须）

## Execution Steps

详细执行规则参见 `prompts/extraction-guide.md` Phase 1。

### Step 1: 解析需求文档

读取需求文档，识别用户故事、功能模块、业务流程。

### Step 2-5: 构建业务树

按提取指南 Step 2-5 执行：
1. 识别业务入口点
2. 追踪业务流程
3. 识别分支点
4. 构建业务树

### Step 6: L1-L4 场景生成

按提取指南的L1-L4分层覆盖规则生成所有场景。

### Step 7: 广度追问

反复追问直到收敛（连续2轮无新增）。

### Step 8: 保存业务树

保存到`.test-case/business_tree.json`。

## Completion Report

```
## 业务建模完成

**需求文档**: {document_path}

**业务树**:
  入口点: {entry_points}个
  分支点: {branch_points}个
  叶子节点: {leaf_nodes}个

**场景覆盖**:
  L1 主路径: {count}个 (100%)
  L2 分支路径: {count}个 (100%)
  L3 异常模板: {count}个 (100%)
  L4 想象力场景: {count}个

**广度追问**: {rounds}轮, {converged}

**下一步**: 请告诉我是否需要调整业务树，或者说"继续"进入需求评审
```

## Done When

- [ ] `.test-case/business_tree.json` 文件已创建
- [ ] 所有入口点已识别
- [ ] 所有分支点已识别，空分支已标记
- [ ] L1-L3覆盖率达到100%
- [ ] L4广度追问已收敛
- [ ] Completion Report 已展示给用户