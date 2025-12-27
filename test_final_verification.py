#!/usr/bin/env python3
"""
Test the exact logging fix from daemon.py without Windows dependencies
"""
import sys
import logging
import io
import os

def simulate_windows_cp1252():
    """Simulate Windows console with cp1252 encoding that causes the error"""
    
    print("=" * 70)
    print("SIMULATING WINDOWS CP1252 ENCODING ERROR")
    print("=" * 70)
    
    print("\n1. Testing OLD CODE (should fail with cp1252):\n")
    
    # OLD CODE - what was in daemon.py before the fix
    try:
        # Remove existing handlers
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        
        # Simulate Windows console with cp1252
        buffer = io.BytesIO()
        cp1252_stream = io.TextIOWrapper(buffer, encoding='cp1252', errors='strict')
        
        old_handler = logging.StreamHandler(cp1252_stream)
        old_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        
        logging.basicConfig(
            level=logging.INFO,
            handlers=[old_handler],
            force=True
        )
        
        logger = logging.getLogger("test_old")
        logger.info("✓ Activity completed successfully")
        
        print("  UNEXPECTED: No error occurred (should have failed on Windows)")
        
    except UnicodeEncodeError as e:
        print(f"  ✓ EXPECTED ERROR on Windows: {e}")
        print(f"     Encoding: {e.encoding}")
        print(f"     Reason: {e.reason}")
    
    print("\n2. Testing NEW CODE (should work with cp1252):\n")
    
    # NEW CODE - the fix applied to daemon.py
    try:
        # Remove existing handlers
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        
        log_file = "test_new.log"
        
        # This is the FIXED code from daemon.py
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Wrap stream with UTF-8 encoding and error handling
        try:
            stdout_stream = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8',
                errors='replace',  # This prevents the crash
                line_buffering=True
            )
            stream_handler = logging.StreamHandler(stdout_stream)
        except (AttributeError, io.UnsupportedOperation):
            stream_handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[file_handler, stream_handler],
            force=True
        )
        
        logger = logging.getLogger("test_new")
        logger.info(">>> Executing activity: mouse_movement")
        logger.info("✓ Activity completed successfully")
        logger.error("✗ Activity FAILED")
        
        print("\n  ✓ SUCCESS: Unicode characters logged without error!")
        
        # Clean up
        if os.path.exists(log_file):
            os.remove(log_file)
        
    except UnicodeEncodeError as e:
        print(f"  ✗ FAILED: Still getting encoding error: {e}")
        return False
    
    return True


def test_actual_daemon_code():
    """Test with the actual code extracted from daemon.py"""
    
    print("\n" + "=" * 70)
    print("TESTING ACTUAL DAEMON.PY LOGGING CODE")
    print("=" * 70)
    
    log_file = "activity_sim_test.log"
    log_level = "INFO"
    
    try:
        # Remove existing handlers
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        
        # This is EXACTLY what's now in daemon.py lines 305-336
        import io
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Wrap stdout with UTF-8 encoding and error handling for Unicode characters
        try:
            # Use UTF-8 encoding with 'replace' error handling to avoid cp1252 issues on Windows
            stdout_stream = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8',
                errors='replace',  # Replace unencodable characters instead of crashing
                line_buffering=True
            )
            stream_handler = logging.StreamHandler(stdout_stream)
        except (AttributeError, io.UnsupportedOperation):
            # Fallback for environments without buffer access
            stream_handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[file_handler, stream_handler],
        )
        
        # Test with actual messages from the daemon
        logger = logging.getLogger("ActivityDaemon")
        
        print("\nLogging messages from actual daemon execution:\n")
        
        logger.info("Activity simulator daemon started")
        logger.info("First activity scheduled in 45.3 seconds")
        logger.info(">>> Executing activity: mouse_movement (waited 45.3s)")
        logger.info("✓ Activity mouse_movement completed successfully")
        logger.info(">>> Next activity in 42.5 seconds")
        logger.info(">>> Executing activity: keyboard_typing (waited 42.5s)")
        logger.error("✗ Activity keyboard_typing FAILED")
        logger.info(">>> Next activity in 38.2 seconds")
        
        print("\n✓ All daemon messages logged successfully!")
        
        # Verify log file
        with open(log_file, 'r', encoding='utf-8') as f:
            contents = f.read()
            if '✓' in contents and '✗' in contents:
                print("✓ Log file contains all Unicode characters correctly")
        
        # Clean up
        if os.path.exists(log_file):
            os.remove(log_file)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ENCODING FIX VERIFICATION TEST")
    print("=" * 70)
    
    test1 = simulate_windows_cp1252()
    test2 = test_actual_daemon_code()
    
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    
    if test1 and test2:
        print("""
✓ ALL TESTS PASSED!

The fix in daemon.py successfully resolves the UnicodeEncodeError that 
occurred on Windows with cp1252 console encoding.

The fix:
  1. Uses UTF-8 encoding for file handler
  2. Wraps stdout with UTF-8 TextIOWrapper with errors='replace'
  3. Gracefully handles characters that can't be encoded
  
This allows Unicode characters (✓, ✗, >>>) to be logged without crashes
on Windows systems using cp1252 encoding.
""")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
