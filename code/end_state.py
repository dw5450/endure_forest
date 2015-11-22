__author__ = 'no_game'

import game_framework

from pico2d import *

import main_state


name = "EndState"
end_image = None
end_sign_image = None
end_sound =None

def enter():
    # fill here
    open_canvas()
    global end_image, end_sign_image, end_sound
    end_image = load_image('image_folder//end.PNG')                         #타이틀 이미지를 가져옴
    end_sign_image = load_image('image_folder//end_sign.PNG')
    end_sound = load_music('sound_folder//End.ogg')
    end_sound.set_volume(64)
    end_sound.repeat_play()

def exit():
    # fill here
    global image
    del(image)
    close_canvas()
    game_framework.quit()

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    # fill here
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            exit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if 300 < event.x and event.x < 470 and 190 < 600 - event.y and 600 - event.y < 280:
                exit()

def update(frame_time):
    pass

def draw(frame_time):
    # fill here
    clear_canvas()
    end_image.draw(400, 300)
    end_sign_image.draw(400, 300)
    update_canvas()


