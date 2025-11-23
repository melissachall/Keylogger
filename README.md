# MEL Keylogger - Research & Educational Edition

## ⚠️ DISCLAIMER / AVERTISSEMENT

**ENGLISH:**
This project is developed for **EDUCATIONAL AND RESEARCH PURPOSES ONLY**. It is intended to demonstrate cybersecurity concepts, threat analysis, and defensive programming techniques. 

- **DO NOT** use this software on any system without explicit written authorization
- Unauthorized use of keyloggers is **ILLEGAL** in most jurisdictions
- This project is meant for controlled environments (VMs, isolated networks, penetration testing labs with proper authorization)
- The author and contributors are **NOT RESPONSIBLE** for any misuse or damage caused by this software

**FRANÇAIS:**
Ce projet est développé **UNIQUEMENT À DES FINS ÉDUCATIVES ET DE RECHERCHE**. Il vise à démontrer les concepts de cybersécurité, l'analyse des menaces et les techniques de programmation défensive.

- **NE PAS** utiliser ce logiciel sur un système sans autorisation écrite explicite
- L'utilisation non autorisée de keyloggers est **ILLÉGALE** dans la plupart des juridictions
- Ce projet est destiné aux environnements contrôlés (VMs, réseaux isolés, laboratoires de tests d'intrusion avec autorisation appropriée)
- L'auteur et les contributeurs ne sont **PAS RESPONSABLES** de toute utilisation abusive ou dommage causé par ce logiciel

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Security Features](#security-features)
- [Educational Objectives](#educational-objectives)
- [Legal Considerations](#legal-considerations)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## 🎯 Features

### Core Functionality
- **Keystroke Logging**: Captures all keyboard inputs with special key detection
- **Periodic Reporting**: Automated log transmission via email at configurable intervals
- **Data Compression**: Reduces log file size using zlib compression
- **Encryption Support**: Includes Fernet encryption framework (currently implemented but not active in data flow)

### Advanced Capabilities
- **Screenshot Capture**: Periodic screen captures at defined intervals
- **Clipboard Monitoring**: Tracks clipboard content changes (Windows only)
- **Audio Recording**: Records ambient audio in configurable durations
- **System Persistence**: Registry-based persistence mechanism (Windows only)
- **Cross-Platform Support**: Windows primary, Linux/macOS partial support

### Defensive Features
- **Error Logging**: Comprehensive error tracking for debugging
- **Graceful Degradation**: Continues operation even if individual modules fail
- **Configurable Intervals**: All timing parameters can be adjusted

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MEL Keylogger                        │
│                  (Main Controller)                      │
└──────────────┬──────────────────────────────────────────┘
               │
               ├──► Keyboard Listener (pynput)
               │    └─► Callback Handler → Log Buffer
               │
               ├──► Timer Subsystem
               │    ├─► Report Timer (Email Sender)
               │    ├─► Screenshot Timer (PIL)
               │    ├─► Clipboard Timer (win32clipboard)
               │    └─► Audio Timer (sounddevice)
               │
               ├──► Data Processing
               │    ├─► Compression (zlib)
               │    └─► Encryption (Fernet - framework)
               │
               ├──► Communication Module
               │    └─► SMTP Email (smtplib)
               │
               └──► Persistence Module (Windows Registry)
```

---

## 📦 Requirements

### Python Version
- Python 3.8 or higher

### Dependencies

```txt
pynput>=1.7.6
Pillow>=9.0.0
sounddevice>=0.4.5
scipy>=1.7.0
cryptography>=38.0.0
pywin32>=305  # Windows only
```

### Operating System
- **Primary**: Windows 10/11
- **Partial Support**: Linux, macOS (no clipboard/persistence features)

---

## 🔧 Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd mel-keylogger

# Or extract from ZIP
unzip mel-keylogger.zip
cd mel-keylogger
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python keylogger.py --help
```

---

## ⚙️ Configuration

### Create Configuration File

Create a file named `keylogger.conf` in the same directory as the script:

```ini
[EMAIL]
address = your_email@outlook.com
password = your_password_here
smtp_host = smtp.office365.com
smtp_port = 587
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `address` | Email address for sending/receiving logs | Required |
| `password` | Email account password | Required |
| `smtp_host` | SMTP server hostname | smtp.office365.com |
| `smtp_port` | SMTP server port | 587 |

### Supported Email Providers

| Provider | SMTP Host | Port |
|----------|-----------|------|
| Outlook/Hotmail | smtp.office365.com | 587 |
| Gmail | smtp.gmail.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |

**Note for Gmail**: You must enable "App Passwords" in your Google Account settings.

---

## 🚀 Usage

### Basic Usage

```bash
python keylogger.py
```

### Command Line Arguments (Currently Implemented)

The current version uses hardcoded parameters in the `__main__` block:

```python
kl = ProKeylogger(interval=60, report_method="email", log_dir="logs")
```

### Modifying Parameters

Edit the script directly to change:

```python
# Change report interval (in seconds)
kl = ProKeylogger(interval=120, ...)  # Reports every 2 minutes

# Change screenshot interval (at top of script)
SCREENSHOT_INTERVAL = 120  # Screenshots every 2 minutes

# Change audio duration
AUDIO_DURATION = 15  # 15 seconds of audio
```

### Testing in Safe Environment

```bash
# Run in a VM with minimal permissions
# Monitor logs directory
python keylogger.py

# Check debug logs
tail -f logs/debug.log  # Linux/macOS
type logs\debug.log     # Windows
```

---

## 📁 Project Structure

```
mel-keylogger/
│
├── keylogger.py           # Main script
├── keylogger.conf         # Configuration file (create this)
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
└── logs/                 # Generated at runtime
    ├── debug.log         # Error and debug logs
    ├── keylog_*.txt      # Keystroke logs
    ├── screenshot_*.png  # Screen captures
    ├── clipboard_*.txt   # Clipboard contents
    └── audio_*.wav       # Audio recordings
```

---

## 🔐 Security Features

### Implemented

1. **Data Compression**: Reduces file size and slightly obfuscates content
   ```python
   compress_data(data)  # zlib + base64
   ```

2. **Encryption Framework**: Fernet symmetric encryption ready to use
   ```python
   encrypt_data(data, key)  # Currently defined but not in data flow
   ```

3. **Secure Communication**: SMTP over TLS for email transmission

4. **Error Isolation**: Exceptions don't crash the main process

### Recommendations for Enhanced Security

```python
# Store encryption key securely
KEY_FILE = os.path.join(log_dir, ".encryption.key")

# Encrypt logs before writing
with open(filename, "wb") as f:
    f.write(encrypt_data(data, LOG_ENCRYPTION_KEY))

# Use environment variables for credentials
import os
EMAIL = os.getenv("KEYLOGGER_EMAIL")
PASSWORD = os.getenv("KEYLOGGER_PASSWORD")
```

---

## 🎓 Educational Objectives

This project demonstrates the following cybersecurity concepts:

### 1. **Threat Modeling**
- Understanding attack vectors
- Analyzing persistence mechanisms
- Evaluating data exfiltration methods

### 2. **Defensive Programming**
- Error handling and logging
- Graceful failure modes
- Resource management

### 3. **System Programming**
- Low-level input capture (keyboard hooks)
- Registry manipulation (Windows)
- Timer-based task scheduling

### 4. **Cryptography**
- Symmetric encryption (Fernet)
- Data compression
- Secure communication channels

### 5. **Detection & Mitigation**
Students should analyze:
- How antivirus software detects this code
- Network signatures for data exfiltration
- Registry monitoring for persistence detection
- Behavioral analysis techniques

---

## ⚖️ Legal Considerations

### When is this LEGAL?

✅ **Permitted scenarios:**
- Personal VM for educational purposes
- Authorized penetration testing with signed contracts
- Corporate security training with proper authorization
- Academic research with institutional approval

### When is this ILLEGAL?

❌ **Prohibited scenarios:**
- Installing on someone else's computer without consent
- Workplace computers without employer authorization
- Public computers or shared devices
- Any system where you don't have explicit permission

### Penalties for Misuse

Unauthorized use may result in:
- Criminal charges (Computer Fraud and Abuse Act - USA, RGPD - EU)
- Civil lawsuits
- Expulsion from educational institutions
- Professional license revocation

**Always consult with legal counsel before deploying monitoring software.**

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Email Not Sending

```
Error: Authentication failed
```

**Solutions:**
- Verify credentials in `keylogger.conf`
- Enable "Less Secure Apps" (Gmail) or use App Password
- Check SMTP host and port settings
- Verify firewall allows outbound port 587

#### 2. Import Errors (Windows)

```
ImportError: No module named 'win32clipboard'
```

**Solution:**
```bash
pip install pywin32
```

#### 3. Permission Errors (Registry)

```
PermissionError: [WinError 5] Access is denied
```

**Solution:**
- Run as Administrator (for persistence testing only)
- Or disable persistence feature for basic testing

#### 4. Audio Recording Fails

```
Error recording audio: [Errno -9996] Invalid input device
```

**Solution:**
- Check microphone permissions
- Verify audio device is connected
- Try different sample rate or device index

---

## 📚 References

### Technical Documentation
- [pynput Documentation](https://pynput.readthedocs.io/)
- [Cryptography Library](https://cryptography.io/)
- [Python Email Handling](https://docs.python.org/3/library/email.html)

### Security Research
- MITRE ATT&CK - Input Capture (T1056)
- OWASP Security Testing Guide
- NIST Cybersecurity Framework

### Legal Resources
- Computer Fraud and Abuse Act (CFAA)
- General Data Protection Regulation (GDPR)
- Electronic Communications Privacy Act (ECPA)

---

## 📝 Academic Report Template

If submitting this for coursework, include:

### Report Sections

1. **Introduction**
   - Objectives of the project
   - Threat landscape overview

2. **Technical Implementation**
   - Architecture diagram
   - Code walkthrough
   - Libraries and their purpose

3. **Security Analysis**
   - Attack surface evaluation
   - Detection methods
   - Mitigation strategies

4. **Testing Methodology**
   - VM setup description
   - Test scenarios
   - Results and observations

5. **Ethical Considerations**
   - Legal framework
   - Responsible disclosure
   - Privacy implications

6. **Conclusion**
   - Lessons learned
   - Future improvements
   - Defensive recommendations

---

## 👨‍🎓 Author

**Melissa Hall** (melissachall)
- Academic Project - Cybersecurity Research
- Date: November 2025

---

## 📄 License

This project is released for **educational purposes only** under the following conditions:

- Source code may be studied and analyzed for learning
- Modifications must maintain educational intent
- Commercial use is strictly prohibited
- Distribution must include this README and disclaimer
- Users accept full legal responsibility for their actions

**NO WARRANTY**: This software is provided "as is" without any guarantees.

---

## 🙏 Acknowledgments

- Educational institution cybersecurity program
- Open source community (pynput, Pillow, cryptography)
- Security research community for threat intelligence

---

**Remember: With great power comes great responsibility. Use this knowledge to defend, not to attack.**
