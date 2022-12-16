from entities import Enemy, Player, Projectile, ShootingEnemy, Pickup, SpawnerEnemy, ObstacleEnemy
from ui import MainMenu, WinMenu, LostMenu
from time import time
from copy import copy
import config


class Game:

    def __init__(self):
        self.level_name2function = {
            "1": self.level_1,
            "2": self.level_2,
            "3": self.level_3,
            "4": self.level_4,
            "5": self.level_5,
        }
        self.main_menu = MainMenu(self.level_name2function)
        self.win_menu = WinMenu()
        self.lost_menu = LostMenu()
        # _state = "playing" | "paused" | "won" | "lost" | "main_menu"
        self._state = "main_menu"
        self.timer_manager = TimerManager()
        self.inputs = set()
        self.start, self.end = PVector(10, 10), PVector(config.RES.x - 10, config.RES.y - 10) # map boundary
        self.on_unpause_callbacks = []
        self.display_text = "3"

    def start_game(self):
        self.pause()
        self.setup()
        self.display_text = "3"
        def countdown_0():
            self.display_text = "0"
            self.resume()
        def countdown_1():
            self.display_text = "1"
            self.create_timer(1, countdown_0)
        def countdown_2():
            self.display_text = "2"
            self.create_timer(1, countdown_1)
        self.create_timer(1, countdown_2)

    def resume(self):
        self._state = "playing"
        for callback in self.on_unpause_callbacks:
            callback()

    def pause(self): self._state = "paused"

    def is_paused(self): return self._state == "paused"

    def setup(self):
        Projectile.projectiles = set()
        Enemy.enemies = set()
        Pickup.pickups = set()
        self.player = Player(PVector(config.RES.x/2, config.RES.y/2))

    def process(self):
        self.process_input()
        self.timer_manager.process_timers()
        if self._state == "playing":
            self.check_win()
            self.player.process()
            for projectile in Projectile.projectiles:
                projectile.process()
                if self.player.check_collision(projectile):
                    self.player.on_collision(projectile)
                    projectile.on_collision(self.player)
            for pickup in Pickup.pickups:
                pickup.process()
                if self.player.check_collision(pickup):
                    self.player.on_collision(pickup)
                    pickup.on_collision(self.player)
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
        if self._state == "main_menu":
            self.main_menu.draw()
        elif self._state == "won":
            self.win_menu.draw()
        elif self._state == "lost":
            self.lost_menu.draw()
        elif self._state in ("playing", "paused"):
            self.player.draw()
            for entity in Enemy.enemies:
                entity.draw()
            for projectile in Projectile.projectiles:
                projectile.draw()
            for pickup in Pickup.pickups:
                pickup.draw()
            fill(0)
            textSize(30)
            textAlign(CENTER, TOP)
            text(self.display_text, config.RES.x/2, 0)

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

    def process_input(self):
        if self._state == "main_menu":
            self.main_menu.process_input(self.inputs)
        elif self._state == "playing":
            self.player.process_input(self.inputs)
        elif self._state == "won":
            self.win_menu.process_input(self.inputs)
        elif self._state == "lost":
            self.lost_menu.process_input(self.inputs)

    def check_win(self):
        if len(Enemy.enemies) == 0:
            self._state = "won"

    def on_player_lost(self): self._state = "lost"

    def go_to_main_menu(self): self._state = "main_menu"

    def level_2(self):
        self.start_game()
        Enemy(PVector(500, 100))
        Pickup(PVector(100, 100))
        Pickup(PVector(100, 500), "damage")
        ObstacleEnemy(PVector(400, 200))
        SpawnerEnemy(PVector(200, 600))
        ShootingEnemy(PVector(500, 500), motion_type="static", shooting_type="shotgun")

    def level_3(self):
        self.start_game()
        ShootingEnemy(PVector(100, 100), motion_type="static", shooting_type="radial")
        ShootingEnemy(PVector(700, 100), motion_type="static", shooting_type="radial")
        ShootingEnemy(PVector(100, 700), motion_type="static", shooting_type="radial")
        ShootingEnemy(PVector(700, 700), motion_type="static", shooting_type="radial")

    def level_4(self):
        self.start_game()
        ShootingEnemy(PVector(700, 700), motion_type="static", shooting_type="radial")
        ShootingEnemy(PVector(100, 100), motion_type="static", shooting_type="radial")
        SpawnerEnemy(PVector(700, 100))
        Pickup(PVector(100, 400))
        ShootingEnemy(PVector(100, 700), motion_type="static", shooting_type="shotgun")

    def level_5(self):
        self.start_game()
        ShootingEnemy(PVector(400, 200), motion_type="static", shooting_type="radial")
        ShootingEnemy(PVector(400, 600), motion_type="static", shooting_type="radial")
        Pickup(PVector(400, 450), "damage")
        ShootingEnemy(PVector(100, 700), motion_type="static", shooting_type="shotgun")
        ShootingEnemy(PVector(100, 100), motion_type="static", shooting_type="shotgun")
        ShootingEnemy(PVector(700, 100), motion_type="static", shooting_type="shotgun")
        ShootingEnemy(PVector(700, 700), motion_type="static", shooting_type="shotgun")

    def level_1(self):
        self.start_game()
        SpawnerEnemy(PVector(100, 700))
        SpawnerEnemy(PVector(100, 100))
        SpawnerEnemy(PVector(700, 700))
        SpawnerEnemy(PVector(700, 100))
        ObstacleEnemy(PVector(400, 300))
        ObstacleEnemy(PVector(400, 500))
        ObstacleEnemy(PVector(300, 400))
        ObstacleEnemy(PVector(500, 400))


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
