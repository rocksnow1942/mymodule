import click


@click.command()
@click.argument("comment",nargs=-1,)
def cli(comment):
    """
    git pull, add . , commit -m 'comment', git push
    4 step in one.
    """
    import subprocess as sub
    from datetime import datetime as date
    import socket 
    msg = " ".join(comment)
    click.echo('\nGit pull')
    sub.run('git pull',shell=True,) 
    if not msg:
        msg = click.prompt("Enter a comment",show_default=True,
            default=f"Commit on {date.now().strftime('%c')}, From {socket.gethostname()}")
    p = sub.run(f'git add . \n git commit -m "{msg}" \n git push',shell=True) 
