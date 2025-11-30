import click
from monitor_everything.checks import CheckResult

def display_results(results):
    click.echo(f"\n📍 Branch: {results['branch']}")
    if results['is_protected']:
        click.echo("⚠️  Protected branch - stricter validation applied")
    
    click.echo(f"\n📁 Files staged: {len(results['files'])}")
    
    if not results['checks']:
        click.echo("\n✓ No checks enabled")
        return
    
    click.echo("\n" + "=" * 60)
    
    has_issues = False
    for check in results['checks']:
        if check['result'] == CheckResult.PASS:
            click.echo(f"✓ {check['name']}: {click.style(check['message'], fg='green')}")
        elif check['result'] == CheckResult.WARN:
            click.echo(f"⚠ {check['name']}: {click.style(check['message'], fg='yellow')}")
            if check['details']:
                for detail in check['details'][:5]:
                    click.echo(f"  {detail}")
        elif check['result'] == CheckResult.FAIL:
            has_issues = True
            click.echo(f"✗ {check['name']}: {click.style(check['message'], fg='red')}")
            if check['details']:
                for detail in check['details'][:5]:
                    click.echo(f"  {detail}")
                if len(check['details']) > 5:
                    click.echo(f"  ... and {len(check['details']) - 5} more")
    
    click.echo("=" * 60)
    return has_issues

def prompt_user_action(results):
    has_blocking = False
    has_interactive = False
    
    for check in results['checks']:
        if check['result'] == CheckResult.FAIL:
            if check['behavior'] == 'block':
                has_blocking = True
            elif check['behavior'] == 'interactive':
                has_interactive = True
    
    if has_blocking:
        click.echo("\n❌ Commit blocked due to critical issues")
        click.echo("Fix the issues above before committing")
        return False
    
    if has_interactive:
        click.echo("\n⚠️  Issues found - what would you like to do?")
        choice = click.prompt(
            "Choose action",
            type=click.Choice(['abort', 'continue', 'details']),
            default='abort'
        )
        
        if choice == 'abort':
            click.echo("Commit aborted")
            return False
        elif choice == 'details':
            for check in results['checks']:
                if check['result'] == CheckResult.FAIL and check['details']:
                    click.echo(f"\n{check['name']}:")
                    for detail in check['details']:
                        click.echo(f"  {detail}")
            
            if click.confirm("\nProceed with commit?", default=False):
                return True
            else:
                click.echo("Commit aborted")
                return False
        else:
            return True
    
    return True
