__author__ = 'no_game'

import random
import json
from pico2d import *

import class_folder.Lupin
import class_folder.Foothold
import class_folder.Rope
import class_folder.Boy

def load_lupin():
    lupin_data_file = open('data_folder//lupins_data.txt', 'r')
    lupin_data = json.load(lupin_data_file)
    lupin_data_file.close()

    lupin_state_table = {
        "RIGHT_THROW" : class_folder.Lupin.Lupin.RIGHT_THROW,
        "LEFT_THROW" : class_folder.Lupin.Lupin.LEFT_THROW
    }

    lupins = []
    for name in lupin_data:
        lupin = class_folder.Lupin.Lupin()
        lupin.name = name
        lupin.x = lupin_data[name]['x']
        lupin.y = lupin_data[name]['y'] + 60
        lupin.state = lupin_state_table[lupin_data[name]['StartState']]
        lupin.banana_x = lupin.x
        lupin.banana_y = lupin.y + 10
        lupins.append(lupin)
    return lupins

def load_foothold():
    foothold_data_file = open('data_folder//footholds_data.txt', 'r')
    foothold_data = json.load(foothold_data_file)
    foothold_data_file.close()

    foothold_state_table = {
        "EDGE" : class_folder.Foothold.Foothold.EDGE,
        "NON_EDGE" : class_folder.Foothold.Foothold.NON_EDGE
    }

    footholds = []
    for name in foothold_data:
        foothold = class_folder.Foothold.Foothold()
        foothold.name = name
        foothold.x = foothold_data[name]['x']
        foothold.y = foothold_data[name]['y']
        foothold.state = foothold_state_table[foothold_data[name]['StartState']]
        footholds.append(foothold)
    return footholds

def load_rope():
	# fill here
    rope_data_file = open('data_folder//ropes_data.txt', 'r')
    rope_data = json.load(rope_data_file)
    rope_data_file.close()

    foothold_state_table = {
        "BOTTOM_EDGE" : class_folder.Rope.Rope.BOTTOM_EDGE,
        "NON_EDGE" : class_folder.Rope.Rope.NON_EDGE,
        "TOP_EDGE" : class_folder.Rope.Rope.TOP_EDGE
    }

    ropes = []
    for name in rope_data:
        rope = class_folder.Rope.Rope()
        rope.x = rope_data[name]['x']
        rope.y = rope_data[name]['y']
        rope.state = foothold_state_table[rope_data[name]['StartState']]
        ropes.append(rope)
    return ropes