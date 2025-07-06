import pygame, sys
import configuracion as cfg
from pantallas import menu, pregunta, top10    # irás añadiendo más (gameover, etc.)

pygame.init()
pygame.display.set_caption(cfg.TITULO_VENTANA)
pantalla = pygame.display.set_mode(cfg.SIZE)
icono_sur = pygame.image.load(cfg.ICONO)
icono = pygame.display.set_icon(icono_sur)
reloj    = pygame.time.Clock()

estado  = 'menu'
modulos = {                
    'menu':     menu,
    'pregunta': pregunta,
    'top10': top10
}

modulos[estado].reset()

while True:
    dt = reloj.tick(cfg.FPS)

    # Eventos 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        siguiente = modulos[estado].manejar_evento(ev)
        if siguiente != estado:
            estado = siguiente
            modulos[estado].reset()

    # Lógica + Dibujo 
    modulos[estado].actualizar(dt)
    modulos[estado].dibujar(pantalla)
    pygame.display.update()
