import pygame
from configuracion import ANCHO, GRAVEDAD, AZUL
from nivel import plataformas, escaleras

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 30)
        self.vel_y = 0
        self.saltando = False
        self.en_escalera = False
        self.plat_idx = self.plataforma_actual()
        self.subiendo = False
        self.bajando = False

    def plataforma_actual(self):
        for i, plat in enumerate(plataformas):
            if (self.rect.bottom == plat.top and
                self.rect.right > plat.left and
                self.rect.left < plat.right):
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
            if self.rect.colliderect(escalera):
                if self.esta_alineado_con_escalera(escalera):
                    self.en_escalera = True
                    escalera_candidata = escalera
                    break

        if teclas[pygame.K_LEFT]:
            self.rect.x -= 3
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 3

        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))

        if self.en_escalera and not self.saltando:
            if teclas[pygame.K_UP]:
                self.subir_escalera(escalera_candidata)
            elif teclas[pygame.K_DOWN]:
                self.bajar_escalera(escalera_candidata)
            else:
                self.subiendo = False
                self.bajando = False
                if self.plat_idx >= 0:
                    plat = plataformas[self.plat_idx]
                    self.rect.bottom = plat.top
                else:
                    if escalera_candidata:
                        self.rect.centerx = escalera_candidata.centerx
            self.vel_y = 0
        else:
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

            if not apoyado:
                for escalera in escaleras:
                    margen = 10
                    if escalera.left - margen <= self.rect.centerx <= escalera.right + margen:
                        if abs(self.rect.bottom - escalera.top) < 20:
                            self.rect.bottom = escalera.top
                            self.vel_y = 0
                            self.saltando = False
                            apoyado = True
                            break

            from configuracion import ALTO
            if self.rect.top > ALTO:
                self.rect.bottom = plataformas[-1].top
                self.vel_y = 0
                self.saltando = False

    def subir_escalera(self, escalera):
        if escalera is None:
            return
        siguiente_idx = self.plat_idx - 1
        if siguiente_idx < 0:
            return
        plat_superior = plataformas[siguiente_idx]
        self.rect.bottom = plat_superior.top
        self.rect.centerx = escalera.centerx
        self.subiendo = True
        self.bajando = False
        self.vel_y = 0
        self.plat_idx = siguiente_idx

    def bajar_escalera(self, escalera):
        if escalera is None:
            return
        siguiente_idx = self.plat_idx + 1
        if siguiente_idx >= len(plataformas):
            return
        plat_inferior = plataformas[siguiente_idx]
        self.rect.bottom = plat_inferior.top
        self.rect.centerx = escalera.centerx
        self.bajando = True
        self.subiendo = False
        self.vel_y = 0
        self.plat_idx = siguiente_idx

    def saltar(self):
        puede_saltar = (
            not self.saltando and
            (not self.en_escalera or self.vel_y == 0)
        )
        if puede_saltar:
            self.vel_y = -12
            self.saltando = True

    def dibujar(self, pantalla):
        colores = [(0, 0, 255), (0, 100, 255)]
        frame = (pygame.time.get_ticks() // 300) % 2
        pygame.draw.rect(pantalla, colores[frame], self.rect)