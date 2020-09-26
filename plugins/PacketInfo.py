from Utils import Plugin, Packet, S2C, C2S, sendMessage
import struct

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'PacketInfo'
        self.S2Ccallbacks = {
            S2C['SetVelocity']: self.velocity,
            S2C['HackControl']: self.hackcontrol,
            S2C['serverId']: self.serverid
        }
        self.onLoad()

    def velocity(self, packet, data):
        _, X, Y, Z, XMode, YMode, ZMode = struct.unpack('>ciiiccc', data)
        sendMessage(f'&a[PacketInfo] &fSet player velocity to {X/10000} {Y/10000} {Z/10000}', True)

    def hackcontrol(self, packet, data):
        _, fly, noclip, speed, respawn, thirdperson, jump = struct.unpack('>cccccch', data)

        enabled = []
        disabled = []

        for i,n in zip((fly, noclip, speed, respawn, thirdperson), ('fly', 'noclip', 'speed', 'respawn', 'thirdperson')):
            if i == b'\x01':
                enabled.append(n)
            else:
                disabled.append(n)

        for i in enabled:
            sendMessage(f'&a[PacketInfo] HackControl: &a{i} allowed', True)

        for i in disabled:
            sendMessage(f'&a[PacketInfo] HackControl: &a{i} disallowed', True)

    def serverid(self, packet, data):
        _, _, _, motd, _ = struct.unpack('>cc64s64sc', data)
        sendMessage(b'&a[PacketInfo] &fMOTD was changed to: '+motd, True)