import pygame, configuracion as cfg

def reset():
    global _font_titulo
    _font_titulo = pygame.font.Font(cfg.FONT_REG_PATH, 48)

def manejar_evento(ev):
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
        return 'menu'
    return 'pregunta'

def actualizar(dt):
    pass

def dibujar(win):
    win.fill(cfg.BLANCO)
    txt = _font_titulo.render("Pantalla de Pregunta (Esc vuelve)", True, cfg.NEGRO)
    win.blit(txt, txt.get_rect(center=(cfg.ANCHO//2, cfg.ALTO//2)))
