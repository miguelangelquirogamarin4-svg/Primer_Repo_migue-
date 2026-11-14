import sys
import pygame

# --- Configuración básica ---
ANCHO, ALTO = 800, 600
FPS = 60

# Colores
CIELO = (92, 148, 252)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 216, 0)
ROJO = (220, 40, 40)
VERDE = (60, 180, 60)
VERDE_OSCURO = (30, 120, 30)
LADRILLO = (200, 76, 12)
LADRILLO_OSCURO = (120, 40, 0)
PIEL = (252, 188, 116)
AZUL = (40, 60, 200)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Super Aventura Saltarina")
reloj = pygame.time.Clock()

fuente_titulo = pygame.font.SysFont("arial black", 56)
fuente_menu = pygame.font.SysFont("arial", 36, bold=True)
fuente_pie = pygame.font.SysFont("arial", 18)

opciones = ["JUGAR", "OPCIONES", "SALIR"]
seleccion = 0
nubes_x = [100, 400, 650]
mensaje = ""


def texto_con_sombra(texto, fuente, color, centro):
    sombra = fuente.render(texto, True, NEGRO)
    frente = fuente.render(texto, True, color)
    rect = frente.get_rect(center=centro)
    pantalla.blit(sombra, rect.move(4, 4))
    pantalla.blit(frente, rect)


def dibujar_nube(x, y):
    for dx, dy, r in [(0, 0, 25), (30, -15, 30), (60, 0, 25)]:
        pygame.draw.circle(pantalla, BLANCO, (int(x + dx), y + dy), r)


def dibujar_suelo():
    y_suelo = ALTO - 80
    for x in range(0, ANCHO, 40):
        for y in range(y_suelo, ALTO, 40):
            pygame.draw.rect(pantalla, LADRILLO, (x, y, 40, 40))
            pygame.draw.rect(pantalla, LADRILLO_OSCURO, (x, y, 40, 40), 2)


def dibujar_colinas():
    pygame.draw.ellipse(pantalla, VERDE, (-50, ALTO - 200, 300, 240))
    pygame.draw.ellipse(pantalla, VERDE_OSCURO, (550, ALTO - 160, 250, 200))


def dibujar_tubo(x):
    pygame.draw.rect(pantalla, VERDE, (x, ALTO - 160, 60, 80))
    pygame.draw.rect(pantalla, VERDE, (x - 8, ALTO - 180, 76, 25))
    pygame.draw.rect(pantalla, NEGRO, (x - 8, ALTO - 180, 76, 25), 2)
    pygame.draw.rect(pantalla, NEGRO, (x, ALTO - 155, 60, 75), 2)


def dibujar_personaje(x, y):
    # Personaje simple hecho con rectángulos
    pygame.draw.rect(pantalla, ROJO, (x, y, 30, 10))          # gorra
    pygame.draw.rect(pantalla, PIEL, (x + 3, y + 10, 24, 16))  # cara
    pygame.draw.rect(pantalla, NEGRO, (x + 18, y + 14, 4, 4))  # ojo
    pygame.draw.rect(pantalla, ROJO, (x, y + 26, 30, 14))      # camisa
    pygame.draw.rect(pantalla, AZUL, (x + 2, y + 40, 26, 14))  # pantalón


def dibujar_menu():
    for i, opcion in enumerate(opciones):
        color = AMARILLO if i == seleccion else BLANCO
        y = 280 + i * 60
        texto_con_sombra(opcion, fuente_menu, color, (ANCHO // 2, y))
        if i == seleccion:
            # flecha indicadora
            px = ANCHO // 2 - 130
            pygame.draw.polygon(pantalla, AMARILLO,
                                [(px, y - 12), (px, y + 12), (px + 18, y)])


def accion(opcion):
    global mensaje
    if opcion == "JUGAR":
        mensaje = "¡El juego empezará pronto!"
    elif opcion == "OPCIONES":
        mensaje = "Opciones aún no disponibles"
    elif opcion == "SALIR":
        pygame.quit()
        sys.exit()


# --- Bucle principal ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_w):
                seleccion = (seleccion - 1) % len(opciones)
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                seleccion = (seleccion + 1) % len(opciones)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                accion(opciones[seleccion])

    # Mover nubes
    for i in range(len(nubes_x)):
        nubes_x[i] += 0.5
        if nubes_x[i] > ANCHO + 50:
            nubes_x[i] = -100

    # Dibujar
    pantalla.fill(CIELO)
    dibujar_nube(nubes_x[0], 80)
    dibujar_nube(nubes_x[1], 130)
    dibujar_nube(nubes_x[2], 60)
    dibujar_colinas()
    dibujar_tubo(650)
    dibujar_suelo()
    dibujar_personaje(120, ALTO - 134)

    texto_con_sombra("SUPER AVENTURA", fuente_titulo, AMARILLO, (ANCHO // 2, 120))
    texto_con_sombra("SALTARINA", fuente_titulo, ROJO, (ANCHO // 2, 180))
    dibujar_menu()

    if mensaje:
        texto_con_sombra(mensaje, fuente_pie, BLANCO, (ANCHO // 2, 470))

    pie = fuente_pie.render("Flechas para moverte - ENTER para elegir", True, BLANCO)
    pantalla.blit(pie, pie.get_rect(center=(ANCHO // 2, ALTO - 20)))

    pygame.display.flip()
    reloj.tick(FPS)
