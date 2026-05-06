import pygame

from src.config import IMAGES_DIR

# Cache simples para evitar processar a mesma imagem varias vezes.
# Isso e importante no executavel, porque remover fundo pixel a pixel em
# imagens grandes pode deixar o jogo lento ao iniciar a partida.
_IMAGE_CACHE = {}


def remove_light_background(surface, threshold=232, neutral_tolerance=34):
    """
    Remove fundo branco/cinza claro/quadriculado claro de uma imagem.

    A funcao deve ser usada em imagens ja redimensionadas para o tamanho
    final do jogo. Isso evita travamentos no EXE, pois processar imagens
    grandes pixel a pixel e muito custoso.
    """
    image = surface.convert_alpha()
    width, height = image.get_size()

    for x in range(width):
        for y in range(height):
            r, g, b, a = image.get_at((x, y))

            max_rgb = max(r, g, b)
            min_rgb = min(r, g, b)

            is_light = r >= threshold and g >= threshold and b >= threshold
            is_neutral = (max_rgb - min_rgb) <= neutral_tolerance

            if is_light and is_neutral:
                image.set_at((x, y), (255, 255, 255, 0))

    return image


def crop_transparent_borders(surface):
    """
    Recorta bordas transparentes ao redor do sprite.
    """
    rect = surface.get_bounding_rect()

    if rect.width > 0 and rect.height > 0:
        return surface.subsurface(rect).copy()

    return surface


def load_image(filename, size=None, remove_bg=False, crop=True):
    """
    Carrega imagem da pasta assets/images.

    Otimizacao importante:
    - redimensiona antes de remover o fundo claro;
    - guarda em cache a imagem ja processada.

    Isso corrige a demora apos clicar em JOGAR no executavel.
    """
    cache_key = (filename, size, remove_bg, crop)

    if cache_key in _IMAGE_CACHE:
        return _IMAGE_CACHE[cache_key].copy()

    path = IMAGES_DIR / filename

    try:
        image = pygame.image.load(str(path)).convert_alpha()

        # Primeiro redimensiona para o tamanho real usado no jogo.
        # Assim a remocao de fundo trabalha em poucos pixels.
        if size:
            image = pygame.transform.smoothscale(image, size)

        if remove_bg:
            image = remove_light_background(image)

        if crop:
            image = crop_transparent_borders(image)

            # Se o crop mudar muito o tamanho final, reescala para manter
            # hitbox e layout consistentes no jogo.
            if size:
                image = pygame.transform.smoothscale(image, size)

        _IMAGE_CACHE[cache_key] = image.copy()
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
