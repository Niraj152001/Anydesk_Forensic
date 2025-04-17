import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, Canvas, Frame, Scrollbar, Toplevel
from PIL import Image, ImageTk
import logging
import pandas as pd
import argparse
import re

is_dark_mode = False  # Global state to track current theme


# ---------------------- Logging Setup ----------------------

logging.basicConfig(filename='anydesk_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)

# ---------------------- Parsing Functions ----------------------

def get_anydesk_folder():
    user_profile = os.environ.get('USERPROFILE') or os.environ.get('HOME')
    path = Path(user_profile) / 'AppData' / 'Roaming' / 'AnyDesk'
    if path.exists():
        log_info(f"AnyDesk folder found at: {path}")
        return path
    else:
        log_error("AnyDesk folder not found.")
        return None

def parse_trace_file(filepath):
    lines = []
    try:
        for line in Path(filepath).read_text(errors='ignore').splitlines():
            low = line.lower()
            if any(keyword in low for keyword in ('connected', 'rejected', 'closed', 'session', 'error')):
                lines.append(line.strip())
    except Exception as e:
        log_error(f"Error reading {filepath}: {e}")
        lines.append(f"[!] Error reading {filepath}: {e}")
    return lines

def parse_system_conf(filepath):
    config = {}
    try:
        lines = Path(filepath).read_text(errors='ignore').splitlines()
        current_key = None
        current_value = []

        for line in lines:
            line = line.strip()
            if '=' in line:
                if current_key:
                    config[current_key] = '\n'.join(current_value).strip()
                key, val = line.split('=', 1)
                current_key = key.strip()
                current_value = [val.strip()]
            elif current_key:
                current_value.append(line.strip())

        if current_key:
            config[current_key] = '\n'.join(current_value).strip()

    except Exception as e:
        log_error(f"Error parsing system.conf: {e}")
        config['error'] = f"Error parsing system.conf: {e}"
    return config

# ---------------------- Export Functions ----------------------

def export_to_csv(data, filename='anydesk_report.csv'):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        log_info(f"Data exported to {filename}.")
    except Exception as e:
        log_error(f"Error exporting to CSV: {e}")

def export_to_excel(data, filename='anydesk_report.xlsx'):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        log_info(f"Data exported to {filename}.")
    except Exception as e:
        log_error(f"Error exporting to Excel: {e}")

# ---------------------- Highlighting Feature ----------------------

def highlight_text():
    output_box.tag_remove("ip", "1.0", tk.END)
    output_box.tag_remove("keyword", "1.0", tk.END)
    output_box.tag_remove("timestamp", "1.0", tk.END)

    patterns = {
        "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "timestamp": r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2})\b",
        "keyword": r"\b(connected|rejected|closed|session|error|disconnect|failed|success)\b"
    }

    for tag, pattern in patterns.items():
        start = "1.0"
        while True:
            match = output_box.search(pattern, start, stopindex=tk.END, regexp=True)
            if not match:
                break
            end = f"{match}+{len(output_box.get(match, match + ' wordend'))}c"
            output_box.tag_add(tag, match, end)
            start = end

    output_box.tag_config("ip", foreground="skyblue")
    output_box.tag_config("keyword", foreground="orange red", font=("Consolas", 10, "bold"))
    output_box.tag_config("timestamp", foreground="gray")

# ---------------------- GUI Task Functions ----------------------

def show_log_file(filename, parser_func, header):
    output_box.delete('1.0', tk.END)
    folder = get_anydesk_folder()
    if not folder:
        messagebox.showerror("Error", "AnyDesk folder not found.")
        return
    path = folder / filename
    if not path.exists():
        output_box.insert(tk.END, f"[-] {filename} not found.\n")
        log_error(f"{filename} not found.")
        return
    output_box.insert(tk.END, header)
    parsed_data = parser_func(path)
    if isinstance(parsed_data, dict):
        for key, value in parsed_data.items():
            output_box.insert(tk.END, f"{key} = {value}\n")
    else:
        for ln in parsed_data:
            output_box.insert(tk.END, ln + "\n")
    highlight_text()

def show_ad_trace():
    show_log_file('ad.trace', parse_trace_file, "[+] Contents of ad.trace:\n\n")

def show_ad_svc_trace():
    show_log_file('ad_svc.trace', parse_trace_file, "[+] Contents of ad_svc.trace:\n\n")

def show_connection_trace():
    show_log_file('connection_trace.txt', lambda p: Path(p).read_text(errors='ignore').splitlines(),
                  "[+] Contents of connection_trace.txt:\n\n")

def show_system_conf():
    show_log_file('system.conf', parse_system_conf, "[+] Contents of system.conf:\n\n")

def show_thumbnails():
    folder = get_anydesk_folder()
    if not folder:
        messagebox.showerror("Error", "AnyDesk folder not found.")
        return
    thumb_dir = folder / 'thumbnails'
    if not thumb_dir.exists() or not thumb_dir.is_dir():
        messagebox.showinfo("Info", "No thumbnails directory found.")
        return
    images = list(thumb_dir.glob('*.png')) + list(thumb_dir.glob('*.jpg')) + list(thumb_dir.glob('*.jpeg'))
    if not images:
        messagebox.showinfo("Info", "No image files found in thumbnails folder.")
        return
    win = Toplevel(app)
    win.title("Thumbnails Viewer")
    canvas = Canvas(win)
    scrollbar = Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    thumb_size = (150, 150)
    for img_path in images:
        try:
            img = Image.open(img_path)
            img.thumbnail(thumb_size)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(scroll_frame, image=photo)
            lbl.image = photo
            lbl.pack(padx=5, pady=5)
        except Exception as e:
            tk.Label(scroll_frame, text=f"Error loading {img_path.name}: {e}").pack()

def toggle_dark_mode():
    global is_dark_mode
    if not is_dark_mode:
        app.configure(bg='#1e1e1e')
        output_box.config(bg='#2d2d2d', fg='#ffffff', insertbackground='white')
        btn_frame.config(bg='#1e1e1e')
        toggle_button.config(bg='#333333', fg='white')
        for child in btn_frame.winfo_children():
            child.config(bg='#333333', fg='white')
        is_dark_mode = True
    else:
        app.configure(bg='#f0f0f0')
        output_box.config(bg='white', fg='black', insertbackground='black')
        btn_frame.config(bg='#f0f0f0')
        toggle_button.config(bg='SystemButtonFace', fg='black')
        for child in btn_frame.winfo_children():
            child.config(bg='SystemButtonFace', fg='black')
        is_dark_mode = False


# ---------------------- CLI Functionality ----------------------

def parse_args():
    parser = argparse.ArgumentParser(description="AnyDesk Forensics Tool")
    parser.add_argument('--trace', help="Show trace file", choices=['ad.trace', 'ad_svc.trace', 'connection_trace.txt'])
    parser.add_argument('--system_conf', help="Show system.conf", action='store_true')
    parser.add_argument('--export_csv', help="Export to CSV", action='store_true')
    parser.add_argument('--export_excel', help="Export to Excel", action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.trace:
        show_log_file(args.trace, parse_trace_file, f"[+] Contents of {args.trace}:\n\n")
    if args.system_conf:
        show_system_conf()
    if args.export_csv:
        export_to_csv(parsed_data)
    if args.export_excel:
        export_to_excel(parsed_data)

# ---------------------- GUI Setup ----------------------

app = tk.Tk()
app.title("AnyDesk Trace & Config Viewer")
app.geometry("900x600")

btn_frame = tk.Frame(app)
btn_frame.pack(fill='x', pady=5)

for text, cmd in [
    ("ad.trace", show_ad_trace),
    ("ad_svc.trace", show_ad_svc_trace),
    ("connection_trace.txt", show_connection_trace),
    ("system.conf", show_system_conf),
    ("Thumbnails", show_thumbnails)
]:
    tk.Button(btn_frame, text=text, width=20, command=cmd).pack(side='left', padx=5)

output_box = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Consolas", 10))
output_box.pack(fill='both', expand=True, padx=5, pady=5)

toggle_button = tk.Button(app, text="Toggle Dark Mode", command=toggle_dark_mode)
toggle_button.pack(pady=5)

app.mainloop()

if __name__ == "__main__":
    main()
