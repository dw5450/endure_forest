__author__ = 'no_game'

from function_folder.canvas_property import *
from pico2d import *


class Lupin:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30cm                    #픽셀의 속도를 맞추기 위해서

    TIME_PER_ACTION = 2.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    THROW_SPEED_KMPH = 20.0                    # Km / Hour
    THROW_SPEED_MPM = (THROW_SPEED_KMPH * 1000.0 / 60.0)
    THROW_SPEED_MPS = (THROW_SPEED_MPM / 60.0)
    THROW_SPEED_PPS = (THROW_SPEED_MPS * PIXEL_PER_METER)

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
        self.banana_x = self.x
        self.banana_y = self.y
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

    def return_lupin_hitbox(self):
         return self.x -40, self.y - 40, self.x + 40, self.y + 50

    def return_banana_hibox(self):
        return self.banana_x - 10, self.banana_y - 10, self.banana_x + 10, self.banana_y + 10

    def draw_lupin_hitbox(self):
        draw_rectangle(self.return_lupin_hitbox()[0] -self.player.x_scrolling, self.return_lupin_hitbox()[1] -self.player.y_scrolling,
                       self.return_lupin_hitbox()[2] -self.player.x_scrolling, self.return_lupin_hitbox()[3] -self.player.y_scrolling)

    def draw_banana_hibox(self):
        draw_rectangle(self.return_banana_hibox()[0] -self.player.x_scrolling, self.return_banana_hibox()[1] -self.player.y_scrolling,
                       self.return_banana_hibox()[2] -self.player.x_scrolling, self.return_banana_hibox()[3] -self.player.y_scrolling)

    def draw(self):
        # fill here
        if( self.x - self.player.x_scrolling < canvas_width + 50 and self.y - self.player.y_scrolling < canvas_height + 50):
            self.lupin_image.clip_draw((self.frame) * 100, self.state * 100, 100, 100,self.x - self.player.x_scrolling , self.y - self.player.y_scrolling)
        if(self.throw_banana == True  and self.banana_x - self.player.x_scrolling < canvas_width + 50 and self.banana_y - self.player.y_scrolling < canvas_height + 50):
            self.banana_image.clip_draw((self.banana_frame) * 50, self.state * 50, 40, 50, self.banana_x - self.player.x_scrolling,  self.banana_y  - self.player.y_scrolling)

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
        distance = Lupin.THROW_SPEED_PPS * frame_time

        self.banana_x += (self.throw_dir * distance)

        if(self.banana_total_frames > 7):
            self.banana_time = 0
            self.banana_frame = 0
            self.banana_total_frames = 0
            self.banana_x = self.x
            self.throw_banana = False

    def lupin_crush_optimization(self):
        if(self.player.x - 100 < self.x < self.player.x + 100 and self.player.y - 100 < self.y < self.player.y + 100 ):
            return True
        else: return False


    def banana_crush_optimization(self):
        if(self.player.x - 100 < self.banana_x < self.player.x + 100 and self.player.y - 100 < self.banana_y < self.player.y + 100 ):
            return True
        else: return False