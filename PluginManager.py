import struct
from config import commandPrefix
from Constants import loadedPlugins

def loadPlugin(plugin: str):
    if plugin in loadedPlugins:
        print(f'Plugin {plugin} is already loaded.')
        return
    mod = __import__(f'plugins.{plugin}', fromlist=['plugin'])
    pluginClass = getattr(mod, 'plugin')
    loadedPlugins[plugin] = pluginClass()

def callback(packet, data, S2C):
    if not S2C and packet.id == b'\00':
        init(data)
    if not S2C and packet.id == b'\x0D':
        commandCall(data)
    for pluginClass in loadedPlugins:
        pluginClass = loadedPlugins[pluginClass]
        if S2C:
            asd = pluginClass.S2Ccallbacks
        else:
            asd = pluginClass.C2Scallbacks

        if packet in asd:
            asd[packet](packet, data)
        if '*' in asd:
            asd['*'](packet, data)

def init(data):
    # Determine if client supports CPE
    # TODO: Currently assumes the server supports CPE
    _, _, _, _, padding = struct.unpack('cc64s64sc', data)
    if padding == b'\x42': # CPE magic number
        loadPlugin('CPE')

def commandCall(data):
    _, type, msg = struct.unpack('cc64s', data)
    if type != b'\x00':
        return
    
    msg = msg.decode(encoding="ascii", errors="ignore").rstrip(' ').lower()
    if not msg.startswith(commandPrefix):
        return
 
    cmd = msg.lstrip(commandPrefix).split(' ')[0]

    for pluginClas in loadedPlugins:
        pluginClass = loadedPlugins[pluginClass]
        if cmd in pluginClas.commands:
            return pluginClas.commands[cmd](msg.split(' ')[1:])