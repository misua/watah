"""
Smart Monitor Scheduler
Alternates between GCP and Azure monitors with realistic work patterns
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MonitorScheduler:
    """Schedules and alternates between GCP and Azure monitors"""
    
    def __init__(self, testing_mode=False):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.gcp_dir = os.path.join(self.base_dir, 'gcp_active_monitor')
        self.azure_dir = os.path.join(self.base_dir, 'azure_monitor')
        
        self.current_process: Optional[subprocess.Popen] = None
        self.current_monitor = None
        self.should_stop = False
        self.testing_mode = testing_mode
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.should_stop = True
        self.stop_current_monitor()
        sys.exit(0)
    
    def is_work_hours(self) -> bool:
        """Check if it's during realistic work hours"""
        if self.testing_mode:
            return True  # Always work hours during testing
        
        now = datetime.now()
        
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
        
        current_hour = now.hour
        
        if work_start <= current_hour < work_end:
            return True
        
        return False
    
    def get_session_duration(self) -> int: or 2 min for testing)"""
        if self.testing_mode:
            return 2  # 2 minutes for testing
        
        """Get random session duration for a monitor (30-90 minutes)"""
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
        """Choose which monitor to run next"""
        # Alternate between monitors, with slight bias
        if self.current_monitor is None:
            # First run - 50/50 choice
            return random.choice(['gcp', 'azure'])
        elif self.current_monitor == 'gcp':
            # 85% switch to azure, 15% stay with gcp
            return 'azure' if random.random() < 0.85 else 'gcp'
        else:
            # 85% switch to gcp, 15% stay with azure
            return 'gcp' if random.random() < 0.85 else 'azure'
    
    def start_monitor(self, monitor_type: str) -> bool:
        """Start a monitor (gcp or azure)"""
        try:
            if monitor_type == 'gcp':
                script_path = os.path.join(self.gcp_dir, 'gcp_monitoring.py')
                cwd = self.gcp_dir
                logger.info("Starting GCP monitor...")
            else:  # azure
                script_path = os.path.join(self.azure_dir, 'azure_setup.py')
                cwd = self.azure_dir
                logger.info("Starting Azure monitor...")
            
            # Check if script exists
            if not os.path.exists(script_path):
                logger.error(f"Monitor script not found: {script_path}")
                return False
            
            # Start the monitor process
            # Use pythonw on Windows to avoid console window
            python_cmd = 'pythonw' if sys.platform == 'win32' else 'python3'
            
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
            return False
    
    def stop_current_monitor(self):
        """Stop the currently running monitor"""
        if self.current_process is None:
            return
        
        try:
            logger.info(f"Stopping {self.current_monitor} monitor...")
            
            # Try graceful shutdown first
            self.current_process.terminate()
            
            # Wait up to 5 seconds for graceful shutdown
            try:
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                logger.warning("Monitor not responding, forcing shutdown...")
                self.current_process.kill()
                self.current_process.wait()
            
            logger.info(f"{self.current_monitor} monitor stopped")
            
        except Exception as e:
            logger.error(f"Error stopping monitor: {e}")
        finally:
            self.current_process = None
            self.current_monitor = None
    
    def run_session(self):
        """Run a single monitoring session"""
        # Choose which monitor to run
        monitor_type = self.choose_next_monitor()
        session_duration = self.get_session_duration()
        
        logger.info(f"Starting {monitor_type.upper()} session for {session_duration} minutes")
        
        # Start the monitor
        if not self.start_monitor(monitor_type):
            logger.error("Failed to start monitor, waiting 5 minutes before retry...")
            time.sleep(300)
            return
        
        # Run for the session duration
        start_time = time.time()
        end_time = start_time + (session_duration * 60)
        
        while time.time() < end_time and not self.should_stop:
            # Check if process is still running
            if self.current_process.poll() is not None:
                logger.warning(f"{monitor_type} monitor process ended unexpectedly")
                break
            
            # Sleep for 30 seconds before checking again
            time.sleep(30)
        
        # Stop the monitor
        self.stop_current_monitor()
        
        logger.info(f"Session completed ({session_duration} minutes)")
    
    def run(self):
        """Main scheduler loop"""
        logger.info("Monitor Scheduler started")
        logger.info("=" * 60)
        
        while not self.should_stop:
            try:
                # Check if we're in work hours
                if not self.is_work_hours():
                    now = datetime.now()
                    # Calculate next work day start (around 8 AM)
                    next_day = now + timedelta(days=1)
                    next_start = next_day.replace(hour=8, minute=0, second=0)
                    wait_seconds = (next_start - now).total_seconds()
                    
                    logger.info(f"Outside work hours. Sleeping until {next_start.strftime('%Y-%m-%d %H:%M')}")
                    
                    # Sleep in chunks to allow for shutdown signals
                    while wait_seconds > 0 and not self.should_stop:
                        sleep_time = min(300, wait_seconds)  # Sleep max 5 minutes at a time
                        time.sleep(sleep_time)
                        wait_seconds -= sleep_time
                    
                    continue
                
                # Run a monitoring session
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
                logger.error(f"Traceback: {traceback.format_exc()}")
                time.sleep(60)  # Wait a minute before retrying
        
        logger.info("Monitor Scheduler stopped")
# Check for testing mode flag
    testing_mode = '--test' in sys.argv or '-t' in sys.argv
    
    logger.info("=" * 60)
    logger.info("Smart Monitor Scheduler")
    logger.info("Alternates between GCP and Azure monitors")
    if testing_mode:
        logger.info("TESTING MODE: 2-minute intervals")
    else:
        logger.info("Simulates realistic 8-hour workday patterns")
    logger.info("=" * 60)
    
    scheduler = MonitorScheduler(testing_mode=testing_mode
    logger.info("Smart Monitor Scheduler")
    logger.info("Alternates between GCP and Azure monitors")
    logger.info("Simulates realistic 8-hour workday patterns")
    logger.info("=" * 60)
    
    scheduler = MonitorScheduler()
    
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
