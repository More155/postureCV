"""Funciones geométricas para medir ángulos entre puntos del cuerpo."""

import numpy as np


def calcular_angulo(punto_a, punto_b, punto_c):
    """Calcula el ángulo en grados que forman tres puntos.

    El vértice del ángulo es ``punto_b``. Por ejemplo, para el ángulo de
    la rodilla: cadera (a), rodilla (b) y tobillo (c).

    Args:
        punto_a: Tupla (x, y) del primer extremo.
        punto_b: Tupla (x, y) del vértice.
        punto_c: Tupla (x, y) del segundo extremo.

    Returns:
        El ángulo en grados, entre 0 y 180.

    Raises:
        ValueError: Si algún extremo coincide con el vértice.
    """
    a = np.array(punto_a)
    b = np.array(punto_b)
    c = np.array(punto_c)

    vector_ba = a - b
    vector_bc = c - b

    producto_normas = np.linalg.norm(vector_ba) * np.linalg.norm(vector_bc)
    if producto_normas == 0:
        raise ValueError("Un extremo coincide con el vértice del ángulo.")

    coseno = np.dot(vector_ba, vector_bc) / producto_normas
    coseno = np.clip(coseno, -1.0, 1.0)
    return float(np.degrees(np.arccos(coseno)))


def angulo_con_vertical(punto_superior, punto_inferior):
    """Calcula cuánto se inclina un segmento respecto de la vertical.

    Sirve para medir la inclinación del torso: hombro (superior) y
    cadera (inferior). 0° es perfectamente derecho.

    Args:
        punto_superior: Tupla (x, y) del extremo de arriba.
        punto_inferior: Tupla (x, y) del extremo de abajo.

    Returns:
        La inclinación en grados, entre 0 y 180.
    """
    x_inferior, y_inferior = punto_inferior
    # En una imagen el eje y crece hacia ABAJO, por eso "arriba" es y - 1.
    punto_arriba = (x_inferior, y_inferior - 1)
    return calcular_angulo(punto_superior, punto_inferior, punto_arriba)

