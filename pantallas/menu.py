import pygame, configuracion as cfg
import modulos.music as music

# Estos objetos se crean una vez y viven en el módulo
_fondo = None
_font  = None
_btn_jugar_rect = pygame.Rect(540, 200, 200, 80)
_btn_top10_rect  = _btn_jugar_rect.copy().move(0, 120)  # lo bajo 120 px
_btn_config_rect = _btn_top10_rect.copy().move(0, 120)  # lo bajo 120 px + 120 px


def main():
    global _fondo, _font
    if _fondo is None:
        _fondo = pygame.image.load(cfg.IMG_FONDO_MENU).convert()
        _font  = pygame.font.Font(cfg.FONT_BOLD_PATH, 60)
    music.init_icon(cfg.ANCHO, cfg.ALTO)

def manejar_evento(ev):
    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        if _btn_jugar_rect.collidepoint(ev.pos):
            music.sonido_click().play()
            return 'pregunta'
        if _btn_top10_rect.collidepoint(ev.pos):
            music.sonido_click().play()
            return 'top10'
        if _btn_config_rect.collidepoint(ev.pos):
            music.sonido_click().play()
            return 'config'    
    return 'menu'

def actualizar(dt):
    pass  # nada animado aún

def dibujar(win):
    win.blit(_fondo, (0, 0))
    #boton Jugar! 
    pygame.draw.rect(win, cfg.AMARILLO, _btn_jugar_rect,  border_radius=12)
    txt_jugar = _font.render("Jugar!", True, cfg.NEGRO)
    win.blit(txt_jugar, txt_jugar.get_rect(center=_btn_jugar_rect.center))

    # botón Top 10
    pygame.draw.rect(win, cfg.AMARILLO, _btn_top10_rect, border_radius=12)
    txt_top10 = _font.render("Top 10", True, cfg.NEGRO)
    win.blit(txt_top10, txt_top10.get_rect(center=_btn_top10_rect.center))

    # botón config
    pygame.draw.rect(win, cfg.AMARILLO, _btn_config_rect, border_radius=12)
    txt_top10 = _font.render("Config", True, cfg.NEGRO)
    win.blit(txt_top10, txt_top10.get_rect(center=_btn_config_rect.center))
