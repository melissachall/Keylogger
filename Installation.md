# Installation Guide - MEL Keylogger

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (primary), Linux, macOS (partial support)
- **Python Version**: 3.8 or higher
- **RAM**: 256 MB minimum
- **Disk Space**: 100 MB for dependencies + storage for logs
- **Network**: Internet connection for email reporting

### Required Permissions
- Microphone access (for audio recording)
- File system write access
- Network access (SMTP port 587)
- Administrator rights (optional, for persistence feature)

---

## Installation Methods

### Method 1: Standard Installation (Recommended for Testing)

#### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
```cmd
python --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

#### Step 2: Create Project Directory

```bash
# Create and navigate to project folder
mkdir mel-keylogger
cd mel-keylogger

# Extract or copy project files here
```

#### Step 3: Set Up Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your prompt should now show `(venv)`.

#### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Platform-Specific Notes:**

**Windows:**
```cmd
# All dependencies should install normally
pip install -r requirements.txt
```

**Linux:**
```bash
# Install system dependencies first
sudo apt install portaudio19-dev python3-dev gcc

# Then install Python packages
pip install -r requirements.txt
```

**macOS:**
```bash
# Install portaudio via Homebrew
brew install portaudio

# Then install Python packages
pip install -r requirements.txt
```

#### Step 5: Configure Email

```bash
# Copy example configuration
cp keylogger.conf.example keylogger.conf

# Edit with your credentials
nano keylogger.conf  # or use your preferred editor
```

#### Step 6: Test Installation

```bash
python keylogger.py
```

Press `Ctrl+C` to stop after verifying it starts without errors.

---

### Method 2: System-Wide Installation (Not Recommended)

```bash
# Skip virtual environment
pip install -r requirements.txt
python keylogger.py
```

⚠️ **Warning**: May conflict with other Python packages.

---

## Troubleshooting Installation

### Issue: pip not found

```bash
# Windows
python -m ensurepip --upgrade

# Linux
sudo apt install python3-pip
```

### Issue: Permission denied (Linux/macOS)

```bash
# Use virtual environment instead of sudo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: pywin32 fails on Linux/macOS

```bash
# Edit requirements.txt and comment out:
# pywin32>=305

# Or install without Windows dependencies:
grep -v pywin32 requirements.txt | pip install -r /dev/stdin
```

### Issue: sounddevice installation fails

```bash
# Install system audio libraries first

# Ubuntu/Debian:
sudo apt install libportaudio2 portaudio19-dev

# Fedora:
sudo dnf install portaudio-devel

# macOS:
brew install portaudio

# Then retry:
pip install sounddevice
```

### Issue: "Microsoft Visual C++ required" (Windows)

Download and install:
- [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

Or install Build Tools:
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

---

## Verification Checklist

Run these commands to verify installation:

```bash
# Check Python version
python --version  # Should be 3.8+

# Check pip version
pip --version

# Verify pynput
python -c "from pynput import keyboard; print('pynput OK')"

# Verify Pillow
python -c "from PIL import ImageGrab; print('Pillow OK')"

# Verify cryptography
python -c "from cryptography.fernet import Fernet; print('cryptography OK')"

# Verify sounddevice
python -c "import sounddevice as sd; print('sounddevice OK')"

# Windows only - verify pywin32
python -c "import win32clipboard; print('pywin32 OK')"
```

All should print "OK" without errors.

---

## Email Provider Setup

### Gmail

1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password
3. Use in `keylogger.conf`:
```ini
[EMAIL]
address = yourname@gmail.com
password = xxxx xxxx xxxx xxxx
smtp_host = smtp.gmail.com
smtp_port = 587
```

### Outlook/Hotmail

```ini
[EMAIL]
address = yourname@outlook.com
password = your_regular_password
smtp_host = smtp.office365.com
smtp_port = 587
```

### Yahoo Mail

1. Generate App Password: https://login.yahoo.com/account/security
2. Configure:
```ini
[EMAIL]
address = yourname@yahoo.com
password = your_app_password
smtp_host = smtp.mail.yahoo.com
smtp_port = 587
```

---

## VM Setup (Recommended for Testing)

### Using VirtualBox

1. **Create VM:**
   - OS: Windows 10/11
   - RAM: 2 GB minimum
   - Disk: 20 GB

2. **Install Guest Additions** for clipboard sharing

3. **Network Settings:**
   - NAT (for internet access)
   - Or Host-Only (for isolated testing)

4. **Snapshot Before Testing:**
   ```
   VM → Snapshots → Take Snapshot
   ```

5. **Install Python and dependencies** inside VM

6. **Test keylogger** in isolated environment

---

## Next Steps

After successful installation:

1. ✅ Review `README.md` for usage instructions
2. ✅ Configure `keylogger.conf` with your email
3. ✅ Read `TESTING.md` for safe testing procedures
4. ✅ Review `ETHICS.md` for legal considerations
5. ✅ Run initial test: `python keylogger.py`

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate if active
deactivate

# Delete virtual environment folder
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### Remove Persistence (Windows)

If you enabled persistence, remove it:

```cmd
# Run as Administrator
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v WindowsUpdate /f

# Delete copied executable
del "%APPDATA%\svchost.exe"
```

---

## Support

For installation issues specific to this educational project, document:
- Operating system and version
- Python version (`python --version`)
- Error message (full text)
- Steps that failed

Include this information when asking your professor for assistance.

---

**Installation Date**: 2025-11-23
**Last Updated**: 2025-11-23
**Version**: 1.0
