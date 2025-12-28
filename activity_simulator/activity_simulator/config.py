"""
Configuration management
"""
import yaml
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "daemon": {
        "pid_file": "activity_sim.pid",
        "log_file": "activity_sim.log",
        "log_level": "INFO",
    },
    "timing": {
        "base_interval": 180,
        "intensity": "medium",
        "enable_circadian": True,
        "enable_end_of_day_shutdown": False,
    },
    "activities": {
        "mouse_movement": {"enabled": True, "weight": 0.3},
        "mouse_scroll": {"enabled": True, "weight": 0.25},
        "keyboard_navigation": {"enabled": True, "weight": 0.15},
        "keyboard_typing": {"enabled": True, "weight": 0.1},
        "tab_switching": {"enabled": True, "weight": 0.1},
        "composite_workflows": {"enabled": True, "weight": 0.1},
    },
    "safety": {
        "pause_on_user_input": True,
        "pause_duration": 30,
        "emergency_stop_hotkey": "ctrl+alt+q",
        "safe_zone": "current_screen",
    },
    "anti_detection": {
        "enable_monitoring_detection": True,
        "detection_interval": 300,
        "adaptive_behavior": True,
        "entropy_injection": True,
    },
}


class Config:
    """Configuration manager"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, path: str):
        """Load configuration from YAML file"""
        try:
            with open(path, "r") as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self._merge_config(self.config, user_config)
            logger.info(f"Loaded configuration from {path}")
        except Exception as e:
            logger.error(f"Failed to load config from {path}: {e}")

    def _merge_config(self, base: Dict, override: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def save_config(self, path: str):
        """Save configuration to YAML file"""
        try:
            with open(path, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)
            logger.info(f"Saved configuration to {path}")
        except Exception as e:
            logger.error(f"Failed to save config to {path}: {e}")

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration"""
        return self.config.copy()
