from math import pi
from random import randint

import game_singleton


class Entity:

    def __init__(self, pos, radius=10, direction=PVector(1, 0)):
        self.pos = pos
        self.radius = radius
        self.health = 5
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

    def shoot(self, projectile_direction=None, projectile_type="imprecise"):
        """projectile_type = "precise" | "imprecise" """
        if not projectile_direction:
            projectile_direction = self.prev_non_zero_direction
        projectile_radius = 2
        projectile_pos = self.pos + (self.radius + projectile_radius + 3) * projectile_direction
        if projectile_type == "imprecise":
            projectile_direction = projectile_direction.copy().rotate(randint(-20, 20)/100.0)
        Projectile(
            projectile_pos,
            self,
            projectile_direction,
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

    def process_input(self, inputs):
        self.direction = PVector(0, 0)
        for input_keyCode in inputs:
            if input_keyCode == RIGHT:
                self.direction.x += 1
            elif input_keyCode == LEFT:
                self.direction.x -= 1
            elif input_keyCode == UP:
                self.direction.y -= 1
            elif input_keyCode == DOWN:
                self.direction.y += 1
            elif input_keyCode == game_singleton.game.MOUSE:
                self.shoot((PVector(mouseX, mouseY) - self.pos).normalize())
        self.direction.normalize()

    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Enemy):
            self.vel = (self.pos - other_colliding_obj.pos).normalize()*self.knock_back_speed
            self.frozen = True
        elif isinstance(other_colliding_obj, Projectile):
            self.health -= other_colliding_obj.damage
            if self.health <= 0:
                # game_singleton.game.pause()
                pass

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
    def __init__(self, pos, radius=30, direction=PVector(1, 0)):
        Entity.__init__(self, pos, radius, direction)
        self.speed = 3
        Enemy.enemies.append(self)

    def draw(self):
        fill(255, 0, 0)
        circle(self.pos.x, self.pos.y, self.radius*2)

    def process(self):
        self.direction = (game_singleton.game.player.pos - self.pos).normalize()
        Entity.process(self)

    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Projectile):
            self.health -= other_colliding_obj.damage
            if self.health <= 0:
                Enemy.enemies.remove(self)


class ShootingEnemy(Enemy):
    shotgun_projectile_num = 3
    radial_projectile_num = 5

    def __init__(self, pos, motion_type="static", shooting_type="single", radius=30, direction=PVector(1, 0)):
        """
        motion_type = "static" | "moving"
        shooting_type = "single" | "shotgun" | "radial"
        """
        Enemy.__init__(self, pos, radius, direction)
        if motion_type == "static":
            self.speed = 0
        self.shooting_type = shooting_type
        game_singleton.game.create_timer(1, self.on_timer)

    def on_timer(self):
        if not (self in Enemy.enemies): return

        if self.shooting_type == "single":
            self.shoot((game_singleton.game.player.pos - self.pos).normalize(), projectile_type="precise")
        elif self.shooting_type == "shotgun":
            for _ in range(ShootingEnemy.shotgun_projectile_num):
                self.shoot((game_singleton.game.player.pos - self.pos).normalize(), projectile_type="imprecise")
        elif self.shooting_type == "radial":
            main_direction = (game_singleton.game.player.pos - self.pos).normalize()
            angle_step = (2*pi)/ShootingEnemy.radial_projectile_num
            for idx in range(ShootingEnemy.radial_projectile_num):
                self.shoot(main_direction.copy().rotate(angle_step*idx), projectile_type="precise")
        game_singleton.game.create_timer(1, self.on_timer)


class Projectile(Entity):

    projectiles = []
    def __init__(self, pos, parent, direction, radius=8):
        Entity.__init__(self, pos, radius=8, direction=direction)
        self.damage = 5
        self.parent = parent
        self.speed = 15
        Projectile.projectiles.append(self)

    def on_collision(self, other_colliding_obj):
        if not (self.parent is other_colliding_obj):
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
