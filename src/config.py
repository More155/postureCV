"""Constantes y umbrales del programa."""

# Ángulo de la rodilla (grados) para considerar que la persona está de pie.
UMBRAL_RODILLA_ARRIBA = 160

# Ángulo de la rodilla (grados) por debajo del cual la sentadilla es válida.
UMBRAL_RODILLA_ABAJO = 100

# Inclinación máxima del torso respecto de la vertical, en grados. (valor inicial)
# Hay que ajustarlo probando con el cuerpo.
INCLINACION_MAXIMA_TORSO = 60

# Cantidad de cuadros que se promedian para suavizar el ángulo.
VENTANA_SUAVIZADO = 5