from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"

# Janela
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 580
FPS = 60

# Jogo
WIN_SCORE = 5
MAX_ERRORS = 3

# Cores
WHITE = (248, 250, 252)
BLACK = (20, 24, 33)
BLUE = (18, 67, 124)
LIGHT_BLUE = (38, 119, 204)
GREEN = (34, 160, 91)
DARK_GREEN = (20, 108, 61)
YELLOW = (250, 196, 55)
RED = (218, 55, 60)
PINK = (242, 139, 174)
GRAY = (90, 98, 110)
LIGHT_GRAY = (225, 231, 240)
BACKGROUND = (235, 241, 247)
GRASS = (187, 219, 145)
WOOD = (166, 112, 68)