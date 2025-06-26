import pygame
import random
from configuracion import NARANJA, GRAVEDAD
from nivel import plataformas, escaleras

class Barril:
    COLOR = NARANJA

    def __init__(self, x, y, dir=1):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.radio = 10
        self.dir = dir
        self.velocidad_horizontal = 3
        self.vel_y = 0
        self.fall = False
        self.morir = False

        for plat in plataformas:
            if plat.left <= self.rect.centerx <= plat.right:
                self.rect.bottom = plat.top
                self.plat_idx = plataformas.index(plat)
                break
        else:
            self.plat_idx = 0

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            for idx in range(self.plat_idx + 1, len(plataformas)):
                plat = plataformas[idx]
                if (plat.left - 5 <= self.rect.centerx <= plat.right + 5 and
                    self.rect.bottom >= plat.top):
                    self.rect.bottom = plat.top
                    self.plat_idx = idx
                    self.fall = False
                    self.vel_y = 0
                    return

            if self.rect.top > 600:
                self.morir = True

        else:
            plat = plataformas[self.plat_idx]
            self.rect.x += self.velocidad_horizontal * self.dir

            if self.dir == 1 and self.rect.right >= plat.right:
                self.rect.right = plat.right
                self.fall = True
                self.vel_y = 2
                return
            elif self.dir == -1 and self.rect.left <= plat.left:
                self.rect.left = plat.left
                self.fall = True
                self.vel_y = 2
                return
            if self.COLOR == NARANJA:
                for esc in escaleras:
                    if (esc.left - 10 <= self.rect.centerx <= esc.right + 10 and
                        abs(self.rect.bottom - esc.top) <= 5 and
                        random.random() < 0.02):
                        self.fall = True
                        self.vel_y = 2
                        return

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.COLOR, self.rect.center, self.radio)

    def colisiona_con(self, rect):
        dx = self.rect.centerx - rect.centerx
        dy = self.rect.centery - rect.centery
        return dx*dx + dy*dy < (self.radio + rect.width//2)**2

    def esta_fuera_de_pantalla(self):
        return self.morir or self.rect.top > 600


class BarrilRapido(Barril):
    COLOR = (255, 0, 0)
    def __init__(self, x, y, dir=1):
        super().__init__(x, y, dir)
        self.velocidad_horizontal = 6

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            for idx in range(self.plat_idx + 1, len(plataformas)):
                plat = plataformas[idx]
                if (plat.left - 5 <= self.rect.centerx <= plat.right + 5 and
                    self.rect.bottom >= plat.top):
                    self.rect.bottom = plat.top
                    self.plat_idx = idx
                    self.fall = False
                    self.vel_y = 0
                    self.dir *= -1  
                    return

            if self.rect.top > 600:
                self.morir = True

        else:
            plat = plataformas[self.plat_idx]
            self.rect.x += self.velocidad_horizontal * self.dir

            if self.dir == 1 and self.rect.right >= plat.right:
                self.rect.right = plat.right
                self.fall = True
                self.vel_y = 2
                return
            elif self.dir == -1 and self.rect.left <= plat.left:
                self.rect.left = plat.left
                self.fall = True
                self.vel_y = 2
                return


class BarrilLento(Barril):
    COLOR = (0, 255, 0)
    def __init__(self, x, y, dir=1):
        super().__init__(x, y, dir)
        self.velocidad_horizontal = 2


class BarrilRebotador(Barril):
    COLOR = (0, 0, 255)
    def __init__(self, x, y, dir=1):
        self.rebotando = False  
        super().__init__(x, y, dir)
        self.velocidad_horizontal = 4
        self.rebote_fuerza = -10

    def actualizar(self):
        if not self.fall:
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
                self.vel_y = 2
                return
            elif self.dir == -1 and self.rect.left <= plat.left:
                self.rect.left = plat.left
                self.fall = True
                self.vel_y = 2
                return
        else:
            super().actualizar()

class BarrilNivel1(Barril):
    COLOR = NARANJA
    def __init__(self, x, y, dir=1):
        super().__init__(x, y, dir)

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            for idx in range(self.plat_idx + 1, len(plataformas)):
                plat = plataformas[idx]
                if (plat.left - 5 <= self.rect.centerx <= plat.right + 5 and
                    self.rect.bottom >= plat.top):
                    self.rect.bottom = plat.top
                    self.plat_idx = idx
                    self.fall = False
                    self.vel_y = 0
                    self.dir *= -1  
                    return

            if self.rect.top > 600:
                self.morir = True

        else:
            plat = plataformas[self.plat_idx]
            self.rect.x += self.velocidad_horizontal * self.dir

            if self.dir == 1 and self.rect.right >= plat.right:
                self.rect.right = plat.right
                self.fall = True
                self.vel_y = 2
                return
            elif self.dir == -1 and self.rect.left <= plat.left:
                self.rect.left = plat.left
                self.fall = True
                self.vel_y = 2
                return

class BarrilNivel2(Barril):
    COLOR = (255, 165, 0)

    def __init__(self, x, y, dir=1):
        super().__init__(x, y, dir)
        self.velocidad_horizontal = 3

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            salto = 1
            if random.random() < 0.25 and self.plat_idx + 2 < len(plataformas):
                salto = 2

            aterrizo = False
            for idx in range(self.plat_idx + 1, min(self.plat_idx + salto + 1, len(plataformas))):
                plat = plataformas[idx]
                if (plat.left - 15 <= self.rect.centerx <= plat.right + 15 and
                    self.rect.bottom >= plat.top):
                    self.rect.bottom = plat.top
                    self.plat_idx = idx
                    self.fall = False
                    self.vel_y = 0
                    self.dir *= -1
                    if random.random() < 0.15:
                        self.dir *= -1
                    aterrizo = True
                    break

            if not aterrizo:
                self.fall = False
                self.vel_y = 0

        else:
            plat = plataformas[self.plat_idx]
            self.rect.x += self.velocidad_horizontal * self.dir

            borde = (self.rect.right >= plat.right and self.dir == 1) or (self.rect.left <= plat.left and self.dir == -1)
            if borde:
                hay_plataforma_debajo = False
                for idx in range(self.plat_idx + 1, len(plataformas)):
                    next_plat = plataformas[idx]
                    if next_plat.left - 15 <= self.rect.centerx <= next_plat.right + 15:
                        hay_plataforma_debajo = True
                        break
                if hay_plataforma_debajo:
                    if self.dir == 1:
                        self.rect.right = plat.right
                    else:
                        self.rect.left = plat.left
                    self.fall = True
                    self.vel_y = 2
                    return
                else:
                    if self.dir == 1:
                        self.rect.right = plat.right
                    else:
                        self.rect.left = plat.left
                    return
