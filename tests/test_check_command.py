import subprocess
from click.testing import CliRunner
from monitor_everything.main import cli

def test_check_command_not_git_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['check'])
    
    assert result.exit_code == 1
    assert "Not a git repository" in result.output

def test_check_command_no_staged_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=tmp_path, capture_output=True)
    
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['check'])
    
    assert result.exit_code == 0
    assert "Running checks" in result.output

def test_check_command_with_staged_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feature/test"], cwd=tmp_path, capture_output=True)
    
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")
    subprocess.run(["git", "add", "test.py"], cwd=tmp_path, capture_output=True)
    
    monkeypatch.setattr("monitor_everything.config.LOCAL_CONFIG_PATH", tmp_path / ".merc")
    monkeypatch.setattr("monitor_everything.config.GLOBAL_CONFIG_PATH", tmp_path / "global" / ".merc")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['check'])
    
    assert "Running checks" in result.output
    assert "feature/test" in result.output
