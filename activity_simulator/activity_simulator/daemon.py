"""
Daemon controller for Windows background service
"""
import os
import sys
import time
import logging
import signal
import atexit
from pathlib import Path
from typing import Optional
from pynput import mouse, keyboard as kb
from .config import Config
from .win32_input import Win32InputInjector
from .activities import MouseActivity, KeyboardActivity, CompositeActivity
from .timing import TimingRandomizer, BehavioralPatternModel
from .monitoring import MonitoringDetector
import numpy as np

logger = logging.getLogger(__name__)


class ActivityDaemon:
    """Main daemon for activity simulation"""

    def __init__(self, config: Config):
        self.config = config
        self.running = False
        self.paused = False
        self.last_user_input = time.time()
        self.pause_duration = config.get("safety.pause_duration", 30)

        self.injector = Win32InputInjector()
        self.mouse_activity = MouseActivity(self.injector)
        self.keyboard_activity = KeyboardActivity(self.injector)
        self.composite_activity = CompositeActivity(self.mouse_activity, self.keyboard_activity)

        self.timing = TimingRandomizer(config.get("timing", {}))
        self.behavioral_model = BehavioralPatternModel()
        self.monitor_detector = MonitoringDetector()

        self.activity_weights = self._build_activity_weights()
        self.last_monitoring_check = time.time()

        self.user_input_listener = None
        if config.get("safety.pause_on_user_input", True):
            self._setup_user_input_detection()

    def _build_activity_weights(self):
        """Build activity selection weights from config"""
        activities_config = self.config.get("activities", {})
        weights = {}

        for activity_name, activity_config in activities_config.items():
            if activity_config.get("enabled", True):
                weights[activity_name] = activity_config.get("weight", 0.1)

        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}

        return weights

    def _setup_user_input_detection(self):
        """Setup listeners for user input"""

        def on_mouse_activity(*args):
            self.last_user_input = time.time()
            if not self.paused:
                self.paused = True
                logger.info("User input detected, pausing simulation")

        def on_keyboard_activity(*args):
            self.last_user_input = time.time()
            if not self.paused:
                self.paused = True
                logger.info("User input detected, pausing simulation")

        try:
            mouse_listener = mouse.Listener(
                on_move=on_mouse_activity,
                on_click=on_mouse_activity,
                on_scroll=on_mouse_activity,
            )
            keyboard_listener = kb.Listener(on_press=on_keyboard_activity)

            mouse_listener.start()
            keyboard_listener.start()

            self.user_input_listener = (mouse_listener, keyboard_listener)
            logger.info("User input detection enabled")
        except Exception as e:
            logger.error(f"Failed to setup user input detection: {e}")

    def _check_resume(self):
        """Check if should resume after user input"""
        if self.paused:
            elapsed = time.time() - self.last_user_input
            if elapsed >= self.pause_duration:
                self.paused = False
                logger.info(f"Resuming simulation after {elapsed:.1f}s of inactivity")

    def _select_activity(self):
        """Select next activity based on weights and state"""
        if not self.activity_weights:
            return None

        activities = list(self.activity_weights.keys())
        weights = list(self.activity_weights.values())

        state = self.behavioral_model.get_current_state()
        if state == "typing":
            if "keyboard_typing" in activities:
                idx = activities.index("keyboard_typing")
                weights[idx] *= 2.0
        elif state == "browsing":
            if "mouse_scroll" in activities:
                idx = activities.index("mouse_scroll")
                weights[idx] *= 2.0

        total = sum(weights)
        weights = [w / total for w in weights]

        return np.random.choice(activities, p=weights)

    def _execute_activity(self, activity_name: str) -> bool:
        """Execute selected activity"""
        try:
            if activity_name == "mouse_movement":
                return self.mouse_activity.random_mouse_movement()
            elif activity_name == "mouse_scroll":
                direction = np.random.choice(["up", "down"], p=[0.3, 0.7])
                return self.mouse_activity.scroll_activity(direction)
            elif activity_name == "keyboard_navigation":
                return self.keyboard_activity.press_navigation_key()
            elif activity_name == "keyboard_typing":
                return self.keyboard_activity.type_random_text()
            elif activity_name == "tab_switching":
                return self.composite_activity.tab_switching_workflow()
            elif activity_name == "composite_workflows":
                workflow = np.random.choice(["file_editing", "browsing"])
                if workflow == "file_editing":
                    return self.composite_activity.file_editing_workflow()
                else:
                    return self.composite_activity.browsing_workflow()
            else:
                logger.warning(f"Unknown activity: {activity_name}")
                return False
        except Exception as e:
            logger.error(f"Failed to execute activity {activity_name}: {e}")
            return False

    def _check_monitoring(self):
        """Periodic monitoring software check"""
        now = time.time()
        interval = self.config.get("anti_detection.detection_interval", 300)

        if now - self.last_monitoring_check >= interval:
            self.last_monitoring_check = now
            result = self.monitor_detector.check_monitoring()
            logger.debug(f"Monitoring check: {result}")

    def run(self):
        """Main daemon loop"""
        self.running = True
        logger.info("Activity simulator daemon started")

        last_activity_time = time.time()

        while self.running:
            try:
                self._check_resume()

                if self.paused:
                    time.sleep(1)
                    continue

                self._check_monitoring()

                current_time = time.time()
                elapsed_since_activity = current_time - last_activity_time

                state = self.behavioral_model.get_current_state()
                interval = self.timing.get_next_interval(state)

                if self.monitor_detector.is_adaptive_mode():
                    interval *= self.monitor_detector.get_adaptive_multiplier()

                circadian_mult = self.timing.get_circadian_multiplier()
                interval *= circadian_mult

                if elapsed_since_activity >= interval:
                    activity_name = self._select_activity()
                    if activity_name:
                        logger.info(f"Executing activity: {activity_name} (state: {state})")
                        success = self._execute_activity(activity_name)

                        if success:
                            pause = self.timing.get_pause_duration(activity_name)
                            time.sleep(pause)

                        last_activity_time = current_time
                        self.behavioral_model.transition_state()

                elapsed = time.time() - current_time
                self.behavioral_model.update(elapsed)

                time.sleep(1)

            except KeyboardInterrupt:
                logger.info("Received interrupt signal, stopping...")
                self.stop()
            except Exception as e:
                logger.error(f"Error in daemon loop: {e}", exc_info=True)
                time.sleep(5)

    def stop(self):
        """Stop the daemon"""
        self.running = False
        if self.user_input_listener:
            try:
                self.user_input_listener[0].stop()
                self.user_input_listener[1].stop()
            except:
                pass
        logger.info("Activity simulator daemon stopped")


