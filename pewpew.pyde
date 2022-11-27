from random import randint
from os import getcwd
from entities import Player, Enemy

RES = PVector(800, 800)
TILE_NUM = PVector(20, 20)
TILE_RES = PVector(RES.x//TILE_NUM.x, RES.y//TILE_NUM.y)
path = getcwd()


class Game:
    
    def __init__(self):
        self.signals = dict()
        self.pressed_keys = set()
        self.start, self.end = PVector(10, 10), PVector(RES.x - 10, RES.y - 10) # map boundary
        self.player = Player(PVector(RES.x/2, RES.y/2))
        self.entities = [Enemy(PVector(100, 100), 50)] # all non-player entities
    
    def process(self):
        self.player.process_input(game.pressed_keys)
        self.player.process()

        for entity in self.entities:
            if self.player.check_collision(entity):
                self.player.on_collision(entity)
                entity.on_collision(self.player)

    def draw(self):
        self.player.draw()
        for entity in self.entities:
            entity.draw()

    def connect_to_signal(self, signal_name, callback):
        self.signals[signal_name] = self.signals.get(signal_name, []) + [ callback ]

    def emit_signal(self, signal_name, emitter):
        for callback in self.signals[signal_name]:
            callback(emitter)
    

def spawn_obj_by_class(obj_type):
    """Simple object factory"""
    new_obj = {
        "player": Player,
        "enemy": Enemy,
        "pickup": Pickup
    }[obj_type]()

    if obj_type == "player":
        new_obj = Player()
    elif obj_type == "enemy":
        new_obj = Enemy()
    elif obj_type == "pickup":
        new_obj = Pickup()
    else:
        raise NotImplementedError()


game = Game()

def setup():
    size(int(RES.x), int(RES.y))
    background(255)

def draw():
    background(255)
    game.process()
    game.draw()

def keyPressed():
    game.pressed_keys.add(keyCode)

def keyReleased():
    game.pressed_keys.discard(keyCode)
