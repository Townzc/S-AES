# S-AES Algorithm Implementation Project

## Project Overview

This project is the second assignment for the "Introduction to Information Security" course, implementing a complete 5-level Simplified AES (S-AES) algorithm system. Developed in Python with a graphical user interface, it supports various encryption modes and attack demonstrations.

## ✨ Features & Capabilities

### 🔐 Level 1: Basic Testing
- **Core S-AES Algorithm**: 16-bit data and 16-bit key encryption/decryption
- **Standard Components**: S-box substitution, round key generation, column mixing
- **Flexible Input**: GUI support for both binary and hexadecimal formats

### 🔄 Level 2: Cross-Platform Testing
- **Standardization Compliance**: Ensures algorithm compatibility across implementations
- **Test Vector Validation**: Built-in standard test vectors for verification
- **Cross-Validation Support**: Compatible with other S-AES implementations

### 📝 Level 3: ASCII String Extension
- **String Encryption**: Full support for ASCII character string encryption/decryption
- **Smart Grouping**: Automatic 2-byte block processing with padding
- **Visual Processing**: Real-time visualization of block operations

### 🔢 Level 4: Multiple Encryption Modes
- **Double Encryption**: 32-bit keys with C = E_K2(E_K1(P)) structure
- **Triple Encryption**: Support for both 32-bit (EDE mode) and 48-bit key configurations
- **Meet-in-the-Middle Attack**: Live demonstration of double encryption vulnerabilities

### 🔗 Level 5: CBC Working Mode
- **Cipher Block Chaining**: Complete CBC mode implementation
- **Variable Length Support**: Encryption/decryption for arbitrary message lengths
- **Tampering Detection**: Advanced analysis and impact demonstration

## 📁 Project Structure

```
S-AES-Project/
├── 📜 s_aes.py          # Core S-AES algorithm implementation
├── 🖥️ gui.py            # Graphical user interface
├── 🔢 multi_encrypt.py  # Multiple encryption functionality
├── 🔗 cbc_mode.py       # CBC working mode implementation
├── 🧪 test_cases.py     # Comprehensive test suites
├── 📋 requirements.txt  # Project dependencies
├── 📖 README.md         # Project documentation
└── 📚 user_guide.md     # User operation guide
```

## 🚀 Quick Start Guide

### 🔧 System Requirements
- **Python**: Version 3.7 or higher
- **tkinter**: Python standard library (usually pre-installed)

### 💻 Installation & Setup

1. **📥 Clone Repository**
   ```bash
   git clone <repository-url>
   cd S-AES-Project
   ```

2. **🎮 Launch GUI Interface**
   ```bash
   python gui.py
   ```

3. **🧪 Run Test Suite**
   ```bash
   python test_cases.py
   ```

4. **🔍 Individual Module Testing**
   ```bash
   python s_aes.py          # Test core algorithm
   python multi_encrypt.py  # Test multiple encryption
   python cbc_mode.py       # Test CBC mode
   ```

## 📖 User Guide

### ⚡ Basic Operations

1. **🚀 Launch Application**: Run `python gui.py`
2. **🎯 Select Function**: Click corresponding tabs to choose the test level
3. **📝 Input Data**: Enter plaintext, keys, and other parameters in input fields
4. **▶️ Execute Operation**: Click appropriate buttons to perform encryption, decryption, or attacks
5. **📊 View Results**: Check detailed processing steps and results in the output area

### 📋 Input Formats

- **Binary**: 16-bit binary numbers, e.g., `0110111101101011`
- **Hexadecimal**: 4-digit hex numbers, e.g., `6F6B`
- **ASCII Text**: Arbitrary length strings, e.g., `Hello World!`

### 🎮 Level-Specific Features

#### 🔐 Level 1: Basic Testing
- **Pre-configured Test Cases**: Ready-to-use example data
- **Custom Input Support**: User-defined plaintext and keys
- **Real-time Processing**: Live display of encryption/decryption steps

#### 🔄 Level 2: Cross-Platform Testing
- **Built-in Test Vectors**: Standard validation datasets
- **Compatibility Reports**: Generated cross-validation summaries
- **Algorithm Verification**: Correctness validation against standards

