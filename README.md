# [huik-module][huik]
[![python version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20-blue)][pythonwebsite] 
[![Alt text](https://img.shields.io/pypi/v/huik-module 'Hover to see this text.')][huik]

[huik]:https://pypi.org/project/huik-module
[pythonwebsite]: https://www.python.org/downloads/release/python-375

### **How to install**:

        pip install huik-module

### **Command Line Interface Usage**
Command Line Interface are built with [Click](https://click.palletsprojects.com/en/7.x/).

Use `command --help` for built in help info. 

#### tool list module `tl`
Tool list (`tl`) provide a way to make user defined shortcuts for frequently used shell commands. 
* `tl` to start tool list. 
* `tl --help` to show help menu. 
* `tl [command key]` to quickly invoke saved shell command.

    Hint: Shell commands are ran in a new process, if a command is changing 
    shell behavior this change will not be reflected in the current shell. 
    If user want to retain such behavior, one way to use `exec shell` 
    or `exec zsh` at the end of command. (see folder module for example)

#### folder module `fd`
Folder (`fd`) can mark folder as favorites and let user quickly navigate to that folder
in terminal. 
* `fd [favorite folder shortcut]` cd to saved folder.
* `fd -c` config use bash or zsh as default shell. 

    Under the hood, `fd` uses python subprocess to run shell script. 
    ```python
    subprocess.run("cd /path/to/folder;exec zsh",shell=True,)
    ```
    The subprocess start another process and run shell command. 
    Without `exec zsh`, after the subprocess exits, the current shell 
    will remain in the same folder. `exec zsh` or `exec bash` start a shell in 
    the subprocess and allow user input in that process. 

#### OK module `ok` 
OK module let user write / install plugins to extend its function. 

OK module also manages to import/export/sync configuration and plugins.

Some included plugins are: Dictionary `def`; calculator `cal`; github tools `git` 

One would need to use plugins if simple shell command is not sufficient 
in certain complex using scenarios. For example, to handle user 
inputs or pull data from the web. 

* `ok` or `ok --help` to show help menu.
* `ok sync` to configure Github gist id and user token for upload settings to github. 
User token is not needed for download public gist settings but required for create/upload settigns.
* `ok [command]` to run plugin commands.
* `ok plugins --help` to show help menu for configure plugins.
* `ok plugins -sf` or `--show-folder` show plugins folder. 

#### Plugins 
Plugins are single python files and stored under `cli/plugins` 
folder. These individual files are read and loaded at runtime. 

Basic structure:
```python
import click 
# other imports if needed 

@click.command() # optionally use click.group() to allow multicommands.
@click.option('--option') # add other options or arguments if needed.
def cli(option):
    """
    Documents
    """
    # handle option 
```
