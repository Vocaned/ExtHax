import math
import struct
accuratePos = False
noSpam = True
showUnknown = True

def printInfo(server, packet, *data):
    if noSpam and packet in spam_handlers:
        return
    if not showUnknown and packet == '???':
        return
    if server:
        print(f'[S->C] [{packet}] {", ".join(str(x) for x in data)}')
    else:
        print(f'[C->S] [{packet}] {", ".join(str(x) for x in data)}')
    

def h_noop(data, server):
    return

def h_padding(data, server):
    return data[1:]

def h_position(data, server):
    blockID = struct.unpack('B', data[:1])[0]
    X,Y,Z = struct.unpack('>lll', data[1:13])
    X /= 32
    Y /= 32
    Y -= 1.59375
    Z /= 32
    yaw,pitch = struct.unpack('BB', data[13:15])
    yaw *= 1.41176470588
    pitch *= 1.41176470588
    if accuratePos:
        printInfo(server,'Position', 'Held block ID', blockID,'X, Y, Z', X, Y, Z, 'Yaw, Pitch', yaw, pitch)
    else:
        printInfo(server,'Position', 'Held block ID', blockID, 'X, Y, Z', math.floor(X), math.floor(Y), math.floor(Z), 'Yaw, Pitch', math.floor(yaw), math.floor(pitch))
    return data[15:]

def h_twowayping(data, server):
    direction,count = struct.unpack('>bh', data[:3])
    printInfo(server,'TwoWayPing', direction, count)
    return data[3:]

def h_message(data, server):
    #PlayerID not used that much anymore, so I wont bother with it
    #playerID = struct.unpack('b', data[0:1])[0]
    print(server)
    message = "".join(map(chr, data[1:65]))
    if not server and message.startswith('.'):
        message = message[1:]
        print('[$] Command: ' + message)
        return data[65:]

    for key in colors.keys():
        message = message.replace(key, colors[key])
    l = list(message)
    while '&' in l:
        l[l.index('&'):l.index('&')+2] = '\x1B[0m'
    message = ''.join(l)

    printInfo(server, 'Message', str(message).strip() + '\x1B[0m')
    return data[65:]

def h_playerclicked(data, server):
    button, action = struct.unpack('bb', data[:2])
    yaw, pitch = struct.unpack('HH', data[2:6])
    targetentityid = struct.unpack('b', data[6:7])[0]
    targetX, targetY, targetZ = struct.unpack('>hhh', data[7:13])
    targetBlockFace = struct.unpack('b', data[13:14])[0]
    printInfo(server, 'PlayerClicked', button, action, yaw, pitch, targetentityid, targetX, targetY, targetZ, targetBlockFace)
    return data[14:]

def h_setblock(data, server):
    X,Y,Z = struct.unpack('>hhh', data[0:6])
    block = struct.unpack('b', data[6:7])[0]
    printInfo(server, 'SetBlock', 'Block', block, 'XYZ', X, Y, Z)
    return data[7:]

colors = {
    '&0': '\x1B[30m',
    '&4': '\x1B[31m',
    '&2': '\x1B[32m',
    '&6': '\x1B[33m',
    '&1': '\x1B[34m',
    '&5': '\x1B[35m',
    '&3': '\x1B[36m',
    '&7': '\x1B[37m',
    '&8': '\x1B[90m',
    '&c': '\x1B[91m',
    '&a': '\x1B[92m',
    '&e': '\x1B[93m',
    '&9': '\x1B[94m',
    '&d': '\x1B[95m',
    '&b': '\x1B[96m',
    '&f': '\x1B[97m',
}

spam_handlers = {
    'Position',
    'TwoWayPing'
}

s2c_handlers = {
     #b'\x00': h_padding,
     b'\x08': h_position,
     b'\x2b': h_twowayping,
     b'\x0d': h_message,
     b'\x0a': h_noop,
     b'\x0b': h_noop,
     b'\x09': h_noop,
     b'\x06': h_setblock,
     b'\x26': h_noop
}

c2s_handlers = {
     #b'\x00': h_padding,
     b'\x08': h_position,
     b'\x2b': h_twowayping,
     b'\x0d': h_message,
     b'\x22': h_playerclicked
}

def parse(src_port, dest_port, data):
    if dest_port == 25565:
        while data != None and len(data) > 0:
            packet_id = struct.unpack('c', data[0:1])[0]
            if packet_id not in c2s_handlers:
                printInfo(False, '???', data.hex())
            data = c2s_handlers.get(packet_id, h_noop)(data[1:],False)
    else:
        while data != None and len(data) > 0:
            packet_id = struct.unpack('c', data[0:1])[0]
            if packet_id not in s2c_handlers:
                printInfo(True, '???', data.hex())
            data = s2c_handlers.get(packet_id, h_noop)(data[1:],True)
