 # res=subprocess.Popen(['pwd'],stdout=subprocess.PIPE,stdin=subprocess.PIPE, encoding="utf-8")
        # re = res.communicate()
        # print(re

import click
import os
import json
import subprocess
from cli.utils import TermRow, TermCol, TableDisplay
from mymodule import mkdirs


