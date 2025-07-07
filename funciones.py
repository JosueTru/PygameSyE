import pygame
import random
from colores import *

def crear_render_y_rect(texto:str, coordenadas:tuple, fuente, color:tuple=BLACK):
    fuente = pygame.font.SysFont("Arial", 30)
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=coordenadas)
    return render, rect


def ingresar_nombre(pantalla):

    nombre_jugador = ""

    flag_correr = True
    while flag_correr:
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False

                
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[0:-1]
                else:
                    nombre_jugador += evento.unicode
                if evento.key == pygame.K_RETURN:
                    flag_correr = False


        pantalla.fill(COLOR_CELESTE) 

        texto_titulo, rect_titulo = crear_render_y_rect("Ingrese su nombre: ", (800,300), BLACK)
        texto_nombre, rect_nombre = crear_render_y_rect(nombre_jugador, (800, 350), BLACK)


        pantalla.blit(texto_titulo, rect_titulo)
        pantalla.blit(texto_nombre, rect_nombre)

        pygame.display.flip()

    return nombre_jugador


def menu(pantalla, lista_eventos, fondo):
    fuente = pygame.font.SysFont("Arial", 30)
    
    render_jugar, rect_jugar = crear_render_y_rect("Desea jugar", (800, 350), BLACK)
    render_puntaje, rect_puntaje = crear_render_y_rect("Ver puntajes", (800,450), BLACK)
    render_salir, rect_salir = crear_render_y_rect("Salir", (800,550), BLACK)

    estado_menu = "menu"


    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            estado_menu = "salir"
                
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_jugar.collidepoint(evento.pos):
                estado_menu = "trivia"
            elif rect_puntaje.collidepoint(evento.pos):
                ver_puntajes(pantalla, fondo)
            elif rect_salir.collidepoint(evento.pos):
                estado_menu = "salir"

    #pantalla.fill(COLOR_CELESTE)   
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(render_jugar, rect_jugar)
    pantalla.blit(render_puntaje, rect_puntaje)
    pantalla.blit(render_salir, rect_salir)

    pygame.display.flip()

        
    return estado_menu




def trivia(pantalla, preguntas_copia, posicion, fondo, jugador, tablero, imagen_puntos, imagen_temporizador, derrota_music, victoria_music):
    

    nombre = ingresar_nombre(pantalla).strip()


    while len(preguntas_copia) > 0:

        pregunta_dict = sacar_pregunta_dict(preguntas_copia)
        opciones = sacar_opciones_pregunta_dict(pregunta_dict)
        respuesta_correcta = pregunta_dict["respuesta_correcta"]

        render_salir, rect_salir = crear_render_y_rect("Terminar juego", (1300, 700), BLACK)

        #contador
        tiempo_inicial = pygame.time.get_ticks()  # milisegundos
        tiempo_limite = 10000 

        flag = True
        while flag:

            #contador
            tiempo_actual = pygame.time.get_ticks()
            tiempo_restante = max(0, tiempo_limite - (tiempo_actual - tiempo_inicial))
            if tiempo_restante == 0:
                posicion -= 1
                posicion = calcular_direccion_tablero(posicion, -1, tablero)
                flag = False


            lista_eventos = pygame.event.get()
            for evento in lista_eventos:
                if evento.type == pygame.QUIT:
                    #flag = False
                    return posicion, "salir"


        


                if evento.type == pygame.MOUSEBUTTONDOWN:

                    if rect_salir.collidepoint(evento.pos):
                        guardar_datos(nombre, posicion)
                        return posicion, "salir"

                    

                    clic_valido = False
                    for letra, render_opcion, rect_opcion in opciones:
                        if rect_opcion.collidepoint(evento.pos):
                            posicion = mover(respuesta_correcta, posicion, evento.pos, tablero, opciones)
                            clic_valido = True
                            break

                    if clic_valido:
                        estado_juego = verificar_fin_juego(posicion, tablero)
                        if estado_juego == "Perdistee":
                            pygame.mixer.music.stop()
                            derrota_music.play()

                        elif estado_juego == "Ganastee":
                            pygame.mixer.music.stop()
                            victoria_music.play()
    
                        if estado_juego != "continua":
                            mostrar_mensaje(pantalla, f"¡{estado_juego}!", fondo)
                            guardar_datos(nombre, posicion)

                            return posicion, "menu"
                        flag = False     






            
            #pantalla.fill(COLOR_CELESTE)   
            pantalla.blit(fondo, (0, 0))


            #
            render_pregunta, rect_pregunta = crear_render_y_rect(pregunta_dict["pregunta"], (800, 300), BLACK)
            pantalla.blit(render_pregunta,rect_pregunta)

            #Iteracion de la lista de tuplas para mostrar las opciones en pantalla
            for letra, render_opcion, rect_opcion in opciones:
                pantalla.blit(render_opcion, rect_opcion)

            render_posicion, rect_posicion = crear_render_y_rect(str(posicion), (100, 100), BLACK)
            pantalla.blit(render_posicion,rect_posicion)

            pantalla.blit(imagen_puntos, (40, 80))  # coordenadas a gusto, ajustalas si se solapan

            


            pantalla.blit(render_salir,rect_salir)

            dibujar_tablero(pantalla, tablero, posicion, jugador)


            segundos = tiempo_restante // 1000
            render_timer, rect_timer = crear_render_y_rect(f"{segundos}", (1500, 100), BLACK)
            pantalla.blit(render_timer, rect_timer)

            pantalla.blit(imagen_temporizador, (1430, 75))

            pygame.display.flip()

    pantalla.fill(COLOR_CELESTE)
    render_fin, rect_fin = crear_render_y_rect("Se acabaron las preguntas!", (800, 400), BLACK)
    pantalla.blit(render_fin, rect_fin)
    pygame.display.flip()
    
    pygame.time.delay(2000)  # pausa 2 segundos
    guardar_datos(nombre, posicion)


    return posicion, "menu"



