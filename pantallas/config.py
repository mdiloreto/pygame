import pygame, configuracion as cfg
import modulos.music as music

_fondo = None
_iconos_grandes = False

def main():
    global _fondo, _font_titulo, _titulo_surf, _titulo_rect, _iconos_grandes

    if _fondo is None:
        _fondo = pygame.image.load(cfg.IMG_FONDO_MENU).convert()

    _font_titulo  = pygame.font.Font(cfg.FONT_BOLD_PATH, 80)
    _titulo_surf  = _font_titulo.render("Configuración de volumen", True, cfg.AMARILLO)
    _titulo_rect  = _titulo_surf.get_rect(midtop=(cfg.ANCHO // 2, 30))

    if not _iconos_grandes:
        music.resize_icons(1.8)
        _iconos_grandes = True

    music.init_icon(cfg.ANCHO // 2 + 100, cfg.ALTO // 2) 

def actualizar(dt):
    pass

def manejar_evento(ev):
    # 1.  tecla ESC   →  volver al menú
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
        music.resize_icons(1.0)                 # restaurá tamaño normal
        music.init_icon(cfg.ANCHO, cfg.ALTO)    # esquina inf-der
        return "menu"

    # 2.  clicks sobre los controles de volumen
    music.manejar_evento(ev)
    return "config"

def dibujar(win):
    win.blit(_fondo, (0, 0))
    win.blit(_titulo_surf, _titulo_rect) # título centrado arriba
    music.dibujar_icono(win)  