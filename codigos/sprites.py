from random import randint

import pygame

from codigos.timer import *
from configs import *
from math import sin


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(bottomleft=pos)


class Bala(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        #ajuste
        self.image = pygame.transform.flip(self.image, direction == -1, False)

        # movimentação
        self.direction = direction
        self.speed = 600

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fogo(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos,surf,groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart= True, func= self.kill)
        self.y_offset = pygame.Vector2(0,8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True,False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self,_):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class AnimetedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animated(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Inimigo(AnimetedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func = self.kill)

    def destroy(self):
        self.kill()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        if not self.death_timer:
            self.move(dt)
            self.animated(dt)
        self.constraint()

class Esqueleto(Inimigo):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(500,600)
        self.frequency = randint(300,600)


    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.right <= 0:
            self.kill()

class Olho(Inimigo):
    def __init__(self, frames, rect, groups, speed):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = randint(160,180)
        self.direction = 1


    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt


    def constraint(self):
        if not self.main_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]

class Player(AnimetedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, manipulador_entrada, criar_bala):
        super().__init__(frames, pos, groups)
        self.flip = False
        self.criar_bala = criar_bala
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 200
        self.gravity = 40
        self.direction.y = 0
        self.pulo = False
        self.no_chao = False
        self.facing_right = True
        self.manipulador_entrada = manipulador_entrada


        # bala time
        self.shoot_timer = Timer(500)

    def get_bala_origem(self):
        if self.flip:
            return self.rect.left, self.rect.centery
        else:
            return self.rect.right, self.rect.centery

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        if self.no_chao:
            self.gravity = 0
        else:
            self.gravity = 40

        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')

    def input(self):
        self.direction.x = self.manipulador_entrada.get_horizontal()
        keys = pygame.key.get_pressed()
        if self.manipulador_entrada.pulo() and self.no_chao:
            self.direction.y = -11
            self.pulo = True

        if keys[pygame.K_h] and not self.shoot_timer:
            bala_origem = self.get_bala_origem()
            self.criar_bala(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def verificar_chao(self):
        bottom_rect = pygame.FRect(self.rect.x, self.rect.bottom, self.rect.width, 2)
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(bottom_rect):
                return True
        return False

    def update(self, dt):
        self.shoot_timer.update()
        self.no_chao = self.verificar_chao()
        self.input()
        self.move(dt)
        self.animate(dt)

    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        self.frame_index = 7 if not self.no_chao else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
