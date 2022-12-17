add_library('minim')
from random import randint

import config
import game_singleton


def setup():
    size(int(config.RES.x), int(config.RES.y))
    background(255)
    game_singleton.populate_sound_name2obj(Minim(this).loadFile)
    game_singleton.play_music_by_name("main_music", is_loop_infinitely=True)


def draw():
    background(255)
    game_singleton.game.process()
    game_singleton.game.draw()


def keyPressed():
    game_singleton.game.inputs.add(keyCode)


def keyReleased():
    game_singleton.game.inputs.discard(keyCode)


def mousePressed():
    game_singleton.game.inputs.add(config.MOUSE)


def mouseReleased():
    game_singleton.game.inputs.remove(config.MOUSE)
