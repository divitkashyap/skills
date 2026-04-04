#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
clipboard_image.py — Save image from clipboard to a temp file.
Cross-platform: macOS, Linux, Windows.

Usage:
    python3 clipboard_image.py [output_path]
    # If output_path omitted, saves to /tmp/vision-clipboard-<timestamp>.png

Exit codes:
    0 — image saved successfully
    1 — no image in clipboard
    2 — platform not supported / dependency missing
"""

import os
import sys
import platform
import subprocess
import tempfile
from datetime import datetime

TIMEOUT = 10


def save_mac_clipboardImage(output_path: str) -> bool:
    try:
        script = (
            'set theImage to clipboard as record '
            '(class type TIFF picture, class type PNG picture) '
            'in theSystemClipboard; '
            'set theData to theImage as TIFF picture; '
            'return (do shell script "mkdir -p $(dirname ' + output_path.replace("'", "'\\''") + ") && echo 'ok'") as string; '
            'do shell script "cat > ' + output_path.replace("'", "'\\''") + "' with scalar input theData"
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        return result.returncode == 0 and os.path.exists(output_path)
    except Exception:
        return False


def save_linux_clipboard_image(output_path: str) -> bool:
    tools = [
        ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
        ["wl-paste", "-t", "image/png"],
    ]
    for cmd in tools:
        try:
            with open(output_path, "wb") as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, timeout=TIMEOUT)
            if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return True
        except Exception:
            continue
    return False


def save_windows_clipboard_image(output_path: str) -> bool:
    ps = (
        f"Add-Type -AssemblyName System.Windows.Forms; "
        f"$img = [System.Windows.Forms.Clipboard]::GetImage(); "
        f"if ($img) {{ $img.Save('{output_path.replace(chr(92), chr(92)*2)}', [System.Drawing.Imaging.ImageFormat]::Png); exit 0 }} else {{ exit 1 }}"
    )
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        return result.returncode == 0 and os.path.exists(output_path)
    except Exception:
        return False


def save_clipboard_image(output_path: str = None) -> str:
    if output_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/vision-clipboard-{ts}.png"

    os.makedirs(os.path.dirname(output_path) or "/tmp", exist_ok=True)

    system = platform.system()
    if system == "Darwin":
        ok = save_mac_clipboardImage(output_path)
    elif system == "Linux":
        ok = save_linux_clipboard_image(output_path)
    elif system == "Windows":
        ok = save_windows_clipboard_image(output_path)
    else:
        print(f"ERROR: Unsupported platform: {system}", file=sys.stderr)
        sys.exit(2)

    if ok and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(output_path)
        sys.exit(0)
    else:
        print("ERROR: No image found in clipboard", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    save_clipboard_image(sys.argv[1] if len(sys.argv) > 1 else None)
