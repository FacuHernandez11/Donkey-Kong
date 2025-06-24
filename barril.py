import pygame
import random
from configuracion import NARANJA, GRAVEDAD
from nivel import plataformas, direcciones_plataformas
from personaje import donkey_kong

class Barril:
    COLOR = NARANJA

    def __init__(self):
        self.plat_idx = random.choice([0, 1])
        plat = plataformas[self.plat_idx]
        x = donkey_kong["rect"].centerx if self.plat_idx == 0 else plat.left + 10
        self.rect = pygame.Rect(x, plat.top - 20, 20, 20)
        self.dir = direcciones_plataformas[self.plat_idx]
        self.vel_y = 0
        self.fall = False
        self.radio = 10
        self.velocidad_horizontal = 3
        self.puede_rotar = random.choice([True, False])

    def en_plataforma(self, plat):
        return plat.left <= self.rect.centerx <= plat.right

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            next_idx = self.plat_idx + 1  
            if next_idx < len(plataformas):
                next_plat = plataformas[next_idx]
                if self.rect.bottom >= next_plat.top:
                    self.rect.bottom = next_plat.top
                    self.plat_idx = next_idx
                    if self.puede_rotar and random.random() < 0.5:
                        self.dir *= -1
                    else:
                        self.dir = direcciones_plataformas[self.plat_idx]
                    self.fall = False
                    self.vel_y = 0
        else:
            self.rect.x += self.velocidad_horizontal * self.dir
            plat = plataformas[self.plat_idx]
            if self.rect.left < plat.left or self.rect.right > plat.right:
                if self.dir == 1:
                    self.rect.right = plat.right
                else:
                    self.rect.left = plat.left
                self.fall = True
                self.vel_y = 0

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.COLOR, self.rect.center, self.radio)

    def colisiona_con(self, rect):
        dx = self.rect.centerx - rect.centerx
        dy = self.rect.centery - rect.centery
        distancia = dx ** 2 + dy ** 2
        return distancia < (self.radio + rect.width // 2) ** 2

    def esta_fuera_de_pantalla(self):
        return self.rect.top > 600

class BarrilRapido(Barril):
    COLOR = (255, 0, 0)

    def __init__(self):
        super().__init__()
        self.velocidad_horizontal = 6

class BarrilLento(Barril):
    COLOR = (0, 255, 0)

    def __init__(self):
        super().__init__()
        self.velocidad_horizontal = 2

class BarrilRebotador(Barril):
    COLOR = (0, 0, 255)

    def __init__(self):
        super().__init__()
        self.velocidad_horizontal = 4
        self.rebote_fuerza = -10
        self.rebotando = False

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            next_idx = self.plat_idx + 1
            if next_idx < len(plataformas):
                next_plat = plataformas[next_idx]
                if self.rect.bottom >= next_plat.top:
                    self.rect.bottom = next_plat.top
                    self.plat_idx = next_idx
                    if self.puede_rotar and random.random() < 0.5:
                        self.dir *= -1
                    else:
                        self.dir = direcciones_plataformas[self.plat_idx]
                    self.fall = False
                    self.vel_y = 0
        else:
            self.rect.x += self.velocidad_horizontal * self.dir
            
            if not self.rebotando and self.rect.bottom == plataformas[self.plat_idx].top:
                self.vel_y = self.rebote_fuerza
                self.rebotando = True
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y
            if self.rect.bottom >= plataformas[self.plat_idx].top:
                self.rect.bottom = plataformas[self.plat_idx].top
                self.vel_y = 0
                self.rebotando = False

            plat = plataformas[self.plat_idx]
            if self.rect.left < plat.left or self.rect.right > plat.right:
                if self.dir == 1:
                    self.rect.right = plat.right
                else:
                    self.rect.left = plat.left
                self.fall = True
                self.vel_y = 0