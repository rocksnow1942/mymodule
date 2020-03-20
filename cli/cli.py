import click
from cli.plugins import _plugins
from cli.toollist import toollist
from cli.dictionary import dictionary

"""
combine modules together
"""

@click.group(invoke_without_command=True,cls=click.CommandCollection)
@click.option('--version','-v',is_flag=True,default=False,help="Show current version.")
@click.pass_context
def menu(ctx,version):
    "Main Entrance for tools."
    if version:
        from cli import __version__
        click.echo(__version__)
    elif ctx._depth == 2:
        click.echo(ctx.get_help())
        ctx.exit()



menu.sources = [_plugins,toollist,dictionary]