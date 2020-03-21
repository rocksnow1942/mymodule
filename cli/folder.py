import click
import os
import json
import subprocess
from mymodule import mkdirs
from cli.utils import TermRow, TermCol, TableDisplay, Config

data = Config('folders')



@click.group()
def folder():
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
