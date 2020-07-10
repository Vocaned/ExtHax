import struct
import Utils
from config import debug

clientCPEs = []
serverCPEs = []
CPEs = []
entrycount = 0

#[0] = sent to client
#[1] = sent to server
returndata = [b'', b'']

def NOP(packet, data):
    pass

addLen = lambda packet,length: Packet(packet.id, packet.length + length, callback=packet.callback)
setLen = lambda packet,length: Packet(packet.id, length, callback=packet.callback)

def S_ExtEntry(packet, data):
    global serverCPEs
    _, name, ver = struct.unpack('>c64si', data)
    serverCPEs.append((name.strip(), ver))

def C_ExtInfo(packet, data):
    global entrycount
    _, _, entrycount = struct.unpack('>c64sh', data)

def C_ExtEntry(packet, data):
    global CPEs, clientCPEs, entrycount, S2C, C2S
    _, name, ver = struct.unpack('>c64si', data)
    clientCPEs.append((name.strip(), ver))
    entrycount -= 1
    if entrycount == 0:
        CPEs = [i for i in clientCPEs if i in serverCPEs]
        for CPE in CPEs:
            CPEname = CPE[0].decode('utf-8')
            Utils.sprint(Utils.Status.INFO, f"CPE {CPEname} v{CPE[1]} enabled.")
            if CPEname == 'EnvMapAppearance':
                S2C['EnvSetMapAppearance'] =    addLen(S2C['EnvSetMapAppearance'], 4)
            elif CPEname == 'BlockDefinitionsExt' and CPE[1] > 1:
                S2C['DefineBlockExt'] =         addLen(S2C['DefineBlockExt'], 3)
            elif CPEname == 'ExtEntityPositions':
                C2S['posOri'] =                 addLen(C2S['posOri'], 6)
                S2C['spawnPlayer'] =            addLen(S2C['spawnPlayer'], 6)
                S2C['posOri'] =                 addLen(S2C['posOri'], 6)
                S2C['ExtAddEntity2'] =          addLen(S2C['ExtAddEntity2'], 6)
                S2C['SetSpawnpoint'] =          addLen(S2C['SetSpawnpoint'], 6)
            elif CPEname == 'FastMap':
                S2C['lvlInit'] =                addLen(S2C['lvlInit'], 4)
            elif CPEname == 'CustomModels' and CPE[1] == 2:
                S2C['DefineModelPart'] =        setLen(S2C['DefineModelPart'], 167)
            elif CPEname == 'ExtendedTextures':
                S2C['DefineBlock'] =            addLen(S2C['DefineBlock'], 3)
                S2C['DefineBlockExt'] =         addLen(S2C['DefineBlockExt'], 6)
            elif CPEname == 'ExtendedBlocks':
                S2C['posOri'] =                 addLen(S2C['posOri'], 1)
                C2S['posOri'] =                 addLen(C2S['posOri'], 1)
                C2S['setBlock'] =               addLen(C2S['setBlock'], 1)
                S2C['setBlock'] =               addLen(S2C['setBlock'], 1)
                S2C['HeldBlock'] =              addLen(S2C['HeldBlock'], 1)
                S2C['SetBlockPermission'] =     addLen(S2C['SetBlockPermission'], 1)
                S2C['RemoveBlockDefinition'] =  addLen(S2C['RemoveBlockDefinition'], 1)
                S2C['BulkBlockUpdate'] =        addLen(S2C['BulkBlockUpdate'], 64)
                S2C['SetInventoryOrder'] =      addLen(S2C['SetInventoryOrder'], 2)
                S2C['SetHotbar'] =              addLen(S2C['SetHotbar'], 1)
                S2C['DefineBlock'] =            addLen(S2C['DefineBlock'], 1)
                S2C['DefineBlockExt'] =         addLen(S2C['DefineBlockExt'], 1)

def S_Message(packet, data):
    _, type, msg = struct.unpack('cc64s', data)
    if type == b'\x00':
        Utils.sprint('MSG', msg.decode(encoding="ascii", errors="ignore"))

class Packet():
    def __init__(self, packet_id, length, callback=NOP):
        self.id = packet_id
        self.length = length
        self.callback = callback

