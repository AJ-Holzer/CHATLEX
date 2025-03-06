import ctypes
import customtkinter as ctk
from ctypes import wintypes

# Constants
WDA_EXCLUDEFROMCAPTURE = 0x00000011
# Function prototypes
user32 = ctypes.WinDLL('user32', use_last_error=True)
SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
SetWindowDisplayAffinity.argtypes = [wintypes.HWND, wintypes.DWORD]
SetWindowDisplayAffinity.restype = wintypes.BOOL

def exlude_from_screen_recording(ctk_root: ctk.CTk) -> None:
    hwnd = ctypes.windll.user32.GetParent(ctk_root.winfo_id())
    if not SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE):
        raise ctypes.WinError(ctypes.get_last_error())
