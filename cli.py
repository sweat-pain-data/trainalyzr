#!/usr/bin/env python

import logging
import click
from trainalyzr.cli.ingest import ingest


class Context:  # pylint: disable=too-few-public-methods
    def __init__(self, debug=False):
        self.debug = debug


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = Context(debug)
    logging.basicConfig(
        level='DEBUG' if ctx.obj.debug else 'WARN',
        format="%(asctime)-15s [%(levelname)s] %(message)s")


cli.add_command(ingest)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
