import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man - Juego Funcional")
reloj = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# Jugador
player_x = ANCHO // 2
player_y = ALTO // 2
velocidad = 5

# Fantasmas
fantasmas = [
    {"x": 100, "y": 100, "color": ROJO},
    {"x": ANCHO - 100, "y": 100, "color": (255, 0, 255)},
    {"x": 100, "y": ALTO - 100, "color": (0, 255, 255)},
    {"x": ANCHO - 100, "y": ALTO - 100, "color": (255, 165, 0)}
]

# Puntos
puntos = []
for i in range(80):
    x = random.randint(40, ANCHO - 40)
    y = random.randint(40, ALTO - 40)
    puntos.append([x, y])

puntuacion = 0
vidas = 3
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72)

# Variables del juego
jugando = True
invulnerable = False
tiempo_invulnerable = 0

# Bucle principal
while jugando:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
    
    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        player_x -= velocidad
    if teclas[pygame.K_RIGHT]:
        player_x += velocidad
    if teclas[pygame.K_UP]:
        player_y -= velocidad
    if teclas[pygame.K_DOWN]:
        player_y += velocidad
    
    # Mantener dentro de la pantalla
    player_x = max(20, min(ANCHO - 20, player_x))
    player_y = max(20, min(ALTO - 20, player_y))
    
    # Movimiento de fantasmas (persiguen al jugador)
    for fantasma in fantasmas:
        if fantasma["x"] < player_x:
            fantasma["x"] += 2
        if fantasma["x"] > player_x:
            fantasma["x"] -= 2
        if fantasma["y"] < player_y:
            fantasma["y"] += 2
        if fantasma["y"] > player_y:
            fantasma["y"] -= 2
    
    # Colisión con puntos
    for punto in puntos[:]:
        distancia = ((player_x - punto[0])**2 + (player_y - punto[1])**2) ** 0.5
        if distancia < 20:
            puntos.remove(punto)
            puntuacion += 10
    
    # Colisión con fantasmas
    if not invulnerable:
        for fantasma in fantasmas:
            distancia = ((player_x - fantasma["x"])**2 + (player_y - fantasma["y"])**2) ** 0.5
            if distancia < 30:
                vidas -= 1
                if vidas <= 0:
                    jugando = False
                else:
                    # Reiniciar posiciones
                    player_x = ANCHO // 2
                    player_y = ALTO // 2
                    invulnerable = True
                    tiempo_invulnerable = 90  # 1.5 segundos a 60 FPS
                break
    else:
        tiempo_invulnerable -= 1
        if tiempo_invulnerable <= 0:
            invulnerable = False
    
    # Dibujar todo
    pantalla.fill(NEGRO)
    
    # Dibujar puntos
    for punto in puntos:
        pygame.draw.circle(pantalla, BLANCO, punto, 4)
    
    # Dibujar jugador (Pac-Man)
    if invulnerable and (tiempo_invulnerable // 5) % 2 == 0:
        # Parpadeo cuando es invulnerable
        pygame.draw.circle(pantalla, (255, 255, 100), (player_x, player_y), 20)
    else:
        pygame.draw.circle(pantalla, AMARILLO, (player_x, player_y), 20)
    
    # Dibujar fantasmas
    for fantasma in fantasmas:
        pygame.draw.circle(pantalla, fantasma["color"], (fantasma["x"], fantasma["y"]), 18)
        # Ojos
        pygame.draw.circle(pantalla, BLANCO, (fantasma["x"] - 6, fantasma["y"] - 5), 4)
        pygame.draw.circle(pantalla, BLANCO, (fantasma["x"] + 6, fantasma["y"] - 5), 4)
        pygame.draw.circle(pantalla, NEGRO, (fantasma["x"] - 6, fantasma["y"] - 5), 2)
        pygame.draw.circle(pantalla, NEGRO, (fantasma["x"] + 6, fantasma["y"] - 5), 2)
    
    # Mostrar puntuación y vidas
    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
    pantalla.blit(texto_puntos, (10, 10))
    
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 50))
    
    # Mostrar instrucciones
    texto_inst = fuente.render("Usa flechas para moverte", True, BLANCO)
    pantalla.blit(texto_inst, (ANCHO - 250, 10))
    
    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

# Mensaje de Game Over
pantalla.fill(NEGRO)
texto_game = fuente_grande.render("GAME OVER", True, ROJO)
rect_game = texto_game.get_rect(center=(ANCHO//2, ALTO//2 - 50))
pantalla.blit(texto_game, rect_game)

texto_puntos_final = fuente.render(f"Puntuación final: {puntuacion}", True, BLANCO)
rect_puntos = texto_puntos_final.get_rect(center=(ANCHO//2, ALTO//2 + 50))
pantalla.blit(texto_puntos_final, rect_puntos)

pygame.display.flip()
pygame.time.wait(3000)  # Esperar 3 segundos

# Salir del juego
pygame.quit()
sys.exit()
