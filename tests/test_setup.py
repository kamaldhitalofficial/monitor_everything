from click.testing import CliRunner
from monitor_everything.main import cli
from pathlib import Path
import json

def test_setup_wizard_basic(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['setup'], input='n\nn\nn\nn\nn\nmain\nn\ny\n')
    
    assert result.exit_code == 0
    assert "Welcome to Monitor Everything setup!" in result.output
    assert "✓ Setup complete!" in result.output
    
    config_path = tmp_path / ".merc"
    assert config_path.exists()
    
    with open(config_path) as f:
        config = json.load(f)
        assert config["protected_branches"] == ["main"]

def test_setup_wizard_with_checks(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['setup'], input='y\ny\nn\nn\nn\nmain,develop\nblock\nwarn\nn\ny\n')
    
    assert result.exit_code == 0
    
    config_path = tmp_path / ".merc"
    with open(config_path) as f:
        config = json.load(f)
        assert config["checks"]["linting"] == True
        assert config["checks"]["formatting"] == True
        assert config["behavior"]["linting"] == "block"
        assert config["behavior"]["formatting"] == "warn"
        assert config["protected_branches"] == ["main", "develop"]

def test_setup_wizard_global_save(tmp_path, monkeypatch):
    local_path = tmp_path / "local" / ".merc"
    global_path = tmp_path / "global" / ".merc"
    
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", local_path)
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", global_path)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['setup'], input='n\nn\nn\nn\nn\nmain\ny\nn\n')
    
    assert result.exit_code == 0
    assert global_path.exists()
    assert not local_path.exists()
