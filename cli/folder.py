 # res=subprocess.Popen(['pwd'],stdout=subprocess.PIPE,stdin=subprocess.PIPE, encoding="utf-8")
        # re = res.communicate()
        # print(re
import click
import os
import json
import subprocess
from mymodule import mkdirs


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
