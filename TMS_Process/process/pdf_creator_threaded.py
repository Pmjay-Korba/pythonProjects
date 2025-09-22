import os
import re
import random
from io import BytesIO
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# --- Helper Functions ---

def find_images_in_folder(folder):
    exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    return sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in exts
    ])

def save_pdf_in_memory(images, max_size_bytes, start_quality=95, min_quality=30, step=5):
    quality = start_quality
    while quality >= min_quality:
        try:
            pil_images = [Image.open(img).convert("RGB") for img in images]
            if not pil_images:
                return None
            buffer = BytesIO()
            pil_images[0].save(
                buffer,
                format="PDF",
                save_all=True,
                append_images=pil_images[1:],
                quality=quality,
                optimize=True
            )
            size = buffer.tell()
            if size <= max_size_bytes:
                return buffer.getvalue()
        except Exception as e:
            print(f"⚠️ Error saving PDF: {e}")
            return None
        quality -= step
    return None

def create_pdf(group, pdf_path, max_bytes, lock=None):
    """Create PDF in memory and write to disk."""
    if not group:
        return None
    pdf_bytes = save_pdf_in_memory(group, max_bytes)
    if pdf_bytes:
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
    else:
        # fallback: save without strict compression
        pil_images = [Image.open(img).convert("RGB") for img in group]
        if pil_images:
            pil_images[0].save(pdf_path, save_all=True, append_images=pil_images[1:])
    if lock:
        lock.acquire()
    size_mb = os.path.getsize(pdf_path) / (1024 * 1024) if os.path.exists(pdf_path) else 0
    print(f"✅ Saved: {pdf_path} ({size_mb:.2f} MB)")
    if lock:
        lock.release()
    return pdf_path

# --- Main Function ---

def generate_fixed_pdfs_threaded(txt_file_path, num_pdfs=3, max_size_mb=0.95):
    """
    Generate exactly num_pdfs PDFs from images in the folder of txt_file_path.
    PDFs are balanced by total image bytes and compressed ≤ max_size_mb.
    """
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"TXT file not found: {txt_file_path}")

    folder = os.path.dirname(txt_file_path)
    all_images = find_images_in_folder(folder)
    if not all_images:
        print("⚠️ No images found in folder.")
        return []

    # Shuffle and get sizes
    images_with_sizes = [(img, os.path.getsize(img)) for img in all_images]
    random.shuffle(images_with_sizes)

    # Initialize PDF groups
    pdf_groups = [[] for _ in range(num_pdfs)]
    pdf_sizes = [0 for _ in range(num_pdfs)]

    # Size-based greedy assignment
    for img, size in sorted(images_with_sizes, key=lambda x: -x[1]):
        min_idx = pdf_sizes.index(min(pdf_sizes))
        pdf_groups[min_idx].append(img)
        pdf_sizes[min_idx] += size

    # Base PDF name
    parent_name = os.path.basename(folder)
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', parent_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)

    max_bytes = int(max_size_mb * 1024 * 1024)
    pdf_paths = []

    # Lock for thread-safe printing
    lock = Lock()

    # --- Threaded PDF creation ---
    with ThreadPoolExecutor(max_workers=min(num_pdfs, 8)) as executor:
        futures = []
        for idx, group in enumerate(pdf_groups):
            if not group:
                continue  # skip empty group
            pdf_path = os.path.join(folder, f"{safe_name}_{idx+1}.pdf")
            pdf_paths.append(pdf_path)
            futures.append(executor.submit(create_pdf, group, pdf_path, max_bytes, lock))
        # Wait for all threads
        for f in futures:
            f.result()

    # Duplicate PDFs to reach requested num_pdfs
    while len(pdf_paths) < num_pdfs:
        duplicate_pdf = pdf_paths[-1]
        new_pdf = os.path.join(folder, f"{safe_name}_{len(pdf_paths)+1}.pdf")
        with open(duplicate_pdf, "rb") as f_src, open(new_pdf, "wb") as f_dst:
            f_dst.write(f_src.read())
        pdf_paths.append(new_pdf)
        size_mb = os.path.getsize(new_pdf) / (1024 * 1024)
        print(f"✅ Duplicated: {new_pdf} ({size_mb:.2f} MB)")

    print(f"✅ Total PDFs generated: {len(pdf_paths)}")
    return pdf_paths

# --- User Input Wrapper ---

if __name__ == "__main__":
    txt_input = r"C:\Users\RAKESH\Desktop\SUNITA\IMG-20250823-WA0792.jpg"

    generate_fixed_pdfs_threaded(txt_input)
