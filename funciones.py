import pygame
import random
from colores import *


# Funcion reutilizable que crea render y rects
def crear_render_y_rect(texto:str, coordenadas:tuple, fuente, color:tuple=BLACK):
    fuente = pygame.font.SysFont("Arial", 30)
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=coordenadas)
    return render, rect

# Funcion que se encarga de recibir y mostrar el nombre
def ingresar_nombre(pantalla:any,fondo:any)->str:

    nombre_jugador = ""

    #inicio de bucle para ingresar nombre
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


        # Muestra por pantalla

        #fondo
        pantalla.blit(fondo, (0, 0)) 

        texto_titulo, rect_titulo = crear_render_y_rect("Ingrese su nombre: ", (800,300), BLACK)
        texto_nombre, rect_nombre = crear_render_y_rect(nombre_jugador, (800, 350), BLACK)

        #Titulo e input
        pantalla.blit(texto_titulo, rect_titulo)
        pantalla.blit(texto_nombre, rect_nombre)

        pygame.display.flip()

    return nombre_jugador



# Funcion que muestra el menu
def menu(pantalla:any, lista_eventos:list, fondo:any)->str:   

    #Renders y rects de las opciones
    render_jugar, rect_jugar = crear_render_y_rect("Desea jugar", (800, 250), BLACK)
    render_puntaje, rect_puntaje = crear_render_y_rect("Ver puntajes", (800,350), BLACK)
    render_salir, rect_salir = crear_render_y_rect("Salir", (800,450), BLACK)

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
    # Muestra fondo y opciones
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(render_jugar, rect_jugar)
    pantalla.blit(render_puntaje, rect_puntaje)
    pantalla.blit(render_salir, rect_salir)

    pygame.display.flip()

        
    return estado_menu



# Funcionalidad del juego, muestra la trivia, se encarga de los movimientos y toda la logica de las preguntas
def trivia(pantalla:any, preguntas_copia:list, posicion:int, fondo:any, jugador, tablero:list, imagen_puntos, imagen_temporizador, derrota_music, victoria_music)->tuple:
    
    # Inicializa la funcion de pedir nombre en una variable
    nombre = ingresar_nombre(pantalla,fondo).strip()

    #Bucle quue se encatga de conseguir la pregunta
    while len(preguntas_copia) > 0:

        pregunta_dict = sacar_pregunta_dict(preguntas_copia)
        opciones = sacar_opciones_pregunta_dict(pregunta_dict)
        respuesta_correcta = pregunta_dict["respuesta_correcta"]

        render_salir, rect_salir = crear_render_y_rect("Atrás", (65, 685), BLACK)

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


        

                # si clickeas en salir
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_salir.collidepoint(evento.pos):
                        guardar_datos(nombre, posicion)
                        return posicion, "menu"

                    
                    #Valida que se haya clickeado en las opciones (rects)
                    clic_valido = False
                    for letra, render_opcion, rect_opcion in opciones:
                        if rect_opcion.collidepoint(evento.pos):
                            posicion = mover(respuesta_correcta, posicion, evento.pos, tablero, opciones)
                            clic_valido = True
                            break
                    
                    #si fue validado, entonces calcula si ganaste,perdiste o continua
                    if clic_valido:
                        estado_juego = verificar_fin_juego(posicion, tablero)
                        if estado_juego == "Perdiste, vuelve a intentarlo":
                            pygame.mixer.music.stop()
                            derrota_music.play()

                        elif estado_juego == "Felicidades, ganastee!":
                            pygame.mixer.music.stop()
                            victoria_music.play()
    
                        if estado_juego != "continua":
                            mostrar_mensaje(pantalla, f"¡{estado_juego}!", fondo)
                            guardar_datos(nombre, posicion)

                            return posicion, "menu"
                        flag = False     






            
            #pantalla.fill(COLOR_CELESTE) 
            
            #Muestra las preguntas, opciones, reloj, puntaje y tablero  
            pantalla.blit(fondo, (0, 0))


            #
            render_pregunta, rect_pregunta = crear_render_y_rect(pregunta_dict["pregunta"], (800, 300), BLACK)
            pantalla.blit(render_pregunta,rect_pregunta)

            #Iteracion de la lista de tuplas para mostrar las opciones en pantalla
            for letra, render_opcion, rect_opcion in opciones:
                pantalla.blit(render_opcion, rect_opcion)

            #puntaje
            render_posicion, rect_posicion = crear_render_y_rect(str(posicion), (100, 100), BLACK)
            pantalla.blit(render_posicion,rect_posicion)

            pantalla.blit(imagen_puntos, (40, 80))  

            

            #opcion salir
            pantalla.blit(render_salir,rect_salir)

            dibujar_tablero(pantalla, tablero, posicion, jugador)

            # tiempo
            segundos = tiempo_restante // 1000
            render_timer, rect_timer = crear_render_y_rect(f"{segundos}", (1500, 100), BLACK)
            pantalla.blit(render_timer, rect_timer)

            pantalla.blit(imagen_temporizador, (1430, 75))

            pygame.display.flip()

    #Esto sucede cuando se acaban las preguntas
    pantalla.blit(fondo, (0, 0))
    render_fin, rect_fin = crear_render_y_rect("Se acabaron las preguntas!", (800, 400), BLACK)
    pantalla.blit(render_fin, rect_fin)
    pygame.display.flip()
    
    pygame.time.delay(2000)  # pausa 2 segundos
    guardar_datos(nombre, posicion)


    return posicion, "menu"


