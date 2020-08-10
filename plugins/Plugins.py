from Constants import loadedPlugins, Plugin, sendMessage, setReturnData, loadPlugin
import glob

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
