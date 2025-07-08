# Documentación Extensiva de `pantallas/pregunta.py`

Este documento detalla el funcionamiento interno del módulo `pregunta.py`, que gestiona la lógica y la interfaz de usuario de la pantalla de preguntas en el juego.

---

## 1. Importaciones y Constantes Globales

El módulo comienza importando las librerías y módulos necesarios, así como definiendo constantes que se utilizan a lo largo del código.

```python
import csv, random, pygame, configuracion as cfg
import textwrap
import modulos.music as music
from pantallas.game_over import preguntas_info
import modulos.comodines as comodines

# Constantes
TIEMPO_PREGUNTA_MS = 20_000
EVENTO_FEEDBACK    = pygame.USEREVENT + 1          # 1,2 s de pausa
RECTS_OPC = [
    # x = coord horizontal, y = cord vertical, w = ancho del rect y h = alto del rect
    pygame.Rect(390, 300, 500, 70),
    pygame.Rect(390, 390, 500, 70),
    pygame.Rect(390, 480, 500, 70),
    pygame.Rect(390, 570, 500, 70),
]
```

*   **`csv`**: Módulo para leer archivos CSV, utilizado para cargar las preguntas.
*   **`random`**: Módulo para operaciones aleatorias, como mezclar opciones y preguntas.
*   **`pygame`**: La biblioteca principal para el desarrollo del juego.
*   **`configuracion as cfg`**: Módulo personalizado que contiene configuraciones globales del juego (colores, rutas de imágenes, etc.).
*   **`textwrap`**: Módulo para ajustar texto a un ancho determinado, utilizado para formatear las preguntas largas.
*   **`modulos.music as music`**: Módulo personalizado para la gestión de la música y efectos de sonido.
*   **`pantallas.game_over import preguntas_info`**: Importa una función del módulo `game_over` para pasar el puntaje final.
*   **`modulos.comodines as comodines`**: Módulo personalizado para la gestión de los comodines del juego.

*   **`TIEMPO_PREGUNTA_MS`**: Constante que define el tiempo límite para responder una pregunta en milisegundos (20 segundos).
*   **`EVENTO_FEEDBACK`**: Un evento personalizado de Pygame (`pygame.USEREVENT + 1`) que se utiliza para controlar el tiempo de espera después de que el jugador responde una pregunta o se le acaba el tiempo. El comentario indica una pausa de 1.2 segundos.
*   **`RECTS_OPC`**: Una lista de objetos `pygame.Rect` que definen las posiciones y dimensiones de los rectángulos donde se dibujarán las opciones de respuesta. Cada `Rect` tiene `(x, y, width, height)`.

---

## 2. Variables de Estado Globales

Estas variables mantienen el estado actual de la pantalla de preguntas y la partida en curso.

```python
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
show_msg_vida_add = False
```

*   **`preguntas_csv`**: Ruta al archivo CSV que contiene las preguntas del juego.
*   **`preguntas`**: Una lista que almacenará todas las preguntas cargadas del CSV. Cada pregunta es un diccionario.
*   **`idx`**: Índice de la pregunta actual en la lista `preguntas`.
*   **`opciones`**: Lista que contiene las opciones de respuesta para la pregunta actual.
*   **`estado`**: Cadena que representa el estado actual de la pantalla (`"pregunta"` o `"feedback"`).
    *   `"pregunta"`: El jugador está viendo la pregunta y sus opciones.
    *   `"feedback"`: Se muestra el resultado de la respuesta (correcta/incorrecta) o el tiempo se ha agotado.
*   **`total_vidas`**: Número inicial de vidas del jugador.
*   **`puntaje`**: Puntaje actual del jugador.
*   **`t0_ms`**: Marca de tiempo (en milisegundos) cuando la pregunta actual comenzó, utilizada para controlar el temporizador.
*   **`fondo`**: Objeto `pygame.Surface` que representa la imagen de fondo de la pantalla. Se carga una vez.
*   **`font_q`**: Objeto `pygame.font.Font` para renderizar el texto de la pregunta. Se carga una vez.
*   **`font_opt`**: Objeto `pygame.font.Font` para renderizar el texto de las opciones. Se carga una vez.
*   **`racha`**: Contador de respuestas correctas consecutivas.
*   **`show_msg_vida_add`**: Booleano que controla si se debe mostrar el mensaje de "vida extra" por racha.
*   **`msg_expira_ms`**: Marca de tiempo cuando el mensaje de "vida extra" debe desaparecer.

---

## 3. Funciones Principales

### `main()`

