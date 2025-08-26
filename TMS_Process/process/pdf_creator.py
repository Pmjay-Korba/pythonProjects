import os
import time
from io import BytesIO
from PIL import Image
import os
import random
import re
import img2pdf
from pathlib import Path


from EHOSP.ehospital_proper.colour_print_ehosp import ColourPrint
from EHOSP.tk_ehosp.alert_boxes import error_tk_box
from dkbssy.utils.colour_prints import message_box


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

    # ---- Sanitize parent_name: replace non-alphanumeric with spaces ----
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', parent_name).strip()
    # Collapse multiple spaces into one
    safe_name = re.sub(r'\s+', ' ', safe_name)

    # ---- Part 1: strictly < 0.95 MB ----
    part1_pdf = os.path.join(first_folder, f"{safe_name}1.pdf")
    if part1_imgs:
        ok1 = save_pdf(part1_imgs, part1_pdf, max_size=int(0.95 * 1024 * 1024))  # 0.95 MB
        if ok1:
            size1 = os.path.getsize(part1_pdf) / (1024 * 1024)
            print(f"✅ {part1_pdf} ({size1:.2f} MB)")
        else:
            print(f"⚠️ {part1_pdf} could not be compressed under 0.95 MB")

    # ---- Part 2: strictly < 4.95 MB ----
    part2_pdf = os.path.join(first_folder, f"{safe_name}2.pdf")
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


def custom_size_pdf_from_txt_list( txt_file_paths, max_size_mb=4.95 ):
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
        return None

    # ---- Shuffle before saving ----
    random.shuffle(all_images)

    # Use the name of the first folder (from first TXT) as base name
    first_folder = os.path.dirname(txt_file_paths[0])
    parent_name = os.path.basename(first_folder)

    # ---- Sanitize parent_name: replace non-alphanumeric with spaces ----
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', parent_name).strip()
    # Collapse multiple spaces into one
    safe_name = re.sub(r'\s+', ' ', safe_name)


    # ---- One PDF with given size ----
    pdf_path = os.path.join(first_folder, f"{safe_name}.pdf")
    ok = save_pdf(all_images, pdf_path, max_size=int(max_size_mb * 1024 * 1024))

    if ok:
        size = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"✅ {pdf_path} ({size:.2f} MB, limit {max_size_mb:.2f} MB)")
        return pdf_path
    else:
        print(f"⚠️ {pdf_path} could not be compressed under {max_size_mb:.2f} MB")
        ColourPrint.print_yellow(message_box("GENERATING BACKUP PDF ..."))

        return save_pdf_backup(txt_file_paths=txt_file_paths, max_size_mb=max_size_mb)



def save_pdf_backup(txt_file_paths, max_size_mb=0.95):
    """
    Fast backup PDF from images in folders of given TXT files.
    Stops before exceeding max_size_mb.
    Returns path to PDF if created, else None.
    """
    if not txt_file_paths:
        print("⚠️ No TXT files provided")
        return None

    all_images = []
    for txt_path in txt_file_paths:
        folder = os.path.dirname(txt_path)
        images = [str(p) for p in Path(folder).glob("*.jpg")] + \
                 [str(p) for p in Path(folder).glob("*.png")] + \
                 [str(p) for p in Path(folder).glob("*.jpeg")]
        all_images.extend(images)

    if not all_images:
        print("⚠️ No images found in any folder")
        return None

    random.shuffle(all_images)

    first_folder = os.path.dirname(txt_file_paths[0])
    parent_name = os.path.basename(first_folder)
    safe_name = re.sub(r'[^A-Za-z0-9]+', ' ', parent_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)

    output_pdf = os.path.join(first_folder, f"{safe_name}_backup.pdf")
    max_size = int(max_size_mb * 1024 * 1024)

    included = []
    for img in all_images:
        test_list = included + [img]
        pdf_bytes = img2pdf.convert(test_list)
        if len(pdf_bytes) <= max_size:
            included.append(img)
        else:
            break

    if not included:
        print("⚠️ Could not fit any images into backup PDF")
        return None

    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(included))

    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"✅ Backup PDF saved: {output_pdf} ({size_mb:.2f} MB, limit {max_size_mb:.2f} MB)")
    return output_pdf

# if __name__ == "__main__":
    # txt_path = r"C:\Users\HP\Desktop\test\1011550154.txt"
    # generate_pdfs_from_txt(txt_path)
    # time.sleep(3)
    # delete_pdfs_from_txt(txt_path)
