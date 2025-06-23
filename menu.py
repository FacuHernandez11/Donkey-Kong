import pygame
import sys
import subprocess

pygame.init()

ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú de Juegos")

menu_img = pygame.image.load("img/menu.png")
menu_img = pygame.transform.scale(menu_img, (ANCHO, ALTO))


boton_donkey = pygame.Rect(200, 500, 200, 80)
boton_diddy = pygame.Rect(800, 500, 200, 80)

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
                if boton_donkey.collidepoint(x, y):
                    iniciar_donkey_kong()
                if boton_diddy.collidepoint(x, y):
                    iniciar_diddy_kong_racing()

        pantalla.blit(menu_img, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    menu()

