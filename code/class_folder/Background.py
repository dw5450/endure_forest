__author__ = 'no_game'

from pico2d import *
from class_folder.canvas_property import *

class Background:
    def __init__(self):
        self.image = load_image('image_folder//map_background.PNG')
        self.left = 0
        self.bottom = 0

    def draw(self):
        self.image.clip_draw_to_origin(self.left, self.bottom, int( backgraound_width - self.left * backgraound_width / backgraound_original_width),int( backgraound_height - self.bottom * backgraound_height / backgraound_original_height), 0, 0)
    def set_player(self, player):
        self.player = player

    def update(self, frame_time):
        #scrolling to right
        if(int(self.player.x) > canvas_width/2 and self.player.x_dir == 1 and int(self.player.x) < (backgraound_width - canvas_width)):
            self.left +=1

         #scrolling to left
        if(int(self.player.x) > canvas_width/2 and self.player.x_dir == -1 and int(self.player.x) < (backgraound_width - canvas_width)):
            self.left -=1

        #scrolling to up
        if(int(self.player.y) > canvas_height/2 and self.player.x_dir == 1 and int(self.player.y) < (backgraound_height - canvas_height)):
            self.bottom +=1

        #scrolling to down
        if(int(self.player.y) > canvas_height/2 and self.player.x_dir == -1 and int(self.player.y) < (backgraound_height - canvas_height)):
            self.bottom -=1
