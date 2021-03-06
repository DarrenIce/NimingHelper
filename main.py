from users import Users
import yaml
import sys
import os
import platform

from rich.live import Live

from display import DisplayLayout

if sys.platform == 'win32':
    import keyboard
    keyboard.add_hotkey('ctrl+alt+z', os._exit, args=[0])

conf = None
with open('config.yml' ,'r', encoding='utf-8') as f:
    conf = yaml.safe_load(f)

users = Users(conf)
# with Live(DisplayLayout.my_layout, refresh_per_second=1):
users.login()
users.run()