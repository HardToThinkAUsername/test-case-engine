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
- `.docx` → 需要先另存为 `.txt` 格式
- `.pdf` → 需要复制粘贴内容到 `.txt` 文件

### 第3步：告诉AI

打开你的AI编程助手（Claude Code / OpenCode / 其他），输入：

```
我有一份需求文档，路径是：D:\我的需求文档.txt
请帮我按照 test-case-engine/prompts/extraction-guide.md 的流程，
自动生成测试用例。
```

### 第4步：等待结果

AI会自动：
1. 分析需求文档
2. 识别所有业务功能
3. 生成测试用例
4. 输出Excel文件

## 看看效果

参考 `examples/output/test_cases.xlsx`，这就是AI生成的测试用例示例。

## 常见问题

**Q: 我没有AI编程助手怎么办？**
A: 需要安装一个。推荐使用 Claude Code（https://claude.ai/download）。

**Q: 我的需求文档是Word格式怎么办？**
A: 用Word打开，另存为.txt格式，再提供给AI。

**Q: 生成的测试用例在哪里？**
A: 默认保存在 `.test-case/test_cases.xlsx`。

**Q: 我能调整生成的用例吗？**
A: 可以。直接告诉AI："把用例XXX的步骤修改一下"，AI会帮你更新。

## 更多信息

- 详细的使用说明请查看 `docs/` 目录
- 示例需求文档：`examples/online-shop-prd.md`
- 示例输出：`examples/output/`