#!/bin/bash
# S-AES算法实现系统启动脚本

echo "===================================="
echo "     S-AES算法实现系统启动器"
echo "===================================="
echo

echo "正在启动S-AES算法系统..."
echo

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误：未找到Python环境"
        echo "请确保Python 3.7或更高版本已正确安装"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "使用Python命令: $PYTHON_CMD"
$PYTHON_CMD --version

# 启动程序
$PYTHON_CMD 启动程序.py

if [ $? -eq 0 ]; then
    echo
    echo "程序已正常退出"
else
    echo
    echo "程序执行出错，请检查错误信息"
fi

echo "按任意键继续..."
read -n 1 -s
