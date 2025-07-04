import pygame
from colores import *
from funciones import *
from preguntas import *

posicion = {"valor": 15}

pygame.init()
pygame.display.set_caption("Mi Juego")
pantalla = pygame.display.set_mode((1400,900))


preguntas_copia = copiar_y_mezclar(preguntas)


nombre_jugador = ingresar_nombre(pantalla)
print("Nombre ingresado:", nombre_jugador)


#font_menu = pygame.font.SysFont("Arial", 30)

texto_jugar = crear_texto("Desea jugar")
rect_jugar = crear_rect(texto_jugar, (250,150))

texto_puntaje = crear_texto("Puntajes")
rect_puntaje = crear_rect(texto_puntaje, (250, 220))

texto_salir = crear_texto("Salir")
rect_salir = crear_rect(texto_salir, (250, 290))



flag_correr = True
while flag_correr:
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            print("cerrando juegooo")
            guardar_datos(nombre_jugador, posicion["valor"])

            flag_correr = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_jugar.collidepoint(evento.pos):
                resultado = trivia(pantalla, preguntas_copia, posicion)
                if resultado == "gano":
                    print("¡Ganaste el juego!")
                    guardar_datos(nombre_jugador, posicion["valor"])

                    flag_correr = False
                elif resultado == "perdio":
                    print("Perdiste el juego.")
                    guardar_datos(nombre_jugador, posicion["valor"])

                    flag_correr = False

            if rect_puntaje.collidepoint(evento.pos):
                print("Apretaste puntajee")
            if rect_salir.collidepoint(evento.pos):
                print("Apretaste Salir")
                flag_correr = False
                guardar_datos(nombre_jugador, posicion["valor"])








    pantalla.fill(BLACK)

    pantalla.blit(texto_jugar, rect_jugar)
    pantalla.blit(texto_puntaje, rect_puntaje)
    pantalla.blit(texto_salir, rect_salir)


    pygame.display.flip()

pygame.quit()


















""" font_input = pygame.font.SysFont("Arial", 30)
ingreso = ""
ingreso_rect = pygame.Rect(100,200,150,40)


letra_a = pygame.image.load("./a.jpg")
letra_a = pygame.transform.scale(letra_a, (50,50))
rect_a = letra_a.get_rect()

rect_a.x = 80
rect_a.y = 400

letra_b = pygame.image.load("./b.jpg")
letra_b = pygame.transform.scale(letra_b, (50,50))
rect_b = letra_b.get_rect()

rect_b.x = 220
rect_b.y = 400

letra_c = pygame.image.load("./c.png")
letra_c = pygame.transform.scale(letra_c, (50,50))
rect_c = letra_c.get_rect()

rect_c.x = 380
rect_c.y = 400

estado_juego = "menu"

flag_correr = True

while flag_correr:



    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            print("Cerrando el juegoo")
            flag_correr = False


        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_a.collidepoint(evento.pos):
                print("APRETASTE EL A")
            elif rect_b.collidepoint(evento.pos):
                print("apretaste b")
            elif rect_c.collidepoint(evento.pos):
                print("apretaste c")
            
            print(evento.pos)
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                ingreso = ingreso[0:-1]
            else:
                ingreso += evento.unicode

        if estado_juego == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_jugar.collidepoint(evento.pos):
                    estado_juego = "jugando"
                elif rect_puntajes.collidepoint(evento.pos):
                    print("Mostrar puntajes (aún no implementado)")
                elif rect_salir.collidepoint(evento.pos):
                    flag_correr = False


    pantalla.fill(colores.DARKSLATEBLUE)
    
    if estado_juego == "menu":
        font_menu = pygame.font.SysFont("Arial", 40)
        texto_jugar = font_menu.render("Desea jugar", True, colores.BLACK)
        texto_puntajes = font_menu.render("Ver puntajes", True, colores.BLACK)
        texto_salir = font_menu.render("Salir", True, colores.BLACK)

        rect_jugar = texto_jugar.get_rect(center=(250, 150))
        rect_puntajes = texto_puntajes.get_rect(center=(250, 220))
        rect_salir = texto_salir.get_rect(center=(250, 290))

        pantalla.blit(texto_jugar, rect_jugar)
        pantalla.blit(texto_puntajes, rect_puntajes)
        pantalla.blit(texto_salir, rect_salir)
    elif estado_juego == "jugando":
        jugar(pantalla, letra_a, letra_b, letra_c, rect_a, rect_b, rect_c, ingreso_rect, font_input, ingreso)

    pygame.display.flip()


pygame.quit() """




"""  pantalla.fill(colores.DARKVIOLET)
    
    #pantalla.blit(foto, (50,50))

    pantalla.blit(letra_a, (80,400))
    pantalla.blit(letra_b, (220,400))
    pantalla.blit(letra_c, (380,400))


    #print("ingreso: ", ingreso)

    pygame.draw.rect(pantalla, colores.BLACK, ingreso_rect, 2)
    font_input_surface = font_input.render(ingreso, True, colores.BLACK)
    pantalla.blit(font_input_surface, (ingreso_rect.x+5, ingreso_rect.y+5))

    pygame.display.flip() """


