from cli._version import __version__
import click
from cli.plugins import _plugins
from cli.dictionary import dictionary
from cli.utils import Config, TableDisplay,ColorText
import os,json
from mymodule import mkdirs
from cli.plugins import plugin_folder
import requests
from datetime import datetime

td = TableDisplay()

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()

def export_config(ctx,param,path):
    if path is None or ctx.resilient_parsing:
        return
    result = extract_settings('conf')
    if path.endswith('-'):
        newtd=TableDisplay(color=ColorText({"[]":"fC"}))
        click.echo(newtd(title= ">>>[ Config Parameters ]<<<" ,text=json.dumps(result,indent=2).strip('{}') ))
    else:
        mkdirs(path)
        filepath = os.path.join(path,'OK_config.json')
        with open(filepath,'wt') as f:
            json.dump(result,f,indent=2)
        click.echo(td(text=f' Config data Saved! \n File saved to:\n [{filepath}]'))
    ctx.exit()

def extract_settings(settings):
    """
    extract all config files to a dictionary
    """
    data = {}
    if settings == 'conf':
        for name in Config.list_config():
            if name != 'sync_settings':
                data[name] = Config(name).readData()
    elif settings =='plugin':
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                with open(os.path.join(plugin_folder, filename), 'rt') as f:
                    data[filename] = f.read()
    return data

def write_settings(data,settings):
    """
    write all the config files to conf folder.
    """
    if settings == 'conf':
        for name,settings in data.items():
            if name!='sync_settings':
                config=Config(name)
                config.saveData(settings)
                click.echo(td(text=f"<g>Success!</g> <y>{name}</y> configuration imported."))
    elif settings == 'plugin':
        for name, txt in data.items():
            with open(os.path.join(plugin_folder, name), 'wt') as f:
                f.write(txt)
            click.echo(
                td(text=f"<g>Success!</g> Plugin <y>{name[:-3]}</y> imported."))    
 
def write_gist(data,auth,gist,settings):
    """
    write a data dict to gist.
    settings = 'plugin' or 'config'
    """
    url = f"https://api.github.com/gists/{gist}"
    headers = {
        'Authorization': f'token {auth}',
        'Content-Type': 'applicaiton/json'
    }
    payload = {
        "description": f"OK tools settings configuration and plugins",
        "files": {
            f"{settings}.json": {
                "content": json.dumps(data,indent=2),
            },
            "OK_config_lastupdate" : {
                "content": f'Last update time: {datetime.now().strftime("%c")}'
            }
        }
    }
    try:
        res = requests.patch(url,headers=headers,data = json.dumps(payload))
        if res.status_code == 200:
            click.echo(
                td(text=f"<g>Successfully synced</g> <y>{settings}</y> <g>settings!</g>\nGist @ [https://gist.github.com/{gist}]"))
        else:
            jsontd = TableDisplay(color=ColorText({"[]": "fR"}))
            click.echo(jsontd(title=">>> [Sync failed with following response] <<<",
                          text=json.dumps(res.json(), indent=2).strip("{}")))
    except Exception as e:
        click.echo(td(title=">>> <r> ! Sync Failed </r><<<", text=f"{e}"))

def extract_gist(gist,settings):
    url = f"https://api.github.com/gists/{gist}"
    try:
        res = requests.request('GET',url,).json()
        if res.get('message',None):
            raise ValueError (f"Failed to load gist: [{url}]\nReason: <a> {res.get('message')} </a>")
        data = json.loads(res['files'][f'{settings}.json']['content'])
        return data
    except Exception as e:
        click.echo(td(title= ">>> <r> ! Import Failed </r><<<" ,text=f"{e}")) 
        return None

def import_config(ctx,param,value):
    """
    from a file or url
    "url": "https://api.github.com/gists/02641f8b5a9e9c0de1a9b2a6825d3f60",
    """
    if value is None or ctx.resilient_parsing:
        return
    data = json.load(value)
    write_settings(data,settings='conf')
    ctx.exit()

def execute_sync(direction,option,sync_settings):
    gist = sync_settings.get('gist', None)
    if not gist:
        click.echo(
            td(text="<a> Set up gist ID to sync. </a>\nRefer to: [https://gist.github.com/]"))
        return 
    if direction == 'up':
        auth = sync_settings.get('auth', None)
        if not auth:
            click.echo(
                td(text="<a> Set up Auth Token to Upload settings. </a>\nRefer to: [https://github.com/settings/tokens]"))
            return
        data = extract_settings(option)
        write_gist(data,auth,gist,option)
        return 
    elif direction == 'down':
        data = extract_gist(gist,option)
        write_settings(data,option)
        return


@click.group(cls=click.CommandCollection)
@click.option('--version','-V', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,help='Show version.')
@click.option('--export-config',type=click.Path(allow_dash=True,resolve_path=True), callback=export_config,
              expose_value=False, is_eager=True,help='Export config to a file.')
@click.option('--import-config',type=click.File('r'),callback=import_config,
              expose_value=False, is_eager=True,help='Import config from a file.' )
@click.pass_context
def menu(ctx):
    "Main Entrance for plugins. And dictionary."
    pass

menu.sources = [_plugins, dictionary]


@_plugins.command()
@click.option('--set-auth','-sa','auth',default=None,help="Set Github Auth Token for sync.")
@click.option('--set-gist','-sg','gist',default=None,help="Set Github Gist ID for sync.")
@click.option('--upload','-u','direction',flag_value='up',help="Upload settings.")
@click.option('--download','-d','direction',flag_value='down',help="Download settings.")
@click.option('--plugin','-p','option',flag_value='plugin',help="Sync plugins.")
@click.option('--conf','-c','option',flag_value='conf',help="Sync configuration.")
@click.pass_context
def sync(ctx,auth,direction,option,gist):
    """
    Sync plugins or config with a gist.
    """
    config = Config('sync_settings')
    data = config.readData()
    # for syncing: need gist, auth. if only gist, can download, 
    showhelp = True
    if auth:
        showhelp = False
        data.update(auth=auth)
        config.saveData(data)
        click.echo(td(text=f"Saved auth: [{auth}]."))
        
    if gist:
        showhelp = False
        data.update(gist=gist)
        config.saveData(data)
        click.echo(td(text=f"Saved gist ID: [{gist}]."))
       
    if direction:
        if not option:
            pp = td(
                text=f"No sync option specified. \nDo you want to sync <g>both plugin and conf</g>?") + '\n'
            click.confirm(pp,default=False,abort=True)
            execute_sync(direction,'plugin',data)
            execute_sync(direction,'conf',data)
        else:
            execute_sync(direction,option,data)
        ctx.exit() 
    if option:
        pp = td(text=f"You are going to sync >> [{option}] <<\n<r>No syncing direction specified.</r>\nYou must specify upload / download before continue.") + '\n'
        direction = click.prompt( pp,type=click.Choice(['up','down'],case_sensitive=False))
        execute_sync(direction, option, data)
        ctx.exit()
    
    if showhelp:
        click.echo(ctx.get_help())
