from random import randint
from os import getcwd

RES = PVector(800, 800)
TILE_NUM = PVector(20, 20)
TILE_RES = PVector(RES.x//TILE_NUM.x, RES.y//TILE_NUM.y)
path = getcwd()

class Player:
    
    def __init__(self):
        self.speed = 10
        self.vel = PVector(0, 0)
        self.pos = PVector(20, 20)
        self.direction = PVector(20, 20)
        self.friction = 0.85
    
    def process(self):
        if self.direction.magSq() == 0:
            self.vel *= self.friction
            if self.vel.magSq() < 1:
                self.vel.set(0, 0)
        else:
            self.vel = self.speed * self.direction
        self.pos += self.vel
    
    def draw(self):
        circle(self.pos.x, self.pos.y, 20)

    def process_input(self):
        self.direction = PVector(0, 0)
        for input_keyCode in game.pressed_keys:
            if input_keyCode == RIGHT:
                self.direction.x += 1
            elif input_keyCode == LEFT:
                self.direction.x -= 1
            elif input_keyCode == UP:
                self.direction.y -= 1
            elif input_keyCode == DOWN:
                self.direction.y += 1
        self.direction.normalize()


class Game:
    
    def __init__(self):
        self.player = Player()
        self.signals = dict()
        self.pressed_keys = set()

    def connect_to_signal(self, signal_name, callback):
        self.signals[signal_name] = self.signals.get(signal_name, []) + [ callback ]

    def emit_signal(self, signal_name, emitter):
        for callback in self.signals[signal_name]:
            callback(emitter)

game = Game()

def setup():
    size(int(RES.x), int(RES.y))
    background(255)

def draw():
    background(255)
    game.player.process_input()
    game.player.process()
    game.player.draw()

def keyPressed():
    game.pressed_keys.add(keyCode)

def keyReleased():
    game.pressed_keys.discard(keyCode)
