"""
S-AES算法GUI界面
提供用户友好的图形界面，支持所有5个关卡的功能测试

作者：吴彦组（Zhice Tang，Xiaohao Zhou）
日期：2025年10月
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import filedialog
import threading
import time
from s_aes import SAES
from multi_encrypt import MultiEncrypt
from cbc_mode import CBCMode

class SAESGui:
    def __init__(self, root):
        self.root = root
        self.root.title("S-AES算法实现 - 信息安全导论作业")
        self.root.geometry("800x600")
        
        # 初始化算法实例
        self.saes = SAES()
        self.multi_encrypt = MultiEncrypt()
        self.cbc_mode = CBCMode()
        
        # 创建标签页
        self.create_notebook()
        
    def create_notebook(self):
        """创建多标签页界面"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 第1关：基本测试
        self.create_basic_tab()
        
        # 第2关：交叉测试
        self.create_cross_test_tab()
        
        # 第3关：ASCII扩展
        self.create_ascii_tab()
        
        # 第4关：多重加密
        self.create_multi_encrypt_tab()
        
        # 第5关：CBC模式
        self.create_cbc_tab()
        
        # 关于页面
        self.create_about_tab()
    
    def create_basic_tab(self):
        """第1关：基本测试标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="第1关：基本测试")
        
        # 主框架
        main_frame = ttk.LabelFrame(frame, text="S-AES基本加解密", padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 明文输入
        ttk.Label(input_frame, text="明文 (16位二进制或4位十六进制):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.plaintext_entry = ttk.Entry(input_frame, width=30)
        self.plaintext_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.plaintext_entry.insert(0, "0110111101101011")
        
        # 密钥输入
        ttk.Label(input_frame, text="密钥 (16位二进制或4位十六进制):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.key_entry = ttk.Entry(input_frame, width=30)
        self.key_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.key_entry.insert(0, "1010011100111011")
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(button_frame, text="加密", command=self.basic_encrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="解密", command=self.basic_decrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清除", command=self.clear_basic).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.basic_result = scrolledtext.ScrolledText(result_frame, height=15, wrap=tk.WORD)
        self.basic_result.pack(fill=tk.BOTH, expand=True)
    
    def create_cross_test_tab(self):
        """第2关：交叉测试标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="第2关：交叉测试")
        
        main_frame = ttk.LabelFrame(frame, text="交叉测试验证", padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 测试说明
        desc_text = """交叉测试说明：
1. 使用标准S-AES算法确保不同实现的兼容性
2. 相同的明文和密钥应产生相同的密文
3. 验证算法的标准化实现"""
        
        ttk.Label(main_frame, text=desc_text, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 20))
        
        # 标准测试用例
        test_frame = ttk.LabelFrame(main_frame, text="标准测试用例", padding=10)
        test_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加标准测试按钮
        ttk.Button(test_frame, text="运行标准测试用例", command=self.run_standard_tests).pack(pady=10)
        
        # 结果显示
        self.cross_test_result = scrolledtext.ScrolledText(test_frame, height=15, wrap=tk.WORD)
        self.cross_test_result.pack(fill=tk.BOTH, expand=True)
    
    def create_ascii_tab(self):
        """第3关：ASCII扩展标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="第3关：ASCII扩展")
        
        main_frame = ttk.LabelFrame(frame, text="ASCII字符串加解密", padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # ASCII文本输入
        ttk.Label(input_frame, text="ASCII文本:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ascii_text_entry = ttk.Entry(input_frame, width=40)
        self.ascii_text_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.ascii_text_entry.insert(0, "Hello!")
        
        # 密钥输入
        ttk.Label(input_frame, text="密钥 (16位):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ascii_key_entry = ttk.Entry(input_frame, width=40)
        self.ascii_key_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.ascii_key_entry.insert(0, "1010011100111011")
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(button_frame, text="加密ASCII", command=self.ascii_encrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="解密ASCII", command=self.ascii_decrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清除", command=self.clear_ascii).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ascii_result = scrolledtext.ScrolledText(result_frame, height=15, wrap=tk.WORD)
        self.ascii_result.pack(fill=tk.BOTH, expand=True)
    
    def create_multi_encrypt_tab(self):
        """第4关：多重加密标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="第4关：多重加密")
        
        main_frame = ttk.LabelFrame(frame, text="多重加密模式", padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 模式选择
        mode_frame = ttk.LabelFrame(main_frame, text="加密模式", padding=10)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.multi_mode = tk.StringVar(value="double")
        ttk.Radiobutton(mode_frame, text="双重加密 (32位密钥)", variable=self.multi_mode, value="double").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="三重加密 (32位密钥)", variable=self.multi_mode, value="triple_2key").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="三重加密 (48位密钥)", variable=self.multi_mode, value="triple_3key").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="中间相遇攻击", variable=self.multi_mode, value="meet_middle").pack(anchor=tk.W)
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(input_frame, text="明文 (16位):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.multi_plain_entry = ttk.Entry(input_frame, width=40)
        self.multi_plain_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.multi_plain_entry.insert(0, "0110111101101011")
        
        ttk.Label(input_frame, text="密钥 (32或48位):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.multi_key_entry = ttk.Entry(input_frame, width=40)
        self.multi_key_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.multi_key_entry.insert(0, "10100111001110111010011100111011")
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(button_frame, text="多重加密", command=self.multi_encrypt_action).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="多重解密", command=self.multi_decrypt_action).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="中间相遇攻击", command=self.meet_in_middle_attack).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清除", command=self.clear_multi).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.multi_result = scrolledtext.ScrolledText(result_frame, height=12, wrap=tk.WORD)
        self.multi_result.pack(fill=tk.BOTH, expand=True)
    
    def create_cbc_tab(self):
        """第5关：CBC模式标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="第5关：CBC模式")
        
        main_frame = ttk.LabelFrame(frame, text="密码分组链(CBC)模式", padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(input_frame, text="明文:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cbc_plain_entry = ttk.Entry(input_frame, width=50)
        self.cbc_plain_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.cbc_plain_entry.insert(0, "This is a longer message for CBC mode testing!")
        
        ttk.Label(input_frame, text="密钥 (16位):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cbc_key_entry = ttk.Entry(input_frame, width=50)
        self.cbc_key_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.cbc_key_entry.insert(0, "1010011100111011")
        
        ttk.Label(input_frame, text="初始向量 (16位):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cbc_iv_entry = ttk.Entry(input_frame, width=50)
        self.cbc_iv_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        self.cbc_iv_entry.insert(0, "1111000011110000")
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(button_frame, text="CBC加密", command=self.cbc_encrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="CBC解密", command=self.cbc_decrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="篡改测试", command=self.cbc_tamper_test).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清除", command=self.clear_cbc).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.cbc_result = scrolledtext.ScrolledText(result_frame, height=12, wrap=tk.WORD)
        self.cbc_result.pack(fill=tk.BOTH, expand=True)
    
    def create_about_tab(self):
        """关于页面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="关于")
        
        about_text = """
S-AES算法实现
信息安全导论课程第二次作业

项目特点：
• 完整实现S-AES算法的5个关卡功能
• 基本测试：16位数据和密钥的加解密
• 交叉测试：确保算法标准化兼容性
• ASCII扩展：支持字符串的分组加解密
• 多重加密：双重、三重加密及中间相遇攻击
• CBC模式：密码分组链工作模式

技术实现：
• Python 3.x + Tkinter GUI
• 模块化设计，易于扩展和测试
• 完整的S盒、轮密钥生成、列混淆等核心组件
• 符合密码学课程标准的算法实现

作者：吴彦组（Zhice Tang，Xiaohao Zhou）
版本：v1.0 (2025年10月)
        """
        
        text_widget = tk.Text(frame, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)
    
    # 第1关：基本测试功能
    def basic_encrypt(self):
        """基本加密功能"""
        try:
            plaintext_str = self.plaintext_entry.get().strip()
            key_str = self.key_entry.get().strip()
            
            # 解析输入
            plaintext = self.parse_input(plaintext_str)
            key = self.parse_input(key_str)
            
            # 加密
            ciphertext = self.saes.encrypt(plaintext, key)
            
            # 显示结果
            result = f"=== 加密结果 ===\\n"
            result += f"明文: {plaintext:016b} ({plaintext:04X})\\n"
            result += f"密钥: {key:016b} ({key:04X})\\n"
            result += f"密文: {ciphertext:016b} ({ciphertext:04X})\\n\\n"
            
            self.basic_result.insert(tk.END, result)
            self.basic_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}")
    
    def basic_decrypt(self):
        """基本解密功能"""
        try:
            ciphertext_str = self.plaintext_entry.get().strip()  # 用明文输入框作为密文输入
            key_str = self.key_entry.get().strip()
            
            # 解析输入
            ciphertext = self.parse_input(ciphertext_str)
            key = self.parse_input(key_str)
            
            # 解密
            plaintext = self.saes.decrypt(ciphertext, key)
            
            # 显示结果
            result = f"=== 解密结果 ===\\n"
            result += f"密文: {ciphertext:016b} ({ciphertext:04X})\\n"
            result += f"密钥: {key:016b} ({key:04X})\\n"
            result += f"明文: {plaintext:016b} ({plaintext:04X})\\n\\n"
            
            self.basic_result.insert(tk.END, result)
            self.basic_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"解密失败: {str(e)}")
    
    def clear_basic(self):
        """清除基本测试结果"""
        self.basic_result.delete(1.0, tk.END)
    
    # 第2关：交叉测试功能
    def run_standard_tests(self):
        """运行标准测试用例以验证交叉兼容性"""
        self.cross_test_result.delete(1.0, tk.END)
        
        # 标准测试用例
        test_cases = [
            {"plain": 0b0110111101101011, "key": 0b1010011100111011, "expected": None},
            {"plain": 0b0000000000000000, "key": 0b0000000000000000, "expected": None},
            {"plain": 0b1111111111111111, "key": 0b1111111111111111, "expected": None},
            {"plain": 0b1010101010101010, "key": 0b0101010101010101, "expected": None},
        ]
        
        result = "=== S-AES标准交叉测试 ===\\n\\n"
        
        for i, test in enumerate(test_cases, 1):
            plain = test["plain"]
            key = test["key"]
            
            # 加密
            cipher = self.saes.encrypt(plain, key)
            
            # 解密验证
            decrypted = self.saes.decrypt(cipher, key)
            
            # 记录结果
            result += f"测试用例 {i}:\\n"
            result += f"  明文: {plain:016b} ({plain:04X})\\n"
            result += f"  密钥: {key:016b} ({key:04X})\\n"
            result += f"  密文: {cipher:016b} ({cipher:04X})\\n"
            result += f"  解密: {decrypted:016b} ({decrypted:04X})\\n"
            result += f"  状态: {'✓ 通过' if plain == decrypted else '✗ 失败'}\\n\\n"
        
        result += "这些测试用例可用于与其他实现进行交叉验证\\n"
        result += "确保不同平台和实现的兼容性\\n"
        
        self.cross_test_result.insert(tk.END, result)
    
    # 第3关：ASCII扩展功能
    def ascii_encrypt(self):
        """ASCII字符串加密"""
        try:
            text = self.ascii_text_entry.get()
            key_str = self.ascii_key_entry.get().strip()
            key = self.parse_input(key_str)
            
            # 分组加密
            result = f"=== ASCII加密结果 ===\\n"
            result += f"原文: {text}\\n"
            result += f"密钥: {key:016b} ({key:04X})\\n\\n"
            
            encrypted_blocks = []
            for i in range(0, len(text), 2):
                block = text[i:i+2]
                if len(block) == 1:
                    block += '\\0'  # 填充
                
                # 转换为16位整数
                plain_int = (ord(block[0]) << 8) | ord(block[1])
                
                # 加密
                cipher_int = self.saes.encrypt(plain_int, key)
                encrypted_blocks.append(cipher_int)
                
                result += f"分组 {i//2 + 1}: '{block}' -> {plain_int:016b} -> {cipher_int:016b} ({cipher_int:04X})\\n"
            
            # 转换为字符串（可能包含不可打印字符）
            encrypted_text = ""
            for cipher_int in encrypted_blocks:
                encrypted_text += chr((cipher_int >> 8) & 0xFF) + chr(cipher_int & 0xFF)
            
            result += f"\\n加密后字符串: {repr(encrypted_text)}\\n"
            result += f"十六进制表示: {' '.join(f'{b:04X}' for b in encrypted_blocks)}\\n\\n"
            
            self.ascii_result.insert(tk.END, result)
            self.ascii_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"ASCII加密失败: {str(e)}")
    
    def ascii_decrypt(self):
        """ASCII字符串解密"""
        try:
            # 这里简化处理，用户需要输入十六进制密文
            cipher_text = self.ascii_text_entry.get().strip()
            key_str = self.ascii_key_entry.get().strip()
            key = self.parse_input(key_str)
            
            result = f"=== ASCII解密结果 ===\\n"
            result += f"输入: {cipher_text}\\n"
            result += f"密钥: {key:016b} ({key:04X})\\n\\n"
            
            # 解析十六进制密文
            if len(cipher_text) % 4 == 0:
                # 十六进制格式
                cipher_blocks = []
                for i in range(0, len(cipher_text), 4):
                    block_hex = cipher_text[i:i+4]
                    cipher_blocks.append(int(block_hex, 16))
            else:
                # 字符格式
                cipher_blocks = []
                for i in range(0, len(cipher_text), 2):
                    block = cipher_text[i:i+2]
                    if len(block) == 2:
                        cipher_int = (ord(block[0]) << 8) | ord(block[1])
                        cipher_blocks.append(cipher_int)
            
            # 解密各分组
            decrypted_text = ""
            for i, cipher_int in enumerate(cipher_blocks):
                plain_int = self.saes.decrypt(cipher_int, key)
                char1 = chr((plain_int >> 8) & 0xFF)
                char2 = chr(plain_int & 0xFF)
                decrypted_text += char1 + (char2 if char2 != '\\0' else '')
                
                result += f"分组 {i + 1}: {cipher_int:016b} -> {plain_int:016b} -> '{char1}{char2}'\\n"
            
            result += f"\\n解密结果: {decrypted_text}\\n\\n"
            
            self.ascii_result.insert(tk.END, result)
            self.ascii_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"ASCII解密失败: {str(e)}")
    
    def clear_ascii(self):
        """清除ASCII测试结果"""
        self.ascii_result.delete(1.0, tk.END)
    
    # 第4关：多重加密功能
    def multi_encrypt_action(self):
        """多重加密"""
        try:
            plain_str = self.multi_plain_entry.get().strip()
            key_str = self.multi_key_entry.get().strip()
            mode = self.multi_mode.get()
            
            plaintext = self.parse_input(plain_str)
            
            result = f"=== 多重加密结果 ===\\n"
            result += f"模式: {mode}\\n"
            result += f"明文: {plaintext:016b} ({plaintext:04X})\\n"
            result += f"密钥: {key_str}\\n\\n"
            
            if mode == "double":
                # 双重加密
                key1 = int(key_str[:16], 2) if len(key_str) == 32 else int(key_str[:8], 16)
                key2 = int(key_str[16:], 2) if len(key_str) == 32 else int(key_str[8:], 16)
                ciphertext = self.multi_encrypt.double_encrypt(plaintext, key1, key2)
                result += f"双重加密结果: {ciphertext:016b} ({ciphertext:04X})\\n"
                
            elif mode == "triple_2key":
                # 三重加密（2密钥）
                key1 = int(key_str[:16], 2) if len(key_str) == 32 else int(key_str[:8], 16)
                key2 = int(key_str[16:], 2) if len(key_str) == 32 else int(key_str[8:], 16)
                ciphertext = self.multi_encrypt.triple_encrypt_2key(plaintext, key1, key2)
                result += f"三重加密结果(2密钥): {ciphertext:016b} ({ciphertext:04X})\\n"
                
            elif mode == "triple_3key":
                # 三重加密（3密钥）
                if len(key_str) != 48:
                    raise ValueError("三重加密(3密钥)需要48位密钥")
                key1 = int(key_str[:16], 2)
                key2 = int(key_str[16:32], 2)
                key3 = int(key_str[32:], 2)
                ciphertext = self.multi_encrypt.triple_encrypt_3key(plaintext, key1, key2, key3)
                result += f"三重加密结果(3密钥): {ciphertext:016b} ({ciphertext:04X})\\n"
            
            result += "\\n"
            self.multi_result.insert(tk.END, result)
            self.multi_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"多重加密失败: {str(e)}")
    
    def multi_decrypt_action(self):
        """多重解密"""
        try:
            cipher_str = self.multi_plain_entry.get().strip()
            key_str = self.multi_key_entry.get().strip()
            mode = self.multi_mode.get()
            
            ciphertext = self.parse_input(cipher_str)
            
            result = f"=== 多重解密结果 ===\\n"
            result += f"模式: {mode}\\n"
            result += f"密文: {ciphertext:016b} ({ciphertext:04X})\\n"
            result += f"密钥: {key_str}\\n\\n"
            
            if mode == "double":
                # 双重解密
                key1 = int(key_str[:16], 2) if len(key_str) == 32 else int(key_str[:8], 16)
                key2 = int(key_str[16:], 2) if len(key_str) == 32 else int(key_str[8:], 16)
                plaintext = self.multi_encrypt.double_decrypt(ciphertext, key1, key2)
                result += f"双重解密结果: {plaintext:016b} ({plaintext:04X})\\n"
                
            elif mode == "triple_2key":
                # 三重解密（2密钥）
                key1 = int(key_str[:16], 2) if len(key_str) == 32 else int(key_str[:8], 16)
                key2 = int(key_str[16:], 2) if len(key_str) == 32 else int(key_str[8:], 16)
                plaintext = self.multi_encrypt.triple_decrypt_2key(ciphertext, key1, key2)
                result += f"三重解密结果(2密钥): {plaintext:016b} ({plaintext:04X})\\n"
                
            elif mode == "triple_3key":
                # 三重解密（3密钥）
                if len(key_str) != 48:
                    raise ValueError("三重解密(3密钥)需要48位密钥")
                key1 = int(key_str[:16], 2)
                key2 = int(key_str[16:32], 2)
                key3 = int(key_str[32:], 2)
                plaintext = self.multi_encrypt.triple_decrypt_3key(ciphertext, key1, key2, key3)
                result += f"三重解密结果(3密钥): {plaintext:016b} ({plaintext:04X})\\n"
            
            result += "\\n"
            self.multi_result.insert(tk.END, result)
            self.multi_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"多重解密失败: {str(e)}")
    
    def meet_in_middle_attack(self):
        """中间相遇攻击"""
        try:
            # 使用固定的明密文对进行演示
            self.multi_result.insert(tk.END, "=== 中间相遇攻击演示 ===\\n")
            self.multi_result.insert(tk.END, "正在执行攻击，请稍候...\\n\\n")
            self.multi_result.see(tk.END)
            
            # 在后台线程中执行攻击以避免界面冻结
            def attack_thread():
                try:
                    result = self.multi_encrypt.meet_in_middle_attack()
                    self.root.after(0, lambda: self.display_attack_result(result))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"中间相遇攻击失败: {str(e)}"))
            
            threading.Thread(target=attack_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动中间相遇攻击失败: {str(e)}")
    
    def display_attack_result(self, result):
        """显示攻击结果"""
        self.multi_result.insert(tk.END, result)
        self.multi_result.see(tk.END)
    
    def clear_multi(self):
        """清除多重加密结果"""
        self.multi_result.delete(1.0, tk.END)
    
    # 第5关：CBC模式功能
    def cbc_encrypt(self):
        """CBC模式加密"""
        try:
            plaintext = self.cbc_plain_entry.get()
            key_str = self.cbc_key_entry.get().strip()
            iv_str = self.cbc_iv_entry.get().strip()
            
            key = self.parse_input(key_str)
            iv = self.parse_input(iv_str)
            
            # CBC加密
            ciphertext, blocks_info = self.cbc_mode.encrypt(plaintext, key, iv)
            
            result = f"=== CBC加密结果 ===\\n"
            result += f"明文: {plaintext}\\n"
            result += f"密钥: {key:016b} ({key:04X})\\n"
            result += f"初始向量: {iv:016b} ({iv:04X})\\n\\n"
            result += f"分组详情:\\n{blocks_info}\\n"
            result += f"密文(hex): {ciphertext}\\n\\n"
            
            self.cbc_result.insert(tk.END, result)
            self.cbc_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"CBC加密失败: {str(e)}")
    
    def cbc_decrypt(self):
        """CBC模式解密"""
        try:
            ciphertext_hex = self.cbc_plain_entry.get().strip()  # 使用明文框输入密文
            key_str = self.cbc_key_entry.get().strip()
            iv_str = self.cbc_iv_entry.get().strip()
            
            key = self.parse_input(key_str)
            iv = self.parse_input(iv_str)
            
            # CBC解密
            plaintext, blocks_info = self.cbc_mode.decrypt(ciphertext_hex, key, iv)
            
            result = f"=== CBC解密结果 ===\\n"
            result += f"密文(hex): {ciphertext_hex}\\n"
            result += f"密钥: {key:016b} ({key:04X})\\n"
            result += f"初始向量: {iv:016b} ({iv:04X})\\n\\n"
            result += f"分组详情:\\n{blocks_info}\\n"
            result += f"明文: {plaintext}\\n\\n"
            
            self.cbc_result.insert(tk.END, result)
            self.cbc_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"CBC解密失败: {str(e)}")
    
    def cbc_tamper_test(self):
        """CBC篡改测试"""
        try:
            plaintext = "Hello World! This is CBC test."
            key_str = self.cbc_key_entry.get().strip()
            iv_str = self.cbc_iv_entry.get().strip()
            
            key = self.parse_input(key_str)
            iv = self.parse_input(iv_str)
            
            result = f"=== CBC篡改测试 ===\\n"
            result += f"原始明文: {plaintext}\\n"
            
            # 正常加密
            ciphertext, _ = self.cbc_mode.encrypt(plaintext, key, iv)
            result += f"正常密文: {ciphertext}\\n\\n"
            
            # 正常解密
            decrypted, _ = self.cbc_mode.decrypt(ciphertext, key, iv)
            result += f"正常解密: {decrypted}\\n\\n"
            
            # 篡改密文（修改第一个分组的第一个字节）
            tampered_ciphertext = self.tamper_ciphertext(ciphertext)
            result += f"篡改密文: {tampered_ciphertext}\\n\\n"
            
            # 解密篡改后的密文
            tampered_decrypted, _ = self.cbc_mode.decrypt(tampered_ciphertext, key, iv)
            result += f"篡改解密: {tampered_decrypted}\\n\\n"
            
            result += "观察结果：CBC模式中单个分组的篡改会影响当前和下一个分组的解密结果\\n\\n"
            
            self.cbc_result.insert(tk.END, result)
            self.cbc_result.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"CBC篡改测试失败: {str(e)}")
    
    def tamper_ciphertext(self, ciphertext_hex):
        """篡改密文的第一个字节"""
        if len(ciphertext_hex) >= 2:
            # 修改第一个字节
            first_byte = int(ciphertext_hex[:2], 16)
            tampered_byte = first_byte ^ 0x01  # 翻转最低位
            return f"{tampered_byte:02X}" + ciphertext_hex[2:]
        return ciphertext_hex
    
    def clear_cbc(self):
        """清除CBC测试结果"""
        self.cbc_result.delete(1.0, tk.END)
    
    # 工具函数
    def parse_input(self, input_str):
        """解析输入字符串为整数（支持二进制和十六进制）"""
        input_str = input_str.replace(" ", "")
        
        if len(input_str) == 16 and all(c in "01" for c in input_str):
            # 16位二进制
            return int(input_str, 2)
        elif len(input_str) == 4 and all(c in "0123456789ABCDEFabcdef" for c in input_str):
            # 4位十六进制
            return int(input_str, 16)
        elif len(input_str) == 32 and all(c in "01" for c in input_str):
            # 32位二进制
            return int(input_str, 2)
        elif len(input_str) == 8 and all(c in "0123456789ABCDEFabcdef" for c in input_str):
            # 8位十六进制
            return int(input_str, 16)
        else:
            try:
                # 尝试直接解析
                if 'x' in input_str.lower():
                    return int(input_str, 16)
                elif len(input_str) > 16:
                    return int(input_str, 2)
                else:
                    return int(input_str, 16)
            except ValueError:
                raise ValueError(f"无法解析输入: {input_str}")

def main():
    root = tk.Tk()
    app = SAESGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
