import pygame
import random
from configuracion import ANCHO, ALTO, BLANCO, FPS, AMARILLO
from jugador import Jugador
from nivel import dibujar as dibujar_nivel, crear_nivel, plataformas, escaleras
from personaje import donkey_kong, donkey_kong2, princesa
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
    if not plataformas:
        raise Exception("Las plataformas no están inicializadas. Llama a crear_nivel(nivel) antes.")
    return plataformas[-1].left + 100, plataformas[-1].top - altura_jugador


def juego(num_nivel=1):
    reloj = pygame.time.Clock()
    crear_nivel(num_nivel)

    x, y = posicion_inicial_jugador()
    jugador = Jugador(x, y)
    barriles = []

    SPAWN_BARRIL = pygame.USEREVENT + 1
    if num_nivel == 1:
        pygame.time.set_timer(SPAWN_BARRIL, 2500000)
        barril_tipos = [Barril, BarrilRapido, BarrilLento, BarrilRebotador]
        fondo = BLANCO
    else:
        pygame.time.set_timer(SPAWN_BARRIL, 12000000)
        barril_tipos = [BarrilRapido, BarrilRebotador, BarrilRebotador, Barril]
        fondo = (200, 200, 255)

    if num_nivel == 1:
        donkey_kong["rect"].x, donkey_kong["rect"].y = 150, 10
        princesa["rect"].x, princesa["rect"].y = 700, 10
    else:
        # Primera plataforma del nivel 2
        plat = plataformas[0]
        donkey_kong["rect"].x = plat.left + 20
        donkey_kong["rect"].y = plat.top - donkey_kong["rect"].height
        donkey_kong2["rect"].x = plat.right - donkey_kong2["rect"].width - 20
        donkey_kong2["rect"].y = plat.top - donkey_kong2["rect"].height
        princesa["rect"].x, princesa["rect"].y = 700, 270

    imagen_nivel_superado = pygame.image.load("img/pantalla1.gif")
    imagen_nivel_superado = pygame.transform.scale(imagen_nivel_superado, (ANCHO, ALTO))
    imagen_perdiste = pygame.image.load("img/pantalla2.png")
    imagen_perdiste = pygame.transform.scale(imagen_perdiste, (ANCHO, ALTO))

    resultado = None
    ejecutando = True
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    # Solo en el segundo nivel
    if num_nivel == 2:
        # Primera plataforma
        plat = plataformas[0]
        llave_x = plat.left + plat.width // 2 + 120  # Ajusta si quieres moverla en X
        llave_y = plat.top - 35  # Más arriba que antes
        llave_rect = pygame.Rect(llave_x, llave_y, 20, 20)
        llave_direccion = 1
        # Recorrido vertical corto y más arriba
        llave_min_y = plat.top - 35
        llave_max_y = plat.top - 20
        llave_tomada = False
        puerta_abierta = False
        # Teletransportador en la 3ra plataforma (índice 2)
        plat_tele = plataformas[2]
        tele_x = plat_tele.left + plat_tele.width // 2 - 15  # Centrado en la plataforma
        tele_y = plat_tele.top - 20  # Justo sobre la plataforma
        tele_rect = pygame.Rect(tele_x, tele_y, 30, 30)
    else:
        llave_rect = None
        llave_tomada = False
        puerta_abierta = True  # En el primer nivel la puerta siempre está abierta
        tele_rect = None

    while ejecutando:
        reloj.tick(FPS)
        pantalla.fill(fondo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == SPAWN_BARRIL:
                if num_nivel == 1:
                    for _ in range(2):
                        tipo = random.choice(barril_tipos)
                        barriles.append(tipo())
                else:
                    
                    tipo_izq = random.choice(barril_tipos)
                    tipo_der = random.choice(barril_tipos)
                    barriles.append(tipo_izq(lado='izq'))
                    barriles.append(tipo_der(lado='der'))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            jugador.saltar()

        jugador.actualizar(teclas)

        dibujar_nivel(pantalla)
        jugador.dibujar(pantalla)
        pygame.draw.rect(pantalla, donkey_kong["color"], donkey_kong["rect"])
        if num_nivel == 2:
            pygame.draw.rect(pantalla, donkey_kong2["color"], donkey_kong2["rect"])
        pygame.draw.rect(pantalla, princesa["color"], princesa["rect"])

        # Mueve la llave arriba y abajo (solo nivel 2 y si no fue tomada)
        if num_nivel == 2 and not llave_tomada:
            llave_rect.y += llave_direccion * 1  # Más lento
            if llave_rect.y <= llave_min_y or llave_rect.y >= llave_max_y:
                llave_direccion *= -1

        # Dibuja la llave si no fue tomada
        if num_nivel == 2 and not llave_tomada:
            pygame.draw.rect(pantalla, AMARILLO, llave_rect)

        # Dibuja la puerta de Peach (puedes cambiar el color si está abierta)
        if num_nivel == 2:
            color_puerta = (0, 255, 0) if puerta_abierta else (128, 0, 128)
            puerta_rect = pygame.Rect(princesa["rect"].x, princesa["rect"].y, princesa["rect"].width, princesa["rect"].height)
            pygame.draw.rect(pantalla, color_puerta, puerta_rect)
        else:
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

        # Colisión con la llave
        if num_nivel == 2 and not llave_tomada and jugador.rect.colliderect(llave_rect):
            llave_tomada = True
            puerta_abierta = True

        # Solo puede ganar si la puerta está abierta
        if jugador.rect.colliderect(princesa["rect"]) and puerta_abierta:
            pantalla.blit(imagen_nivel_superado, (0, 0))
            pygame.display.flip()
            pygame.time.wait(2000)
            print("¡Ganaste!")
            ejecutando = False
            resultado = "ganaste"

        # Teletransporte al jugador (solo nivel 2 y si toca el teletransportador)
        if num_nivel == 2 and tele_rect and jugador.rect.colliderect(tele_rect):
            x, y = posicion_inicial_jugador()
            jugador.rect.x = x
            jugador.rect.y = y

        # Dibuja el teletransportador solo en el nivel 2
        if num_nivel == 2 and tele_rect:
            pygame.draw.rect(pantalla, (255, 0, 255), tele_rect)  # Color magenta

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
