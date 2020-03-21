import click
import os
import json
import subprocess
from mymodule import mkdirs
from cli.utils import TermRow, TermCol, TableDisplay, Config

config = Config('folders')

@click.group()
def folder():
    """
    Open favorite folders by $ fd \n
    """
    pass


@folder.command()
def mk():
    """
    Mark folder to favorites.
    """
    print(os.getcwd())
       
    pass 


@folder.command()
def cd():
    """
    cd to favorites
    """

@folder.command()
def ve():
    """
    activate virtual environment
    """
