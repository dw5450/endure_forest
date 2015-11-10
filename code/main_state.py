from pico2d import *

import game_framework

import title_state

import class_folder.Boy
import class_folder.Background
import class_folder.rupin


background = None
boy = None
rupin = None
running = True
frame_time = 0

def enter():
    # fill here
    global background
    global boy
    global rupin
    background = class_folder.Background.Background()
    boy = class_folder.Boy.Boy()
    rupin = class_folder.rupin.Lupin()
    background.set_senter(boy)

def exit():
    global background
    global boy
    global rupin
    del(background)
    del(boy)
    del(rupin)
    close_canvas()
    game_framework.pop_state()

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
             exit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
             exit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
             game_framework.change_state(title_state)
        else:
            boy.handle_event(event)


def update(frame_time):
    # fill here
    frame_time+=0.01
    background.update(frame_time)
    boy.update(frame_time)
    rupin.update(frame_time)
    delay(0.01);

def draw(frame_time):
    # fill here
    clear_canvas()
    background.draw()
    boy.draw()
    rupin.draw()
    update_canvas()

def main():
    enter()
    while running:
        handle_events(frame_time)
        update(frame_time)
        draw(frame_time)

if __name__ == '__main__':
    main()