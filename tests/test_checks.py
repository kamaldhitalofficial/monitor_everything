import subprocess
from monitor_everything.checks import (
    Check,
    CheckResult,
    CheckOutput,
    CheckRegistry,
    BranchAwarenessCheck,
    registry
)

def test_check_output():
    output = CheckOutput(
        result=CheckResult.PASS,
        message="Test passed",
        details=["Detail 1", "Detail 2"]
    )
    assert output.result == CheckResult.PASS
    assert output.message == "Test passed"
    assert len(output.details) == 2

def test_check_registry():
    reg = CheckRegistry()
    
    class TestCheck(Check):
        def run(self, files):
            return CheckOutput(CheckResult.PASS, "test")
    
    reg.register("test", TestCheck)
    assert "test" in reg.list_available()
    assert reg.get("test") == TestCheck

def test_branch_awareness_check(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feature/test"], cwd=tmp_path, capture_output=True)
    
    check = BranchAwarenessCheck()
    result = check.run([])
    
    assert result.result == CheckResult.PASS
    assert "feature/test" in result.message

def test_registry_has_branch_awareness():
    assert "branch_awareness" in registry.list_available()
    check_class = registry.get("branch_awareness")
    assert check_class == BranchAwarenessCheck

def test_ruff_check_no_python_files():
    from monitor_everything.checks import RuffCheck
    import shutil
    
    check = RuffCheck()
    result = check.run(["test.txt", "test.js"])
    
    if shutil.which("ruff"):
        assert result.result == CheckResult.PASS
        assert "No Python files" in result.message
    else:
        assert result.result == CheckResult.WARN
        assert "not installed" in result.message

def test_black_check_no_python_files():
    from monitor_everything.checks import BlackCheck
    check = BlackCheck()
    result = check.run(["test.txt", "test.js"])
    assert result.result == CheckResult.PASS
    assert "No Python files" in result.message

def test_mypy_check_no_python_files():
    from monitor_everything.checks import MypyCheck
    check = MypyCheck()
    result = check.run(["test.txt", "test.js"])
    assert result.result == CheckResult.PASS
    assert "No Python files" in result.message

def test_registry_has_all_checks():
    assert "linting" in registry.list_available()
    assert "formatting" in registry.list_available()
    assert "type_checking" in registry.list_available()
