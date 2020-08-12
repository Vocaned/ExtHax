from Utils import loadedPlugins, Plugin, sendMessage, setReturnData, loadPlugin
import glob
from os import sys
from importlib import reload

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'Plugins'
        self.description = 'Plugin related commands'
        self.commands = {
            'plugin': self.pluginCmd,
            'plugins': self.pluginCmd,
            'pluginlist': self.pluginListCmd,
            'loadplugin': self.loadPluginCmd,
            'unloadplugin': self.unloadPluginCmd,
            'reloadplugin': self.reloadPluginCmd
        }
        self.onLoad()

    def pluginCmd(self, args):
        if len(args) == 1:
            if args[0] == 'list':
                return self.pluginListCmd(args)
        elif len(args) == 2:
            if args[0] == 'load':
                return self.loadPluginCmd([args[1],])
            elif args[0] == 'unload':
                return self.unloadPluginCmd([args[1],])
            elif args[0] == 'reload':
                return self.reloadPluginCmd([args[1],])
        return self.pluginListCmd(args)

    def pluginListCmd(self, args):
        sendMessage('&eLoaded plugins:', True)
        for plugin in loadedPlugins:
            sendMessage(f"&a - {plugin}", True)

        sendMessage('&eUnloaded plugins:', True)
        for file in glob.glob('plugins/*.py'):
            file = file.replace('plugins/', '').rsplit('.', 1)[0]
            if file != '__init__' and file not in loadedPlugins:
                sendMessage(f"&c - {file}", True)

    def loadPluginCmd(self, args):
        if len(args) > 1:
            sendMessage('&cToo many arguments.', True)
        else:
            loadPlugin(args[0])

    def unloadPluginCmd(self, args):
        if len(args) > 1:
            sendMessage('&cToo many arguments.', True)
        elif args[0] not in loadedPlugins:
            sendMessage('&cPlugin not loaded.', True)
        else:
            sendMessage(f'&7Plugin {args[0]} unloaded.', True)
            del loadedPlugins[args[0]]

    def reloadPluginCmd(self, args):
        if len(args) > 1:
            sendMessage('&cToo many arguments.', True)
        elif args[0] not in loadedPlugins:
            sendMessage('&cPlugin not loaded.', True)
        else:
            # TODO: Reload doesn't re-initialize the class. Not sure if that should be done
            reload(sys.modules[f'plugins.{args[0]}'])
            sendMessage(f'&7Plugin {args[0]} reloaded.', True)