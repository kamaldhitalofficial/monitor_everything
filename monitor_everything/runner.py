from monitor_everything.config import Config
from monitor_everything.checks import registry, CheckResult
from monitor_everything.git_utils import get_staged_files, is_protected_branch, get_current_branch
from typing import List, Dict

class CheckRunner:
    def __init__(self, config: Config):
        self.config = config
    
    def run_all_checks(self) -> Dict:
        files = get_staged_files()
        branch = get_current_branch()
        is_protected = is_protected_branch(branch, self.config.get("protected_branches", []))
        
        results = {
            "branch": branch,
            "is_protected": is_protected,
            "files": files,
            "checks": []
        }
        
        enabled_checks = self.config.get("checks", {})
        
        for check_type, enabled in enabled_checks.items():
            if not enabled:
                continue
            
            check_class = registry.get(check_type)
            if not check_class:
                continue
            
            check = check_class()
            result = check.run(files)
            
            behavior = self.config.get(f"behavior.{check_type}", "interactive")
            if is_protected:
                if behavior == "warn":
                    behavior = "interactive"
            
            results["checks"].append({
                "name": check.name,
                "type": check_type,
                "result": result.result,
                "message": result.message,
                "details": result.details,
                "behavior": behavior
            })
        
        return results
    
    def should_block(self, results: Dict) -> bool:
        for check in results["checks"]:
            if check["result"] == CheckResult.FAIL:
                if check["behavior"] == "block":
                    return True
        return False
