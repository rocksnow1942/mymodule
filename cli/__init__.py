from cli.toollist import toollist 
from cli._version import __version__
import click
from cli.plugins import _plugins
from cli.dictionary import dictionary
from cli.folder import folder

@click.group(invoke_without_command=True,cls=click.CommandCollection)
@click.option('--version','-v',is_flag=True,default=False,help="Show current version.")
@click.pass_context
def menu(ctx,version):
    "Main Entrance for plugins. And dictionary."
    if version:
        click.echo(__version__)
    elif ctx._depth == 2:
        click.echo(ctx.get_help())
        ctx.exit()

menu.sources = [_plugins,dictionary]