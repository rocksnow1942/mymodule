import click
from cli.plugins import plugins
from cli.toollist import toollist

"""
combine modules together
"""

menu = click.CommandCollection(sources=[plugins,toollist],
help="Main Entrance for tools.")