```python
def main():
    """Se usa para entrar en la pantalla.
        -> Inicia la carga de preguntas "_cargar_preguntas"
        -> Inicia una nueva partida "_nueva_partida"
    """
    global fondo, font_q, font_opt, opciones

    if fondo is None:
        fondo    = pygame.image.load(cfg.IMG_FONDO_PREGUNTAS)
    if font_q is None:
        font_q   = pygame.font.Font(cfg.FONT_BOLD_PATH, 46)
    if font_opt is None:
        font_opt = pygame.font.Font(cfg.FONT_REG_PATH, 38)

    comodines.init_comodines(cfg.ALTO)
    _cargar_preguntas(preguntas_csv)
    _nueva_partida()
```

*   **Propósito**: Esta función es el punto de entrada principal para la pantalla de preguntas. Se llama cada vez que se activa esta pantalla (por ejemplo, al iniciar una nueva partida desde el menú).
*   **Funcionamiento**:
    *   Verifica si el `fondo` y las fuentes (`font_q`, `font_opt`) ya han sido cargados. Si no, los carga para evitar recargas innecesarias.
    *   Inicializa la posición de los comodines llamando a `comodines.init_comodines(cfg.ALTO)`.
    *   Llama a `_cargar_preguntas(preguntas_csv)` para cargar todas las preguntas del archivo CSV.
    *   Llama a `_nueva_partida()` para inicializar una nueva sesión de juego.

### `_usar_comodin_bomba(lista_op)`

```python
def _usar_comodin_bomba(lista_op):
    global preguntas

    correcta = preguntas[idx]["correct"]
    incorrectas = [o for o in lista_op if o != correcta]
    nuevas = [correcta, random.choice(incorrectas)]
    random.shuffle(nuevas)
    while len(nuevas) < 4:
        nuevas.append(None)
    return nuevas
```

*   **Propósito**: Implementa la lógica del comodín "bomba", que elimina dos opciones incorrectas, dejando solo la correcta y una incorrecta.
*   **Parámetros**:
    *   `lista_op`: La lista actual de opciones de respuesta para la pregunta.
*   **Funcionamiento**:
    *   Obtiene la respuesta correcta de la pregunta actual (`preguntas[idx]["correct"]`).
    *   Crea una lista `incorrectas` filtrando las opciones que no son la correcta.
    *   Crea una nueva lista `nuevas` que contiene la respuesta correcta y una opción incorrecta elegida al azar.
    *   Mezcla aleatoriamente estas dos opciones.
    *   Rellena la lista `nuevas` con `None` hasta que tenga 4 elementos. Esto es crucial para que las opciones "eliminadas" no se dibujen, pero los rectángulos de las opciones sigan existiendo.
    *   Retorna la lista `nuevas` modificada.

### `_cargar_preguntas(path)`

```python
def _cargar_preguntas(path):
    """Carga el CSV de las preguntas 

    Args:
        ruta (path): Path del archivo CSV de las preguntas
    """
    global preguntas
    with open(path, encoding="utf-8") as f:
        preguntas = list(csv.DictReader(f))
    random.shuffle(preguntas)
```

*   **Propósito**: Carga las preguntas desde un archivo CSV y las almacena en la variable global `preguntas`.
*   **Parámetros**:
    *   `path`: La ruta al archivo CSV de preguntas.
*   **Funcionamiento**:
    *   Abre el archivo CSV especificado en modo lectura con codificación UTF-8.
    *   Utiliza `csv.DictReader` para leer el CSV, tratando cada fila como un diccionario donde las claves son los encabezados de las columnas.
    *   Convierte el `DictReader` a una lista y la asigna a la variable global `preguntas`.
    *   Mezcla aleatoriamente el orden de las preguntas para asegurar variedad en cada partida.

### `_nueva_partida()`

```python
def _nueva_partida():
    """Inicializa una nueva partida. Resetea los valores de idx, vidas y puntaje. 
    
    """
    global idx, vidas, puntaje
    comodines.reset()
    vidas = total_vidas
    idx, puntaje = 0, 0
    _nueva_pregunta()
```

*   **Propósito**: Reinicia el estado del juego para una nueva partida.
*   **Funcionamiento**:
    *   Llama a `comodines.reset()` para restablecer el estado de todos los comodines.
    *   Restablece las `vidas` al valor inicial de `total_vidas`.
    *   Reinicia el `idx` (índice de pregunta) y el `puntaje` a 0.
    *   Llama a `_nueva_pregunta()` para cargar la primera pregunta de la nueva partida.

### `_nueva_pregunta()`

