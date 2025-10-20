"""
多重加密模块
实现双重加密、三重加密和中间相遇攻击

作者：吴彦组（Zhice Tang，Xiaohao Zhou）
日期：2025年10月
"""

import time
from s_aes import SAES

class MultiEncrypt:
    def __init__(self):
        self.saes = SAES()
    
    def double_encrypt(self, plaintext, key1, key2):
        """
        双重加密：C = E_K2(E_K1(P))
        """
        # 第一次加密
        intermediate = self.saes.encrypt(plaintext, key1)
        # 第二次加密
        ciphertext = self.saes.encrypt(intermediate, key2)
        return ciphertext
    
    def double_decrypt(self, ciphertext, key1, key2):
        """
        双重解密：P = D_K1(D_K2(C))
        """
        # 第一次解密
        intermediate = self.saes.decrypt(ciphertext, key2)
        # 第二次解密
        plaintext = self.saes.decrypt(intermediate, key1)
        return plaintext
    
    def triple_encrypt_2key(self, plaintext, key1, key2):
        """
        三重加密（2密钥）：C = E_K1(D_K2(E_K1(P)))
        使用EDE模式（加密-解密-加密）
        """
        # 第一次加密
        temp1 = self.saes.encrypt(plaintext, key1)
        # 解密
        temp2 = self.saes.decrypt(temp1, key2)
        # 第二次加密
        ciphertext = self.saes.encrypt(temp2, key1)
        return ciphertext
    
    def triple_decrypt_2key(self, ciphertext, key1, key2):
        """
        三重解密（2密钥）：P = D_K1(E_K2(D_K1(C)))
        """
        # 第一次解密
        temp1 = self.saes.decrypt(ciphertext, key1)
        # 加密
        temp2 = self.saes.encrypt(temp1, key2)
        # 第二次解密
        plaintext = self.saes.decrypt(temp2, key1)
        return plaintext
    
    def triple_encrypt_3key(self, plaintext, key1, key2, key3):
        """
        三重加密（3密钥）：C = E_K3(E_K2(E_K1(P)))
        """
        # 三次连续加密
        temp1 = self.saes.encrypt(plaintext, key1)
        temp2 = self.saes.encrypt(temp1, key2)
        ciphertext = self.saes.encrypt(temp2, key3)
        return ciphertext
    
    def triple_decrypt_3key(self, ciphertext, key1, key2, key3):
        """
        三重解密（3密钥）：P = D_K1(D_K2(D_K3(C)))
        """
        # 三次连续解密（逆序）
        temp1 = self.saes.decrypt(ciphertext, key3)
        temp2 = self.saes.decrypt(temp1, key2)
        plaintext = self.saes.decrypt(temp2, key1)
        return plaintext
    
    def meet_in_middle_attack(self, known_pairs=None):
        """
        中间相遇攻击
        假设已知明密文对，尝试找到双重加密的密钥
        """
        # 如果没有提供已知对，使用默认测试用例
        if known_pairs is None:
            # 生成一个已知的明密文对用于演示
            test_key1 = 0b1010011100111011  # K1
            test_key2 = 0b1100001111000011  # K2
            test_plaintext = 0b0110111101101011
            test_ciphertext = self.double_encrypt(test_plaintext, test_key1, test_key2)
            known_pairs = [(test_plaintext, test_ciphertext)]
            
            result = f"生成测试用例:\\n"
            result += f"真实密钥K1: {test_key1:016b} ({test_key1:04X})\\n"
            result += f"真实密钥K2: {test_key2:016b} ({test_key2:04X})\\n"
            result += f"明文: {test_plaintext:016b} ({test_plaintext:04X})\\n"
            result += f"密文: {test_ciphertext:016b} ({test_ciphertext:04X})\\n\\n"
        else:
            result = ""
        
        result += "开始中间相遇攻击...\\n"
        start_time = time.time()
        
        # 第一阶段：计算所有可能的E_K1(P)
        plaintext, ciphertext = known_pairs[0]
        forward_table = {}
        
        result += "第一阶段：计算 E_K1(P) for all K1...\\n"
        
        # 遍历所有可能的K1（16位密钥空间较小，可以暴力破解）
        for k1 in range(0x1000, 0x2000):  # 限制搜索范围以加快演示
            intermediate = self.saes.encrypt(plaintext, k1)
            forward_table[intermediate] = k1
        
        result += f"构建前向表，包含 {len(forward_table)} 个条目\\n"
        
        # 第二阶段：计算D_K2(C)并查找匹配
        result += "第二阶段：计算 D_K2(C) 并查找匹配...\\n"
        
        found_keys = []
        
        for k2 in range(0x1000, 0x2000):  # 限制搜索范围
            intermediate = self.saes.decrypt(ciphertext, k2)
            if intermediate in forward_table:
                k1 = forward_table[intermediate]
                found_keys.append((k1, k2))
                
                # 验证找到的密钥对
                test_cipher = self.double_encrypt(plaintext, k1, k2)
                if test_cipher == ciphertext:
                    result += f"\\n找到正确密钥对!\\n"
                    result += f"K1: {k1:016b} ({k1:04X})\\n"
                    result += f"K2: {k2:016b} ({k2:04X})\\n"
                    
                    # 如果有多个明密文对，进一步验证
                    if len(known_pairs) > 1:
                        all_correct = True
                        for p, c in known_pairs[1:]:
                            if self.double_encrypt(p, k1, k2) != c:
                                all_correct = False
                                break
                        
                        if all_correct:
                            result += "所有明密文对验证通过!\\n"
                            break
                        else:
                            result += "部分明密文对验证失败，继续搜索...\\n"
                    else:
                        break
        
        elapsed_time = time.time() - start_time
        result += f"\\n攻击完成，用时: {elapsed_time:.2f} 秒\\n"
        result += f"发现的候选密钥对数量: {len(found_keys)}\\n"
        
        if not found_keys:
            result += "未找到匹配的密钥对（搜索范围受限）\\n"
        
        return result
    
    def generate_known_pairs(self, key1, key2, num_pairs=3):
        """
        生成已知明密文对用于中间相遇攻击测试
        """
        pairs = []
        test_plaintexts = [
            0b0110111101101011,
            0b1010101010101010,
            0b1111000011110000
        ]
        
        for i in range(min(num_pairs, len(test_plaintexts))):
            plaintext = test_plaintexts[i]
            ciphertext = self.double_encrypt(plaintext, key1, key2)
            pairs.append((plaintext, ciphertext))
        
        return pairs

