"""
Smart Monitor Scheduler
Alternates between GCP and Azure monitors based on active window context
"""
import os
import sys
import time
import random
import subprocess
import logging
from datetime import datetime, timedelta
from typing import Optional, List
import signal
import ctypes
import traceback

# Setup logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scheduler_debug.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8', mode='w'),  # Overwrite each run
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Logging to: {log_file}")


class WindowDetector:
    """Detect and switch active windows"""
    
    @staticmethod
    def get_active_window_title() -> str:
        """Get the title of the active window"""
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value.lower()
            logger.debug(f"Active window: '{title}'")
            return title
        except Exception as e:
            logger.error(f"Failed to get window title: {e}")
            return ""
    
    @staticmethod
    def find_window_by_keywords(keywords: List[str]) -> Optional[int]:
        """Find a window handle by title keywords"""
        logger.debug(f"Searching for windows with keywords: {keywords}")
        user32 = ctypes.windll.user32
        
        def enum_windows_callback(hwnd, results):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value.lower()
                    if any(keyword in title for keyword in keywords):
                        logger.debug(f"Found matching window: '{title}' (hwnd: {hwnd})")
                        results.append(hwnd)
            return True
        
        results = []
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.py_object)
        user32.EnumWindows(EnumWindowsProc(enum_windows_callback), results)
        logger.debug(f"Found {len(results)} matching windows")
        return results[0] if results else None
    
    @staticmethod
    def focus_window(hwnd: int) -> bool:
        """Bring a window to the foreground"""
        try:
            user32 = ctypes.windll.user32
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            user32.SetForegroundWindow(hwnd)
            time.sleep(0.5)  # Give time for window to focus
            return True
        except Exception as e:
            logger.error(f"Failed to focus window: {e}")
            return False
    
    @staticmethod
    def switch_to_browser() -> bool:
        """Switch focus to a browser window"""
        browser_keywords = [
            'chrome', 'firefox', 'edge', 'brave', 'opera',
            'mozilla', 'safari'
        ]
        hwnd = WindowDetector.find_window_by_keywords(browser_keywords)
        if hwnd:
            logger.info("Switching to browser window")
            return WindowDetector.focus_window(hwnd)
        logger.warning("No browser window found")
        return False
    
    @staticmethod
    def switch_to_ide() -> bool:
        """Switch focus to an IDE window"""
        ide_keywords = [
            'visual studio code', 'vscode', 'pycharm', 'intellij',
            'eclipse', 'sublime', 'atom', 'webstorm', 'phpstorm',
            'rider', 'clion', 'netbeans'
        ]
        hwnd = WindowDetector.find_window_by_keywords(ide_keywords)
        if hwnd:
            logger.info("Switching to IDE window")
            return WindowDetector.focus_window(hwnd)
        logger.warning("No IDE window found")
        return False
    
    @staticmethod
    def is_browser_active() -> bool:
        """Check if a browser window is active"""
        title = WindowDetector.get_active_window_title()
        browser_keywords = [
            'chrome', 'firefox', 'edge', 'brave', 'opera',
            'mozilla', 'browser', 'safari'
        ]
        return any(keyword in title for keyword in browser_keywords)
    
    @staticmethod
    def is_ide_active() -> bool:
        """Check if an IDE window is active"""
        title = WindowDetector.get_active_window_title()
        ide_keywords = [
            'visual studio code', 'vscode', 'pycharm', 'intellij',
            'eclipse', 'sublime', 'atom', 'notepad++', 'vim',
            'emacs', 'webstorm', 'phpstorm', 'rider', 'clion'
        ]
        return any(keyword in title for keyword in ide_keywords)
    
    @staticmethod
    def get_preferred_monitor() -> Optional[str]:
        """Get preferred monitor based on active window"""
        if WindowDetector.is_browser_active():
            return 'azure'
        elif WindowDetector.is_ide_active():
            return 'gcp'
        return None


