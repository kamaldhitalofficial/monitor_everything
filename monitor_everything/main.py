import click

__version__ = "0.1.0"

@click.group()
@click.version_option(version=__version__)
def cli():
    """Monitor Everything - Comprehensive pre-commit validation tool"""
    pass

@cli.command()
def setup():
    """Interactive setup wizard for configuring checks and hooks"""
    from monitor_everything.config import Config
    
    click.echo("Welcome to Monitor Everything setup!\n")
    
    config = Config()
    
    # Check selection
    click.echo("Select checks to enable:")
    config.data["checks"]["linting"] = click.confirm("  Enable linting (Ruff)?", default=False)
    config.data["checks"]["formatting"] = click.confirm("  Enable formatting (Black)?", default=False)
    config.data["checks"]["type_checking"] = click.confirm("  Enable type checking (Mypy)?", default=False)
    config.data["checks"]["tests"] = click.confirm("  Enable test execution (Pytest)?", default=False)
    config.data["checks"]["security"] = click.confirm("  Enable security checks?", default=False)
    
    # Protected branches
    click.echo("\nProtected branches configuration:")
    branches_input = click.prompt("  Enter protected branches (comma-separated)", default="main")
    config.data["protected_branches"] = [b.strip() for b in branches_input.split(",")]
    
    # Behavior configuration
    click.echo("\nDefault behavior for checks (block/warn/interactive):")
    for check in ["linting", "formatting", "type_checking", "tests", "security"]:
        if config.data["checks"][check]:
            behavior = click.prompt(f"  {check}", 
                                   type=click.Choice(["block", "warn", "interactive"]),
                                   default="interactive")
            config.data["behavior"][check] = behavior
    
    # Save configuration
    click.echo("\nSave configuration:")
    save_global = click.confirm("  Save as global default?", default=False)
    save_local = click.confirm("  Save in current repository?", default=True)
    
    if save_global:
        config.save(global_config=True)
        click.echo(f"✓ Global config saved to ~/.merc")
    
    if save_local:
        config.save(global_config=False)
        click.echo(f"✓ Local config saved to .merc")
    
    # Hook and alias installation
    from monitor_everything.hooks import install_hook, install_alias
    from monitor_everything.git_utils import is_git_repo
    
    if is_git_repo():
        click.echo("\nGit integration:")
        if click.confirm("  Install pre-commit hook?", default=True):
            success, message = install_hook()
            if success:
                click.echo(f"  ✓ {message}")
            else:
                click.echo(f"  ✗ {message}")
        
        if click.confirm("  Install git alias 'gc'?", default=True):
            install_globally = click.confirm("    Install globally?", default=False)
            success, message = install_alias(install_globally)
            if success:
                click.echo(f"  ✓ {message}")
            else:
                click.echo(f"  ✗ {message}")
    
    click.echo("\n✓ Setup complete!")

@cli.command()
def check():
    """Run all enabled checks on staged files"""
    from monitor_everything.config import Config
    from monitor_everything.runner import CheckRunner
    from monitor_everything.prompt import display_results, prompt_user_action
    from monitor_everything.git_utils import is_git_repo
    import sys
    
    if not is_git_repo():
        click.echo("Error: Not a git repository")
        sys.exit(1)
    
    config = Config()
    runner = CheckRunner(config)
    
    click.echo("Running checks...")
    results = runner.run_all_checks()
    
    display_results(results)
    
    if runner.should_block(results):
        sys.exit(1)
    
    has_issues = any(c['result'].value == 'fail' for c in results['checks'])
    if has_issues:
        if not prompt_user_action(results):
            sys.exit(1)
    
    click.echo("\n✓ All checks passed!")
    sys.exit(0)

@cli.group()
def config():
    """Manage configuration settings"""
    pass

@config.command(name="list")
def config_list():
    """Show current configuration"""
    from monitor_everything.config import Config
    import json
    
    config = Config()
    click.echo(json.dumps(config.data, indent=2))

@cli.command(name="install-hook")
def install_hook_cmd():
    """Install pre-commit git hook"""
    from monitor_everything.hooks import install_hook
    
    success, message = install_hook()
    if success:
        click.echo(f"✓ {message}")
    else:
        click.echo(f"✗ {message}")
        import sys
        sys.exit(1)

@cli.command(name="uninstall-hook")
def uninstall_hook_cmd():
    """Uninstall pre-commit git hook"""
    from monitor_everything.hooks import uninstall_hook
    
    success, message = uninstall_hook()
    if success:
        click.echo(f"✓ {message}")
    else:
        click.echo(f"✗ {message}")
        import sys
        sys.exit(1)

@cli.command(name="install-alias")
@click.option("--global", "global_alias", is_flag=True, help="Install alias globally")
def install_alias_cmd(global_alias):
    """Install git alias 'gc' for commit with checks"""
    from monitor_everything.hooks import install_alias
    
    success, message = install_alias(global_alias)
    if success:
        click.echo(f"✓ {message}")
        click.echo("  Usage: gc -m 'commit message'")
    else:
        click.echo(f"✗ {message}")
        import sys
        sys.exit(1)

@cli.command(name="uninstall-alias")
@click.option("--global", "global_alias", is_flag=True, help="Uninstall alias globally")
def uninstall_alias_cmd(global_alias):
    """Uninstall git alias 'gc'"""
    from monitor_everything.hooks import uninstall_alias
    
    success, message = uninstall_alias(global_alias)
    if success:
        click.echo(f"✓ {message}")
    else:
        click.echo(f"✗ {message}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    cli()
