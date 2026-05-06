import pygame
import sys

from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BLUE,
    WHITE,
    BLACK,
    GREEN,
    RED,
    YELLOW,
    GRAY,
    LIGHT_GRAY,
    GRASS,
    WOOD,
    MAX_ERRORS,
)
from src.menu import Menu
from src.player import Player
from src.product import Product
from src.utils import draw_text, load_image


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Porquinho Brasfeed - Demo 2D")

        self.clock = pygame.time.Clock()

        self.fonts = {
            "title": pygame.font.SysFont("arial", 44, bold=True),
            "subtitle": pygame.font.SysFont("arial", 28, bold=True),
            "normal": pygame.font.SysFont("arial", 21),
            "small": pygame.font.SysFont("arial", 16),
        }

        self.background_image = load_image("fundo_granja.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.menu = Menu(self.screen, self.clock, self.fonts)

    def draw_scenario(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((214, 233, 250))

            pygame.draw.rect(self.screen, GRASS, (0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 90))

            for x in range(0, SCREEN_WIDTH, 80):
                pygame.draw.rect(self.screen, WOOD, (x, SCREEN_HEIGHT - 118, 12, 50))

            pygame.draw.rect(self.screen, WOOD, (0, SCREEN_HEIGHT - 105, SCREEN_WIDTH, 10))

        pygame.draw.rect(self.screen, BLUE, (0, 0, SCREEN_WIDTH, 92))

        draw_text(
            self.screen,
            "PORQUINHO BRASFEED",
            self.fonts["subtitle"],
            WHITE,
            26,
            18
        )

        draw_text(
            self.screen,
            "Coma Brasfeed para crescer. Evite o produto concorrente.",
            self.fonts["normal"],
            WHITE,
            26,
            52
        )

    def draw_hud(self, player):
        panel = pygame.Rect(SCREEN_WIDTH - 310, 16, 280, 58)

        pygame.draw.rect(self.screen, WHITE, panel, border_radius=14)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel, 2, border_radius=14)

        draw_text(
            self.screen,
            f"Crescimento: {player.score}/5",
            self.fonts["small"],
            BLACK,
            panel.x + 18,
            panel.y + 10
        )

        draw_text(
            self.screen,
            f"Doente: {player.errors}/3",
            self.fonts["small"],
            RED,
            panel.x + 18,
            panel.y + 32
        )

        if player.phase == 1:
            phase_name = "LEITAO"
        elif player.phase == 2:
            phase_name = "CRESCENDO"
        else:
            phase_name = "TERMINACAO"

        draw_text(
            self.screen,
            f"Fase: {phase_name}",
            self.fonts["small"],
            BLUE,
            panel.x + 140,
            panel.y + 21
        )

    def final_screen(self, title, message, color):
        while True:
            self.screen.fill(BLUE)

            draw_text(
                self.screen,
                title,
                self.fonts["title"],
                color,
                SCREEN_WIDTH // 2,
                165,
                centered=True
            )

            draw_text(
                self.screen,
                message,
                self.fonts["subtitle"],
                WHITE,
                SCREEN_WIDTH // 2,
                230,
                centered=True
            )

            draw_text(
                self.screen,
                "ENTER - jogar novamente",
                self.fonts["normal"],
                YELLOW,
                SCREEN_WIDTH // 2,
                315,
                centered=True
            )

            draw_text(
                self.screen,
                "ESC - sair",
                self.fonts["normal"],
                WHITE,
                SCREEN_WIDTH // 2,
                350,
                centered=True
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(FPS)

    def play(self):
        player = Player(self.fonts)

        products = [
            Product("brasfeed", self.fonts),
            Product("competitor", self.fonts),
            Product("brasfeed", self.fonts),
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            player.update()

            for product in products:
                product.update()

                if player.rect.colliderect(product.rect):
                    if product.product_type == "brasfeed":
                        player.add_brasfeed()
                    else:
                        player.add_competitor()

                    product.reset()

            self.draw_scenario()
            self.draw_hud(player)

            for product in products:
                product.draw(self.screen)

            player.draw(self.screen)

            draw_text(
                self.screen,
                "Regra: Brasfeed fortalece o animal. Produto concorrente deixa doente.",
                self.fonts["small"],
                GRAY,
                24,
                SCREEN_HEIGHT - 28
            )

            if player.has_won():
                return "win"

            if player.has_lost(MAX_ERRORS):
                return "lose"

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        while True:
            self.menu.show()
            result = self.play()

            if result == "win":
                self.final_screen(
                    "VITORIA!",
                    "O porquinho cresceu ate a terminacao.",
                    GREEN
                )
            else:
                self.final_screen(
                    "DERROTA!",
                    "O porquinho ficou doente com o concorrente.",
                    RED
                )