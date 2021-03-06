from pico2d import *

import game_framework

import title_state
import end_state

import Boy

name = "main_state"

from Boy import Boy
from Foothold import Foothold
from Portal import Portal
from Lupin import Lupin
from Rope import Rope
from UI import UI

from Load_map_object import *
from canvas_property import *

draw_hitbox = False
ui = None
boy = None
portal = None
lupins = []
footholds = []
ropes = []
current_time = 0

def enter():
    # fill here
    global ui, boy, lupins, footholds, ropes, portal

    ui = UI()
    boy = Boy()

    footholds =load_foothold()
    for foothold in footholds:
        foothold.set_player(boy)

    ropes = load_rope()
    for rope in ropes:
        rope.set_player(boy)

    lupins = load_lupin()

    for lupin in lupins:
        lupin.set_player(boy)

    portal = Portal()
    portal.set_player(boy)

    current_time = get_time()


def exit():
    global footholds, ropes, lupins, boy

    del(footholds)
    del(ropes)
    del(lupins)
    del(boy)

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global boy, draw_hitbox
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
             game_framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
             game_framework.quit()
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
        if rope.crush_optimization() == True:
            boy.rope_crush(rope.return_hitbox())


    boy.fall = True
    for foothold in footholds:
         if foothold.crush_optimization() == True:
             boy.foothold_crush(foothold.return_hitbox())


    for lupin in lupins:
        if lupin.banana_crush_optimization() == True:
             boy.obstacle_crush(lupin.return_banana_hibox())
        if lupin.lupin_crush_optimization() == True:
            boy.obstacle_crush(lupin.return_lupin_hitbox())


    boy.portal_crush(portal.return_hitbox())


    if boy.cross_portal() == True:
         game_framework.change_state(end_state)

    portal.update(frame_time)

    current_time += frame_time

def draw(frame_time):
    # fill here
    global draw_hitbox

    clear_canvas()

    global draw_hitbox


    clear_canvas()
    draw_background(boy)


    ui.draw()
    for foothold in footholds:
        foothold.draw()


    for rope in ropes:
         rope.draw()


    for lupin in lupins:
        lupin.draw()


    portal.draw()


     #draw road_sign
    draw_road_sign(boy, 650, 600, 1)
    draw_road_sign(boy, 250, 1200, 0)
    draw_road_sign(boy, 850, 1300, 1)


    boy.draw()



    update_canvas()

def main():
    enter()

    while True:
        handle_events(frame_time)
        update(frame_time)
        draw(frame_time)

if __name__ == '__main__':
    main()