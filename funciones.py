import pygame,random,time,csv
from lista_opciones_respuestas import preguntas_respuestas

pygame.init()
fondo = pygame.image.load(r"juego maqueta\fondo millonario.jpg")
fondo_ganador = pygame.image.load(r"juego maqueta\ganador_millonario.webp")
pygame.mixer.music.load(r"juego maqueta\Y2meta.app - Música relajante para cabezas vacías ᖗ^‿^ᖘ 【Música de Nintendo】 (64 kbps).mp3")
pygame.mixer.music.play(-1)
grafico = pygame.image.load(r"juego maqueta\grafico.png")

posicion_rectangulo = 215

opciones_pos = [
    (285, 460),
    (695, 460),
    (285, 530),
    (695, 530),
]
comodin_areas = [
    pygame.Rect(15, 30, 300, 30), 
    pygame.Rect(15, 80, 300, 30), 
    pygame.Rect(15, 130, 300, 30), 
]

NEGRO = (0, 0, 0)
ANCHO, ALTO = 1200, 600
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)

fuente = pygame.font.Font(None, 30)

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("¿Quién Quiere Ser Millonario?")


lista_comodines = [
    "7. 50-50 - Dos respuestas incorrectas fuera",
    "8. Llamada - Palabra clave",
    "9. Público - Gráfico de porcentajes",
]

def comodin_llamada(palabra_clave):
    """_summary_: 
        Muestra la palabra clave dentro de un diccionario

    Args:
        palabra_clave (str): Una pista

    return:
        None
    """
    if palabra_clave:
        print(f"La palabra clave es: {palabra_clave}")
    else:
        print("Esta pregunta no tiene palabra clave definida.")

def comodin_50_50(opciones, respuesta_correcta):
    """_summary_: 
        Elimina dos respuestas incorrectas

    Args:
        opciones (str): posibles respuestas
        respuesta_correcta (str): La respuesta correcta entre las opciones

    return:
        None
    """
    opciones_correctas = [opciones[respuesta_correcta - 1]]
    opciones_incorrectas = [opciones[i - 1] for i in range(1, 5) if i != respuesta_correcta]

    opciones_aleatorias = opciones_correctas + random.sample(opciones_incorrectas, 1)

    print(f"Opciones 50-50:")
    for opcion in opciones_aleatorias:
        print(opcion)

    mostrar_opciones(opciones_aleatorias)

    return respuesta_correcta

def filtrar_pregunta(lista, valor_premio):
    """_summary_: 
        Filtra una lista por el valor del premio

    Args:
        lista (str): Una lista
        valor_premio (int): Numero entero que representa el valor de los premios

    return:
        lista_valor_premio
        []
    """
    try:
        lista_valor_premio = []
        for pregunta in lista:
            premio = pregunta["premio"]
            if premio == valor_premio:
                lista_valor_premio.append(pregunta)
        return lista_valor_premio
    except KeyError as e:
        print(f"Error al filtrar preguntas: {e}")
        return []

def mostrar_opciones(opciones):
    """_summary_: 
        Muestra las opciones en pantalla

    Args:
        opciones (str): posibles respuestas

    return None
    """
    fuente_opciones = pygame.font.Font(None, 28)
    for i, opcion in enumerate(opciones):
        opcion_texto = fuente_opciones.render(f"{opcion}", True, BLANCO)
        screen.blit(opcion_texto, opciones_pos[i])

def manejar_clic_comodin(mouse_pos, comodin_50_50_uso, comodin_llamada_uso, comodin_grafico_uso, pregunta_actual):
    """_summary_: 
        Detecta el click y ejecuta el comodin correspondiente en base a las coordenadas del click

    Args:
        mouse_pos (int): Coordenadas del mouse
        comodin_50_50_uso (str): 
        comodin_llamada_uso (str): 
        comodin_grafico_uso (str): 
        pregunta_actual (str): 

    return:
        comodin_50_50_uso
        comodin_llamada_uso
        comodin_grafico_uso
    """
    try:
        for i, area in enumerate(comodin_areas):

            if area.collidepoint(mouse_pos):

                if i == 0 and comodin_50_50_uso == 0 and "7. 50-50 - Dos respuestas incorrectas fuera" in lista_comodines:
                    comodin_50_50_uso += 1
                    comodin_50_50(pregunta_actual["Opciones"], pregunta_actual["Respuesta_correcta"])
                    lista_comodines.remove("7. 50-50 - Dos respuestas incorrectas fuera")
                    print("Comodín 50-50 utilizado.")

                elif i == 1 and comodin_llamada_uso == 0 and "8. Llamada - Palabra clave" in lista_comodines:
                    comodin_llamada_uso += 1
                    comodin_llamada(pregunta_actual["Palabra_clave"])
                    lista_comodines.remove("8. Llamada - Palabra clave")
                    print("Comodín Llamada - Palabra clave utilizado.")

                elif i == 2 and comodin_grafico_uso == 0 and "9. Público - Gráfico de porcentajes" in lista_comodines:
                    comodin_grafico_uso += 1
                    mostrar_grafico_porc(r"juego maqueta\grafico.png",(100),(100))
                    lista_comodines.remove("9. Público - Gráfico de porcentajes")
                    print("Comodín Público - Gráfico de porcentajes utilizado.")
                    
        return comodin_50_50_uso, comodin_llamada_uso, comodin_grafico_uso
    except Exception as e:
        print(f"Error al manejar clic de comodín: {e}")

