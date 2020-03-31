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
def cli(folder):
    "Clean residual files from icloud sync, using /.* [2-9]/ pattern"
    td=TableDisplay()
    folder = folder or click.prompt(td(text="Enter [path/to/folder] you want to clean:")+'\n', default=os.getcwd())
    if os.path.isdir(folder):
        click.echo(td(text=f'Cleaning folder [{folder}] ...'))
        save , fileCount, folderCount= delete_stupid_apple_cloud_sync_2(folder)
        click.echo(td(title=">>> <g>Result</g> <<<",
            text=f'Cleaning Done.\n{{{fileCount}}} files\n{{{folderCount}}} folders\nMoved to [{save}].'))
    else:
        click.echo(td(text=f"Path <r>{folder}</r> is not a valid."))

def delete_stupid_apple_cloud_sync_2(path):
    movedFiles = [] 
    movedFolders = []
    pattern = re.compile('.* [2-9]')
    tempfolder = PurePath(path) / '!DELETE SCRIPT TEMP FOLDER'
    filepath = tempfolder / 'Deleted files'
    folderpath = tempfolder / 'Deleted folders'
    mkdirs(tempfolder,filepath,folderpath)
    
    for root, dirs, files in os.walk(path):
        if str(tempfolder) in root:  # avoid looking into temp path.
            continue
        move = bool(pattern.match(root)) # if the root is matched.
        if move:
            # shutil.rmtree(root)
            relative = PurePath(root).relative_to(path)
            print(f'Move Folder < {relative} >')
            shutil.move(root, folderpath / relative)
            movedFolders.append(root)
            continue

        for file in files:
            if pattern.match(file):
                print(f'Remove File < {file} >')
                os.rename(os.path.join(root, file), filepath/file)
                movedFiles.append(os.path.join(root, file))
    with open(tempfolder/'!Deletion Log.txt', 'a') as f:
        f.write(
            f'Moved {len(movedFiles)} files, {len(movedFolders)} folders on {datetime.now().strftime("%Y/%m/%d %H:%M")}\n')
        f.write('\n'.join(movedFiles))
        f.write('\n'+'='*50+'\n')
        f.write('\n'.join(movedFolders))
        f.write('\n'*2)
    return tempfolder, len(movedFiles), len(movedFolders)