```python
def _nueva_pregunta():
    global opciones, estado, t0_ms
    p        = preguntas[idx]
    opciones = [p["correct"], p["wrong1"], p["wrong2"], p["wrong3"]]
    random.shuffle(opciones)
    estado = "pregunta"
    t0_ms  = pygame.time.get_ticks()
```

*   **Propósito**: Prepara la siguiente pregunta para ser mostrada al jugador.
*   **Funcionamiento**:
    *   Obtiene la pregunta actual de la lista `preguntas` usando el `idx`.
    *   Crea la lista `opciones` con la respuesta correcta y las tres respuestas incorrectas de la pregunta actual.
    *   Mezcla aleatoriamente el orden de las `opciones` para que la respuesta correcta no siempre esté en la misma posición.
    *   Establece el `estado` a `"pregunta"`.
    *   Registra el tiempo actual (`pygame.time.get_ticks()`) en `t0_ms` para iniciar el temporizador de la pregunta.

### `_evaluar_respuesta(i)`

```python
def _evaluar_respuesta(i):
    global estado, puntaje, vidas, racha, show_msg_vida_add, msg_expira_ms
    correcta  = preguntas[idx]["correct"]
    seleccion = opciones[i]
    if seleccion == correcta:
        music.sonido_correcto().play()
        if comodines.X2_activo:
            puntaje += 20
            comodines.X2_usado = True
            comodines.X2_activo = False
        else:
            puntaje += 10
        if racha == 5:
            vidas += 1
            racha = 0
            show_msg_vida_add      = True          # activa mensaje
            msg_expira_ms = pygame.time.get_ticks() + 2000   # 2 s
        else:
            racha += 1
    if seleccion != correcta:
        music.sonido_error().play()
        vidas -=1
        racha = 0
    estado = "feedback"
    pygame.time.set_timer(EVENTO_FEEDBACK, 1200)   # Reiniciar el tiempo
```

*   **Propósito**: Evalúa si la respuesta seleccionada por el jugador es correcta o incorrecta y actualiza el estado del juego en consecuencia.
*   **Parámetros**:
    *   `i`: El índice de la opción seleccionada por el jugador.
*   **Funcionamiento**:
    *   Obtiene la respuesta `correcta` de la pregunta actual y la `seleccion` del jugador.
    *   **Si la respuesta es correcta**:
        *   Reproduce el sonido de acierto (`music.sonido_correcto().play()`).
        *   Verifica si el comodín `X2` está activo. Si lo está, duplica los puntos ganados (20 en lugar de 10) y marca el comodín como usado e inactivo.
        *   Incrementa el `puntaje`.
        *   Gestiona la `racha`: si el jugador alcanza 5 respuestas correctas consecutivas, gana una vida extra, se reinicia la racha y se activa un mensaje temporal (`show_msg_vida_add`).
        *   Si no se alcanza la racha, simplemente incrementa el contador de `racha`.
    *   **Si la respuesta es incorrecta**:
        *   Reproduce el sonido de error (`music.sonido_error().play()`).
        *   Decrementa una `vida`.
        *   Reinicia la `racha` a 0.
    *   Establece el `estado` a `"feedback"`.
    *   Configura un temporizador (`pygame.time.set_timer`) para el `EVENTO_FEEDBACK` que se disparará después de 1.2 segundos, lo que permite al jugador ver el resultado antes de pasar a la siguiente pregunta.

### `manejar_evento(ev)`

```python
def manejar_evento(ev):
    global idx, vidas, estado

    comodines.manejar_evento(ev)

    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
        return "menu"
    if ev.type == pygame.QUIT:
        return "salir"
    if estado == "pregunta" and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        for i, r in enumerate(RECTS_OPC):
            if opciones[i] is None:
                continue
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
```

*   **Propósito**: Procesa los eventos de usuario (clics de ratón, pulsaciones de teclado) y los eventos personalizados de Pygame para controlar la navegación y la lógica del juego.
*   **Parámetros**:
    *   `ev`: El objeto evento de Pygame.
