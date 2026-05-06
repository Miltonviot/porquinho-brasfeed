import pygame
import sys

from src.config import (
    SCREEN_WIDTH,
    BLUE,
    WHITE,
    YELLOW,
    BLACK,
    GREEN,
    DARK_GREEN,
    RED,
)
from src.utils import draw_text, draw_button


class Menu:
    def __init__(self, screen, clock, fonts):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts

    def show(self):
        while True:
            self.screen.fill(BLUE)

            draw_text(
                self.screen,
                "PORQUINHO BRASFEED",
                self.fonts["title"],
                WHITE,
                SCREEN_WIDTH // 2,
                90,
                centered=True
            )

            draw_text(
                self.screen,
                "Demo 2D em Python + Pygame",
                self.fonts["subtitle"],
                YELLOW,
                SCREEN_WIDTH // 2,
                138,
                centered=True
            )

            panel = pygame.Rect(185, 190, 590, 215)
            pygame.draw.rect(self.screen, WHITE, panel, border_radius=18)

            draw_text(
                self.screen,
                "COMANDOS",
                self.fonts["subtitle"],
                BLUE,
                SCREEN_WIDTH // 2,
                225,
                centered=True
            )

            draw_text(
                self.screen,
                "W A S D ou SETAS - mover o porquinho",
                self.fonts["normal"],
                BLACK,
                245,
                270
            )

            draw_text(
                self.screen,
                "Coma produtos BRASFEED para crescer.",
                self.fonts["normal"],
                DARK_GREEN,
                245,
                306
            )

            draw_text(
                self.screen,
                "Evite produtos do concorrente para nao adoecer.",
                self.fonts["normal"],
                RED,
                245,
                342
            )

            draw_text(
                self.screen,
                "5 Brasfeed = vitoria | 3 concorrentes = derrota",
                self.fonts["normal"],
                BLACK,
                245,
                378
            )

            button_clicked = draw_button(
                self.screen,
                "JOGAR",
                self.fonts["subtitle"],
                365,
                445,
                230,
                58,
                GREEN,
                WHITE
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONUP and button_clicked:
                    return

            pygame.display.flip()
            self.clock.tick(60)