#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S-AES算法系统启动程序
双击此文件可直接启动图形界面

使用方法：
1. 双击运行此文件
2. 或在命令行执行：python 启动程序.py
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_environment():
    """检查运行环境"""
    try:
        # 检查Python版本
        if sys.version_info < (3, 7):
            messagebox.showerror(
                "版本错误",
                f"需要Python 3.7或更高版本\n当前版本: {sys.version}"
            )
            return False

        # 检查必要文件
        required_files = [
            "s_aes.py",
            "gui.py", 
            "multi_encrypt.py",
            "cbc_mode.py"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            messagebox.showerror(
                "文件缺失",
                f"以下必要文件缺失:\n" + "\n".join(missing_files)
            )
            return False
            
        return True
        
    except Exception as e:
        messagebox.showerror("环境检查失败", f"错误: {str(e)}")
        return False

def main():
    """主程序入口"""
    try:
        # 创建根窗口（用于显示错误消息）
        root = tk.Tk()
        root.withdraw()  # 隐藏根窗口
        
        # 检查环境
        if not check_environment():
            root.destroy()
            return
        
        root.destroy()
        
        # 导入并启动GUI
        from gui import SAESGui
        
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标和标题
        root.title("S-AES算法实现系统")
        
        # 创建应用程序
        app = SAESGui(root)
        
        print("S-AES算法系统已启动")
        print("如需退出，请关闭图形界面窗口")
        
        # 启动GUI主循环
        root.mainloop()
        
    except ImportError as e:
        messagebox.showerror(
            "导入错误", 
            f"无法导入必要模块:\n{str(e)}\n\n请确保所有文件都在同一目录下"
        )
    except Exception as e:
        messagebox.showerror(
            "启动失败",
            f"程序启动失败:\n{str(e)}\n\n请检查Python环境和文件完整性"
        )

if __name__ == "__main__":
    main()
