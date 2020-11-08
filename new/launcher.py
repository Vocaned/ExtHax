import dearpygui.core as dpg
import dearpygui.simple as sdpg
import requests
import config

#region Misc
s = requests.session()

def get(uri):
    r = s.get(uri)
    return(r.json())
def post(uri, data=''):
    r = s.post(uri, data=data)
    return(r.json())

loggedin = False
serverList = None
lastRow = None

loginerrors = {
    'token': 'Internal error! Please try again.',
    'username': 'Invalid username!',
    'password': 'Invalid password!',
    'verification': 'User is not verified! Check your email',
    'login_code': '2FA authorization required. Check your email and log in using the ClassiCube launcher'
}
#endregion

#region Async functions
def try_login(sender, data):
    pre = get('https://www.classicube.net/api/login')
    token = pre['token']
    dpg.log_debug(f'Logging in with token {token}')
    reallogin = post('https://www.classicube.net/api/login', data={'username': data[0], 'password': data[1], 'token': token})
    if reallogin['errors']:
        message = ', '.join(reallogin['errors'])
        for key in loginerrors.keys():
            message = message.replace(key, loginerrors[key])
        return 'error', message
    if not reallogin['authenticated']:
        dpg.log_error(f'Unknown login error! Login succeeded without errors but didn\'t authenticate! Contact Andrew')
        return 'error', 'Could not authenticate. Try again or something idk this shouldn\'t happen anyways'

    return 'success', reallogin['username']

def get_serverlist(sender, data):
    global serverList
    dpg.log_info('Getting server list')
    servers = get('https://www.classicube.net/api/servers')
    servers = servers['servers']
    servers = sorted(servers, key=lambda k: k['players'], reverse=True)
    tabledata = []
    for server in servers:
        tabledata.append((server['name'], f"{server['players']}/{server['maxplayers']}", server['software']))
    serverList = servers
    return tabledata

def join_server(sender, data):
    if not data:
        return
    if not 'mppass' in data:
        dpg.log_info(f"Joining server {data['name']}")
        dpg.log_error('No mppass in server list')
        return

    dpg.log_info(f"Joining server {data['name']} ({data['ip']}:{data['port']})")
    dpg.log_debug(f"mppass {data['mppass']}")
#endregion

#region Async handlers
def login_handler(sender, data):
    global loggedin
    dpg.log_debug(data)
    if data[0] == 'error':
        dpg.log_error(f'Login error: {data[1]}')
        dpg.set_item_color('LoginStatus', 0, [255, 0, 0])
        sdpg.set_item_label('LoginStatus', data[1])
    elif data[0] == 'success':
        dpg.log_info('Logged in')
        dpg.set_value('LoginUsername', data[1])
        dpg.set_item_color('LoginStatus', 0, [0, 255, 0])
        sdpg.set_item_label('LoginStatus', 'Logged In')
        loggedin = True
        if dpg.get_value('LoginRememberMe'):
            config.setValue('username', data[1])
            config.encryptValue('password', dpg.get_value('LoginPassword'))
        else:
            config.setValue('username', None)
            config.setValue('password', None)
        serverlist_refresh_callback(None, None)
        sdpg.hide_item('Login Window')
        sdpg.show_item('Server Window')
    else:
        dpg.log_error('Invalid return from login')

def serverlist_handler(sender, data):
    dpg.set_table_data('ServerTable', data)
#endregion

#region GUI callbacks
def login_callback(sender, data):
    dpg.set_item_color('LoginStatus', 0, [255, 255, 255])
    sdpg.set_item_label('LoginStatus', 'Logging In..')
    sdpg.show_item('LoginStatus')

    asyncdata = (dpg.get_value('LoginUsername'), dpg.get_value('LoginPassword'))
    dpg.run_async_function(try_login, asyncdata, return_handler=login_handler)

def serverlist_refresh_callback(sender, data):
    if not loggedin:
        dpg.set_table_data('ServerTable', [[],])
    else:
        dpg.run_async_function(get_serverlist, None, return_handler=serverlist_handler)

def serverlist_join_callback(sender, data):
    if not serverList:
        return
    selections = dpg.get_table_selections('ServerTable')
    if not selections:
        return
    row = selections[0][0]
    dpg.run_async_function(join_server, serverList[row])

def serverlist_table_callback(sender, data):
    global lastRow
    selections = dpg.get_table_selections('ServerTable')
    dpg.log_debug(selections)

    columns = 3
    rows = len(dpg.get_table_data('ServerTable'))

    for column in range(columns):
        for row in range(rows):
            dpg.set_table_selection('ServerTable', row, column, False)

    row = None
    for selection in selections:
        if selection[0] != lastRow:
            row = selection[0]

    if row == None:
        if lastRow != None:
            row = lastRow
            if serverList:
                dpg.run_async_function(join_server, serverList[row])
        else:
            row = 0
            lastRow = 0
    else:
        lastRow = row

    for column in range(columns):
        dpg.set_table_selection('ServerTable', row, column, True)
#endregion