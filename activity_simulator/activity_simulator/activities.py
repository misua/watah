"""
Activity implementations for mouse, keyboard, and application interactions
"""
import numpy as np
import time
import logging
from typing import Tuple, List, Optional
from .win32_input import Win32InputInjector, VK_CODES
from .code_snippets import CodeSnippetGenerator, WindowDetector

logger = logging.getLogger(__name__)


class MouseActivity:
    """Mouse movement and interaction activities"""

    def __init__(self, injector: Win32InputInjector):
        self.injector = injector
        self.screen_width = injector.screen_width
        self.screen_height = injector.screen_height

    def generate_bezier_curve(
        self, start: Tuple[int, int], end: Tuple[int, int], control_points: int = 2
    ) -> List[Tuple[int, int]]:
        """Generate smooth Bezier curve for mouse movement"""
        t_values = np.linspace(0, 1, 50)

        if control_points == 1:
            cx = (start[0] + end[0]) / 2 + np.random.randint(-100, 100)
            cy = (start[1] + end[1]) / 2 + np.random.randint(-100, 100)
            points = []
            for t in t_values:
                x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * cx + t**2 * end[0]
                y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * cy + t**2 * end[1]
                points.append((int(x), int(y)))
        else:
            cx1 = start[0] + (end[0] - start[0]) / 3 + np.random.randint(-50, 50)
            cy1 = start[1] + (end[1] - start[1]) / 3 + np.random.randint(-50, 50)
            cx2 = start[0] + 2 * (end[0] - start[0]) / 3 + np.random.randint(-50, 50)
            cy2 = start[1] + 2 * (end[1] - start[1]) / 3 + np.random.randint(-50, 50)

            points = []
            for t in t_values:
                x = (
                    (1 - t) ** 3 * start[0]
                    + 3 * (1 - t) ** 2 * t * cx1
                    + 3 * (1 - t) * t**2 * cx2
                    + t**3 * end[0]
                )
                y = (
                    (1 - t) ** 3 * start[1]
                    + 3 * (1 - t) ** 2 * t * cy1
                    + 3 * (1 - t) * t**2 * cy2
                    + t**3 * end[1]
                )
                points.append((int(x), int(y)))

        return points

    def move_mouse_smooth(self, target_x: int, target_y: int) -> bool:
        """Move mouse smoothly along Bezier curve"""
        try:
            start_x, start_y = self.injector.get_cursor_position()
            points = self.generate_bezier_curve((start_x, start_y), (target_x, target_y))

            for i, (x, y) in enumerate(points):
                self.injector.move_mouse_absolute(x, y)
                delay = np.random.uniform(0.008, 0.015)
                time.sleep(delay)

            logger.debug(f"Moved mouse from ({start_x}, {start_y}) to ({target_x}, {target_y})")
            return True
        except Exception as e:
            logger.error(f"Failed to move mouse smoothly: {e}")
            return False

    def random_mouse_movement(self) -> bool:
        """Perform random mouse movement"""
        margin = 100
        target_x = np.random.randint(margin, self.screen_width - margin)
        target_y = np.random.randint(margin, self.screen_height - margin)
        return self.move_mouse_smooth(target_x, target_y)

    def small_mouse_jitter(self) -> bool:
        """Small mouse movement (micro-adjustment)"""
        try:
            current_x, current_y = self.injector.get_cursor_position()
            dx = np.random.randint(-20, 20)
            dy = np.random.randint(-20, 20)
            target_x = max(0, min(self.screen_width, current_x + dx))
            target_y = max(0, min(self.screen_height, current_y + dy))
            return self.move_mouse_smooth(target_x, target_y)
        except Exception as e:
            logger.error(f"Failed mouse jitter: {e}")
            return False

    def scroll_activity(self, direction: str = "down") -> bool:
        """Scroll mouse wheel with multiple scroll events"""
        try:
            scroll_count = np.random.randint(2, 6)
            for _ in range(scroll_count):
                amount = 120
                if direction == "up":
                    amount = -120
                
                success = self.injector.scroll_mouse(amount)
                if not success:
                    logger.error(f"Scroll failed")
                    return False
                time.sleep(np.random.uniform(0.1, 0.3))
            
            logger.debug(f"Scrolled {direction} {scroll_count} times")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll: {e}")
            return False


