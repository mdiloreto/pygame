import pygame
import configuracion as cfg
import modulos.music as music

#Constantes
FONT = pygame.font.Font('recursos/fuentes/Symbola.ttf', 48)
BOMBA = FONT.render("💣", True, (255, 255, 255))
X2     = FONT.render("✖️2", True, (255,255,255))   # usa “x2” si tu fuente no rinde bien
DOBLE = FONT.render("2⏫", True, (255,255,255))
PASO   = FONT.render("⤼",  True, (255,255,255))
RECT_X2 = X2.get_rect()
RECT_DOBLE = DOBLE.get_rect()
RECT_PASO = PASO.get_rect()
RECT_BOMB = BOMBA.get_rect()
ALTO = cfg.ALTO
ANCHO = cfg.ANCHO

# Variables
bomba_usado = False
X2_usado = False
doble_usado = False
paso_usado = False

bomba_activa = False
X2_activo = False
doble_activo = False
paso_activo = False 

def init_comodines(ALTO, margen=20):
    """
    Inicializamos las posiciones de los comodines en pantalla. 
    """
    y_base = ALTO - margen          
    x      = margen

    RECT_BOMB.bottomleft   = (x, y_base)
    x = RECT_BOMB.right + margen

    RECT_X2.bottomleft     = (x, y_base)
    x = RECT_X2.right + margen

    RECT_DOBLE.bottomleft  = (x, y_base)
    x = RECT_DOBLE.right + margen

    RECT_PASO.bottomleft   = (x, y_base)
    
    
def reset():
    """ Resetea las Flags
    """
    global bomba_usado, X2_usado, doble_usado, paso_usado, X2_activo, doble_activo, bomba_activa, paso_activo
    bomba_usado = X2_usado = doble_usado = paso_usado = X2_activo = doble_activo = False
    
def manejar_evento(ev):
    """Manejo de eventos de los comodines

    Args:
        ev (_type_): evento del loop princiapl
    """
    global bomba_usado, X2_usado, doble_usado, paso_usado, X2_activo, doble_activo, bomba_activa, paso_activo

    if ev.type != pygame.MOUSEBUTTONDOWN or ev.button != 1:
        return   
    
    if not bomba_usado and RECT_BOMB.collidepoint(ev.pos):
        music.sonido_click().play()
        bomba_activa = True
    elif bomba_usado and RECT_BOMB.collidepoint(ev.pos):
        music.sonido_click_off().play()
        
    if not X2_usado and RECT_X2.collidepoint(ev.pos):
        music.sonido_click().play()
        X2_activo = True
    elif X2_usado and RECT_X2.collidepoint(ev.pos):
        music.sonido_click_off().play()
    
    if not doble_usado and RECT_DOBLE.collidepoint(ev.pos):
        music.sonido_click().play()
        doble_activo = True
    elif doble_usado and RECT_BOMB.collidepoint(ev.pos):
        music.sonido_click_off().play()
    
    if not paso_usado and RECT_PASO.collidepoint(ev.pos):
        music.sonido_click().play()
        paso_activo = True
    elif paso_usado and RECT_BOMB.collidepoint(ev.pos):
        music.sonido_click_off().play()

def dibujar(win):
    win.blit(BOMBA, RECT_BOMB)
    win.blit(X2, RECT_X2)
    win.blit(DOBLE, RECT_DOBLE)
    win.blit(PASO, RECT_PASO)
