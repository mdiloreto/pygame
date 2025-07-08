import pygame
import configuracion as cfg
import random


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

def init_comodines(ANCHO, ALTO, margen=20):
    """
    Inicializamos las posiciones de los comodines en pantalla. 
    """
    RECT_BOMB.bottomleft = (ANCHO, ALTO)
    RECT_X2.bottomleft = (RECT_BOMB.right + margen, ALTO)
    RECT_DOBLE.bottomleft = (RECT_X2.right + margen, ALTO)
    RECT_PASO.bottomleft = (RECT_DOBLE.right + margen, ALTO)
    
    
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

    if not bomba_usado and RECT_BOMB.collidepoint(ev.pos):
        bomba_activa = True 
        
    if not X2_usado and RECT_X2.collidepoint(ev.pos):
        X2_activo = True
    
    if not doble_usado and RECT_DOBLE.collidepoint(ev.pos):
        doble_activo = True
    
    if not paso_usado and RECT_PASO.collidepoint(ev.pos):
        paso_activo = True

def dibujar(win):
    win.blit(BOMBA, RECT_BOMB)
    win.blit(X2, RECT_X2)
    win.blit(DOBLE, RECT_DOBLE)
    win.blit(PASO, RECT_PASO)
