"""
Tests for configuration management
"""
import pytest
import tempfile
import os
from activity_simulator.config import Config


def test_default_config():
    config = Config()
    
    assert config.get("daemon.log_level") == "INFO"
    assert config.get("timing.intensity") == "medium"
    assert config.get("safety.pause_on_user_input") == True


def test_config_get():
    config = Config()
    
    value = config.get("daemon.pid_file")
    assert value == "activity_sim.pid"
    
    value = config.get("nonexistent.key", "default")
    assert value == "default"


def test_config_save_load():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = f.name
    
    try:
        config = Config()
        config.save_config(config_path)
        
        assert os.path.exists(config_path)
        
        config2 = Config(config_path)
        assert config2.get("daemon.log_level") == config.get("daemon.log_level")
    finally:
        if os.path.exists(config_path):
            os.remove(config_path)
