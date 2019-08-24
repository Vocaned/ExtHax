import select
import socket
import subprocess
import Parser
import Launcher
from Utils import sprint, Status
debug = True
localIP = ("127.0.0.1", 25565)
tries = 0
ccPath = "/home/fam0r/Desktop/Minecraft/McClassic/ClassiCube"

if debug:
    import importlib

def proxy(username, serverIP, mppass):
    global tries, localIP
    if debug:
        sprint(Status.DEBUG, "Starting a proxy [" + ":".join([str(s) for s in localIP]) + " -> " + ":".join([str(s) for s in serverIP]) + "]")
    sockets = []
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(localIP)
    except:
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

    s_src, _ = s.accept()

    s_dst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_dst.connect(serverIP) 
    
    sockets.append(s_src)
    sockets.append(s_dst)
    while True:
        s_read, _, _ = select.select(sockets, [], [])
        
        for s in s_read:
            data = s.recv(4096)
            if data:
                if debug:
                    importlib.reload(Parser)
                if s == s_src:
                    try:
                        d = Parser.parse([b'', data], False)
                        s_src.sendall(d[0])
                        s_dst.sendall(d[1])
                    except Exception as e:
                        sprint(Status.WARN, "[C->S] " + str(e))
                        try:
                            s_dst.sendall(data)
                        except:
                            sprint(Status.ERROR, "[C->S] DROPPING A PACKET DUE TO AN ERROR")
                elif s == s_dst:
                    try:
                        d = Parser.parse([data, b''], True)
                        s_src.sendall(d[0])
                        s_dst.sendall(d[1])
                    except Exception as e:
                        sprint(Status.WARN, "[S->C] " + str(e))
                        try:
                            s_src.sendall(data)
                        except:
                            sprint(Status.ERROR, "[S->C] DROPPING A PACKET DUE TO AN ERROR")

if __name__ == '__main__':
    username = Launcher.login()
    server = Launcher.serverlist()
    proxy(username, (server["ip"], server["port"]), server['mppass'])
    #proxy("Fam0r", ("46.69.208.238", 25565), "asd")