import click
import requests
from cli.utils import ColorText,TableDisplay



def lookupUrban(word,limit):
    """
    look up word on urban dictionary, export a upper limit
    """
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term":word}
    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "939867f4a7mshb9a0332b3f15521p1c6740jsn27072326be60"
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        r=response.json()
        result = []


        for k,d in enumerate(r['list'][0:limit]):

            _def = [("<gDef {}.g> {}".format(k+1,d.get('definition',"None")))]
            txt    =[f'<gExample:g>']
            exp = list((d.get('example',"None")).split('\n'))
            result.append(_def+txt+exp)

        return result
    except Exception as e:
        return e

@click.command()
@click.argument("word",nargs=-1)
@click.option("--limit",'-l',default=5,help="Limit explanation")
def cli(word,limit):
    """
    Urban dictionary.
    """
    word = " ".join(word)
    bkcolor = ColorText(mapping={"[]":"fC",("<g","g>") : "fG",("<alert>","</alert>"):"bR"})
    result = lookupUrban(word,limit)
    if isinstance(result,list) and result:
        td=TableDisplay(bkcolor)
        click.echo("")
        title = " DEFINITION : <g"+f">>> {word.capitalize()} <<<g>"
        click.echo(td.format(title=title,text=result))
        click.echo("")
    else:
        click.echo("")
        click.echo(bkcolor(f'<alert>!Unable to find online definition. \n <{result}> </alert>'))
        click.echo("")
