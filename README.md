# Anydesk_Forensic

---

```markdown
# AnyDesk Trace & Config Viewer

A powerful forensic tool designed to analyze and visualize AnyDesk trace and configuration files. This tool simplifies the process of extracting meaningful insights from log files such as `ad.trace`, `ad_svc.trace`, `connection_trace.txt`, and `system.conf`.

## 🔍 Features

- Parse and view contents of:
  - `ad.trace`
  - `ad_svc.trace`
  - `connection_trace.txt`
  - `system.conf`
- Analyze log patterns like connection attempts, errors, and timestamps
- Filter log entries by keyword, date, or type
- Export parsed data to CSV or Excel (coming soon)
- Toggle between Light and Dark mode for comfortable viewing
- IP Grabber tool to extract IP addresses from logs (planned)

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/anydesk-trace-viewer.git
cd anydesk-trace-viewer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python anydesk_forensic.py
```

## 🖼️ Screenshot

Example output after analyzing `ad.trace`:

![image](https://github.com/user-attachments/assets/f55f0237-fb3c-4a64-ac43-b86d5a109453)

![image](https://github.com/user-attachments/assets/b6eb3373-9649-41b8-9e2c-9ec19d196b86) 

_Example output of parsed `ad.trace` log data. This is sample data for demonstration purposes only._

## ⚙️ Usage

- Click on a log file button to load and view its contents.
- Use the built-in filters to search specific keywords or timestamps.
- Toggle Dark Mode for better readability in low-light conditions.

## 📁 Supported Files

- `ad.trace` – Client trace logs
- `ad_svc.trace` – Service-related logs
- `connection_trace.txt` – Connection logs
- `system.conf` – Configuration file

## 📌 Disclaimer

This tool is meant for forensic and educational purposes. Make sure you have permission to analyze AnyDesk logs on the device you’re working with.

Let me know if you’d like to customize the contact section or add a license!
