import struct
from config import commandPrefix, initPlugins
from Utils import loadedPlugins, loadPlugin, Plugin, setReturnData, sendMessage

def init(data):
    loadPlugin('Plugins')

    # Determine if client supports CPE
    # TODO: Currently assumes the server supports CPE
    _, _, _, _, padding = struct.unpack('cc64s64sc', data)
    if padding == b'\x42': # CPE magic number
        loadPlugin('CPE')

    for plugin in initPlugins:
        loadPlugin(plugin)

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

def commandCall(data):
    _, type, msg = struct.unpack('cc64s', data)
    if type > b'\x01':
        return

    msg = msg.decode(encoding="ascii", errors="ignore").rstrip(' ')
    if not msg.startswith(commandPrefix):
        return

    setReturnData(None, b'')

    cmd = msg.lstrip(commandPrefix).split(' ')[0].lower()

    for pluginClass in loadedPlugins:
        pluginClass = loadedPlugins[pluginClass]
        if cmd in pluginClass.commands:
            return pluginClass.commands[cmd](msg.split(' ')[1:])

    sendMessage(f'&cUnknown command &7{commandPrefix}{cmd}', True)