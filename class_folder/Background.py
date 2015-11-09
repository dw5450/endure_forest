__author__ = 'no_game'

from pico2d import *

backgraound_width = 1600
backgraound_height = 1800

canvas_width = 800
canvas_height = 600

class Background:
    def __init__(self):
        self.image = load_image('image_folder//map_background.PNG')
        self.left = 0
        self.bottom = 0

    def draw(self):
        self.image.clip_draw_to_origin(self.left, self.bottom, int( backgraound_width - self.left * backgraound_width / 236),int( backgraound_height - self.bottom * backgraound_height / 270), 0, 0)

    def update(self, frame_time):
        if(int(self.center_object.x) > canvas_width/2 and self.center_object.dir == 1 and int(self.center_object.x) < (backgraound_width - canvas_width)):
            self.left +=1

        if(int(self.center_object.x) > canvas_width/2 and self.center_object.dir == -1 and int(self.center_object.x) < (backgraound_width - canvas_width)):
            self.left -=1

        if(int(self.center_object.y) > canvas_height/2 and self.center_object.dir_y == 1 and int(self.center_object.y) < (backgraound_height - canvas_height)):
            self.bottom +=1

        if(int(self.center_object.y) > canvas_height/2 and self.center_object.dir_y == -1 and int(self.center_object.y) < (backgraound_height - canvas_height)):
            self.bottom -=1
