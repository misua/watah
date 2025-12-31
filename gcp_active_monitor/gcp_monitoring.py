"""
GCP Active Monitor - Cloud resource monitoring utility
"""
import sys
import os
import ctypes
import traceback

def set_process_name(name):
    """Set the process name"""
    try:
        if sys.platform == 'win32':
            ctypes.windll.kernel32.SetConsoleTitleW(name)
    except:
        pass

def run_monitor():
    """Run the monitoring service"""
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Set window title to something innocuous
    set_process_name("GCP Monitor Service")
    
    # Import modules
    from gcp_utils.config import Config
    from gcp_utils.daemon import DaemonController
    import logging
    
    # Log ONLY to file - NO console output
    log_file = os.path.join(script_dir, "monitor.log")
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    file_handler.setLevel(logging.DEBUG)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    
    logger = logging.getLogger(__name__)
    
    # Load config
    config_file = os.path.join(script_dir, "config.vm.yaml")
    if not os.path.exists(config_file):
        config_file = os.path.join(script_dir, "config.yaml")
    
    try:
        config = Config(config_file) if os.path.exists(config_file) else Config()
        controller = DaemonController(config)
        controller.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    run_monitor()
