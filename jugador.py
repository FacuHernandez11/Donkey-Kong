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
        self.imagen_der = pygame.image.load("img/mario.png").convert_alpha()
        self.imagen_der = pygame.transform.scale(self.imagen_der, (self.rect.width, self.rect.height))
        self.imagen_izq = pygame.image.load("img/mario2.png").convert_alpha()
        self.imagen_izq = pygame.transform.scale(self.imagen_izq, (self.rect.width, self.rect.height))
        self.imagen = self.imagen_der
        self.facing_left = False

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
        margen = 5
        return (
            self.rect.right > escalera.left + margen and
            self.rect.left < escalera.right - margen and
            self.rect.bottom > escalera.top and
            self.rect.top < escalera.bottom
        )

    def actualizar(self, teclas):
        self.plat_idx = self.plataforma_actual()
        self.en_escalera = False

        escalera_candidata = None
        for escalera in escaleras:
            if self.rect.colliderect(escalera) and self.esta_alineado_con_escalera(escalera):
                self.en_escalera = True
                escalera_candidata = escalera
                break

        if teclas[pygame.K_LEFT]:
            self.rect.x -= 3
            self.facing_left = True
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 3
            self.facing_left = False

        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))

        if self.en_escalera and not self.saltando:
            if teclas[pygame.K_UP]:
                self.rect.y -= 3
            elif teclas[pygame.K_DOWN]:
                self.rect.y += 3
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

            if self.rect.top > ALTO:
                self.rect.bottom = plataformas[-1].top
                self.vel_y = 0
                self.saltando = False

        # Cambia la imagen según la dirección
        if self.facing_left:
            self.imagen = self.imagen_izq
        else:
            self.imagen = self.imagen_der

    def saltar(self):
        if not self.saltando:
            self.vel_y = -12
            self.saltando = True

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
