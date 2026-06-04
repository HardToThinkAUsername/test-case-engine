# 测试用例生成系统

**一句话**：上传需求文档，AI帮你自动生成测试用例。

## 它能做什么

- 你给它一份需求文档
- 它自动分析需求，生成98个测试用例
- 输出Excel文件，直接可用

## 怎么用

### 第1步：下载代码

```bash
git clone https://github.com/HardToThinkAUsername/test-case-engine.git
```

### 第2步：准备你的需求文档

支持的格式：
- `.md` 或 `.txt` → 直接用
- `.docx` → AI会自动帮你转换（需要安装python-docx库）
- `.pdf` → AI会自动帮你提取文本（需要安装pdfplumber库）

**或者最简单的方式**：直接把需求文档内容复制粘贴到对话中

### 第3步：告诉AI

打开你的AI编程助手（Claude Code / OpenCode / 其他），输入：

```
我有一份需求文档，路径是：D:\我的需求文档.docx
请帮我按照 test-case-engine/prompts/extraction-guide.md 的流程，
自动生成测试用例。
```

### 第4步：和AI对话

AI会引导你完成整个流程：

1. **AI分析需求** → 生成业务树
2. **你确认或调整** → "把注册拆成手机号和邮箱"
3. **AI评审需求** → 发现问题
4. **你确认或修改** → "密码锁定改为1小时"
5. **AI生成大纲** → 你确认
6. **AI生成用例** → 你确认
7. **AI导出Excel** → 完成

整个过程是**对话式的**，你可以随时调整。

## 看看效果

参考 `examples/output/test_cases.xlsx`，这就是AI生成的测试用例示例。

## 常见问题

**Q: 我没有AI编程助手怎么办？**
A: 需要安装一个。推荐使用 Claude Code（https://claude.ai/download）。

**Q: 我的需求文档是Word格式怎么办？**
A: AI可以自动处理.docx格式。直接告诉AI文件路径即可，AI会自动转换。或者直接复制粘贴内容到对话中。

**Q: 生成的测试用例在哪里？**
A: 默认保存在 `.test-case/test_cases.xlsx`。

**Q: 我能调整生成的用例吗？**
A: 可以。直接告诉AI："把用例XXX的步骤修改一下"，AI会帮你更新。

## 更多信息

- 详细的使用说明请查看 `docs/` 目录
- 示例需求文档：`examples/online-shop-prd.md`
- 示例输出：`examples/output/`