import subprocess
import tempfile
from pathlib import Path
from monitor_everything.git_utils import (
    is_git_repo,
    get_current_branch,
    is_protected_branch,
    get_staged_files,
    get_git_root
)

def test_is_git_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert is_git_repo() == False
    
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    assert is_git_repo() == True

def test_get_current_branch(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=tmp_path, capture_output=True)
    
    branch = get_current_branch()
    assert branch == "main"

def test_is_protected_branch():
    assert is_protected_branch("main", ["main", "develop"]) == True
    assert is_protected_branch("feature/test", ["main", "develop"]) == False

def test_get_staged_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    subprocess.run(["git", "add", "test.txt"], cwd=tmp_path, capture_output=True)
    
    files = get_staged_files()
    assert "test.txt" in files

def test_get_git_root(tmp_path, monkeypatch):
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    monkeypatch.chdir(subdir)
    
    root = get_git_root()
    assert root == tmp_path
