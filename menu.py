import pygame
import sys
import subprocess

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú de Juegos")

# Reproduce el audio al inicio del menú
pygame.mixer.music.load("audio/menu.mp3")  # Cambia la ruta si tu archivo tiene otro nombre o extensión
pygame.mixer.music.play(-1)  # -1 para que se repita en loop, usa 0 para una sola vez

menu_img = pygame.image.load("img/menu.jpg")
menu_img = pygame.transform.scale(menu_img, (ANCHO, ALTO))

# Ajusta los rectángulos para que coincidan con los logos
# Donkey Kong logo (izquierda)
logo_donkey_rect = pygame.Rect(180, 180, 400, 350)  # Ajusta según el tamaño y posición del logo
# Diddy Racing logo (derecha)
logo_diddy_rect = pygame.Rect(700, 180, 400, 350)   # Ajusta según el tamaño y posición del logo

def iniciar_donkey_kong():
    pygame.quit()
    subprocess.run([sys.executable, "main.py"])

def iniciar_diddy_kong_racing():
    pygame.quit()
    subprocess.run([sys.executable, "carrera/main.py"])

def menu():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if logo_donkey_rect.collidepoint(x, y):
                    iniciar_donkey_kong()
                if logo_diddy_rect.collidepoint(x, y):
                    iniciar_diddy_kong_racing()

        pantalla.blit(menu_img, (0, 0))
        
        pygame.display.flip()

if __name__ == "__main__":
    menu()