C2S = {
    # Vanilla
    'playerId' :              Packet(b'\x00', 131),
    'setBlock' :              Packet(b'\x05', 8),
    'posOri' :                Packet(b'\x08', 10),
    'message' :               Packet(b'\x0D', 66),

    # CPE
    'ExtInfo' :               Packet(b'\x10', 67, callback=C_ExtInfo),
    'ExtEntry' :              Packet(b'\x11', 69, callback=C_ExtEntry),
    'CustomBlockSupportLvl' : Packet(b'\x13', 2),
    'PlayerClicked' :         Packet(b'\x22', 15),
    'TwoWayPing' :            Packet(b'\x2B', 4)
}


S2C = {
    # Vanilla
    'serverId' :              Packet(b'\x00', 131),
    'ping' :                  Packet(b'\x01', 1),
    'lvlInit' :               Packet(b'\x02', 1),
    'lvlChunk' :              Packet(b'\x03', 1028),
    'lvlFinal' :              Packet(b'\x04', 7),
    'setBlock' :              Packet(b'\x06', 8),
    'spawnPlayer' :           Packet(b'\x07', 74),
    'posOri' :                Packet(b'\x08', 10),
    'posOriUpdate' :          Packet(b'\x09', 7),
    'posUpdate' :             Packet(b'\x0A', 5),
    'oriUpdate' :             Packet(b'\x0B', 4),
    'despawn' :               Packet(b'\x0C', 2),
    'message' :               Packet(b'\x0D', 66, callback=S_Message),
    'disconnect' :            Packet(b'\x0E', 65),
    'updateUser' :            Packet(b'\x0F', 2),

    # CPE
    'ExtInfo' :               Packet(b'\x10', 67),
    'ExtEntry' :              Packet(b'\x11', 69, callback=S_ExtEntry),
    'ClickDistance' :         Packet(b'\x12', 3),
    'CustomBlockSupportLvl' : Packet(b'\x13', 2),
    'HeldBlock' :             Packet(b'\x14', 3),
    'SetTextHotKey' :         Packet(b'\x15', 134),
    'ExtAddPlayerName' :      Packet(b'\x16', 196),
    'AddEntity' :             Packet(b'\x17', 130),
    'ExtRemovePlayerName' :   Packet(b'\x18', 3),
    'EnvSetColor' :           Packet(b'\x19', 8),
    'MakeSelection' :         Packet(b'\x1A', 86),
    'RemoveSelection' :       Packet(b'\x1B', 2),
    'SetBlockPermission' :    Packet(b'\x1C', 4),
    'ChangeModel' :           Packet(b'\x1D', 66),
    'EnvSetMapAppearance' :   Packet(b'\x1E', 73),
    'EnvSetWeatherType' :     Packet(b'\x1F', 2),
    'HackControl' :           Packet(b'\x20', 8),
    'ExtAddEntity2' :         Packet(b'\x21', 138),
    'DefineBlock' :           Packet(b'\x23', 80),
    'RemoveBlockDefinition' : Packet(b'\x24', 2),
    'DefineBlockExt' :        Packet(b'\x25', 85),
    'BulkBlockUpdate' :       Packet(b'\x26', 1282),
    'SetTextColor' :          Packet(b'\x27', 6),
    'SetMapEnvUrl' :          Packet(b'\x28', 65),
    'SetMapEnvProperty' :     Packet(b'\x29', 6),
    'SetEntityProperty' :     Packet(b'\x2A', 7),
    'TwoWayPing' :            Packet(b'\x2B', 4),
    'SetInventoryOrder' :     Packet(b'\x2C', 3),
    'SetHotbar' :             Packet(b'\x2D', 3),
    'SetSpawnpoint' :         Packet(b'\x2E', 3),
    'SetVelocity' :           Packet(b'\x2F', 16),
    'DefineEffect' :          Packet(b'\x30', 36),
    'SpawnEffect' :           Packet(b'\x31', 26),
    'DefineModel' :           Packet(b'\x32', 116),
    'DefineModelPart' :       Packet(b'\x33', 104),
    'UndefineModel' :         Packet(b'\x34', 2)
}


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
    global returndata
    if S2C:
        packet = getS2CPacket(opcode)
        returndata = [opcode+data, b'']
    else:
        packet = getC2SPacket(opcode)
        returndata = [b'', opcode+data]
    if not packet:
        return False
    packet.callback(packet, opcode+data)
    return returndata