#### 📝 Level 3: ASCII Extension
- **Automatic String Grouping**: Intelligent 2-byte block processing
- **Step-by-step Visualization**: Display of each block's processing
- **Special Character Support**: Handle text with special symbols

#### 🔢 Level 4: Multiple Encryption
- **Three Encryption Modes**: Choose from double/triple encryption options
- **Live Attack Demonstration**: Real-time meet-in-the-middle attack simulation
- **Detailed Attack Analysis**: Complete process and result breakdown

#### 🔗 Level 5: CBC Mode
- **Variable Message Length**: Support for arbitrary-length message encryption
- **Tampering Detection Demo**: Interactive corruption impact analysis
- **CBC Chain Visualization**: Visual representation of cipher block chaining

## ⚙️ Technical Implementation

### 🧬 Core Algorithms

1. **S-Box Substitution**: Standard 4×4 S-box and inverse S-box operations
2. **Row Shifting**: Lower row nibble exchange mechanism
3. **Column Mixing**: Matrix operations in GF(2^4) finite field
4. **Round Key Generation**: Standard key expansion algorithm implementation

### 🌟 Key Features

- **🧩 Modular Design**: Independent function implementations for easy testing and extension
- **✅ Complete Validation**: Every operation includes corresponding inverse operation verification
- **👥 User-Friendly Interface**: Intuitive GUI with detailed operational guidance
- **🎓 Educational Focus**: Comprehensive display of algorithm execution process and intermediate results

## 🧪 Testing & Validation

The project includes comprehensive test suites to verify the correctness of all functionalities:

```bash
python test_cases.py
```

**Test Coverage:**
- ✅ **Core S-AES**: Basic encryption/decryption functionality
- ✅ **Multiple Encryption**: All encryption mode variations
- ✅ **CBC Working Mode**: Cipher block chaining operations
- ✅ **Cross-Compatibility**: Validation against standard implementations
- ✅ **Performance Benchmarks**: Speed and efficiency testing

## 🤝 Contributing Guidelines

### 📝 Code Standards

1. **📏 Naming Convention**: Use camelCase or snake_case consistently
2. **💬 Documentation**: Add detailed comments for complex algorithms and key logic
3. **🎯 Function Design**: Single-purpose functions for easy testing and reusability
4. **⚠️ Error Handling**: Appropriate exception handling with user-friendly messages

### 💡 Development Best Practices

1. **🔧 Pre-Modification Testing**: Run complete test suite before modifying core algorithms
2. **🆕 Feature Testing**: Include corresponding test cases for new functionality
3. **📖 Code Readability**: Maintain clean, readable, and maintainable code structure
4. **🔒 Cryptographic Standards**: Follow established cryptographic algorithm implementations

## ❓ Frequently Asked Questions

### Q: Why was Python chosen for implementation?
**A:** Python offers clean syntax that makes algorithm logic easy to understand, plus built-in GUI libraries that enable rapid development of educational demonstration interfaces.

### Q: How can I verify the implementation's correctness?
**A:** The project provides comprehensive test cases and standard test vectors to ensure consistency with theoretical standards.

### Q: Why is the meet-in-the-middle attack search range limited?
**A:** This is designed for demonstration purposes and runtime efficiency. In actual attacks, the complete key space would be searched.

### Q: Can this be cross-validated with implementations in other programming languages?
**A:** Absolutely! The project provides standard test vectors that support comparison with implementations in C++, Java, and other languages.

## 📋 Version History

- **v1.0** (October 2025): Initial release implementing all 5 level functionalities
  - ✨ Complete S-AES algorithm implementation
  - 🖥️ Graphical user interface
  - 🔢 Multiple encryption and CBC mode support
  - ⚔️ Meet-in-the-middle attack demonstration

## 📄 License

This project is intended for **educational purposes only**. Please do not use in actual cryptographic systems.

## 📞 Contact Information

- **Course**: Introduction to Information Security
- **Assignment**: Assignment #2 - S-AES Algorithm Implementation
- **Development Team**: Wu Yan Group (Zhice Tang, Xiaohao Zhou)

---

<div align="center">
<em>This project implements all S-AES algorithm functionalities with comprehensive testing validation and user documentation.</em>
</div>
