import json
import tempfile
from pathlib import Path
from monitor_everything.config import Config, DEFAULT_CONFIG

def test_load_default_config():
    config = Config()
    assert config.data == DEFAULT_CONFIG

def test_config_get():
    config = Config()
    assert config.get("checks.linting") == False
    assert config.get("protected_branches") == ["main"]
    assert config.get("nonexistent", "default") == "default"

def test_config_set():
    config = Config()
    config.set("checks.linting", True)
    assert config.get("checks.linting") == True

def test_config_save_and_load(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    
    config = Config()
    config.set("checks.linting", True)
    config.save()
    
    new_config = Config()
    assert new_config.get("checks.linting") == True

def test_config_merge(tmp_path, monkeypatch):
    global_path = tmp_path / "global" / ".merc"
    local_path = tmp_path / "local" / ".merc"
    
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", global_path)
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", local_path)
    
    global_path.parent.mkdir(parents=True, exist_ok=True)
    with open(global_path, 'w') as f:
        json.dump({"checks": {"linting": True}}, f)
    
    local_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, 'w') as f:
        json.dump({"checks": {"formatting": True}}, f)
    
    config = Config()
    assert config.get("checks.linting") == True
    assert config.get("checks.formatting") == True
