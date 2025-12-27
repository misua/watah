#!/usr/bin/env python3
"""Test script to simulate Windows cp1252 encoding issue"""

import sys
import logging
import io
import codecs

print(f"System default encoding: {sys.getdefaultencoding()}")
print(f"Stdout encoding: {sys.stdout.encoding}")

def test_with_cp1252_simulation():
    """Simulate Windows console with cp1252 encoding"""
    
    print("\n=== Simulating Windows cp1252 Console ===\n")
    
    # Test 1: Simulate cp1252 encoding (like Windows console)
    print("1. Testing with cp1252 encoding (Windows behavior):")
    try:
        # Create a BytesIO buffer wrapped with cp1252 encoding
        buffer = io.BytesIO()
        cp1252_stream = io.TextIOWrapper(buffer, encoding='cp1252', errors='strict')
        
        # Try to write Unicode characters
        test_messages = [
            "✓ Activity completed successfully",
            "✗ Activity FAILED",
            ">>> Executing activity"
        ]
        
        for msg in test_messages:
            try:
                cp1252_stream.write(msg + "\n")
                cp1252_stream.flush()
                print(f"  ✗ UNEXPECTED: '{msg[:20]}...' encoded without error")
            except UnicodeEncodeError as e:
                print(f"  ✓ EXPECTED ERROR: '{msg[:20]}...' -> {e.reason}")
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # Test 2: With 'replace' error handling
    print("\n2. Testing with cp1252 + errors='replace':")
    try:
        buffer = io.BytesIO()
        cp1252_stream = io.TextIOWrapper(buffer, encoding='cp1252', errors='replace')
        
        test_messages = [
            "✓ Activity completed successfully",
            "✗ Activity FAILED",
            ">>> Executing activity"
        ]
        
        for msg in test_messages:
            try:
                cp1252_stream.write(msg + "\n")
                cp1252_stream.flush()
                # Read back what was written
                buffer.seek(0)
                result = buffer.read().decode('cp1252')
                print(f"  ✓ SUCCESS: '{msg[:20]}...' -> '{result.strip()[:30]}...'")
                buffer.truncate(0)
                buffer.seek(0)
            except Exception as e:
                print(f"  ✗ FAILED: {e}")
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # Test 3: With UTF-8 encoding
    print("\n3. Testing with UTF-8 encoding:")
    try:
        buffer = io.BytesIO()
        utf8_stream = io.TextIOWrapper(buffer, encoding='utf-8', errors='replace')
        
        test_messages = [
            "✓ Activity completed successfully",
            "✗ Activity FAILED",
            ">>> Executing activity"
        ]
        
        for msg in test_messages:
            try:
                utf8_stream.write(msg + "\n")
                utf8_stream.flush()
                buffer.seek(0)
                result = buffer.read().decode('utf-8')
                print(f"  ✓ SUCCESS: '{msg[:20]}...' preserved as '{result.strip()[:30]}...'")
                buffer.truncate(0)
                buffer.seek(0)
            except Exception as e:
                print(f"  ✗ FAILED: {e}")
    except Exception as e:
        print(f"  ERROR: {e}")


def test_logging_fix():
    """Test the logging configuration fix"""
    
    print("\n=== Testing Logging Configuration Fix ===\n")
    
    # Simulate the fixed code
    print("Testing fixed logging setup:")
    try:
        # Remove any existing handlers
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        
        # Use the fixed approach
        import io
        log_file = "test_activity.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Wrap stdout with UTF-8 encoding and error handling
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
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[file_handler, stream_handler],
            force=True
        )
        
        logger = logging.getLogger("test")
        logger.info("✓ Activity mouse_movement completed successfully")
        logger.error("✗ Activity keyboard_typing FAILED")
        logger.info(">>> Executing activity: mouse_scroll")
        logger.info(">>> Next activity in 45.3 seconds")
        
        print("\n  ✓ All logging messages handled correctly!")
        
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_with_cp1252_simulation()
    test_logging_fix()
    print("\n=== Test Complete ===")
