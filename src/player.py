import pygame

from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLUE,
    WHITE,
    BLACK,
    PINK,
    WIN_SCORE,
)
from src.utils import load_image, draw_text


class Player:
    def __init__(self, fonts):
        self.fonts = fonts

        self.score = 0
        self.errors = 0
        self.phase = 1
        self.speed = 6
        self.invulnerable_time = 0

        self.images = {
            1: load_image("porco_leitao.png", (95, 75)),
            2: load_image("porco_crescendo.png", (120, 92)),
            3: load_image("porco_grande.png", (155, 115)),
        }

        self.rect = pygame.Rect(80, SCREEN_HEIGHT - 175, 95, 75)

    def update_size(self):
        bottom = self.rect.bottom

        if self.score >= 4:
            self.phase = 3
            self.rect.size = (155, 115)
        elif self.score >= 2:
            self.phase = 2
            self.rect.size = (120, 92)
        else:
            self.phase = 1
            self.rect.size = (95, 75)

        self.rect.bottom = bottom

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.x = max(20, min(SCREEN_WIDTH - self.rect.width - 20, self.rect.x))
        self.rect.y = max(125, min(SCREEN_HEIGHT - self.rect.height - 45, self.rect.y))

    def add_brasfeed(self):
        self.score += 1
        self.update_size()

    def add_competitor(self):
        if self.invulnerable_time <= 0:
            self.errors += 1
            self.invulnerable_time = 90

    def update(self):
        self.move()

        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1

    def draw_fallback(self, surface):
        pygame.draw.ellipse(surface, PINK, self.rect)
        pygame.draw.ellipse(surface, BLACK, self.rect, 2)

        ear_left = pygame.Rect(self.rect.x + 8, self.rect.y - 8, 24, 24)
        ear_right = pygame.Rect(self.rect.right - 34, self.rect.y - 8, 24, 24)

        pygame.draw.ellipse(surface, PINK, ear_left)
        pygame.draw.ellipse(surface, PINK, ear_right)

        eye_left = pygame.Rect(self.rect.x + self.rect.w * 0.32, self.rect.y + self.rect.h * 0.30, 7, 7)
        eye_right = pygame.Rect(self.rect.x + self.rect.w * 0.58, self.rect.y + self.rect.h * 0.30, 7, 7)

        pygame.draw.ellipse(surface, BLACK, eye_left)
        pygame.draw.ellipse(surface, BLACK, eye_right)

        nose = pygame.Rect(self.rect.centerx - 18, self.rect.centery - 4, 36, 22)
        pygame.draw.ellipse(surface, (232, 105, 145), nose)

        draw_text(
            surface,
            str(self.phase),
            self.fonts["small"],
            BLACK,
            self.rect.centerx,
            self.rect.centery + 28,
            centered=True
        )

    def draw(self, surface):
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 >= 5:
            return

        image = self.images.get(self.phase)

        if image:
            surface.blit(image, self.rect)
        else:
            self.draw_fallback(surface)

    def has_won(self):
        return self.score >= WIN_SCORE

    def has_lost(self, max_errors):
        return self.errors >= max_errors