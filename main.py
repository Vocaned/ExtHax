import select
import socket
import subprocess
import Parser
import Launcher
import time
from config import ccPath, localIP
from Utils import sprint, Status
tries = 0

def proxy(username, serverIP, mppass):
    global tries, localIP
    sprint(Status.INFO, "Starting a proxy [" + ":".join([str(s) for s in localIP]) + " -> " + ":".join([str(s) for s in serverIP]) + "]")
    sockets = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(localIP)
    except:
        # Try binding to multiple ports in case default port is already taken
        if tries > 10:
            sprint(Status.ERROR, "Could not create a proxy.")
            exit(1)
        sprint(Status.WARN, "Error binding port, trying another...")
        tries += 1
        localIP = (localIP[0], localIP[1]+1)
        proxy(username, serverIP, mppass)
        return
    s.listen(1)

    subprocess.Popen([ccPath, username, mppass, localIP[0], str(localIP[1])], stdout=subprocess.DEVNULL)

    client, _ = s.accept()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(serverIP)

    sockets.append(client)
    sockets.append(server)
    while True:
        s_read, _, _ = select.select(sockets, [], [])
        for s in s_read:
            S2C = bool(s == server)
            s.setblocking(False)
            try:
                packetID = s.recv(1)
            except socket.error:
                continue
            s.setblocking(True)

            if not packetID:
                continue

            if S2C:
                packet = Parser.getS2CPacket(packetID)
            else:
                packet = Parser.getC2SPacket(packetID)

            if not packet:
                sprint(Status.FATAL, f'Invalid packet {packetID.hex()}.. fuck.', fullColor=True)
                exit()

            needData = packet.length-1
            data = b''

            while needData > 0:
                newData = s.recv(needData)
                data += newData
                needData -= len(newData)
            try:
                if S2C:
                    d = Parser.parse(packetID, data, True)
                else:
                    d = Parser.parse(packetID, data, False)
                if not d:
                    sprint(Status.ERROR, f'Could not parse packet {packetID}', fullColor=True)
                client.sendall(d[0])
                server.sendall(d[1])
            except SystemExit:
                exit()
            except Exception as e:
                # raise e # debug
                try:
                    if S2C:
                        sprint(Status.WARN, "[S->C] " + str(e))
                        sprint(Status.WARN, "[S->C] " + packetID.hex() + data.hex())
                        client.sendall(packetID+data)
                    else:
                        sprint(Status.WARN, "[C->S] " + str(e))
                        sprint(Status.WARN, "[C->S] " + packetID.hex() + data.hex())
                        server.sendall(packetID+data)
                except:
                    sprint(Status.FATAL, "Exception while sending packets.")
                    exit(1)

if __name__ == '__main__':
    username = Launcher.login()
    server = Launcher.serverlist()
    proxy(username, (server["ip"], server["port"]), server['mppass'])
    #proxy("asd", ('127.0.0.1', 25565), 'asd')