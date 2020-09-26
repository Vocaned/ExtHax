import struct
from Utils import Plugin, Packet, S2C, sendMessage, setReturnData

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'ForceMOTD'
        self.S2Ccallbacks = {
            S2C['HackControl']: self.hackcontrol,
            S2C['serverId']: self.serverid
        }
        self.onLoad()

    def hackcontrol(self, packet, data):
        setReturnData(b'', None)
        sendMessage(b'&f[&cForceMOTD&f] &7Server tried to change hackcontrol', True)

    def serverid(self, packet, data):
        _, _, _, motd, _ = struct.unpack('>cc64s64sc', data)
        setReturnData(b'', None)
        sendMessage(b'&f[&cForceMOTD&f] &7Server tried to set motd to &f'+motd, True)