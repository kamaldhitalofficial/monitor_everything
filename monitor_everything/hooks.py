import os
from pathlib import Path
from monitor_everything.git_utils import get_git_root

HOOK_SCRIPT = """#!/usr/bin/env python3
import sys
import subprocess

result = subprocess.run(["me", "check"], capture_output=False)
sys.exit(result.returncode)
"""

def install_hook():
    git_root = get_git_root()
    if not git_root:
        return False, "Not a git repository"
    
    hooks_dir = git_root / ".git" / "hooks"
    hook_path = hooks_dir / "pre-commit"
    
    if hook_path.exists():
        backup_path = hooks_dir / "pre-commit.backup"
        hook_path.rename(backup_path)
    
    hook_path.write_text(HOOK_SCRIPT)
    hook_path.chmod(0o755)
    
    return True, f"Pre-commit hook installed at {hook_path}"

def uninstall_hook():
    git_root = get_git_root()
    if not git_root:
        return False, "Not a git repository"
    
    hook_path = git_root / ".git" / "hooks" / "pre-commit"
    
    if not hook_path.exists():
        return False, "No pre-commit hook found"
    
    hook_path.unlink()
    
    backup_path = git_root / ".git" / "hooks" / "pre-commit.backup"
    if backup_path.exists():
        backup_path.rename(hook_path)
        return True, "Pre-commit hook removed and backup restored"
    
    return True, "Pre-commit hook removed"

def install_alias(global_alias=False):
    import subprocess
    
    git_root = get_git_root()
    if not git_root and not global_alias:
        return False, "Not a git repository"
    
    scope = "--global" if global_alias else "--local"
    
    try:
        subprocess.run(
            ["git", "config", scope, "alias.gc", "!me check && git commit"],
            check=True,
            capture_output=True
        )
        scope_text = "globally" if global_alias else "locally"
        return True, f"Git alias 'gc' installed {scope_text}"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install alias: {e.stderr.decode()}"

def uninstall_alias(global_alias=False):
    import subprocess
    
    git_root = get_git_root()
    if not git_root and not global_alias:
        return False, "Not a git repository"
    
    scope = "--global" if global_alias else "--local"
    
    try:
        subprocess.run(
            ["git", "config", scope, "--unset", "alias.gc"],
            check=True,
            capture_output=True
        )
        scope_text = "globally" if global_alias else "locally"
        return True, f"Git alias 'gc' removed {scope_text}"
    except subprocess.CalledProcessError:
        return False, "No 'gc' alias found"
