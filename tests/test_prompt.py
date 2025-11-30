from click.testing import CliRunner
from monitor_everything.prompt import display_results, prompt_user_action
from monitor_everything.checks import CheckResult

def test_display_results_no_checks():
    results = {
        "branch": "main",
        "is_protected": False,
        "files": ["test.py"],
        "checks": []
    }
    
    has_issues = display_results(results)
    assert has_issues is None

def test_display_results_with_pass():
    results = {
        "branch": "main",
        "is_protected": False,
        "files": ["test.py"],
        "checks": [
            {
                "name": "Test Check",
                "result": CheckResult.PASS,
                "message": "All good",
                "details": []
            }
        ]
    }
    
    has_issues = display_results(results)
    assert has_issues == False

def test_display_results_with_fail():
    results = {
        "branch": "main",
        "is_protected": False,
        "files": ["test.py"],
        "checks": [
            {
                "name": "Test Check",
                "result": CheckResult.FAIL,
                "message": "Issues found",
                "details": ["Error 1", "Error 2"]
            }
        ]
    }
    
    has_issues = display_results(results)
    assert has_issues == True

def test_prompt_user_action_blocking():
    results = {
        "checks": [
            {
                "result": CheckResult.FAIL,
                "behavior": "block",
                "details": []
            }
        ]
    }
    
    should_continue = prompt_user_action(results)
    assert should_continue == False

def test_prompt_user_action_no_issues():
    results = {
        "checks": [
            {
                "result": CheckResult.PASS,
                "behavior": "interactive",
                "details": []
            }
        ]
    }
    
    should_continue = prompt_user_action(results)
    assert should_continue == True
