from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from ctypes import (
    WINFUNCTYPE,
    Structure,
    byref,
    c_int,
    create_unicode_buffer,
    windll,
)
from ctypes.wintypes import BOOL, DWORD, HWND, LPARAM
from pathlib import Path
from typing import Any


FAP_NX_NASTRAN = 36
FT_LOAD_DIR = 12
FT_BC_DIR = 17
DEFAULT_FEMAP_EXE = Path(r"C:\Program Files\Siemens\Femap 2512\femap.exe")
SW_RESTORE = 9
SW_SHOW = 5
SWP_SHOWWINDOW = 0x0040
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


class Rect(Structure):
    _fields_ = [
        ("left", c_int),
        ("top", c_int),
        ("right", c_int),
        ("bottom", c_int),
    ]


EnumWindowsProc = WINFUNCTYPE(BOOL, HWND, LPARAM)


def require_pywin32() -> tuple[Any, Any]:
    try:
        import pythoncom
        import win32com.client
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "pywin32 is required. Use a Python environment and dependency location "
            "permitted by the target project."
        ) from exc
    return pythoncom, win32com.client


def window_text(hwnd: int) -> str:
    length = windll.user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def process_image_name(pid: int) -> str:
    handle = windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return ""
    try:
        size = DWORD(32768)
        buf = create_unicode_buffer(size.value)
        ok = windll.kernel32.QueryFullProcessImageNameW(handle, 0, buf, byref(size))
        return buf.value if ok else ""
    finally:
        windll.kernel32.CloseHandle(handle)


def enum_femap_windows() -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []

    @EnumWindowsProc
    def callback(hwnd: int, _lparam: int) -> int:
        if not windll.user32.IsWindowVisible(hwnd):
            return 1
        pid = DWORD()
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        title = window_text(hwnd)
        image = process_image_name(pid.value)
        lower_title = title.lower()
        lower_image = image.lower()
        if "femap" in lower_title or lower_image.endswith("\\femap.exe"):
            windows.append({"hwnd": hwnd, "pid": pid.value, "title": title, "image": image})
        return 1

    windll.user32.EnumWindows(callback, 0)
    return windows


def latest_femap_window(timeout_s: float) -> dict[str, Any]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        windows = enum_femap_windows()
        if windows:
            return windows[-1]
        time.sleep(1)
    raise RuntimeError("No visible Femap window was found.")


def window_rect(hwnd: int) -> dict[str, int]:
    rect = Rect()
    if not windll.user32.GetWindowRect(hwnd, byref(rect)):
        raise RuntimeError("GetWindowRect failed.")
    return {
        "left": rect.left,
        "top": rect.top,
        "right": rect.right,
        "bottom": rect.bottom,
        "width": rect.right - rect.left,
        "height": rect.bottom - rect.top,
    }


def resize_window(hwnd: int, x: int, y: int, width: int, height: int) -> dict[str, int]:
    windll.user32.ShowWindow(hwnd, SW_RESTORE)
    windll.user32.ShowWindow(hwnd, SW_SHOW)
    ok = windll.user32.SetWindowPos(hwnd, 0, x, y, width, height, SWP_SHOWWINDOW)
    if not ok:
        raise RuntimeError("SetWindowPos failed.")
    windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    return window_rect(hwnd)


def call_or_value(obj: Any, name: str, *args: Any) -> Any:
    value = getattr(obj, name)
    if callable(value):
        return value(*args)
    if args:
        raise TypeError(f"{name} is not callable in the current FEMAP COM binding.")
    return value


def connect_femap(win32com_client: Any, timeout_s: float) -> Any:
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            return win32com_client.GetActiveObject("femap.model")
        except Exception as exc:  # COM server may register after the main window appears.
            last_error = exc
            time.sleep(1)
    try:
        return win32com_client.Dispatch("femap.model")
    except Exception as exc:
        raise RuntimeError(f"Could not connect to FEMAP COM: {last_error or exc}") from exc


def show_femap(app: Any) -> None:
    for action in (
        lambda: app.feAppVisible(True),
        lambda: app.feAppShowWindow(False),
        lambda: app.feAppBringToTop(True, 0),
        lambda: app.feAppUpdatePanes(True),
    ):
        try:
            action()
        except Exception:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Open a model in Siemens Femap and set the visible window size.")
    parser.add_argument("--model", required=True, help="BDF/DAT model path to import with FEMAP.")
    parser.add_argument("--femap-exe", default=str(DEFAULT_FEMAP_EXE), help="Path to femap.exe.")
    parser.add_argument("--width", type=int, default=1440, help="Target outer window width.")
    parser.add_argument("--height", type=int, default=1024, help="Target outer window height.")
    parser.add_argument("--x", type=int, default=40, help="Target window left coordinate.")
    parser.add_argument("--y", type=int, default=40, help="Target window top coordinate.")
    parser.add_argument("--no-new-model", action="store_true", help="Import into the current model instead of creating a new model first.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Seconds to wait for Femap COM/window startup.")
    args = parser.parse_args()

    model = Path(args.model).expanduser().resolve()
    femap_exe = Path(args.femap_exe).expanduser().resolve()
    if not model.exists():
        raise FileNotFoundError(model)
    if not femap_exe.exists():
        raise FileNotFoundError(femap_exe)

    pythoncom, win32com_client = require_pywin32()
    existing_windows = enum_femap_windows()
    launched_pid: int | None = None
    if not existing_windows:
        proc = subprocess.Popen([str(femap_exe)])
        launched_pid = proc.pid

    pythoncom.CoInitialize()
    try:
        app = connect_femap(win32com_client, args.timeout)
        show_femap(app)
        new_model_rc = None if args.no_new_model else int(call_or_value(app, "feFileNew"))
        import_bdf_rc = int(app.feFileReadNastran(FAP_NX_NASTRAN, str(model)))
        active_bc_set = int(app.Info_ActiveID(FT_BC_DIR))
        active_load_set = int(app.Info_ActiveID(FT_LOAD_DIR))
        try:
            app.feAppMessage(0, f"[Codex] Opened verification model: {model}")
        except Exception:
            pass
        try:
            app.feViewRegenerate(0)
        except Exception:
            pass
    finally:
        pythoncom.CoUninitialize()

    window = latest_femap_window(args.timeout)
    rect = resize_window(int(window["hwnd"]), args.x, args.y, args.width, args.height)
    summary = {
        "model": str(model),
        "femap_exe": str(femap_exe),
        "launched_pid": launched_pid,
        "window_pid": window["pid"],
        "window_title": window["title"],
        "new_model_rc": new_model_rc,
        "import_bdf_rc": import_bdf_rc,
        "active_bc_set": active_bc_set,
        "active_load_set": active_load_set,
        "rect": rect,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
