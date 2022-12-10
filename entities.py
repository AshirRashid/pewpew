from math import pi
from random import randint

import game_singleton, config


class Entity:

    def __init__(self, pos, radius=10, direction=PVector(0, 0), health=30.0, speed=10):
        self.pos = pos
        self.radius = radius
        self.health = health
        self.speed = speed
        self.direction = direction

        self._init_health = self.health
        self._vel = PVector(0, 0)
        self._prev_non_zero_direction = direction
        self._friction = 0.85

    def check_collision(self, other_colliding_obj):
        return (
            self.pos.dist(other_colliding_obj.pos)
            <= self.radius + other_colliding_obj.radius
            )

    def keep_bounded(self):
        new_pos = PVector(
            min(max(self.radius, self.pos.x), config.RES.x - self.radius),
            min(max(self.radius, self.pos.y), config.RES.y - self.radius)
        )
        if self.pos != new_pos:
            self.on_boundary_exit()
        self.pos = new_pos

    def process(self):
        if self.direction.magSq() == 0:
            self._vel *= self._friction
            if self._vel.magSq() < 1:
                self._vel.set(0, 0)
        else:
            self._prev_non_zero_direction = self.direction
            self._vel = self.speed * self.direction
        self.pos += self._vel
        self.keep_bounded()

    def on_boundary_exit(self):
        pass

    def draw(self):
        raise NotImplementedError()
    
    def on_collision(self, other_colliding_obj):
        raise NotImplementedError()

    def shoot(self, projectile_direction=None, projectile_type="imprecise"):
        """projectile_type = "precise" | "imprecise" """
        if not projectile_direction:
            projectile_direction = self._prev_non_zero_direction
        projectile_pos = self.pos + (self.radius + Projectile.radius + 3) * projectile_direction
        if projectile_type == "imprecise":
            projectile_direction = projectile_direction.copy().rotate(randint(-20, 20)/100.0)
        Projectile(
            projectile_pos,
            self,
            projectile_direction,
        )

class Player(Entity):
    
    def __init__(self, pos):
        Entity.__init__(self, pos, radius=20)
        self.frozen = False
        self.is_ready_to_shoot = True
        self.knock_back_speed = 30
        self.frozen_friction = 0.65

    def draw(self):
        noStroke()
        fill(0, 255, 0)
        circle(self.pos.x, self.pos.y, (self.health / self._init_health) * self.radius * 2)
        stroke(0)
        noFill()
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
            elif input_keyCode == config.MOUSE:
                self.shoot((PVector(mouseX, mouseY) - self.pos).normalize())
        self.direction.normalize()

    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Enemy):
            self._vel = (self.pos - other_colliding_obj.pos).normalize()*self.knock_back_speed
            self.frozen = True
        elif isinstance(other_colliding_obj, Projectile):
            self.health -= other_colliding_obj.damage
            if self.health <= 0:
                game_singleton.game.on_player_lost()

    def shoot(self, projectile_direction=None):
        if self.is_ready_to_shoot:
            Entity.shoot(self, projectile_direction)
            self.is_ready_to_shoot = False
            def __(): self.is_ready_to_shoot = True
            game_singleton.game.create_timer(0.1, __)

    def process(self):
        is_dir_0 = self.direction.magSq() == 0
        if not is_dir_0:
            self._prev_non_zero_direction = self.direction
        if self.frozen or is_dir_0:
            self._vel *= self._friction if not self.frozen else self.frozen_friction
            if self._vel.magSq() < 1:
                self.frozen = False
                self._vel.set(0, 0)
        elif not self.frozen:
            self._vel = self.speed * self.direction
        self.pos += self._vel
        self.keep_bounded()


class Enemy(Entity):

    enemies = set()
    def __init__(self, pos, radius=20, direction=PVector(1, 0)):
        Entity.__init__(self, pos, radius, direction)
        self.speed = 3
        Enemy.enemies.add(self)

    def draw(self):
        noStroke()
        fill(255, 0, 0)
        circle(self.pos.x, self.pos.y, (self.health / self._init_health) * self.radius * 2)
        stroke(0)
        noFill()
        circle(self.pos.x, self.pos.y, self.radius*2)

    def process(self):
        self.direction = (game_singleton.game.player.pos - self.pos).normalize()
        Entity.process(self)

    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Projectile):
            self.health -= other_colliding_obj.damage
            if self.health <= 0:
                Enemy.enemies.discard(self)


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

        def create_shooting_timer():
            game_singleton.game.create_timer(1, self.on_timer)

        if game_singleton.game.is_paused():
            game_singleton.game.on_unpause_callbacks.append(create_shooting_timer)
        else:
            create_shooting_timer()

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

    projectiles = set()
    radius = 5
    def __init__(self, pos, parent, direction):
        Entity.__init__(self, pos, radius=Projectile.radius, direction=direction, speed=15)
        self.damage = 5
        self.parent = parent
        Projectile.projectiles.add(self)

    def on_collision(self, other_colliding_obj):
        if not (self.parent is other_colliding_obj):
            Projectile.projectiles.discard(self)

    def draw(self):
        fill(20)
        noStroke()
        circle(self.pos.x, self.pos.y, self.radius*2)

    def on_boundary_exit(self):
        Projectile.projectiles.discard(self)

class Pickup(Entity):

    pickups = set()
    def __init__(self, pos, radius=15, direction=PVector(1, 0)):
        Entity.__init__(self, pos, radius, direction)
        self.speed = 0
        Pickup.pickups.add(self)

    def draw(self):
        stroke(0)
        fill(255, 255, 0)
        circle(self.pos.x, self.pos.y, self.radius*2)

    def on_collision(self, other_colliding_obj):
        if isinstance(other_colliding_obj, Player):
            Pickup.pickups.discard(self)
