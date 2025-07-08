import pygame
from colores import *
from funciones import *
from preguntas import *
from datos import *
import pygame.mixer as mixer
mixer.init()
mixer.music.load('./musica.mp3')
mixer.music.set_volume(volumen_por_defecto)
mixer.music.play()


derrota_music = mixer.Sound("derrota.mp3")
derrota_music.set_volume(0.1)
victoria_music = mixer.Sound("ganaste.mp3")
victoria_music.set_volume(0.1)


def main(posicion, tablero):
    posicion_inicial = posicion["valor"]

    pygame.init()

    
    pygame.display.set_caption("Serpientes y escaleras")
    pantalla = pygame.display.set_mode(tamaño_pantalla)
    clock = pygame.time.Clock()

    fondo = pygame.image.load("fondo.jpeg").convert()
    fondo = pygame.transform.scale(fondo, tamaño_pantalla)

    imagen_jugador = pygame.image.load("mariox.png").convert_alpha()
    imagen_jugador = pygame.transform.scale(imagen_jugador, tamaño_jugador)

    imagen_puntos = pygame.image.load("moneda.png").convert_alpha()
    imagen_puntos = pygame.transform.scale(imagen_puntos, tamaño_moneda)

    imagen_temporizador = pygame.image.load("temporizador.png").convert_alpha()
    imagen_temporizador = pygame.transform.scale(imagen_temporizador, tamaño_tempo)

    estado = "menu"
    flag_correr = True
    while flag_correr:
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                estado = "salir"   
                
            if estado == "menu":
                if not mixer.music.get_busy():
                    mixer.music.load("musica.mp3")
                    mixer.music.set_volume(0.1)
                    mixer.music.play(1)

                estado = menu(pantalla, lista_eventos, fondo)

            elif estado == "trivia":
                copia_mezclada_preguntas = copiar_y_mezclar_lista(preguntas)
                posicion, estado = trivia(pantalla, copia_mezclada_preguntas, posicion_inicial, fondo, imagen_jugador,tablero, imagen_puntos, imagen_temporizador, derrota_music, victoria_music)
                
            elif estado == "salir":
                flag_correr = False





            
            clock.tick(60)
        

    pygame.quit()

main(posicion, tablero)