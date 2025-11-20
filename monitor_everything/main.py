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
    
    click.echo("\n✓ Setup complete!")

@cli.command()
def check():
    """Run all enabled checks on staged files"""
    click.echo("Check command coming soon...")

@cli.group()
def config():
    """Manage configuration settings"""
    pass

@config.command(name="list")
def config_list():
    """Show current configuration"""
    click.echo("Config list coming soon...")

if __name__ == "__main__":
    cli()
