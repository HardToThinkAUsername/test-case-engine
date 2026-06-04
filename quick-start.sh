#!/bin/bash

# 测试用例生成系统 - 快速开始脚本

echo "=== 测试用例生成系统 - 快速开始 ==="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Claude Code
if ! command -v claude &> /dev/null; then
    echo "警告: 未找到Claude Code"
    echo "请访问 https://claude.ai/code 安装Claude Code"
    echo ""
fi

# 安装依赖
echo "正在安装依赖..."
pip install -e . -q

# 初始化项目
echo "正在初始化项目..."
test-case-engine init --project-name "demo"

# 显示状态
echo ""
echo "=== 项目状态 ==="
test-case-engine status

echo ""
echo "=== 快速开始完成 ==="
echo ""
echo "下一步："
echo "1. 在Claude Code中打开此目录"
echo "2. 告诉Claude：按照test-case-engine流程，帮我从需求文档生成测试用例"
echo "3. Claude会读取prompts/目录下的skill文件，按照流程执行"
echo ""
echo "或使用CLI命令："
echo "  test-case-engine model --document examples/online-shop-prd.md"
echo "  test-case-engine review"
echo "  test-case-engine outline"
echo "  test-case-engine generate"
echo "  test-case-engine export"