"""
Windows SendInput API wrapper for hardware-level input injection
"""
import ctypes
import time
from ctypes import wintypes
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

user32 = ctypes.windll.user32

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_ABSOLUTE = 0x8000

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION),
    ]


class Win32InputInjector:
    """Low-level Windows input injection using SendInput API"""

    def __init__(self):
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        logger.info(f"Initialized Win32 input injector: {self.screen_width}x{self.screen_height}")

    def move_mouse_relative(self, dx: int, dy: int) -> bool:
        """Move mouse by relative offset"""
        try:
            extra = ctypes.c_ulong(0)
            ii_ = INPUT_UNION()
            ii_.mi = MOUSEINPUT(
                dx=dx,
                dy=dy,
                mouseData=0,
                dwFlags=MOUSEEVENTF_MOVE,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x = INPUT(type=INPUT_MOUSE, union=ii_)
            result = user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            return result == 1
        except Exception as e:
            logger.error(f"Failed to move mouse: {e}")
            return False

    def move_mouse_absolute(self, x: int, y: int) -> bool:
        """Move mouse to absolute position"""
        try:
            normalized_x = int(x * 65535 / self.screen_width)
            normalized_y = int(y * 65535 / self.screen_height)

            extra = ctypes.c_ulong(0)
            ii_ = INPUT_UNION()
            ii_.mi = MOUSEINPUT(
                dx=normalized_x,
                dy=normalized_y,
                mouseData=0,
                dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_input = INPUT(type=INPUT_MOUSE, union=ii_)
            result = user32.SendInput(1, ctypes.pointer(x_input), ctypes.sizeof(x_input))
            return result == 1
        except Exception as e:
            logger.error(f"Failed to move mouse absolute: {e}")
            return False

    def get_cursor_position(self) -> Tuple[int, int]:
        """Get current cursor position"""
        try:
            point = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(point))
            return (point.x, point.y)
        except Exception as e:
            logger.error(f"Failed to get cursor position: {e}")
            return (0, 0)

    def scroll_mouse(self, amount: int) -> bool:
        """Scroll mouse wheel (positive = up, negative = down)"""
        try:
            extra = ctypes.c_ulong(0)
            ii_ = INPUT_UNION()
            ii_.mi = MOUSEINPUT(
                dx=0,
                dy=0,
                mouseData=wintypes.DWORD(amount),
                dwFlags=MOUSEEVENTF_WHEEL,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x = INPUT(type=INPUT_MOUSE, union=ii_)
            result = user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            return result == 1
        except Exception as e:
            logger.error(f"Failed to scroll mouse: {e}")
            return False

    def click_mouse(self, button: str = "left") -> bool:
        """Click mouse button"""
        try:
            if button == "left":
                down_flag = MOUSEEVENTF_LEFTDOWN
                up_flag = MOUSEEVENTF_LEFTUP
            elif button == "right":
                down_flag = MOUSEEVENTF_RIGHTDOWN
                up_flag = MOUSEEVENTF_RIGHTUP
            else:
                down_flag = MOUSEEVENTF_MIDDLEDOWN
                up_flag = MOUSEEVENTF_MIDDLEUP

            extra = ctypes.c_ulong(0)

            ii_down = INPUT_UNION()
            ii_down.mi = MOUSEINPUT(
                dx=0, dy=0, mouseData=0, dwFlags=down_flag, time=0, dwExtraInfo=ctypes.pointer(extra)
            )
            x_down = INPUT(type=INPUT_MOUSE, union=ii_down)

            ii_up = INPUT_UNION()
            ii_up.mi = MOUSEINPUT(
                dx=0, dy=0, mouseData=0, dwFlags=up_flag, time=0, dwExtraInfo=ctypes.pointer(extra)
            )
            x_up = INPUT(type=INPUT_MOUSE, union=ii_up)

            inputs = (INPUT * 2)(x_down, x_up)
            result = user32.SendInput(2, ctypes.pointer(inputs), ctypes.sizeof(INPUT))
            return result == 2
        except Exception as e:
            logger.error(f"Failed to click mouse: {e}")
            return False

    def press_key(self, vk_code: int, hold_time: float = 0.05) -> bool:
        """Press and release a key"""
        try:
            extra = ctypes.c_ulong(0)

            ii_down = INPUT_UNION()
            ii_down.ki = KEYBDINPUT(
                wVk=wintypes.WORD(vk_code),
                wScan=0,
                dwFlags=0,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_down = INPUT(type=INPUT_KEYBOARD, union=ii_down)

            ii_up = INPUT_UNION()
            ii_up.ki = KEYBDINPUT(
                wVk=wintypes.WORD(vk_code),
                wScan=0,
                dwFlags=KEYEVENTF_KEYUP,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_up = INPUT(type=INPUT_KEYBOARD, union=ii_up)

            user32.SendInput(1, ctypes.pointer(x_down), ctypes.sizeof(x_down))
            time.sleep(hold_time)
            user32.SendInput(1, ctypes.pointer(x_up), ctypes.sizeof(x_up))
            return True
        except Exception as e:
            logger.error(f"Failed to press key: {e}")
            return False

    def type_text(self, text: str, delay: float = 0.05) -> bool:
        """Type text using Unicode input"""
        try:
            for char in text:
                extra = ctypes.c_ulong(0)

                ii_down = INPUT_UNION()
                ii_down.ki = KEYBDINPUT(
                    wVk=0,
                    wScan=ord(char),
                    dwFlags=KEYEVENTF_UNICODE,
                    time=0,
                    dwExtraInfo=ctypes.pointer(extra),
                )
                x_down = INPUT(type=INPUT_KEYBOARD, union=ii_down)

                ii_up = INPUT_UNION()
                ii_up.ki = KEYBDINPUT(
                    wVk=0,
                    wScan=ord(char),
                    dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP,
                    time=0,
                    dwExtraInfo=ctypes.pointer(extra),
                )
                x_up = INPUT(type=INPUT_KEYBOARD, union=ii_up)

                user32.SendInput(1, ctypes.pointer(x_down), ctypes.sizeof(x_down))
                time.sleep(delay)
                user32.SendInput(1, ctypes.pointer(x_up), ctypes.sizeof(x_up))
                time.sleep(delay)
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False


VK_CODES = {
    "tab": 0x09,
    "enter": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "alt": 0x12,
    "escape": 0x1B,
    "space": 0x20,
    "pageup": 0x21,
    "pagedown": 0x22,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "delete": 0x2E,
}
