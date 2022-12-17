add_library('minim')
from random import randint

import config
import game_singleton


def setup():
    size(int(config.RES.x), int(config.RES.y))
    background(255)
    config.populate_sound_name2obj(Minim(this).loadFile)
    config.sound_name2obj["main_music"].loop(-1)


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
