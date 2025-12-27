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
            
            # Check if we should stop (user input detected)
            from .daemon import ActivityDaemon
            daemon_instance = getattr(self.injector, '_daemon_ref', None)
            
            # Try to detect file type from window, but default to Python if it fails
            file_ext = ".py"
            try:
                window_title = self.window_detector.get_active_window_title()
                if window_title:
                    logger.debug(f"Active window: {window_title}")
                    detected_ext = self.window_detector.detect_file_extension()
                    if detected_ext:
                        file_ext = detected_ext
                        logger.debug(f"Detected file extension: {file_ext}")
            except Exception as e:
                logger.debug(f"Window detection failed: {e}, using .py default")
            
            # Prefer end of file to avoid destroying code
            typing_strategy = np.random.choice(
                ['end_of_file', 'new_line_after_current', 'comment_only'],
                p=[0.6, 0.3, 0.1]  # 60% end of file, 30% new line after, 10% comment
            )
            
            if typing_strategy == 'end_of_file':
                logger.debug("Moving to end of file (safest)")
                self.injector.press_key(VK_CODES["control"], hold=True)
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["end"])
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["control"], hold=False)
                time.sleep(0.1)
                # Add double newline for safety
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.1)
            elif typing_strategy == 'new_line_after_current':
                logger.debug("Creating new line after current")
                self.injector.press_key(VK_CODES["end"])
                time.sleep(0.1)
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.1)
            else:  # comment_only
                logger.debug("Adding comment only (very safe)")
                self.injector.press_key(VK_CODES["end"])
                time.sleep(0.1)
                self.injector.press_key(VK_CODES["enter"])
                time.sleep(0.1)
                # Override to use comment snippet
                if file_ext == ".py":
                    snippet = "# " + np.random.choice(["TODO: implement", "FIXME", "Review this", "Optimize later"])
                else:
                    snippet = "// " + np.random.choice(["TODO", "FIXME", "Review", "Check this"])
                
                for char in snippet:
                    self.injector.type_text(char, delay=np.random.uniform(0.05, 0.15))
                logger.info(f"Added comment: {snippet}")
                return True
            
            snippet = self.snippet_generator.get_snippet(file_ext)
            
            try:
                snippet_safe = snippet.encode('ascii').decode('ascii')
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                logger.error(f"Snippet contains non-ASCII characters: {e}, filtering...")
                snippet_safe = ''.join(c for c in snippet if ord(c) < 128)
            
            logger.info(f"Typing snippet ({file_ext}) at safe location ({typing_strategy}): {snippet_safe[:50]}...")

            # Realistic typing speed: 60-120 WPM = 5-10 chars/sec
            # Faster bursts when in the zone, slower when thinking
            typing_mode = np.random.choice(['burst', 'normal', 'thinking'], p=[0.4, 0.4, 0.2])
            
            if typing_mode == 'burst':
                base_delay = (0.02, 0.05)  # Fast typing
                pause_chance = 0.03
                line_pause = (0.1, 0.3)  # Quick between lines
            elif typing_mode == 'normal':
                base_delay = (0.04, 0.08)  # Normal speed
                pause_chance = 0.08
                line_pause = (0.3, 0.7)  # Normal pause between lines
            else:  # thinking
                base_delay = (0.08, 0.15)  # Slower, thinking
                pause_chance = 0.15
                line_pause = (0.5, 1.2)  # Longer thinking pauses

            # Split snippet into lines and type line by line (like a real developer)
            lines = snippet_safe.split('\n')
            for line_idx, line in enumerate(lines):
                # Handle indentation: convert leading spaces to tabs for code editors
                leading_spaces = len(line) - len(line.lstrip(' '))
                if leading_spaces > 0:
                    # Most code editors use 4 spaces = 1 tab for Python, 2 spaces = 1 tab for Terraform
                    spaces_per_tab = 4 if file_ext == ".py" else 2
                    num_tabs = leading_spaces // spaces_per_tab
                    remaining_spaces = leading_spaces % spaces_per_tab
                    
                    # Type tabs for indentation
                    for _ in range(num_tabs):
                        self.injector.press_key(VK_CODES["tab"])
                        time.sleep(np.random.uniform(0.05, 0.1))
                    
                    # Type any remaining spaces
                    for _ in range(remaining_spaces):
                        self.injector.type_text(' ', delay=0.05)
                    
                    # Type the rest of the line (without leading spaces)
                    line_content = line.lstrip(' ')
                else:
                    line_content = line
                
                for char in line_content:
                    try:
                        success = self.injector.type_text(char, delay=np.random.uniform(*base_delay))
                        if not success:
                            logger.error(f"Failed to type character: {char}")
                    except Exception as e:
                        logger.error(f"Error typing character '{char}': {e}")
                        continue
                    # Occasional thinking pauses within a line
                    if np.random.random() < pause_chance:
                        time.sleep(np.random.uniform(0.2, 0.6))
                
                # Press Enter at end of line (except for last line)
                if line_idx < len(lines) - 1:
                    self.injector.press_key(VK_CODES["enter"])
                    # Pause between lines (thinking about next line)
                    time.sleep(np.random.uniform(*line_pause))
            
            # Final newline after the whole snippet
            self.injector.press_key(VK_CODES["enter"])
            time.sleep(np.random.uniform(0.1, 0.3))

            logger.info(f"Successfully typed snippet: {snippet[:100]}")
            
            # 30% chance to type multiple related snippets (realistic coding session)
            if np.random.random() < 0.3:
                num_extra_lines = np.random.randint(1, 3)
                logger.info(f"Typing {num_extra_lines} additional snippets...")
                for _ in range(num_extra_lines):
                    time.sleep(np.random.uniform(0.5, 1.5))  # Think before next block
                    extra_snippet = self.snippet_generator.get_snippet(file_ext)
                    
                    # Type the extra snippet line by line too
                    extra_lines = extra_snippet.split('\n')
                    for line_idx, line in enumerate(extra_lines):
                        for char in line:
                            self.injector.type_text(char, delay=np.random.uniform(0.03, 0.07))
                        if line_idx < len(extra_lines) - 1:
                            self.injector.press_key(VK_CODES["enter"])
                            time.sleep(np.random.uniform(0.2, 0.5))
                    
                    self.injector.press_key(VK_CODES["enter"])
                    time.sleep(np.random.uniform(0.1, 0.3))
            
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
        """Press Ctrl+Key combination (e.g., Ctrl+Tab for tab switching)"""
        try:
            import ctypes
            from ctypes import wintypes
            from .win32_input import INPUT, INPUT_UNION, KEYBDINPUT, INPUT_KEYBOARD, KEYEVENTF_KEYUP
            
            extra = ctypes.c_ulong(0)
            user32 = ctypes.windll.user32
            
            # Get the VK code for the key - only use ord() for single characters
            key_lower = key.lower()
            if key_lower in VK_CODES:
                key_vk = VK_CODES[key_lower]
            elif len(key) == 1:
                key_vk = ord(key.upper())
            else:
                logger.error(f"Unknown key: {key}")
                return False
                
            logger.info(f"Attempting Ctrl+{key} (VK: 0x{VK_CODES['control']:02X} + 0x{key_vk:02X})")
            
            # Press Ctrl down
            ctrl_down = INPUT_UNION()
            ctrl_down.ki = KEYBDINPUT(
                wVk=wintypes.WORD(VK_CODES["control"]),
                wScan=0,
                dwFlags=0,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_ctrl_down = INPUT(type=INPUT_KEYBOARD, union=ctrl_down)
            
            # Press key down
            key_down = INPUT_UNION()
            key_down.ki = KEYBDINPUT(
                wVk=wintypes.WORD(key_vk),
                wScan=0,
                dwFlags=0,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_key_down = INPUT(type=INPUT_KEYBOARD, union=key_down)
            
            # Release key
            key_up = INPUT_UNION()
            key_up.ki = KEYBDINPUT(
                wVk=wintypes.WORD(key_vk),
                wScan=0,
                dwFlags=KEYEVENTF_KEYUP,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_key_up = INPUT(type=INPUT_KEYBOARD, union=key_up)
            
            # Release Ctrl
            ctrl_up = INPUT_UNION()
            ctrl_up.ki = KEYBDINPUT(
                wVk=wintypes.WORD(VK_CODES["control"]),
                wScan=0,
                dwFlags=KEYEVENTF_KEYUP,
                time=0,
                dwExtraInfo=ctypes.pointer(extra),
            )
            x_ctrl_up = INPUT(type=INPUT_KEYBOARD, union=ctrl_up)
            
            # Send the input events in sequence
            result1 = user32.SendInput(1, ctypes.pointer(x_ctrl_down), ctypes.sizeof(x_ctrl_down))
            time.sleep(0.02)
            result2 = user32.SendInput(1, ctypes.pointer(x_key_down), ctypes.sizeof(x_key_down))
            time.sleep(0.02)
            result3 = user32.SendInput(1, ctypes.pointer(x_key_up), ctypes.sizeof(x_key_up))
            time.sleep(0.02)
            result4 = user32.SendInput(1, ctypes.pointer(x_ctrl_up), ctypes.sizeof(x_ctrl_up))
            
            logger.info(f"Ctrl+{key} SendInput results: {result1}, {result2}, {result3}, {result4}")
            return all([result1, result2, result3, result4])
        except Exception as e:
            logger.error(f"Failed to press Ctrl+{key}: {e}", exc_info=True)
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
            logger.info("=== STARTING TAB SWITCHING WORKFLOW ===")
            
            # Actually switch tabs with Ctrl+Tab
            logger.info("Attempting first Ctrl+Tab...")
            result1 = self.keyboard.press_ctrl_key_combo("tab")
            logger.info(f"First Ctrl+Tab result: {result1}")
            time.sleep(np.random.uniform(0.5, 1.0))
            
            # Sometimes switch again
            if np.random.random() < 0.4:
                logger.info("Attempting second Ctrl+Tab...")
                result2 = self.keyboard.press_ctrl_key_combo("tab")
                logger.info(f"Second Ctrl+Tab result: {result2}")
                time.sleep(np.random.uniform(0.5, 1.0))

            # Scroll in new tab
            logger.info("Scrolling in new tab...")
            self.mouse.scroll_activity(np.random.choice(["up", "down"]))
            time.sleep(np.random.uniform(1.0, 2.0))

            logger.info("=== COMPLETED TAB SWITCHING WORKFLOW ===")
            return True
        except Exception as e:
            logger.error(f"Failed tab switching workflow: {e}", exc_info=True)
            return False
