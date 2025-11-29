import subprocess
from monitor_everything.runner import CheckRunner
from monitor_everything.config import Config
from monitor_everything.checks import CheckResult

def test_check_runner_initialization():
    config = Config()
    runner = CheckRunner(config)
    assert runner.config == config

def test_check_runner_runs_enabled_checks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=tmp_path, capture_output=True)
    
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")
    subprocess.run(["git", "add", "test.py"], cwd=tmp_path, capture_output=True)
    
    config = Config()
    config.data["checks"]["branch_awareness"] = True
    config.data["checks"]["linting"] = False
    
    runner = CheckRunner(config)
    results = runner.run_all_checks()
    
    assert results["branch"] == "main"
    assert len(results["checks"]) == 1
    assert results["checks"][0]["type"] == "branch_awareness"

def test_check_runner_protected_branch_stricter(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=tmp_path, capture_output=True)
    
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")
    subprocess.run(["git", "add", "test.py"], cwd=tmp_path, capture_output=True)
    
    config = Config()
    config.data["checks"]["branch_awareness"] = True
    config.data["behavior"]["branch_awareness"] = "warn"
    config.data["protected_branches"] = ["main"]
    
    runner = CheckRunner(config)
    results = runner.run_all_checks()
    
    assert results["is_protected"] == True
    assert results["checks"][0]["behavior"] == "interactive"

def test_check_runner_should_block():
    config = Config()
    runner = CheckRunner(config)
    
    results = {
        "checks": [
            {"result": CheckResult.FAIL, "behavior": "block"},
        ]
    }
    assert runner.should_block(results) == True
    
    results = {
        "checks": [
            {"result": CheckResult.FAIL, "behavior": "warn"},
        ]
    }
    assert runner.should_block(results) == False
    
    results = {
        "checks": [
            {"result": CheckResult.PASS, "behavior": "block"},
        ]
    }
    assert runner.should_block(results) == False
