"""
Monitoring software detection and adaptive behavior
"""
import psutil
import logging
from typing import List, Dict, Set
import ctypes

logger = logging.getLogger(__name__)


class MonitoringDetector:
    """Detect monitoring software and adapt behavior"""

    KNOWN_MONITORS = {
        "insightful.exe",
        "timedoctor.exe",
        "hubstaff.exe",
        "activtrak.exe",
        "teramind.exe",
        "workpuls.exe",
        "desktime.exe",
        "timecampdesktop.exe",
        "worksnaps.exe",
    }

    def __init__(self):
        self.detected_monitors: Set[str] = set()
        self.adaptive_mode = False
        self.hook_detected = False

    def scan_processes(self) -> List[str]:
        """Scan for known monitoring processes"""
        detected = []
        try:
            for proc in psutil.process_iter(["name"]):
                try:
                    proc_name = proc.info["name"].lower()
                    if proc_name in self.KNOWN_MONITORS:
                        detected.append(proc_name)
                        self.detected_monitors.add(proc_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Failed to scan processes: {e}")

        return detected

    def detect_api_hooks(self) -> bool:
        """Detect Windows API hooks (basic detection)"""
        try:
            user32 = ctypes.windll.user32
            
            hook_count = 0
            for hook_type in [2, 3, 4, 5, 7, 8, 13, 14]:
                try:
                    result = user32.GetWindowsHookExW(hook_type, None, None, 0)
                    if result:
                        hook_count += 1
                except:
                    pass

            self.hook_detected = hook_count > 3
            return self.hook_detected
        except Exception as e:
            logger.error(f"Failed to detect API hooks: {e}")
            return False

    def check_monitoring(self) -> Dict[str, any]:
        """Comprehensive monitoring check"""
        processes = self.scan_processes()
        hooks = self.detect_api_hooks()

        detected = len(processes) > 0 or hooks

        if detected and not self.adaptive_mode:
            self.adaptive_mode = True
            logger.warning(f"Monitoring software detected: {processes}")
            logger.info("Switching to adaptive mode")
        elif not detected and self.adaptive_mode:
            self.adaptive_mode = False
            logger.info("No monitoring detected, returning to normal mode")

        return {
            "detected": detected,
            "processes": processes,
            "hooks_detected": hooks,
            "adaptive_mode": self.adaptive_mode,
        }

    def is_adaptive_mode(self) -> bool:
        """Check if in adaptive mode"""
        return self.adaptive_mode

    def get_adaptive_multiplier(self) -> float:
        """Get timing multiplier for adaptive mode"""
        if self.adaptive_mode:
            return 1.3
        return 1.0