class KeyboardActivity:
    """Keyboard interaction activities"""

    def __init__(self, injector: Win32InputInjector):
        self.injector = injector
        self.snippet_generator = CodeSnippetGenerator()
        self.window_detector = WindowDetector()

    def type_random_text(self, length: int = None) -> bool:
        """Type context-aware code snippet in editor"""
        try:
            logger.info("Starting keyboard typing activity")
            
            try:
                window_title = self.window_detector.get_active_window_title()
                logger.debug(f"Active window: {window_title}")
                
                if not any(editor in window_title.lower() for editor in ['vscode', 'code', 'visual studio', 'notepad', 'sublime', 'atom', 'vim', 'pycharm']):
                    logger.warning(f"Not in code editor window: {window_title}, skipping typing")
                    return False
                
                file_ext = self.window_detector.detect_file_extension()
                logger.debug(f"Detected file extension: {file_ext}")
            except Exception as e:
                logger.warning(f"Window detection failed: {e}, using .py default")
                file_ext = ".py"
            
            typing_strategy = np.random.choice(['end_of_file', 'new_line_after_current', 'new_line_before_current'])
            
            if typing_strategy == 'end_of_file':
                logger.debug("Moving to end of file")
                self.injector.press_key(VK_CODES["control"], hold=True)
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["end"])
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["control"], hold=False)
                time.sleep(0.1)
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.1)
            elif typing_strategy == 'new_line_after_current':
                logger.debug("Creating new line after current")
                self.injector.press_key(VK_CODES["end"])
                time.sleep(0.1)
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.1)
            else:
                logger.debug("Creating new line before current")
                self.injector.press_key(VK_CODES["home"])
                time.sleep(0.1)
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.1)
                self.injector.press_key(VK_CODES["up"])
                time.sleep(0.1)
            
            snippet = self.snippet_generator.get_snippet(file_ext)
            
            try:
                snippet_safe = snippet.encode('ascii').decode('ascii')
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                logger.error(f"Snippet contains non-ASCII characters: {e}, filtering...")
                snippet_safe = ''.join(c for c in snippet if ord(c) < 128)
            
            logger.info(f"Typing snippet ({file_ext}) at safe location ({typing_strategy}): {snippet_safe[:50]}...")

            for char in snippet_safe:
                try:
                    success = self.injector.type_text(char, delay=np.random.uniform(0.05, 0.15))
                    if not success:
                        logger.error(f"Failed to type character: {char}")
                except Exception as e:
                    logger.error(f"Error typing character '{char}': {e}")
                    continue
                if np.random.random() < 0.1:
                    time.sleep(np.random.uniform(0.3, 0.8))
            
            self.injector.press_key(VK_CODES["enter"])
            time.sleep(np.random.uniform(0.2, 0.5))

            logger.info(f"Successfully typed snippet: {snippet}")
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}", exc_info=True)
            return False

    def press_navigation_key(self) -> bool:
        """Press navigation key (arrow, page up/down, etc.)"""
        keys = ["up", "down", "left", "right", "pageup", "pagedown", "home", "end"]
        key = np.random.choice(keys)

        try:
            vk_code = VK_CODES.get(key, 0x28)
            self.injector.press_key(vk_code)
            logger.debug(f"Pressed key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to press navigation key: {e}")
            return False

    def press_tab(self) -> bool:
        """Press Tab key"""
        try:
            self.injector.press_key(VK_CODES["tab"])
            logger.debug("Pressed Tab")
            return True
        except Exception as e:
            logger.error(f"Failed to press Tab: {e}")
            return False

    def press_ctrl_key_combo(self, key: str) -> bool:
        """Press Ctrl+Key combination"""
        try:
            extra = __import__("ctypes").c_ulong(0)
            from .win32_input import INPUT, INPUT_UNION, KEYBDINPUT, INPUT_KEYBOARD, KEYEVENTF_KEYUP
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32

            ctrl_down = INPUT_UNION()
            ctrl_down.ki = KEYBDINPUT(
                wVk=wintypes.WORD(VK_CODES["ctrl"]),
                wScan=0,
                dwFlags=0,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_ctrl_down = INPUT(type=INPUT_KEYBOARD, union=ctrl_down)

            key_vk = VK_CODES.get(key, ord(key.upper()))
            key_down = INPUT_UNION()
            key_down.ki = KEYBDINPUT(
                wVk=wintypes.WORD(key_vk),
                wScan=0,
                dwFlags=0,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_key_down = INPUT(type=INPUT_KEYBOARD, union=key_down)

            key_up = INPUT_UNION()
            key_up.ki = KEYBDINPUT(
                wVk=wintypes.WORD(key_vk),
                wScan=0,
                dwFlags=KEYEVENTF_KEYUP,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_key_up = INPUT(type=INPUT_KEYBOARD, union=key_up)

            ctrl_up = INPUT_UNION()
            ctrl_up.ki = KEYBDINPUT(
                wVk=wintypes.WORD(VK_CODES["ctrl"]),
                wScan=0,
                dwFlags=KEYEVENTF_KEYUP,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_ctrl_up = INPUT(type=INPUT_KEYBOARD, union=ctrl_up)

            user32.SendInput(1, ctypes.pointer(x_ctrl_down), ctypes.sizeof(x_ctrl_down))
            time.sleep(0.05)
            user32.SendInput(1, ctypes.pointer(x_key_down), ctypes.sizeof(x_key_down))
            time.sleep(0.05)
            user32.SendInput(1, ctypes.pointer(x_key_up), ctypes.sizeof(x_key_up))
            time.sleep(0.05)
            user32.SendInput(1, ctypes.pointer(x_ctrl_up), ctypes.sizeof(x_ctrl_up))

            logger.debug(f"Pressed Ctrl+{key}")
            return True
        except Exception as e:
            logger.error(f"Failed to press Ctrl+{key}: {e}")
            return False


class CompositeActivity:
    """Composite activities combining multiple actions"""

    def __init__(self, mouse: MouseActivity, keyboard: KeyboardActivity):
        self.mouse = mouse
        self.keyboard = keyboard

    def file_editing_workflow(self) -> bool:
        """Simulate file editing workflow"""
        try:
            self.mouse.random_mouse_movement()
            time.sleep(np.random.uniform(0.5, 1.5))

            self.mouse.injector.click_mouse("left")
            time.sleep(np.random.uniform(1.0, 2.0))

            self.keyboard.type_random_text()
            time.sleep(np.random.uniform(1.5, 3.0))

            self.mouse.scroll_activity("down")
            time.sleep(np.random.uniform(0.8, 1.5))

            self.keyboard.type_random_text()
            time.sleep(np.random.uniform(1.0, 2.0))

            logger.info("Completed file editing workflow")
            return True
        except Exception as e:
            logger.error(f"Failed file editing workflow: {e}")
            return False

    def browsing_workflow(self) -> bool:
        """Simulate web browsing workflow"""
        try:
            self.mouse.random_mouse_movement()
            time.sleep(np.random.uniform(0.5, 1.0))

            for _ in range(np.random.randint(2, 5)):
                self.mouse.scroll_activity("down")
                time.sleep(np.random.uniform(1.5, 3.0))

            if np.random.random() < 0.3:
                self.mouse.injector.click_mouse("left")
                time.sleep(np.random.uniform(1.0, 2.0))

            logger.info("Completed browsing workflow")
            return True
        except Exception as e:
            logger.error(f"Failed browsing workflow: {e}")
            return False

    def tab_switching_workflow(self) -> bool:
        """Simulate tab switching in application"""
        try:
            self.keyboard.press_ctrl_key_combo("tab")
            time.sleep(np.random.uniform(0.5, 1.5))

            self.mouse.scroll_activity(np.random.choice(["up", "down"]))
            time.sleep(np.random.uniform(1.0, 2.0))

            logger.info("Completed tab switching workflow")
            return True
        except Exception as e:
            logger.error(f"Failed tab switching workflow: {e}")
            return False
