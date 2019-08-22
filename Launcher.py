import requests
from Utils import *
import base64
s = requests.session()

rememberMe = True

loginerrors = {
    'token': 'Internal error! Please try again.',
    'username': 'Invalid username!',
    'password': 'Invalid password!',
    'verification': 'User is not verified!'
}

def get(uri):
    r = s.get(uri)
    return(r.json())
def post(uri, data=''):
    r = s.post(uri, data=data)
    return(r.json())

def login():
    if rememberMe:
        try:
            with open("session.dat", "r") as f:
                
                test = s.get('https://www.classicube.net/api/login', cookies={"session": base64.b85decode(f.read().encode()).decode()}).json()
                if test["authenticated"]:
                    return test["username"]
        except:
            pass
    print("\nClassiCube Login\n")
    print("Username: ")
    print("Password: ")
    username = input('\x1B[2A\x1B[10C\x1B[35m')
    password = getpass('\x1B[10C\x1B[0m')
    pre = get('https://www.classicube.net/api/login')
    token = pre["token"]
    reallogin = post('https://www.classicube.net/api/login', data={'username': username, 'password': password, 'token': token})
    if reallogin['errors'] or not reallogin['authenticated']:
        message = ', '.join(reallogin['errors'])
        for key in loginerrors.keys():
            message = message.replace(key, loginerrors[key])
        sprint(Status.ERROR, message)
        exit()
    username = reallogin['username']
    if rememberMe:
        with open("session.dat", "w") as f:
            f.write(base64.b85encode([c for c in s.cookies if c.name == "session"][0].value.encode()).decode())
    return username

def serverlist():
    servers = get('https://www.classicube.net/api/servers')
    servers = servers['servers']
    servers = sorted(servers, key=lambda k: k['players'], reverse=True)
    sList = []
    for i in range(len(servers)):
        col = ''
        if servers[i]['players'] > 0: col = '\x1B[92m'
        display = str(servers[i]['name']) + '\x1B[0m' + ' | ' + col + str(servers[i]['players']) + '/' + str(servers[i]['maxplayers'])
        if servers[i]['featured']:
            sList.append((str(i+1), FG.brightyellow + display))
        else:
            sList.append((str(i+1), display))
    sList = sList[::-1]
    for s in sList:
        sprint(s[0], s[1])
    sprint("0", "Logout")
    sprint(Status.INFO, 'Select the server number you want to join!')
    sel = input('> ')
    if not sel.isdigit():
        sprint(Status.ERROR, sel + ' is not a valid number!')
        return serverlist()
    sel = int(sel)
    if sel < 0 or sel > len(servers):
        sprint(Status.ERROR, 'Server number ' + str(sel) + ' does not exist!')
        return serverlist()
    sel -= 1
    if sel == -1:
        open("session.dat", "w").close()
        sprint(Status.INFO, "Logged out.")
        exit(0)
    server = servers[sel]
    return server