__author__ = 'no_game'

from pico2d import *
from function_folder.canvas_property import *

class Foothold:

    EDGE, NON_EDGE = 0, 1
    image = None

    def __init__(self):

        #위치 관련 변수
        self.x = 200
        self.y = 400

        #스크롤링 관련 변수
        self.player = None                                      #유저가 조종하는 플레이어

        #현제 상태 관련 변수
        self.state = self.EDGE

        #이미지 관련 변수
        if(self.image == None):
            self.image = load_image('image_folder//map_object.png')

    def set_player(self, player):
        self.player = player

    def return_hitbox(self):
        return self.x -50, self.y , self.x + 50, self.y + 20

    def draw(self):
        if( self.x - self.player.x_scrolling < canvas_width + 50 and self.y - self.player.y_scrolling < canvas_height + 50):
            self.image.clip_draw((self.state) * 100, 0, 100, 100, self.x - self.player.x_scrolling, self.y -self.player.y_scrolling)

    def draw_hitbox(self):
        if( self.x - self.player.x_scrolling < canvas_width + 50 and self.y - self.player.y_scrolling < canvas_height + 50):
            draw_rectangle(self.return_hitbox()[0] -self.player.x_scrolling, self.return_hitbox()[1] -self.player.y_scrolling,
                       self.return_hitbox()[2] -self.player.x_scrolling, self.return_hitbox()[3] -self.player.y_scrolling)

    #def optimization(self):
