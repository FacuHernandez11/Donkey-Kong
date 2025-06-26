import pygame
import random
from configuracion import ANCHO, ALTO, BLANCO, FPS, AMARILLO
from jugador import Jugador
from nivel import dibujar as dibujar_nivel, crear_nivel, plataformas, escaleras
from personaje import donkey_kong, donkey_kong2, princesa
from barril import Barril, BarrilRapido, BarrilLento, BarrilRebotador, BarrilNivel1, BarrilNivel2


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

    vidas = 2
    parpadeo = False
    parpadeo_timer = 0
    parpadeo_duracion = 1500  
    parpadeo_intervalo = 150  
    ultimo_parpadeo = 0

    tiempo_limite = 30  
    tiempo_inicio = pygame.time.get_ticks() if num_nivel == 3 else None

    SPAWN_BARRIL = pygame.USEREVENT + 1
    if num_nivel == 1:
        pygame.time.set_timer(SPAWN_BARRIL, 1500000)
        barril_tipos = [BarrilNivel1, BarrilRapido]
        fondo = BLANCO
    elif num_nivel == 2:
        pygame.time.set_timer(SPAWN_BARRIL, 1500000)
        barril_tipos = [BarrilRapido, BarrilRebotador, BarrilNivel2, BarrilNivel2]
        fondo = (200, 200, 255)
    elif num_nivel == 3:
        pygame.time.set_timer(SPAWN_BARRIL, 1500000) 
        barril_tipos = [BarrilRapido, BarrilRebotador, BarrilNivel2, BarrilNivel1]
        fondo = (220, 220, 220)

    if num_nivel == 3:
        plat_peach = plataformas[0]
        princesa["rect"].x = plat_peach.left + plat_peach.width // 2 - princesa["rect"].width // 2
        princesa["rect"].y = plat_peach.top - princesa["rect"].height

        plat_mono = plataformas[1]  
        donkey_kong["rect"].x = plat_mono.left
        donkey_kong["rect"].y = plat_mono.top - donkey_kong["rect"].height
    elif num_nivel == 1:
        plat = plataformas[0]
        donkey_kong["rect"].x = plat.left - 30
        donkey_kong["rect"].y = plat.top - donkey_kong["rect"].height
        princesa["rect"].x, princesa["rect"].y = 700, 10
    else:
        plat_izq = plataformas[2]
        plat_der = plataformas[3]
        donkey_kong["rect"].x = plat_izq.left
        donkey_kong["rect"].y = plat_izq.top - donkey_kong["rect"].height
        donkey_kong2["rect"].x = plat_der.right - donkey_kong2["rect"].width
        donkey_kong2["rect"].y = plat_der.top - donkey_kong2["rect"].height
        princesa["rect"].x, princesa["rect"].y = 700, 270

    imagen_nivel_superado = pygame.image.load("img/pantalla1.gif")
    imagen_nivel_superado = pygame.transform.scale(imagen_nivel_superado, (ANCHO, ALTO))
    imagen_perdiste = pygame.image.load("img/pantalla2.png")
    imagen_perdiste = pygame.transform.scale(imagen_perdiste, (ANCHO, ALTO))

    resultado = None
    ejecutando = True
    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    if num_nivel == 2 or num_nivel == 3:
        plat = plataformas[0]
        llave_x = plat.left + plat.width // 2 + 120  
        llave_y = plat.top - 35  
        llave_rect = pygame.Rect(llave_x, llave_y, 20, 20)
        llave_direccion = 1
        llave_min_y = plat.top - 35
        llave_max_y = plat.top - 20
        llave_tomada = False
        puerta_abierta = False
        plat_tele = plataformas[2]
        tele_x = plat_tele.left + plat_tele.width // 2 - 15  
        tele_y = plat_tele.top - 20  
        tele_rect = pygame.Rect(tele_x, tele_y, 30, 30)
    else:
        llave_rect = None
        llave_tomada = False
        puerta_abierta = True  
        tele_rect = None

    tele_rects = []
    if num_nivel == 1:
        plat_tele = plataformas[1]
        tele_x = plat_tele.left + plat_tele.width // 2 - 15
        tele_y = plat_tele.top - 20
        tele_rects.append(pygame.Rect(tele_x, tele_y, 30, 30))
    elif num_nivel == 2:
        plat_tele1 = plataformas[2]
        tele1_x = plat_tele1.left + plat_tele1.width // 2 - 15
        tele1_y = plat_tele1.top - 20
        tele_rects.append(pygame.Rect(tele1_x, tele1_y, 30, 30))
        plat_tele2 = plataformas[5]
        tele2_x = plat_tele2.left + plat_tele2.width // 2 - 15
        tele2_y = plat_tele2.top - 20
        tele_rects.append(pygame.Rect(tele2_x, tele2_y, 30, 30))

    while ejecutando:
        reloj.tick(FPS)
        pantalla.fill(fondo)

        if num_nivel == 3:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_restante = max(0, tiempo_limite - (tiempo_actual - tiempo_inicio) // 1000)
            fuente = pygame.font.SysFont(None, 36)
            texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante}", True, (255, 0, 0))
            pantalla.blit(texto_tiempo, (ANCHO // 2 - 60, 10))
            if tiempo_restante <= 0:
                pantalla.blit(imagen_perdiste, (0, 0))
                pygame.display.flip()
                pygame.time.wait(3000)
                ejecutando = False
                resultado = "perdiste"
                continue

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == SPAWN_BARRIL:
                if num_nivel == 1:
                    for _ in range(3):  
                        tipo = random.choice(barril_tipos)
                        if tipo == BarrilNivel1:
                            barriles.append(tipo())
                        else:
                            plat = plataformas[0]
                            x = plat.left + 10
                            y = plat.top - 20
                            barriles.append(tipo(x, y, dir=1))
                else:
                    tipo_izq = random.choice(barril_tipos)
                    tipo_der = random.choice(barril_tipos)
                    x_izq = donkey_kong["rect"].centerx - 10
                    y_izq = donkey_kong["rect"].bottom
                    barriles.append(tipo_izq(x_izq, y_izq, dir=1))
                    x_der = donkey_kong2["rect"].centerx - 10
                    y_der = donkey_kong2["rect"].bottom
                    barriles.append(tipo_der(x_der, y_der, dir=-1))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            jugador.saltar()

        jugador.actualizar(teclas)

        dibujar_nivel(pantalla)
        mostrar_jugador = True
        if parpadeo:
            ahora = pygame.time.get_ticks()
            if ahora - parpadeo_timer > parpadeo_duracion:
                parpadeo = False
                mostrar_jugador = True
            else:
                if (ahora - ultimo_parpadeo) > parpadeo_intervalo:
                    ultimo_parpadeo = ahora
                mostrar_jugador = ((ahora - parpadeo_timer) // parpadeo_intervalo) % 2 == 0
            if mostrar_jugador:
                x, y = posicion_inicial_jugador()
                jugador.rect.x = x
                jugador.rect.y = y

        if mostrar_jugador:
            jugador.dibujar(pantalla)
        pygame.draw.rect(pantalla, donkey_kong["color"], donkey_kong["rect"])
        if num_nivel == 2:
            pygame.draw.rect(pantalla, donkey_kong2["color"], donkey_kong2["rect"])
        pygame.draw.rect(pantalla, princesa["color"], princesa["rect"])

        if num_nivel == 2 and not llave_tomada:
            llave_rect.y += llave_direccion * 1  
            if llave_rect.y <= llave_min_y or llave_rect.y >= llave_max_y:
                llave_direccion *= -1

        if num_nivel == 2 and not llave_tomada:
            pygame.draw.rect(pantalla, AMARILLO, llave_rect)

        if num_nivel == 2:
            color_puerta = (0, 255, 0) if puerta_abierta else (128, 0, 128)
            puerta_rect = pygame.Rect(princesa["rect"].x, princesa["rect"].y, princesa["rect"].width, princesa["rect"].height)
            pygame.draw.rect(pantalla, color_puerta, puerta_rect)
        else:
            pygame.draw.rect(pantalla, princesa["color"], princesa["rect"])

        if (num_nivel == 2 or num_nivel == 3) and not llave_tomada and jugador.rect.colliderect(llave_rect):
            llave_tomada = True
            puerta_abierta = True

        for b in barriles[:]:
            b.actualizar()
            b.dibujar(pantalla)
            if b.colisiona_con(jugador.rect) and not parpadeo:
                vidas -= 1
                if vidas > 0:
                    parpadeo = True
                    parpadeo_timer = pygame.time.get_ticks()
                    ultimo_parpadeo = parpadeo_timer
                else:
                    pantalla.blit(imagen_perdiste, (0, 0))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    print("¡Perdiste por barril!")
                    ejecutando = False
                    resultado = "perdiste"
            if b.esta_fuera_de_pantalla():
                barriles.remove(b)

        if (jugador.rect.colliderect(donkey_kong["rect"]) or 
            (num_nivel == 2 and jugador.rect.colliderect(donkey_kong2["rect"]))) and not parpadeo:
            vidas -= 1
            if vidas > 0:
                parpadeo = True
                parpadeo_timer = pygame.time.get_ticks()
                ultimo_parpadeo = parpadeo_timer
            else:
                pantalla.blit(imagen_perdiste, (0, 0))
                pygame.display.flip()
                pygame.time.wait(3000)
                print("¡Perdiste por mono!")
                ejecutando = False
                resultado = "perdiste"

        for tele_rect in tele_rects:
            if jugador.rect.colliderect(tele_rect):
                x, y = posicion_inicial_jugador()
                jugador.rect.x = x
                jugador.rect.y = y

        for tele_rect in tele_rects:
            pygame.draw.rect(pantalla, (255, 0, 255), tele_rect)

        for i in range(vidas):
            vida_rect = pygame.Rect(20 + i*35, 15, 20, 30)
            pygame.draw.rect(pantalla, (0, 100, 255), vida_rect)

        if num_nivel == 3 and jugador.rect.colliderect(princesa["rect"]) and puerta_abierta:
            pantalla.blit(imagen_nivel_superado, (0, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            ejecutando = False
            resultado = "ganaste"
            continue
        if num_nivel == 1 and jugador.rect.colliderect(princesa["rect"]):
            pantalla.blit(imagen_nivel_superado, (0, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            ejecutando = False
            resultado = "ganaste"
            continue
        if num_nivel == 2 and jugador.rect.colliderect(princesa["rect"]) and puerta_abierta:
            pantalla.blit(imagen_nivel_superado, (0, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            ejecutando = False
            resultado = "ganaste"
            continue

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
        nivel_actual = 3
    elif resultado == "ganaste" and nivel_actual == 3:
        print("¡Completaste todos los niveles!")
        break
    else:
        nivel_actual = 1
