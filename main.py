import pygame
import random
from configuracion import ANCHO, ALTO, BLANCO, FPS
from jugador import Jugador
from nivel import dibujar as dibujar_nivel, crear_nivel, plataformas
from personaje import donkey_kong, princesa
from barril import Barril, BarrilRapido, BarrilLento, BarrilRebotador

def menu_principal():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Donkey Kong - Menú Principal")
   
    imagen_controles = pygame.image.load("img/controles.png")
    imagen_controles = pygame.transform.scale(imagen_controles, (ANCHO, ALTO))
    ejecutando_menu = True
    while ejecutando_menu:
        pantalla.blit(imagen_controles, (0, 0))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                ejecutando_menu = False

def posicion_inicial_jugador():
    altura_jugador = 30
    return plataformas[-1].left + 100, plataformas[-1].top - altura_jugador

def juego(nivel=1):
    reloj = pygame.time.Clock()
    crear_nivel(nivel)  # Inicializa plataformas antes de usarlas

    x, y = posicion_inicial_jugador()
    jugador = Jugador(x, y)
    barriles = []

    SPAWN_BARRIL = pygame.USEREVENT + 1
    if nivel == 1:
        pygame.time.set_timer(SPAWN_BARRIL, 1000)
        barril_tipos = [Barril, BarrilRapido, BarrilLento, BarrilRebotador]
        fondo = BLANCO
    else:
        pygame.time.set_timer(SPAWN_BARRIL, 600)
        barril_tipos = [BarrilRapido, BarrilRebotador, BarrilRebotador, Barril]
        fondo = (200, 200, 255)

    # Cambia la posición de Donkey Kong y la princesa según el nivel
    if nivel == 1:
        donkey_kong["rect"].x, donkey_kong["rect"].y = 150, 10
        princesa["rect"].x, princesa["rect"].y = 700, 10
    else:
        donkey_kong["rect"].x, donkey_kong["rect"].y = 50, 180
        princesa["rect"].x, princesa["rect"].y = 700, 270

    imagen_nivel_superado = pygame.image.load("img/pantalla1.gif")
    imagen_nivel_superado = pygame.transform.scale(imagen_nivel_superado, (ANCHO, ALTO))
    imagen_perdiste = pygame.image.load("img/pantalla2.png")
    imagen_perdiste = pygame.transform.scale(imagen_perdiste, (ANCHO, ALTO))

    resultado = None
    ejecutando = True
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    while ejecutando:
        reloj.tick(FPS)
        pantalla.fill(fondo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == SPAWN_BARRIL:
                for _ in range(2 if nivel == 1 else 3):
                    tipo = random.choice(barril_tipos)
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
                pantalla.blit(imagen_perdiste, (0, 0))
                pygame.display.flip()
                pygame.time.wait(3000)
                print("¡Perdiste por barril!")
                ejecutando = False
                resultado = "perdiste"
            if b.esta_fuera_de_pantalla():
                barriles.remove(b)

        if jugador.rect.colliderect(princesa["rect"]):
            pantalla.blit(imagen_nivel_superado, (0, 0))
            pygame.display.flip()
            pygame.time.wait(2000)
            print("¡Ganaste!")
            ejecutando = False
            resultado = "ganaste"

        pygame.display.flip()
    return resultado

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
nivel_actual = 1

while True:
    menu_principal()
    resultado = juego(nivel_actual)
    if resultado == "ganaste" and nivel_actual == 1:
        nivel_actual = 2
    elif resultado == "ganaste" and nivel_actual == 2:
        print("¡Completaste todos los niveles!")
        break
    else:
        nivel_actual = 1