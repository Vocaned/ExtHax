import typing

#[0] = sent to client
#[1] = sent to server
returndata = [b'', b'']

def setReturnData(S2C: typing.Union[None, bytes], C2S: typing.Union[None, bytes]):
    if S2C != None:
        returndata[0] = S2C
    if C2S != None:
        returndata[1] = C2S
    return returndata

def appendReturnData(S2C: typing.Union[None, bytes], C2S: typing.Union[None, bytes]):
    if S2C != None:
        returndata[0] += S2C
    if C2S != None:
        returndata[1] += C2S
    return returndata

def getReturnData():
    return returndata

#List of plugin classes currently loaded
loadedPlugins = {}

def loadPlugin(plugin: str):
    if plugin in loadedPlugins:
        print(f'Plugin {plugin} is already loaded.')
        return
    mod = __import__(f'plugins.{plugin}', fromlist=['plugin'])
    pluginClass = getattr(mod, 'plugin')
    loadedPlugins[plugin] = pluginClass()

def sendMessage(string: typing.Union[str, bytes], S2C: bool):
    # TODO: Check that client and server support LongerMessages CPE
    # TODO: Rewrite to put > in front of long S2C messages
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
                appendReturnData(b'\x0d\x00' + chunks[i], None)
            else:
                appendReturnData(None, b'\x0d\x01' + chunks[i])
        else:
            if S2C:
                appendReturnData(b'\x0d\x00' + chunks[i], None)
            else:
                appendReturnData(None, b'\x0d\x00' + chunks[i])

def stringToStr(string: bytes) -> str:
    return string.decode(encoding="ascii", errors="ignore").rstrip(' ')

class Packet(object):
    def __init__(self, packet_id, length):
        self.id = packet_id
        self.length = length

class Plugin(object):
    #from Constants import sendMessage
    def __init__(self):
        self.name = 'Unknown Plugin'
        self.description = ''
        self.S2Ccallbacks = {}
        self.C2Scallbacks = {}
        self.commands = {}

    def onLoad(self):
        sendMessage(f'&7Plugin {self.name} loaded.', True)

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

class FG:
	black =			"\x1B[30m"
	red =			"\x1B[31m"
	green =			"\x1B[32m"
	yellow =		"\x1B[33m"
	blue =			"\x1B[34m"
	magenta =		"\x1B[35m"
	cyan =			"\x1B[36m"
	white =			"\x1B[37m"
	brightblack =	"\x1B[90m"
	brightred =		"\x1B[91m"
	brightgreen =	"\x1B[92m"
	brightyellow =	"\x1B[93m"
	brightblue =	"\x1B[94m"
	brightmagenta =	"\x1B[95m"
	brightcyan =	"\x1B[96m"
	brightwhite =	"\x1B[97m"

class BG:
	black =			"\x1B[40m"
	red =			"\x1B[41m"
	green =			"\x1B[42m"
	yellow =		"\x1B[43m"
	blue =			"\x1B[44m"
	magenta =		"\x1B[45m"
	cyan =			"\x1B[46m"
	white =			"\x1B[47m"
	brightblack =	"\x1B[100m"
	brightred =		"\x1B[101m"
	brightgreen =	"\x1B[102m"
	brightyellow =	"\x1B[103m"
	brightblue =	"\x1B[104m"
	brightmagenta =	"\x1B[105m"
	brightcyan =	"\x1B[106m"
	brightwhite =	"\x1B[107m"

class Text:
	reset =			"\x1B[0m"
	bold =			"\x1B[1m"
	faint =			"\x1B[2m"
	italic =		"\x1B[3m"
	underline =		"\x1B[4m"
	blink =			"\x1B[5m"
	invert =		"\x1B[7m"
	conceal =		"\x1B[8m"
	strikethrough =	"\x1B[9m"
	franktur =		"\x1B[20m"
	framed =		"\x1B[51m"
	encircled =		"\x1B[52m"
	overlined =		"\x1B[53m"
	clear = 		"\x1B[2J"
	save =			"\x1B[s"
	restore =		"\x1B[u"

class Status:
	DEBUG = FG.magenta + "DEBUG"
	INFO = FG.brightcyan + "INFO"
	SUCCESS = FG.green + "SUCCESS"
	WARN = FG.yellow + "WARN"
	ERROR = FG.red + "ERROR"
	FATAL = BG.red + FG.black + "FATAL"

def sprint(status: str, value: str, fullColor=False):
	"""Print status updates"""
	label = "[" + status + Text.reset + "] "

	value = value.replace("\n", "\n        ")

	if fullColor:
		print(label + status.split("m")[0]+"m" + value, end=Text.reset + "\n")
	else:
		print(label + value, end=Text.reset + "\n")

