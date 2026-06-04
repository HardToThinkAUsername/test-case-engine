---
description: 初始化测试用例生成项目，创建宪法文件
handoffs:
  - label: 开始业务建模
    agent: test-case.model
    prompt: 基于已定义的宪法，开始业务建模
---

# /test-case.init

## Goal

初始化测试用例生成项目，创建宪法文件，定义核心原则。

## Operating Constraints

- 宪法一旦创建，核心原则不可修改
- 必须包含显式引导、完整性、先广度再深度、零冗余、边界值覆盖5个原则

## Pre-Execution Checks

检查`.test-case/`目录是否已存在。

## User Input

```text
$ARGUMENTS
```

参数：
- `--project-name`: 项目名称（必须）
- `--document`: 需求文档路径（可选，后续model命令使用）

## Execution Steps

### Step 1: 创建项目目录

创建`.test-case/`目录。

### Step 2: 加载宪法模板

读取`prompts/constitution.md`作为模板。

### Step 3: 适配项目信息

根据用户输入的项目名称，生成项目专属的宪法文件。

### Step 4: 保存宪法文件

保存到`.test-case/constitution.md`。

## Completion Report

```
## 项目初始化完成

**项目名称**: {project_name}
**宪法文件**: .test-case/constitution.md

**下一步**: 请提供需求文档路径，我来帮你开始业务建模
```

## Done When

- [ ] `.test-case/` 目录已创建
- [ ] `.test-case/constitution.md` 文件已创建
- [ ] 宪法包含所有5个核心原则
- [ ] Completion Report 已展示给用户