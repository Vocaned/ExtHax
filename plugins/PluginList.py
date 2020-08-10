from Constants import loadedPlugins, Plugin, sendMessage, setReturnData

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'PluginList'
        self.description = 'Plugin related commands'
        self.commands = {
            'plugins': self.pluginListCmd
        }
        self.onLoad()

    def pluginListCmd(self, args):
        setReturnData(None, b'')
        sendMessage('&eLoaded plugins:', True)
        for plugin in loadedPlugins:
            sendMessage(f'&7 - {plugin}', True)