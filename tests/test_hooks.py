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

def test_install_alias_local(tmp_path, monkeypatch):
    from monitor_everything.hooks import install_alias
    
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    success, message = install_alias(global_alias=False)
    assert success == True
    assert "installed locally" in message
    
    result = subprocess.run(
        ["git", "config", "--local", "alias.gc"],
        capture_output=True,
        text=True
    )
    assert "me check" in result.stdout

def test_install_alias_global():
    from monitor_everything.hooks import install_alias, uninstall_alias
    
    success, message = install_alias(global_alias=True)
    assert success == True
    assert "installed globally" in message
    
    result = subprocess.run(
        ["git", "config", "--global", "alias.gc"],
        capture_output=True,
        text=True
    )
    assert "me check" in result.stdout
    
    uninstall_alias(global_alias=True)

def test_uninstall_alias_local(tmp_path, monkeypatch):
    from monitor_everything.hooks import install_alias, uninstall_alias
    
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    install_alias(global_alias=False)
    
    success, message = uninstall_alias(global_alias=False)
    assert success == True
    assert "removed locally" in message

def test_uninstall_alias_not_found(tmp_path, monkeypatch):
    from monitor_everything.hooks import uninstall_alias
    
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    success, message = uninstall_alias(global_alias=False)
    assert success == False
    assert "No 'gc' alias found" in message
