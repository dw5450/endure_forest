__author__ = 'no_game'

from pico2d import *
from class_folder.canvas_property import *


class Lupin:

    TIME_PER_ACTION = 2.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self):
        self.image = load_image('image_folder//lupin.png')
        self.banana_image = load_image('image_folder//banana.png')
        self.total_frames = 0.0
        self.frame = 0

        self.throw_banana = False
        self.banana_time = 0
        self.banana_total_frames = 0.0
        self.banana_frame = 0

        self.x = 400
        self.y = 200

    def draw(self):
        # fill here
        global com_x, com_y
        self.image.clip_draw((self.frame) * 100, 100, 100, 100,self.x , self.y )
        if(self.throw_banana == True):
            self.banana_image.clip_draw((self.banana_frame) * 50, 50, 40, 50, self.x + 30 * int(self.banana_total_frames), self.y )

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        if(self.frame == 6):
            self.throw_banana = True

        if(self.throw_banana == True):
            self.banana_total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * self.banana_time
            self.banana_frame = int(self.banana_total_frames) % 4
            self.banana_time = 0.04

            if(self.banana_total_frames > 7):
                self.banana_time = 0
                self.banana_frame = 0
                self.banana_total_frames = 0
                self.throw_banana = False