import pygame, configuracion as cfg
import json
from datetime import datetime


#Variables
nombre      = ""
editable    = True
estado_puntaje = 0
_fondo = None
_iconos_grandes = False

#Constates
MAX_CHARS   = 12
FONT_INPUT  = None   
RECT_INPUT  = pygame.Rect(cfg.ANCHO//2 - 200, 460, 400, 70) 

def main():
    global _titulo_txt, _fondo, _font_titulo, _iconos_grandes, FONT_INPUT

    if _fondo is None:
        _fondo = pygame.image.load(cfg.IMG_DERROTA).convert()

    FONT_INPUT  = pygame.font.Font(cfg.FONT_BOLD_PATH, 48)
    _font_titulo  = pygame.font.Font(cfg.FONT_BOLD_PATH, 80)
    _titulo_txt = "Escribí tu nombre..." 
        
def actualizar(dt):
    pass

def preguntas_info(puntaje):
    global estado_puntaje
    estado_puntaje = puntaje
    
def manejar_evento(ev):
    global nombre, editable
    if editable and ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_RETURN:
            if nombre:
                guardar_puntaje(nombre)
                editable = False
                return "top10" 
        elif ev.key == pygame.K_BACKSPACE:
            nombre = nombre[:-1]       
        else:
            char = ev.unicode
            if char.isprintable() and len(nombre) < MAX_CHARS:
                nombre += char 
    return 'game_over'

def dibujar(win):
    win.blit(_fondo, (0, 0))
    titulo = _font_titulo.render(_titulo_txt, True, cfg.BLANCO)
    win.blit(titulo, (cfg.ANCHO//2 - titulo.get_width()//2, 140))

    pygame.draw.rect(win, cfg.BLANCO, RECT_INPUT, width=2, border_radius=6)
    txt = FONT_INPUT.render(nombre or "Nombre...", True, (200,200,200) if nombre=="" else cfg.BLANCO)
    win.blit(txt, txt.get_rect(center=RECT_INPUT.center))
    
def guardar_puntaje(name, archivo='datos/partidas.json'):
    current_datetime = datetime.now().isoformat()
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = [] 

    data.append({"nombre": name, "puntaje": estado_puntaje, "fecha": current_datetime})

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)