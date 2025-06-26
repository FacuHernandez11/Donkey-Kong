import pygame
from configuracion import MARRON, CIAN, ANCHO, ALTO

plataformas = []
direcciones_plataformas = []
escaleras = []

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
            pygame.Rect(100, 60, 600, 20),     # y=60
            pygame.Rect(50, 150, 700, 20),     # y=150
            pygame.Rect(150, 250, 650, 20),    # y=250
            pygame.Rect(50, 350, 700, 20),     # y=350
            pygame.Rect(200, 450, 440, 20),    # y=450
            pygame.Rect(0, ALTO - 20, ANCHO, 20),  # y=580
        ])
        escaleras.extend([
            # Escalera 1: conecta plataforma 0 (y=60) y 1 (y=150)
            pygame.Rect(390, 70, 40, 100),      # y=70, alto=100 → llega a y=170 (20px sobre la plataforma de y=150)
            # Escalera 2: conecta plataforma 1 (y=150) y 2 (y=250)
            pygame.Rect(120, 170, 40, 110),     # y=170, alto=110 → llega a y=280 (30px sobre la plataforma de y=250)
            # Escalera 3: conecta plataforma 2 (y=250) y 3 (y=350)
            pygame.Rect(600, 270, 40, 110),     # y=270, alto=110 → llega a y=380 (30px sobre la plataforma de y=350)
            # Escalera 4: conecta plataforma 3 (y=350) y 4 (y=450) (ya funciona bien)
            pygame.Rect(220, 370, 40, 110),     # y=370, alto=110 → llega a y=480 (30px sobre la plataforma de y=450)
            # Escalera 5: conecta plataforma 4 (y=450) y suelo (y=580) (ya funciona bien)
            pygame.Rect(600, 450, 40, 140),     # y=450, alto=140 → llega a y=590 (10px sobre el suelo)
        ])

def dibujar(pantalla):
    for escalera in escaleras:
        pygame.draw.rect(pantalla, CIAN, escalera)
    for plataforma in plataformas:
        pygame.draw.rect(pantalla, MARRON, plataforma)