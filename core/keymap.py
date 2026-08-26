import pygame

# Pygame distingue las teclas del teclado numerico (K_KP_*) de la fila
# superior de numeros (K_0..K_9). Los niveles de numeros y el modo
# dedicado de Numpad (secciones 4, 5 y 17 del documento maestro) necesitan
# saber cual de las dos se presiono, asi que el mapeo vive aparte desde ya.
NUMPAD_KEYS = {
    pygame.K_KP0: "0",
    pygame.K_KP1: "1",
    pygame.K_KP2: "2",
    pygame.K_KP3: "3",
    pygame.K_KP4: "4",
    pygame.K_KP5: "5",
    pygame.K_KP6: "6",
    pygame.K_KP7: "7",
    pygame.K_KP8: "8",
    pygame.K_KP9: "9",
    pygame.K_KP_PERIOD: ".",
    pygame.K_KP_ENTER: "\n",
}


def is_numpad_key(key):
    return key in NUMPAD_KEYS