# Copia, mezcla la copiada y la retorna
def copiar_y_mezclar_lista(preguntas:list)->list:
    preguntas_copia = preguntas.copy()
    random.shuffle(preguntas_copia)
    return preguntas_copia

#Obtiene la pregunta copiada y le saca un elemento
def sacar_pregunta_dict(preguntas:list)->dict:
    pregunta_elegida = preguntas.pop()

    return pregunta_elegida

#Se encarga de procesar las opciones (respuestas) y devuelve sus rects
def sacar_opciones_pregunta_dict(pregunta:dict)->tuple:
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


#Encargado del movimiento de posicion
def mover( respuesta_correcta:str, posicion:int,evento_pos , tablero:list, opciones)->int:

    #Toma la respuesta correcta del dict elegido

    #Calcula la direccion y saltos
    operacion = calcular_direccion_base(opciones, evento_pos, respuesta_correcta)
    posicion += operacion
    # añade el salto tablero
    posicion = calcular_direccion_tablero(posicion, operacion, tablero)

    return posicion

#calcula salto base segun la respuesta
def calcular_direccion_base(opciones, evento_pos, respuesta_correcta):
    resultado = 0

    for letra, render, rect in opciones:
        if rect.collidepoint(evento_pos):
            if letra == respuesta_correcta:

                resultado += 1
            else:
                resultado += -1
    return resultado

#calcula salto adicional de tablero segun donde caiga
def calcular_direccion_tablero(posicion, calculo, tablero):
    salto_adicional = tablero[posicion]
    posicion += salto_adicional * calculo

    return posicion


# se encarga de todo el tablero, calcular las dimensioens de las casillas, sus colores y su muestra por pantalla
def dibujar_tablero(pantalla, tablero:list, posicion_jugador:int, jugador):
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
        else:
            color = VIOLET

        # Dibujar casilla
        rect = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(pantalla, color, rect)

        # Dibujar borde
        pygame.draw.rect(pantalla, BLACK, rect, 1)


        texto_valor, rect_valor = crear_render_y_rect(str(valor), rect.center, "Arial", BLACK)
        pantalla.blit(texto_valor, rect_valor)

        # Dibujar imagen del jugador
        if i == posicion_jugador:
            rect_centro = jugador.get_rect(center=rect.center)
            pantalla.blit(jugador, rect_centro)



#devuelve el resultado del juego segun la posicion dada
def verificar_fin_juego(posicion:int, tablero:list)->str:
    veredicto = "continua"
    if posicion <= 0:
        veredicto = "Perdistee"
    elif posicion >= len(tablero)-1:

        veredicto = "Ganastee"
    return veredicto

#Muestra el mensaje de cuando se queda sin preguntas
def mostrar_mensaje(pantalla, texto:str, fondo):
    pantalla.blit(fondo, (0, 0))
    render_mensaje, rect_mensaje = crear_render_y_rect(texto, (800, 400), BLACK)
    pantalla.blit(render_mensaje, rect_mensaje)
    pygame.display.flip()
    pygame.time.delay(3600)



# Guarda los datos en un csv
def guardar_datos(nombre_jugador: str, posicion: int):
    with open("puntaje.csv", "a", encoding="utf-8") as puntajes:
        puntajes.write(f"{nombre_jugador} || {posicion} puntos.\n")




#lee el archivo y lo devuelve 

def leer_obtener_puntajes():
    with open("puntaje.csv", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    return lineas

#desarma lo extraido del csv y lo ordena
def ordenar_puntajes(lineas:list)->list:
    puntajes = []
    for linea in lineas:
        partes = linea.strip().split()
        nombre = partes[0].strip()
        puntos = int(partes[2])
        puntajes.append([nombre, puntos])

    #ordena la lista puntajes
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

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando = False

        pantalla.blit(fondo, (0, 0))

        # Título
        titulo, rect_titulo = crear_render_y_rect("PUNTAJES", (800, 100), None, BLACK)
        pantalla.blit(titulo, rect_titulo)

        print(puntajes)
        # Mostrar cada puntaje
        y = 180
        for nombre, puntos in puntajes:
            texto = f"{nombre} - {puntos} puntos"
            render, rect = crear_render_y_rect(texto, (800, y), None, BLACK)
            pantalla.blit(render, rect)
            y += 50

        # Instruccion para volver
        volver, rect_volver = crear_render_y_rect("Presiona ESC para volver al menu", (800, 750), BLACK)
        pantalla.blit(volver, rect_volver)

        pygame.display.flip()


