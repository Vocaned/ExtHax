# Might add comments at some point if I figure out how this code even works
import dearpygui.core as dpg
import dearpygui.simple as sdpg
from launcher import login_callback, serverlist_refresh_callback, serverlist_table_callback, serverlist_join_callback

import config

# region callbacks
def show_window(sender, data):
    if sender == 'LoginMenu':
        sdpg.show_item('Login Window')
    elif sender == 'ServerMenu':
        sdpg.show_item('Server Window')
#endregion

with sdpg.window('Login Window', autosize=True, no_resize=True):
    dpg.add_input_text('LoginUsername', label='Username', on_enter=True, callback=login_callback)
    dpg.add_input_text('LoginPassword', label='Password', password=True, on_enter=True, callback=login_callback)
    dpg.add_button('LoginButton', label='Login', callback=login_callback)
    dpg.add_same_line()
    dpg.add_checkbox('LoginRememberMe', label='Remember Me')
    dpg.add_label_text('LoginStatus', label='Not Logged In', show=False)

    tmpuser = config.getValue('username')
    tmppass = config.decryptValue('password')
    if tmpuser != None:
        dpg.set_value('LoginUsername', tmpuser)
    if tmppass != None:
        dpg.set_value('LoginPassword', tmppass)
    if tmpuser != None or tmppass != None:
        dpg.set_value('LoginRememberMe', value=True)

with sdpg.window('Server Window', show=False, no_scrollbar=True):
    dpg.add_button('ServerRefrestButton', label='Refresh', callback=serverlist_refresh_callback)
    dpg.add_same_line()
    dpg.add_button('ServerJoinButton', label='Join Server', callback=serverlist_join_callback)
    dpg.add_separator()
    dpg.add_table('ServerTable', ['Server Name', 'Player Count', 'Server Software'], callback=serverlist_table_callback)
    serverlist_refresh_callback(None, None)

with sdpg.window("Main Window"):
    with sdpg.menu_bar('Menu Bar'):
        with sdpg.menu('AccountMenu', label='Account'):
            dpg.add_menu_item('LoginMenu', label='Login', callback=show_window)
            dpg.add_menu_item('ServerMenu', label='Server List', callback=show_window)
        with sdpg.menu('InfoMenu', label='Info'):
            dpg.add_menu_item('LoggerMenu', label='Show Logger', callback=dpg.show_logger)
        dpg.add_menu_item('DebugMenu', label='Debug', callback=sdpg.show_debug)

    dpg.set_log_level(0)
    dpg.show_logger()

    dpg.add_text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis odio eget elit vehicula fermentum in sit amet leo. Aenean et mauris eget tellus tempor bibendum. Duis euismod, ipsum eget cursus porttitor, elit odio aliquam enim, ut lobortis tortor ligula vel ipsum. Nam pretium, dui quis scelerisque faucibus, dui massa hendrerit mauris, at suscipit enim nisl sit amet augue. Etiam eu pretium lorem, vel hendrerit purus. Aliquam est dolor, efficitur ut justo eu, dictum venenatis arcu. Nunc nec placerat risus. Curabitur vulputate nisl a metus egestas, vel sodales arcu malesuada. Sed eu mauris et sem volutpat condimentum ut sit amet arcu. Sed at lorem magna. Maecenas vitae eleifend leo. Aliquam semper efficitur ante in pharetra. Donec tempor sem lorem, in molestie lacus facilisis nec. Ut varius, risus in faucibus hendrerit, tortor nisl vulputate erat, quis facilisis ex orci eu orci. Maecenas ornare sapien eget arcu sollicitudin, vel vehicula augue condimentum.')
dpg.start_dearpygui(primary_window="Main Window")