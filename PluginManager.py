import struct
from config import commandPrefix

from plugins.CPE import CPEplugin
from plugins.MessagePrint import MessagePrint
#from plugins.DebugPrint import DebugPrint
from plugins.ExampleCommand import ExampleCommand


plugins = [CPEplugin(), MessagePrint(), ExampleCommand()]

def callback(packet, data, S2C):
    if not S2C and packet.id == b'\x0D':
        commandCall(data)
    for pluginClass in plugins:
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
    if type != b'\x00':
        return
    
    msg = msg.decode(encoding="ascii", errors="ignore").rstrip(' ').lower()
    if not msg.startswith(commandPrefix):
        return
 
    cmd = msg.lstrip(commandPrefix).split(' ')[0]

    for commandClass in plugins:
        if cmd in commandClass.commands:
            return commandClass.commands[cmd](msg.split(' ')[1:])