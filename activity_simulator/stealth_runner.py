"""
Stealth runner - disguises the process name to avoid detection
"""
import sys
import os
import ctypes

def set_process_name(name):
    """Set the process name to disguise the application"""
    try:
        if sys.platform == 'win32':
            # On Windows, change the console window title
            ctypes.windll.kernel32.SetConsoleTitleW(name)
            
            # Try to spoof process name in task manager
            # This requires the process to be renamed before running
            pass
    except Exception as e:
        print(f"Warning: Could not set process name: {e}")

def run_disguised():
    """Run the daemon with a disguised process name"""
    # Set innocent-looking process names
    process_names = [
        "Adobe Update Service",
        "Windows Update Assistant", 
        "Microsoft Edge Update",
        "notepad.exe",
        "System Idle Process",
        "RuntimeBroker.exe"
    ]
    
    import random
    disguise_name = random.choice(process_names)
    set_process_name(disguise_name)
    
    # Now run the actual daemon
    from activity_simulator.config import Config
    from activity_simulator.daemon import DaemonController
    import logging
    
    # Suppress console output for stealth mode
    logging.basicConfig(
        level=logging.ERROR,  # Only show errors
        format="%(message)s",
        handlers=[logging.FileHandler("syslog.tmp", encoding='utf-8')],  # Hidden log file
    )
    
    config_file = os.path.join(os.path.dirname(__file__), "config.yaml")
    if not os.path.exists(config_file):
        config_file = os.path.join(os.path.dirname(__file__), "config.example.yaml")
    
    config = Config(config_file) if os.path.exists(config_file) else Config()
    controller = DaemonController(config)
    
    try:
        controller.start()
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    run_disguised()
