__author__ = 'no_game'

from pico2d import *

class UI:
    forest_bgm = None
    def __init__(self):
         if UI.forest_bgm == None:
            UI.forest_bgm = load_music('sound_folder//forest_bgm.mp3')
            UI.forest_bgm.set_volume(128)
            UI.forest_bgm.repeat_play()