*   **Funcionamiento**:
    *   Llama a `comodines.manejar_evento(ev)` para que el módulo de comodines procese sus propios eventos (clics en los iconos de comodín).
    *   **Manejo de teclado**:
        *   Si se presiona `ESC`, retorna `"menu"` para volver a la pantalla del menú.
        *   Si el evento es `pygame.QUIT`, retorna `"salir"` para cerrar el juego.
    *   **Manejo de clics en opciones (solo en estado "pregunta")**:
        *   Si el estado es `"pregunta"` y se detecta un clic del ratón:
            *   Itera sobre los rectángulos de las opciones (`RECTS_OPC`).
            *   Verifica si la opción actual no es `None` (importante para el comodín bomba).
            *   Si el clic colisiona con el rectángulo de una opción, llama a `_evaluar_respuesta(i)` con el índice de la opción y sale del bucle.
    *   **Manejo del `EVENTO_FEEDBACK`**:
        *   Cuando se dispara el `EVENTO_FEEDBACK` (después de la pausa de 1.2 segundos):
            *   Desactiva el temporizador del `EVENTO_FEEDBACK` (`pygame.time.set_timer(EVENTO_FEEDBACK, 0)`).
            *   **Verifica vidas**: Si las `vidas` son 0 o menos, llama a `preguntas_info(puntaje)` para pasar el puntaje a la pantalla de Game Over y retorna `"game_over"`.
            *   **Avanza a la siguiente pregunta**: Incrementa el `idx` para pasar a la siguiente pregunta.
            *   **Verifica fin de preguntas**: Si `idx` es mayor o igual al número total de `preguntas`, significa que se han respondido todas las preguntas. Llama a `preguntas_info(puntaje)` y retorna `"game_over"`.
            *   Si hay más preguntas y vidas, llama a `_nueva_pregunta()` para cargar la siguiente pregunta.
    *   Por defecto, retorna `"pregunta"` para indicar que la pantalla actual debe seguir siendo la de preguntas.

### `actualizar(dt)`

```python
def actualizar(dt):
    global estado, vidas, show_msg_vida_add, opciones
    if show_msg_vida_add and pygame.time.get_ticks() > msg_expira_ms:
        show_msg_vida_add = False

    if estado == "pregunta" and pygame.time.get_ticks() - t0_ms > TIEMPO_PREGUNTA_MS:
        vidas -= 1
        estado = "feedback"
        pygame.time.set_timer(EVENTO_FEEDBACK, 1200)

    # ejecución de comodines
    if comodines.bomba_activa:
        opciones = _usar_comodin_bomba(opciones)
        comodines.bomba_activa = False
        comodines.bomba_usado = True
```

*   **Propósito**: Actualiza el estado lógico del juego en cada fotograma.
*   **Parámetros**:
    *   `dt`: El tiempo transcurrido desde el último fotograma (delta time), aunque no se usa directamente en esta función para cálculos de tiempo.
*   **Funcionamiento**:
    *   **Mensaje de vida extra**: Si `show_msg_vida_add` es `True` y el tiempo actual excede `msg_expira_ms`, oculta el mensaje (`show_msg_vida_add = False`).
    *   **Temporizador de pregunta**: Si el `estado` es `"pregunta"` y el tiempo transcurrido desde `t0_ms` excede `TIEMPO_PREGUNTA_MS` (el tiempo límite para la pregunta):
        *   Decrementa una `vida`.
        *   Cambia el `estado` a `"feedback"`.
        *   Configura el `EVENTO_FEEDBACK` para que se dispare después de 1.2 segundos.
    *   **Ejecución del comodín bomba**:
        *   Si `comodines.bomba_activa` es `True`:
            *   Llama a `_usar_comodin_bomba(opciones)` para modificar las opciones de respuesta.
            *   Establece `comodines.bomba_activa` a `False` para que el comodín no se active repetidamente.
            *   Marca `comodines.bomba_usado` como `True` para indicar que el comodín ya fue utilizado en esta partida.

### `dibujar(win)`

```python
def dibujar(win):
    global opciones, preguntas

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
    comodines.dibujar(win)
    # pregunta
    lineas = textwrap.wrap(preguntas[idx]["question"], width=50)   
    y = 140                                                       
    for linea in lineas:
        surf = font_q.render(linea, True, cfg.BLANCO)
        win.blit(surf, (cfg.ANCHO//2 - surf.get_width()//2, y))  
        y += font_q.get_linesize()  

    # muestra opciones, correcta, incorrecta y todas 
    for i, opc in enumerate(opciones):
        if opc is None:
            continue
        color = cfg.AMARILLO
        if estado == "feedback":
            if opc == preguntas[idx]["correct"]:
                color = cfg.VERDE
            elif RECTS_OPC[i].collidepoint(pygame.mouse.get_pos()):
                color = cfg.ROJO
        pygame.draw.rect(win, color, RECTS_OPC[i], border_radius=8)
        txt_opciones = font_opt.render(opc, True, cfg.NEGRO)
        win.blit(txt_opciones, txt_opciones.get_rect(center=RECTS_OPC[i].center))

    if show_msg_vida_add:
        font_msg = pygame.font.Font(cfg.FONT_BOLD_PATH, 36)
        surf_msg = font_msg.render("+1 VIDA ❤", True, cfg.VERDE)
        win.blit(surf_msg, (cfg.ANCHO - surf_msg.get_width() - 40, 100))
```

