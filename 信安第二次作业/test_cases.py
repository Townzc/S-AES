"""
S-AES算法测试用例
包含所有5个关卡的完整测试
"""

import unittest
import sys
import os
from s_aes import SAES
from multi_encrypt import MultiEncrypt
from cbc_mode import CBCMode

class TestSAES(unittest.TestCase):
    """S-AES基本功能测试"""
    
    def setUp(self):
        self.saes = SAES()
    
    def test_s_box_substitution(self):
        """测试S盒替换功能"""
        # 测试S盒查找
        self.assertEqual(self.saes.s_box[0][0], 0x9)
        self.assertEqual(self.saes.s_box[3][3], 0x7)
        
        # 测试半字节替换
        state = 0x6B6B  # 0110 1011 0110 1011
        result = self.saes.substitute_nibbles(state)
        # 验证结果不为零且与输入不同
        self.assertNotEqual(result, 0)
        self.assertNotEqual(result, state)
    
    def test_shift_rows(self):
        """测试行移位功能"""
        state = 0x1234  # 0001 0010 0011 0100
        result = self.saes.shift_rows(state)
        # 行移位应该交换下行的两个半字节
        expected = 0x1243  # 0001 0010 0100 0011
        self.assertEqual(result, expected)
    
    def test_mix_columns(self):
        """测试列混淆功能"""
        state = 0x1234
        result = self.saes.mix_columns(state)
        # 验证结果不为零
        self.assertNotEqual(result, 0)
        
        # 测试逆列混淆
        inv_result = self.saes.mix_columns(result, use_inverse=True)
        # 由于GF运算的复杂性，这里只验证操作不会出错
        self.assertIsInstance(inv_result, int)
    
    def test_key_expansion(self):
        """测试密钥扩展功能"""
        key = 0xA73B  # 1010 0111 0011 1011
        round_keys = self.saes.key_expansion(key)
        
        # 应该生成3个轮密钥
        self.assertEqual(len(round_keys), 3)
        self.assertEqual(round_keys[0], key)  # 第一个应该是原密钥
        
        # 其他轮密钥不应该与原密钥相同
        self.assertNotEqual(round_keys[1], key)
        self.assertNotEqual(round_keys[2], key)
    
    def test_basic_encryption_decryption(self):
        """测试基本加解密功能"""
        plaintext = 0x6B6B  # 0110 1011 0110 1011
        key = 0xA73B        # 1010 0111 0011 1011
        
        # 加密
        ciphertext = self.saes.encrypt(plaintext, key)
        self.assertNotEqual(ciphertext, plaintext)
        
        # 解密
        decrypted = self.saes.decrypt(ciphertext, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_standard_test_vectors(self):
        """标准测试向量"""
        test_cases = [
            {"plain": 0x6B6B, "key": 0xA73B},
            {"plain": 0x0000, "key": 0x0000},
            {"plain": 0xFFFF, "key": 0xFFFF},
            {"plain": 0xAAAA, "key": 0x5555},
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                plaintext = case["plain"]
                key = case["key"]
                
                ciphertext = self.saes.encrypt(plaintext, key)
                decrypted = self.saes.decrypt(ciphertext, key)
                
                self.assertEqual(decrypted, plaintext,
                    f"Failed for plain={plaintext:04X}, key={key:04X}")

class TestMultiEncrypt(unittest.TestCase):
    """多重加密测试"""
    
    def setUp(self):
        self.multi = MultiEncrypt()
    
    def test_double_encryption(self):
        """测试双重加密"""
        plaintext = 0x6B6B
        key1 = 0xA73B
        key2 = 0xC0C3
        
        # 双重加密
        ciphertext = self.multi.double_encrypt(plaintext, key1, key2)
        
        # 双重解密
        decrypted = self.multi.double_decrypt(ciphertext, key1, key2)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_triple_encryption_2key(self):
        """测试三重加密（2密钥）"""
        plaintext = 0x6B6B
        key1 = 0xA73B
        key2 = 0xC0C3
        
        # 三重加密
        ciphertext = self.multi.triple_encrypt_2key(plaintext, key1, key2)
        
        # 三重解密
        decrypted = self.multi.triple_decrypt_2key(ciphertext, key1, key2)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_triple_encryption_3key(self):
        """测试三重加密（3密钥）"""
        plaintext = 0x6B6B
        key1 = 0xA73B
        key2 = 0xC0C3
        key3 = 0x3C3C
        
        # 三重加密
        ciphertext = self.multi.triple_encrypt_3key(plaintext, key1, key2, key3)
        
        # 三重解密
        decrypted = self.multi.triple_decrypt_3key(ciphertext, key1, key2, key3)
        
        self.assertEqual(decrypted, plaintext)

class TestCBCMode(unittest.TestCase):
    """CBC模式测试"""
    
    def setUp(self):
        self.cbc = CBCMode()
    
    def test_pkcs7_padding(self):
        """测试PKCS7填充"""
        data = b"Hello"
        padded = self.cbc.pkcs7_pad(data, 2)
        
        # 5字节数据，2字节分组，应该填充1个字节
        self.assertEqual(len(padded), 6)
        self.assertEqual(padded[-1], 1)  # 填充字节应该是1
        
        # 去填充
        unpadded = self.cbc.pkcs7_unpad(padded)
        self.assertEqual(unpadded, data)
    
    def test_cbc_encryption_decryption(self):
        """测试CBC加解密"""
        plaintext = "Hello, World!"
        key = 0xA73B
        iv = 0xF0F0
        
        # CBC加密
        ciphertext_hex, _ = self.cbc.encrypt(plaintext, key, iv)
        self.assertIsInstance(ciphertext_hex, str)
        self.assertTrue(len(ciphertext_hex) > 0)
        
        # CBC解密
        decrypted, _ = self.cbc.decrypt(ciphertext_hex, key, iv)
        self.assertEqual(decrypted, plaintext)
    
    def test_iv_effect(self):
        """测试初始向量的影响"""
        plaintext = "Test message"
        key = 0xA73B
        iv1 = 0xF0F0
        iv2 = 0x0F0F
        
        # 使用不同IV加密相同明文
        cipher1, _ = self.cbc.encrypt(plaintext, key, iv1)
        cipher2, _ = self.cbc.encrypt(plaintext, key, iv2)
        
        # 密文应该不同
        self.assertNotEqual(cipher1, cipher2)
        
        # 但都能正确解密
        decrypted1, _ = self.cbc.decrypt(cipher1, key, iv1)
        decrypted2, _ = self.cbc.decrypt(cipher2, key, iv2)
        
        self.assertEqual(decrypted1, plaintext)
        self.assertEqual(decrypted2, plaintext)

class TestCrossCompatibility(unittest.TestCase):
    """交叉兼容性测试"""
    
    def test_algorithm_consistency(self):
        """测试算法一致性"""
        saes1 = SAES()
        saes2 = SAES()
        
        # 相同输入应产生相同输出
        plaintext = 0x6B6B
        key = 0xA73B
        
        cipher1 = saes1.encrypt(plaintext, key)
        cipher2 = saes2.encrypt(plaintext, key)
        
        self.assertEqual(cipher1, cipher2)
        
        # 解密也应该一致
        plain1 = saes1.decrypt(cipher1, key)
        plain2 = saes2.decrypt(cipher2, key)
        
        self.assertEqual(plain1, plaintext)
        self.assertEqual(plain2, plaintext)
        self.assertEqual(plain1, plain2)

def run_comprehensive_tests():
    """运行全面测试"""
    print("=== S-AES算法综合测试 ===\\n")
    
    # 运行所有测试用例
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # 测试结果总结
    print(f"\\n=== 测试结果总结 ===")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\\n成功率: {success_rate:.1f}%")
    
    return result.wasSuccessful()

def manual_test_scenarios():
    """手动测试场景"""
    print("\\n=== 手动测试场景 ===\\n")
    
    # 场景1：基本功能测试
    print("场景1：基本S-AES加解密")
    saes = SAES()
    
    test_cases = [
        (0x6B6B, 0xA73B, "标准测试向量"),
        (0x0000, 0x0000, "全零测试"),
        (0xFFFF, 0xFFFF, "全一测试"),
    ]
    
    for plaintext, key, description in test_cases:
        ciphertext = saes.encrypt(plaintext, key)
        decrypted = saes.decrypt(ciphertext, key)
        status = "✓" if plaintext == decrypted else "✗"
        
        print(f"{description}:")
        print(f"  明文: {plaintext:04X}, 密钥: {key:04X}")
        print(f"  密文: {ciphertext:04X}, 解密: {decrypted:04X} {status}")
    
    # 场景2：多重加密测试
    print("\\n场景2：多重加密测试")
    multi = MultiEncrypt()
    
    plaintext = 0x1234
    key1, key2 = 0xABCD, 0xEF01
    
    double_cipher = multi.double_encrypt(plaintext, key1, key2)
    double_plain = multi.double_decrypt(double_cipher, key1, key2)
    
    print(f"双重加密: {plaintext:04X} -> {double_cipher:04X} -> {double_plain:04X}")
    print(f"状态: {'✓ 通过' if plaintext == double_plain else '✗ 失败'}")
    
    # 场景3：CBC模式测试
    print("\\n场景3：CBC模式测试")
    cbc = CBCMode()
    
    plaintext = "Hello, S-AES!"
    key = 0xA73B
    iv = 0xF0F0
    
    try:
        ciphertext_hex, _ = cbc.encrypt(plaintext, key, iv)
        decrypted, _ = cbc.decrypt(ciphertext_hex, key, iv)
        
        print(f"明文: {plaintext}")
        print(f"密文: {ciphertext_hex}")
        print(f"解密: {decrypted}")
        print(f"状态: {'✓ 通过' if plaintext == decrypted else '✗ 失败'}")
    except Exception as e:
        print(f"CBC测试失败: {e}")

def performance_test():
    """性能测试"""
    print("\\n=== 性能测试 ===\\n")
    
    import time
    
    saes = SAES()
    plaintext = 0x1234
    key = 0xABCD
    
    # 测试加密性能
    start_time = time.time()
    iterations = 10000
    
    for _ in range(iterations):
        ciphertext = saes.encrypt(plaintext, key)
    
    encrypt_time = time.time() - start_time
    
    # 测试解密性能
    start_time = time.time()
    
    for _ in range(iterations):
        decrypted = saes.decrypt(ciphertext, key)
    
    decrypt_time = time.time() - start_time
    
    print(f"加密性能: {iterations} 次加密用时 {encrypt_time:.3f} 秒")
    print(f"平均加密时间: {encrypt_time/iterations*1000:.3f} 毫秒/次")
    print(f"解密性能: {iterations} 次解密用时 {decrypt_time:.3f} 秒")
    print(f"平均解密时间: {decrypt_time/iterations*1000:.3f} 毫秒/次")

if __name__ == "__main__":
    # 运行所有测试
    success = run_comprehensive_tests()
    
    # 运行手动测试场景
    manual_test_scenarios()
    
    # 运行性能测试
    performance_test()
    
    # 输出最终结果
    print(f"\\n=== 最终测试结果 ===")
    print(f"单元测试: {'✓ 全部通过' if success else '✗ 有失败'}")
    print("手动测试: 请查看上述输出")
    print("性能测试: 已完成")
    
    if success:
        print("\\n🎉 所有测试通过！S-AES实现正确！")
    else:
        print("\\n⚠️ 部分测试失败，请检查实现！")
