from math import pi
from random import randint

import game_singleton


class Entity:

    def __init__(self, pos, radius=10, direction=PVector(1, 0)):
        self.pos = pos
        self.radius = radius
        self.health = 10
        self.speed = 10
        self.vel = PVector(0, 0)
        self.direction = direction
        self.prev_non_zero_direction = direction
        self.friction = 0.85

    def check_collision(self, other_colliding_obj):
        return (
            self.pos.dist(other_colliding_obj.pos)
            <= self.radius + other_colliding_obj.radius
            )

    def process(self):
        if self.direction.magSq() == 0:
            self.vel *= self.friction
            if self.vel.magSq() < 1:
                self.vel.set(0, 0)
        else:
            self.prev_non_zero_direction = self.direction
            self.vel = self.speed * self.direction
        self.pos += self.vel

    def draw(self):
        raise NotImplementedError()
    
    def on_collision(self, other_colliding_obj):
        raise NotImplementedError()

    def shoot(self, projectile_direction=None):
        projectile_radius = 2
        projectile_pos = self.pos + (self.radius + projectile_radius) * self.prev_non_zero_direction
        Projectile(
            projectile_pos,
            self,
            self.prev_non_zero_direction.copy().rotate(randint(-20, 20)/100.0),
            radius=projectile_radius
        )


class Player(Entity):
    
    def __init__(self, pos):
        Entity.__init__(self, pos, radius=25)
        self.frozen = False
        self.is_ready_to_shoot = True
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
            elif input_keyCode == 32: # 32 = ASCII code for space
                self.shoot(self.prev_non_zero_direction)
        self.direction.normalize()

    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Enemy):
            self.vel = (self.pos - other_colliding_obj.pos).normalize()*self.knock_back_speed
            self.frozen = True

    def shoot(self, projectile_direction=None):
        if self.is_ready_to_shoot:
            Entity.shoot(self, projectile_direction)
            self.is_ready_to_shoot = False
            def __(): self.is_ready_to_shoot = True
            game_singleton.game.create_timer(0.1, __)

    def process(self):
        is_dir_0 = self.direction.magSq() == 0
        if not is_dir_0:
            self.prev_non_zero_direction = self.direction
        if self.frozen or is_dir_0:
            self.vel *= self.friction if not self.frozen else self.frozen_friction
            if self.vel.magSq() < 1:
                self.frozen = False
                self.vel.set(0, 0)
        elif not self.frozen:
            self.vel = self.speed * self.direction
        self.pos += self.vel


class Enemy(Entity):

    enemies = []
    def __init__(self, pos, radius=10, direction=PVector(1, 0)):
        Entity.__init__(self, pos, radius, direction)
        Enemy.enemies.append(self)

    def draw(self):
        fill(255, 0, 0)
        circle(self.pos.x, self.pos.y, self.radius*2)

    def on_collision(self, other_colliding_obj):
        if other_colliding_obj is Projectile:
            self.health -= other_colliding_obj.damage
            if self.health <= 0:
                Enemy.enemies.remove(self)


class Projectile(Entity):

    projectiles = []
    def __init__(self, pos, parent, direction, radius=8):
        Entity.__init__(self, pos, radius=8, direction=direction)
        self.damage = 10
        self.parent = parent
        self.speed = 15
        Projectile.projectiles.append(self)

    def on_collision(self, other_colliding_obj):
        Projectile.projectiles.remove(self)

    def draw(self):
        fill(0, 255, 0)
        circle(self.pos.x, self.pos.y, self.radius*2)

    def process(self):
        Entity.process(self)
        if (
                self.pos.x < 0
                or self.pos.x > game_singleton.game.RES.x
                or self.pos.y < 0
                or self.pos.y > game_singleton.game.RES.y
        ):
            Projectile.projectiles.remove(self)
