import click
import httpx
import os
from urllib.parse import urljoin

DEFAULT_URL = os.environ.get('AIDE_AGENT_URL', 'http://127.0.0.1:8123')

@click.group()
def cli():
    pass

@cli.command()
@click.argument("prompt", nargs=-1)
@click.option("--apply", is_flag=True, default=False, help="Apply the plan (dangerous).")
@click.option("--dry-run/--no-dry-run", default=True)
def ask(prompt, apply, dry_run):
    """Send a natural language request to the aide.ai agent"""
    text = " ".join(prompt)
    payload = {"prompt": text, "apply": apply, "dry_run": dry_run}
    url = os.environ.get("AIDE_AGENT_URL", DEFAULT_URL)
    with httpx.Client(timeout=60) as client:
        r = client.post(urljoin(url, "/api/v1/prompt"), json=payload)
        if r.status_code != 200:
            click.echo("Error from agent: " + r.text)
            raise SystemExit(1)
        data = r.json()
        click.echo("Explanation:\n")
        click.echo(data.get("explanation", "")[:2000])
        click.echo("\nPlan:")
        for step in data.get("plan", []):
            click.echo(f"- {step.get('type')}: {step.get('command')}")
        click.echo("\nAudit:", nl=False)
        click.echo(data.get("audit_entry"))

if __name__ == "__main__":
    cli()