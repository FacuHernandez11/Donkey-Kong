import pygame
import random
from configuracion import NARANJA, GRAVEDAD
from nivel import plataformas, direcciones_plataformas
from personaje import donkey_kong

class Barril:
    COLOR = NARANJA

    def __init__(self):
        self.plat_idx = 0
        plat = plataformas[self.plat_idx]
        x = donkey_kong["rect"].centerx
        self.rect = pygame.Rect(x, plat.top - 20, 20, 20)
        self.dir = direcciones_plataformas[self.plat_idx]
        self.vel_y = 0
        self.fall = False
        self.radio = 10
        self.velocidad_horizontal = 3

    def en_plataforma(self, plat):
        # Devuelve True si está centrado sobre la plataforma
        return plat.left <= self.rect.centerx <= plat.right

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            if self.plat_idx + 1 < len(plataformas):
                siguiente = plataformas[self.plat_idx + 1]
                if self.rect.bottom >= siguiente.top and self.en_plataforma(siguiente):
                    self.rect.bottom = siguiente.top
                    self.plat_idx += 1
                    self.dir = direcciones_plataformas[self.plat_idx]
                    self.vel_y = 0
                    self.fall = False
                    if random.random() < 0.3:
                        self.dir *= -1
        else:
            self.rect.x += self.velocidad_horizontal * self.dir
            plat = plataformas[self.plat_idx]
            if self.rect.left < plat.left or self.rect.right > plat.right:
                self.fall = True

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
        self.rebote_fuerza = -6

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            if self.plat_idx + 1 < len(plataformas):
                siguiente = plataformas[self.plat_idx + 1]
                if self.rect.bottom >= siguiente.top and self.en_plataforma(siguiente):
                    self.rect.bottom = siguiente.top
                    self.plat_idx += 1
                    self.dir = direcciones_plataformas[self.plat_idx]
                    self.vel_y = self.rebote_fuerza  # rebote vertical
                    self.fall = False
                    if random.random() < 0.3:
                        self.dir *= -1
        else:
            self.rect.x += self.velocidad_horizontal * self.dir
            plat = plataformas[self.plat_idx]
            if self.rect.left < plat.left or self.rect.right > plat.right:
                self.dir *= -1  # rebote lateral
                self.fall = True
