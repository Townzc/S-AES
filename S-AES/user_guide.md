# S-AES Algorithm System User Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Installation & Launch](#installation--launch)
3. [Interface Introduction](#interface-introduction)
4. [Feature Details](#feature-details)
5. [Operation Examples](#operation-examples)
6. [FAQ](#faq)
7. [Technical Support](#technical-support)

## System Overview

The S-AES (Simplified AES) algorithm implementation system is a complete educational demonstration tool that implements the core functionality of a simplified version of the AES algorithm. The system features a graphical user interface and supports functional testing of 5 levels, making it suitable for cryptography learning and research.

### Key Features
- 🔒 Complete S-AES algorithm implementation
- 🖥️ Intuitive graphical user interface
- 📊 Detailed algorithm execution process display
- 🧪 Multiple testing modes and attack demonstrations
- 📚 Rich test cases and documentation

## Installation & Launch

### System Requirements
- Operating System: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- Python Version: 3.7 or higher
- Memory: At least 512MB available memory
- Storage: Approximately 50MB available space

### Installation Steps

1. **Verify Python Environment**
   ```bash
   python --version
   # Should display Python 3.7.x or higher
   ```

2. **Download Project Files**
   - Download the project archive from the provided link
   - Extract to local directory

3. **Launch System**
   ```bash
   cd S-AES-Project-Directory
   python gui.py
   ```

### Installation Verification
After launch, you should see a graphical interface with 5 tabs. If errors occur, please refer to the [FAQ](#faq) section.

## Interface Introduction

### Main Interface Layout

The system uses a tab design, with each tab corresponding to a functional level:

```
┌─────────────────────────────────────────────────────────┐
│ [Level 1: Basic Test] [Level 2: Cross Test] [Level 3: ASCII] │
│ [Level 4: Multi Encrypt] [Level 5: CBC Mode] [About]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Input Area:                                            │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ Plaintext Input │  │ Key Input       │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  Action Buttons:                                        │
│  [Encrypt] [Decrypt] [Clear]                           │
│                                                         │
│  Result Display Area:                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │         Detailed Process and Results             │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Input Format Instructions

The system supports multiple input formats:

1. **Binary Format**: 16-bit binary numbers
   - Example: `0110111101101011`
   - Purpose: Direct display of algorithm bit operations

2. **Hexadecimal Format**: 4-digit hexadecimal numbers
   - Example: `6F6B`
   - Purpose: Compact representation, convenient for calculation verification

3. **ASCII Text**: Arbitrary length strings
   - Example: `Hello World!`
   - Purpose: Real application scenario simulation

## Feature Details

### Level 1: Basic Testing

**Function Overview**: Implements basic encryption/decryption functionality of the standard S-AES algorithm.

**Operation Steps**:
1. Enter 16-bit data in the "Plaintext" input box
2. Enter 16-bit key in the "Key" input box
3. Click "Encrypt" button to execute encryption
4. View detailed process in the result area
5. Use ciphertext as input for decryption verification

**Output Information**:
- Input plaintext and key (binary and hexadecimal formats)
- Generated ciphertext
- Decryption verification results
- Algorithm execution status

**Typical Use Case**:
```
Plaintext: 0110111101101011 (6F6B)
Key: 1010011100111011 (A73B)
Ciphertext: 1111000110000110 (F186)
```

### Level 2: Cross Testing

**Function Overview**: Verifies standardized compatibility of algorithm implementation.

**Operation Steps**:
1. Click "Run Standard Test Cases" button
2. System automatically executes multiple preset tests
3. View detailed results of each test case
4. Verify if all tests pass

**Test Content**:
- Standard test vector verification
- Boundary condition testing (all 0s, all 1s)
- Random data testing
- Encryption/decryption consistency verification

**Result Interpretation**:
- ✓ Pass: Test case is correct
- ✗ Fail: Implementation may have issues
- Detailed information: Shows specific input/output data

### Level 3: ASCII Extension

**Function Overview**: Supports block encryption/decryption of ASCII strings.

**Operation Steps**:
1. Enter the string to encrypt in the "ASCII Text" box
2. Set 16-bit key
3. Click "Encrypt ASCII" to process the string
4. View block processing procedure
5. Use hexadecimal ciphertext for decryption testing

**Processing Procedure**:
1. Convert string to byte sequence
2. Group by 2 bytes (16 bits)
3. Automatically pad insufficient parts
4. Execute S-AES encryption on each block
5. Convert results to hexadecimal representation

**Notes**:
- Decryption requires hexadecimal format ciphertext input
- Encrypted strings may contain non-printable characters
- Padding characters are automatically removed during decryption

### Level 4: Multiple Encryption

**Function Overview**: Implements double encryption, triple encryption, and meet-in-the-middle attack demonstrations.

#### Double Encryption
- **Principle**: C = E_K2(E_K1(P))
- **Key Length**: 32 bits (K1 + K2)
- **Security**: Equivalent to 21-bit key strength (birthday attack)

#### Triple Encryption (2-key)
- **Principle**: C = E_K1(D_K2(E_K1(P)))
- **Mode**: EDE (Encrypt-Decrypt-Encrypt)
- **Key Length**: 32 bits (K1 + K2)

#### Triple Encryption (3-key)
- **Principle**: C = E_K3(E_K2(E_K1(P)))
- **Key Length**: 48 bits (K1 + K2 + K3)
- **Security**: Highest security level

#### Meet-in-the-Middle Attack
- **Target**: Break double encryption
- **Principle**: Time-space trade-off attack
- **Demonstration**: Automatically find correct key pairs

**Operation Steps**:
1. Select encryption mode (radio buttons)
2. Enter key of corresponding length
3. Execute encryption or decryption operation
4. Observe meet-in-the-middle attack execution process

### Level 5: CBC Working Mode

**Function Overview**: Implements Cipher Block Chaining mode, supporting arbitrary length plaintext.

**CBC Mode Characteristics**:
- Each block is XORed with the previous ciphertext block
- First block is XORed with Initialization Vector (IV)
- Errors propagate to subsequent blocks
- Same plaintext blocks produce different ciphertexts

**Operation Steps**:
1. Enter arbitrary length plaintext message
2. Set 16-bit key and initialization vector
3. Execute CBC encryption
4. View block processing details
5. Perform decryption verification or tampering tests

**Tampering Test**:
- Modify a specific block in the ciphertext
- Observe the impact on decryption results
- Understand CBC mode error propagation characteristics

## Operation Examples

### Example 1: Basic Encryption/Decryption Test

1. **Prepare Data**
   ```
   Plaintext: 0110111101101011
   Key: 1010011100111011
   ```

2. **Execute Encryption**
   - Switch to "Level 1: Basic Testing"
   - Enter plaintext and key
   - Click "Encrypt" button

3. **Expected Result**
   ```
   Ciphertext: 1111000110000110 (F186)
   Status: ✓ Encryption successful
   ```

4. **Verify Decryption**
   - Copy ciphertext to plaintext input box
   - Click "Decrypt" button
   - Confirm recovery of original plaintext

### Example 2: ASCII String Processing

1. **Input String**
   ```
   Text: Hello!
   Key: A73B
   ```

2. **View Block Process**
   ```
   Block 1: 'He' -> 4865 (hex) -> After encryption...
   Block 2: 'll' -> 6C6C (hex) -> After encryption...
   Block 3: 'o!' -> 6F21 (hex) -> After encryption...
   ```

3. **Decryption Verification**
   - Use generated hexadecimal ciphertext
   - Execute decryption operation
   - Confirm recovery of original string

### Example 3: Meet-in-the-Middle Attack Demonstration

1. **Launch Attack**
   - Select "Meet-in-the-Middle Attack" mode
   - Click "Meet-in-the-Middle Attack" button
   - Wait for attack completion

2. **Observe Process**
   ```
   Phase 1: Computing E_K1(P) for all K1...
   Building forward table with 4096 entries
   Phase 2: Computing D_K2(C) and searching for matches...
   Found correct key pair!
   K1: 1010011100111011 (A73B)
   K2: 1100001111000011 (C0C3)
   ```

### Example 4: CBC Mode Testing

1. **Set Parameters**
   ```
   Plaintext: This is a test message for CBC mode.
   Key: A73B
   Initialization Vector: F0F0
   ```

2. **Execute Encryption**
   - System automatically groups and pads
   - Display processing procedure for each block
   - Generate complete ciphertext sequence

3. **Tampering Test**
   - System automatically modifies a byte in ciphertext
   - Execute decryption and show impact
   - Observe error propagation effects

## FAQ

### Installation Issues

**Q: Runtime error "ModuleNotFoundError"**
A: Check if Python version meets requirements (≥3.7), ensure tkinter is installed.

**Q: Interface display abnormalities or garbled text**
A: Confirm system supports Unicode display, try adjusting system encoding settings.

### Usage Issues

**Q: Incorrect input format error**
A: Check input format:
- Binary: Only contains 0 and 1, length must be 16 bits
- Hexadecimal: Only contains 0-9 and A-F, length must be 4 digits
- ASCII: Any printable characters

**Q: Encryption/decryption results don't match**
A: Confirm using same key and parameters, check input data accuracy.

**Q: Meet-in-the-middle attack takes very long time**
A: This is normal behavior, attack needs to search through many key combinations, please wait patiently.

**Q: CBC mode decryption fails**
A: Confirm initialization vector (IV) is consistent with encryption, check ciphertext format integrity.

### Performance Issues

**Q: Program runs slowly**
A: S-AES is primarily for educational demonstration, performance is not the main consideration. To improve performance:
- Reduce detailed information display
- Limit test data scale
- Use faster computers

**Q: High memory usage**
A: Clear result display area history, close unnecessary tabs.

## Technical Support

### Log Information

If you encounter problems, check detailed console output:

```bash
python gui.py
# View detailed execution logs in console
```

### Test Verification

Run complete test suite to verify system functionality:

```bash
python test_cases.py
```

### Contact Information

- **Course Forum**: Post technical questions and discussions
- **Email Support**: Send detailed error information and system environment
- **Lab Office Hours**: On-site demonstration and debugging
- **Development Team**: Wu Yan Group (Zhice Tang, Xiaohao Zhou)

### System Information Collection

When reporting issues, please provide the following information:
1. Operating system version
2. Python version
3. Specific error steps
4. Complete error message content
5. Expected vs actual results

---

*This user guide covers all functionality and operation methods of the S-AES algorithm system. For other questions, please refer to project documentation or contact technical support.*
