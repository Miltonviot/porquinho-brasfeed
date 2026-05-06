import pygame
import sys

from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLUE,
    DARK_BLUE,
    WHITE,
    YELLOW,
    BLACK,
    GREEN,
    DARK_GREEN,
    RED,
    LIGHT_GRAY,
    LOGO_SIZE,
)
from src.utils import draw_text, draw_button, draw_panel, load_image


class Menu:
    def __init__(self, screen, clock, fonts):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts

        self.logo = load_image("logo_brasfeed.png", LOGO_SIZE, remove_bg=True)

    def show(self):
        while True:
            self.screen.fill(BLUE)

            # Faixa superior escura
            pygame.draw.rect(self.screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, 180))

            if self.logo:
                logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, 92))
                self.screen.blit(self.logo, logo_rect)
            else:
                draw_text(
                    surface=self.screen,
                    text="PORQUINHO BRASFEED",
                    font=self.fonts["title"],
                    color=WHITE,
                    x=SCREEN_WIDTH // 2,
                    y=82,
                    centered=True
                )

            draw_text(
                surface=self.screen,
                text="Demo 2D em Python + Pygame",
                font=self.fonts["normal"],
                color=YELLOW,
                x=SCREEN_WIDTH // 2,
                y=168,
                centered=True
            )

            panel = pygame.Rect(170, 215, 620, 220)
            draw_panel(
                surface=self.screen,
                rect=panel,
                color=WHITE,
                border_color=LIGHT_GRAY,
                radius=20,
                border_width=2
            )

            draw_text(
                surface=self.screen,
                text="COMANDOS E OBJETIVO",
                font=self.fonts["subtitle"],
                color=BLUE,
                x=SCREEN_WIDTH // 2,
                y=250,
                centered=True
            )

            draw_text(
                surface=self.screen,
                text="W A S D ou SETAS - mover o porquinho",
                font=self.fonts["normal"],
                color=BLACK,
                x=230,
                y=292
            )

            draw_text(
                surface=self.screen,
                text="Coma produtos BRASFEED para crescer.",
                font=self.fonts["normal"],
                color=DARK_GREEN,
                x=230,
                y=326
            )

            draw_text(
                surface=self.screen,
                text="Evite produtos do concorrente para nao adoecer.",
                font=self.fonts["normal"],
                color=RED,
                x=230,
                y=360
            )

            draw_text(
                surface=self.screen,
                text="5 Brasfeed = vitoria | 3 concorrentes = derrota",
                font=self.fonts["normal"],
                color=BLACK,
                x=230,
                y=394
            )

            button_clicked = draw_button(
                surface=self.screen,
                text="JOGAR",
                font=self.fonts["subtitle"],
                x=365,
                y=470,
                width=230,
                height=58,
                color=GREEN,
                text_color=WHITE
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