import pygame

from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    WIN_SCORE,
    MAX_ERRORS,
    INITIAL_MONEY,
    MONEY_GAIN_BRASFEED,
    MONEY_LOSS_COMPETITOR,
    MONEY_LOSS_PER_SECOND,
    INITIAL_HEALTH,
    HEALTH_GAIN_BRASFEED,
    HEALTH_LOSS_COMPETITOR,
    HEALTH_LOSS_PER_SECOND,
    BLACK,
    PINK,
    PIGLET_SIZE,
    PIG_GROWING_SIZE,
    PIG_BIG_SIZE,
)
from src.utils import load_image, draw_text, clamp


class Player:
    def __init__(self, fonts):
        self.fonts = fonts

        self.score = 0
        self.errors = 0
        self.phase = 1

        self.money = INITIAL_MONEY
        self.initial_money = INITIAL_MONEY
        self.health = INITIAL_HEALTH
        self.elapsed_seconds = 0.0
        self._time_accumulator_ms = 0

        self.last_event_text = "Gestao do lote iniciada. Busque Brasfeed para melhorar o ROI."
        self.last_event_timer = 180

        self.speed = PLAYER_SPEED
        self.invulnerable_time = 0

        self.images = {
            1: load_image("porco_leitao.png", PIGLET_SIZE, remove_bg=True),
            2: load_image("porco_crescendo.png", PIG_GROWING_SIZE, remove_bg=True),
            3: load_image("porco_grande.png", PIG_BIG_SIZE, remove_bg=True),
        }

        self.rect = pygame.Rect(80, SCREEN_HEIGHT - 160, *PIGLET_SIZE)
        self.rect.bottom = SCREEN_HEIGHT - 45

    def update_size(self):
        old_center = self.rect.center
        old_bottom = self.rect.bottom

        if self.score >= 4:
            self.phase = 3
            self.rect.size = PIG_BIG_SIZE
        elif self.score >= 2:
            self.phase = 2
            self.rect.size = PIG_GROWING_SIZE
        else:
            self.phase = 1
            self.rect.size = PIGLET_SIZE

        self.rect.center = old_center
        self.rect.bottom = old_bottom

        self.rect.x = clamp(self.rect.x, 20, SCREEN_WIDTH - self.rect.width - 20)
        self.rect.y = clamp(self.rect.y, 120, SCREEN_HEIGHT - self.rect.height - 35)

    def move(self):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = clamp(self.rect.x, 20, SCREEN_WIDTH - self.rect.width - 20)
        self.rect.y = clamp(self.rect.y, 120, SCREEN_HEIGHT - self.rect.height - 35)

    def set_event_text(self, text):
        self.last_event_text = text
        self.last_event_timer = 210

    def add_brasfeed(self):
        self.score += 1
        self.money += MONEY_GAIN_BRASFEED
        self.health = clamp(self.health + HEALTH_GAIN_BRASFEED, 0, INITIAL_HEALTH)
        self.set_event_text("Brasfeed: +crescimento, +saude e +caixa do lote.")
        self.update_size()

    def add_competitor(self):
        if self.invulnerable_time <= 0:
            self.errors += 1
            self.money -= MONEY_LOSS_COMPETITOR
            self.health = clamp(self.health - HEALTH_LOSS_COMPETITOR, 0, INITIAL_HEALTH)
            self.set_event_text("Concorrente: doenca, atraso e prejuizo na margem.")
            self.invulnerable_time = 90

    def update_economy(self, delta_ms):
        self._time_accumulator_ms += delta_ms

        while self._time_accumulator_ms >= 1000:
            self._time_accumulator_ms -= 1000
            self.elapsed_seconds += 1
            self.money -= MONEY_LOSS_PER_SECOND
            self.health = clamp(self.health - HEALTH_LOSS_PER_SECOND, 0, INITIAL_HEALTH)

    def update(self, delta_ms=0):
        self.move()
        self.update_economy(delta_ms)

        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1

        if self.last_event_timer > 0:
            self.last_event_timer -= 1

    def draw_fallback(self, surface):
        pygame.draw.ellipse(surface, PINK, self.rect)
        pygame.draw.ellipse(surface, BLACK, self.rect, 2)

        ear_left = pygame.Rect(self.rect.x + 8, self.rect.y - 8, 24, 24)
        ear_right = pygame.Rect(self.rect.right - 34, self.rect.y - 8, 24, 24)

        pygame.draw.ellipse(surface, PINK, ear_left)
        pygame.draw.ellipse(surface, PINK, ear_right)

        eye_left = pygame.Rect(
            int(self.rect.x + self.rect.w * 0.34),
            int(self.rect.y + self.rect.h * 0.30),
            7,
            7
        )
        eye_right = pygame.Rect(
            int(self.rect.x + self.rect.w * 0.58),
            int(self.rect.y + self.rect.h * 0.30),
            7,
            7
        )

        pygame.draw.ellipse(surface, BLACK, eye_left)
        pygame.draw.ellipse(surface, BLACK, eye_right)

        nose = pygame.Rect(self.rect.centerx - 18, self.rect.centery - 4, 36, 22)
        pygame.draw.ellipse(surface, (232, 105, 145), nose)

        draw_text(
            surface=surface,
            text=str(self.phase),
            font=self.fonts["small"],
            color=BLACK,
            x=self.rect.centerx,
            y=self.rect.centery + 28,
            centered=True
        )

    def draw(self, surface):
        # Efeito de piscar quando come concorrente.
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 >= 5:
            return

        image = self.images.get(self.phase)

        if image:
            surface.blit(image, self.rect)
        else:
            self.draw_fallback(surface)

    def get_phase_name(self):
        if self.phase == 1:
            return "LEITAO"
        if self.phase == 2:
            return "CRESCIMENTO"
        return "TERMINACAO"

    def get_roi_percent(self):
        return int(((self.money - self.initial_money) / self.initial_money) * 100)

    def get_money_text(self):
        value = max(0, int(self.money))
        return f"R$ {value:,}".replace(",", ".")

    def get_health_percent(self):
        return int(clamp(self.health, 0, INITIAL_HEALTH))

    def get_time_text(self):
        return f"{int(self.elapsed_seconds)}s"

    def has_won(self):
        return self.score >= WIN_SCORE and self.money > 0 and self.health > 0

    def has_lost(self, max_errors=MAX_ERRORS):
        return self.errors >= max_errors or self.money <= 0 or self.health <= 0
