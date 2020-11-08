# Sorry I wrote all of this at 4 AM, I really don't know how this library even works
# Might add comments at some point if I figure out how this code even works


import dearpygui.core as dpg
import dearpygui.simple as sdpg

import requests
import base64

s = requests.session()

def get(uri):
    r = s.get(uri)
    return(r.json())
def post(uri, data=''):
    r = s.post(uri, data=data)
    return(r.json())

loggedin = False
serverList = None

loginerrors = {
    'token': 'Internal error! Please try again.',
    'username': 'Invalid username!',
    'password': 'Invalid password!',
    'verification': 'User is not verified! Check your email',
    'login_code': '2FA authorization required. Check your email and log in using the ClassiCube launcher'
}

def try_login(sender, data):
    pre = get('https://www.classicube.net/api/login')
    token = pre['token']
    dpg.log_debug(f'Logging in with token {token}')
    reallogin = post('https://www.classicube.net/api/login', data={'username': dpg.get_value('LoginUsername'), 'password': dpg.get_value('LoginPassword'), 'token': token})
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
    dpg.log_debug('Getting server list')
    servers = get('https://www.classicube.net/api/servers')
    servers = servers['servers']
    servers = sorted(servers, key=lambda k: k['players'], reverse=True)
    tabledata = []
    for server in servers:
        tabledata.append((server['name'], f"{server['players']}/{server['maxplayers']}", server['software']))
    serverList = servers
    return tabledata

def join_server(sender, data):
    if not 'mppass' in data:
        dpg.log_info(f"Joining server {data['name']}")
        dpg.log_error('No mppass in server list')
        return

    dpg.log_info(f"Joining server {data['name']} ({data['ip']}:{data['port']})")
    dpg.log_debug(f"mppass {data['mppass']}")

def login_handler(sender, data):
    global loggedin
    dpg.log_debug(sender)
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
        serverlist_refresh_callback(None, None)
        sdpg.hide_item('Login Window')
        sdpg.show_item('Server Window')
    else:
        dpg.log_error('Invalid return from login')

def serverlist_handler(sender, data):
    dpg.set_table_data('ServerTable', data)

def login_callback(sender, data):
    dpg.set_item_color('LoginStatus', 0, [255, 255, 255])
    sdpg.set_item_label('LoginStatus', 'Logging In..')
    sdpg.show_item('LoginStatus')
    dpg.run_async_function(try_login, None, return_handler=login_handler)

def serverlist_refresh_callback(sender, data):
    if not loggedin:
        dpg.set_table_data('ServerTable', [['NOT LOGGED IN', 'NOT LOGGED IN', 'NOT LOGGED IN'],])
    else:
        dpg.run_async_function(get_serverlist, None, return_handler=serverlist_handler)

def serverlist_join_callback(sender, data):
    selections = dpg.get_table_selections('ServerTable')
    if not selections:
        return
    row = selections[0][0]
    dpg.run_async_function(join_server, serverList[row])

lastRow = None
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
        if lastRow:
            row = lastRow
            dpg.run_async_function(join_server, serverList[row])
        else:
            row = 0
            lastRow = 0
    else:
        lastRow = row

    for column in range(columns):
        dpg.set_table_selection('ServerTable', row, column, True)

def show_window(sender, data):
    if sender == 'LoginMenu':
        sdpg.show_item('Login Window')
    elif sender == 'ServerMenu':
        sdpg.show_item('Server Window')

with sdpg.window('Login Window', autosize=True, no_resize=True):
    dpg.add_input_text('LoginUsername', label='Username', on_enter=True, callback=login_callback)
    dpg.add_input_text('LoginPassword', label='Password', password=True, on_enter=True, callback=login_callback)
    dpg.add_button('LoginButton', label='Login', callback=login_callback)
    dpg.add_label_text('LoginStatus', label='Not Logged In', show=False)

with sdpg.window('Server Window', show=False, no_scrollbar=True):
    dpg.add_button('ServerRefrestButton', label='Refresh', callback=serverlist_refresh_callback)
    dpg.add_button('ServerJoinButton', label='Join Server', callback=serverlist_join_callback)
    dpg.add_table('ServerTable', ['Server Name', 'Player Count', 'Server Software'], callback=serverlist_table_callback)
    serverlist_refresh_callback(None, None)

with sdpg.window("Main Window"):
    with sdpg.menu_bar('Menu Bar'):
        with sdpg.menu('Account'):
            dpg.add_menu_item('LoginMenu', label='Login', callback=show_window)
            dpg.add_menu_item('ServerMenu', label='Server List', callback=show_window)
        with sdpg.menu('Info'):
            dpg.add_menu_item('LoggerMenu', label='Show Logger', callback=dpg.show_logger)

    dpg.set_log_level(0)
    dpg.show_logger()

    #sdpg.show_documentation()
    #sdpg.show_debug()

    dpg.add_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis odio eget elit vehicula fermentum in sit amet leo. Aenean et mauris eget tellus tempor bibendum. Duis euismod, ipsum eget cursus porttitor, elit odio aliquam enim, ut lobortis tortor ligula vel ipsum. Nam pretium, dui quis scelerisque faucibus, dui massa hendrerit mauris, at suscipit enim nisl sit amet augue. Etiam eu pretium lorem, vel hendrerit purus. Aliquam est dolor, efficitur ut justo eu, dictum venenatis arcu. Nunc nec placerat risus. Curabitur vulputate nisl a metus egestas, vel sodales arcu malesuada. Sed eu mauris et sem volutpat condimentum ut sit amet arcu. Sed at lorem magna. Maecenas vitae eleifend leo. Aliquam semper efficitur ante in pharetra. Donec tempor sem lorem, in molestie lacus facilisis nec. Ut varius, risus in faucibus hendrerit, tortor nisl vulputate erat, quis facilisis ex orci eu orci. Maecenas ornare sapien eget arcu sollicitudin, vel vehicula augue condimentum.')
dpg.start_dearpygui(primary_window="Main Window")