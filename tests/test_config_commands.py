from click.testing import CliRunner
from monitor_everything.main import cli
import json

def test_config_list(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['config', 'list'])
    
    assert result.exit_code == 0
    assert "protected_branches" in result.output

def test_config_set(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['config', 'set', 'checks.linting', 'true'])
    
    assert result.exit_code == 0
    assert "Set checks.linting = True" in result.output
    
    config_path = tmp_path / ".merc"
    with open(config_path) as f:
        config = json.load(f)
        assert config["checks"]["linting"] == True

def test_config_add_protected(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['config', 'add-protected', 'develop'])
    
    assert result.exit_code == 0
    assert "Added 'develop' to protected branches" in result.output
    
    config_path = tmp_path / ".merc"
    with open(config_path) as f:
        config = json.load(f)
        assert "develop" in config["protected_branches"]

def test_config_add_protected_duplicate(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    runner.invoke(cli, ['config', 'add-protected', 'develop'])
    result = runner.invoke(cli, ['config', 'add-protected', 'develop'])
    
    assert result.exit_code == 0
    assert "already protected" in result.output

def test_config_remove_protected(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    runner.invoke(cli, ['config', 'add-protected', 'develop'])
    result = runner.invoke(cli, ['config', 'remove-protected', 'develop'])
    
    assert result.exit_code == 0
    assert "Removed 'develop' from protected branches" in result.output
    
    config_path = tmp_path / ".merc"
    with open(config_path) as f:
        config = json.load(f)
        assert "develop" not in config["protected_branches"]

def test_config_remove_protected_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['config', 'remove-protected', 'nonexistent'])
    
    assert result.exit_code == 1
    assert "not in protected branches" in result.output
