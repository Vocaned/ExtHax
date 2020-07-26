from Constants import Plugin, Packet, S2C, C2S
import struct

class CPEplugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'CPE Support'
        self.S2Ccallbacks = {
            S2C['ExtEntry']: self.S_ExtEntry
        }
        self.C2Scallbacks = {
            C2S['ExtInfo']: self.C_ExtInfo,
            C2S['ExtEntry']: self.C_ExtEntry
        }
        self.onLoad()

    clientCPEs = []
    serverCPEs = []
    CPEs = []
    entrycount = 0

    addLen = lambda self,packet,length: Packet(packet.id, packet.length + length)
    setLen = lambda self,packet,length: Packet(packet.id, length)

    def S_ExtEntry(self, packet, data):
        _, name, ver = struct.unpack('>c64si', data)
        self.serverCPEs.append((name.strip(), ver))

    def C_ExtInfo(self, packet, data):
        _, _, self.entrycount = struct.unpack('>c64sh', data)

    def C_ExtEntry(self, packet, data):
        _, name, ver = struct.unpack('>c64si', data)
        self.clientCPEs.append((name.strip(), ver))
        self.entrycount -= 1
        if self.entrycount == 0:
            self.CPEs = [i for i in self.clientCPEs if i in self.serverCPEs]
            for CPE in self.CPEs:
                CPEname = CPE[0].decode('utf-8')
                CPEver = CPE[1]
                #Utils.sprint(Utils.Status.INFO, f"CPE {CPEname} v{CPEver} enabled.")
                print(f"CPE {CPEname} v{CPEver} enabled.")
                if CPEname == 'EnvMapAppearance':
                    S2C['EnvSetMapAppearance'] =    self.addLen(S2C['EnvSetMapAppearance'], 4)
                elif CPEname == 'BlockDefinitionsExt' and CPEver > 1:
                    S2C['DefineBlockExt'] =         self.addLen(S2C['DefineBlockExt'], 3)
                elif CPEname == 'ExtEntityPositions':
                    C2S['posOri'] =                 self.addLen(C2S['posOri'], 6)
                    S2C['spawnPlayer'] =            self.addLen(S2C['spawnPlayer'], 6)
                    S2C['posOri'] =                 self.addLen(S2C['posOri'], 6)
                    S2C['ExtAddEntity2'] =          self.addLen(S2C['ExtAddEntity2'], 6)
                    S2C['SetSpawnpoint'] =          self.addLen(S2C['SetSpawnpoint'], 6)
                elif CPEname == 'FastMap':
                    S2C['lvlInit'] =                self.addLen(S2C['lvlInit'], 4)
                elif CPEname == 'CustomModels' and CPEver == 2:
                    S2C['DefineModelPart'] =        self.setLen(S2C['DefineModelPart'], 167)
                elif CPEname == 'ExtendedTextures':
                    S2C['DefineBlock'] =            self.addLen(S2C['DefineBlock'], 3)
                    S2C['DefineBlockExt'] =         self.addLen(S2C['DefineBlockExt'], 6)
                elif CPEname == 'ExtendedBlocks':
                    C2S['posOri'] =                 self.addLen(C2S['posOri'], 1)
                    C2S['setBlock'] =               self.addLen(C2S['setBlock'], 1)
                    S2C['setBlock'] =               self.addLen(S2C['setBlock'], 1)
                    S2C['HeldBlock'] =              self.addLen(S2C['HeldBlock'], 1)
                    S2C['SetBlockPermission'] =     self.addLen(S2C['SetBlockPermission'], 1)
                    S2C['RemoveBlockDefinition'] =  self.addLen(S2C['RemoveBlockDefinition'], 1)
                    S2C['BulkBlockUpdate'] =        self.addLen(S2C['BulkBlockUpdate'], 64)
                    S2C['SetInventoryOrder'] =      self.addLen(S2C['SetInventoryOrder'], 2)
                    S2C['SetHotbar'] =              self.addLen(S2C['SetHotbar'], 1)
                    S2C['DefineBlock'] =            self.addLen(S2C['DefineBlock'], 1)
                    S2C['DefineBlockExt'] =         self.addLen(S2C['DefineBlockExt'], 1)