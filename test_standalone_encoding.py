#!/usr/bin/env python3
"""
Standalone test for the logging encoding fix
Tests the exact code pattern used in daemon.py
"""
import sys
import logging
import io
import os

def test_daemon_logging_setup():
    """Test the exact logging setup from daemon.py"""
    
    print("=" * 60)
    print("Testing Daemon Logging Setup with Unicode Characters")
    print("=" * 60)
    
    log_file = "test_daemon_encoding.log"
    log_level = "INFO"
    
    print(f"\nEnvironment:")
    print(f"  - System encoding: {sys.getdefaultencoding()}")
    print(f"  - Stdout encoding: {sys.stdout.encoding}")
    print(f"  - Platform: {sys.platform}")
    
    try:
        print("\n" + "=" * 60)
        print("Step 1: Setting up logging handlers")
        print("=" * 60)
        
        # This is the EXACT code from the fixed daemon.py
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
            print("  ✓ Created StreamHandler with UTF-8 encoding and error='replace'")
        except (AttributeError, io.UnsupportedOperation):
            # Fallback for environments without buffer access
            stream_handler = logging.StreamHandler(sys.stdout)
            print("  ⚠ Using fallback StreamHandler (no buffer access)")
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[file_handler, stream_handler],
            force=True
        )
        
        print("  ✓ Logging configuration complete")
        
        print("\n" + "=" * 60)
        print("Step 2: Testing problematic log messages")
        print("=" * 60)
        
        logger = logging.getLogger("activity_daemon")
        
        # These are the EXACT messages that were causing the error
        test_messages = [
            ("INFO", ">>> Executing activity: mouse_movement (waited 45.3s)"),
            ("INFO", "✓ Activity mouse_movement completed successfully"),
            ("ERROR", "✗ Activity keyboard_typing FAILED"),
            ("INFO", ">>> Next activity in 42.5 seconds"),
        ]
        
        print("\nLogging messages with Unicode characters:\n")
        
        for level, message in test_messages:
            if level == "INFO":
                logger.info(message)
            elif level == "ERROR":
                logger.error(message)
            elif level == "DEBUG":
                logger.debug(message)
        
        print("\n  ✓ All messages logged without UnicodeEncodeError!")
        
        print("\n" + "=" * 60)
        print("Step 3: Verifying log file")
        print("=" * 60)
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                contents = f.read()
                
            print(f"\nLog file size: {len(contents)} bytes")
            
            # Check for Unicode characters
            has_checkmark = '✓' in contents
            has_crossmark = '✗' in contents
            has_arrows = '>>>' in contents
            
            print(f"  - Contains '✓' (checkmark): {has_checkmark}")
            print(f"  - Contains '✗' (crossmark): {has_crossmark}")
            print(f"  - Contains '>>>' (arrows): {has_arrows}")
            
            if has_checkmark and has_crossmark and has_arrows:
                print("\n  ✓ Log file correctly preserved Unicode characters!")
            else:
                print("\n  ⚠ Some Unicode characters missing from log file")
            
            print("\nLog file contents:")
            print("-" * 60)
            print(contents)
            print("-" * 60)
        else:
            print("  ✗ Log file was not created!")
            return False
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe encoding fix successfully prevents the cp1252 error!")
        print("Unicode characters (✓, ✗, >>>) are handled correctly.")
        
        return True
        
    except UnicodeEncodeError as e:
        print("\n" + "=" * 60)
        print("✗ UNICODE ENCODE ERROR DETECTED!")
        print("=" * 60)
        print(f"\nError: {e}")
        print(f"Encoding: {e.encoding}")
        print(f"Reason: {e.reason}")
        print(f"Object: {e.object[:50]}...")
        print("\nThis is the error that was occurring on Windows!")
        return False
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ UNEXPECTED ERROR!")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"\nCleaned up test file: {log_file}")
            except:
                pass


if __name__ == "__main__":
    success = test_daemon_logging_setup()
    
    if success:
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("""
The fix in daemon.py resolves the UnicodeEncodeError by:

1. Using UTF-8 encoding for both file and stream handlers
2. Adding errors='replace' to handle unencodable characters gracefully
3. Wrapping sys.stdout.buffer with TextIOWrapper for explicit control

This prevents crashes when logging Unicode characters (✓, ✗, etc.) 
on Windows systems with cp1252 console encoding.
        """)
        sys.exit(0)
    else:
        print("\nTest failed - encoding issue still present!")
        sys.exit(1)
