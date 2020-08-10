#[0] = sent to client
#[1] = sent to server
returndata = [b'', b'']

def setReturnData(S2C, C2S):
    if S2C != None:
        returndata[0] = S2C
    if C2S != None:
        returndata[1] = C2S
    return returndata

def appendReturnData(S2C, C2S):
    if S2C != None:
        returndata[0] += S2C
    if C2S != None:
        returndata[1] += C2S
    return returndata

def getReturnData():
    return returndata

#List of plugin classes currently loaded
loadedPlugins = {}

def sendMessage(string, S2C: bool):
    # TODO: Check that client and server support LongerMessages CPE
    chunks = []
    if type(string) == str:
        string = string.encode(encoding="ascii", errors="ignore")
    for chunk in [string[i:i+64] for i in range(0, len(string), 64)]:
        if len(chunk) < 64:
            chunk += b'\x20' * (64 - len(chunk))
        chunks.append(chunk)
    
    for i in range(len(chunks)):
        if i < len(chunks)-1:
            if S2C:
                appendReturnData(b'\x0d\x01' + chunk, None)
            else:
                appendReturnData(None, b'\x0d\x01' + chunk)
        else:
            if S2C:
                appendReturnData(b'\x0d\x00' + chunk, None)
            else:
                appendReturnData(None, b'\x0d\x00' + chunk)

class Packet(object):
    def __init__(self, packet_id, length):
        self.id = packet_id
        self.length = length

class Plugin(object):
    def __init__(self):
        self.name = 'Unknown Plugin'
        self.description = ''
        self.S2Ccallbacks = {}
        self.C2Scallbacks = {}
        self.commands = {}

    def onLoad(self):
        print(f'Plugin {self.name} loaded.')

C2S = {
    # Vanilla
    'playerId' :              Packet(b'\x00', 131),
    'setBlock' :              Packet(b'\x05', 9),
    'posOri' :                Packet(b'\x08', 10),
    'message' :               Packet(b'\x0D', 66),

    # CPE
    'ExtInfo' :               Packet(b'\x10', 67),
    'ExtEntry' :              Packet(b'\x11', 69),
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
    'message' :               Packet(b'\x0D', 66),
    'disconnect' :            Packet(b'\x0E', 65),
    'updateUser' :            Packet(b'\x0F', 2),

    # CPE
    'ExtInfo' :               Packet(b'\x10', 67),
    'ExtEntry' :              Packet(b'\x11', 69),
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
    'SetSpawnpoint' :         Packet(b'\x2E', 9),
    'SetVelocity' :           Packet(b'\x2F', 16),
    'DefineEffect' :          Packet(b'\x30', 36),
    'SpawnEffect' :           Packet(b'\x31', 26),
    'DefineModel' :           Packet(b'\x32', 116),
    'DefineModelPart' :       Packet(b'\x33', 104),
    'UndefineModel' :         Packet(b'\x34', 2)
}