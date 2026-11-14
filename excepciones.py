# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: PROGRAMACIÓN (213023)
# Fase 4: PRÁCTICAS SIMULADAS
# Trabajo: SISTEMA INTEGRAL SOFTWARE FJ
# Nombre del producto: excepciones.py
# Estudiante: Karen Lizeth Gonzalez Cante 

# Módulo de Excepciones Personalizadas (excepciones.py)
# Define los errores específicos del sistema Software FJ para garantizar
# un manejo robusto y controlado de excepciones.

class SoftwareFJError(Exception):
    # Clase base para todas las excepciones del sistema Software FJ.
    pass


class ClienteInvalidoError(SoftwareFJError):
    # Se lanza cuando los datos de un cliente son incorrectos, incompletos o vacíos.
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    # Se lanza cuando se intenta acceder o contratar un servicio que no existe o está inactivo.
    pass


class ReservaError(SoftwareFJError):
    # Se lanza cuando ocurre un fallo al procesar, confirmar o cancelar una reserva.
    pass
