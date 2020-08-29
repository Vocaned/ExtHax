import requests
import base64
from getpass import getpass
from config import rememberMe
s = requests.session()

loginerrors = {
    'token': 'Internal error! Please try again.',
    'username': 'Invalid username!',
    'password': 'Invalid password!',
    'verification': 'User is not verified! Check your email',
    'login_code': '2FA authorization required. Check your email and log in using the ClassiCube launcher'
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
            with open('session.dat', 'r') as f:
                test = s.get('https://www.classicube.net/api/login', cookies={'session': base64.b85decode(f.read().encode()).decode()}).json()
                if test['authenticated']:
                    return test['username']
        except:
            pass
    print('\nClassiCube Login\n')
    print('Username: ')
    print('Password: ')
    username = input('\x1B[2A\x1B[10C\x1B[35m')
    password = getpass('\x1B[10C\x1B[0m')
    pre = get('https://www.classicube.net/api/login')
    token = pre['token']
    reallogin = post('https://www.classicube.net/api/login', data={'username': username, 'password': password, 'token': token})
    if reallogin['errors']:
        message = ', '.join(reallogin['errors'])
        for key in loginerrors.keys():
            message = message.replace(key, loginerrors[key])
        print('\x1B[31m[ERROR] \x1B[0m' + message)
        exit()

    if not reallogin['authenticated']:
        print('\x1B[31m[ERROR] \x1B[0mCould not authenticate. Try again or something idk this shouldn\'t happen anyways')
        exit()

    username = reallogin['username']
    if rememberMe:
        with open('session.dat', 'w') as f:
            f.write(base64.b85encode([c for c in s.cookies if c.name == 'session'][0].value.encode()).decode())
    return username

def serverlist():
    servers = get('https://www.classicube.net/api/servers')
    servers = servers['servers']
    servers = sorted(servers, key=lambda k: k['players'], reverse=True)
    sList = []
    for i in range(len(servers)):
        col = ''
        if servers[i]['players'] > 0: col = '\x1B[92m'
        display = f"{servers[i]['name']}\x1B[0m | {col}{servers[i]['players']}/{servers[i]['maxplayers']}\x1B[0m"
        if servers[i]['featured']:
            sList.append((str(i+1), f'\x1B[93m{display}'))
        else:
            sList.append((str(i+1), display))
    sList = sList[::-1]
    for s in sList:
        print(f'[{s[0]}] {s[1]}')
    print('[0] Logout')
    print('Select the server number you want to join')
    sel = input('> ')
    if not sel.isdigit():
        print('\x1B[31m[ERROR] \x1B[0m is not a valid number')
        return serverlist()
    sel = int(sel)
    if sel < 0 or sel > len(servers):
        print(f'\x1B[31m[ERROR] \x1B[0m Server number {sel} does not exist')
        return serverlist()
    sel -= 1
    if sel == -1:
        open('session.dat', 'w').close()
        print('Logged out.')
        exit(0)
    server = servers[sel]
    return server