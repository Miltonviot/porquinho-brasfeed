from pathlib import Path
import sys

# ============================================================
# CAMINHO BASE PORTAVEL
# ============================================================


def get_base_dir():
    """
    Retorna a pasta base do jogo.

    No VS Code / Python:
        usa a raiz do projeto.

    No executavel PyInstaller:
        usa a pasta onde esta o PorquinhoBrasfeed.exe.

    Isso permite entregar apenas:
        PorquinhoBrasfeed.exe
        assets/
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()

# ============================================================
# CAMINHOS DOS ASSETS
# ============================================================

ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"

# ============================================================
# JANELA
# ============================================================

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 580
FPS = 60

GAME_TITLE = "Porquinho Brasfeed - ROI Suinos"

# ============================================================
# REGRAS DO JOGO
# ============================================================

WIN_SCORE = 5
MAX_ERRORS = 3

PRODUCT_COUNT = 3

PLAYER_SPEED = 6
PRODUCT_MIN_SPEED = 2
PRODUCT_MAX_SPEED = 5

# ============================================================
# ECONOMIA / ROI DA GAMEPLAY
# ============================================================

# Valores simplificados para deixar o conceito de ROI claro na gameplay:
# - tempo parado consome margem;
# - Brasfeed melhora desempenho, saude e caixa;
# - concorrente gera doenca, atraso e prejuizo.
INITIAL_MONEY = 1000.0
MONEY_GAIN_BRASFEED = 220.0
MONEY_LOSS_COMPETITOR = 280.0
MONEY_LOSS_PER_SECOND = 4.0

INITIAL_HEALTH = 100.0
HEALTH_GAIN_BRASFEED = 10.0
HEALTH_LOSS_COMPETITOR = 32.0
HEALTH_LOSS_PER_SECOND = 0.12

# ============================================================
# TAMANHOS DOS ASSETS
# ============================================================

LOGO_SIZE = (300, 120)
BACKGROUND_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PIGLET_SIZE = (115, 90)
PIG_GROWING_SIZE = (145, 110)
PIG_BIG_SIZE = (180, 132)

PRODUCT_SIZE = (82, 82)

# ============================================================
# CORES
# ============================================================

WHITE = (248, 250, 252)
BLACK = (20, 24, 33)

BLUE = (18, 67, 124)
LIGHT_BLUE = (38, 119, 204)
DARK_BLUE = (9, 39, 82)

GREEN = (34, 160, 91)
DARK_GREEN = (20, 108, 61)

YELLOW = (250, 196, 55)
ORANGE = (238, 141, 42)

RED = (218, 55, 60)
DARK_RED = (140, 35, 40)

PINK = (242, 139, 174)

GRAY = (90, 98, 110)
DARK_GRAY = (45, 52, 62)
LIGHT_GRAY = (225, 231, 240)

BACKGROUND = (235, 241, 247)
GRASS = (187, 219, 145)
WOOD = (166, 112, 68)

TRANSPARENT_BLACK = (0, 0, 0, 120)
