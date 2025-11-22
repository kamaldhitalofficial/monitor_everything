from enum import Enum
from dataclasses import dataclass
from typing import List

class CheckResult(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"

@dataclass
class CheckOutput:
    result: CheckResult
    message: str
    details: List[str] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = []

class Check:
    def __init__(self, name: str):
        self.name = name
    
    def run(self, files: List[str]) -> CheckOutput:
        raise NotImplementedError

class CheckRegistry:
    def __init__(self):
        self._checks = {}
    
    def register(self, check_type: str, check_class):
        self._checks[check_type] = check_class
    
    def get(self, check_type: str):
        return self._checks.get(check_type)
    
    def list_available(self):
        return list(self._checks.keys())

registry = CheckRegistry()

class BranchAwarenessCheck(Check):
    def __init__(self):
        super().__init__("Branch Awareness")
    
    def run(self, files: List[str]) -> CheckOutput:
        from monitor_everything.git_utils import get_current_branch
        
        branch = get_current_branch()
        if branch:
            return CheckOutput(
                result=CheckResult.PASS,
                message=f"Current branch: {branch}",
                details=[f"You are committing to branch: {branch}"]
            )
        else:
            return CheckOutput(
                result=CheckResult.WARN,
                message="Could not detect current branch",
                details=[]
            )

registry.register("branch_awareness", BranchAwarenessCheck)
