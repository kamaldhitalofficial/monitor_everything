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
