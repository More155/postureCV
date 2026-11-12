"""Detección de pose corporal con MediaPipe."""

from pathlib import Path

import cv2
import mediapipe as mp

RUTA_MODELO_POR_DEFECTO = Path("models/pose_landmarker_lite.task")
VISIBILIDAD_MINIMA = 0.5

# Posición de cada articulación en la lista de 33 puntos de MediaPipe.
INDICES_POR_LADO = {
    "izquierdo": {"hombro": 11, "cadera": 23, "rodilla": 25, "tobillo": 27},
    "derecho": {"hombro": 12, "cadera": 24, "rodilla": 26, "tobillo": 28},
}


class DetectorPose:
    """Detecta los 33 puntos del cuerpo en cada cuadro de un video."""

    def __init__(self, ruta_modelo=RUTA_MODELO_POR_DEFECTO):
        """Carga el modelo de MediaPipe.

        Args:
            ruta_modelo: Ruta al archivo .task del modelo.

        Raises:
            FileNotFoundError: Si el archivo del modelo no existe.
        """
        ruta = Path(ruta_modelo)
        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en '{ruta}'. "
                "Descargalo siguiendo las instrucciones del README."
            )
        opciones = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(ruta)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
        )
        self._landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(
            opciones
        )

    def detectar(self, cuadro_bgr, timestamp_ms):
        """Busca una persona en un cuadro de video.

        Args:
            cuadro_bgr: Imagen de OpenCV (formato BGR).
            timestamp_ms: Instante del cuadro en milisegundos. Debe ir
                aumentando de un cuadro al siguiente.

        Returns:
            La lista de 33 landmarks de la primera persona detectada,
            o None si no se encontró a nadie.
        """
        cuadro_rgb = cv2.cvtColor(cuadro_bgr, cv2.COLOR_BGR2RGB)
        imagen = mp.Image(image_format=mp.ImageFormat.SRGB, data=cuadro_rgb)
        resultado = self._landmarker.detect_for_video(imagen, timestamp_ms)
        if not resultado.pose_landmarks:
            return None
        return resultado.pose_landmarks[0]

    def cerrar(self):
        """Libera los recursos del modelo."""
        self._landmarker.close()


def extraer_puntos(landmarks, ancho, alto, lado="izquierdo"):
    """Obtiene las articulaciones de un lado del cuerpo en píxeles.

    Args:
        landmarks: Lista de 33 landmarks devuelta por DetectorPose.
        ancho: Ancho del cuadro en píxeles.
        alto: Alto del cuadro en píxeles.
        lado: "izquierdo" o "derecho", el lado que mira a la cámara.

    Returns:
        Un diccionario {nombre: (x, y)} con hombro, cadera, rodilla y
        tobillo, o None si alguno no es lo bastante visible.
    """
    puntos = {}
    for nombre, indice in INDICES_POR_LADO[lado].items():
        landmark = landmarks[indice]
        if (landmark.visibility or 0.0) < VISIBILIDAD_MINIMA:
            return None
        puntos[nombre] = (landmark.x * ancho, landmark.y * alto)
    return puntos