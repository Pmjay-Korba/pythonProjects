import os
import sys
import re
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta

# Ensure Unicode print works on Windows
sys.stdout.reconfigure(encoding='utf-8')

# --------------------- Log file ---------------------
LOG_FILE = os.path.join(os.path.dirname(__file__), "pdf_created.log")

# --------------------- Cleanup old PDFs ---------------------
def cleanup_old_pdfs(hours=1):
    if not os.path.exists(LOG_FILE):
        return
    now = datetime.now()
    lines_to_keep = []
    deleted_count = 0

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        try:
            timestamp_str, pdf_path = line.strip().split("|", 1)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            if now - timestamp > timedelta(hours=hours):
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                    deleted_count += 1
            else:
                lines_to_keep.append(line)
        except Exception:
            lines_to_keep.append(line)  # Keep malformed lines

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines_to_keep)

    if deleted_count:
        print(f"🗑️ Deleted {deleted_count} old PDF(s).")

# --------------------- Log newly created PDF ---------------------
def log_pdf_created(pdf_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp}|{pdf_path}\n")
    except Exception as e:
        print(f"❌ Failed to write log: {e}")

# --------------------- Clean command-line arguments ---------------------
def clean_args(args):
    cleaned = []
    for a in args:
        a = a.strip().strip('"').strip("'")
        if os.path.exists(a):
            cleaned.append(a)
    return cleaned

# --------------------- Main PDF creation ---------------------
def make_pdf_from_selection(image_paths):
    image_paths = clean_args(image_paths)

    if not image_paths:
        print("⚠️ No image files selected.")
        return

    exts = (".jpg", ".jpeg", ".png")
    image_paths = [p for p in image_paths if p.lower().endswith(exts) and os.path.exists(p)]

    if not image_paths:
        print("⚠️ No valid image files found.")
        return

    # Sort alphabetically
    image_paths.sort()

    # Open images
    images = [Image.open(p).convert("RGB") for p in image_paths]

    # --------------------- Determine PDF path ---------------------
    first_folder = os.path.dirname(image_paths[0])
    folder_name = os.path.basename(first_folder.rstrip("\\/"))
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', folder_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)

    # Add timestamp to avoid overwriting: HHMMSS
    timestamp_str = datetime.now().strftime("%H%M%S")
    pdf_name = f"{safe_name}_{timestamp_str}.pdf"
    pdf_path = os.path.join(first_folder, pdf_name)

    # --------------------- Compress PDF under ~900KB ---------------------
    target_limit = 0.9  # MB
    quality = 95
    scale = 1.0

    while True:
        buf = BytesIO()
        resized = [
            img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))))
            for img in images
        ]
        resized[0].save(buf, format="PDF", save_all=True, append_images=resized[1:], quality=quality)
        size_mb = buf.getbuffer().nbytes / (1024 * 1024)
        if size_mb <= target_limit or quality <= 20:
            with open(pdf_path, "wb") as f:
                f.write(buf.getvalue())
            break
        quality -= 5
        scale *= 0.9

    print(f"✅ PDF created: {pdf_path} ({os.path.getsize(pdf_path)/(1024*1024):.2f} MB)")

    # Log the created PDF
    log_pdf_created(pdf_path)

# --------------------- Entry point ---------------------
if __name__ == "__main__":
    print(f"📥 Raw args received: {sys.argv[1:]}")

    # 1️⃣ Cleanup PDFs older than 1 hour
    cleanup_old_pdfs(hours=1)

    # 2️⃣ Create new PDF
    make_pdf_from_selection(sys.argv[1:])
