import click
from cli.plugins import _plugins
from cli.toollist import toollist
from cli.dictionary import dictionary

"""
combine modules together
"""

menu = click.CommandCollection(sources=[_plugins,toollist,dictionary],
help="Main Entrance for tools.")


