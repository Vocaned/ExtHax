import struct
import Utils
from config import debug
PACKET = "[\x1B[35mPACKET\x1B[0m]"
PREFIX = "."

#[0] = sent to client
#[1] = sent to server
returndata = [b'', b'']

# server = To server

def paddedString(string):
    if len(string) < 64:
        string += b'\x20' * (64 - len(string))
    if len(string) > 64:
        return b"&cTODO: MESSAGE OVER 64 BYTES" + b'\x20' * (64 - 29)
    return string

def sendPacket(data, server):
    global returndata
    # printPacket(data.hex()[:2], data.hex()[2:], server)
    if not server:
        returndata[0] = bytearray(returndata[0] + data)
    else:
        data = data.replace(b"&", b"%")
        returndata[1] = bytearray(returndata[1] + data)


def sendMessage(string, server, messageType=0):
    prefix = ""
    if not server:
        prefix = "&f[&aExtHAX&f] "
    sendPacket(b"\x0d" + bytes([messageType]) + paddedString((prefix + string).encode("cp437")), server)

def printPacket(packet_id, string, server=False):
    if debug:
        if server:
            print(PACKET + "[S->C][" + str(packet_id) + "] " + str(string))
        else:
            print(PACKET + "[C->S][" + str(packet_id) + "] " + str(string))

def h_posandori(data, server):
    #printPacket("0x8", data[:16].hex(), server)
    if server:
        # entityID = struct.unpack('c', data[1:2])[0]
        # X, Y, Z = struct.unpack('>iii', data[2:14])
        return data[16:]
    else:
        # entityID = struct.unpack('h', data[1:3])[0]
        # X, Y, Z = struct.unpack('>iii', data[3:15])
        return data[17:]
    #printPacket("0x8", f"ID {str(entityID)} {str(round(X/32))}, {str(round(Y/32-1))}, {str(round(Z/32))}", server)

def h_posandoriupdate(data, server):
    return data[7:]

def h_posupdate(data, server):
    return data[5:]

def h_oriupdate(data, server):
    return data[4:]

def h_addplayername(data, server):
    return data[196:]

def h_removeplayername(data, server):
    return data[3:]

def h_ping(data, server):
    """server = struct.unpack('?', data[1:2])[0]
    if server:
        printPacket("2b", "Pong!", True)
    else:
        printPacket("2b", "Ping!")"""
    return data[4:]

def h_playerclick(data, server):
    return data[15:]

def h_identification(data, server):
    return data[131:]

def h_envcolor(data, server):
    return data[8:]

def h_changemodel(data, server):
    return data[66:]

def h_hackcontrol(data, server):
    return data[8:]

def h_mapenv(data, server):
    return data[6:]

def h_weather(data, server):
    return data[2:]

def h_velocity(data, server):
    X,Y,Z = struct.unpack('>iii', data[1:13])
    sendMessage("Velocity set to " + str(X) + ", " + str(Y) + ", " + str(Z), False)
    return data[16:]

def h_reach(data, server):
    #dist = struct.unpack('>h', data[1:3])[0]/32
    #print(str(dist))
    return data[3:]

def h_message(data, server):
    msg = data[2:66].decode("cp437").strip()
    printPacket("2b", msg, server)
    if not server and msg.startswith("."):
        clientCommands(msg)
    return data[66:]

