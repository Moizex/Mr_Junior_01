import pygame
from configs import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(bottomleft=pos)


class AnimetedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animated(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


class Player(AnimetedSprite):
    # Criando função para os sprites e as variáveis do player
    def __init__(self, pos, groups, collision_sprites, frames):
        #surf = pygame.Surface((40, 20))
        super().__init__(frames, pos, groups)
        self.images_right = []
        self.images_left = []
        self.index = 0

        for num in range(0, 17):
            img_right = pygame.image.load(f'imagens/boneco/{num}.png').convert_alpha()
            self.images_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect(bottomleft=pos)

        # Movimentação e colisão
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 200  # Velocidade que o boneco anda
        self.gravity = 50
        self.direction.y = 0  # Velocidade de pulo e queda
        self.pulo = False
        self.no_chao = False  # Variável para verificar se o player está no chão
        self.facing_right = True

    def move(self, dt):
        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical
        self.direction.y += self.gravity * dt  # Adiciona gravidade
        self.rect.y += self.direction.y
        self.collision('vertical')

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.no_chao:
            self.direction.y = -15  # Altura do pulo
            self.pulo = True  # Limitar pulo infinito

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def verificar_chao(self):
        bottom_rect = pygame.FRect(self.rect.x, self.rect.bottom, self.rect.width, 2)
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(bottom_rect):
                return True
        return False

    def update(self, dt):
        self.no_chao = self.verificar_chao()
        self.input()
        self.move(dt)
        self.animate()

    def animate(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
                self.index = 0
            else:
                self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if keys[pygame.K_LEFT]:
                self.image = self.images_left[self.index]
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.image = self.images_right[self.index]
                self.facing_right = True
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or self.pulo):
            self.index = 1
            self.image = self.images_right[self.index] if self.facing_right else self.images_left[self.index]

# Certifique-se de que as constantes width, height, fps, tile_size, background estejam definidas em configs.py














