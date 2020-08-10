import struct
import Utils
from Constants import S2C, C2S, setReturnData, getReturnData
from PluginManager import callback

def getC2SPacket(data):
    for packet in C2S.values():
        if packet.id == data[:1]:
            return packet
    return False

def getS2CPacket(data):
    for packet in S2C.values():
        if packet.id == data[:1]:
            return packet
    return False

def parse(opcode, data, S2C):
    setReturnData(b'', b'')
    if S2C:
        packet = getS2CPacket(opcode)
        setReturnData(opcode+data, None)
    else:
        packet = getC2SPacket(opcode)
        setReturnData(None, opcode+data)
    if not packet:
        return False

    callback(packet, opcode+data, S2C)
    return getReturnData()