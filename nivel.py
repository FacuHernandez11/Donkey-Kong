import pygame
from configuracion import MARRON, CIAN, ANCHO, ALTO


plataformas = [
    pygame.Rect(200, 100, 450, 20),   
    pygame.Rect(50, 180, 700, 20),
    pygame.Rect(45, 270, 600, 20),
    pygame.Rect(100, 370, 650, 20),
    pygame.Rect(60, 470, 680, 20),
    pygame.Rect(0, ALTO - 20, ANCHO, 20),  
]


direcciones_plataformas = [1, -1, 1, -1, 1, 1]


escaleras = [
    pygame.Rect(220, 100, 40, 80),    
    pygame.Rect(400, 180, 40, 90),    
    pygame.Rect(600, 270, 40, 100),   
    pygame.Rect(300, 370, 40, 100),   
    pygame.Rect(700, 470, 40, 110),   
]

def dibujar(pantalla):
    for plataforma in plataformas:
        pygame.draw.rect(pantalla, MARRON, plataforma)
    for escalera in escaleras:
        pygame.draw.rect(pantalla, CIAN, escalera)
