import random
import pygame

from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PRODUCT_SIZE,
    PRODUCT_MIN_SPEED,
    PRODUCT_MAX_SPEED,
    GREEN,
    RED,
    WHITE,
)
from src.utils import load_image, draw_text


class Product:
    def __init__(self, product_type, fonts):
        self.fonts = fonts

        self.product_type = product_type
        self.rect = pygame.Rect(0, 0, *PRODUCT_SIZE)
        self.speed = 3

        self.images = {
            "brasfeed": load_image("produto_brasfeed.png", PRODUCT_SIZE, remove_bg=True),
            "competitor": load_image("produto_concorrente.png", PRODUCT_SIZE, remove_bg=True),
        }

        self.reset(start_outside=False)

    def reset(self, start_outside=True):
        self.product_type = random.choice(["brasfeed", "competitor"])

        if start_outside:
            self.rect.x = SCREEN_WIDTH + random.randint(30, 360)
        else:
            self.rect.x = random.randint(320, SCREEN_WIDTH - 100)

        self.rect.y = random.randint(135, SCREEN_HEIGHT - 150)
        self.speed = random.randint(PRODUCT_MIN_SPEED, PRODUCT_MAX_SPEED)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.reset(start_outside=True)

    def draw_fallback(self, surface):
        if self.product_type == "brasfeed":
            color = GREEN
            label = "BF"
        else:
            color = RED
            label = "X"

        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)

        draw_text(
            surface=surface,
            text=label,
            font=self.fonts["subtitle"],
            color=WHITE,
            x=self.rect.centerx,
            y=self.rect.centery,
            centered=True
        )

    def draw(self, surface):
        image = self.images.get(self.product_type)

        if image:
            surface.blit(image, self.rect)
        else:
            self.draw_fallback(surface)