def test_multi_encrypt():
    """
    测试多重加密功能
    """
    multi = MultiEncrypt()
    
    plaintext = 0b0110111101101011
    key1 = 0b1010011100111011
    key2 = 0b1100001111000011
    key3 = 0b0011110000111100
    
    print("=== 多重加密测试 ===")
    print(f"明文: {plaintext:016b} ({plaintext:04X})")
    print(f"密钥1: {key1:016b} ({key1:04X})")
    print(f"密钥2: {key2:016b} ({key2:04X})")
    print(f"密钥3: {key3:016b} ({key3:04X})")
    print()
    
    # 测试双重加密
    print("--- 双重加密测试 ---")
    double_cipher = multi.double_encrypt(plaintext, key1, key2)
    print(f"双重加密密文: {double_cipher:016b} ({double_cipher:04X})")
    
    double_plain = multi.double_decrypt(double_cipher, key1, key2)
    print(f"双重解密明文: {double_plain:016b} ({double_plain:04X})")
    print(f"双重加密测试: {'✓ 通过' if plaintext == double_plain else '✗ 失败'}")
    print()
    
    # 测试三重加密（2密钥）
    print("--- 三重加密（2密钥）测试 ---")
    triple2_cipher = multi.triple_encrypt_2key(plaintext, key1, key2)
    print(f"三重加密密文: {triple2_cipher:016b} ({triple2_cipher:04X})")
    
    triple2_plain = multi.triple_decrypt_2key(triple2_cipher, key1, key2)
    print(f"三重解密明文: {triple2_plain:016b} ({triple2_plain:04X})")
    print(f"三重加密（2密钥）测试: {'✓ 通过' if plaintext == triple2_plain else '✗ 失败'}")
    print()
    
    # 测试三重加密（3密钥）
    print("--- 三重加密（3密钥）测试 ---")
    triple3_cipher = multi.triple_encrypt_3key(plaintext, key1, key2, key3)
    print(f"三重加密密文: {triple3_cipher:016b} ({triple3_cipher:04X})")
    
    triple3_plain = multi.triple_decrypt_3key(triple3_cipher, key1, key2, key3)
    print(f"三重解密明文: {triple3_plain:016b} ({triple3_plain:04X})")
    print(f"三重加密（3密钥）测试: {'✓ 通过' if plaintext == triple3_plain else '✗ 失败'}")
    print()
    
    # 中间相遇攻击演示
    print("--- 中间相遇攻击演示 ---")
    attack_result = multi.meet_in_middle_attack()
    print(attack_result)

if __name__ == "__main__":
    test_multi_encrypt()
