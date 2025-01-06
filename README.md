# KeyLogger: Keystroke Logging and Contextual Window Tracking

## Overview

**KeyLogger** is a Python-based project that demonstrates how to capture keystrokes, track active windows, and log user activity for educational purposes. This project provides a hands-on example of basic keylogging functionality while emphasizing ethical use and security practices.

This project is intended for:
- Learning about Python's ability to interact with system-level events.
- Understanding the importance of ethical and secure programming practices.

## Key Features

- **Cross-Platform Support**: Works on Windows, macOS, and Linux.
- **Contextual Window Tracking**: Captures and logs the title of the currently active window.
- **Keystroke Logging**: Logs keystrokes in a readable format with common key substitutions (e.g., `[ENTER]`, `[BACKSPACE]`).
- **Periodic Log Rotation**: Writes logs to temporary files and sends them via email.
- **Environment-Based Configuration**: Securely handles email credentials using environment variables.

## How It Works

1. **Active Window Tracking**: The script identifies and logs the currently active window's title whenever it changes.
2. **Keystroke Logging**: Captures keystrokes in real-time and substitutes special keys for readability.
3. **Log Management**: Periodically writes logs to a file and emails them to the configured address.
4. **Clean-Up**: Deletes log files after successful email delivery to ensure privacy and security.

## Setup

### Requirements

- Python 3.7+
- Required libraries (install using `pip install -r requirements.txt`):
  - `pynput`
  - `requests`
  - `python-dotenv`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/keylogger-project
   cd keylogger-project
   ```

2. Create a `.env` file in the root directory:
   ```plaintext
   EMAIL_ADDRESS=your_email@example.com
   EMAIL_PASSWORD=your_password
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python keylogger.py
   ```

## Ethical Use Disclaimer

This project is intended strictly for educational purposes. Unauthorized use of this software to monitor or log user activity is illegal and unethical. Always obtain explicit consent before deploying this software in any environment.

## Key Components

### Code Highlights

- **Window Tracking**:
  The `get_active_window` function retrieves the title of the active window using platform-specific methods.

- **Keystroke Capture**:
  The `on_press` function captures and logs keystrokes, substituting special keys (e.g., `[ENTER]`) for better readability.

- **Email Integration**:
  The `send_email` function securely sends log files as email attachments using SMTP.

- **Periodic Logging**:
  The `periodic_email` function rotates logs every 10 minutes and sends them via email.

### Configuration

- **Environment Variables**:
  Store sensitive credentials (e.g., email and password) in a `.env` file to ensure security and portability.

- **Log File Management**:
  Log files are written to a temporary directory (`temp_logs`) and are automatically deleted after being emailed.

## Future Improvements

- **Encryption**: Add encryption for log files before sending them via email.
- **Delivery Methods**: Support alternative delivery options (e.g., cloud storage).
- **Enhanced User Interface**: Provide a GUI for easier setup and configuration.
- **Error Handling**: Improve error handling and logging for better reliability.

---

For questions or contributions, feel free to create an issue or submit a pull request on the repository.
