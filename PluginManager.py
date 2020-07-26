from plugins.CPE import CPEplugin
from plugins.MessagePrint import MessagePrint
#from plugins.DebugPrint import DebugPrint

plugins = [CPEplugin(), MessagePrint()]

def callback(packet, data, S2C):
    for pluginClass in plugins:
        if S2C:
            asd = pluginClass.S2Ccallbacks
        else:
            asd = pluginClass.C2Scallbacks

        if packet in asd:
            asd[packet](packet, data)
        if '*' in asd:
            asd['*'](packet, data)