import pygame
from configuracion import MARRON, CIAN, ANCHO, ALTO
plataformas = []
direcciones_plataformas = []
escaleras = []

escalera_img = None
plataforma_img = None

def crear_nivel(nivel):
    global plataformas, direcciones_plataformas, escaleras
    plataformas.clear()
    direcciones_plataformas.clear()
    escaleras.clear()
    if nivel == 1:
        plataformas.extend([
            pygame.Rect(200, 60, 450, 20),
            pygame.Rect(50, 180, 700, 20),
            pygame.Rect(45, 270, 600, 20),
            pygame.Rect(100, 370, 650, 20),
            pygame.Rect(60, 470, 680, 20),
            pygame.Rect(0, ALTO - 20, ANCHO, 20),
        ])
        direcciones_plataformas.extend([1, -1, 1, -1, 1, 1])
        escaleras.extend([
            pygame.Rect(220, 60, 40, 140),
            pygame.Rect(400, 180, 40, 90),
            pygame.Rect(600, 270, 40, 100),
            pygame.Rect(300, 370, 40, 100),
            pygame.Rect(700, 470, 40, 110),
        ])
    elif nivel == 2:
        plataformas.extend([
            pygame.Rect(200, 60, 200, 20),
            pygame.Rect(400, 60, 250, 20),
            pygame.Rect(50, 180, 300, 20),
            pygame.Rect(400, 180, 350, 20),
            pygame.Rect(45, 270, 200, 20),
            pygame.Rect(350, 270, 295, 20),
            pygame.Rect(100, 370, 650, 20),
            pygame.Rect(60, 470, 300, 20),
            pygame.Rect(400, 470, 340, 20),
            pygame.Rect(0, ALTO - 20, ANCHO, 20),
        ])
        direcciones_plataformas.extend([1, -1, 1, -1, 1, -1, 1, -1, 1, 1])
        escaleras.extend([
            pygame.Rect(220, 60, 40, 120),
            pygame.Rect(600, 60, 40, 120),
            pygame.Rect(400, 180, 40, 90),
            pygame.Rect(600, 270, 40, 100),
            pygame.Rect(300, 370, 40, 100),
            pygame.Rect(700, 470, 40, 110),
            pygame.Rect(100, 470, 40, 110),
        ])
    elif nivel == 3:
        plataformas.extend([
            pygame.Rect(100, 60, 600, 20),      
            pygame.Rect(50, 150, 700, 20),     
            pygame.Rect(120, 250, 680, 20),     
            pygame.Rect(50, 350, 700, 20),   
            pygame.Rect(200, 450, 440, 20),     
            pygame.Rect(0, ALTO - 20, ANCHO, 20),  
        ])
        escaleras.extend([
            pygame.Rect(600, 450, 40, 140),    
            pygame.Rect(220, 350, 40, 110),     
            pygame.Rect(600, 250, 40, 110),     
            pygame.Rect(120, 150, 40, 110),    
            pygame.Rect(390, 60, 40, 100),      
        ])

def dibujar(pantalla):
    global escalera_img, plataforma_img
    if escalera_img is None:
        escalera_img = pygame.image.load("img/escalera.png").convert_alpha()
    if plataforma_img is None:
        plataforma_img = pygame.image.load("img/plataforma.jpg").convert_alpha()
    for escalera in escaleras:
        img_escalada = pygame.transform.scale(escalera_img, (escalera.width, escalera.height))
        pantalla.blit(img_escalada, escalera.topleft)
    for plataforma in plataformas:
        img_plat = pygame.transform.scale(plataforma_img, (plataforma.width, plataforma.height))
        pantalla.blit(img_plat, plataforma.topleft)