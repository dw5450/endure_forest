from pico2d import *

import game_framework

import title_state

import class_folder.UI
import class_folder.Boy
import class_folder.Lupin
import class_folder.Foothold
import class_folder.Rope

import function_folder.Load_map_object
import function_folder.canvas_property

draw_hitbox = False
UI = None
boy = None
lupins = []
footholds = []
ropes = []
current_time =0
frame_time = 0

def enter():
    # fill here
    global ui, boy, lupins, footholds, ropes


    ui = class_folder.UI.UI()
    boy = class_folder.Boy.Boy()

    footholds = function_folder.Load_map_object.load_foothold()
    for foothold in footholds:
        foothold.set_player(boy)

    ropes = function_folder.Load_map_object.load_rope()
    for rope in ropes:
        rope.set_player(boy)

    lupins = function_folder.Load_map_object.load_lupin()
    for lupin in lupins:
        lupin.set_player(boy)

    current_time = get_time()


def exit():
    global footholds, ropes, lupins, boy

    del(footholds)
    del(ropes)
    del(lupins)
    del(boy)
    close_canvas()
    game_framework.pop_state()

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global boy, draw_hitbox
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
             exit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
             exit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
             game_framework.change_state(title_state)
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
            if(draw_hitbox == True):
                draw_hitbox = False
            elif(draw_hitbox == False):
                draw_hitbox = True
        else:
            boy.handle_event(event)


def update(frame_time):
    # fill here
    global current_time
    frame_time = get_time() - current_time
    boy.update(frame_time)
    for lupin in lupins:
        lupin.update(frame_time)

    boy.can_hang = False
    for rope in ropes:
        boy.rope_crush(rope.return_hitbox())

    boy.fall = True
    for foothold in footholds:
        boy.foothold_crush(foothold.return_hitbox())

    for lupin in lupins:
        boy.obstacle_crush(lupin.return_banana_hibox())
        boy.obstacle_crush(lupin.return_lupin_hitbox())


    current_time += frame_time

def draw(frame_time):
    # fill here
    global draw_hitbox
    clear_canvas()
    function_folder.canvas_property.draw_background(boy)
    ui.draw()
    for foothold in footholds:
        foothold.draw()
        if(draw_hitbox == True):
            foothold.draw_hitbox()

    for rope in ropes:
        rope.draw()
        if(draw_hitbox == True):
            rope.draw_hitbox()

    for lupin in lupins:
        lupin.draw()
        if(draw_hitbox == True):
            lupin.draw_lupin_hitbox()
            lupin.draw_banana_hibox()

    boy.draw()
    if(draw_hitbox == True):
        boy.draw_hitbox()

    update_canvas()

def main():
    enter()

    while True:
        handle_events(frame_time)
        update(frame_time)
        draw(frame_time)

if __name__ == '__main__':
    main()