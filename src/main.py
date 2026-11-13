"""Punto de entrada: muestra la pose y el ángulo de la rodilla en vivo."""

import argparse

import cv2

from src.detector_pose import DetectorPose, extraer_puntos
from src.ejercicios import Sentadilla
from src.superposicion import COLOR_ALERTA, dibujar_esqueleto, escribir_texto

# Se asume un video de unos 30 cuadros por segundo (33 ms por cuadro).
MS_POR_CUADRO = 33
TECLA_SALIR = ord("q")


def leer_argumentos():
    """Lee los argumentos de la línea de comandos.

    Returns:
        Un objeto con los atributos ``fuente`` y ``lado``.
    """
    parser = argparse.ArgumentParser(
        description="Corrector de ejercicios con estimación de postura."
    )
    parser.add_argument(
        "--fuente",
        default="0",
        help="Número de cámara (por defecto 0) o ruta a un archivo de video.",
    )
    parser.add_argument(
        "--lado",
        choices=("izquierdo", "derecho"),
        default="izquierdo",
        help="Lado del cuerpo que mira a la cámara.",
    )
    return parser.parse_args()


def abrir_fuente(fuente):
    """Abre una cámara o un archivo de video.

    Args:
        fuente: Texto con un número de cámara ("0") o una ruta de archivo.

    Returns:
        El objeto cv2.VideoCapture ya abierto.

    Raises:
        RuntimeError: Si no se pudo abrir la fuente.
    """
    captura = cv2.VideoCapture(int(fuente) if fuente.isdigit() else fuente)
    if not captura.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente de video: {fuente}")
    return captura


def procesar_cuadro(cuadro, detector, sentadilla, lado, timestamp_ms):
    """Detecta la pose en un cuadro y dibuja el resultado sobre él.

    Args:
        cuadro: Imagen de OpenCV (se modifica).
        detector: Instancia de DetectorPose.
        sentadilla: Instancia de Sentadilla que lleva la cuenta.
        lado: "izquierdo" o "derecho".
        timestamp_ms: Instante del cuadro en milisegundos.
    """
    alto, ancho = cuadro.shape[:2]
    landmarks = detector.detectar(cuadro, timestamp_ms)
    if landmarks is None:
        return

    puntos = extraer_puntos(landmarks, ancho, alto, lado)
    if puntos is None:
        return

    sentadilla.actualizar(puntos)
    dibujar_esqueleto(cuadro, puntos)
    escribir_texto(
        cuadro, f"Rodilla: {sentadilla.angulo_rodilla:.0f} grados", (20, 40)
    )
    escribir_texto(
        cuadro, f"Repeticiones: {sentadilla.repeticiones}", (20, 80)
    )
    if sentadilla.espalda_inclinada:
        escribir_texto(cuadro, "Espalda recta!", (20, 120), COLOR_ALERTA)


def main():
    """Ejecuta el bucle principal hasta que se cierre la fuente o se pulse q."""
    argumentos = leer_argumentos()
    try:
        captura = abrir_fuente(argumentos.fuente)
        detector = DetectorPose()
    except (RuntimeError, FileNotFoundError) as error:
        print(error)
        return

    sentadilla = Sentadilla()
    numero_cuadro = 0
    try:
        while True:
            hay_cuadro, cuadro = captura.read()
            if not hay_cuadro:
                print("No se recibieron cuadros de la fuente de video.")
                break
            procesar_cuadro(
                cuadro,
                detector,
                sentadilla,
                argumentos.lado,
                numero_cuadro * MS_POR_CUADRO,
            )
            numero_cuadro += 1
            cv2.imshow("Corrector de ejercicios", cuadro)
            if cv2.waitKey(1) & 0xFF == TECLA_SALIR:
                break
    finally:
        captura.release()
        detector.cerrar()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()