
import game_framework

from pico2d import *

name = "TitleState"
image = None
title_sound =None
global mouse_x, mouse_y

import main_state
import explain_state



def enter():
    # fill here
    open_canvas()
    global image, title_sound
    image = load_image('image_folder//title.PNG')                         #타이틀 이미지를 가져옴
    title_sound = load_music('sound_folder//Title.ogg')
    title_sound.set_volume(64)
    title_sound.repeat_play()

def exit():
    # fill here
    global image
    del(image)

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    # fill here
    global title_sound
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if 370 < event.x and event.x < 460 and 190 < 600 - event.y and 600 - event.y < 230:
                game_framework.change_state(main_state)
            elif 485 < event.x and event.x < 575 and 190 < 600 - event.y and 600 - event.y < 230:
                game_framework.change_state(explain_state)
            elif 600 < event.x and event.x < 675 and 190 < 600 - event.y and 600 - event.y < 230:
                game_framework.quit()


def update(frame_time):
    pass

def draw(frame_time):
    # fill here
    clear_canvas()
    image.draw(400, 300)

    update_canvas()


def main():
    enter()

    while True:
        handle_events(0)
        update(0)
        draw(0)

if __name__ == '__main__':
    main()






