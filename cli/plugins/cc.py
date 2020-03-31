import click
import re
from cli.utils import TableDisplay
from mymodule import mkdirs
import os
from datetime import datetime
from pathlib import PurePath
import shutil


@click.command()
@click.option('--folder','-f',default=None,type=click.Path(exists=False, file_okay=False,resolve_path=True),help="Provide folder to clean.")
@click.option('--pattern','-p',default=None, help = "Use custom regex pattern to delete.")
def cli(folder,pattern):
    """
    Clean files from a folder using regex pattern search.\n
    Default using icloud sync duplicate pattern / [2-9]$/ .
    """
    td=TableDisplay()
    folder = folder or click.prompt(td(text="Enter [path/to/folder] you want to clean:")+'\n', default=os.getcwd())
    pattern = pattern or click.prompt(td(text="Enter regex pattern:")+'\n', default=" [2-9]$") 
    try:
        pattern = re.compile(pattern)
    except re.error as e:
        click.echo(td(text=f"Regex compile error: <r>{e}</r>"))
        return 
    if os.path.isdir(folder):       
        click.echo(td(text=f'Cleaning folder [{folder}] ...'))
        save , fileCount, folderCount= delete_by_pattern(folder,pattern) 
        click.echo(td(title=">>> <g>Result</g> <<<",
            text=f'Cleaning Done.\n{{{fileCount}}} files\n{{{folderCount}}} folders\nMoved to [{save}].'))
    else:
        click.echo(td(text=f"Path <r>{folder}</r> is invalid."))

def delete_by_pattern(path,pattern):
    regex = pattern.pattern
    movedFiles = 0
    movedFolders = 0
    tempfolder = PurePath(path) / '!DELETE SCRIPT TEMP FOLDER'
    filepath = tempfolder / 'Deleted files'
    folderpath = tempfolder / 'Deleted folders'
    mkdirs(tempfolder,filepath,folderpath)
    f = open(tempfolder/'!Deletion Log.txt', 'a')
    f.write(f'Start cleaning {path} on {datetime.now().strftime("%Y/%m/%d %H:%M")}\n')
    f.write(f"Cleaning pattern: >{regex}<\n")
    f.write('='*50+'\n')
    for root, dirs, files in os.walk(path):
        if str(tempfolder) in root:  # avoid looking into temp path.
            continue
        if pattern.search(root):  # if the root folder is matched.
            relative = PurePath(root).relative_to(path)
            click.echo(f'Move [FOLDER] <{relative}>')
            f.write(f'Move [FOLDER] <{root}>\n')
            shutil.move(root, folderpath / relative)
            movedFolders += 1
            continue
        for file in files:
            if pattern.search(file):
                click.echo(f'Move [ FILE ] <{file}>')
                f.write(f'Move [ FILE ] <{os.path.join(root, file)}>\n')
                os.rename(os.path.join(root, file), filepath/file)
                movedFiles += 1 #.append(oas.path.join(root, file))

    f.write('='*50+'\n')
    f.write(
        f'Moved {movedFiles} files, {movedFolders} folders, finished on {datetime.now().strftime("%Y/%m/%d %H:%M")}\n\n')
    f.close()
    return tempfolder, movedFiles, movedFolders
