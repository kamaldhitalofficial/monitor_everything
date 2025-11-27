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

class RuffCheck(Check):
    def __init__(self):
        super().__init__("Ruff Linting")
    
    def run(self, files: List[str]) -> CheckOutput:
        import subprocess
        import shutil
        
        if not shutil.which("ruff"):
            return CheckOutput(
                result=CheckResult.WARN,
                message="Ruff not installed",
                details=["Install with: uv pip install ruff"]
            )
        
        python_files = [f for f in files if f.endswith(".py")]
        if not python_files:
            return CheckOutput(
                result=CheckResult.PASS,
                message="No Python files to check",
                details=[]
            )
        
        try:
            result = subprocess.run(
                ["ruff", "check"] + python_files,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return CheckOutput(
                    result=CheckResult.PASS,
                    message="No linting issues found",
                    details=[]
                )
            else:
                return CheckOutput(
                    result=CheckResult.FAIL,
                    message="Linting issues found",
                    details=result.stdout.strip().split("\n")
                )
        except Exception as e:
            return CheckOutput(
                result=CheckResult.FAIL,
                message=f"Error running ruff: {str(e)}",
                details=[]
            )

class BlackCheck(Check):
    def __init__(self):
        super().__init__("Black Formatting")
    
    def run(self, files: List[str]) -> CheckOutput:
        import subprocess
        import shutil
        
        if not shutil.which("black"):
            return CheckOutput(
                result=CheckResult.WARN,
                message="Black not installed",
                details=["Install with: uv pip install black"]
            )
        
        python_files = [f for f in files if f.endswith(".py")]
        if not python_files:
            return CheckOutput(
                result=CheckResult.PASS,
                message="No Python files to check",
                details=[]
            )
        
        try:
            result = subprocess.run(
                ["black", "--check"] + python_files,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return CheckOutput(
                    result=CheckResult.PASS,
                    message="All files formatted correctly",
                    details=[]
                )
            else:
                return CheckOutput(
                    result=CheckResult.FAIL,
                    message="Formatting issues found",
                    details=result.stderr.strip().split("\n")
                )
        except Exception as e:
            return CheckOutput(
                result=CheckResult.FAIL,
                message=f"Error running black: {str(e)}",
                details=[]
            )

class MypyCheck(Check):
    def __init__(self):
        super().__init__("Mypy Type Checking")
    
    def run(self, files: List[str]) -> CheckOutput:
        import subprocess
        import shutil
        
        if not shutil.which("mypy"):
            return CheckOutput(
                result=CheckResult.WARN,
                message="Mypy not installed",
                details=["Install with: uv pip install mypy"]
            )
        
        python_files = [f for f in files if f.endswith(".py")]
        if not python_files:
            return CheckOutput(
                result=CheckResult.PASS,
                message="No Python files to check",
                details=[]
            )
        
        try:
            result = subprocess.run(
                ["mypy"] + python_files,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return CheckOutput(
                    result=CheckResult.PASS,
                    message="No type errors found",
                    details=[]
                )
            else:
                return CheckOutput(
                    result=CheckResult.FAIL,
                    message="Type errors found",
                    details=result.stdout.strip().split("\n")
                )
        except Exception as e:
            return CheckOutput(
                result=CheckResult.FAIL,
                message=f"Error running mypy: {str(e)}",
                details=[]
            )

registry.register("branch_awareness", BranchAwarenessCheck)
registry.register("linting", RuffCheck)
registry.register("formatting", BlackCheck)
registry.register("type_checking", MypyCheck)

class PytestCheck(Check):
    def __init__(self):
        super().__init__("Pytest Tests")
    
    def run(self, files: List[str]) -> CheckOutput:
        import subprocess
        import shutil
        
        if not shutil.which("pytest"):
            return CheckOutput(
                result=CheckResult.WARN,
                message="Pytest not installed",
                details=["Install with: uv pip install pytest"]
            )
        
        try:
            result = subprocess.run(
                ["pytest", "-v"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                summary = [l for l in lines if "passed" in l]
                return CheckOutput(
                    result=CheckResult.PASS,
                    message="All tests passed",
                    details=summary
                )
            else:
                lines = result.stdout.strip().split("\n")
                return CheckOutput(
                    result=CheckResult.FAIL,
                    message="Tests failed",
                    details=lines[-10:]
                )
        except Exception as e:
            return CheckOutput(
                result=CheckResult.FAIL,
                message=f"Error running pytest: {str(e)}",
                details=[]
            )

registry.register("tests", PytestCheck)

class SecurityCheck(Check):
    def __init__(self):
        super().__init__("Security Checks")
        self.secret_patterns = [
            (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})', "API Key"),
            (r'(?i)(secret[_-]?key|secretkey)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})', "Secret Key"),
            (r'(?i)(password)\s*[:=]\s*["\']([^"\']{8,})', "Password"),
            (r'(?i)(token)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})', "Token"),
            (r'(?i)(aws[_-]?access[_-]?key[_-]?id)\s*[:=]\s*["\']?([A-Z0-9]{20})', "AWS Access Key"),
            (r'(?i)(aws[_-]?secret[_-]?access[_-]?key)\s*[:=]\s*["\']?([a-zA-Z0-9/+=]{40})', "AWS Secret Key"),
        ]
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def run(self, files: List[str]) -> CheckOutput:
        import re
        import os
        
        issues = []
        
        for file_path in files:
            if not os.path.exists(file_path):
                continue
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                size_mb = file_size / (1024 * 1024)
                issues.append(f"{file_path}: Large file ({size_mb:.1f}MB)")
            
            # Check for secrets in text files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern, secret_type in self.secret_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            issues.append(f"{file_path}:{line_num}: Possible {secret_type} detected")
            except (UnicodeDecodeError, PermissionError):
                pass
        
        if issues:
            return CheckOutput(
                result=CheckResult.FAIL,
                message=f"Security issues found ({len(issues)})",
                details=issues
            )
        else:
            return CheckOutput(
                result=CheckResult.PASS,
                message="No security issues found",
                details=[]
            )

registry.register("security", SecurityCheck)
