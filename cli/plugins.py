import click
import os

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

class MyCLI(click.MultiCommand):
    """
    lazy load of sub commands from commands folder. 
    """
    commandList = {}
    def list_commands(self, ctx):
        rv = list(self.commandList.keys())
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        if name in self.commandList:
            return self.commandList[name]
        fn = os.path.join(plugin_folder, name + '.py')
        ns = {'__file__':fn}
        if os.path.isfile(fn):
            with open(fn) as f:
                # code = compile(f.read(), fn, 'exec')
                exec(f.read(), ns, ns)
            return ns['cli']
        else:
            return None

    def add_command(self,f):
        self.commandList[f.__name__] = f

    def add_command(self, cmd, name=None):
        """Registers another :class:`Command` with this group.  If the name
        is not provided, the name of the command is used.
        """
        name = name or cmd.name
        if name is None:
            raise TypeError("Command has no name.")
        if name in self.list_commands(1):
            raise RuntimeError(f'Command {name} already exist.')
        self.commandList[name] = cmd

    def command(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a command to
        the group.  This takes the same arguments as :func:`command` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        command = click.command

        def decorator(f):
            cmd = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        return decorator

# menu = MyCLI(help="Entry Point for other Commands",invoke_without_command=True)

@click.group(cls=MyCLI,)
@click.pass_context
def plugins(ctx):
   
    pass 

# @plugins.command()
# def cl():
#     """
#     wowo
#     """
#     print('hello')
