import struct
import Utils
from Constants import S2C, C2S, setReturnData, getReturnData
from PluginManager import callback

#def paddedString(string: bytes):
#    if len(string) < 64:
#        string += b'\x20' * (64 - len(string))
#    if len(string) > 64:
#        return b"&cTODO: MESSAGE OVER 64 BYTES" + b'\x20' * (64 - 29)
#    return string

#def sendToClient(data: bytes):
#    returndata[0] += data

#def msgToClient(message: str, messageType=0):
#    message.replace('&', '%')
#    sendToClient(b"\x0d" + bytes([messageType]) + paddedString(message.encode("cp437")))

#def S_Message(packet, data):
#    _, type, msg = struct.unpack('cc64s', data)
#    if type == b'\x00':
#        Utils.sprint('MSG', msg.decode(encoding="ascii", errors="ignore"))

#def S_SetVelocity(packet, data):
#    _, x, y, z, xmode, ymode, zmode = struct.unpack('>ciiiccc', data)
#    msgToClient(f'Velocity {x/1000} {y/1000} {z/1000} with modes {xmode} {ymode} {zmode}')

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