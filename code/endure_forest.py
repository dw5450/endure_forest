__author__ = 'no_game'

import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86/"
elif platform.architecture()[0] == '64bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

# fill here

import game_framework
import title_state

game_framework.run(title_state)
