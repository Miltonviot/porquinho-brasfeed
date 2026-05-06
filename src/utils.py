import pygame

from src.config import IMAGES_DIR


def load_image(filename, size=None):
    """
    Carrega uma imagem da pasta assets/images.
    Se a imagem não existir ou falhar, retorna None.
    """
    path = IMAGES_DIR / filename

    try:
        image = pygame.image.load(str(path)).convert_alpha()

        if size:
            image = pygame.transform.smoothscale(image, size)

        return image
    except Exception as error:
        print(f"[AVISO] Nao foi possivel carregar imagem: {filename} | {error}")
        return None


def draw_text(surface, text, font, color, x, y, centered=False):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()

    if centered:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(rendered, rect)
    return rect


def draw_button(surface, text, font, x, y, width, height, color, text_color):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    rect = pygame.Rect(x, y, width, height)
    hover = rect.collidepoint(mouse_pos)

    final_color = tuple(min(255, c + 18) for c in color) if hover else color

    pygame.draw.rect(surface, final_color, rect, border_radius=16)
    pygame.draw.rect(surface, text_color, rect, 2, border_radius=16)

    draw_text(
        surface=surface,
        text=text,
        font=font,
        color=text_color,
        x=x + width // 2,
        y=y + height // 2,
        centered=True
    )

    return hover and mouse_pressed


def draw_panel(surface, rect, color, border_color=None, radius=16, border_width=2):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

    if border_color:
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=radius)


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))