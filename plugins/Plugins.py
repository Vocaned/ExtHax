from Constants import loadedPlugins, Plugin, sendMessage, setReturnData, loadPlugin

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'Plugins'
        self.description = 'Plugin related commands'
        self.commands = {
            'plugins': self.pluginListCmd,
            'pluginlist': self.pluginListCmd,
            'loadplugin': self.loadPluginCmd
        }
        self.onLoad()

    def pluginListCmd(self, args):
        sendMessage('&eLoaded plugins:', True)
        for plugin in loadedPlugins:
            sendMessage(f'&7 - {plugin}', True)

    def loadPluginCmd(self, args):
        if len(args) > 1:
            sendMessage('&cToo many arguments.', True)
        else:
            loadPlugin(args[0])
