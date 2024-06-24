import os

from codigos.support import import_folder
from sprites import *  # Certifique-se de que os sprites estejam corretos
from configs import *
from grupos import AllSprites


# Inicializando módulos da classe pygame
class Jogo:
    def __init__(self):
        pygame.init()
        # Músicas usadas no jogo
        # pygame.mixer.music.set_volume(1)  # volume da música (entre 0 e 1)
        # mscFundo = pygame.mixer.music.load(join('Musicas', 'SuperMario.mp3'))
        # pygame.mixer.music.play(-1)  # música repetir pra sempre
        # self.som_Pulo = pygame.mixer.Sound(join('audio', 'pulo_mario.mp3'))
        self.display_surface = pygame.display.set_mode((width, height))  # criando superfície (tela)
        pygame.display.set_caption('MrJunior01')  # Nome da tela
        self.running = True  # boolean para ser usado no loop while
        self.clock = pygame.time.Clock()  # variável a ser usada pra definir o fps

        # Grupos
        self.all_sprites = AllSprites()
        self.collisions = pygame.sprite.Group()

        # Carregar jogo
        self.carregar_assets()
        self.map()

    def carregar_assets(self):
        # graficos

        self.player_frames = import_folder('imagens/boneco')

    def map(self):
        tmx_map = load_pygame(join('data', 'maps', 'mapa.tmx'))

        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x * tile_size, y * tile_size), image, (self.all_sprites, self.collisions ))

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collisions, self.player_frames)

    def run(self):
        while self.running:
            dt = self.clock.tick(fps) / 1000.0  # Corrigir divisão para obter float
            # Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Update
            self.all_sprites.update(dt)  # Mudança de sprite baseada no fps do jogo

            # Desenhando o jogo
            self.display_surface.fill(background)
            # self.display_surface.blit(self.imgFundo, (-75, -75))  # Adaptando para pegar o fundo
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.run()
