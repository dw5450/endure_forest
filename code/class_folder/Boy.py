__author__ = 'no_game'

from pico2d import *

from function_folder.canvas_property import *


class Boy:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    JUMP_HIGHT = 40                         #점프 높이

    image = None

    LEFT_RUN, RIGHT_RUN = 0, 1
    LEFT_STAND, RIGHT_STAND = 0, 1
    LEFT_JUMP, RIGHT_JUMP = 2, 3
    LEFT_LIE, RIGHT_LIE = 4, 5

    def __init__(self):

        #위치 관련 변수
        self.x, self.y = 0, 90
        self.x_dir = 0
        self.y_dir = 0

        #스크롤링 관련 변수
        self.x_scrolling = 0;
        self.y_scrolling = 0;

        #프레임 관련 변수
        self.frame = 0
        self.total_frames = 0.0

        #현제 상태 관련 변수
        self.state = self.RIGHT_RUN

        #점프 관련 변수
        self.jump_max_point =  self.y + self.JUMP_HIGHT
        self.jump_dir = 0
        self.jump_prev_y = self.y
        self.jump_prev_state = None

        #보이 이미지 변수
        if Boy.image == None:
            Boy.image = load_image('image_folder//character_sprite.png')

    def update(self, frame_time):
        self._set_pos(frame_time)
        self._set_scrolling(frame_time)
        if(self.jump_dir != 0):
            self._jump()

        self._canvas_crush()

        self._set_frame(frame_time)

    def _set_pos(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time

        self.x += (self.x_dir * distance)
        self.y += (self.y_dir * distance)

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

    def _jump(self):

        if(self.x_dir > 0 or self.state == self.RIGHT_STAND):
            self.state = self.RIGHT_JUMP
        elif(self.x_dir < 0 or self.state == self.LEFT_STAND):
            self.state = self.LEFT_JUMP

        if (self.jump_dir > 0 and self.y > self.jump_max_point):
            self.jump_dir = -1
            self.y = self.jump_max_point

        elif self.jump_dir < 0 and self.y < self.jump_prev_y:                                                                           #추후에 충돌체크로 바꿔야함
            self.jump_dir = 0
            self.y = 90
            self.state = self.jump_prev_state
            if(self.x_dir > 0):
                self.state = self.RIGHT_STAND
            elif(self.x_dir < 0):
                self.state = self.LEFT_STAND

        self.y_dir = self.jump_dir

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
        self.jump_prev_y = self.y
        self.jump_prev_state = self.state

        if(self.state == self.RIGHT_RUN or self.state == self.RIGHT_STAND):
            self.state= self.RIGHT_JUMP
        elif(self.state == self.LEFT_RUN or self.state == self.LEFT_STAND):
            self.state= self.LEFT_JUMP

        self.jump_dir = 1

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


