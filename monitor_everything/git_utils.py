import subprocess
from pathlib import Path

def is_git_repo():
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_current_branch():
    try:
        result = subprocess.run(["git", "branch", "--show-current"],
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def is_protected_branch(branch, protected_branches):
    return branch in protected_branches

def get_staged_files():
    try:
        result = subprocess.run(["git", "diff", "--cached", "--name-only"],
                              capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
        return [f for f in files if f]
    except subprocess.CalledProcessError:
        return []

def get_git_root():
    try:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, check=True)
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return None