class DaemonController:
    """Controller for daemon lifecycle"""

    def __init__(self, config: Config):
        self.config = config
        self.pid_file = config.get("daemon.pid_file", "activity_sim.pid")

    def get_pid(self) -> Optional[int]:
        """Get PID from file"""
        try:
            if os.path.exists(self.pid_file):
                with open(self.pid_file, "r") as f:
                    return int(f.read().strip())
        except:
            pass
        return None

    def write_pid(self, pid: int):
        """Write PID to file"""
        try:
            with open(self.pid_file, "w") as f:
                f.write(str(pid))
        except Exception as e:
            logger.error(f"Failed to write PID file: {e}")

    def remove_pid(self):
        """Remove PID file"""
        try:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
        except Exception as e:
            logger.error(f"Failed to remove PID file: {e}")

    def is_running(self) -> bool:
        """Check if daemon is running"""
        pid = self.get_pid()
        if pid is None:
            return False

        try:
            import psutil

            return psutil.pid_exists(pid)
        except:
            return False

    def start(self):
        """Start daemon"""
        if self.is_running():
            logger.error("Daemon is already running")
            return False

        log_file = self.config.get("daemon.log_file", "activity_sim.log")
        log_level = self.config.get("daemon.log_level", "INFO")

        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

        self.write_pid(os.getpid())
        atexit.register(self.remove_pid)

        daemon = ActivityDaemon(self.config)
        daemon.run()

        return True

    def stop(self):
        """Stop daemon"""
        pid = self.get_pid()
        if pid is None:
            logger.error("Daemon is not running")
            return False

        try:
            import psutil

            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=10)
            self.remove_pid()
            logger.info("Daemon stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop daemon: {e}")
            return False

    def status(self):
        """Get daemon status"""
        if self.is_running():
            pid = self.get_pid()
            return {"running": True, "pid": pid}
        else:
            return {"running": False, "pid": None}
