"""
CBC模式实现
密码分组链(Cipher Block Chaining)工作模式
"""

import os
from s_aes import SAES

class CBCMode:
    def __init__(self):
        self.saes = SAES()
    
    def encrypt(self, plaintext, key, iv):
        """
        CBC模式加密
        每个分组与前一个密文分组异或后再加密
        """
        # 将明文转换为字节并进行PKCS7填充
        plaintext_bytes = plaintext.encode('utf-8')
        padded_plaintext = self.pkcs7_pad(plaintext_bytes, 2)  # 2字节分组
        
        # 分组处理
        blocks = []
        previous_block = iv
        blocks_info = "分组加密过程:\\n"
        
        for i in range(0, len(padded_plaintext), 2):
            # 获取当前分组（16位）
            if i + 1 < len(padded_plaintext):
                current_block = (padded_plaintext[i] << 8) | padded_plaintext[i + 1]
            else:
                current_block = padded_plaintext[i] << 8
            
            # 与前一个密文分组异或
            xor_block = current_block ^ previous_block
            
            # 加密
            cipher_block = self.saes.encrypt(xor_block, key)
            blocks.append(cipher_block)
            
            # 更新前一个密文分组
            previous_block = cipher_block
            
            # 记录详细信息
            blocks_info += f"分组 {i//2 + 1}:\\n"
            blocks_info += f"  明文: {current_block:016b} ({current_block:04X})\\n"
            blocks_info += f"  异或: {xor_block:016b} ({xor_block:04X})\\n"
            blocks_info += f"  密文: {cipher_block:016b} ({cipher_block:04X})\\n"
        
        # 转换为十六进制字符串
        ciphertext_hex = ''.join(f'{block:04X}' for block in blocks)
        
        return ciphertext_hex, blocks_info
    
    def decrypt(self, ciphertext_hex, key, iv):
        """
        CBC模式解密
        """
        # 解析十六进制密文
        if len(ciphertext_hex) % 4 != 0:
            raise ValueError("密文长度必须是4的倍数")
        
        cipher_blocks = []
        for i in range(0, len(ciphertext_hex), 4):
            block_hex = ciphertext_hex[i:i+4]
            cipher_blocks.append(int(block_hex, 16))
        
        # 解密各分组
        plaintext_blocks = []
        previous_block = iv
        blocks_info = "分组解密过程:\\n"
        
        for i, cipher_block in enumerate(cipher_blocks):
            # 解密当前分组
            decrypted_block = self.saes.decrypt(cipher_block, key)
            
            # 与前一个密文分组异或得到明文
            plain_block = decrypted_block ^ previous_block
            plaintext_blocks.append(plain_block)
            
            # 更新前一个密文分组
            previous_block = cipher_block
            
            # 记录详细信息
            blocks_info += f"分组 {i + 1}:\\n"
            blocks_info += f"  密文: {cipher_block:016b} ({cipher_block:04X})\\n"
            blocks_info += f"  解密: {decrypted_block:016b} ({decrypted_block:04X})\\n"
            blocks_info += f"  明文: {plain_block:016b} ({plain_block:04X})\\n"
        
        # 转换回字节串
        plaintext_bytes = []
        for block in plaintext_blocks:
            plaintext_bytes.append((block >> 8) & 0xFF)
            plaintext_bytes.append(block & 0xFF)
        
        # 去除填充
        unpadded_bytes = self.pkcs7_unpad(bytes(plaintext_bytes))
        
        # 转换为字符串
        try:
            plaintext = unpadded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # 如果无法解码，返回字节的十六进制表示
            plaintext = unpadded_bytes.hex()
        
        return plaintext, blocks_info
    
    def pkcs7_pad(self, data, block_size):
        """
        PKCS7填充
        """
        pad_len = block_size - (len(data) % block_size)
        if pad_len == 0:
            pad_len = block_size
        padding = bytes([pad_len] * pad_len)
        return data + padding
    
    def pkcs7_unpad(self, data):
        """
        PKCS7去填充
        """
        if len(data) == 0:
            raise ValueError("数据为空")
        
        pad_len = data[-1]
        if pad_len > len(data):
            raise ValueError("填充长度无效")
        
        # 验证填充
        for i in range(pad_len):
            if data[-(i+1)] != pad_len:
                raise ValueError("填充格式无效")
        
        return data[:-pad_len]
    
    def generate_iv(self):
        """
        生成随机初始向量
        """
        # 生成16位随机数
        random_bytes = os.urandom(2)
        return (random_bytes[0] << 8) | random_bytes[1]
    
    def demonstrate_tamper_effect(self, plaintext, key, iv):
        """
        演示密文篡改对解密结果的影响
        """
        # 正常加密
        ciphertext_hex, _ = self.encrypt(plaintext, key, iv)
        
        # 正常解密
        normal_decryption, _ = self.decrypt(ciphertext_hex, key, iv)
        
        result = f"=== CBC篡改效果演示 ===\\n"
        result += f"原始明文: {plaintext}\\n"
        result += f"正常密文: {ciphertext_hex}\\n"
        result += f"正常解密: {normal_decryption}\\n\\n"
        
        # 篡改第一个分组
        if len(ciphertext_hex) >= 4:
            tampered_hex = self.tamper_hex_string(ciphertext_hex, 0, 1)
            result += f"篡改密文: {tampered_hex}\\n"
            
            try:
                tampered_decryption, _ = self.decrypt(tampered_hex, key, iv)
                result += f"篡改解密: {tampered_decryption}\\n"
            except Exception as e:
                result += f"篡改解密失败: {str(e)}\\n"
            
            result += "\\n观察：CBC模式中单个分组的篡改会影响当前和后续分组的解密结果\\n"
        
        # 篡改中间分组（如果有的话）
        if len(ciphertext_hex) >= 8:
            tampered_hex2 = self.tamper_hex_string(ciphertext_hex, 4, 1)
            result += f"\\n篡改中间分组密文: {tampered_hex2}\\n"
            
            try:
                tampered_decryption2, _ = self.decrypt(tampered_hex2, key, iv)
                result += f"篡改解密结果: {tampered_decryption2}\\n"
            except Exception as e:
                result += f"篡改解密失败: {str(e)}\\n"
        
        return result
    
    def tamper_hex_string(self, hex_string, position, byte_offset):
        """
        篡改十六进制字符串中的指定位置
        """
        if position + 1 < len(hex_string):
            # 获取要篡改的字符
            char = hex_string[position + byte_offset]
            # 简单地改变一个比特
            if char == '0':
                new_char = '1'
            elif char.isdigit():
                new_char = str((int(char) + 1) % 10)
            else:
                new_char = 'A' if char.lower() == 'f' else chr(ord(char) + 1)
            
            # 替换字符
            return hex_string[:position + byte_offset] + new_char + hex_string[position + byte_offset + 1:]
        
        return hex_string

