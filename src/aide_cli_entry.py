import sys
from src.cli.cli import cli as _cli

def main():
    # Expose the click CLI as console script entry point
    _cli(prog_name='aide')  # ensures help shows 'aide'