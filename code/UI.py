__author__ = 'no_game'

from pico2d import *

class UI:

    def __init__(self):

        self.forest_bgm = load_music('sound_folder//forest_bgm.mp3')
        self.forest_bgm.set_volume(64)
        self.forest_bgm.repeat_play()


    def draw(self):
        draw_rectangle(0, 0, 1, 1)