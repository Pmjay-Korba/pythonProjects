import os
import threading
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


# --- PDF generation (always ≤0.95MB) ---
def make_pdf_from_folder(folder):
    exts = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    if not files:
        print("⚠️ No images found in folder.")
        return

    files.sort()
    images = [Image.open(os.path.join(folder, f)).convert("RGB") for f in files]

    # --- Sanitize folder name ---
    parent_name = os.path.basename(folder.rstrip("\\/"))
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', parent_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)

    pdf_path = os.path.join(folder, f"{safe_name}.pdf")

    strict_limit = 0.95  # MB
    quality = 95
    scale_ratio = 1.0

    while True:
        buffer = BytesIO()
        temp_images = [
            img.resize((max(1, int(img.size[0] * scale_ratio)),
                        max(1, int(img.size[1] * scale_ratio))))
            for img in images
        ]

        temp_images[0].save(
            buffer,
            format="PDF",
            save_all=True,
            append_images=temp_images[1:],
            quality=quality
        )
        size_mb = buffer.getbuffer().nbytes / (1024 * 1024)

        if size_mb <= strict_limit or quality <= 10:
            with open(pdf_path, "wb") as f:
                f.write(buffer.getvalue())
            break

        # Reduce quality & scale gradually
        quality -= 5
        scale_ratio *= 0.95

    print(f"✅ PDF created: {pdf_path} ({os.path.getsize(pdf_path)/(1024*1024):.2f} MB)")
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


# --- Hotkey listener ---
def listen_hotkey():
    def run_task():
        folder = get_active_explorer_path()
        if folder:
            make_pdf_from_folder(folder)
        else:
            print("⚠️ No active Explorer folder detected.")

    keyboard.add_hotkey("ctrl+shift+alt+p", lambda: threading.Thread(target=run_task, daemon=True).start())
    keyboard.wait()


if __name__ == "__main__":
    print("✅ PDF hotkey script running. Press Ctrl+Shift+Alt+P in Explorer folder...")
    listen_hotkey()
