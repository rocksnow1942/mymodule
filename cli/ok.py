from cli._version import __version__
import click
from cli.plugins import _plugins
from cli.dictionary import dictionary
from cli.utils import Config, TableDisplay,ColorText
import os,json
from mymodule import mkdirs


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()

def export_config(ctx,param,path):
    if path is None or ctx.resilient_parsing:
        return
    result = {}
    for name in Config.list_config():
        data = Config(name).readData()
        result[name]=data
    if path.endswith('-'):
        newtd=TableDisplay(color=ColorText({"[]":"fC"}))
        click.echo(newtd(title= ">>>[ Config Parameters ]<<<" ,text=json.dumps(result,indent=2).strip('{}') ))
    else:
        td = TableDisplay()
        mkdirs(path)
        filepath = os.path.join(path,'OK_config.json')
        with open(filepath,'wt') as f:
            json.dump(result,f,indent=2)
        click.echo(td(text=f' Config data Saved! \n File saved to:\n [{filepath}]'))
    ctx.exit()

def import_config(ctx,param,value):
    """
    from a file or url
    "url": "https://api.github.com/gists/02641f8b5a9e9c0de1a9b2a6825d3f60",
    https://gist.github.com/rocksnow1942/02641f8b5a9e9c0de1a9b2a6825d3f60
    """
    def sync(data):
        for name,settings in data.items():
            config=Config(name)
            config.saveData(settings)
            click.echo(td(text=f"<g>Success!</g> <y>{name}</y> configuration imported."))

    if value is None or ctx.resilient_parsing:
        return

    td = TableDisplay()
    if os.path.isfile(value):
        with open(value,'rt') as f:
            data = json.load(f)
        sync(data)
    else:
        if value == 'gist': value = "02641f8b5a9e9c0de1a9b2a6825d3f60"
        import requests
        url = f"https://api.github.com/gists/{value}"
        try:
            res = requests.request('GET',url,).json()
            if res.get('message',None):
                raise ValueError (f"Failed to load gist: [{url}]\nReason: <a> {res.get('message')} </a>")
            data = json.loads(res['files']['OK_config.json']['content'])
            sync(data)
        except Exception as e:
            click.echo(td(title= ">>> <r> ! Import Failed </r><<<" ,text=f"{e}"))
    ctx.exit()


@click.group(cls=click.CommandCollection)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,help='Show version.')
@click.option('--export-config',type=click.Path(allow_dash=True,resolve_path=True), callback=export_config,
              expose_value=False, is_eager=True,help='Export config to a file.')
@click.option('--import-config',callback=import_config,
              expose_value=False, is_eager=True,help='Import config from a file or gist.' )
@click.pass_context
def menu(ctx):
    "Main Entrance for plugins. And dictionary."
    pass
    # if ctx._depth == 2:
    #     click.echo(ctx.get_help())
    #     ctx.exit()

@_plugins.command()
def test():
    print('test inside ok')


menu.sources = [_plugins,dictionary]