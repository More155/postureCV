"""Dibujo de información sobre el video con OpenCV."""

import cv2

COLOR_PUNTO = (0, 255, 0)
COLOR_LINEA = (255, 255, 255)
COLOR_TEXTO = (255, 255, 255)
COLOR_ALERTA = (0, 0, 255)

ORDEN_ARTICULACIONES = ("hombro", "cadera", "rodilla", "tobillo")
RADIO_PUNTO = 6
GROSOR_LINEA = 2


def dibujar_esqueleto(cuadro, puntos):
    """Dibuja el segmento hombro-cadera-rodilla-tobillo sobre el cuadro.

    Args:
        cuadro: Imagen de OpenCV sobre la que se dibuja (se modifica).
        puntos: Diccionario {nombre: (x, y)} en píxeles, como el que
            devuelve extraer_puntos.
    """
    posiciones = [
        (int(puntos[nombre][0]), int(puntos[nombre][1]))
        for nombre in ORDEN_ARTICULACIONES
    ]
    for inicio, fin in zip(posiciones, posiciones[1:]):
        cv2.line(cuadro, inicio, fin, COLOR_LINEA, GROSOR_LINEA)
    for posicion in posiciones:
        cv2.circle(cuadro, posicion, RADIO_PUNTO, COLOR_PUNTO, -1)


def escribir_texto(cuadro, texto, posicion, color=COLOR_TEXTO):
    """Escribe un texto sobre el cuadro.

    Args:
        cuadro: Imagen de OpenCV sobre la que se escribe (se modifica).
        texto: Texto a mostrar.
        posicion: Tupla (x, y) de la esquina inferior izquierda del texto.
        color: Color BGR del texto.
    """
    cv2.putText(
        cuadro, texto, posicion, cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
    )