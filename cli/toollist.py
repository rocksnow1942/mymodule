import click
import os

@click.group()
def toollist():
    pass


@toollist.command()
def ass():
    print('all available')



if __name__ == "__main__":
    toollist()