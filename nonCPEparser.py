import math
import struct
accuratePos = True
noSpam = False

def h_noop(data):
    return

def h_position(data):
    if noSpam:
        return data[10:]
    entity_id = struct.unpack('B', data[1:2])[0]
    X,Y,Z = struct.unpack('>hhh', data[2:2+3*2])
    X /= 32
    Y /= 32
    Y -= 1.59375
    Z /= 32
    yaw,pitch = struct.unpack('BB', data[8:10])
    yaw *= 1.41176470588
    pitch *= 1.41176470588
    if accuratePos:
        print(f'[ID/X/Y/Z/YAW/PITCH] {str(entity_id)} / {X} / {Y} / {Z} / {yaw} / {pitch}')
    else:
        None
        #print(f'[ID/X/Y/Z/YAW/PITCH] {entity_id} / {math.floor(X)} / {math.floor(Y)} / {math.floor(Z)} / {math.floor(yaw)} / {math.floor(pitch)}')
    #print('Returning ' + str(len(data[10:])))
    return data[10:]

def h_OriUpdate(data):
    if noSpam:
        return data[4:]
    entity_id = struct.unpack('B', data[1:2])[0]
    yaw,pitch = struct.unpack('BB', data[2:4])
    yaw *= 1.41176470588
    pitch *= 1.41176470588
    if accuratePos:
        print(f'[YAW/PITCH] [CHANGE] {entity_id} / {yaw} / {pitch}')
    else:
        print(f'[YAW/PITCH] [CHANGE] {entity_id} / {math.floor(yaw)} / {math.floor(pitch)}')
    return data[4:]

def h_posOriUpdate(data):
    if noSpam:
        return data[7:]
    entity_id = struct.unpack('B', data[1:2])[0]
    X,Y,Z = struct.unpack('bbb', data[2:2+3])
    X /= 32
    Y /= 32
    Y -= 1.59375
    Z /= 32
    yaw,pitch = struct.unpack('BB', data[5:7])
    yaw *= 1.41176470588
    pitch *= 1.41176470588
    if accuratePos:
        print(f'[ID/X/Y/Z/YAW/PITCH] [CHANGE] {entity_id} / {X} / {Y} / {Z} / {yaw} / {pitch}')
    else:
        print(f'[ID/X/Y/Z/YAW/PITCH] [CHANGE] {entity_id} / {math.floor(X)} / {math.floor(Y)} / {math.floor(Z)} / {math.floor(yaw)} / {math.floor(pitch)}')
    return data[7:]

def h_positionUpdate(data):
    if noSpam:
        return data[5:]
    entity_id = struct.unpack('b', data[1:2])[0]
    X,Y,Z = struct.unpack('bbb', data[2:5])
    X /= 32
    Y /= 32
    Y -= 1.59375
    Z /= 32
    if accuratePos:
        print(f'[ID/X/Y/Z] [CHANGE] {entity_id} / {X} / {Y} / {Z}')
    else:
        print(f'[ID/X/Y/Z] [CHANGE] {entity_id} / {math.floor(X)} / {math.floor(Y)} / {math.floor(Z)}')
    return data[5:]

def h_ping(data):
    if noSpam:
        return data[1:]
    print('Ping')
    return data[1:]

def h_spawn(data):
    if noSpam:
        return data[1:]
    print(data)
    return data[1:]

def h_receiveblock(data):
    #print(f'Data {data.hex()}')
    X,Y,Z = struct.unpack('>hhh', data[1:1+3*2])
    block = struct.unpack('B', data[7:8])[0]
    print(f'[MODIFIED] [X/Y/Z/BLOCKID] {X} / {Y} / {Z} / {block}')
    return data[8:]

def h_setblock(data):
    #print(f'Data {data.hex()}')
    X,Y,Z = struct.unpack('>hhh', data[1:1+3*2])
    mode,block = struct.unpack('BB', data[7:9])
    if mode == 0:
        print(f'[BREAK] [X/Y/Z/BLOCKID] {X} / {Y} / {Z} / {block}')
    else: 
        print(f'[PLACE] [X/Y/Z/BLOCKID] {X} / {Y} / {Z} / {block}')
    return data[9:]

def h_sendmessage(data):
    message = "".join(map(chr, data[2:65]))
    print(f'Sent message {message}')
    return data[66:]

def h_receivemessage(data):
    playerID = struct.unpack('b', data[1:2])[0]
    message = "".join(map(chr, data[2:65]))
    print(f'From PlayerID {playerID}, received message {message}')
    return data[66:]

def h_despawn(data):
    playerID = struct.unpack('B', data[1:2])[0]
    print(f'Despawning entity id {playerID}')
    return data[2:]

def h_initlevel(data):
    print('Loading new level')
    return data[1:]

def h_identify(data):
    print('Server ID')
    return

c2s_handlers = {
    b'\x08': h_position,
    b'\x05': h_setblock,
    b'\x0d': h_sendmessage
}

s2c_handlers = {
        b'\x0d': h_receivemessage,
        b'\x0c': h_despawn,
        b'\x06': h_receiveblock,
        b'\x02': h_initlevel,
        b'\x00': h_identify,

        b'\x0a': h_positionUpdate,
        b'\x09': h_posOriUpdate,
        b'\x0b': h_OriUpdate,
        b'\x08': h_position,
        b'\x01': h_ping,
        #level change
        b'\x03': h_noop
}

def parse(src_port, dest_port, data):
    if dest_port == 25565:
        while data != None and len(data) > 0:
            packet_id = struct.unpack('c', data[:1])[0]
            if packet_id not in c2s_handlers:
                print (f'Unknown packet id {packet_id.hex()} ({data.hex()})')
            data = c2s_handlers.get(packet_id, h_noop)(data)
    else:
        while data != None and len(data) > 0:
            packet_id = struct.unpack('c', data[:1])[0]
            if packet_id not in s2c_handlers:
                print (f'Unknown packet id {packet_id.hex()} ({data.hex()})')
            data = s2c_handlers.get(packet_id, h_noop)(data)