class MonitorScheduler:
    """Schedules and alternates between GCP and Azure monitors"""
    
    def __init__(self, testing_mode=False):
        logger.info("=" * 60)
        logger.info("Initializing MonitorScheduler")
        logger.info(f"Testing mode: {testing_mode}")
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.gcp_dir = os.path.join(self.base_dir, 'gcp_active_monitor')
        self.azure_dir = os.path.join(self.base_dir, 'azure_monitor')
        
        logger.info(f"Base directory: {self.base_dir}")
        logger.info(f"GCP directory: {self.gcp_dir}")
        logger.info(f"Azure directory: {self.azure_dir}")
        logger.info(f"GCP dir exists: {os.path.exists(self.gcp_dir)}")
        logger.info(f"Azure dir exists: {os.path.exists(self.azure_dir)}")
        
        self.current_process: Optional[subprocess.Popen] = None
        self.current_monitor = None
        self.should_stop = False
        self.testing_mode = testing_mode
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("MonitorScheduler initialized successfully")
        logger.info("=" * 60)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.should_stop = True
        self.stop_current_monitor()
        sys.exit(0)
    
    def is_work_hours(self) -> bool:
        """Check if it's during realistic work hours"""
        logger.debug("Checking work hours...")
        
        if self.testing_mode:
            logger.debug("Testing mode - always work hours")
            return True
        
        now = datetime.now()
        logger.debug(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S %A')}")
        
        # Weekend check - 20% chance of working on weekends
        if now.weekday() >= 5:  # Saturday=5, Sunday=6
            if random.random() > 0.2:
                logger.info("It's the weekend, skipping (80% chance)")
                return False
            logger.info("Working on weekend (20% chance)")
        
        # Work hours: 8 AM - 6 PM with some variance
        # Add ±2 hours randomness for realistic start/end times
        work_start = 8 + random.randint(-2, 2)  # 6-10 AM
        work_end = 18 + random.randint(-2, 2)   # 4-8 PM
        
        logger.debug(f"Work hours today: {work_start}:00 - {work_end}:00")
        
        current_hour = now.hour
        
        if work_start <= current_hour < work_end:
            logger.info(f"Within work hours ({current_hour}:00 is between {work_start}:00-{work_end}:00)")
            return True
        
        logger.info(f"Outside work hours ({current_hour}:00 is not between {work_start}:00-{work_end}:00)")
        return False
    
    def get_session_duration(self) -> int:
        """Get random session duration for a monitor (30-90 minutes or 2 min for testing)"""
        if self.testing_mode:
            logger.debug("Testing mode: using 2 minute session")
            return 2  # 2 minutes for testing
        
        # Most sessions are 45-60 minutes, with occasional longer/shorter ones
        weights = [0.1, 0.3, 0.4, 0.15, 0.05]  # Distribution weights
        durations = [30, 45, 60, 75, 90]       # Minutes
        
        duration = random.choices(durations, weights=weights)[0]
        
        # Add small random variance (±5 minutes)
        duration += random.randint(-5, 5)
        
        return max(25, min(95, duration))  # Clamp between 25-95 minutes
    
    def should_take_break(self) -> bool:
        """Randomly decide if we should take a break (15% chance)"""
        return random.random() < 0.15
    
    def get_break_duration(self) -> int:
        """Get break duration in minutes"""
        # Short breaks (5-15 min) or lunch breaks (30-60 min)
        if random.random() < 0.7:  # 70% short breaks
            return random.randint(5, 15)
        else:  # 30% lunch breaks
            return random.randint(30, 60)
    
    def choose_next_monitor(self) -> str:
        """Choose which monitor to run next based on active window"""
        logger.debug("Choosing next monitor...")
        
        # Try to detect preferred monitor from active window
        preferred = WindowDetector.get_preferred_monitor()
        
        if preferred:
            logger.info(f"Detected {'browser' if preferred == 'azure' else 'IDE'} window, using {preferred.upper()} monitor")
            return preferred
        
        # No clear window context - alternate between monitors
        if self.current_monitor is None:
            # First run - 50/50 choice
            monitor = random.choice(['gcp', 'azure'])
            logger.info(f"No specific window detected, choosing {monitor.upper()} monitor")
            return monitor
        elif self.current_monitor == 'gcp':
            # 70% switch to azure, 30% stay with gcp
            return 'azure' if random.random() < 0.7 else 'gcp'
        else:
            # 70% switch to gcp, 30% stay with azure
            return 'gcp' if random.random() < 0.7 else 'azure'
    
    def start_monitor(self, monitor_type: str) -> bool:
        """Start a monitor (gcp or azure) and switch to appropriate window"""
        try:
            logger.info(f"start_monitor called for: {monitor_type}")
            
            # First, switch to the appropriate window for this monitor
            if monitor_type == 'gcp':
                logger.info("Attempting to switch to IDE...")
                if not WindowDetector.switch_to_ide():
                    logger.warning("Could not switch to IDE, monitor may not work optimally")
                script_path = os.path.join(self.gcp_dir, 'gcp_monitoring.py')
                cwd = self.gcp_dir
                logger.info("Starting GCP monitor...")
            else:  # azure
                logger.info("Attempting to switch to browser...")
                if not WindowDetector.switch_to_browser():
                    logger.warning("Could not switch to browser, monitor may not work optimally")
                script_path = os.path.join(self.azure_dir, 'azure_setup.py')
                cwd = self.azure_dir
                logger.info("Starting Azure monitor...")
            
            # Check if script exists
            logger.info(f"Looking for script: {script_path}")
            if not os.path.exists(script_path):
                logger.error(f"Monitor script not found: {script_path}")
                return False
            logger.info(f"Script found!")
            
            # Give window switch time to complete
            logger.debug("Waiting for window switch to complete...")
            time.sleep(1)
            
            # Start the monitor process
            # Use pythonw on Windows to avoid console window
            python_cmd = 'pythonw' if sys.platform == 'win32' else 'python3'
            logger.info(f"Starting process: {python_cmd} {script_path}")
            logger.info(f"Working directory: {cwd}")
            
            self.current_process = subprocess.Popen(
                [python_cmd, script_path],
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            self.current_monitor = monitor_type
            logger.info(f"{monitor_type.upper()} monitor started (PID: {self.current_process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start {monitor_type} monitor: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def stop_current_monitor(self):
        """Stop the currently running monitor"""
        if self.current_process is None:
            logger.debug("No process to stop")
            return
        
        try:
            logger.info(f"Stopping {self.current_monitor} monitor (PID: {self.current_process.pid})...")
            
            # Try graceful shutdown first
            self.current_process.terminate()
            
            # Wait up to 5 seconds for graceful shutdown
            try:
                self.current_process.wait(timeout=5)
                logger.info("Process terminated gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                logger.warning("Monitor not responding, forcing shutdown...")
                self.current_process.kill()
                self.current_process.wait()
                logger.info("Process killed")
            
            logger.info(f"{self.current_monitor} monitor stopped")
            
        except Exception as e:
            logger.error(f"Error stopping monitor: {e}")
            logger.error(traceback.format_exc())
        finally:
            self.current_process = None
            self.current_monitor = None
    
    def run_session(self):
        """Run a single monitoring session with window context awareness"""
        logger.info("=" * 60)
        logger.info("Starting new session")
        
        # Choose which monitor to run
        monitor_type = self.choose_next_monitor()
        session_duration = self.get_session_duration()
        
        logger.info(f"Chosen monitor: {monitor_type.upper()}")
        logger.info(f"Session duration: {session_duration} minutes")
        
        # Start the monitor
        if not self.start_monitor(monitor_type):
            logger.error("Failed to start monitor, waiting 5 minutes before retry...")
            time.sleep(300)
            return
        
        # Run for the session duration with periodic window checks
        start_time = time.time()
        end_time = start_time + (session_duration * 60)
        last_context_check = time.time()
        
        logger.info(f"Session will run until {datetime.fromtimestamp(end_time).strftime('%H:%M:%S')}")
        
        iteration = 0
        while time.time() < end_time and not self.should_stop:
            iteration += 1
            remaining_min = (end_time - time.time()) / 60
            logger.debug(f"Session check iteration {iteration}, remaining: {remaining_min:.1f} min")
            
            # Check if process is still running
            poll_result = self.current_process.poll()
            if poll_result is not None:
                logger.warning(f"{monitor_type} monitor process ended unexpectedly")
                logger.warning(f"Exit code: {poll_result}")
                # Try to capture any output
                try:
                    stdout, stderr = self.current_process.communicate(timeout=1)
                    if stdout:
                        logger.debug(f"Process stdout: {stdout.decode('utf-8', errors='ignore')[:500]}")
                    if stderr:
                        logger.debug(f"Process stderr: {stderr.decode('utf-8', errors='ignore')[:500]}")
                except:
                    pass
                break
            
            # Every 2 minutes, verify we're still on the right window
            if time.time() - last_context_check > 120:
                logger.debug("Checking window context...")
                current_context = WindowDetector.get_preferred_monitor()
                logger.debug(f"Current context: {current_context}, Expected: {monitor_type}")
                
                if current_context != monitor_type:
                    logger.info(f"Window context mismatch, refocusing...")
                    # Try to refocus the correct window
                    if monitor_type == 'gcp':
                        WindowDetector.switch_to_ide()
                    else:
                        WindowDetector.switch_to_browser()
                last_context_check = time.time()
            
            # Sleep for 30 seconds before checking again
            time.sleep(30)
        
        # Stop the monitor
        self.stop_current_monitor()
        
        elapsed = (time.time() - start_time) / 60
        logger.info(f"Session completed ({elapsed:.1f} minutes)")
        logger.info("=" * 60)
    
    def run(self):
        """Main scheduler loop"""
        logger.info("=" * 60)
        logger.info("Monitor Scheduler STARTED")
        logger.info("=" * 60)
        
        loop_iteration = 0
        while not self.should_stop:
            loop_iteration += 1
            logger.info(f"\n>>> Main loop iteration {loop_iteration}")
            
            try:
                # Check if we're in work hours
                if not self.is_work_hours():
                    now = datetime.now()
                    # Calculate next work day start (around 8 AM)
                    next_day = now + timedelta(days=1)
                    next_start = next_day.replace(hour=8, minute=0, second=0)
                    wait_seconds = (next_start - now).total_seconds()
                    
                    logger.info(f"Outside work hours. Sleeping until {next_start.strftime('%Y-%m-%d %H:%M')}")
                    logger.info(f"Sleep duration: {wait_seconds/3600:.1f} hours")
                    
                    # Sleep in chunks to allow for shutdown signals
                    while wait_seconds > 0 and not self.should_stop:
                        sleep_time = min(300, wait_seconds)  # Sleep max 5 minutes at a time
                        time.sleep(sleep_time)
                        wait_seconds -= sleep_time
                    
                    continue
                
                # Run a monitoring session
                logger.info("Work hours confirmed, running session...")
                self.run_session()
                
                # Decide if we should take a break
                if self.should_take_break():
                    break_duration = self.get_break_duration()
                    logger.info(f"Taking a break for {break_duration} minutes")
                    
                    # Sleep in chunks
                    remaining = break_duration * 60
                    while remaining > 0 and not self.should_stop:
                        sleep_time = min(60, remaining)
                        time.sleep(sleep_time)
                        remaining -= sleep_time
                else:
                    # Short pause between sessions (2-5 minutes)
                    pause = random.randint(2, 5)
                    logger.info(f"Brief pause ({pause} minutes) before next session")
                    time.sleep(pause * 60)
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                logger.error(traceback.format_exc())
                time.sleep(60)  # Wait a minute before retrying
        
        logger.info("Monitor Scheduler STOPPED")


def main():
    """Entry point"""
    
    # Check for testing mode flag
    testing_mode = '--test' in sys.argv or '-t' in sys.argv
    
    logger.info("=" * 60)
    logger.info("Smart Monitor Scheduler")
    logger.info("Window-aware: Browser→Azure, IDE→GCP")
    if testing_mode:
        logger.info("TESTING MODE: 2-minute intervals")
    else:
        logger.info("Production mode: 30-90 minute sessions during work hours")
    logger.info("=" * 60)
    
    scheduler = MonitorScheduler(testing_mode=testing_mode)
    
    try:
        scheduler.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
    finally:
        scheduler.stop_current_monitor()


if __name__ == '__main__':
    main()
