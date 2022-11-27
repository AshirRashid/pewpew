from os import getcwd
from random import randint

from game import Game

path = getcwd()
game = Game()


def setup():
    size(int(game.RES.x), int(game.RES.y))
    background(255)

def draw():
    background(255)
    game.process()
    game.draw()

def keyPressed():
    game.pressed_keys.add(keyCode)

def keyReleased():
    game.pressed_keys.discard(keyCode)
