import os
import sys
import re
from io import BytesIO
from PIL import Image

# Ensure UTF-8 console output
sys.stdout.reconfigure(encoding='utf-8')


def clean_args(args):
    cleaned = []
    for a in args:
        # Remove wrapping quotes or slashes that batch might add
        a = a.strip().strip('"').strip("'").strip("\\")
        if os.path.exists(a):
            cleaned.append(a)
    return cleaned


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

    images = [Image.open(p).convert("RGB") for p in image_paths]

    first_folder = os.path.dirname(image_paths[0])
    folder_name = os.path.basename(first_folder.rstrip("\\/"))
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', folder_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)
    pdf_path = os.path.join(first_folder, f"{safe_name}.pdf")

    # Compress PDF under ~900KB
    target_limit = 0.9  # MB
    quality = 95
    scale = 1.0

    while True:
        buf = BytesIO()
        resized = [
            img.resize((int(img.width * scale), int(img.height * scale)))
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


if __name__ == "__main__":
    print(f"📥 Raw args received: {sys.argv[1:]}")
    make_pdf_from_selection(sys.argv[1:])
