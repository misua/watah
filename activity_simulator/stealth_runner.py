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
    
    # Log to file at INFO level for debugging, but suppress console output
    log_file = "activity_sim_stealth.log"
    logging.basicConfig(
        level=logging.INFO,  # Log everything to file
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file, encoding='utf-8')],
    )
    print(f"Stealth mode: Logging to {log_file}")
    
    config_file = os.path.join(os.path.dirname(__file__), "config.yaml")
    if not os.path.exists(config_file):
        config_file = os.path.join(os.path.dirname(__file__), "config.example.yaml")
    
    print(f"Starting in stealth mode as '{disguise_name}'...")
    print(f"Monitor logs: type 'tail -f {log_file}' (Linux) or open {log_file} in notepad")
    
    config = Config(config_file) if os.path.exists(config_file) else Config()
    controller = DaemonController(config)
    
    try:
        controller.start()
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    run_disguised()
