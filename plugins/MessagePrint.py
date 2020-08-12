import struct
from Utils import Plugin, Packet, S2C, C2S

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'MessagePrint'
        self.S2Ccallbacks = {
            S2C['message']: self.S_Message,
        }
        self.onLoad()

    def S_Message(self, packet, data):
        _, type, msg = struct.unpack('cc64s', data)
        if type == b'\x00':
            print(msg.decode(encoding="ascii", errors="ignore").rstrip(' '))
