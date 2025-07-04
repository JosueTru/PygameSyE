import pygame
import colores
import random
import preguntas

tablero = [0,1,0,0,0,3,0,0,0,0,0,1,0,0,2,1,1,0,0,0,1,0,0,2,0,0,0,1,0,0,0]


def crear_texto(texto:str, color= colores.WHITE, tamaño=30,  fuente:str="Arial" )->any:
    fuente = pygame.font.SysFont(fuente, tamaño)
    texto_render = fuente.render(texto, True, color) 
    return texto_render


def crear_rect(texto_render, centro=(0,0)):
    rect = texto_render.get_rect(center=centro)
    return rect




def dibujar_textos(pantalla, lista_elementos):
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






def trivia(pantalla, preguntas_copia):

    
    while len(preguntas_copia) > 0:

        pregunta = sacar_pregunta(preguntas_copia)

        # Crear texto y rectángulo de la pregunta

        texto_pregunta = crear_texto(pregunta["pregunta"])
        rect_pregunta = crear_rect(texto_pregunta, (700, 150))


        texto_pregunta = crear_texto(pregunta["pregunta"])
        rect_pregunta = crear_rect(texto_pregunta, (700, 150))
        lista_pregunta = [(texto_pregunta, rect_pregunta)]
        lista_opciones = crear_elementos_opciones(pregunta)



        jugando = True
        while jugando:
            for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()

                
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        posicion = evento.pos
                        jugando = False

        
            pantalla.fill((0,0,0))
            #dibujar_textos(pantalla, [(texto_pregunta, rect_pregunta)])
            dibujar_textos(pantalla, lista_pregunta + lista_opciones)

            pygame.display.flip()



        print(pregunta["pregunta"])
        print(len(preguntas_copia))



        

def crear_elementos_opciones(pregunta_dict):
    letras = ["a", "b", "c"]
    posiciones_x = [350, 800, 1250]
    y = 250

    lista_tuplas = []

    for i in range(len(letras)):
        letra = letras[i]
        texto = f"{letra.upper()}) {pregunta_dict[f'respuesta_{letra}']}"
        texto_render = crear_texto(texto)
        rect = crear_rect(texto_render, (posiciones_x[i], y))

        lista_tuplas.append((texto_render, rect))

    return lista_tuplas





def ingresar_nombre(pantalla):
    nombre = ""
    font = pygame.font.SysFont("Arial", 30)
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
        rect_titulo = crear_rect(texto_titulo, (200, 150))


        texto_nombre = crear_texto(nombre)
        rect_nombre = crear_rect(texto_nombre, (200, 200))



        dibujar_textos(pantalla, [
        (texto_titulo, rect_titulo),
        (texto_nombre, rect_nombre)])

        pygame.display.flip()
   
    return nombre






