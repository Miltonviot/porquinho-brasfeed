import pygame
import sys

from src.config import (
    SCREEN_WIDTH,
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
                logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, 86))
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
                text="ROI Suinos: tempo parado vira custo, escolha certa vira resultado.",
                font=self.fonts["normal"],
                color=YELLOW,
                x=SCREEN_WIDTH // 2,
                y=168,
                centered=True
            )

            panel = pygame.Rect(145, 210, 670, 240)
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
                text="COMANDOS, ROI E OBJETIVO",
                font=self.fonts["subtitle"],
                color=BLUE,
                x=SCREEN_WIDTH // 2,
                y=246,
                centered=True
            )

            draw_text(
                surface=self.screen,
                text="W A S D ou SETAS - mover o porquinho",
                font=self.fonts["normal"],
                color=BLACK,
                x=205,
                y=288
            )

            draw_text(
                surface=self.screen,
                text="Brasfeed: melhora crescimento, caixa e ROI do lote.",
                font=self.fonts["normal"],
                color=DARK_GREEN,
                x=205,
                y=322
            )

            draw_text(
                surface=self.screen,
                text="Concorrente: causa doenca, atraso e prejuizo.",
                font=self.fonts["normal"],
                color=RED,
                x=205,
                y=356
            )

            draw_text(
                surface=self.screen,
                text="O tempo tambem custa dinheiro: termine rapido com caixa positivo.",
                font=self.fonts["normal"],
                color=BLACK,
                x=205,
                y=390
            )

            draw_text(
                surface=self.screen,
                text="5 Brasfeed = lote terminado | 3 erros ou caixa zerado = derrota",
                font=self.fonts["small"],
                color=BLACK,
                x=205,
                y=422
            )

            button_clicked = draw_button(
                surface=self.screen,
                text="JOGAR",
                font=self.fonts["subtitle"],
                x=365,
                y=475,
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
