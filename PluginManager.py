import struct
from config import commandPrefix

from plugins.CPE import CPEplugin
from plugins.MessagePrint import MessagePrint
#from plugins.DebugPrint import DebugPrint
from plugins.ExampleCommand import ExampleCommand
from Constants import C2S

plugins = [CPEplugin(), MessagePrint()]

commands = [ExampleCommand()]

def callback(returndata, packet, data, S2C):
    if not S2C and packet == C2S['message']:
        returndata = commandCall(returndata, data)
    for pluginClass in plugins:
        if S2C:
            asd = pluginClass.S2Ccallbacks
        else:
            asd = pluginClass.C2Scallbacks

        if packet in asd:
            asd[packet](packet, data)
        if '*' in asd:
            asd['*'](packet, data)
    return returndata
    

def commandCall(returndata, data):
    _, type, msg = struct.unpack('cc64s', data)
    if type != b'\x00':
        return returndata
    
    msg = msg.decode(encoding="ascii", errors="ignore").rstrip(' ').lower()
    if not msg.startswith(commandPrefix):
        return returndata
 
    for commandClass in commands:
        if msg.startswith(commandPrefix + commandClass.name):
            return commandClass.call(returndata, msg.split(' ')[1:])

    return returndata