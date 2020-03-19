import re,os
from colorama import init, Fore,Back,Style
from textwrap import TextWrapper
from terminaltables import SingleTable

TermRow, TermCol = [int(i) for i in os.popen('stty size', 'r').read().split()]    

class ColorText():
    """
    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL
    """
    _color ={"K":"BLACK","R":"RED","Y":"YELLOW","G":"GREEN","B":'BLUE',"M":"MAGENTA","C":"CYAN","W":"WHITE",}
    _style={"D":"DIM","N":"NORMAL","B":"BRIGHT"}
    _mapping = {"f":_color,"s":_style,"b":_color}
    _type={'f':Fore,'b':Back,"s":Style}
    def __init__(self,mapping={"[]":"fBsB","{}":"fR"}):
        """
        mapping: { pattern : color }
        pattern: "[]"/"{}"/(<p>,</p>)
        color:"fBbWsD"
        """
        self.color = {}
        ptns = []
        for k,i in mapping.items():
            color = ""
            for (s,c) in zip(i[::2],i[1::2]):
                color+=getattr(self._type[s],self._mapping[s][c])
            ptns.append((f"{re.escape(k[0])}(?P<{i}>.*?){re.escape(k[1])}"))
            self.color[i]=color
        self.pattern = re.compile("|".join(ptns),flags=re.DOTALL)

    def format(self,text):
        return self(text)

    def __call__(self,text,):
        def repl(x):
            mk = [k for k,i in x.groupdict().items() if i!=None][0]
            ct = x.groupdict()[mk]
            return self.color[mk]+ct+Style.RESET_ALL
        return self.pattern.sub(repl,text)


class TableDisplay():
    def __init__(self,color=ColorText(mapping={"[]":"fC",("<g>","</g>") : "fG",("<a>","</a>"):"bR","{}":"bB"})):
        self.col = (TermCol)
        self.color=color

    def format(self,title="",text=[]):
        """
        text = [ [ row 1 [ line1, line2 ] ], [row 2 [ lines]] ]
        if text is a string, then convert to single row, but respect the \n
        """
        if isinstance(text,str):
            text = [[i for i in text.split('\n')]]
        tw = TextWrapper(fix_sentence_endings=True,width=self.col-4)
        table_data = [ [self.color("\n".join(tw.fill(j,) for j in i))] for i in text]
        table = SingleTable(table_data,self.color(title))
        table.inner_row_border = True
        return table.table

    def __call__(self,title="",text=[]):
        return self.format(title,text)