*   **Propósito**: Dibuja todos los elementos visuales de la pantalla de preguntas en la ventana del juego.
*   **Parámetros**:
    *   `win`: El objeto `pygame.Surface` que representa la ventana del juego donde se dibujarán los elementos.
*   **Funcionamiento**:
    *   Dibuja la imagen de `fondo`.
    *   **Indicador de vidas y puntaje**:
        *   Determina el color de las vidas (`COLOR_VIDAS`) basándose en el número actual de `vidas` (rojo si es bajo, amarillo si es medio, verde si es alto).
        *   Renderiza el texto del `puntaje` y las `vidas` (usando emojis de corazón) y los dibuja en la esquina superior de la pantalla.
    *   Llama a `comodines.dibujar(win)` para dibujar los iconos de los comodines.
    *   **Pregunta**:
        *   Utiliza `textwrap.wrap` para dividir el texto de la pregunta en `lineas` que se ajusten a un ancho de 50 caracteres.
        *   Itera sobre cada línea y la renderiza y dibuja en la parte superior central de la pantalla.
    *   **Opciones de respuesta**:
        *   Itera sobre cada `opc`ión en la lista `opciones`.
        *   Si una opción es `None` (debido al comodín bomba), la salta y no la dibuja.
        *   Determina el `color` del rectángulo de la opción:
            *   Por defecto, es `AMARILLO`.
            *   Si el `estado` es `"feedback"`:
                *   Si la opción es la `correcta`, el color es `VERDE`.
                *   Si el ratón está sobre una opción y no es la correcta, el color es `ROJO` (indicando la opción seleccionada incorrectamente).
        *   Dibuja el rectángulo de la opción con el color determinado y un `border_radius`.
        *   Renderiza el texto de la opción y lo dibuja centrado dentro de su rectángulo.
    *   **Mensaje de vida extra**: Si `show_msg_vida_add` es `True`, renderiza y dibuja el mensaje "+1 VIDA ❤" en la esquina superior derecha.

---

## 4. Flujo de la Lógica

1.  **Inicio de la pantalla (`main`)**:
    *   Carga recursos (fondo, fuentes).
    *   Inicializa comodines.
    *   Carga todas las preguntas del CSV.
    *   Inicia una nueva partida (`_nueva_partida`).
2.  **Nueva partida (`_nueva_partida`)**:
    *   Reinicia comodines, vidas y puntaje.
    *   Prepara la primera pregunta (`_nueva_pregunta`).
3.  **Nueva pregunta (`_nueva_pregunta`)**:
    *   Selecciona la pregunta actual.
    *   Mezcla las opciones.
    *   Establece el estado a "pregunta" y reinicia el temporizador.
4.  **Bucle principal del juego (en `main.py` que llama a `manejar_evento`, `actualizar`, `dibujar`)**:
    *   **`manejar_evento`**:
        *   Detecta clics en las opciones: Si el jugador hace clic en una opción, llama a `_evaluar_respuesta`.
        *   Detecta `ESC` o `QUIT` para salir o volver al menú.
        *   Procesa el `EVENTO_FEEDBACK`: Después de la pausa, avanza a la siguiente pregunta o a la pantalla de Game Over si se acabaron las vidas o las preguntas.
    *   **`actualizar`**:
        *   Verifica el tiempo límite de la pregunta: Si se agota, decrementa vidas y pasa al estado "feedback".
        *   Activa el comodín bomba si está marcado como activo.
    *   **`dibujar`**:
        *   Renderiza el fondo, puntaje, vidas, pregunta y opciones.
        *   Cambia el color de las opciones en estado "feedback" para mostrar el resultado.
        *   Dibuja los comodines.
5.  **Evaluación de respuesta (`_evaluar_respuesta`)**:
    *   Compara la opción seleccionada con la correcta.
    *   Actualiza puntaje, vidas y racha.
    *   Reproduce sonidos.
    *   Establece el estado a "feedback" y activa el temporizador para la pausa.
6.  **Comodín Bomba (`_usar_comodin_bomba`)**:
    *   Modifica la lista de opciones para eliminar dos incorrectas, dejando solo la correcta y una incorrecta.

---

Este documento proporciona una visión detallada de cómo `pantallas/pregunta.py` gestiona la lógica y la presentación de las preguntas en el juego, incluyendo la interacción con otros módulos como `modulos.music` y `modulos.comodines`.
