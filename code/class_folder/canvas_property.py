__author__ = 'no_game'
import json

canvas_width = None
canvas_height = None

backgraound_width = None
backgraound_height = None

backgraound_original_width = None
backgraound_original_height = None

canvas_property_file = open('data_folder//canvas_property.txt', 'r')
canvas_property = json.load(canvas_property_file)
canvas_property_file.close()

backgraound_width = canvas_property['backgraound_width']
backgraound_height = canvas_property['backgraound_height']

canvas_width = canvas_property['canvas_width']
canvas_height = canvas_property['canvas_height']

backgraound_original_width = canvas_property['backgraound_original_width']
backgraound_original_height = canvas_property['backgraound_original_height']
