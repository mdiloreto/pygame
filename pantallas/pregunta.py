import csv, random, pygame, configuracion as cfg
import textwrap
import music
from pantallas.game_over import preguntas_info

TIEMPO_PREGUNTA_MS = 20_000
EVENTO_FEEDBACK    = pygame.USEREVENT + 1          # 1,2 s de pausa

RECTS_OPC = [
    # x = coord horizontal, y = cord vertical, w = ancho del rect y h = alto del rect
    pygame.Rect(390, 300, 500, 70), 
    pygame.Rect(390, 390, 500, 70),
    pygame.Rect(390, 480, 500, 70),
    pygame.Rect(390, 570, 500, 70),
]

# Init variables
preguntas_csv = "datos/preguntas.csv"
preguntas  = []     
idx        = 0
opciones   = []
estado      = "pregunta"   
total_vidas = 5
puntaje    = 0
t0_ms      = 0           
fondo      = None
font_q     = None
font_opt   = None
racha      = 0
show_msg = False 
# 


def loop_principal():
    """Se usa para entrar en la pantalla.
        -> Inicia la carga de preguntas "_cargar_preguntas"
        -> Inicia una nueva partida "_nueva_partida"
    """
    global fondo, font_q, font_opt

    if fondo is None:
        fondo    = pygame.image.load(cfg.IMG_FONDO_PREGUNTAS)
    if font_q is None:
        font_q   = pygame.font.Font(cfg.FONT_BOLD_PATH, 46)
    if font_opt is None: 
        font_opt = pygame.font.Font(cfg.FONT_REG_PATH, 38)


    _cargar_preguntas(preguntas_csv)
    _nueva_partida()

def _cargar_preguntas(path):
    """Carga el CSV de las preguntas 

    Args:
        ruta (path): Path del archivo CSV de las preguntas
    """
    global preguntas
    with open(path, encoding="utf-8") as f:
        preguntas = list(csv.DictReader(f))
    random.shuffle(preguntas)

def _nueva_partida():
    """Inicializa una nueva partida. Resetea los valores de idx, vidas y puntaje. 
    
    """
    global idx, vidas, puntaje
    vidas = total_vidas
    idx, puntaje = 0, 0
    _nueva_pregunta()

def _nueva_pregunta():
    global opciones, estado, t0_ms
    p        = preguntas[idx]
    opciones = [p["correct"], p["wrong1"], p["wrong2"], p["wrong3"]]
    random.shuffle(opciones)
    estado = "pregunta"
    t0_ms  = pygame.time.get_ticks()

def _evaluar_respuesta(i):
    global estado, puntaje, vidas, racha, show_msg, msg_expira_ms
    correcta  = preguntas[idx]["correct"]
    seleccion = opciones[i]
    if seleccion == correcta:
        music.sonido_correcto().play()
        puntaje += 10
        if racha == 5:
            vidas += 1
            racha = 0
            show_msg      = True          # activa mensaje
            msg_expira_ms = pygame.time.get_ticks() + 2000   # 2 s
        else: 
            racha += 1
    if seleccion != correcta:
        music.sonido_error().play()
        vidas -=1
        racha = 0
    estado = "feedback"
    pygame.time.set_timer(EVENTO_FEEDBACK, 1200)   # Reiniciar el tiempo

def manejar_evento(ev):
    global idx, vidas, estado

    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
        return "menu"
    if ev.type == pygame.QUIT:
        return "salir"
    if estado == "pregunta" and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        for i, r in enumerate(RECTS_OPC):
            if r.collidepoint(ev.pos):
                _evaluar_respuesta(i)
                break
    
    # Pasar de pregunta + Reiniciar el tieempo. 
    # Esto sucede si 1) se quedó sin tiempo en la pregunta 2) si contestó 
    if ev.type == EVENTO_FEEDBACK:                  
        pygame.time.set_timer(EVENTO_FEEDBACK, 0)
        # si se quedó sin vidas: 
        if vidas <= 0:
            preguntas_info(puntaje)
            return "game_over"

        idx += 1
        # Si se acaban las preguntas >>
        if idx >= len(preguntas):
            preguntas_info(puntaje)
            return "game_over"

        _nueva_pregunta()

    return "pregunta"

def actualizar(dt):
    global estado, vidas, show_msg
    if show_msg and pygame.time.get_ticks() > msg_expira_ms:
        show_msg = False
    if estado == "pregunta" and pygame.time.get_ticks() - t0_ms > TIEMPO_PREGUNTA_MS:
        vidas -= 1
        estado = "feedback"
        pygame.time.set_timer(EVENTO_FEEDBACK, 1200)
        

def dibujar(win):
    win.blit(fondo, (0, 0))

    # Color vidas 
    if vidas < total_vidas // 2:
        COLOR_VIDAS = cfg.ROJO
    elif vidas == total_vidas // 2: 
        COLOR_VIDAS = cfg.AMARILLO
    elif vidas > total_vidas // 2:
        COLOR_VIDAS = cfg.VERDE

    font_emoji = pygame.font.Font("recursos/fuentes/Symbola.ttf", 64)
    txt_pts  = font_opt.render(f"Puntos: {puntaje}", True, cfg.BLANCO)
    txt_live = font_emoji.render("❤️" * vidas, True, COLOR_VIDAS)     
    win.blit(txt_pts,  (20, 20))
    win.blit(txt_live, (cfg.ANCHO - txt_live.get_width() - 20, 20)) # total del ancho - with del texto de la vida - 20 px de margen

    # pregunta
    lineas = textwrap.wrap(preguntas[idx]["question"], width=50)   
    y = 140                                                       
    for linea in lineas:
        surf = font_q.render(linea, True, cfg.BLANCO)
        win.blit(surf, (cfg.ANCHO//2 - surf.get_width()//2, y))  
        y += font_q.get_linesize()  

    # opciones
    for i, opc in enumerate(opciones):
        color = cfg.AMARILLO
        if estado == "feedback":
            if opc == preguntas[idx]["correct"]:
                color = cfg.VERDE
            elif RECTS_OPC[i].collidepoint(pygame.mouse.get_pos()):
                color = cfg.ROJO
        pygame.draw.rect(win, color, RECTS_OPC[i], border_radius=8)
        txt_o = font_opt.render(opc, True, cfg.NEGRO)
        win.blit(txt_o, txt_o.get_rect(center=RECTS_OPC[i].center))

    if show_msg:
        font_msg = pygame.font.Font(cfg.FONT_BOLD_PATH, 36)
        surf_msg = font_msg.render("+1 VIDA ❤", True, cfg.VERDE)
        win.blit(surf_msg, (cfg.ANCHO - surf_msg.get_width() - 40, 100))