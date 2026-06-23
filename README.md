# 测试用例生成系统

> **一句话，AI 帮你从需求文档生成测试用例，输出 Excel。**

<p align="center">
  <a href="https://github.com/HardToThinkAUsername/test-case-engine"><img src="https://img.shields.io/badge/Claude%20Code-Skill-blueviolet" alt="Claude Code Skill"></a>
</p>

---

## 这是什么

一个 **Claude Code Skill**。安装后，你的 AI 编程助手就获得了"测试用例生成"能力——你给需求，它给用例，对话式、可调整、输出 Excel。

**为什么不直接对 AI 说"帮我生成测试用例"？** 因为 AI 写用例看起来全面，实际上会遗漏大量边界场景。这套 skill 提供了一套方法论——业务树建模、L1-L4 分层覆盖、5 维度需求评审、10 种想象力增强技术——确保生成的用例系统性、无遗漏、无冗余。

## 它能做什么

| 能力 | 产出 | 耗时 |
|------|------|------|
| 分析需求文档 | 业务树（入口点、流程、分支点） | 取决于文档复杂度 |
| 评审需求质量 | 5 维度问题清单（完整性、一致性、清晰性、边界性、异常性） | 取决于文档复杂度 |
| 生成测试大纲 | 按模块组织的测试点，标注优先级和来源 | 取决于文档复杂度 |
| 生成测试用例 | 完整用例（编号、步骤、预期结果、关联需求） | 取决于文档复杂度 |
| 导出 Excel | 格式化 Excel，冻结表头，P1 红色标注，支持筛选 | ~10 秒 |

## 怎么用

### 下载

```bash
git clone https://github.com/HardToThinkAUsername/test-case-engine.git
cd test-case-engine
```

在 Claude Code 中打开此目录，直接对话即可。不需要 `pip install`，不需要配置。

```
我有一份需求文档：我的需求文档.md
请帮我按照 test-case-engine 的流程，生成测试用例。
```

AI 会引导你走完整个流程，每一步你都可以确认、调整、或者推翻重来。

### 使用 CLI（可选，需要 Python 3.12+）

```bash
pip install -e .

# 必须按顺序执行（后一步依赖前一步的输出）
test-case-engine init --project-name "我的项目"     # ① 初始化
test-case-engine model --document 我的需求文档.md   # ② 业务建模
test-case-engine review                             # ③ 需求评审（可循环）
test-case-engine outline                            # ④ 测试大纲
test-case-engine generate                           # ⑤ 生成用例
test-case-engine export                             # ⑥ 导出 Excel
```

## 看看效果

以 `examples/online-shop-prd.md`（在线商城需求文档）为例：

| 指标 | 结果 |
|------|------|
| 入口点 | 17 个 |
| 分支点 | 18 个 |
| L1 主路径 | 22 个场景（100%） |
| L2 分支路径 | 23 个场景（100%） |
| L3 异常模板 | 34 个场景（100%） |
| L4 想象力场景 | 40 个场景 |
| 测试模块 | 6 个 |
| 测试用例 | 98 个 |

输出文件：`examples/output/test_cases.xlsx`

## 核心机制

### 业务树建模

不是直接把需求扔给 AI 生成用例。而是先构建"业务树"——从需求文档中系统性提取所有入口点、追踪业务流程、识别所有分支点。业务树是整个流程的核心资产，后续的评审、大纲、用例生成都基于它。

### L1-L4 分层覆盖

| 层级 | 覆盖什么 | 怎么生成 |
|------|---------|---------|
| L1 | 主路径：每个入口点的正向流程 | 结构化提取 |
| L2 | 分支路径：每个分支点的每个走向 | 结构化提取 |
| L3 | 异常模板：10 类异常（前置缺失、输入异常、资源不足、外部依赖失败、并发冲突、超时、权限拒绝、数据不存在、状态非法、空分支） | 模板匹配 |
| L4 | 想象力场景：逆向思考、反模式学习、渐进式假设、多角色视角、数据全生命周期、逐层追问、类比推理、组合交叉、时间和顺序、规模和压力 | 10 种增强技术 + 广度追问 |

### 5 维度需求评审

在生成用例之前，先从完整性、一致性、清晰性、边界性、异常性五个维度评审需求本身。发现的问题在生成用例之前就修复，避免"垃圾进垃圾出"。

### 对话式迭代

每个阶段完成后 AI 都会展示结果并等待你确认。你可以随时用自然语言调整——"把注册拆成手机号和邮箱"、"密码锁定改为 1 小时"。不需要懂技术。

## 支持的文档格式

| 格式 | 处理方式 |
|------|---------|
| `.md` / `.txt` | 直接读取 |
| `.docx` | 需安装 `python-docx`，AI 可协助提取 |
| `.pdf` | 需安装 `pdfplumber`，AI 可协助提取 |
| 直接粘贴 | 最简单，把需求内容复制到对话中 |

## 仓库结构

```
test-case-engine/
├── SKILL.md                  # Skill 注册入口（AI 读这个）
├── README.md                 # 你正在看的文件
├── prompts/
│   ├── constitution.md       # 核心原则（最高优先级）
│   ├── extraction-guide.md   # 完整执行指南（Phase 1-4）
│   └── commands/             # 各阶段独立指令
├── src/
│   ├── cli.py                # CLI 入口（可选）
│   ├── session_service.py    # 状态文件管理
│   └── excel_exporter.py     # Excel 导出
└── examples/
    ├── online-shop-prd.md    # 示例需求文档
    ├── validation-result.md  # 验证记录
    └── output/               # 示例输出
```

## 常见问题

**Q: 这个 skill 和直接对 AI 说"帮我写测试用例"有什么区别？**
A: 直接写 AI 会遗漏大量边界场景。这套 skill 有系统的方法论——业务树建模、L1-L4 分层覆盖、5 维度需求评审、10 种想象力增强技术——确保零遗漏、零冗余。

**Q: 需要安装什么？**
A: 纯对话方式不需要任何安装。CLI 方式需要 Python 3.12+。

**Q: 生成的用例数量是固定的吗？**
A: 不固定。取决于需求文档的复杂度，从几十到几百个。

**Q: 生成的用例在哪里？**
A: `.test-case/test_cases.xlsx`。

**Q: 我能中途调整吗？**
A: 每个阶段都可以。直接告诉 AI 你想怎么改。

**Q: 没有 AI 编程助手怎么办？**
A: 推荐安装 Claude Code（https://claude.ai/code）。