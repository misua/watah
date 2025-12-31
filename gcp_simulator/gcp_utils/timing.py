"""
Multi-layered timing randomization with behavioral patterns
"""
import numpy as np
from scipy import stats
from typing import Dict, Any
import time
import logging

logger = logging.getLogger(__name__)


class TimingRandomizer:
    """Multi-layered timing randomization engine"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_interval = config.get("base_interval", 180)
        self.intensity = config.get("intensity", "medium")
        self.last_activity_time = time.time()
        self.activity_history = []

    def get_next_interval(self, state: str = "work") -> float:
        """Get next activity interval - simple and aggressive for active coding"""
        if self.intensity == "high":
            base = 7
            variance = 3
        elif self.intensity == "medium":
            base = 15
            variance = 5
        else:
            base = 30
            variance = 10

        interval = base + np.random.uniform(-variance, variance)
        interval = max(3, min(20, interval))

        logger.debug(f"Next interval calculated: {interval:.1f}s")
        return interval

    def get_pause_duration(self, activity_type: str) -> float:
        """Get pause duration after activity"""
        if activity_type == "mouse_movement":
            base = 0.3
        elif activity_type == "mouse_scroll":
            base = 0.5
        elif activity_type == "keyboard_typing":
            base = 1.0
        elif activity_type == "keyboard_navigation":
            base = 0.2
        else:
            base = 0.5

        jitter = np.random.uniform(-0.1, 0.3)
        return max(0.1, base + jitter)

    def get_typing_delay(self) -> float:
        """Get delay between keystrokes"""
        base = np.random.gamma(2, 0.05)
        burst_factor = np.random.choice([1.0, 0.5, 0.3], p=[0.7, 0.2, 0.1])
        return base * burst_factor

    def get_mouse_movement_duration(self, distance: float) -> float:
        """Get duration for mouse movement based on distance"""
        base_speed = 1000
        duration = distance / base_speed
        jitter = np.random.uniform(0.8, 1.2)
        return max(0.1, duration * jitter)

    def should_take_break(self, work_duration: float) -> bool:
        """Determine if should take a break"""
        if work_duration < 1200:
            return False

        break_probability = min(0.8, (work_duration - 1200) / 1800)
        return np.random.random() < break_probability

    def get_circadian_multiplier(self, enable_end_of_day: bool = False) -> float:
        """Get activity multiplier based on time of day
        
        Returns:
            float: Multiplier for activity interval (higher = less frequent)
                   Returns float('inf') during natural break periods
                   Exits process if past end of day when enabled
        """
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min

        # Lunch break: 12:00pm-1:00pm (no activity)
        if hour == 12:
            logger.debug("Lunch break period: no activity")
            return float('inf')  # Effectively disables activity during lunch
        
        # Mid-morning coffee break: 10:30am-10:45am
        if hour == 10 and 30 <= minute < 45:
            logger.debug("Morning coffee break: no activity")
            return float('inf')
        
        # Afternoon coffee break: 3:00pm-3:15pm
        if hour == 15 and 0 <= minute < 15:
            logger.debug("Afternoon coffee break: no activity")
            return float('inf')
        
        # End of day shutdown (if enabled)
        if enable_end_of_day:
            # End of day: stop at random time between 4:00pm-4:30pm
            if not hasattr(self, '_stop_minute'):
                import random
                self._stop_minute = random.randint(0, 30)
                logger.info(f"End of day scheduled at 4:{self._stop_minute:02d}pm")
            
            if hour == 16 and minute >= self._stop_minute:
                logger.info(f"End of day reached at {hour}:{minute:02d}, stopping simulator")
                import sys
                sys.exit(0)
            
            # After 4:30pm, always stop
            if hour >= 17 or (hour == 16 and minute > 30):
                logger.info(f"Past end of day (4:30pm), stopping simulator")
                import sys
                sys.exit(0)

        # Work periods with different intensity levels
        if 9 <= hour < 12:
            return 1.0  # Morning: normal activity
        elif 13 <= hour < 14:  # After lunch, 1pm-2pm
            return 1.3  # Slightly slower after lunch
        elif 14 <= hour < 16:  # 2pm-4pm
            return 1.1  # Normal afternoon
        elif 19 <= hour < 22:
            return 1.2  # Evening work
        else:
            return 2.0  # Off-hours: very slow activity


class MarkovChain:
    """Markov chain for state transitions"""

    def __init__(self):
        self.states = ["work", "break", "reading", "typing", "browsing"]
        self.transition_matrix = {
            "work": {"work": 0.4, "break": 0.05, "reading": 0.15, "typing": 0.25, "browsing": 0.15},
            "break": {"work": 0.5, "break": 0.1, "reading": 0.1, "typing": 0.2, "browsing": 0.1},
            "reading": {"work": 0.2, "break": 0.05, "reading": 0.3, "typing": 0.3, "browsing": 0.15},
            "typing": {"work": 0.2, "break": 0.05, "reading": 0.1, "typing": 0.5, "browsing": 0.15},
            "browsing": {
                "work": 0.2,
                "break": 0.05,
                "reading": 0.15,
                "typing": 0.4,
                "browsing": 0.2,
            },
        }
        self.current_state = "typing"  # Start in typing state for more coding

    def next_state(self) -> str:
        """Get next state based on transition probabilities"""
        transitions = self.transition_matrix[self.current_state]
        states = list(transitions.keys())
        probabilities = list(transitions.values())

        self.current_state = np.random.choice(states, p=probabilities)
        return self.current_state

    def get_state(self) -> str:
        """Get current state"""
        return self.current_state


class BehavioralPatternModel:
    """Model realistic human behavioral patterns"""

    def __init__(self):
        self.work_session_duration = 0
        self.break_duration = 0
        self.session_start = time.time()
        self.in_break = False
        self.markov_chain = MarkovChain()

    def update(self, elapsed: float):
        """Update behavioral state"""
        if self.in_break:
            self.break_duration += elapsed
            if self.break_duration >= np.random.uniform(300, 900):
                self.in_break = False
                self.break_duration = 0
                self.session_start = time.time()
                logger.info("Break ended, resuming work session")
        else:
            self.work_session_duration += elapsed
            if self.work_session_duration >= np.random.uniform(1200, 3000):
                if np.random.random() < 0.7:
                    self.in_break = True
                    self.work_session_duration = 0
                    logger.info("Starting break period")

    def get_current_state(self) -> str:
        """Get current behavioral state"""
        if self.in_break:
            return "break"
        return self.markov_chain.get_state()

    def transition_state(self):
        """Transition to next state"""
        self.markov_chain.next_state()

    def is_in_break(self) -> bool:
        """Check if currently in break"""
        return self.in_break
