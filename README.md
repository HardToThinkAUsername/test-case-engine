# 测试用例生成系统

基于业务树建模方法论的AI测试用例生成工具。

## 核心特点

- 从业务需求文档自动生成测试用例
- L1-L4分层覆盖，确保零遗漏
- 10种想象力增强技术，生成边界场景
- 功能测试与性能测试自动分离
- 输出Excel文档，直接可用

## 安装方式

### 最简单的安装

1. 克隆或下载这个仓库
2. 在AI编程助手中打开这个目录
3. 告诉AI："请按照prompts/extraction-guide.md的流程，帮我从需求文档生成测试用例"

**不需要安装任何东西**，skill就是prompt文件，AI直接读取即可。

### 具体步骤

**步骤1：获取代码**
```bash
git clone https://github.com/HardToThinkAUsername/test-case-engine.git
```

**步骤2：告诉AI如何使用**
```
请读取 test-case-engine/prompts/extraction-guide.md，
然后按照流程帮我从需求文档生成测试用例。
我的需求文档路径是：/path/to/your-prd.md
```

**步骤3：AI会自动执行**
- 读取skill文件
- 按照流程执行
- 生成业务树、测试用例

### 可选：安装Python依赖

如果你需要CLI命令或Excel导出功能：
```bash
cd test-case-engine
pip install -e .
```

## 快速开始

### 方式一：使用CLI命令

```bash
# 初始化项目
test-case-engine init --project-name "我的项目"

# 查看状态
test-case-engine status

# 业务建模
test-case-engine model --document /path/to/your-prd.md

# 需求评审
test-case-engine review --adjustment "密码锁定改为1小时"

# 生成测试大纲
test-case-engine outline

# 生成测试用例
test-case-engine generate

# 导出Excel
test-case-engine export --output /path/to/output.xlsx

# 查看说明
test-case-engine explain
test-case-engine explain constitution
test-case-engine explain model
```

### 方式二：在Claude对话框中使用（推荐）

1. 打开Claude Code
2. 告诉Claude：
   ```
   请读取 /path/to/test-case-engine/prompts/extraction-guide.md，
   然后按照流程帮我从需求文档生成测试用例。
   我的需求文档是：/path/to/your-prd.md
   ```
3. Claude会读取skill文件，按照流程执行
4. 你可以通过自然语言调整业务树、修改评审结果

**支持的文档格式**：
- `.md` / `.txt` → 直接读取
- `.docx` → Claude会提示你转换为.txt，或用Python脚本提取
- `.pdf` → Claude会提示你复制粘贴内容

## 文件结构

```
test-case-engine/
├── prompts/                    # Skill文件（Claude读取的prompt）
│   ├── constitution.md        # 核心原则
│   ├── extraction-guide.md    # 执行步骤
│   └── commands/              # 各阶段命令
│       ├── init.md
│       ├── model.md
│       ├── review.md
│       ├── outline.md
│       ├── generate.md
│       └── export.md
├── examples/                  # 示例需求文档
│   └── online-shop-prd.md    # 在线商城示例
├── src/                       # 代码（辅助工具）
│   ├── cli.py                # CLI命令
│   ├── session_service.py    # 会话管理
│   └── excel_exporter.py     # Excel导出
├── SKILL.md                  # Skill元数据（OpenCode需要）
└── examples/output/          # 示例输出
    ├── business_tree.json    # 业务树示例
    ├── outline.json          # 测试大纲示例
    ├── test_cases.json       # 测试用例示例
    └── test_cases.xlsx       # Excel示例
```

## SKILL.md说明

`SKILL.md`是skill的元数据文件，包含：
- skill的名称和描述
- 核心原则
- 执行流程
- 使用说明

OpenCode等AI编程助手会读取这个文件来识别和加载skill。

## 使用流程

```
Phase 1: 业务建模
  上传需求文档 → 识别入口点 → 追踪流程 → 构建业务树

Phase 2: 需求评审（可循环）
  五维度评审 → 输出问题 → 用户调整 → 再次评审

Phase 3: 测试大纲
  按模块组织 → 标注优先级 → 标注来源层级

Phase 4: 用例生成
  逐个场景生成 → 广度追问 → 去重验证

Phase 5: 导出
  生成Excel → 分离功能/性能测试
```

## 示例

参考 `examples/online-shop-prd.md` 查看示例需求文档。

示例输出保存在 `examples/output/` 目录：
- `business_tree.json` - 业务树
- `outline.json` - 测试大纲
- `test_cases.json` - 测试用例
- `test_cases.xlsx` - Excel文档

实际使用时，输出保存在 `.test-case/` 目录。

## 常见问题

### Q: Claude不识别命令怎么办？
A: 在Claude对话框中直接说"按照test-case-engine流程执行"，Claude会读取skill文件。

### Q: 如何调整业务树？
A: 在对话中直接说自然语言指令，如"把注册拆分成手机号和邮箱"。

### Q: 如何修改测试用例？
A: 在对话中说"用例XXX的步骤需要修改..."，Claude会更新用例。

### Q: 输出的Excel在哪里？
A: 默认保存在 `.test-case/test_cases.xlsx`。

## 技术支持

如有问题，请提供：
1. 使用的命令或对话内容
2. 错误信息
3. 需求文档内容（脱敏后）