# Monitor Everything (me)

Comprehensive pre-commit validation tool with code quality, testing, and security checks.

## Installation

### Quick Install (one command)

```bash
curl -sSL https://raw.githubusercontent.com/kamaldhitalofficial/monitor_everything/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/kamaldhitalofficial/monitor_everything.git
cd monitor_everything
uv venv .venv
source .venv/bin/activate
uv pip install -e .
me setup
```

## Quick Start

```bash
# Run interactive setup wizard
me setup

# Run checks manually
me check

# View configuration
me config list
```

## Features

- [x] Basic CLI structure with Click
- [x] Configuration management (global + local)
- [x] Interactive setup wizard
- [x] Git utilities and branch detection
- [x] Check framework and registry system
- [x] Code quality checks (Ruff, Black, Mypy)
- [x] Test execution check (Pytest)
- [x] Security checks (secrets, file size)
- [x] Check execution engine
- [x] Interactive prompt system
- [x] Manual check command
- [x] Git hook installation
- [x] Git alias setup (gc command)
- [x] Config management commands
- [x] Branch protection with stricter validation

## Available Checks

• **Branch Awareness** - Shows current git branch
• **Linting (Ruff)** - Python code linting
• **Formatting (Black)** - Python code formatting
• **Type Checking (Mypy)** - Static type checking
• **Tests (Pytest)** - Run test suite
• **Security** - Detect secrets and large files

## Configuration

Configuration is stored in `.merc` files:
• Global: `~/.merc`
• Local: `.merc` in repository root

### Configuration Structure

```json
{
  "checks": {
    "linting": false,
    "formatting": false,
    "type_checking": false,
    "tests": false,
    "security": false,
    "branch_awareness": true
  },
  "protected_branches": ["main"],
  "behavior": {
    "linting": "interactive",
    "formatting": "interactive",
    "type_checking": "interactive",
    "tests": "block",
    "security": "block",
    "branch_awareness": "warn"
  }
}
```

### Behavior Options

• **block** - Prevent commit if check fails
• **warn** - Show warning but allow commit
• **interactive** - Prompt user for action

## Commands

### Setup

```bash
me setup
```

Interactive wizard to configure checks, protected branches, and install git integration.

### Check

```bash
me check
```

Run all enabled checks on staged files.

### Configuration

```bash
# Show current configuration
me config list

# Set configuration value
me config set checks.linting true

# Add protected branch
me config add-protected develop

# Remove protected branch
me config remove-protected develop
```

### Git Integration

```bash
# Install pre-commit hook
me install-hook

# Uninstall pre-commit hook
me uninstall-hook

# Install git alias 'gc'
me install-alias
me install-alias --global

# Uninstall git alias 'gc'
me uninstall-alias
me uninstall-alias --global
```

## Usage with Git Alias

After installing the git alias:

```bash
gc -m "your commit message"
```

This runs checks before committing. If checks pass, commit proceeds automatically.

## Protected Branches

Protected branches receive stricter validation:
• `warn` behavior becomes `interactive`
• Ensures critical branches maintain higher quality

## Tech Stack

• Python 3.13+
• Click for CLI
• UV for package management
