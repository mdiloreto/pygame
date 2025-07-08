import pygame, sys
import configuracion as cfg
import modulos.music as music
from pantallas import menu, pregunta, top10, game_over, config


pygame.init()
music.play_music()
pygame.display.set_caption(cfg.TITULO_VENTANA)
pantalla = pygame.display.set_mode(cfg.SIZE)
icono_sur = pygame.image.load(cfg.ICONO) #Icono 
icono = pygame.display.set_icon(icono_sur) # Apply del icono 
reloj    = pygame.time.Clock()

pantalla_actual  = 'menu'
pantallas = {
    'menu':      menu,
    'pregunta':  pregunta,
    'top10':     top10,
    'config':    config,
    'game_over': game_over
    
}

# inicializar la plantalla 'menu' al empezar el juego 
pantallas[pantalla_actual].loop_principal()

while True:
    dt = reloj.tick(cfg.FPS)

    # Eventos 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        music.manejar_evento(ev)
        siguiente = pantallas[pantalla_actual].manejar_evento(ev)
        if siguiente != pantalla_actual:
            pantalla_actual = siguiente
            pantallas[pantalla_actual].loop_principal()

    # Lógica + Dibujo 
    pantallas[pantalla_actual].actualizar(dt)
    pantallas[pantalla_actual].dibujar(pantalla)
    music.dibujar_icono(pantalla)
    pygame.display.update()