def copiar_y_mezclar_lista(preguntas:list):
    preguntas_copia = preguntas.copy()
    random.shuffle(preguntas_copia)
    return preguntas_copia

def sacar_pregunta_dict(preguntas:list):
    pregunta_elegida = preguntas.pop()

    return pregunta_elegida


def sacar_opciones_pregunta_dict(pregunta):
    letras = ["a","b","c"]
    render_y_rect_opciones = []
    posicion_x = 0

    for i in range(len(letras)):
        posicion_x += 400
        letra = letras[i]
        respuestas = pregunta[f"respuesta_{letra}"]
        texto = f"{letra}) {respuestas}"
        render_opciones, rect_opciones = crear_render_y_rect(texto, (posicion_x, 400), BLACK)

        render_y_rect_opciones.append((letra, render_opciones, rect_opciones))

    return render_y_rect_opciones



def mover( respuesta_correcta:str, posicion:int,evento_pos , tablero:list, opciones)->int:

    #Toma la respuesta correcta del dict elegido

    #Calcula la direccion y saltos
    operacion = calcular_direccion_base(opciones, evento_pos, respuesta_correcta)
    posicion += operacion

    posicion = calcular_direccion_tablero(posicion, operacion, tablero)



    return posicion


def calcular_direccion_base(opciones, evento_pos, respuesta_correcta):
    resultado = 0

    for letra, render, rect in opciones:
        if rect.collidepoint(evento_pos):
            if letra == respuesta_correcta:

                resultado += 1
            else:
                resultado += -1
    return resultado

def calcular_direccion_tablero(posicion, calculo, tablero):
    salto_adicional = tablero[posicion]
    posicion += salto_adicional * calculo

    return posicion



def dibujar_tablero(pantalla, tablero, posicion_jugador, jugador):
    x_inicial = 0
    y = 760
    ancho = 51.65
    alto = 100
    espacio = 0

    for i in range(len(tablero)):
        x = x_inicial + i * (ancho + espacio)

        # Color según tipo de casillero
        valor = tablero[i]
        if valor == 0:
            color = GRAY
        elif valor == 1:
            color = YELLOW1
        elif valor == 2:
            color = GREEN
        elif valor == 3:
            color = BLUE

        # Dibujar casilla
        rect = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(pantalla, color, rect)

        # Dibujar borde
        pygame.draw.rect(pantalla, BLACK, rect, 2)

        # Dibujar imagen del jugador
        if i == posicion_jugador:
            rect_centro = jugador.get_rect(center=rect.center)
            pantalla.blit(jugador, rect_centro)



def verificar_fin_juego(posicion, tablero):
    veredicto = "continua"
    if posicion <= 0:
        veredicto = "Perdistee"
    elif posicion >= len(tablero)-1:

        veredicto = "Ganastee"
    return veredicto


def mostrar_mensaje(pantalla, texto, fondo):
    pantalla.blit(fondo, (0, 0))
    render_mensaje, rect_mensaje = crear_render_y_rect(texto, (800, 400), BLACK)
    pantalla.blit(render_mensaje, rect_mensaje)
    pygame.display.flip()
    pygame.time.delay(3000)




def guardar_datos(nombre_jugador: str, posicion: int):
    with open("puntaje.csv", "a", encoding="utf-8") as puntajes:
        puntajes.write(f"{nombre_jugador} || {posicion} puntos.\n")



def leer_obtener_puntajes():
    with open("puntaje.csv", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    return lineas

def ordenar_puntajes(lineas):
    puntajes = []
    
    for linea in lineas:
        partes = linea.strip().split()
        nombre = partes[0].strip()
        puntos = int(partes[2])
        puntajes.append([nombre, puntos])

    for i in range(len(puntajes)-1):
        for j in range(i+1,len(puntajes)):
            if puntajes[i][1] < puntajes[j][1]:
                aux = puntajes[i][1]
                puntajes[i][1] = puntajes[j][1]
                puntajes[j][1] = aux
    return puntajes






def ver_puntajes(pantalla,fondo):

    lineas = leer_obtener_puntajes()
    puntajes = ordenar_puntajes(lineas)

    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando = False

        pantalla.blit(fondo, (0, 0))

        # Título
        titulo, rect_titulo = crear_render_y_rect("PUNTAJES", (800, 100), None, BLACK)
        pantalla.blit(titulo, rect_titulo)

        # Mostrar cada puntaje
        y = 180
        for nombre, puntos in puntajes:
            texto = f"{nombre} - {puntos} puntos"
            render, rect = crear_render_y_rect(texto, (800, y), None, BLACK)
            pantalla.blit(render, rect)
            y += 50

        # Instrucción para volver
        volver, rect_volver = crear_render_y_rect("Presioná ESC para volver al menú", (800, 750), None, BLACK)
        pantalla.blit(volver, rect_volver)

        pygame.display.flip()


