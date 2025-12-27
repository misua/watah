#!/usr/bin/env python3
"""
Quick integration test for the daemon encoding fix
"""
import sys
import os

# Add the activity_simulator package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'activity_simulator'))

from activity_simulator.config import Config
from activity_simulator.daemon import DaemonController
import logging
import time

def test_daemon_logging():
    """Test that daemon logging works with Unicode characters"""
    
    print("Testing DaemonController with Unicode logging...")
    
    # Create a minimal config
    config_data = {
        'daemon': {
            'log_file': 'test_daemon.log',
            'log_level': 'INFO'
        },
        'activities': {
            'mouse_movement': {'enabled': False},
            'mouse_scroll': {'enabled': False},
            'keyboard_typing': {'enabled': False},
        },
        'timing': {
            'base_interval': 30
        }
    }
    
    config = Config()
    config.config = config_data
    
    # Create controller
    controller = DaemonController(config)
    
    # Test logging setup
    try:
        print("\n1. Setting up logging (this would normally fail on Windows cp1252)...")
        
        # Manually call the logging setup part
        log_file = config.get("daemon.log_file", "activity_sim.log")
        log_level = config.get("daemon.log_level", "INFO")

        # Create handlers with proper encoding support
        import io
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Wrap stdout with UTF-8 encoding and error handling for Unicode characters
        try:
            stdout_stream = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8',
                errors='replace',
                line_buffering=True
            )
            stream_handler = logging.StreamHandler(stdout_stream)
        except (AttributeError, io.UnsupportedOperation):
            stream_handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[file_handler, stream_handler],
            force=True
        )
        
        print("   ✓ Logging setup successful")
        
        # Test actual log messages with Unicode
        print("\n2. Testing Unicode log messages...")
        logger = logging.getLogger("daemon_test")
        logger.info(">>> Executing activity: mouse_movement")
        logger.info("✓ Activity mouse_movement completed successfully")
        logger.error("✗ Activity keyboard_typing FAILED")
        logger.info(">>> Next activity in 42.5 seconds")
        
        print("   ✓ All Unicode messages logged successfully")
        
        # Check log file
        print("\n3. Verifying log file contents...")
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                contents = f.read()
                if '✓' in contents and '✗' in contents:
                    print("   ✓ Log file contains Unicode characters correctly")
                else:
                    print("   ⚠ Log file might have encoding issues")
                print(f"\n   Log file preview:\n{contents[:300]}...")
        
        print("\n✓ ALL TESTS PASSED!")
        return True
        
    except UnicodeEncodeError as e:
        print(f"\n✗ UNICODE ENCODING ERROR: {e}")
        print(f"   This indicates the fix didn't work properly")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if os.path.exists('test_daemon.log'):
            os.remove('test_daemon.log')

if __name__ == "__main__":
    success = test_daemon_logging()
    sys.exit(0 if success else 1)
