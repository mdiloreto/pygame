import pygame, configuracion as cfg
import json
from datetime import datetime

_fondo = None
_fuente_titulo = None
_fuente_puntaje = None
_puntajes = []

def main():
    global _fondo, _fuente_titulo, _fuente_puntaje, _puntajes

    if _fondo is None:
        _fondo = pygame.image.load(cfg.IMG_TOP10).convert()

    _fuente_titulo = pygame.font.Font(cfg.FONT_BOLD_PATH, 60)
    _fuente_puntaje = pygame.font.Font(cfg.FONT_BOLD_PATH, 36)

    _cargar_puntajes()

def _cargar_puntajes(archivo='datos/partidas.json'):
    global _puntajes
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            _puntajes = json.load(f)
        # Ordenar por 'puntaje'  orden descendente
        _puntajes.sort(key=lambda x: x.get('puntaje', 0), reverse=True)
        # solo los 10 primeros 
        _puntajes = _puntajes[:10]
    except (FileNotFoundError, json.JSONDecodeError):
        _puntajes = []

def actualizar(dt):
    pass

def manejar_evento(ev):
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
        return 'menu'
    return 'top10'

def dibujar(win):
    win.blit(_fondo, (0, 0))

        # Titulo
    if not _puntajes:
            titulo_render = _fuente_titulo.render("Aún No hay puntajes", True, cfg.AMARILLO)
            titulo_rect = titulo_render.get_rect(center=(cfg.ANCHO // 2, 80))
            win.blit(titulo_render, titulo_rect)
    else:
        titulo_render = _fuente_titulo.render("Top 10 Mejores Puntajes", True, cfg.AMARILLO)
        titulo_rect = titulo_render.get_rect(center=(cfg.ANCHO // 2, 80))
        win.blit(titulo_render, titulo_rect)

    # Dibujar puntajes
    alto = 180
    for i, puntaje_entry in enumerate(_puntajes):
        name = puntaje_entry.get('nombre', 'N/A')
        puntaje = puntaje_entry.get('puntaje', 0)
        fecha = puntaje_entry.get('fecha', 'N/A')
        fecha_obj = datetime.fromisoformat(fecha)
        fecha_formateada = fecha_obj.strftime("%d-%m-%Y")

        puntaje_text = f"{i+1}. {name} - Puntos: {puntaje} - Fecha: {fecha_formateada}"
        puntaje_render = _fuente_puntaje.render(puntaje_text, True, cfg.BLANCO)
        puntaje_rect = puntaje_render.get_rect(center=(cfg.ANCHO // 2, alto))
        win.blit(puntaje_render, puntaje_rect)
        alto += 40