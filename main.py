import pygame
import pytmx


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.images_rigth = []
        self.index = 0
        self.counter = 0
        for num in range(1, 18):
            img_right = pygame.image.load(f'imagens/boneco/boneco{num}.png')
            self.images_rigth.append(img_right)
        self.image = self.images_rigth[self.index]
        self.rect = self.image.get_frect(center=(window_width / 2, window_height / 2))
        self.direction = pygame.Vector2(1, 0)
        self.speed = 200  # velocidada que o boneco anda
        self.vel_y = 0
        self.pulo = False

    def update(self, dt):
        dx = 0
        dy = 0

        # -- PULO ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.pulo == False and self.rect.bottom == window_height:
            self.vel_y = -20  # altura do pulo
            self.pulo = True

        if not keys[pygame.K_SPACE]:
            self.pulo = False

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        # animation
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.index += 1
            if self.index >= len(self.images_rigth):
                self.index = 0
            self.image = self.images_rigth[self.index]
        if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or self.pulo) == False:
            self.index = 1
            self.image = self.images_rigth[self.index]

        # gravidade
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # update
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
            dy = 0


# class TiledMap:
#     def __init__(self, filename):
#         tm = pytmx.load_pygame(filename, pixelalpha=True)
#         self.width = tm.width * TILE_SIZE
#         self.height = tm.height * TILE_SIZE
#         self.tmxdata = tm
#
#     def render(self, surface):
#         ti = self.tmxdata.get_tile_image_by_gid
#         for layer in self.tmxdata.visible_layers:
#             if isinstance(layer, pytmx.TiledTileLayer):
#                 for x, y, gid in layer:
#                     tile = ti(gid)
#                     if tile:
#                         tile = pg.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
#                         surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
#
#     def make_map(self):
#         temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
#         self.render(temp_surface)
#         return temp_surface


pygame.init()
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('MrJunior01')
running = True
clock = pygame.time.Clock()
fps = 24

# superfície
surf = pygame.Surface((100, 200))
surf.fill('gray')
x = 100

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

# imports
# player_surf = pygame.image.load('gatinho.png').convert_alpha()
# player_rect = player_surf.get_frect(center = (window_width/2, window_height/2))
# player_direction = pygame.math.Vector2(1,0)
# player_speed = 100

while running:
    clock.tick(fps)
    dt = clock.tick(fps) / 1000
    # loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)

    # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
    # if event.type == pygame.MOUSEMOTION:
    #     player_rect.center = event.pos

    # inputs
    # print(pygame.mouse.get_rel())
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # player_direction = player_direction.normalize() if player_direction else player_direction
    # player_rect.center += player_speed * player_direction * dt

    # desenhando o jogo
    display_surface.fill('white')
    all_sprites.draw(display_surface)

    # movimento do jogador
    # player_rect.x += player_direction * 0.4
    # if player_rect.right > window_width or player_rect.left < 0:
    #     player_direction *= -1
    # display_surface.blit(player_surf, player_rect)
    # if player_rect.bottom > window_height or player_rect.top < 0:
    #     player_direction.y *= -1
    # if player_rect.right > window_width or player_rect.left < 0:
    #     player_direction.x *= -1
    #
    # player_rect.center += player_direction * player_speed * dt
    # display_surface.blit(player_surf,player_rect)

    pygame.display.update()

pygame.quit()
