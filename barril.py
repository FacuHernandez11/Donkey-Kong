import pygame
import random
from configuracion import NARANJA, GRAVEDAD
from nivel import plataformas, direcciones_plataformas
from personaje import donkey_kong

class Barril:
    def __init__(self):
        self.plat_idx = 0
        plat = plataformas[self.plat_idx]
        self.rect = pygame.Rect(donkey_kong["rect"].centerx, plat.top - 20, 20, 20)
        self.dir = random.choice([1, -1])
        self.fall = False
        self.vel_y = 0
        self.radio = 10

    def actualizar(self):
        if self.fall:
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y
            if self.plat_idx + 1 < len(plataformas):
                sig_plat = plataformas[self.plat_idx + 1]
                if self.rect.colliderect(sig_plat) and self.vel_y >= 0:
                    self.rect.bottom = sig_plat.top
                    self.plat_idx += 1
                    self.dir = random.choice([1, -1])
                    self.fall = False
                    self.vel_y = 0
        else:
            self.rect.x += 5 * self.dir
            plat = plataformas[self.plat_idx]
            if self.rect.right > plat.right or self.rect.left < plat.left:
                if self.plat_idx + 1 < len(plataformas):
                    if random.random() < 0.5:
                        self.fall = True
                    else:
                        self.dir *= -1
                        if self.rect.right > plat.right:
                            self.rect.right = plat.right
                        if self.rect.left < plat.left:
                            self.rect.left = plat.left
                else:
                    self.dir *= -1
                    if self.rect.right > plat.right:
                        self.rect.right = plat.right
                    if self.rect.left < plat.left:
                        self.rect.left = plat.left

    def dibujar(self, pantalla):
        color1 = NARANJA
        color2 = (255, 200, 0)
        frame = (pygame.time.get_ticks() // 300) % 2
        color = color1 if frame == 0 else color2
        pygame.draw.circle(pantalla, color, self.rect.center, self.radio)

    def colisiona_con(self, rect):
        dx = self.rect.centerx - rect.centerx
        dy = self.rect.centery - rect.centery
        distancia = dx ** 2 + dy ** 2
        return distancia < (self.radio + rect.width // 2) ** 2
