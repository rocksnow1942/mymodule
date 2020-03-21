import click
import os
import json
import subprocess
from cli.utils import TermRow, TermCol, TableDisplay, Config
from mymodule import mkdirs

TL_CONFIG = Config('tools')

td = TableDisplay()
    
def displayMenu(data):
    dis = []
    for k in sorted(data.keys()):
        dis.append(f" >><g> [ {k} ] </g><< {data[k]['name']}  ")
    click.echo(td(title= "[>>Tools Menu<<]", text=[dis]))

def run_tool(key,data):
    """
    key is the key to command dictionary sotred in data dict. 
    data dict: key:{name: ... , command: ...}
    """
    if key in data:
        name = data[key]['name']
        command = data[key]['command']
        click.echo(td(text=f"Run [{name}]\n>>> {{{command}}}"))
        subprocess.run(command,shell=True)
    else:
        click.echo(td(title="",text=[[f"<a> '{key}' not in menu.</a>"]]))
        return

@click.group(invoke_without_command=True)
@click.pass_context
def toollist(ctx):
    """
    Open up tools menu. 
    Use tl config [-ops] to configure.
    """
    if ctx._depth == 2:
        # data = readData()
        data = TL_CONFIG.readData()
        # no downstream is called. print the menu and let user run script.
        displayMenu(data)
        key = click.prompt('Enter Key',type=str)
        return run_tool(key,data)

@toollist.command()
@click.argument('sele',nargs=1,)
def rt(sele):
    """
    Run option from tool list.
    """
    data = TL_CONFIG.readData()
    return run_tool(sele,data)

@toollist.command()
@click.option('-a','--add','ops',flag_value='add', help="Add new command.")
@click.option('-d','--delete','ops',flag_value='delete',help="Delete a command.")
@click.option('-e','--edit','ops',flag_value='edit',help="Edit a command.")
@click.option('-o','--open','ops',flag_value='open',help="Open command configure in editor.")
@click.pass_context
def config(ctx,ops):
    """
    To configure the tool list menu.
    """
    if not ops:
        click.echo(ctx.get_help())
        ctx.exit()

    if ops == "open":
        subprocess.run(f"open {TL_CONFIG.path}",shell=True)
        return

    data = TL_CONFIG.readData()
    if ops == "add":
        click.echo("Add a New Command")
        name = click.prompt('Enter Command Name', type=str)
        click.echo(f"You Entered: {name}\n")
        command = click.prompt('Enter Command Script',type=str)
        click.echo(f"You Entered: {command}\n")
        key = click.prompt('Enter Associated Key',type=str)
        click.echo(f"You Entered: {key}\n")
        if click.confirm('Do you want to save?',abort=True,default=True):
            temp = key 
            while temp in data:
                temp+="d"
            if temp != key:
                data[temp]=data.pop(key)
            data[key]={'name':name,'command':command}
            
    elif ops == "delete":
        displayMenu(data)
        key = click.prompt('Enter the command you wan to delete',type=str)
        if key in data:
            name = data.pop(key)['name']
        else:
            click.echo(td(title="",text=[[f"<a> '{key}' not in menu.</a>"]]))
            return
    elif ops == 'edit':
        displayMenu(data)
        key = click.prompt('Enter the command you wan to edit',type=str)
        if key not in data:
            click.echo(td(title="",text=[[f"<a> '{key}' not in menu.</a>"]]))
            return
        edit = data[key]
        name = click.prompt('Enter New Command Name', default=edit['name'])
        click.echo(f"You Entered: {name}\n")
        command = click.prompt('Enter New Command Script',default=edit['command'])
        click.echo(f"You Entered: {command}\n")
        newkey = click.prompt('Enter New Associated Key',default=key)
        click.echo(f"You Entered: {newkey}\n")
        if click.confirm('Do you want to save?',abort=True,default=True):
            data.pop(key)
            temp = newkey 
            while temp in data:
                temp+="d"
            if temp != newkey:
                data[temp]=data.pop(newkey)
            data[newkey]={'name':name,'command':command}

    TL_CONFIG.saveData(data,indent=2)
    
    click.echo(td(title="",text=f"<g> {ops.capitalize()} to '{name}' was saved.</g>"))
    
    


if __name__ == "__main__":
    toollist()

