__author__ = 'no_game'


from pico2d import *
from function_folder.canvas_property import *

class Portal:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    def __init__(self):
        self.x, self.y = 540 , 1220
        self.image = load_image('image_folder//portal.PNG')

        self.total_frames = 0
        self.frame =0

    def set_player(self, player):
        self.player = player

    def draw(self):
        if( self.x - self.player.x_scrolling < canvas_width + 50 and self.y - self.player.y_scrolling < canvas_height + 50):
            self.image.clip_draw(150 * self.frame, 0, 100, 200, self.x - self.player.x_scrolling ,self.y - self.player.y_scrolling  )

    def return_hitbox(self):
        return self.x - 50, self.y - 50, self.x +50, self.y +50


    def draw_hitbox(self):

        if( self.x - self.player.x_scrolling < canvas_width and self.y - self.player.y_scrolling < canvas_height):
            draw_rectangle(self.return_hitbox()[0] -self.player.x_scrolling, self.return_hitbox()[1] -self.player.y_scrolling,
                       self.return_hitbox()[2] -self.player.x_scrolling, self.return_hitbox()[3] -self.player.y_scrolling)

    def update(self, frame_time):

        self.total_frames += Portal.FRAMES_PER_ACTION * Portal.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 7 + 1