import pygame

from codigo.configs import *


# import pytmx
# Criando Classe do Player
class Player(pygame.sprite.Sprite):
    # Criando função para os sprites e as variávies do player
    def __init__(self, groups):
        super().__init__(groups)
        self.images_rigth = []  # Lista de sprites
        self.index = 0  # Escolher número do sprite
        # self.counter = 0 VÁRIAVEL DECLARADA E NÃO USADA
        for num in range(1, 18):  # Loop para a mudança de imagens da lista
            img_right = pygame.image.load(f'imagens/boneco/boneco{num}.png')
            self.images_rigth.append(img_right)  # append = acrescentar
        self.image = self.images_rigth[self.index]  # frame atual (??)
        self.rect = self.image.get_frect(center=(width / 2, height / 2))
        self.direction = pygame.Vector2(1, 0)
        self.speed = 200  # velocidada que o boneco anda
        self.vel_y = 0  # Velocidade de pulo e queda
        self.pulo = False

    def update(self, dt):
        dx = 0  # DeltaX
        dy = 0  # DeltaY

        # -- PULO ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.pulo == False and self.rect.bottom == height:
            # somPulo.play()#chamando som do pulo
            self.vel_y = -20  # altura do pulo
            self.pulo = True  # limitar pulo infinito

        if not keys[pygame.K_SPACE]:
            self.pulo = False  # limitar pulo infinito

        # Movimentação
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt

        # animation
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.index += 1  # mudança de sprite, atualizando número da lista
            if self.index >= len(self.images_rigth):
                self.index = 0  # resetando index pra voltar o sprite
            self.image = self.images_rigth[self.index]
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or self.pulo):
            self.index = 1  # sprite inicial ao ficar parado
            self.image = self.images_rigth[self.index]

        # gravidade
        self.vel_y += 1  # aceleração de queda
        if self.vel_y > 10:  # velocidade máxima que ele cai
            self.vel_y = 10
        dy += self.vel_y

        # update
        self.rect.x += dx
        self.rect.y += dy

        # colisão com a parte de baixo da tela
        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

# iniciando módulos da classe pygame
pygame.init()

# Músicas usadas no jogo
# pygame.mixer.music.set_volume(1) #volume da musica (entre 0 e 1)
# mscFundo = pygame.mixer.music.load(f'Musicas\SuperMario.mp3')
# pygame.mixer.music.play(-1)#musica repetir pra sempre
#
# somPulo = pygame.mixer.Sound(f'Musicas\PuloMario.wav')
display_surface = pygame.display.set_mode((width, height))  # criando superfície(tela)
pygame.display.set_caption('MrJunior01')  # Nome da tela
running = True  # boolean para ser usado no loop while
clock = pygame.time.Clock()  #variável a ser usada pra definir o fps

#Imagem de fundo
imgFundo = pygame.image.load(f'imagens/Ambiente/ImagemFundo.png')
imgFundo = pygame.transform.scale(imgFundo, [width + 100, height + 100])
#tamanho ta maior pq png nao preenche fundo todo ai to adaptando

# superfície
surf = pygame.Surface((100, 200))
surf.fill('gray')  # cor da superficie
x = 100

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

while running:
    clock.tick(fps)
    dt = clock.tick(fps) / 1000
    # loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)  # mudança de sprite baseado no fps do jogo
    # desenhando o jogo
    display_surface.blit(imgFundo, (-50, -50))  #adaptando pra pegar o fundo
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