def clientCommands(msg):
    global returndata
    returndata[1] = b''
    commands = [
        ("help", "Shows all commands"),
        ("hello", "Hello, World!"),
        ("tp", "Teleports to X Y Z"),
        ("motd", "Change the MOTD"),
        ("client", "Change client name"),
        ("model", "Change your model"),
        ("reach", "Change how far you can reach"),
        ("env", "Change the environment"),
        ("boost", "Change velocity")
    ]

    try:
        args = msg.split()
        args[0] = args[0].lstrip(PREFIX).lower()
        if args[0] == "help":
            sendMessage("&bby Fam0r", False, 100)
            sendMessage("&bCommands:", False)
            for command in commands:
                sendMessage("&3" + PREFIX + command[0] + " &f- &3" + command[1], False)
        elif args[0] == "hello":
            sendMessage("&bHello, World!", False)
        elif args[0] == "tp":
                X, Y, Z = msg.split()[1:4]
                sendPacket(b"\x08\xFF" + struct.pack('>iii', int(X)*32+16, int(Y)*32+32, int(Z)*32+16) + b"\x00\x00", False)
        elif args[0] == "motd":
            sendPacket(b"\x00\x07" + paddedString(b"ExtHAX") + paddedString(" ".join(msg.split(" ")[1:]).encode("cp437")) + b"\x64", False)
            sendMessage("&bMOTD set to " + " ".join(msg.split(" ")[1:]), False)
        elif args[0] == "client":
            sendPacket(b"\x10" + paddedString(" ".join(msg.split(" ")[1:]).encode("cp437")) + b"\x00\x00", True)
            sendMessage("&bClient name was set to " + " ".join(msg.split(" ")[1:]), False)
        elif args[0] == "model":
            sendPacket(b"\x1d\xff" + paddedString(" ".join(msg.split(" ")[1:]).encode("cp437")), False)
            sendMessage("&bChanged was set to " + " ".join(msg.split(" ")[1:]), False)
        elif args[0] == "reach":
            sendPacket(b"\x12" + struct.pack('>h', int(int(msg.split()[1])*32)), False)
            sendMessage("&bReach distance was set to " + msg.split()[1], False)
        elif args[0] == "env":
            vals = ("sky", "cloud", "fog", "shadow", "sun", "weather")
            if len(args) < 3 or args[1].lower() not in vals:
                sendMessage("&cInvalid environment. Possible values:", False)
                sendMessage("&csky, cloud, fog, shadow, sun, weather", False)
                return
            args[1] = args[1].lower()
            args[2] = args[2].lower()
            if args[1] == "sky":
                r,g,b = Utils.hex2RGB(args[2])
                sendPacket(b"\x19\x00" + struct.pack(">hhh", r,g,b), False)
            elif args[1] == "cloud" or args[1] == "clouds":
                r,g,b = Utils.hex2RGB(args[2])
                sendPacket(b"\x19\x01" + struct.pack(">hhh", r,g,b), False)
            elif args[1] == "fog":
                r,g,b = Utils.hex2RGB(args[2])
                sendPacket(b"\x19\x02" + struct.pack(">hhh", r,g,b), False)
            elif args[1] == "shadow" or args[1] == "shadows":
                r,g,b = Utils.hex2RGB(args[2])
                sendPacket(b"\x19\x03" + struct.pack(">hhh", r,g,b), False)
            elif args[1] == "sun":
                r,g,b = Utils.hex2RGB(args[2])
                sendPacket(b"\x19\x04" + struct.pack(">hhh", r,g,b), False)
            elif args[1] == "weather":
                if args[2] == "sun":
                    sendPacket(b"\x1f\x00", False)
                elif args[2] == "rain":
                    sendPacket(b"\x1f\x01", False)
                elif args[2] == "snow":
                    sendPacket(b"\x1f\x02", False)
                else:
                    sendMessage("&cInvalid weather. Possible values:", False)
                    sendMessage("&csun, rain, snow", False)
        elif args[0] == "boost":
            X, Y, Z = msg.split()[1:4]
            xmode = ymode = zmode = b"\x01"
            if X[0] == "~":
                xmode = b"\x00"
                X = X[1:]
            if Y[0] == "~":
                ymode = b"\x00"
                Y = Y[1:]
            if Z[0] == "~":
                zmode = b"\x00"
                Z = Z[1:]
            sendPacket(b"\x2f" + struct.pack('>iii', int(X)*10000, int(Y)*10000, int(Z)*10000) + xmode+ymode+zmode, False)
        else:
            sendMessage("&cUnknown command!", False)
    except Exception as e:
            print(e)
            sendMessage("&cCould not execute the command!", False)


packets = {
    "00": h_identification,
    "08": h_posandori,
    "09": h_posandoriupdate,
    "0a": h_posupdate,
    "0b": h_oriupdate,
    "16": h_addplayername,
    "18": h_removeplayername,
    "19": h_envcolor,
    "1d": h_changemodel,
    "1f": h_weather,
    "20": h_hackcontrol,
    "22": h_playerclick,
    "29": h_mapenv,
    "2b": h_ping,
    "0d": h_message,
    "12": h_reach,
    "2f": h_velocity
}

def parse(origdata, server):
    global returndata
    returndata = origdata
    for data in origdata:
        while len(data) > 1:
            packet_id = struct.unpack('c', data[:1])[0].hex()
            found = packets.get(packet_id, False)
            if found:
                data = found(data, server)
            else:
                printPacket(packet_id, "Unknown packet, length " + str(len(data)), server)
                break
    return returndata