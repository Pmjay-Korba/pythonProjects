from pathlib import Path
import os

def test_drive_letter_change(abs_path: str) -> str | None:
    """
    Test if a cached absolute path still exists.
    If not, check same path on all drive letters (A–Z).
    Print both original and resolved paths.
    Return the working path if found, else None.
    """
    print(f"[CACHE] Original cached path: {abs_path}")

    p = Path(abs_path)
    if p.exists():
        print(f"[OK] File exists at cached path")
        return str(p)

    drive, rest = os.path.splitdrive(abs_path)
    if not rest:
        print("[WARN] Invalid cached path format")
        return None

    for d in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        candidate = f"{d}:{rest}"
        if Path(candidate).exists():
            print(f"[FIX] File found at new path: {candidate}")
            return str(Path(candidate))

    print("[FAIL] File not found on any drive")
    return None


cached = r"X:\Other computers\MSW 2025\IPD2025 MSW\MONTH OF JULY\15.07.2025\DUBRAJ SINGH GOND\1010869893.txt"

resolved = test_drive_letter_change(cached)
print("Resolved path:", resolved)
