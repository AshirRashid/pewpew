from os import getcwd
from random import randint

from game import Game
import game_singleton

path = getcwd()
game_singleton.game = Game()


def setup():
    size(int(game_singleton.game.RES.x), int(game_singleton.game.RES.y))
    background(255)

def draw():
    background(255)
    game_singleton.game.process()
    game_singleton.game.draw()

def keyPressed():
    game_singleton.game.pressed_keys.add(keyCode)

def keyReleased():
    game_singleton.game.pressed_keys.discard(keyCode)
