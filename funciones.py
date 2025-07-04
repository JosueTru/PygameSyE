import pygame
import colores
import random
import preguntas

tablero = [0,1,0,0,0,3,0,0,0,0,0,1,0,1,2,1,1,0,0,0,1,0,0,2,0,0,0,1,0,0,0]
posicion = 15


def crear_texto(texto:str, color= colores.WHITE, tamaño=30,  fuente:str="Arial" )->any:
    fuente = pygame.font.SysFont(fuente, tamaño)
    texto_render = fuente.render(texto, True, color) 
    return texto_render


def crear_rect(texto_render:str, centro=(0,0))->any:
    rect = texto_render.get_rect(center=centro)
    return rect




def dibujar_textos(pantalla, lista_elementos:list):
    for texto_render, rect in lista_elementos:
        pantalla.blit(texto_render, rect)


# Funciones logica

def copiar_lista(preguntas:list)->list:
    preguntas_copia = preguntas.copy()
    return preguntas_copia

def mezclar(preguntas_copia:list):
    random.shuffle(preguntas_copia)
    return preguntas_copia


def sacar_pregunta(preguntas:list)->dict:
    pregunta_elegida = preguntas.pop()

    return pregunta_elegida

def copiar_y_mezclar(preguntas):
    lista_copiada = copiar_lista(preguntas)
    lista_copiada_mezclada = mezclar(lista_copiada)

    return lista_copiada_mezclada






def posicion_a_pixel(posicion_valor):
    min_x = 200
    max_x = 1200
    max_pos = len(tablero) - 1
    x = min_x + (posicion_valor / max_pos) * (max_x - min_x)
    return int(x)


def calcular_direccion_base(respuesta:str, respuesta_correcta:str) -> int:
    if respuesta == respuesta_correcta:
        print("-CORRECTO-")
        return 1
    else:
        print("-INCORRECTO-")
        return -1

def calcular_direccion_tablero(posicion:int, tablero:list, operacion:int) -> int:
    salto_adicional = tablero[posicion]
    # Mover hacia la dirección con el salto adicional
    posicion += salto_adicional * operacion
    return posicion

def mover(posicion: dict, respuesta_usuario: str, respuesta_correcta: str, tablero: list) -> int:
    operacion = calcular_direccion_base(respuesta_usuario, respuesta_correcta)

    # avanzar o retroceder 1
    posicion["valor"] += operacion

    #llimitar que no se salga del tablero antes de calcular salto extra
    #posicion["valor"] = max(0, min(posicion["valor"], len(tablero) - 1))

    # calcular salto adicional según tablero
    posicion["valor"] = calcular_direccion_tablero(posicion["valor"], tablero, operacion)

    # limitar que no se salga del tablero después del salto
    #posicion["valor"] = max(0, min(posicion["valor"], len(tablero) - 1))

    print(f"Tu posición actual es {posicion['valor']} !")

    return posicion["valor"]


def verificar_estado_juego(posicion, tablero):
    if posicion <= 0:
        print("Perdiste. Volvé a intentarlo.")
        return "perdio"
    elif posicion >= len(tablero) - 1:
        print("¡FELICIDADES, GANASTE!")
        return "gano"
    else:
        return "continua"


def trivia(pantalla, preguntas_copia, posicion):
    while len(preguntas_copia) > 0:
        pregunta = sacar_pregunta(preguntas_copia)

        texto_pregunta = crear_texto(pregunta["pregunta"])
        rect_pregunta = crear_rect(texto_pregunta, (700, 150))
        lista_pregunta = [(texto_pregunta, rect_pregunta)]

        lista_opciones, rects_opciones = crear_elementos_opciones(pregunta)
        respuesta_correcta = pregunta["respuesta_correcta"]

        jugando = True
        while jugando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()


                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_click = evento.pos
                    for letra, rect in rects_opciones.items():
                        print(letra, rect)
                        if rect.collidepoint(pos_click):
                            mover(posicion, letra, respuesta_correcta, tablero)
                            estado = verificar_estado_juego(posicion["valor"], tablero)
                            if estado in ["gano", "perdio"]:
                                jugando = False
                                return estado  # termina la trivia aca
                            jugando = False
                            break

            pantalla.fill((0, 0, 0))
            dibujar_textos(pantalla, lista_pregunta + lista_opciones)

            pos_x = posicion_a_pixel(posicion["valor"])
            texto_pos = crear_texto(f"Posición: {posicion['valor']}")
            rect_pos = crear_rect(texto_pos, (pos_x, 850))
            pantalla.blit(texto_pos, rect_pos)

            pygame.display.flip()




        

def crear_elementos_opciones(pregunta_dict):
    letras = ["a", "b", "c"]
    posiciones_x = [350, 800, 1250]
    y = 250

    lista_tuplas = []
    rects_opciones = {}

    for i in range(len(letras)):
        letra = letras[i]

        # Armo el texto de las opciones (a,b,c) y sus respuestas 
        texto = f"{letra.upper()}) {pregunta_dict[f'respuesta_{letra}']}"

        #Creo texto render y su rect
        texto_render = crear_texto(texto)
        rect = crear_rect(texto_render, (posiciones_x[i], y))

        #lleno la lista con los textos render y rects, en tuplas para usar la funcion dibujar
        lista_tuplas.append((texto_render, rect))

        #lleno la llave para guardar los rects con sus respectivas letras
        rects_opciones[letra] = rect

    #devuelvo una tupla de listas y llaves
    return lista_tuplas, rects_opciones





def ingresar_nombre(pantalla):
    nombre = ""

    input_activo = True
    while input_activo:
        pantalla.fill(colores.BLACK)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[0:-1]
                else:
                    nombre += evento.unicode
                if evento.key == pygame.K_RETURN:
                    input_activo = False
                    


        # Render del texto
        texto_titulo = crear_texto("Ingrese su nombre:")
        rect_titulo = crear_rect(texto_titulo, (400, 250))


        texto_nombre = crear_texto(nombre)
        rect_nombre = crear_rect(texto_nombre, (400, 300))



        dibujar_textos(pantalla, [
        (texto_titulo, rect_titulo),
        (texto_nombre, rect_nombre)])

        pygame.display.flip()
   
    return nombre






def guardar_datos(nombre_jugador: str, posicion: int):
    with open("puntaje.csv", "a", encoding="utf-8") as puntajes:
        puntajes.write(f"{nombre_jugador} || {posicion} puntos.\n")