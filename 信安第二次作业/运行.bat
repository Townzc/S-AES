@echo off
chcp 65001 >nul
echo ====================================
echo      S-AES算法实现系统启动器
echo ====================================
echo.
echo 正在启动S-AES算法系统...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python环境
    echo 请确保Python 3.7或更高版本已正确安装
    pause
    exit /b 1
)

python 启动程序.py

if errorlevel 1 (
    echo.
    echo 程序执行出错，请检查错误信息
    pause
) else (
    echo.
    echo 程序已正常退出
)

pause
