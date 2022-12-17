"""
Main Processing python file

Classes:

Functions:
    setup
    draw
    keyPressed: add key to an event queue
    keyReleased: remove key from the event queue
    mousePressed: add mouse input to the event queue
        (Represented as constansts.MOUSE)
    mouseReleased: remove mouse input from the event queue

Misc variables:

"""
add_library('minim')

import game_singleton
from constants import MOUSE, RES


def setup():
    size(int(RES.x), int(RES.y))
    background(255)
    game_singleton.populate_sound_name2obj(Minim(this).loadFile)
    game_singleton.play_music_by_name("main_music", is_loop_infinitely=True)


def draw():
    background(255)
    game_singleton.game.process()
    game_singleton.game.draw()


def keyPressed(): game_singleton.game.inputs.add(keyCode)


def keyReleased(): game_singleton.game.inputs.discard(keyCode)


def mousePressed(): game_singleton.game.inputs.add(MOUSE)


def mouseReleased(): game_singleton.game.inputs.remove(MOUSE)
