#!/usr/bin/env python3
"""Test script to reproduce and verify the encoding issue fix"""

import sys
import logging
import io

print(f"System default encoding: {sys.getdefaultencoding()}")
print(f"Stdout encoding: {sys.stdout.encoding}")
print(f"Stderr encoding: {sys.stderr.encoding}")

# Try to reproduce the issue
def test_logging_with_unicode():
    """Test logging with Unicode characters that cause cp1252 errors"""
    
    # Setup logging like the daemon does
    log_file = "test_encoding.log"
    
    print("\n1. Testing with default StreamHandler (should fail on Windows with cp1252):")
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Uses system default encoding
            ],
            force=True  # Reset any existing config
        )
        logger = logging.getLogger(__name__)
        logger.info("✓ Activity completed successfully")
        logger.error("✗ Activity FAILED")
        logger.info(">>> Executing activity")
        print("  SUCCESS: No encoding error with default handler")
    except UnicodeEncodeError as e:
        print(f"  FAILED: {e}")
    
    # Test with UTF-8 StreamHandler
    print("\n2. Testing with UTF-8 StreamHandler:")
    try:
        # Remove all handlers
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        
        # Setup with explicit UTF-8 encoding on StreamHandler
        utf8_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        stream_handler = logging.StreamHandler(utf8_stream)
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                stream_handler
            ],
            force=True
        )
        
        logger = logging.getLogger(__name__)
        logger.info("✓ Activity completed successfully")
        logger.error("✗ Activity FAILED")
        logger.info(">>> Executing activity")
        print("  SUCCESS: UTF-8 handler works correctly")
    except Exception as e:
        print(f"  FAILED: {e}")
    
    # Test with error handling
    print("\n3. Testing with error='replace' on default StreamHandler:")
    try:
        # Remove all handlers
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        
        # Setup with error handling
        stream_handler = logging.StreamHandler()
        stream_handler.stream = io.TextIOWrapper(
            sys.stdout.buffer, 
            encoding=sys.stdout.encoding or 'utf-8',
            errors='replace'  # Replace unencodable characters
        )
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                stream_handler
            ],
            force=True
        )
        
        logger = logging.getLogger(__name__)
        logger.info("✓ Activity completed successfully")
        logger.error("✗ Activity FAILED")  
        logger.info(">>> Executing activity")
        print("  SUCCESS: Error handling prevents crashes")
    except Exception as e:
        print(f"  FAILED: {e}")

if __name__ == "__main__":
    test_logging_with_unicode()
    print("\nTest complete!")
