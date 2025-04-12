import os
import pygame
from landing_pad import LandingPadCollection
from player import Player

ROWS = 960
COLUMNS = 576
WIDTH = 50
HEIGHT = 50

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((COLUMNS, ROWS))
        pygame.display.set_caption("Petr Jump Game")

        self.shift = 1
        self.clock = pygame.time.Clock()
        start_row, start_col = ROWS // 2, COLUMNS / 2 - WIDTH / 2
        self.player = Player(start_row, start_col, self.shift)
        self.landing_pads = LandingPadCollection(ROWS, COLUMNS, start_row + HEIGHT, start_col)
        self.player_died = False
        self.running = True

    def processInput(self):
        self.command_right = False
        self.command_left = False
        self.command_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.command_right = True
                elif event.key == pygame.K_LEFT:
                    self.command_left = True
                elif event.key == pygame.K_UP:
                    self.command_up = True

        self.player.process_command(self.command_left, self.command_right, self.command_up)

    def update(self):
        self.landing_pads.scroll(self.shift)
        
        self.player.update_location()
        on_pad = self.landing_pads.is_on_pad(self.player.row + HEIGHT, self.player.col, WIDTH)
        self.player.constant_fall(on_pad)

        if self.player.has_died(ROWS):
            self.player_died = True
            self.running = False

    def draw_landing_pads(self):
        for p in self.landing_pads.get_all():
            pygame.draw.rect(self.window, (0, 0, 255), (p.col, p.row, p.width, 10))

    def draw_player(self):
        pygame.draw.rect(self.window, (255, 0, 0), (self.player.col, self.player.row, WIDTH, HEIGHT))

    def render(self):
        self.window.fill((0, 0, 0))
        self.draw_player()
        self.draw_landing_pads()
        pygame.display.update()

    def game_over(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 70)
        img = font.render('GAME OVER', True, (255, 255, 255))
        self.window.blit(img, (COLUMNS // 4, ROWS // 2))
        pygame.display.update()

        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    break

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

        self.game_over()

        pygame.quit()