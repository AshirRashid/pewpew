from utils import CollisionShape

class Pickup:

    def __init__(self):
        """self.type = "heal" | "slow_enemies" | "increase_damage" """
        self.type = None
        self.pos = PVector(20, 20)
        self.collision_shape = CollisionShape(self, self.pos, 20, self.on_collision)
