"""
Stealth runner - disguises the process name to avoid detection
"""
import sys
import os
import ctypes
import traceback

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
    # Change to script directory to ensure relative paths work
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
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
    
    # Log to file at DEBUG level for debugging
    log_file = os.path.join(script_dir, "activity_sim_stealth.log")
    logging.basicConfig(
        level=logging.DEBUG,  # Log everything to file
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file, encoding='utf-8')],
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Stealth mode: Logging to {log_file}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"PID: {os.getpid()}")
    
    # Try config files in order: config.vm.yaml -> config.yaml -> config.example.yaml
    config_file = os.path.join(script_dir, "config.vm.yaml")
    if not os.path.exists(config_file):
        config_file = os.path.join(script_dir, "config.yaml")
    if not os.path.exists(config_file):
        config_file = os.path.join(script_dir, "config.example.yaml")
    
    logger.info(f"Using config file: {config_file}")
    logger.info(f"Starting in stealth mode as '{disguise_name}'...")
    
    try:
        config = Config(config_file) if os.path.exists(config_file) else Config()
        controller = DaemonController(config)
        controller.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        controller.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        run_disguised()
    except Exception as e:
        # Write crash info to file since console may not be visible
        with open("stealth_crash.log", "w") as f:
            f.write(f"Crash: {e}\n")
            f.write(traceback.format_exc())
