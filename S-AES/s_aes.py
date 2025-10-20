"""
S-AES算法核心实现
实现简化的AES算法，包括S盒、轮密钥生成、加解密等核心功能

作者：吴彦组（Zhice Tang，Xiaohao Zhou）
日期：2025年10月
"""

class SAES:
    def __init__(self):
        # S盒定义（根据S-AES标准）
        self.s_box = [
            [0x9, 0x4, 0xa, 0xb],
            [0xd, 0x1, 0x8, 0x5],
            [0x6, 0x2, 0x0, 0x3],
            [0xc, 0xe, 0xf, 0x7]
        ]
        
        # 逆S盒
        self.inv_s_box = [
            [0xa, 0x5, 0x9, 0xb],
            [0x1, 0x7, 0x8, 0xf],
            [0x6, 0x0, 0x2, 0x3],
            [0xc, 0x4, 0xd, 0xe]
        ]
        
        # 轮常数
        self.rcon = [0x80, 0x30]
        
    def substitute_nibbles(self, state, use_inverse=False):
        """
        半字节替换：使用S盒或逆S盒对状态进行替换
        """
        s_box = self.inv_s_box if use_inverse else self.s_box
        result = 0
        
        for i in range(4):
            nibble = (state >> (4 * (3 - i))) & 0xF
            row = (nibble >> 2) & 0x3
            col = nibble & 0x3
            new_nibble = s_box[row][col]
            result |= (new_nibble << (4 * (3 - i)))
            
        return result
    
    def shift_rows(self, state):
        """
        行移位：交换下行的两个半字节
        """
        # 提取4个半字节
        s00 = (state >> 12) & 0xF
        s01 = (state >> 8) & 0xF  
        s10 = (state >> 4) & 0xF
        s11 = state & 0xF
        
        # 交换下行
        return (s00 << 12) | (s01 << 8) | (s11 << 4) | s10
    
    def mix_columns(self, state, use_inverse=False):
        """
        列混淆：使用矩阵乘法混淆列
        """
        # 提取4个半字节
        s00 = (state >> 12) & 0xF
        s01 = (state >> 8) & 0xF
        s10 = (state >> 4) & 0xF
        s11 = state & 0xF
        
        if use_inverse:
            # 逆列混淆矩阵
            new_s00 = self.gf_multiply(0x9, s00) ^ self.gf_multiply(0x2, s01)
            new_s01 = self.gf_multiply(0x2, s00) ^ self.gf_multiply(0x9, s01)
            new_s10 = self.gf_multiply(0x9, s10) ^ self.gf_multiply(0x2, s11)
            new_s11 = self.gf_multiply(0x2, s10) ^ self.gf_multiply(0x9, s11)
        else:
            # 正向列混淆矩阵
            new_s00 = self.gf_multiply(0x1, s00) ^ self.gf_multiply(0x4, s01)
            new_s01 = self.gf_multiply(0x4, s00) ^ self.gf_multiply(0x1, s01)
            new_s10 = self.gf_multiply(0x1, s10) ^ self.gf_multiply(0x4, s11)
            new_s11 = self.gf_multiply(0x4, s10) ^ self.gf_multiply(0x1, s11)
        
        return (new_s00 << 12) | (new_s01 << 8) | (new_s10 << 4) | new_s11
    
    def gf_multiply(self, a, b):
        """
        GF(2^4)域上的乘法运算
        """
        result = 0
        for i in range(4):
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & 0x10:  # 如果超出4位
                a ^= 0x13  # 约化多项式 x^4 + x + 1
        return result & 0xF
    
    def add_round_key(self, state, key):
        """
        轮密钥加：状态与轮密钥异或
        """
        return state ^ key
    
    def key_expansion(self, key):
        """
        密钥扩展：从16位主密钥生成两个轮密钥
        """
        # 提取密钥的两个字节
        w0 = (key >> 8) & 0xFF
        w1 = key & 0xFF
        
        # 第一轮密钥扩展
        # RotNib(w1)
        temp = ((w1 << 4) | (w1 >> 4)) & 0xFF
        
        # SubNib(RotNib(w1))
        temp = self.sub_nib(temp)
        
        # w2 = w0 ⊕ RCON1 ⊕ SubNib(RotNib(w1))
        w2 = w0 ^ self.rcon[0] ^ temp
        
        # w3 = w2 ⊕ w1
        w3 = w2 ^ w1
        
        # 第二轮密钥扩展
        # RotNib(w3)
        temp = ((w3 << 4) | (w3 >> 4)) & 0xFF
        
        # SubNib(RotNib(w3))
        temp = self.sub_nib(temp)
        
        # w4 = w2 ⊕ RCON2 ⊕ SubNib(RotNib(w3))
        w4 = w2 ^ self.rcon[1] ^ temp
        
        # w5 = w4 ⊕ w3
        w5 = w4 ^ w3
        
        return [key, (w2 << 8) | w3, (w4 << 8) | w5]
    
    def sub_nib(self, byte_val):
        """
        对一个字节的两个半字节分别进行S盒替换
        """
        high_nibble = (byte_val >> 4) & 0xF
        low_nibble = byte_val & 0xF
        
        # S盒替换
        high_row = (high_nibble >> 2) & 0x3
        high_col = high_nibble & 0x3
        new_high = self.s_box[high_row][high_col]
        
        low_row = (low_nibble >> 2) & 0x3
        low_col = low_nibble & 0x3
        new_low = self.s_box[low_row][low_col]
        
        return (new_high << 4) | new_low
    
    def encrypt(self, plaintext, key):
        """
        S-AES加密
        """
        # 密钥扩展
        round_keys = self.key_expansion(key)
        
        # 初始轮密钥加
        state = self.add_round_key(plaintext, round_keys[0])
        
        # 第1轮
        state = self.substitute_nibbles(state)
        state = self.shift_rows(state)
        state = self.mix_columns(state)
        state = self.add_round_key(state, round_keys[1])
        
        # 第2轮
        state = self.substitute_nibbles(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, round_keys[2])
        
        return state
    
    def decrypt(self, ciphertext, key):
        """
        S-AES解密
        """
        # 密钥扩展
        round_keys = self.key_expansion(key)
        
        # 初始轮密钥加
        state = self.add_round_key(ciphertext, round_keys[2])
        
        # 逆第2轮
        state = self.shift_rows(state)  # 逆行移位（S-AES中相同）
        state = self.substitute_nibbles(state, use_inverse=True)
        state = self.add_round_key(state, round_keys[1])
        
        # 逆第1轮
        state = self.mix_columns(state, use_inverse=True)
        state = self.shift_rows(state)
        state = self.substitute_nibbles(state, use_inverse=True)
        state = self.add_round_key(state, round_keys[0])
        
        return state

def test_s_aes():
    """
    测试S-AES算法的基本功能
    """
    saes = SAES()
    
    # 测试用例
    plaintext = 0b0110111101101011  # 16位明文
    key = 0b1010011100111011        # 16位密钥
    
    print(f"明文: {plaintext:016b} ({plaintext:04X})")
    print(f"密钥: {key:016b} ({key:04X})")
    
    # 加密
    ciphertext = saes.encrypt(plaintext, key)
    print(f"密文: {ciphertext:016b} ({ciphertext:04X})")
    
    # 解密
    decrypted = saes.decrypt(ciphertext, key)
    print(f"解密: {decrypted:016b} ({decrypted:04X})")
    
    # 验证
    if plaintext == decrypted:
        print("✓ 加解密测试通过！")
    else:
        print("✗ 加解密测试失败！")

if __name__ == "__main__":
    test_s_aes()
