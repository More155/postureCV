"""Lógica de los ejercicios: conteo de repeticiones y control de postura."""

from src import config
from src.angulos import angulo_con_vertical, calcular_angulo
from src.suavizado import PromedioMovil

ESTADO_ARRIBA = "arriba"
ESTADO_ABAJO = "abajo"


class Sentadilla:
    """Cuenta sentadillas y vigila la inclinación de la espalda.

    Usa una máquina de estados de dos posiciones: la persona está "arriba"
    (de pie) o "abajo" (agachada). Una repetición se suma al volver a
    subir después de haber bajado lo suficiente.

    Attributes:
        repeticiones: Cantidad de sentadillas completadas.
        angulo_rodilla: Último ángulo de rodilla, ya suavizado.
        espalda_inclinada: True si el torso se inclina más de lo permitido.
    """

    def __init__(self):
        """Crea una sentadilla lista para empezar a contar."""
        self.repeticiones = 0
        self.angulo_rodilla = 0.0
        self.espalda_inclinada = False
        self._estado = ESTADO_ARRIBA
        self._suavizador = PromedioMovil(config.VENTANA_SUAVIZADO)

    def actualizar(self, puntos):
        """Procesa las articulaciones de un cuadro y actualiza el estado.

        Args:
            puntos: Diccionario {nombre: (x, y)} con hombro, cadera,
                rodilla y tobillo, como el que devuelve extraer_puntos.
        """
        angulo = calcular_angulo(
            puntos["cadera"], puntos["rodilla"], puntos["tobillo"]
        )
        self.angulo_rodilla = self._suavizador.agregar(angulo)
        self._actualizar_repeticiones()

        inclinacion = angulo_con_vertical(puntos["hombro"], puntos["cadera"])
        self.espalda_inclinada = inclinacion > config.INCLINACION_MAXIMA_TORSO

    def _actualizar_repeticiones(self):
        """Cambia de estado y suma una repetición al completar el ciclo."""
        if (
            self._estado == ESTADO_ARRIBA
            and self.angulo_rodilla < config.UMBRAL_RODILLA_ABAJO
        ):
            self._estado = ESTADO_ABAJO
        elif (
            self._estado == ESTADO_ABAJO
            and self.angulo_rodilla > config.UMBRAL_RODILLA_ARRIBA
        ):
            self._estado = ESTADO_ARRIBA
            self.repeticiones += 1