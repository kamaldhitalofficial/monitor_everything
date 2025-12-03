import subprocess
from pathlib import Path
from monitor_everything.hooks import install_hook, uninstall_hook

def test_install_hook_not_git_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    success, message = install_hook()
    assert success == False
    assert "Not a git repository" in message

def test_install_hook_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    success, message = install_hook()
    assert success == True
    assert "installed" in message
    
    hook_path = tmp_path / ".git" / "hooks" / "pre-commit"
    assert hook_path.exists()
    assert hook_path.stat().st_mode & 0o111

def test_install_hook_with_existing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    hook_path = tmp_path / ".git" / "hooks" / "pre-commit"
    hook_path.write_text("old hook")
    
    success, message = install_hook()
    assert success == True
    
    backup_path = tmp_path / ".git" / "hooks" / "pre-commit.backup"
    assert backup_path.exists()
    assert backup_path.read_text() == "old hook"

def test_uninstall_hook_not_git_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    success, message = uninstall_hook()
    assert success == False
    assert "Not a git repository" in message

def test_uninstall_hook_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    install_hook()
    
    success, message = uninstall_hook()
    assert success == True
    assert "removed" in message
    
    hook_path = tmp_path / ".git" / "hooks" / "pre-commit"
    assert not hook_path.exists()

def test_uninstall_hook_no_hook(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    success, message = uninstall_hook()
    assert success == False
    assert "No pre-commit hook found" in message
