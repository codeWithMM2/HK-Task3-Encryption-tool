# 🔐 Custom Data Encryption & Decryption Tool
### 🚀 The Maryam Cryptographic Protocol v1.0 (CLI-Based Security Application)
*Developed in fulfillment of **HK— Task 3** Internship Requirements.*

---

## 🎯 1. Project Objective & Overview
This repository contains a high-grade Command Line Interface (CLI) based data security application built in Python. The tool simulates real-world enterprise data protection schemes by implementing a strict **4-Layer Cascading Hybrid Cryptographic Architecture System**. It provides absolute confidentiality, integrity, and non-repudiation configurations without relying on standard un-customized encoding.

---

## 🚀 2. Architectural Deep-Dive: The 4-Layer Hybrid Cryptography
To fulfill the advanced system specifications demanding a **custom algorithm** rather than plain encoding, this tool processes input via four tightly integrated modular layers:

| Layer Level | Layer Technique Name | Structural Logic & Cryptographic Engine |
| :--- | :--- | :--- |
| **Layer 1** | Dynamic Caesar Shift | Takes the unique SHA-256 hash byte array of the user's password/key. Computes an index-bound mathematical modulo operation `(hash_value % 47) + 1` to generate an unpredictable runtime character shift offset strictly constrained between 1 and 47. |
| **Layer 2** | Monoalphabetic Substitution | Maps individual characters to a specialized positional substitution lookup table array. Swaps alphanumeric values based on localized randomized character indexing to defeat baseline frequency analysis attacks. |
| **Layer 3** | Bitwise XOR Manipulation & Sequencing | Executes character-by-character binary XOR processing bound directly against the raw password byte stream. Formats mathematical byte remnants into strict 3-digit padded numbers (`:03d`) and reverses the final sequence using string slicing matrix `[::-1]`. |
| **Layer 4** | Universal Base64 VIP Formatting | Standardizes raw bitwise outputs and binary arrays into high-compatibility, universally readable ASCII safe-text blocks. This layer guarantees zero file system corruption or text bleeding during long-term storage configurations. |

---

## 📊 3. File Handling & Structural Integrity (JSON Auditing)
To elevate data accountability, this application exports encrypted payloads using highly standardized **JSON Metadata Packages** instead of vulnerable flat TXT arrays. This satisfies strict system validation checks:

### Metadata Object Schema Archetype:
* 🏷️ `tool`: Tracks application configuration logs (`"The Maryam Protocol v1.0"`).
* 📅 `timestamp`: Records system-clock parameters when execution finishes (`YYYY-MM-DD HH:MM:SS`).
* 💡 `hint`: User-defined password recovery contextual string (Never stores raw password values).
* 🔒 `encrypted_data`: Secure universal Base64-wrapped multi-layered encrypted string block.

---

## 🛠️ 4. Functional Requirements & Setup Instructions

### ⚙️ System Requirements & Setup
The engineering pipeline relies entirely upon **Python 3.x Standard Built-in Libraries** (`os`, `json`, `hashlib`, `base64`, `datetime`). 
* No external third-party `pip` installations are required.
* Fully cross-platform compliant (Windows, Linux, macOS compatible).

### 🚀 Execution Command
Open your terminal inside the source folder and execute:
```bash
python encryption tool.py
