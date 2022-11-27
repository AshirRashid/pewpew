from entities import Enemy, Player


class Game:

    def __init__(self):
        self.RES = PVector(800, 800)
        self.TILE_NUM = PVector(20, 20)
        self.TILE_RES = PVector(self.RES.x//self.TILE_NUM.x, self.RES.y//self.TILE_NUM.y)

        self.signals = dict()
        self.pressed_keys = set()
        self.start, self.end = PVector(10, 10), PVector(self.RES.x - 10, self.RES.y - 10) # map boundary
        self.projectiles = []
        self.player = Player(PVector(self.RES.x/2, self.RES.y/2), self.projectiles)
        self.entities = [
            # Enemy(PVector(100, 100), self.projectiles, 50),
            # Enemy(PVector(200, 200), self.projectiles, 50)
        ] # all non-player entities

    def process(self):
        self.player.process_input(self.pressed_keys)
        self.player.process()

        for entity in self.entities:
            entity.process()
            if self.player.check_collision(entity):
                self.player.on_collision(entity)
                entity.on_collision(self.player)
        for projectile in self.projectiles:
            projectile.process()
            if self.player.check_collision(projectile):
                pass

    def draw(self):
        self.player.draw()
        for entity in self.entities:
            entity.draw()
        for projectile in self.projectiles:
            projectile.draw()

    def connect_to_signal(self, signal_name, callback):
        self.signals[signal_name] = self.signals.get(signal_name, []) + [ callback ]

    def emit_signal(self, signal_name, emitter):
        for callback in self.signals[signal_name]:
            callback(emitter)

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
