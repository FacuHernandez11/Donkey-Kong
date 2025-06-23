import pygame
import random
from configuracion import ANCHO, ALTO, BLANCO, FPS
from jugador import Jugador
from nivel import dibujar as dibujar_nivel
from personaje import donkey_kong, princesa
from barril import Barril, BarrilRapido, BarrilLento, BarrilRebotador

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Donkey Kong - Escaleras y Barriles")

reloj = pygame.time.Clock()
jugador = Jugador(100, ALTO - 80)
barriles = []

SPAWN_BARRIL = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_BARRIL, 1500)

ejecutando = True
while ejecutando:
    reloj.tick(FPS)
    pantalla.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == SPAWN_BARRIL:
            tipo = random.choice([Barril, BarrilRapido, BarrilLento, BarrilRebotador])
            barriles.append(tipo())

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE]:
        jugador.saltar()

    jugador.actualizar(teclas)

    dibujar_nivel(pantalla)
    jugador.dibujar(pantalla)
    pygame.draw.rect(pantalla, donkey_kong["color"], donkey_kong["rect"])
    pygame.draw.rect(pantalla, princesa["color"], princesa["rect"])

    for b in barriles[:]:
        b.actualizar()
        b.dibujar(pantalla)
        if b.colisiona_con(jugador.rect):
            print("¡Perdiste por barril!")
            ejecutando = False
        if b.esta_fuera_de_pantalla():
            barriles.remove(b)

    if jugador.rect.colliderect(princesa["rect"]):
        print("¡Ganaste!")
        ejecutando = False

    pygame.display.flip()

pygame.quit()
