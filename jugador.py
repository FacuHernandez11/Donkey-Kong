import pygame
from configuracion import ANCHO, ALTO, GRAVEDAD
from nivel import plataformas, escaleras

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 30)
        self.vel_y = 0
        self.saltando = False
        self.en_escalera = False
        self.plat_idx = self.plataforma_actual()

    def plataforma_actual(self):
        for i, plat in enumerate(plataformas):
            if (
                self.rect.bottom <= plat.top + 5 and
                self.rect.bottom >= plat.top - 15 and
                self.rect.right > plat.left and
                self.rect.left < plat.right
            ):
                return i
        return -1

    def esta_alineado_con_escalera(self, escalera):
        margen = 10
        return escalera.left - margen <= self.rect.centerx <= escalera.right + margen

    def actualizar(self, teclas):
        self.plat_idx = self.plataforma_actual()
        self.en_escalera = False

        escalera_candidata = None
        for escalera in escaleras:
            if self.rect.colliderect(escalera) and self.esta_alineado_con_escalera(escalera):
                self.en_escalera = True
                escalera_candidata = escalera
                break

        # Movimiento horizontal
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 3
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 3

        # Limita dentro de la pantalla
        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))

        # Movimiento vertical si está en escalera
        if self.en_escalera and not self.saltando:
            if teclas[pygame.K_UP]:
                self.rect.y -= 3
            elif teclas[pygame.K_DOWN]:
                self.rect.y += 3
            self.vel_y = 0
        else:
            # Física del salto y gravedad
            self.vel_y += GRAVEDAD
            self.rect.y += self.vel_y

            apoyado = False
            for plat in plataformas:
                if self.vel_y >= 0 and self.rect.bottom <= plat.top + 15 and self.rect.right > plat.left and self.rect.left < plat.right:
                    if self.rect.bottom + self.vel_y >= plat.top:
                        self.rect.bottom = plat.top
                        self.vel_y = 0
                        self.saltando = False
                        apoyado = True
                        break

            # Si cae fuera de la pantalla, lo reposiciona
            if self.rect.top > ALTO:
                self.rect.bottom = plataformas[-1].top
                self.vel_y = 0
                self.saltando = False

    def saltar(self):
        if not self.saltando:
            self.vel_y = -12
            self.saltando = True

    def dibujar(self, pantalla):
        color = (0, 100, 255)
        pygame.draw.rect(pantalla, color, self.rect)
