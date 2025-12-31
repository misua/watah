"""
Azure Portal Configuration Helper
Assists with Azure portal navigation and resource management
"""
import time
import logging
import numpy as np
import ctypes
from typing import Tuple, List
import yaml

from win32_input import Win32InputInjector, VK_CODES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='azure_config.log',
    filemode='a'
)
logger = logging.getLogger('AzurePortalHelper')

user32 = ctypes.windll.user32


class WindowDetector:
    """Detect active window and browser"""
    
    @staticmethod
    def get_active_window_title() -> str:
        """Get title of active window"""
        try:
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value
        except Exception as e:
            logger.error(f"Failed to get window title: {e}")
            return ""
    
    @staticmethod
    def is_browser_active() -> bool:
        """Check if a browser window is active"""
        title = WindowDetector.get_active_window_title()
        browsers = ['chrome', 'edge', 'firefox', 'brave', 'opera', 'safari']
        return any(browser in title.lower() for browser in browsers)


class AzurePortalHelper:
    """Azure portal navigation and configuration assistant"""
    
    def __init__(self, config: dict):
        self.config = config
        self.injector = Win32InputInjector()
        self.window_detector = WindowDetector()
        
        # Define safe click zones (relative to screen size)
        self.zones = {
            'sidebar': {
                'x_range': (0.05, 0.20),  # Left 5-20% of screen
                'y_range': (0.30, 0.80)   # Middle 30-80% vertically
            },
            'content': {
                'x_range': (0.25, 0.85),  # Center 25-85% of screen
                'y_range': (0.25, 0.75)   # Middle 25-75% vertically
            },
            'tabs': {
                'x_range': (0.15, 0.70),  # Top center 15-70%
                'y_range': (0.08, 0.12)   # Top 8-12% (tab area)
            }
        }
        
        logger.info("Azure Portal Helper initialized")
    
    def get_random_point_in_zone(self, zone_name: str) -> Tuple[int, int]:
        """Get random coordinates within a safe zone"""
        zone = self.zones.get(zone_name)
        if not zone:
            raise ValueError(f"Unknown zone: {zone_name}")
        
        x_min = int(self.injector.screen_width * zone['x_range'][0])
        x_max = int(self.injector.screen_width * zone['x_range'][1])
        y_min = int(self.injector.screen_height * zone['y_range'][0])
        y_max = int(self.injector.screen_height * zone['y_range'][1])
        
        x = np.random.randint(x_min, x_max)
        y = np.random.randint(y_min, y_max)
        
        return x, y
    
    def click_in_zone(self, zone_name: str) -> bool:
        """Click at random position in specified zone"""
        try:
            x, y = self.get_random_point_in_zone(zone_name)
            
            # Move mouse smoothly to position
            current_x, current_y = self.injector.get_cursor_position()
            steps = 20
            for i in range(steps):
                progress = (i + 1) / steps
                new_x = int(current_x + (x - current_x) * progress)
                new_y = int(current_y + (y - current_y) * progress)
                self.injector.move_mouse_absolute(new_x, new_y)
                time.sleep(0.01)
            
            # Click
            time.sleep(0.1)
            self.injector.click_mouse("left")
            logger.info(f"Clicked in {zone_name} at ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Failed to click in zone {zone_name}: {e}")
            return False
    
    def switch_tab(self) -> bool:
        """Switch to next browser tab using Ctrl+Tab"""
        try:
            self.injector.press_key(VK_CODES["control"], hold=True)
            time.sleep(0.05)
            self.injector.press_key(VK_CODES["tab"])
            time.sleep(0.05)
            self.injector.press_key(VK_CODES["control"], hold=False)
            logger.info("Switched browser tab")
            return True
        except Exception as e:
            logger.error(f"Failed to switch tab: {e}")
            return False
    
    def scroll(self, direction: str = "down") -> bool:
        """Scroll the page"""
        try:
            scroll_count = np.random.randint(2, 5)
            for _ in range(scroll_count):
                amount = 120 if direction == "down" else -120
                self.injector.scroll_mouse(amount)
                time.sleep(np.random.uniform(0.15, 0.3))
            logger.info(f"Scrolled {direction} {scroll_count} times")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll: {e}")
            return False
    
    def select_activity(self) -> str:
        """Select random activity based on weights"""
        activities = list(self.config['activities'].keys())
        weights = [self.config['activities'][a]['weight'] for a in activities]
        
        # Normalize weights
        total = sum(weights)
        probabilities = [w / total for w in weights]
        
        return np.random.choice(activities, p=probabilities)
    
    def execute_activity(self, activity: str) -> bool:
        """Execute the selected activity"""
        if activity == 'click_content':
            return self.click_in_zone('content')
        elif activity == 'click_sidebar':
            return self.click_in_zone('sidebar')
        elif activity == 'switch_tab':
            return self.switch_tab()
        elif activity == 'scroll_down':
            return self.scroll('down')
        elif activity == 'scroll_up':
            return self.scroll('up')
        else:
            logger.warning(f"Unknown activity: {activity}")
            return False
    
    def run(self):
        """Main loop"""
        logger.info("Starting Azure portal configuration service...")
        logger.info("Service running in background")
        
        try:
            while True:
                # Check if browser is active
                if not self.window_detector.is_browser_active():
                    logger.warning("Browser not active, waiting...")
                    time.sleep(5)
                    continue
                
                # Select and execute activity
                activity = self.select_activity()
                logger.info(f">>> Executing: {activity}")
                
                success = self.execute_activity(activity)
                if success:
                    logger.info(f"✓ {activity} completed")
                else:
                    logger.error(f"✗ {activity} failed")
                
                # Wait before next activity
                interval = np.random.uniform(
                    self.config['timing']['min_interval'],
                    self.config['timing']['max_interval']
                )
                logger.info(f"Next activity in {interval:.1f} seconds")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Stopping Azure portal configuration service...")


def load_config(config_file: str = 'config.yaml') -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(f"Config file {config_file} not found, using defaults")
        return {
            'timing': {
                'min_interval': 5,
                'max_interval': 15
            },
            'activities': {
                'click_content': {'weight': 0.40},
                'click_sidebar': {'weight': 0.30},
                'switch_tab': {'weight': 0.20},
                'scroll_down': {'weight': 0.08},
                'scroll_up': {'weight': 0.02}
            }
        }


if __name__ == '__main__':
    config = load_config()
    helper = AzurePortalHelper(config)
    helper.run()
