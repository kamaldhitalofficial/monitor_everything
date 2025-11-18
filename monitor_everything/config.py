import os
from pathlib import Path
import tomllib
import json

GLOBAL_CONFIG_PATH = Path.home() / ".merc"
LOCAL_CONFIG_PATH = Path(".merc")

DEFAULT_CONFIG = {
    "checks": {
        "linting": False,
        "formatting": False,
        "type_checking": False,
        "tests": False,
        "security": False,
        "branch_awareness": True
    },
    "protected_branches": ["main"],
    "behavior": {
        "linting": "interactive",
        "formatting": "interactive",
        "type_checking": "interactive",
        "tests": "block",
        "security": "block",
        "branch_awareness": "warn"
    }
}

class Config:
    def __init__(self):
        self.data = self._load()
    
    def _load(self):
        config = DEFAULT_CONFIG.copy()
        
        if GLOBAL_CONFIG_PATH.exists():
            with open(GLOBAL_CONFIG_PATH, 'r') as f:
                global_config = json.load(f)
                config = self._merge(config, global_config)
        
        if LOCAL_CONFIG_PATH.exists():
            with open(LOCAL_CONFIG_PATH, 'r') as f:
                local_config = json.load(f)
                config = self._merge(config, local_config)
        
        return config
    
    def _merge(self, base, override):
        result = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result:
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def save(self, global_config=False):
        path = GLOBAL_CONFIG_PATH if global_config else LOCAL_CONFIG_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key, value):
        keys = key.split('.')
        data = self.data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
