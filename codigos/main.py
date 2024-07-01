import os
import sys

import pygame
from codigos.support import *
from sprites import *  # Certifique-se de que os sprites estejam corretos
from configs import *
from grupos import AllSprites
from random import randint
from audio import *


class ManipuladorEntradaTeclado:
    def get_horizontal(self):
        keys = pygame.key.get_pressed()
        return int(keys[pygame.K_d]) - int(keys[pygame.K_a])

    def pulo(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_SPACE]


class ManipuladorEntradaControle:
    def __init__(self, controle):
        self.controle = controle

    def get_horizontal(self):
        eixo_horizontal = self.controle.get_axis(0)
        if eixo_horizontal < -0.1:
            return -1
        elif eixo_horizontal > 0.1:
            return 1
        return 0

    def pulo(self):
        return self.controle.get_button(0)


# Classe para objetos de interação
class InteracaoObjeto(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, dialogo):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill((0, 255, 0))  # Verde para distinguir
        self.rect = self.image.get_rect(topleft=pos)
        self.dialogo = dialogo
        self.mostrar_dialogo = False

    def ativar_dialogo(self):
        self.mostrar_dialogo = True

    def desativar_dialogo(self):
        self.mostrar_dialogo = False


# Inicializando módulos da classe pygame
class Jogo:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.controle = pygame.joystick.Joystick(0)
            self.controle.init()
            print("Joystick detectado: ", self.controle.get_name())
        else:
            self.controle = None
            print("Nenhum joystick detectado.")

        infoObject = pygame.display.Info()
        self.screen_width = infoObject.current_w
        self.screen_height = infoObject.current_h

        self.display_surface = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.display_surface = pygame.display.set_mode((width, height))  # criando superfície (tela)
        pygame.display.set_caption('Mr. Júnior')  # Nome da tela
        self.running = True  # boolean para ser usado no loop while
        self.clock = pygame.time.Clock()  # variável a ser usada pra definir o fps
        self.player_start_pos = None


        # Grupos
        self.all_sprites = AllSprites()
        self.collisions = pygame.sprite.Group()
        self.bala_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()  # Parei aqui
        self.interactive_objects = pygame.sprite.Group()

        # Carregar jogo
        self.carregar_assets()
        self.map()

        self.esqueleto_timer = Timer(1225, func=self.criar_esqueleto,autostart=True, repeat=True)
        self.esqueleto_timer.activate()

        # Defina o estado inicial do jogo
        self.intro_active = True
        self.final_active = False
        self.void_limit = height_void

        self.background_x = 0
        self.background_image = pygame.image.load('imagens/Ambiente/fundo_jogo.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.logo_image = pygame.image.load('imagens/Ambiente/fundo_jogo.jpg').convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, (self.background_image.get_width(), self.background_image.get_height()))
        self.logo_rect = self.logo_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        self.font_big = pygame.font.Font('imagens/letras/Roboto-Regular.ttf', 96)
        self.font_medium = pygame.font.Font('imagens/letras/Roboto-Regular.ttf', 48)
        self.font_small = pygame.font.Font('imagens/letras/Roboto-Regular.ttf', 36)

    def criar_esqueleto(self):
        Esqueleto(frames = self.esqueleto_frames,
                  pos= ((self.level_width + width),(randint(0,self.level_heigth))),
                  groups = (self.all_sprites,self.enemy_sprites),
                  speed= randint(75,125))

    def criar_bala(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bala_surf.get_width()
        Bala(self.bala_surf, (x, pos[1]), direction, (self.all_sprites, self.bala_sprites))
        Fogo(self.fogo_surf, pos,self.all_sprites,self.player)

    def carregar_assets(self):
        # gráficos
        self.player_frames = import_folder('imagens/boneco')
        self.bala_surf = pygame.image.load('imagens/tiro/bala.png').convert_alpha()
        self.fogo_surf = pygame.image.load('imagens/tiro/fogo.png').convert_alpha()
        self.olho_frames = import_folder('imagens/inimigos/olho')
        self.esqueleto_frames = import_folder('imagens/inimigos/esqueleto')

        # sons usar depois
        # self.audio = audio_importer('audio')
        # print(self.audio)
        # self.audio['musicc'].play

        self.background_image = pygame.image.load('imagens/Ambiente/fundo_jogo.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

        # Texto de introdução
        self.fonte = pygame.font.Font('imagens/letras/CyberpunkCraftpixPixel.otf', 24)
        self.texto_intro = [
            "Mr.Junior: Between the chair and the keyboard",
            "",
            "Em um mundo digital repleto de codigos e algoritmos,",
            "nossos herois tecnologicos enfrentam desafios alem das telas.",
            "Conheca os problemas osseos que assolam os programadores,",
            "designers e engenheiros de software, e descubra como prevenir",
            "e aliviar essas dores enquanto avanca pelas fases do jogo.",
            "",
            "Pressione qualquer tecla para continuar..."
        ]

        self.texto_final = ["Sindrome do Tunel do Carpo",
                            "",
                            "Desafio:", "Programadores frequentemente sofrem com", "essa sindrome causando dor",
                            "e formigamento nos punhos e maos.",
                            "Prevencao:",
                            "Use teclados ergonomicos.",
                            "Faca exercicios para os punhos.",
                            "Alivio:",
                            "Fisioterapia e uso de splints.",
                            "Ajude nossos herois a enfrentar esses desafios osseos!",
                            "Lembre-se sempre de consultar um profissional de saude", "para orientacoes especificas."]

    def map(self):
        tmx_map = load_pygame(join('data', 'maps', 'mapa.tmx'))
        self.level_width = tmx_map.width * tile_size
        self.level_heigth = tmx_map.height * tile_size

        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite((x * tile_size, y * tile_size), image, (self.all_sprites, self.collisions))

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                manipulador_entrada = ManipuladorEntradaControle(
                    self.controle) if self.controle else ManipuladorEntradaTeclado()
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collisions, self.player_frames,
                                     manipulador_entrada, self.criar_bala)
                self.player_start_pos = (obj.x, obj.y)
            # if obj.name == 'OLHO':
            #     Olho(self.olho_frames, pygame.FRect(obj.x, obj.y, obj.width, obj.height), self.all_sprites, 1000)

    def collision(self):
        # Colisões entre balas e inimigos
        for bala in self.bala_sprites:
            sprite_collision = pygame.sprite.spritecollide(bala, self.enemy_sprites, True, pygame.sprite.collide_mask)
            if sprite_collision:
                print(f"Bala {bala} colidiu com inimigo(s) {sprite_collision}")
            for enemy_hit in sprite_collision:
                bala.kill()
                enemy_hit.destroy()

        # Verificar colisão com o jogador
        player_hit = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if player_hit:
            self.reiniciar_jogo()
        if self.player.rect.bottom > self.void_limit:
            self.reiniciar_jogo()

    def reiniciar_jogo(self):
        # Reiniciar posição do jogador
        if self.player_start_pos:
            self.player.rect.topleft = self.player_start_pos

        # Reiniciar estado do jogo
        self.intro_active = False
        self.final_active = False
        self.running = True

    def mostrar_intro(self):
        self.display_surface.fill((0, 0, 0))  # Cor de fundo da introdução
        y_offset = height // 2 - len(self.texto_intro) * 10
        for linha in self.texto_intro:
            texto_surface = self.fonte.render(linha, True, (0, 255, 0))
            texto_rect = texto_surface.get_rect(center=(width // 2, y_offset))
            self.display_surface.blit(texto_surface, texto_rect)
            y_offset += 30
        pygame.display.update()

    def mostrar_final(self):
        self.display_surface.fill((0, 0, 0))  # Cor de fundo da tela final
        y_offset = height // 2 - len(self.texto_final) * 10
        for linha in self.texto_final:
            texto_surface = self.fonte.render(linha, True, (0, 255, 0))
            texto_rect = texto_surface.get_rect(center=(width // 2, y_offset))
            self.display_surface.blit(texto_surface, texto_rect)
            y_offset += 30
        pygame.display.update()

    def draw_text(self, text, font, text_color, border_color, surface, x, y):
        text_surface = font.render(text, True, text_color)
        border_surface = font.render(text, True, border_color)

        text_rect = text_surface.get_rect(center=(x, y))
        border_rect = border_surface.get_rect(center=(x, y))

        surface.blit(border_surface, border_rect.move(1, 1))
        surface.blit(border_surface, border_rect.move(-1, 1))
        surface.blit(border_surface, border_rect.move(1, -1))
        surface.blit(border_surface, border_rect.move(-1, -1))

        surface.blit(text_surface, text_rect)

    def draw_button(self, text, font, text_color, bg_color, surface, x, y, width, height, action=None):
        button_rect = pygame.Rect(x - width // 1.15, y - height // 1.15, width, height)

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (255, 255, 255), button_rect, border_radius=15)  # Efeito de hover
        else:
            pygame.draw.rect(surface, bg_color, button_rect, border_radius=15)

        textobj = font.render(text, True, text_color)
        textrect = textobj.get_rect(center=button_rect.center)
        surface.blit(textobj, textrect)

        return button_rect

    def game_start_screen(self):
        self.background_x = 0

        start_button_rect = self.draw_button('Iniciar Jogo', self.font_medium, (128, 0, 128), (255, 255, 153), self.display_surface,
                                             self.screen_width // 2, self.screen_height // 2, 300, 70)

        quit_button_rect = self.draw_button('Sair', self.font_small, (128, 0, 128), (255, 255, 153), self.display_surface,
                                            self.screen_width // 2, self.screen_height // 2 + 100, 200, 50)

        text_x = self.screen_width // 2 - 100
        text_y = self.screen_height // 2 - 150  # Ajustado para posicionar mais acima

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Verifica se é o botão esquerdo do mouse
                        mouse_pos = pygame.mouse.get_pos()
                        if start_button_rect.collidepoint(mouse_pos):
                            print("Iniciar clicado!")
                            running = False
                            self.intro_active = True
                        elif quit_button_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()

            self.background_x -= 1

            if self.background_x <= -self.background_image.get_width():
                self.background_x = 0

            logo_x = self.screen_width // 2 + self.background_x
            self.logo_rect.centerx = logo_x

            self.display_surface.blit(self.background_image, (self.background_x, 0))
            self.display_surface.blit(self.background_image,
                                      (self.background_x + self.background_image.get_width(), 0))
            self.display_surface.blit(self.logo_image, self.logo_rect)

            self.draw_text('Mr. Júnior', self.font_big, (0, 255, 0), (0, 0, 0), self.display_surface, text_x, text_y)

            self.draw_button('Iniciar Jogo', self.font_medium, (0, 255, 0), (0, 0, 0), self.display_surface,
                             self.screen_width // 2, self.screen_height // 2, 300, 70)
            self.draw_button('Sair', self.font_small, (0, 255, 0), (0, 0, 0), self.display_surface,
                             self.screen_width // 2, self.screen_height // 2 + 100, 300, 70)

            pygame.display.flip()

    def run(self):
        self.game_start_screen()

        while self.running:
            dt = self.clock.tick(fps) / 1000.0  # Corrigir divisão para obter float

            if self.intro_active:
                self.mostrar_intro()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type in (pygame.KEYDOWN, pygame.JOYBUTTONDOWN):
                        self.intro_active = False
            elif self.final_active:
                self.mostrar_final()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False  # Sair do jogo após tela final
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                # Lógica para ativar a tela final (exemplo: ao completar o jogo)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F10]:
                    self.final_active = True

                # Update
                self.esqueleto_timer.update()
                self.all_sprites.update(dt)  # Mudança de sprite baseada no fps do jogo
                self.collision()

                # Desenhar o jogo
                self.display_surface.blit(self.background_image, (0, 0))  # Desenhar a imagem de fundo
                self.all_sprites.draw(self.player.rect.center)  # Corrigir para passar a posição do jogador

                pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.run()
