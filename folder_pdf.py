import os
import threading
import tkinter as tk
from PIL import Image
import keyboard
import win32gui
import win32com.client
import pythoncom
import re
from io import BytesIO
import pyperclip


def copy_to_clipboard(text):
    pyperclip.copy(text)
    print(f"📋 PDF path copied to clipboard: {text}")


# --- PDF generation using BytesIO ---
def make_pdf_from_folder(folder, max_size_mb=None):
    exts = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    if not files:
        print("No images found in folder.")
        return

    files.sort()
    images = [Image.open(os.path.join(folder, f)).convert("RGB") for f in files]

    # --- Sanitize folder name for PDF ---
    parent_name = os.path.basename(folder.rstrip("\\/"))
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', parent_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)

    pdf_path = os.path.join(folder, f"{safe_name}.pdf")


    # Strict limits
    strict_limit = None
    if max_size_mb == 1:
        strict_limit = 0.95
    elif max_size_mb == 2:
        strict_limit = 1.95
    elif max_size_mb == 5:
        strict_limit = 4.95

    # Start adaptive compression loop using BytesIO
    quality = 95
    scale_ratio = 1.0

    while True:
        buffer = BytesIO()
        temp_images = []
        for img in images:
            w, h = img.size
            img_resized = img.resize((max(1, int(w*scale_ratio)), max(1, int(h*scale_ratio))))
            temp_images.append(img_resized)

        temp_images[0].save(buffer, format="PDF", save_all=True, append_images=temp_images[1:], quality=quality)
        size_mb = buffer.getbuffer().nbytes / (1024*1024)

        if strict_limit is None or size_mb <= strict_limit or quality <= 10:
            # Write final PDF to disk
            with open(pdf_path, "wb") as f:
                f.write(buffer.getvalue())
            break

        # Reduce quality slightly
        quality -= 5
        # Reduce dimensions proportionally
        scale_ratio *= 0.95  # shrink 5% per iteration

    print(f"✅ PDF created: {pdf_path} ({os.path.getsize(pdf_path)/(1024*1024):.2f} MB)")
    # --- Copy PDF path to clipboard ---
    copy_to_clipboard(pdf_path)

# --- Get active Explorer folder ---
def get_active_explorer_path():
    pythoncom.CoInitialize()
    try:
        shell = win32com.client.Dispatch("Shell.Application")
        hwnd = win32gui.GetForegroundWindow()
        for window in shell.Windows():
            try:
                if int(window.HWND) == hwnd:
                    return window.Document.Folder.Self.Path
            except Exception:
                continue
    finally:
        pythoncom.CoUninitialize()
    return None

# --- Popup menu ---
def popup():
    folder = get_active_explorer_path()
    if not folder:
        print("No active Explorer folder detected.")
        return

    root = tk.Tk()
    root.title("Make PDF")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    # Center window
    window_width, window_height = 200, 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2) - 50
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def run_and_close(size):
        make_pdf_from_folder(folder, size)
        root.destroy()

    tk.Button(root, text="PDF ≤ 1 MB", command=lambda: run_and_close(1)).pack(pady=5, fill="x")
    tk.Button(root, text="PDF ≤ 2 MB", command=lambda: run_and_close(2)).pack(pady=5, fill="x")
    tk.Button(root, text="PDF ≤ 5 MB", command=lambda: run_and_close(5)).pack(pady=5, fill="x")
    tk.Button(root, text="✕ Close", command=root.destroy, fg="red").pack(pady=5, fill="x")

    root.mainloop()

# --- Listen to hotkey ---
def listen_hotkey():
    keyboard.add_hotkey("ctrl+shift+alt+p", lambda: threading.Thread(target=popup).start())
    keyboard.wait()

if __name__ == "__main__":
    print("✅ PDF hotkey script running. Press Ctrl+Shift+Alt+P in Explorer folder...")
    listen_hotkey()

# adde