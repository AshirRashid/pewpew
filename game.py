from entities import Enemy, Player, Projectile, ShootingEnemy
from time import time
from copy import copy


class Game:

    def __init__(self):
        self.SPACE = 32 # ASCII code for space
        self.MOUSE = -1
        self.RES = PVector(800, 800)
        self.TILE_NUM = PVector(20, 20)
        self.TILE_RES = PVector(self.RES.x//self.TILE_NUM.x, self.RES.y//self.TILE_NUM.y)

        # _state = "playing" | "paused" | "won" | "lost" | "main_menu"
        self._state = "playing"
        self.timer_manager = TimerManager()
        self.inputs = set()
        self.start, self.end = PVector(10, 10), PVector(self.RES.x - 10, self.RES.y - 10) # map boundary
        self.player = Player(PVector(self.RES.x/2, self.RES.y/2))

    def resume(self): self._state = "playing"

    def pause(self): self._state = "paused"

    def setup(self):
        # Enemy(PVector(500, 100))
        # ShootingEnemy(PVector(100, 100), motion_type="static", shooting_type="radial")
        # ShootingEnemy(PVector(500, 500), motion_type="static", shooting_type="shotgun")

        # One Level
        # ShootingEnemy(PVector(100, 100), motion_type="static", shooting_type="radial")
        # ShootingEnemy(PVector(700, 100), motion_type="static", shooting_type="radial")
        # ShootingEnemy(PVector(100, 700), motion_type="static", shooting_type="radial")
        ShootingEnemy(PVector(700, 700), motion_type="static", shooting_type="radial")

    def process(self):
        if self._state == "playing":
            self.timer_manager.process_timers()
            self.player.process_input(self.inputs)
            self.player.process()

            for projectile in Projectile.projectiles:
                projectile.process()
                if self.player.check_collision(projectile):
                    self.player.on_collision(projectile)
                    projectile.on_collision(self.player)
            for entity in Enemy.enemies:
                entity.process()
                for projectile in Projectile.projectiles:
                    if entity.check_collision(projectile):
                        entity.on_collision(projectile)
                        projectile.on_collision(entity)
                if self.player.check_collision(entity):
                    self.player.on_collision(entity)
                    entity.on_collision(self.player)
        elif self._state == "paused":
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
