"""Suavizado de señales ruidosas mediante promedio móvil."""

from collections import deque


class PromedioMovil:
    """Calcula el promedio de los últimos N valores recibidos.

    Se usa para estabilizar los ángulos: los puntos que detecta la cámara
    "vibran" un poco entre cuadros, y promediar los últimos valores
    evita saltos bruscos.
    """

    def __init__(self, tamano_ventana=5):
        """Crea el filtro.

        Args:
            tamano_ventana: Cantidad de valores recientes a promediar.

        Raises:
            ValueError: Si la ventana es menor que 1.
        """
        if tamano_ventana < 1:
            raise ValueError("La ventana debe tener al menos 1 valor.")
        self._valores = deque(maxlen=tamano_ventana)

    def agregar(self, valor):
        """Agrega un valor nuevo y devuelve el promedio actual.

        Args:
            valor: Número (por ejemplo, un ángulo en grados).

        Returns:
            El promedio de los valores que hay en la ventana.
        """
        self._valores.append(valor)
        return sum(self._valores) / len(self._valores)

    def reiniciar(self):
        """Descarta los valores guardados, por ejemplo al perder a la persona."""
        self._valores.clear()