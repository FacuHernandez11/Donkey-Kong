import pygame
import random
from configuracion import NARANJA, GRAVEDAD
from nivel import plataformas, direcciones_plataformas, escaleras

class Barril:
    COLOR = NARANJA

    def __init__(self):
        plat = plataformas[0]
        x = plat.left + 20
        y = plat.top
        self.rect = pygame.Rect(x, y - 20, 20, 20)
        self.plat_idx = 0
        self.rect.bottom = plataformas[self.plat_idx].top
        self.dir = direcciones_plataformas[self.plat_idx]
        self.vel_y = 0
        self.fall = False
        self.radio = 10
        self.velocidad_horizontal = 3
        self.morir = False

    def en_plataforma(self, plat, margen=2):
        return plat.left - margen <= self.rect.centerx <= plat.right + margen

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            next_idx = self.plat_idx + 1
            if next_idx < len(plataformas):
                next_plat = plataformas[next_idx]
                if self.rect.bottom >= next_plat.top and self.en_plataforma(next_plat):
                    self.rect.bottom = next_plat.top
                    self.plat_idx = next_idx
                    self.dir = direcciones_plataformas[self.plat_idx]
                    self.fall = False
                    self.vel_y = 0
            else:
                if self.rect.top > 600:
                    self.morir = True
        else:
            self.rect.x += self.velocidad_horizontal * self.dir
            plat = plataformas[self.plat_idx]

            if self.dir == 1 and self.rect.right >= plat.right:
                self.rect.right = plat.right
                self.fall = True
                self.vel_y = 0
                return
            elif self.dir == -1 and self.rect.left <= plat.left:
                self.rect.left = plat.left
                self.fall = True
                self.vel_y = 0
                return

            if self.COLOR == NARANJA:
                for escalera in escaleras:
                    margen_x = 10
                    margen_y = 5
                    if (escalera.left - margen_x <= self.rect.centerx <= escalera.right + margen_x and
                        abs(self.rect.bottom - escalera.top) <= margen_y):
                        if random.random() < 0.02:
                            self.fall = True
                            self.vel_y = 2
                            return

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
        self.morir = False

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            next_idx = self.plat_idx + 1
            if next_idx < len(plataformas):
                next_plat = plataformas[next_idx]
                if self.rect.bottom >= next_plat.top and self.en_plataforma(next_plat):
                    self.rect.bottom = next_plat.top
                    self.plat_idx = next_idx
                    self.dir = direcciones_plataformas[self.plat_idx]
                    self.fall = False
                    self.vel_y = 0
                    self.rebotando = False
            else:
                if self.rect.top > 600:
                    self.morir = True
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

            if self.dir == 1 and self.rect.right >= plat.right:
                self.rect.right = plat.right
                self.fall = True
                self.vel_y = 0
                return
            elif self.dir == -1 and self.rect.left <= plat.left:
                self.rect.left = plat.left
                self.fall = True
                self.vel_y = 0
                return
