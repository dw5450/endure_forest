__author__ = 'no_game'

from pico2d import *

from canvas_property import *


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

    JUMP_HIGHT = 60                             #점프 높이
    JUMP_SPEED_KMPH = 40.0          # Km / Hour                       #점프는 원하는 속도 + 떨어지는 속도로 설정
    JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
    JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
    JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

    PUSHED_MAX_METER = 80                                          #팅겨지기 원하는 거리
    PUSHED_SPEED_KMPH = 20       # Km / Hour                       #팅겨지기 원하는 속도
    PUSHED_SPEED_MPM = (PUSHED_SPEED_KMPH * 1000.0 / 60.0)
    PUSHED_SPEED_MPS = (PUSHED_SPEED_MPM / 60.0)
    PUSHED_SPEED_PPS = (PUSHED_SPEED_MPS * PIXEL_PER_METER)

    INVINCIVLE_TIME_MAX = 1

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    image = None
    bgm = None
    run_sound = None
    jump_sound = None
    pushed_sound = None

    LEFT_RUN, RIGHT_RUN = 0, 1
    LEFT_STAND, RIGHT_STAND = 0, 1
    LEFT_JUMP, RIGHT_JUMP = 2, 3
    LEFT_LIE, RIGHT_LIE = 4, 5
    HANG = 6

    SOUND_NONE_PLAY = 21
    SOUND_PAUSE = 22
    SOUND_PLAY= 23

    def __init__(self):

        #위치 관련 변수
        self.x, self.y = 0, 200
        self.x_dir = 0
        self.y_dir = 0
        self.fall = False
        if(Boy.run_sound == None):
            Boy.run_sound = load_wav('sound_folder//stonewalk_01.wav')
            Boy.run_sound.set_volume(128)
            Boy.run_sound_cnt = 0

        #방해물 충돌 관련 변수
        self.pushed = False
        self.pushed_meter = 0
        self.cur_pushed_meter = 0
        self.pushed_dir = 0

        # 매달리기 관련 변수
        self.rope_x_pos = 0
        self.rope_y_end_pos = 0
        self.stand_hang = False
        self.hang = False
        self.can_hang = False
        self.hang_y_dir = 0
        self.hang_x_dir = 0

        if(Boy.pushed_sound == None):
            Boy.pushed_sound = load_wav('sound_folder//gourd_hit_01.wav')
            Boy.pushed_sound.set_volume(64)

        #무적 관련 함수
        self.invincible = False
        self.invincible_sprite = 0
        self.invincible_time = 0

        #스크롤링 관련 변수
        self.x_scrolling = 0
        self.y_scrolling = 0

        #점프 관련 변수
        self.cur_jumped_meter = 0
        self.jump = 0
        self.jump_sound_state = Boy.SOUND_NONE_PLAY
        if Boy.jump_sound == None:
            Boy.jump_sound = load_wav('sound_folder//walk_floor_01.wav')
            Boy.jump_sound.set_volume(64)


        #프레임 관련 변수
        self.frame = 0
        self.total_frames = 0.0

        #현제 상태 관련 변수
        self.state = self.RIGHT_RUN

        #보이 이미지 변수
        if Boy.image == None:
            Boy.image = load_image('image_folder//character_sprite.png')


        #포탈 관련 변수
            self.stand_cross_portal = False
            self.can_cross_portal = False

    def return_hitbox(self):
        if(self.state in (self.LEFT_LIE, self.RIGHT_LIE)):
            return self.x - 30, self.y -30, self.x + 30, self.y
        else:
            return self.x - 20, self.y -30, self.x + 20, self.y + 30

    #업데이트
    def update(self, frame_time):
        if(self.pushed == True):
            self._pushed(frame_time)

        elif(self.x_dir != 0):
            self._move_x(frame_time)

        if(self.invincible == True ):
            self._invincible(frame_time)

        if(self.stand_hang == True ):
            self._hang(frame_time)

        if(self.jump == True):
            self._jump(frame_time)

        elif(self.fall == True):
            self._fall(frame_time)

        self._set_scrolling(frame_time)

        self._canvas_crush()

        self._set_frame(frame_time)

        if(self.y < 90):
            self.y = 90

    def _pushed(self, frame_time):
        distance = Boy.PUSHED_SPEED_PPS * frame_time
        self.cur_pushed_meter += distance
        self.invincible_sprite = 400

        #밀어낼려는 미터보다 크거나 같은 경우
        if(self.cur_pushed_meter >= self.PUSHED_MAX_METER):
            self.pushed = False
            self.pushed_meter = 0
            self.cur_pushed_meter = 0
            self.invincible = True
            distance -= self.cur_pushed_meter - self.pushed_meter

        self.x += self.pushed_dir * distance

    def _move_x(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.x += (self.x_dir * distance)
        if(self.state == self.LEFT_RUN and self.x_dir == 1):
            self.state = self.RIGHT_RUN
        elif (self.state == self.RIGHT_RUN and self.x_dir == -1):
            self.state = self.LEFT_RUN

    def _invincible(self, frame_time):
        self.invincible_time +=frame_time;
        self.invincible_sprite = 400

        if self.invincible_time > self.INVINCIVLE_TIME_MAX:
            self.invincible = False
            self.invincible_time = 0
            self.invincible_sprite = 0

    def _fall(self, frame_time):

        distance = Boy.FALL_SPEED_PPS * frame_time

        self.y_dir = -1;
        self.y -= distance

        if(self.state in (self.LEFT_STAND, self.LEFT_RUN)):
            self.state = self.LEFT_JUMP
        elif(self.state in(self.RIGHT_STAND, self.RIGHT_RUN)):
            self.state = self.RIGHT_JUMP

    def _hang(self, frame_time):
         #매달리기 상태에서 밀어내긱 일어날 경우
        if self.pushed == True:
            self.can_hang = False
            if(self.pushed_dir < 0):
                 self.state = self.RIGHT_JUMP
            elif (self.pushed_dir > 0):
                self.state = self.LEFT_JUMP

        elif(self.can_hang == True ):
            self.fall = False
            self.x = self.rope_x_pos

            #만약 이동중 매달리기 상태로 변했을 경우
            if(self.x_dir != 0):
                self.hang_x_dir = self.x_dir

            #나머지 상태
            else:
                self.x_dir = 0
                self.state = self.HANG
                self.hang = True
                distance = Boy.RUN_SPEED_PPS * frame_time
                self.y += self.hang_y_dir * distance

        if(self.hang == True and self.can_hang == False):
            self.x_dir = self.hang_x_dir
            self.hang = False
            self.stand_hang = False

    def _set_scrolling(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time

        if(canvas_width /2<= self.x  and self.x < (backgraound_width - canvas_width)):
            self.x_scrolling = self.x - canvas_width /2

        if(self.y >=  canvas_height/2 and self.y < (backgraound_height - canvas_height)):
            self.y_scrolling = self.y - canvas_height/2

    def _canvas_crush(self):
        if self.x - self.x_scrolling > canvas_width:
            self.x= canvas_width + self.x_scrolling
        elif self.x < 0:
            self.x = 0

    def foothold_crush(self, foothold_hitbox):
        left_boy, bottom_boy, right_boy, top_boy = self.return_hitbox()
        left_foothold, bottom_foothold, right_foothold, top_foothold = foothold_hitbox

        if bottom_boy < top_foothold and bottom_boy > bottom_foothold:foothold_crush = True
        else:foothold_crush = False
        if left_boy > right_foothold: foothold_crush = False
        if right_boy < left_foothold : foothold_crush = False


        if(foothold_crush == True and self.hang == False):
            self.fall = False
            self.y = top_foothold + 29
            self.jump_max_point =  self.y + self.JUMP_HIGHT

            if(self.state == self.HANG):
                self.state = self.RIGHT_STAND

            if self.state == self.RIGHT_JUMP:
                self.state = self.RIGHT_STAND

            elif self.state == self.LEFT_JUMP:
                self.state = self.LEFT_STAND

            self.y_dir = 0

    def rope_crush(self, rope_hitbox):
        left_boy, bottom_boy, right_boy, top_boy = self.return_hitbox()
        left_rope, bottom_rope, right_rope, top_rope = rope_hitbox

        rope_crush = True
        if left_boy > right_rope: rope_crush = False
        elif right_boy < left_rope : rope_crush = False
        elif top_boy < bottom_rope : rope_crush = False
        elif bottom_boy > top_rope : rope_crush = False

        if(rope_crush == True):
            self.can_hang = True
            self.rope_x_pos = (left_rope + right_rope) / 2

    def obstacle_crush(self, obstacle_hitbox):
        left_boy, bottom_boy, right_boy, top_boy = self.return_hitbox()
        left_obstacle, bottom_obstacle, right_obstacle, top_obstacle = obstacle_hitbox

        obstacle_crush = True
        if left_boy > right_obstacle: obstacle_crush = False
        elif right_boy < left_obstacle : obstacle_crush = False
        elif top_boy < bottom_obstacle : obstacle_crush = False
        elif bottom_boy > top_obstacle : obstacle_crush = False


        if(obstacle_crush == True and self.pushed == False and self.invincible == False):
            self.pushed_sound.play()

            if self.x > (left_obstacle + right_obstacle) / 2:
                self.pushed_dir = 1
            elif self.x < (left_obstacle + right_obstacle) / 2:
                self.pushed_dir = -1

            self.pushed_meter = self.PUSHED_MAX_METER
            self.pushed = True

    def portal_crush(self, portal_hitbox):
        left_boy, bottom_boy, right_boy, top_boy = self.return_hitbox()
        left_portal, bottom_portal, right_portal, top_portal = portal_hitbox

        if left_boy > right_portal: self.can_cross_portal = False
        elif right_boy < left_portal : self.can_cross_portal = False
        elif top_boy < bottom_portal : self.can_cross_portal = False
        elif bottom_boy > top_portal : self.can_cross_portal = False
        else: self.can_cross_portal = True

    def cross_portal(self):
        if(self.can_cross_portal == True and self.stand_cross_portal == True):
            return True
        else : return False

    def _jump(self, frame_time):

        #점프 모션 설정
        if( self.state in (self.RIGHT_STAND, self.RIGHT_RUN, self.HANG)):
            self.state = self.RIGHT_JUMP
        elif(self.state in (self.LEFT_STAND, self.LEFT_RUN, self.HANG)):
            self.state = self.LEFT_JUMP

        #점프한 높이 설정
        distance = Boy.JUMP_SPEED_PPS * frame_time
        self.y_dir = 1;
        self.cur_jumped_meter += distance
        #점프의 마지막 높이 설정
        if (self.cur_jumped_meter > self.JUMP_HIGHT):
            self.y += distance - self.cur_jumped_meter + self.JUMP_HIGHT
            self.jump = False
            self.cur_jumped_meter = 0
            self.jump_sound_state = self.SOUND_NONE_PLAY
        else:
            self.y += distance

    def _set_frame(self, frame_time):
        if (self.x_dir == 0 and (self.state == self.RIGHT_STAND or self.state == self.LEFT_STAND)):  #멈췃을때 이미지 스프라이트가 없어서 편법 사용
            self.total_frames = 0
        elif (self.state == self.RIGHT_LIE or self.state == self.LEFT_LIE):
            self.total_frames = 0
        elif (self.state == self.RIGHT_JUMP or self.state == self.LEFT_JUMP):
            self.total_frames = 0

        if (self.state == self.HANG and self.hang_y_dir == 0):
            self.frame = 0

        else : self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time

        if(self.frame % 4 == 1 and self.state in (self.LEFT_RUN, self.RIGHT_RUN) and self.run_sound_cnt == 0):
            self.run_sound.play()
            self.run_sound_cnt +=1
        elif self.frame %4 == 3:
            self.run_sound_cnt = 0

        self.frame = int(self.total_frames) % 4

    def draw(self):
        self.image.clip_draw((self.frame) * 100 + self.invincible_sprite, self.state * 100, 100, 100, self.x - self.x_scrolling, self.y - self.y_scrolling)

    def draw_hitbox(self):
        draw_rectangle(self.return_hitbox()[0] -self.x_scrolling, self.return_hitbox()[1] -self.y_scrolling,
                       self.return_hitbox()[2] -self.x_scrolling, self.return_hitbox()[3] -self.y_scrolling)

    #키입력
    def handle_event(self, event):

        #오른쪽 방향키 입력
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self._handle_right_run()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN, self.RIGHT_JUMP, self.HANG):
                self._handle_right_stand()

        #왼쪽 방향키 입력
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self._handle_left_run()
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,self.LEFT_JUMP, self.HANG):
                self._handle_left_stand()

        #위쪽 방향키 입력
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN, self.HANG, self.LEFT_JUMP, self.RIGHT_JUMP):
                self._handle_up_hang()
            self.stand_cross_portal = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state == self.HANG:
                self._handle_hang_False()
            self.stand_cross_portal = False

        #아래쪽 방향키 입력
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN):
                self._handle_lie()

            self._handle_down_hang()

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.RIGHT_LIE, self.LEFT_LIE):
                self._handle_rise()

            self._handle_hang_False()

        #왼쪽 알트키 입력
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LALT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN, self.LEFT_RUN, self.HANG):
                self._handle_jump()

    def _handle_right_run(self):

        if(self.hang == True):
            self.hang_x_dir = 1
        elif self.fall == False:
            self.x_dir = 1
            self.state = self.RIGHT_RUN
            self.run_sound_cnt = 0

    def _handle_right_stand(self):
        self.x_dir = 0
        self.hang_x_dir = 0
        self.state = self.RIGHT_STAND

    def _handle_left_run(self):

        if(self.hang == True):
            self.hang_x_dir = -1
        elif self.fall == False:
            self.x_dir = -1
            self.state = self.LEFT_RUN
            self.run_sound_cnt = 0

    def _handle_left_stand(self):
        self.x_dir = 0
        self.hang_x_dir = 0
        self.state = self.LEFT_STAND

    def _handle_jump(self):
        if(self.jump == False):
            self.jump_sound.play()
            self.jump = True

        if(self.hang == True):
            self.stand_hang = False
            self.hang = False
            self.x_dir = self.hang_x_dir

            if(self.x_dir < 0):
                self.state = self.LEFT_JUMP
            elif(self.x_dir > 0):
                self.state = self.RIGHT_JUMP

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

    def _handle_up_hang(self):
        if self.pushed == False:
            self.stand_hang = True
            self.hang_y_dir = 1

    def _handle_down_hang(self):
        if self.pushed == False:
            self.stand_hang = True
            self.hang_y_dir = -1

    def _handle_hang_False(self):
        if(self.can_hang == False):
            self.hang = False

        self.hang_y_dir = 0






