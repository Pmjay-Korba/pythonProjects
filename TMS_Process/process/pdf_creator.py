import os
import time
from io import BytesIO
from PIL import Image
import os
import random

from EHOSP.tk_ehosp.alert_boxes import error_tk_box


def find_images_in_folder(folder):
    exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    return sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in exts
    ])

def save_pdf(images, output_pdf, max_size, start_quality=95, min_quality=30, step=5):
    """
    Save images into a PDF and compress until under max_size (bytes).
    Returns True if success, False otherwise.
    """
    quality = start_quality

    while quality >= min_quality:
        try:
            pil_images = [Image.open(img).convert("RGB") for img in images]

            # Write to memory buffer
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
            if size <= max_size:
                # ✅ Only save if size requirement is met
                with open(output_pdf, "wb") as f:
                    f.write(buffer.getvalue())
                return True

        except Exception as e:
            print(f"⚠️ Error while saving PDF: {e}")
            return False

        # Reduce quality and retry
        quality -= step

    return False

def generate_pdfs_from_txt_list(txt_file_paths):
    if not txt_file_paths:
        print("No TXT files provided")
        err_msg = f'The folder does not contain the text file. Please check'
        error_tk_box(error_title="File Not Found", error_message=err_msg)
        raise FileNotFoundError(err_msg)

    all_images = []

    # Collect all images from folders containing the TXT files
    for txt_path in txt_file_paths:
        folder = os.path.dirname(txt_path)
        images = find_images_in_folder(folder)
        all_images.extend(images)

    if not all_images:
        print("No images found in any folder")
        return []

        # ---- Shuffle before splitting ----
    random.shuffle(all_images)

    # ---- Split into ratio 1:5 ----
    n = len(all_images)
    split_index = n // 6  # 1:5 ratio → first 1/6th, remaining 5/6th
    part1_imgs = all_images[:split_index]
    part2_imgs = all_images[split_index:]

    # Use the name of the first folder (from first TXT) as base name
    first_folder = os.path.dirname(txt_file_paths[0])
    parent_name = os.path.basename(first_folder)

    # ---- Part 1: strictly < 0.95 MB ----
    part1_pdf = os.path.join(first_folder, f"{parent_name}1.pdf")
    if part1_imgs:
        ok1 = save_pdf(part1_imgs, part1_pdf, max_size=int(0.95 * 1024 * 1024))  # 0.95 MB
        if ok1:
            size1 = os.path.getsize(part1_pdf) / (1024 * 1024)
            print(f"✅ {part1_pdf} ({size1:.2f} MB)")
        else:
            print(f"⚠️ {part1_pdf} could not be compressed under 0.95 MB")

    # ---- Part 2: strictly < 4.95 MB ----
    part2_pdf = os.path.join(first_folder, f"{parent_name}2.pdf")
    if part2_imgs:
        ok2 = save_pdf(part2_imgs, part2_pdf, max_size=int(4.95 * 1024 * 1024))  # 4.95 MB
        if ok2:
            size2 = os.path.getsize(part2_pdf) / (1024 * 1024)
            print(f"✅ {part2_pdf} ({size2:.2f} MB)")
        else:
            print(f"⚠️ {part2_pdf} could not be compressed under 4.95 MB")
    else:
        part2_pdf = None

    return part1_pdf, part2_pdf

def delete_pdfs_from_txt(txt_file_path):
    """
    Deletes only the PDFs generated from the given txt file,
    following the naming convention <parent_folder>1.pdf and <parent_folder>2.pdf.
    Only checks the first folder listed in the TXT (where PDFs were saved).
    """
    # Read the first folder path from the TXT file
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        first_folder = None
        for line in f:
            line = line.strip()
            if line:
                first_folder = line
                break

    if not first_folder:
        print("⚠️ No folder paths found in TXT.")
        return

    parent_name = os.path.basename(first_folder)
    pdf_paths = [
        os.path.join(first_folder, f"{parent_name}1.pdf"),
        os.path.join(first_folder, f"{parent_name}2.pdf")
    ]

    for pdf in pdf_paths:
        if os.path.exists(pdf):
            os.remove(pdf)
            print(f"🗑️ Deleted {pdf}")
        else:
            print(f"⚠️ File not found: {pdf}")


def delete_pdf(pdf_path):
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"✅ Deleted: {pdf_path}")
    else:
        print(f"⚠️ File does not exist: {pdf_path}")


# if __name__ == "__main__":
    # txt_path = r"C:\Users\HP\Desktop\test\1011550154.txt"
    # generate_pdfs_from_txt(txt_path)
    # time.sleep(3)
    # delete_pdfs_from_txt(txt_path)
