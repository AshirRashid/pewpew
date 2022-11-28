from entities import Enemy, Player, Projectile
from time import time
from copy import copy


class Game:

    def __init__(self):
        self.RES = PVector(800, 800)
        self.TILE_NUM = PVector(20, 20)
        self.TILE_RES = PVector(self.RES.x//self.TILE_NUM.x, self.RES.y//self.TILE_NUM.y)

        self.timer_manager = TimerManager()
        self.pressed_keys = set()
        self.start, self.end = PVector(10, 10), PVector(self.RES.x - 10, self.RES.y - 10) # map boundary
        self.player = Player(PVector(self.RES.x/2, self.RES.y/2))

    def setup(self):
        Enemy(PVector(100, 100), 30)
        Enemy(PVector(200, 200), 30)

    def process(self):
        self.timer_manager.process_timers()
        self.player.process_input(self.pressed_keys)
        self.player.process()

        for entity in Enemy.enemies:
            entity.process()
            if self.player.check_collision(entity):
                self.player.on_collision(entity)
                entity.on_collision(self.player)
        for projectile in Projectile.projectiles:
            projectile.process()
            if self.player.check_collision(projectile):
                pass

    def draw(self):
        self.player.draw()
        for entity in Enemy.enemies:
            entity.draw()
        for projectile in Projectile.projectiles:
            projectile.draw()

    def spawn_obj_by_class(self, obj_type):
        """Simple object factory"""
        if obj_type == "player":
            new_obj = Player()
        elif obj_type == "enemy":
            new_obj = Enemy()
        elif obj_type == "pickup":
            new_obj = Pickup()
        else:
            raise NotImplementedError()
        return new_obj

    def create_timer(self, time_in_s, callback):
        self.timer_manager.add_timer(time_in_s, callback)


class TimerManager:

    def __init__(self):
        self.timers = []

    def add_timer(self, time_in_s, callback):
        self.timers.append((
            time(),
            time_in_s,
            callback
        ))

    def process_timers(self):
        for timer in copy(self.timers):
            start_time, time_in_s, callback = timer
            if time() > start_time + time_in_s:
                self.timers.remove(timer)
                callback()
