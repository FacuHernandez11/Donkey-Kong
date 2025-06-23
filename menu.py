import pygame
import sys
import subprocess


ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú de Juegos")


BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)


fuente_titulo = pygame.font.SysFont("Arial", 70, bold=True)
fuente_boton = pygame.font.SysFont("Arial", 50, bold=True)


img_donkey = pygame.image.load("assets/donkey.png")
img_diddy = pygame.image.load("assets/diddy.png")
fondo_donkey = pygame.image.load("assets/fondo_donkey.png")
fondo_diddy = pygame.image.load("assets/fondo_diddy.png")

def dibujar_boton(texto, x, y, ancho, alto, color, color_texto):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    pygame.draw.rect(pantalla, NEGRO, (x, y, ancho, alto), 4)
    texto_render = fuente_boton.render(texto, True, color_texto)
    pantalla.blit(texto_render, (x + (ancho - texto_render.get_width()) // 2, y + (alto - texto_render.get_height()) // 2))

def iniciar_donkey_kong():
    pygame.quit()
    subprocess.run([sys.executable, "main.py"])

def iniciar_diddy_kong_racing():
    
    print("Diddy Kong Racing aún no implementado")
    

def menu():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if 200 <= x <= 400 and 500 <= y <= 580:
                    iniciar_donkey_kong()
                if 800 <= x <= 1000 and 500 <= y <= 580:
                    iniciar_diddy_kong_racing()

        pantalla.blit(fondo_donkey, (0, 0))
        pantalla.blit(fondo_diddy, (ANCHO//2, 0))

        titulo_donkey = fuente_titulo.render("DONKEY KONG", True, ROJO)
        pantalla.blit(titulo_donkey, (120, 50))
        titulo_diddy = fuente_titulo.render("DIDDY KONG RACING", True, ROJO)
        pantalla.blit(titulo_diddy, (ANCHO//2 + 60, 50))

        pantalla.blit(img_donkey, (180, 200))
        pantalla.blit(img_diddy, (ANCHO//2 + 180, 200))

        dibujar_boton("START", 200, 500, 200, 80, ROJO, NEGRO)
        dibujar_boton("START", 800, 500, 200, 80, ROJO, NEGRO)

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    menu()

