import pygame
from configuracion import ANCHO, ALTO, BLANCO, FPS
from jugador import Jugador
from nivel import dibujar as dibujar_nivel
from personaje import donkey_kong, princesa
from barril import Barril

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Donkey Kong")

reloj = pygame.time.Clock()
jugador = Jugador(100, ALTO - 80)
barriles = []

SPAWN_BARRIL = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_BARRIL, 10000000)  

ejecutando = True
while ejecutando:
    reloj.tick(FPS)
    pantalla.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == SPAWN_BARRIL:
            
            barriles.append(Barril())
            barriles.append(Barril())

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
        if b.rect.top > ALTO:
            barriles.remove(b)

    if jugador.rect.colliderect(princesa["rect"]):
        print("¡Ganaste!")
        ejecutando = False

    pygame.display.flip()

pygame.quit()
