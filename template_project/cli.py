import logging

import click

from template_project.api.cli import api

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


cli.add_command(api)


@cli.command()
def example():
    print("Example command")


if __name__ == "__main__":
    cli()
