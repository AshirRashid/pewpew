from weapons import Weapon
from time import sleep

class Entity:

    def __init__(self, pos, radius=10):
        self.pos = pos
        self.radius = radius
        self.health = 10
        self.speed = 10
        self.vel = PVector(0, 0)
        self.direction = PVector(20, 20)
        self.friction = 0.85
        self.weapon = Weapon()

    def check_collision(self, other_colliding_obj):
        return (
            self.pos.dist(other_colliding_obj.pos)
            <= self.radius + other_colliding_obj.radius
            )

    def process(self):
        raise NotImplementedError()
    
    def draw(self):
        raise NotImplementedError()
    
    def on_collision(self, other_colliding_obj):
        raise NotImplementedError()


class Player(Entity):
    
    def __init__(self, pos):
        Entity.__init__(self, pos)
        self.frozen = False
        self.knock_back_speed = 30
        self.frozen_friction = 0.65

    def draw(self):
        fill(255)
        circle(self.pos.x, self.pos.y, self.radius*2)

    def process_input(self, pressed_keys):
        self.direction = PVector(0, 0)
        for input_keyCode in pressed_keys:
            if input_keyCode == RIGHT:
                self.direction.x += 1
            elif input_keyCode == LEFT:
                self.direction.x -= 1
            elif input_keyCode == UP:
                self.direction.y -= 1
            elif input_keyCode == DOWN:
                self.direction.y += 1
        self.direction.normalize()
    
    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Enemy):
            self.vel = (self.pos - other_colliding_obj.pos).normalize()*self.knock_back_speed
            self.frozen = True
        # elif other_colliding_obj is Pickup:
        #     pass

    def process(self):
        if self.frozen or self.direction.magSq() == 0:
            self.vel *= self.friction if not self.frozen else self.frozen_friction
            if self.vel.magSq() < 1:
                self.frozen = False
                self.vel.set(0, 0)
        elif not self.frozen:
            self.vel = self.speed * self.direction
        self.pos += self.vel


class Enemy(Entity):

    def draw(self):
        fill(255, 0, 0)
        circle(self.pos.x, self.pos.y, self.radius*2)

    def on_collision(self, other_colliding_obj):
        pass
    
    def process(self):
        pass
