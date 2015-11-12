__author__ = 'no_game'

from pico2d import *

from function_folder.canvas_property import *


class Boy:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30cm                    #픽셀의 속도를 맞추기 위해서
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    FALL_SPEED_KMPH = 20.0                    # Km / Hour
    FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
    FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
    FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

    JUMP_SPEED_KMPH = 40.0          # Km / Hour                       #점프는 원하는 속도 + 떨어지는 속도로 설정
    JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
    JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
    JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    JUMP_HIGHT = 60                             #점프 높이

    image = None

    LEFT_RUN, RIGHT_RUN = 0, 1
    LEFT_STAND, RIGHT_STAND = 0, 1
    LEFT_JUMP, RIGHT_JUMP = 2, 3
    LEFT_LIE, RIGHT_LIE = 4, 5

    def __init__(self):

        #위치 관련 변수
        self.x, self.y = 0, 200
        self.x_dir = 0
        self.y_dir = 0
        self.fall = False

        #스크롤링 관련 변수
        self.x_scrolling = 0;
        self.y_scrolling = 0;

        #점프 관련 변수
        self.jump_max_point =  self.y + self.JUMP_HIGHT
        self.jump = 0

        #프레임 관련 변수
        self.frame = 0
        self.total_frames = 0.0

        #현제 상태 관련 변수
        self.state = self.RIGHT_RUN

        #보이 이미지 변수
        if Boy.image == None:
            Boy.image = load_image('image_folder//character_sprite.png')

    def return_hitbox(self):
        return self.x -50, self.y -50, self.x + 50, self.y + 50

    def update(self, frame_time):
        if(self.x_dir != 0):
            self._move_x(frame_time)

        if(self.fall == True):
            self._fall(frame_time)
        if(self.jump == True):
            self._jump(frame_time)

        self._set_scrolling(frame_time)

        self._canvas_crush()

        self._set_frame(frame_time)

    def _move_x(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.x += (self.x_dir * distance)

    def _fall(self, frame_time):

        if(self.x_dir >= 0):
            self.state = self.RIGHT_JUMP
        else:
            self.state = self.LEFT_JUMP

        distance = Boy.FALL_SPEED_PPS * frame_time

        self.y_dir = -1;
        self.y -= distance

    def _set_scrolling(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        if(canvas_width /2<= self.x  and self.x < (backgraound_width - canvas_width)):
            self.x_scrolling += (self.x_dir * distance)

        if(self.y >=  canvas_height/2 and self.y < (backgraound_height - canvas_height)):
            self.y_scrolling += (self.y_dir * distance)

    def _canvas_crush(self):
        if self.x - self.x_scrolling > canvas_width:
            self.x= canvas_width + self.x_scrolling
        elif self.x < 0:
            self.x = 0

    def foothold_crush(self, foothold_hibox):
        left_boy, bottom_boy, right_boy, top_boy = self.return_hitbox()
        left_foothold, bottom_foothold, right_foothold, top_foothold = foothold_hibox

        foothold_crush = True
        if left_boy > right_foothold: foothold_crush = False
        if right_boy < left_foothold : foothold_crush = False
        if top_boy < bottom_foothold : foothold_crush = False
        if bottom_boy > top_foothold : foothold_crush = False

        if(foothold_crush == True):
            self.fall = False
            self.jump_max_point =  self.y + self.JUMP_HIGHT
            if(self.state in (self.RIGHT_JUMP, self.LEFT_JUMP)):
                if(self.x_dir >= 0):
                    self.state = self.RIGHT_STAND
                elif(self.x_dir < 0 ):
                    self.state = self.LEFT_STAND
            elif(self.x_dir > 0):
                self.state = self.RIGHT_STAND
            elif(self.x_dir < 0 ):
                self.state = self.LEFT_STAND

    def _jump(self, frame_time):

        #점프 모션 설정
        if( self.state in (self.RIGHT_STAND, self.RIGHT_RUN)):
            self.state = self.RIGHT_JUMP
        elif(self.state in (self.LEFT_STAND, self.LEFT_RUN)):
            self.state = self.LEFT_JUMP

        #점프한 높이 설정
        distance = Boy.JUMP_SPEED_PPS * frame_time
        self.y_dir = 1;
        self.y += distance

        #점프의 마지막 높이 설정
        if (self.y > self.jump_max_point):
            self.y = self.jump_max_point
            self.jump = False

    def _set_frame(self, frame_time):
        if (self.x_dir == 0 and (self.state == self.RIGHT_STAND or self.state == self.LEFT_STAND)):  #멈췃을때 이미지 스프라이트가 없어서 편법 사용
            self.total_frames = 0;
        elif (self.state == self.RIGHT_LIE or self.state == self.LEFT_LIE):
            self.total_frames = 0;
        elif (self.state == self.RIGHT_JUMP or self.state == self.LEFT_JUMP):
            self.total_frames = 0;

        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time

        self.frame = int(self.total_frames) % 4

    def draw(self):
        self.image.clip_draw((self.frame) * 100, self.state * 100, 100, 100, self.x - self.x_scrolling, self.y - self.y_scrolling)

    def draw_hitbox(self):
        draw_rectangle(self.return_hitbox()[0] -self.x_scrolling, self.return_hitbox()[1] -self.y_scrolling,
                       self.return_hitbox()[2] -self.x_scrolling, self.return_hitbox()[3] -self.y_scrolling)

    def handle_event(self, event):

        #오른쪽 이동, 멈춤
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state != self.LEFT_LIE and self.state != self.RIGHT_LIE:
                self._handle_right_run()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN, self.RIGHT_JUMP):
                self._handle_right_stand()

        #왼쪽 이동, 멈춤
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state != self.LEFT_LIE and self.state != self.RIGHT_LIE:
                self._handle_left_run()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,self.LEFT_JUMP):
                self._handle_left_stand()

        #점프
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LALT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN):
                self._handle_jump()

        #엎드리기/일어나기
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN):
                self._handle_lie()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.RIGHT_LIE, self.LEFT_LIE):
                self._handle_rise()

    def _handle_right_run(self):
        self.x_dir = 1;
        self.state = self.RIGHT_RUN

    def _handle_right_stand(self):
        self.x_dir = 0;
        self.state = self.RIGHT_STAND

    def _handle_left_run(self):
        self.x_dir = -1;
        self.state = self.LEFT_RUN

    def _handle_left_stand(self):
        self.x_dir = 0;
        self.state = self.LEFT_STAND

    def _handle_jump(self):
        self.jump = True

    def _handle_lie(self):
        if(self.state == self.RIGHT_RUN or self.state == self.RIGHT_STAND):
            self.state = self.RIGHT_LIE

        elif(self.state == self.LEFT_RUN or self.state == self.LEFT_STAND):
            self.state = self.LEFT_LIE

        self.x_dir = 0

    def _handle_rise(self):
        if (self.state == self.RIGHT_LIE):
            self.state = self.RIGHT_STAND

        elif (self.state == self.LEFT_LIE):
            self.state = self.LEFT_STAND



