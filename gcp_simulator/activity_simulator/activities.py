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
            # Check if daemon is paused before starting
            daemon_instance = getattr(self.injector, '_daemon_ref', None)
            if daemon_instance and hasattr(daemon_instance, 'paused') and daemon_instance.paused:
                logger.debug("Daemon is paused, skipping mouse movement")
                return False
            
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

    def double_click_word(self) -> bool:
        """Double-click at current mouse position to select word - Phase 1, Task 1.2"""
        try:
            # Double-click to select word
            self.injector.click_mouse("left")
            time.sleep(0.05)  # Brief delay between clicks
            self.injector.click_mouse("left")
            
            # Selection confirmation pause (100-300ms)
            time.sleep(np.random.uniform(0.1, 0.3))
            
            logger.info("Double-clicked to select word")
            return True
        except Exception as e:
            logger.error(f"Failed to double-click word: {e}")
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
            
            # CRITICAL: Only type in VSCode or IDE windows
            try:
                window_title = self.window_detector.get_active_window_title()
                logger.info(f"Typing check - Active window: '{window_title}'")
                
                # Whitelist: ONLY these applications are allowed for typing
                # Added 'code' for VSCode which often shows as just "Code"
                allowed_apps = ['code', 'visual studio code', 'vscode', 'vs code', 'pycharm', 'intellij', 'sublime text', 'atom', 'notepad++', 'vim', 'emacs']
                is_allowed = any(app in window_title.lower() for app in allowed_apps)
                
                # Blacklist: NEVER type in these applications
                blocked_apps = ['chrome', 'edge', 'firefox', 'brave', 'opera', 'safari', 'outlook', 'mail', 'gmail', 'powershell', 'cmd', 'terminal', 'command prompt', 'windows powershell', 'login', 'sign in', 'password']
                is_blocked = any(app in window_title.lower() for app in blocked_apps)
                
                if is_blocked:
                    logger.warning(f"Typing BLOCKED - dangerous window: {window_title}")
                    return False
                
                if not is_allowed:
                    logger.warning(f"Typing SKIPPED - not in IDE window: {window_title}")
                    return False
                
                logger.info(f"✓ Typing ALLOWED in IDE: {window_title}")
                
                # Detect file extension
                file_ext = self.window_detector.detect_file_extension() or ".py"
                logger.debug(f"Detected file extension: {file_ext}")
            except Exception as e:
                logger.error(f"Window detection FAILED: {e}, skipping typing for safety")
                return False
            
            # Prefer end of file to avoid destroying code
            typing_strategy = np.random.choice(
                ['end_of_file', 'comment_only'],
                p=[0.9, 0.1]  # 90% end of file, 10% comment only
            )
            
            if typing_strategy == 'end_of_file':
                logger.debug("Moving to end of file (safest)")
                self.injector.press_key(VK_CODES["control"], hold=True)
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["end"])
                time.sleep(0.05)
                self.injector.press_key(VK_CODES["control"], hold=False)
                time.sleep(0.1)
                # Add multiple blank lines for safety (separate from existing code)
                for _ in range(3):
                    self.injector.press_key(VK_CODES["enter"])
                    time.sleep(0.05)
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
                # Check if daemon is paused (user input detected)
                if daemon_instance and hasattr(daemon_instance, 'paused') and daemon_instance.paused:
                    logger.info("User input detected during typing, stopping activity")
                    return False
                
                # Strip leading spaces - let editor auto-indent handle spacing
                line_content = line.lstrip(' ')
                
                # Skip empty lines
                if not line_content:
                    if line_idx < len(lines) - 1:
                        self.injector.press_key(VK_CODES["enter"])
                        time.sleep(np.random.uniform(0.1, 0.2))
                    continue
                
                char_index = 0
                for char in line_content:
                    # Realistic typo/correction behavior (2% chance per character, only on letters)
                    if np.random.random() < 0.02 and char.isalpha():
                        # Make a typo: type 1-2 wrong characters
                        num_wrong_chars = np.random.randint(1, 3)
                        wrong_chars = np.random.choice(list('asdfghjklqwertyuiop'), size=num_wrong_chars)
                        
                        for wrong_char in wrong_chars:
                            self.injector.type_text(wrong_char, delay=np.random.uniform(0.03, 0.06))
                        
                        # Pause (realizing the mistake)
                        time.sleep(np.random.uniform(0.1, 0.25))
                        
                        # Delete the wrong characters
                        for _ in range(num_wrong_chars):
                            self.injector.press_key(VK_CODES["backspace"])
                            time.sleep(np.random.uniform(0.05, 0.1))
                        
                        # Brief pause before typing correct character
                        time.sleep(np.random.uniform(0.05, 0.1))
                    
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
                    
                    # Occasionally delete and retype last few characters (rethinking, 1% chance)
                    if char_index > 3 and np.random.random() < 0.01:
                        chars_to_delete = np.random.randint(2, min(4, char_index + 1))
                        # Pause (reconsidering)
                        time.sleep(np.random.uniform(0.2, 0.4))
                        # Delete characters
                        for _ in range(chars_to_delete):
                            self.injector.press_key(VK_CODES["backspace"])
                            time.sleep(np.random.uniform(0.04, 0.08))
                        # Pause before retyping
                        time.sleep(np.random.uniform(0.1, 0.25))
                        # Retype the deleted characters
                        start_idx = max(0, char_index - chars_to_delete + 1)
                        for i in range(start_idx, char_index + 1):
                            if i < len(line):
                                self.injector.type_text(line[i], delay=np.random.uniform(*base_delay))
                                time.sleep(np.random.uniform(0.02, 0.05))
                    
                    char_index += 1
                    
                    # Periodic check for pause (every 10 chars)
                    if char_index % 10 == 0:
                        if daemon_instance and hasattr(daemon_instance, 'paused') and daemon_instance.paused:
                            logger.info("User input detected during typing, stopping activity")
                            return False
                
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
            
            # Phase 1, Task 1.1: Add Ctrl+S save after typing (70% probability)
            if np.random.random() < 0.7:
                # Brief review pause before saving
                time.sleep(np.random.uniform(0.3, 1.0))
                self.press_ctrl_s()
                logger.info("Auto-saved after typing activity")
            
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}", exc_info=True)
            return False

    def press_navigation_key(self) -> bool:
        """Press navigation key (arrow, page up/down, etc.) - ONLY in IDEs"""
        # CRITICAL: Only allow navigation keys in IDEs, not in browsers
        try:
            window_title = self.window_detector.get_active_window_title()
            logger.info(f"Navigation check - Active window: '{window_title}'")
            
            # Whitelist: ONLY these applications are allowed for keyboard navigation
            allowed_apps = ['code', 'visual studio code', 'vscode', 'vs code', 'pycharm', 'intellij', 'sublime text', 'atom', 'notepad++', 'vim', 'emacs']
            is_allowed = any(app in window_title.lower() for app in allowed_apps)
            
            # Blacklist: NEVER use keyboard shortcuts in these applications
            blocked_apps = ['chrome', 'edge', 'firefox', 'brave', 'opera', 'safari', 'outlook', 'mail', 'gmail', 'powershell', 'cmd', 'terminal']
            is_blocked = any(app in window_title.lower() for app in blocked_apps)
            
            if is_blocked:
                logger.warning(f"Navigation BLOCKED - dangerous window: {window_title}")
                return False
            
            if not is_allowed:
                logger.warning(f"Navigation SKIPPED - not in IDE: {window_title}")
                return False
            
            logger.info(f"✓ Navigation ALLOWED in IDE: {window_title}")
        except Exception as e:
            logger.error(f"Window detection FAILED: {e}, skipping navigation for safety")
            return False
        
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

    # Developer-specific keyboard shortcuts (Phase 1 & 2)
    
    def press_ctrl_s(self) -> bool:
        """Press Ctrl+S (Save) - Phase 1, Task 1.1 - ONLY in IDEs"""
        # CRITICAL: Only allow Ctrl+S in IDEs, not in browsers
        try:
            window_title = self.window_detector.get_active_window_title()
            
            # Whitelist: ONLY these applications are allowed for Ctrl+S
            allowed_apps = ['code', 'visual studio code', 'vscode', 'vs code', 'pycharm', 'intellij', 'sublime text', 'atom', 'notepad++', 'vim', 'emacs']
            is_allowed = any(app in window_title.lower() for app in allowed_apps)
            
            # Blacklist: NEVER use Ctrl+S in these applications
            blocked_apps = ['chrome', 'edge', 'firefox', 'brave', 'opera', 'safari', 'outlook', 'mail', 'gmail', 'powershell', 'cmd', 'terminal']
            is_blocked = any(app in window_title.lower() for app in blocked_apps)
            
            if is_blocked:
                logger.warning(f"Ctrl+S BLOCKED - dangerous window: {window_title}")
                return False
            
            if not is_allowed:
                logger.warning(f"Ctrl+S SKIPPED - not in IDE: {window_title}")
                return False
            
            logger.info(f"✓ Ctrl+S ALLOWED in IDE: {window_title}")
        except Exception as e:
            logger.error(f"Window detection FAILED: {e}, skipping Ctrl+S for safety")
            return False
        
        try:
            result = self.press_ctrl_key_combo("s")
            if result:
                # Post-save pause (0.2-0.5s)
                time.sleep(np.random.uniform(0.2, 0.5))
                logger.info("Pressed Ctrl+S (Save)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+S: {e}")
            return False

    def press_ctrl_f(self) -> bool:
        """Press Ctrl+F (Find/Search) - Phase 1, Task 1.3 - ONLY in IDEs"""
        # CRITICAL: Only allow Ctrl+F in IDEs, not in browsers
        try:
            window_title = self.window_detector.get_active_window_title()
            
            # Whitelist: ONLY these applications are allowed for Ctrl+F
            allowed_apps = ['code', 'visual studio code', 'vscode', 'vs code', 'pycharm', 'intellij', 'sublime text', 'atom', 'notepad++', 'vim', 'emacs']
            is_allowed = any(app in window_title.lower() for app in allowed_apps)
            
            # Blacklist: NEVER use Ctrl+F in these applications
            blocked_apps = ['chrome', 'edge', 'firefox', 'brave', 'opera', 'safari', 'outlook', 'mail', 'gmail', 'powershell', 'cmd', 'terminal']
            is_blocked = any(app in window_title.lower() for app in blocked_apps)
            
            if is_blocked:
                logger.warning(f"Ctrl+F BLOCKED - dangerous window: {window_title}")
                return False
            
            if not is_allowed:
                logger.warning(f"Ctrl+F SKIPPED - not in IDE: {window_title}")
                return False
        except Exception as e:
            logger.error(f"Window detection FAILED: {e}, skipping Ctrl+F for safety")
            return False
        
        try:
            result = self.press_ctrl_key_combo("f")
            if result:
                # Pause for search dialog to open (100-200ms)
                time.sleep(np.random.uniform(0.1, 0.2))
                logger.info("Pressed Ctrl+F (Search)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+F: {e}")
            return False

    def press_escape(self) -> bool:
        """Press Escape key (close dialogs) - Phase 1, Task 1.3"""
        try:
            self.injector.press_key(VK_CODES["escape"])
            logger.debug("Pressed Escape")
            return True
        except Exception as e:
            logger.error(f"Failed to press Escape: {e}")
            return False

    def press_home(self) -> bool:
        """Press Home key (line start) - Phase 1, Task 1.5"""
        try:
            self.injector.press_key(VK_CODES["home"])
            # Cursor positioning pause (50-150ms)
            time.sleep(np.random.uniform(0.05, 0.15))
            logger.debug("Pressed Home")
            return True
        except Exception as e:
            logger.error(f"Failed to press Home: {e}")
            return False

    def press_end(self) -> bool:
        """Press End key (line end) - Phase 1, Task 1.5"""
        try:
            self.injector.press_key(VK_CODES["end"])
            # Cursor positioning pause (50-150ms)
            time.sleep(np.random.uniform(0.05, 0.15))
            logger.debug("Pressed End")
            return True
        except Exception as e:
            logger.error(f"Failed to press End: {e}")
            return False

    def press_ctrl_z(self) -> bool:
        """Press Ctrl+Z (Undo) - Phase 2, Task 2.1"""
        try:
            result = self.press_ctrl_key_combo("z")
            if result:
                # Undo pause (200-400ms)
                time.sleep(np.random.uniform(0.2, 0.4))
                logger.info("Pressed Ctrl+Z (Undo)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+Z: {e}")
            return False

    def press_ctrl_y(self) -> bool:
        """Press Ctrl+Y (Redo) - Phase 2, Task 2.1"""
        try:
            result = self.press_ctrl_key_combo("y")
            if result:
                # Redo pause (200-400ms)
                time.sleep(np.random.uniform(0.2, 0.4))
                logger.info("Pressed Ctrl+Y (Redo)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+Y: {e}")
            return False

    def press_ctrl_c(self) -> bool:
        """Press Ctrl+C (Copy) - Phase 2, Task 2.5"""
        try:
            result = self.press_ctrl_key_combo("c")
            if result:
                # Clipboard operation pause (100-200ms)
                time.sleep(np.random.uniform(0.1, 0.2))
                logger.info("Pressed Ctrl+C (Copy)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+C: {e}")
            return False

    def press_ctrl_v(self) -> bool:
        """Press Ctrl+V (Paste) - Phase 2, Task 2.5"""
        try:
            result = self.press_ctrl_key_combo("v")
            if result:
                # Paste completion pause (200-500ms)
                time.sleep(np.random.uniform(0.2, 0.5))
                logger.info("Pressed Ctrl+V (Paste)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+V: {e}")
            return False

    def press_ctrl_slash(self) -> bool:
        """Press Ctrl+/ (Toggle Comment) - Phase 2, Task 2.6"""
        try:
            result = self.press_ctrl_key_combo("/")
            if result:
                # Comment operation pause (150-300ms)
                time.sleep(np.random.uniform(0.15, 0.3))
                logger.info("Pressed Ctrl+/ (Toggle Comment)")
            return result
        except Exception as e:
            logger.error(f"Failed to press Ctrl+/: {e}")
            return False

    def type_search_term(self) -> bool:
        """Type a search term with deliberate speed - Phase 1, Task 1.3"""
        try:
            # Common code search terms
            search_terms = [
                "def ", "class ", "import ", "return ", "function",
                "TODO", "FIXME", "self.", "const ", "var ", "let "
            ]
            term = np.random.choice(search_terms)
            
            # Type slowly and deliberately (80-150ms per char)
            for char in term:
                self.injector.type_text(char, delay=np.random.uniform(0.08, 0.15))
            
            logger.info(f"Typed search term: {term}")
            return True
        except Exception as e:
            logger.error(f"Failed to type search term: {e}")
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
    # Phase 1 Developer Workflows
    
    def search_workflow(self) -> bool:
        """Simulate code search workflow - Phase 1, Task 1.3"""
        try:
            logger.info("Starting search workflow")
            
            # Open search dialog (Ctrl+F)
            if not self.keyboard.press_ctrl_f():
                return False
            
            # Type search term
            if not self.keyboard.type_search_term():
                return False
            
            # Execute search (Enter)
            self.keyboard.injector.press_key(VK_CODES["enter"])
            time.sleep(0.1)
            
            # Read search results (1-3s)
            time.sleep(np.random.uniform(1.0, 3.0))
            
            # Close search dialog (Escape)
            self.keyboard.press_escape()
            
            # Brief pause after closing
            time.sleep(np.random.uniform(0.3, 0.8))
            
            logger.info("Completed search workflow")
            return True
        except Exception as e:
            logger.error(f"Failed search workflow: {e}")
            return False

    def read_code_section(self) -> bool:
        """Read code with scrolling and pauses - Phase 1, Task 1.4"""
        try:
            logger.info("Starting read-code-section")
            
            # Scroll 2-4 times with reading pauses
            scroll_count = np.random.randint(2, 5)
            for _ in range(scroll_count):
                self.mouse.scroll_activity(np.random.choice(["up", "down"]))
                # Reading pause (1.5-3.5s)
                time.sleep(np.random.uniform(1.5, 3.5))
            
            logger.info(f"Read code section ({scroll_count} scrolls)")
            return True
        except Exception as e:
            logger.error(f"Failed read code section: {e}")
            return False

    def edit_with_selection_workflow(self) -> bool:
        """Edit with word selection - Phase 1, Task 1.2"""
        try:
            logger.info("Starting edit-with-selection workflow")
            
            # Double-click to select word
            if not self.mouse.double_click_word():
                return False
            
            # Brief pause before typing replacement
            time.sleep(np.random.uniform(0.1, 0.3))
            
            # Type replacement text (short snippet)
            snippet = self.keyboard.snippet_generator.get_snippet(".py")
            # Take first line only
            first_line = snippet.split('\n')[0] if snippet else "updated_value"
            
            for char in first_line[:30]:  # Limit to 30 chars
                self.keyboard.injector.type_text(char, delay=np.random.uniform(0.05, 0.1))
            
            # Save after editing
            time.sleep(np.random.uniform(0.3, 0.8))
            self.keyboard.press_ctrl_s()
            
            logger.info("Completed edit-with-selection workflow")
            return True
        except Exception as e:
            logger.error(f"Failed edit-with-selection workflow: {e}")
            return False

    def edit_at_line_boundary(self) -> bool:
        """Edit at line start/end with Home/End - Phase 1, Task 1.5"""
        try:
            logger.info("Starting edit-at-line-boundary")
            
            # Choose Home or End
            if np.random.random() < 0.5:
                self.keyboard.press_home()
                position = "start"
            else:
                self.keyboard.press_end()
                position = "end"
            
            # Type something brief
            text = "# " if position == "start" else "  # comment"
            for char in text:
                self.keyboard.injector.type_text(char, delay=np.random.uniform(0.05, 0.1))
            
            time.sleep(np.random.uniform(0.2, 0.5))
            
            logger.info(f"Completed edit at line {position}")
            return True
        except Exception as e:
            logger.error(f"Failed edit-at-line-boundary: {e}")
            return False

    def brave_browsing_workflow(self) -> bool:
        """Switch to Brave browser and scroll - natural browsing behavior"""
        try:
            logger.info("Starting Brave browsing workflow")
            
            # Alt+Tab to switch windows (likely to Brave if it's open)
            logger.info("Pressing Alt+Tab to switch to Brave browser")
            self.keyboard.injector.press_key(VK_CODES["alt"], hold=True)
            time.sleep(0.05)
            self.keyboard.injector.press_key(VK_CODES["tab"], hold_time=0.05)
            time.sleep(0.1)
            self.keyboard.injector.press_key(VK_CODES["alt"], hold=False)
            
            # Wait for window switch to complete
            time.sleep(np.random.uniform(0.3, 0.6))
            
            # Now in Brave - do natural scrolling behavior
            scroll_count = np.random.randint(3, 8)  # 3-7 scrolls
            for i in range(scroll_count):
                # Scroll down or up (mostly down)
                direction = "down" if np.random.random() < 0.8 else "up"
                self.mouse.scroll_activity(direction)
                
                # Natural pause between scrolls (reading content)
                time.sleep(np.random.uniform(1.5, 4.0))
                
                # Occasional small mouse movement (adjusting position)
                if np.random.random() < 0.3:
                    self.mouse.small_mouse_jitter()
                    time.sleep(np.random.uniform(0.3, 0.8))
            
            logger.info(f"Completed Brave browsing workflow ({scroll_count} scrolls)")
            return True
        except Exception as e:
            logger.error(f"Failed Brave browsing workflow: {e}")
            return False
            return False