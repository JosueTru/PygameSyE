import pygame
import colores
from main import *

botones = [
    {"texto": texto_jugar, "rect": rect_jugar, "accion": "Jugar"},
    {"texto": texto_puntaje, "rect": rect_puntaje, "accion": "Puntajes"},
    {"texto": texto_salir, "rect": rect_salir, "accion": "Salir"}
]