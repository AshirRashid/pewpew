from os import getcwd
from random import randint

import game_singleton
from game import Game

path = getcwd()
game_singleton.game = Game()


def setup():
    size(int(game_singleton.game.RES.x), int(game_singleton.game.RES.y))
    background(255)
    game_singleton.game.setup()

def draw():
    background(255)
    game_singleton.game.process()
    game_singleton.game.draw()

def keyPressed():
    game_singleton.game.inputs.add(keyCode)

def keyReleased():
    game_singleton.game.inputs.discard(keyCode)

def mousePressed():
    game_singleton.game.inputs.add(game_singleton.game.MOUSE)

def mouseReleased():
    game_singleton.game.inputs.remove(game_singleton.game.MOUSE)
