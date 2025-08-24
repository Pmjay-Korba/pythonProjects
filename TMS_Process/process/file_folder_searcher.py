import os
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


class ProjectPaths:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    FILE_PATH = Path(__file__).resolve()
    DOWNLOAD_DIR = PROJECT_ROOT / "TMS_Process" / "downloads"
    CACHE_FILE = PROJECT_ROOT / "TMS_Process" / "downloads" / "file_search_cache.json"

def is_skipped(path: Path) -> bool:
    skip_dirs = [
        "$Recycle.Bin",
        "System Volume Information",
        "Windows",
        "Program Files",
        "Program Files (x86)"
    ]
    return any(skip_dir.lower() in str(path).lower() for skip_dir in skip_dirs)


def normalize_filename(name: str) -> str:
    """Trim spaces and normalize filename key for cache."""
    return name.strip()


def is_numeric_txt(name: str) -> bool:
    """Check if file is .txt and starts with digits (ignoring spaces)."""
    base = normalize_filename(name)
    return base.lower().endswith(".txt") and base.split(".")[0].strip().isdigit()


def scan_folder_for_txt(folder: Path) -> dict[str, list[str]]:
    """Recursively scan folder and collect numeric .txt files."""
    found = {}
    try:
        with os.scandir(folder) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False):
                    if not is_skipped(Path(entry.path)):
                        sub_found = scan_folder_for_txt(Path(entry.path))
                        for k, v in sub_found.items():
                            found.setdefault(k, []).extend(v)
                elif entry.is_file(follow_symlinks=False) and is_numeric_txt(entry.name):
                    key = normalize_filename(entry.name)
                    found.setdefault(key, []).append(str(Path(entry.path)))
    except (PermissionError, FileNotFoundError):
        pass
    return found


def scan_drive_for_txt(drive: str, max_workers: int = 8) -> dict[str, list[str]]:
    """Scan a drive by parallelizing top-level folders for numeric .txt files."""
    drive_root = Path(f"{drive}:/")
    found = {}

    print(f"Scanning {drive_root} ...")
    if not drive_root.exists():
        return found

    try:
        with os.scandir(drive_root) as it:
            top_folders = [Path(entry.path) for entry in it if entry.is_dir(follow_symlinks=False)]
    except PermissionError:
        top_folders = []

    # Also check directly under drive root
    for entry in drive_root.iterdir():
        if entry.is_file() and is_numeric_txt(entry.name):
            key = normalize_filename(entry.name)
            found.setdefault(key, []).append(str(entry))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_folder_for_txt, folder): folder for folder in top_folders}
        for future in as_completed(futures):
            try:
                sub_found = future.result()
                for k, v in sub_found.items():
                    found.setdefault(k, []).extend(v)
            except Exception as e:
                print(f"[ERROR] Folder scan failed in {futures[future]}: {e}")

    return found


# ------------------- CACHE LAYER -------------------

def load_cache() -> dict:
    if ProjectPaths.CACHE_FILE.exists():
        try:
            with open(ProjectPaths.CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict):
    try:
        with open(ProjectPaths.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save cache: {e}")


def search_file_all_drives(filename: str, max_workers: int = 6, refresh_cache: bool = False) -> list[str]:
    """
    Search all drives, update cache with ALL numeric .txt files found.
    - If refresh_cache=False (default), use cache first.
    - If refresh_cache=True, force a full rescan.
    """
    filename = normalize_filename(f"{filename}.txt")

    # 🔹 Load existing cache
    cache = load_cache()

    # If not forcing rescan and file exists in cache → return cached result
    if not refresh_cache and filename in cache:
        print(f"[CACHE] Found {len(cache[filename])} cached matches for {filename}")
        return cache[filename]

    # Otherwise, perform full scan
    start_time = time.perf_counter()
    drives = [d for d in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:/")]
    found_all = {}

    with ThreadPoolExecutor(max_workers=min(len(drives), max_workers)) as executor:
        futures = {executor.submit(scan_drive_for_txt, d): d for d in drives}
        for future in as_completed(futures):
            try:
                sub_found = future.result()
                for k, v in sub_found.items():
                    found_all.setdefault(k, []).extend(v)
            except Exception as e:
                print(f"[ERROR] Drive scan failed: {e}")

    elapsed = time.perf_counter() - start_time
    print(f"[SEARCH] Indexed {len(found_all)} numeric .txt files across {len(drives)} drives (took {elapsed:.2f} sec)")

    # 🔹 Merge new findings into cache
    cache.update(found_all)
    save_cache(cache)

    # Return requested file paths
    return cache.get(filename, [])


# ------------------- MAIN -------------------

if __name__ == "__main__":
    # first run will scan, later runs will use cache instantly
    result = search_file_all_drives("1010869893", refresh_cache=False)
    print(result)
