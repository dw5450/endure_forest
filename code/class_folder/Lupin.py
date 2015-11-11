__author__ = 'no_game'

from pico2d import *


class Lupin:

    TIME_PER_ACTION = 2.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    lupin_image = None
    banana_image = None

    RIGHT_THROW, LEFT_THROW = 1, 0
    def __init__(self):

        #위치 관련 변수
        self.x = 400
        self.y = 200

        #스크롤링 관련 변수
        self.player = None                                      #유저가 조종하는 플레이어

        #현제 상태 관련 변수
        self.state = self.LEFT_THROW

        #루팡 프레임 관련 변수
        self.total_frames = 0.0
        self.frame = 0
        self.banana_total_frames = 0.0
        self.banana_frame = 0

        #바나나 관련 변수
        self.banana_total_frames = 0.0
        self.banana_frame = 0
        self.throw_dir = None

        #이미지 관련 변수
        if(self.lupin_image == None):
            self.lupin_image = load_image('image_folder//lupin.png')

        self.throw_banana = False
        if(self.banana_image == None):
            self.banana_image = load_image('image_folder//banana.png')

    def set_player(self, player):
        self.player = player

    def draw(self):
        # fill here
        self.lupin_image.clip_draw((self.frame) * 100, self.state * 100, 100, 100,self.x - self.player.x_scrolling , self.y - self.player.y_scrolling)
        if(self.throw_banana == True):
            self.banana_image.clip_draw((self.banana_frame) * 50, self.state * 50, 40, 50, self.x + 30 * self.throw_dir * (self.banana_total_frames) - self.player.x_scrolling, self.y - self.player.y_scrolling)

    def update(self, frame_time):
        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        if(self.frame == 6):
            self.throw_banana = True

        if(self.throw_banana == True):
            self._throw_banana(frame_time)


    def _throw_banana(self, frame_time):
        self.throw_banana = True

        if(self.state == self.LEFT_THROW):
            self.throw_dir = -1
        elif (self.state == self.RIGHT_THROW):
            self.throw_dir = 1
        self.banana_total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.banana_frame = int(self.banana_total_frames) % 4

        if(self.banana_total_frames > 7):
            self.banana_time = 0
            self.banana_frame = 0
            self.banana_total_frames = 0
            self.throw_banana = False
