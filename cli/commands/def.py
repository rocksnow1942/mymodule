import click
import requests
from cli.utils import ColorText,TableDisplay



def lookupMW(word,limit):
    url1=f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=51697108-9265-4243-808b-27710ef1937a"
    url2=f"https://www.dictionaryapi.com/api/v3/references/medical/json/{word}?key=4e9ac5ef-b27a-44e0-a416-dc9ce902267b"
    try:
        r1 = requests.request("GET", url1, ).json()
        r2 = requests.request("GET", url2, ).json()
        def process(r):
            result = []
            for k,d in enumerate(r[0:limit]):
                if not isinstance(d,dict):
                    continue
                _def = [("<gDef {}.g> [{}]".format(k+1,d.get('fl','None')))]
                for i,l in enumerate(d.get('shortdef',[])):
                    _def.append(f"  [{i+1}]. {l}")
                result.append(_def)
            return result
        res1 = process(r1)
        res2 = process(r2)
        result = [["{From M-W Collegiate Dictionary}"]]+res1+[["{From M-W Medical Dictionary}"]]+res2

        return result
    except Exception as e:
        return e





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
@click.option('-u','--urban','-urban','dictionary',flag_value="urban",default=False,help="Use Urban Dictionary")
@click.option('-mw','--mw','-m','-mw','dictionary',flag_value="mw",default=True,help="Use M-W Dictionary")
@click.option("--dictionary",'-d',type=click.Choice(['mw',"urban"],case_sensitive=False),default='mw',help="Select M-W or Urban Dictionary")
@click.option("--limit",'-l',default=5,help="Limit explanation entries")
@click.pass_context
def cli(ctx,word,limit,dictionary):
    """
    Urban Dictionary or Merriam-Webster Dictionary.
    """
    if not word:
        click.echo(ctx.get_help())
        word = click.prompt('Please enter a word', type=str)
    else:
        word = " ".join(word)
    bkcolor = ColorText(mapping={"[]":"fC",("<g","g>") : "fG",("<alert>","</alert>"):"bR","{}":"bB"})
    if dictionary == "urban":
        result = lookupUrban(word,limit)
    else:
        result = lookupMW(word,limit)
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
