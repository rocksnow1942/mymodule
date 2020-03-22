import click
import subprocess as sub
from datetime import datetime as date
import socket
from cli.utils import TableDisplay

@click.command()
@click.argument("comment",nargs=-1,)
@click.option('--init','-i',help="Init git package with .gitignore and README.md")
def cli(comment,init):
    """
    git pull add commit push
    4 step in one.
    """
    msg = " ".join(comment)
    click.echo('\nGit pull')
    sub.run('git pull',shell=True,)
    click.echo('\nCommit to Git')
    if not msg:
        msg = click.prompt("Enter a comment",show_default=True,
            default=f"ON: {date.now().strftime('%c')}, FROM: {socket.gethostname()}")
    p = sub.run(f'git add . \n git commit -m "{msg}" \n git push',shell=True)

    result = sub.run('git config --get remote.origin.url',stdout=sub.PIPE,encoding='utf-8',shell=True).stdout
    td = TableDisplay()
    click.echo(td(title='>>> <g>! Success</g> <<<',text=f"Commited to [{result.strip()}]"))
