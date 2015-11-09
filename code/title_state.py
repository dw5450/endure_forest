import game_framework

from pico2d import *

import main_state


name = "TitleState"
image = None

def enter():
    # fill here
    open_canvas();
    global image
    image = load_image('image_folder//title.PNG')                         #타이틀 이미지를 가져옴

def exit():
    # fill here
    global image
    del(image)
    close_canvas();
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
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):                           #스페이스를 누를시 게임 화면으로 넘어감
            game_framework.push_state(main_state)

def update(frame_time):
    pass

def draw(frame_time):
    # fill here
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


