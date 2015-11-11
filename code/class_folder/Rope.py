__author__ = 'no_game'


from pico2d import *

class Rope:

    BOTTOM_EDGE, NON_EDGE, TOP_EDGE = 0, 1, 2
    image = None

    def __init__(self):

        #위치 관련 변수
        self.x = 500
        self.y = 400

        #스크롤링 관련 변수
        self.player = None                                      #유저가 조종하는 플레이어

        #현제 상태 관련 변수
        self.state = self.NON_EDGE

        #이미지 관련 변수
        if(self.image == None):
            self.image = load_image('image_folder//map_object.png')

    def set_player(self, player):
        self.player = player

    def draw(self):
        self.image.clip_draw((self.state) * 100, 100, 100, 100, self.x - self.player.x_scrolling, self.y -self.player.y_scrolling)