def test_cbc_mode():
    """
    测试CBC模式
    """
    cbc = CBCMode()
    
    # 测试参数
    plaintext = "Hello, CBC mode! This is a test message."
    key = 0b1010011100111011  # 16位密钥
    iv = 0b1111000011110000   # 16位初始向量
    
    print("=== CBC模式测试 ===")
    print(f"明文: {plaintext}")
    print(f"密钥: {key:016b} ({key:04X})")
    print(f"初始向量: {iv:016b} ({iv:04X})")
    print()
    
    # 加密
    print("--- 加密过程 ---")
    ciphertext_hex, encrypt_info = cbc.encrypt(plaintext, key, iv)
    print(encrypt_info)
    print(f"密文(hex): {ciphertext_hex}")
    print()
    
    # 解密
    print("--- 解密过程 ---")
    decrypted_text, decrypt_info = cbc.decrypt(ciphertext_hex, key, iv)
    print(decrypt_info)
    print(f"解密结果: {decrypted_text}")
    print()
    
    # 验证
    if plaintext == decrypted_text:
        print("✓ CBC模式测试通过！")
    else:
        print("✗ CBC模式测试失败！")
        print(f"期望: {plaintext}")
        print(f"实际: {decrypted_text}")
    print()
    
    # 篡改测试
    print("--- 篡改效果测试 ---")
    tamper_result = cbc.demonstrate_tamper_effect(
        "Short test message", key, iv
    )
    print(tamper_result)

if __name__ == "__main__":
    test_cbc_mode()
