from os import getcwd
from random import randint

import game_singleton, config

path = getcwd()


def setup():
    size(int(config.RES.x), int(config.RES.y))
    background(255)

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