def mostrar_grafico_porc(ruta_grafico, nuevo_ancho, nueva_altura):
    """_summary_: 
        Escala y blitea imagenes 

    Args:
        ruta_grafico (str): Path
        nuevo_ancho (str): Alto del escalado
        nueva_altura (str): Ancho del escalado

    return:
        None
    """
    grafico_original = pygame.image.load(ruta_grafico)
    grafico_redimensionado = pygame.transform.scale(grafico_original, (nuevo_ancho, nueva_altura))

    screen.blit(grafico_redimensionado, (0, 200))
    pygame.display.update()
    time.sleep(2)

    pygame.display.update()

def mostrar_pregunta_opciones(lista, valor_premio, comodin_50_50_uso, comodin_llamada_uso, comodin_grafico_uso, tiempo_inicial):
    """_summary_: 
        Se encarga del funcionamiento principal de la aplicacion

    Args:
        lista (str): lista a ingresar
        valor_premio (int): el valor del premio
        comodin_50_50_uso (str):un comodin
        comodin_llamada_uso (str):un comodin
        comodin_grafico_uso (str): un comodin
        tiempo_inicial (int): tiempo que tendra el usuario para contestar 

    return:
        funcionalidad 
    """
    global posicion_rectangulo
    x = 15
    y = 30
    funcionalidad = 1
    filtro = filtrar_pregunta(lista, valor_premio)
    indice_aleatorio = random.randint(0, len(filtro) - 1)
    pregunta_actual = filtro[indice_aleatorio]
    pregunta = pregunta_actual["Pregunta"]
    opciones = pregunta_actual["Opciones"]

    pregunta_texto = fuente.render(pregunta, True, BLANCO)
    screen.blit(fondo, (0, 0))

    pygame.draw.rect(screen, AMARILLO, (1080, posicion_rectangulo, 1080, 15), 1)

    for comodin in lista_comodines:
        opcion_comodin = fuente.render(comodin, True, BLANCO)
        screen.blit(opcion_comodin, (x, y))
        y += 50
    screen.blit(pregunta_texto, (270, 360))
    mostrar_opciones(opciones)
    
    pygame.display.update()

    tiempo_inicial = time.time()

    respuesta = None
    try:
        while respuesta is None:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    for i, pos in enumerate(opciones_pos):
                        if pos[0] < x < pos[0] + 100 and pos[1] < y < pos[1] + 30:
                            respuesta = i + 1
                    comodin_50_50_uso, comodin_llamada_uso, comodin_grafico_uso = manejar_clic_comodin((x, y), comodin_50_50_uso, comodin_llamada_uso, comodin_grafico_uso, pregunta_actual)
    except ZeroDivisionError:
        print("Error: División por cero.")
    except ValueError:
        print("Error: Conversión de cadena a entero fallida.")

    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial

        if tiempo_transcurrido >= 30:
            funcionalidad = 2
            return funcionalidad
        else:
            if respuesta == pregunta_actual["Respuesta_correcta"]:
                posicion_rectangulo -= 15
                break
            else:
                funcionalidad = 3
                break

    return funcionalidad

def iniciar_juego():
    """_summary_: 
        Se encarga de iniciar el juego y seguir la logica del mismo

    Args:
        palabra_clave (str): Una pista

    return:
        None
    """
    tiempo_inicial = time.time()

    comodin_50_50_uso = 0
    comodin_llamada_uso = 0
    comodin_grafico = 0

    premios = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000,"ganador"]
    indice_premio = 0

    while indice_premio < len(premios):
        print("Comodines:")
        for comodin in lista_comodines:
            print(comodin)
        valor = premios[indice_premio]
        if valor == "ganador":
            screen.fill((0, 0, 0))
            mostrar_grafico_porc(r"juego maqueta\ganador_millonario.webp", ANCHO, ALTO)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            exit()
        retorno = mostrar_pregunta_opciones(preguntas_respuestas, valor, comodin_50_50_uso, comodin_llamada_uso, comodin_grafico, tiempo_inicial)
        if retorno == 1:
            print("Respuesta correcta")
            indice_premio += 1
        elif retorno == 2:
            print("GAME OVER - Pasaron los 30 segundos")
            break
        elif retorno == 3:
            print("GAME OVER - Respuesta incorrecta")
            break
    with open('monto_alcanzado.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Monto Alcanzado'])
        writer.writerow([valor])