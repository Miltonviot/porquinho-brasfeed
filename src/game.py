import pygame
import sys

from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    BLUE,
    DARK_BLUE,
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
    PRODUCT_COUNT,
    BACKGROUND_SIZE,
)
from src.menu import Menu
from src.player import Player
from src.product import Product
from src.utils import draw_text, draw_panel, load_image


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()

        self.fonts = {
            "title": pygame.font.SysFont("arial", 44, bold=True),
            "subtitle": pygame.font.SysFont("arial", 28, bold=True),
            "normal": pygame.font.SysFont("arial", 21),
            "small": pygame.font.SysFont("arial", 16),
            "tiny": pygame.font.SysFont("arial", 13),
        }

        self.background_image = load_image("fundo_granja.png", BACKGROUND_SIZE)
        self.logo_small = load_image("logo_brasfeed.png", (150, 60), remove_bg=True)

        self.menu = Menu(self.screen, self.clock, self.fonts)

    def draw_scenario(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((214, 233, 250))

            pygame.draw.rect(
                self.screen,
                GRASS,
                (0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 90)
            )

            for x in range(0, SCREEN_WIDTH, 80):
                pygame.draw.rect(
                    self.screen,
                    WOOD,
                    (x, SCREEN_HEIGHT - 118, 12, 50)
                )

            pygame.draw.rect(
                self.screen,
                WOOD,
                (0, SCREEN_HEIGHT - 105, SCREEN_WIDTH, 10)
            )

        pygame.draw.rect(self.screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, 92))

        if self.logo_small:
            self.screen.blit(self.logo_small, (18, 15))
            text_x = 185
        else:
            draw_text(
                surface=self.screen,
                text="PORQUINHO BRASFEED",
                font=self.fonts["subtitle"],
                color=WHITE,
                x=26,
                y=16
            )
            text_x = 26

        draw_text(
            surface=self.screen,
            text="ROI Suinos: Brasfeed melhora o lote. Tempo e concorrente reduzem a margem.",
            font=self.fonts["normal"],
            color=WHITE,
            x=text_x,
            y=32
        )

    def draw_hud(self, player):
        panel = pygame.Rect(SCREEN_WIDTH - 330, 12, 306, 68)

        draw_panel(
            surface=self.screen,
            rect=panel,
            color=WHITE,
            border_color=LIGHT_GRAY,
            radius=14,
            border_width=2
        )

        roi = player.get_roi_percent()
        roi_color = GREEN if roi >= 0 else RED

        draw_text(
            surface=self.screen,
            text=f"ROI: {roi:+d}%",
            font=self.fonts["small"],
            color=roi_color,
            x=panel.x + 16,
            y=panel.y + 8
        )

        draw_text(
            surface=self.screen,
            text=f"Caixa: {player.get_money_text()}",
            font=self.fonts["small"],
            color=BLACK,
            x=panel.x + 16,
            y=panel.y + 31
        )

        draw_text(
            surface=self.screen,
            text=f"Cresc.: {player.score}/5",
            font=self.fonts["small"],
            color=BLACK,
            x=panel.x + 150,
            y=panel.y + 8
        )

        draw_text(
            surface=self.screen,
            text=f"Doenca: {player.errors}/3",
            font=self.fonts["small"],
            color=RED,
            x=panel.x + 150,
            y=panel.y + 31
        )

        draw_text(
            surface=self.screen,
            text=f"Fase: {player.get_phase_name()}",
            font=self.fonts["tiny"],
            color=BLUE,
            x=panel.x + 16,
            y=panel.y + 53
        )

    def draw_footer_hint(self):
        footer = pygame.Rect(18, SCREEN_HEIGHT - 38, SCREEN_WIDTH - 36, 26)

        draw_panel(
            surface=self.screen,
            rect=footer,
            color=WHITE,
            border_color=LIGHT_GRAY,
            radius=12,
            border_width=1
        )

        draw_text(
            surface=self.screen,
            text="Regra: Brasfeed aumenta caixa e crescimento. Concorrente causa doenca e prejuizo. Cada segundo reduz a margem.",
            font=self.fonts["tiny"],
            color=GRAY,
            x=footer.centerx,
            y=footer.centery,
            centered=True
        )

    def final_screen(self, title, message, color, roi=None, money_text=None):
        while True:
            self.screen.fill(BLUE)

            pygame.draw.rect(self.screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, 180))

            if self.logo_small:
                logo_rect = self.logo_small.get_rect(center=(SCREEN_WIDTH // 2, 70))
                self.screen.blit(self.logo_small, logo_rect)

            draw_text(
                surface=self.screen,
                text=title,
                font=self.fonts["title"],
                color=color,
                x=SCREEN_WIDTH // 2,
                y=205,
                centered=True
            )

            draw_text(
                surface=self.screen,
                text=message,
                font=self.fonts["subtitle"],
                color=WHITE,
                x=SCREEN_WIDTH // 2,
                y=262,
                centered=True
            )

            if roi is not None and money_text is not None:
                roi_color = GREEN if roi >= 0 else RED
                draw_text(
                    surface=self.screen,
                    text=f"Resultado economico: ROI {roi:+d}% | Caixa final: {money_text}",
                    font=self.fonts["normal"],
                    color=roi_color,
                    x=SCREEN_WIDTH // 2,
                    y=315,
                    centered=True
                )

            draw_text(
                surface=self.screen,
                text="ENTER - jogar novamente",
                font=self.fonts["normal"],
                color=YELLOW,
                x=SCREEN_WIDTH // 2,
                y=370,
                centered=True
            )

            draw_text(
                surface=self.screen,
                text="ESC - sair",
                font=self.fonts["normal"],
                color=WHITE,
                x=SCREEN_WIDTH // 2,
                y=405,
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

    def create_products(self):
        products = []

        for index in range(PRODUCT_COUNT):
            product_type = "brasfeed" if index % 2 == 0 else "competitor"
            products.append(Product(product_type, self.fonts))

        return products

    def play(self):
        player = Player(self.fonts)
        products = self.create_products()

        while True:
            delta_ms = self.clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            player.update(delta_ms)

            for product in products:
                product.update()

                if player.rect.colliderect(product.rect):
                    if product.product_type == "brasfeed":
                        player.add_brasfeed()
                    else:
                        player.add_competitor()

                    product.reset(start_outside=True)

            self.draw_scenario()
            self.draw_hud(player)

            for product in products:
                product.draw(self.screen)

            player.draw(self.screen)
            self.draw_footer_hint()

            if player.has_won():
                return "win", player.get_roi_percent(), player.get_money_text()

            if player.has_lost(MAX_ERRORS):
                return "lose", player.get_roi_percent(), player.get_money_text()

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        while True:
            self.menu.show()
            result, roi, money_text = self.play()

            if result == "win":
                self.final_screen(
                    title="VITORIA!",
                    message="Lote terminado com ROI positivo.",
                    color=GREEN,
                    roi=roi,
                    money_text=money_text
                )
            else:
                self.final_screen(
                    title="DERROTA!",
                    message="O lote perdeu margem por doenca, atraso ou caixa zerado.",
                    color=RED,
                    roi=roi,
                    money_text=money_text
                )
