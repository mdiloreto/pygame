import pygame.mixer as mixer
import pygame
import configuracion as cfg

# Inicialización de pygame y mixer. 
pygame.font.init() 
mixer.init()

# Constantes
FONT = pygame.font.Font('recursos/fuentes/Symbola.ttf', 48)
MUSIC_ON  = FONT.render("🔊", True, (255,255,255))
MUSIC_OFF = FONT.render("🔇", True, (255,255,255))
MUSIC_DOWN = FONT.render("➖", True, (255,255,255))
MUSIC_UP = FONT.render("➕", True, (255,255,255))
ANCHO = cfg.ANCHO
ALTO = cfg.ALTO
RECT_MUTE  = MUSIC_ON.get_rect()
RECT_UP = MUSIC_UP.get_rect()
RECT_DOWN = MUSIC_DOWN.get_rect()

muteado = False
vol = 0

# Efectos de sonido

def sonido_correcto():
    sonido = mixer.Sound('recursos/sonidos/correct.wav')
    sonido.set_volume(0.2)
    return sonido

def sonido_error():
    sonido = mixer.Sound('recursos/sonidos/wrong.mp3')
    sonido.set_volume(0.2)
    return sonido

def sonido_click():
    sonido = mixer.Sound('recursos/sonidos/click.mp3')
    sonido.set_volume(0.2)
    return sonido

def sonido_gameover():
    sonido = mixer.Sound('recursos/sonidos/game_over.mp3')
    sonido.set_volume(0.2)
    return sonido

def sonido_click_off():
    sonido = mixer.Sound('recursos/sonidos/click_off.mp3')
    sonido.set_volume(0.2)
    return sonido

# Musica del juego

def play_music():
    mixer.music.load("recursos/sonidos/Gala - Freed From Desire (1996).mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play(-1) # loop infinito

def stop_music():
    mixer.music.stop()

    # Volumen de la musica del juego
def set_volume(new):
    """Setea el volumen de la musica.

    Args:
        new (_type_): nuevo valor del volumen
    """
    global vol
    vol = max(0.0, min(new, 1.0))  
    mixer.music.set_volume(vol)

# Renderización de las visuales 
    # Inizialización de los iconos 
def init_icon(ancho, alto, margen=20):
    """Llamar una vez (después de crear la ventana) para fijar la posición."""
    RECT_MUTE.bottomright = (ancho - margen, alto - margen)
    RECT_UP.bottomright =  (RECT_MUTE.left- 10, alto - margen)
    RECT_DOWN.bottomright =  (RECT_UP.left - 10, alto - margen)
    
    #Dibujar los iconos
def dibujar_icono(win):
    """ swichea 🔊/🔇 ."""
    win.blit(MUSIC_OFF if muteado else MUSIC_ON, RECT_MUTE)
    win.blit(MUSIC_UP, RECT_UP)
    win.blit(MUSIC_DOWN, RECT_DOWN)
    
    # Manejo de eventos 
def manejar_evento(ev):
    """Manejador de eventos. 

    Args:
        ev (_type_): ingresa el evento de pygame del loop principal.
    """
    global muteado, vol
    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        if RECT_MUTE.collidepoint(ev.pos):
            muteado = not muteado
            if muteado:
                sonido_click().play()
                mixer.music.pause()
            else:
                sonido_click().play()
                mixer.music.unpause()
        elif RECT_UP.collidepoint(ev.pos):
            sonido_click().play
            set_volume(vol + 0.1)
        elif RECT_DOWN.collidepoint(ev.pos):
            sonido_click().play
            set_volume(vol - 0.1)

# Función para cambiar el tamaño de los iconos de control de volumen
def resize_icons(factor=1.0):
    """Escala 🔊 ➕ ➖ y mantiene posición."""
    global MUSIC_ON, MUSIC_OFF, MUSIC_UP, MUSIC_DOWN
    global RECT_MUTE, RECT_UP, RECT_DOWN

    # centros actuales
    c_mute  = RECT_MUTE.center
    c_up    = RECT_UP.center
    c_down  = RECT_DOWN.center

    def _scale(surf):
        w, h = surf.get_size()
        return pygame.transform.smoothscale(surf, (int(w*factor), int(h*factor)))

    MUSIC_ON  = _scale(MUSIC_ON)
    MUSIC_OFF = _scale(MUSIC_OFF)
    MUSIC_UP  = _scale(MUSIC_UP)
    MUSIC_DOWN= _scale(MUSIC_DOWN)

    # rectángulos nuevos, mismo centro
    RECT_MUTE  = MUSIC_ON.get_rect(center=c_mute)
    RECT_UP    = MUSIC_UP.get_rect(center=c_up)
    RECT_DOWN  = MUSIC_DOWN.get_rect(center=c_down)