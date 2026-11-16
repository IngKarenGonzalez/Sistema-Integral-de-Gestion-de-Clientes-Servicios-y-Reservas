
# ============================================================
# UNAD - PROGRAMACION (213023)
# FASE 4: PRACTICAS SIMULADAS
# PRUEBAS DE EXCEPCIONES PERSONALIZADAS Y LOGS
# ============================================================

from excepciones import ReservaError
from logger import registrar_log


def procesar_reserva_invalida():
    """
    Simula una operacion de reserva que genera un error
    de validacion y lo transforma en una excepcion
    personalizada mediante encadenamiento.
    """

    try:
        duracion = 0

        if duracion <= 0:
            raise ValueError(
                "La duracion de la reserva debe ser mayor que cero."
            )

    except ValueError as error:
        raise ReservaError(
            "No fue posible procesar la reserva."
        ) from error


def ejecutar_prueba():

    registrar_log(
        "Inicio de prueba de excepciones personalizadas.",
        "INFO"
    )

    try:
        procesar_reserva_invalida()

    except ReservaError as error:

        print("Excepcion personalizada capturada correctamente.")
        print("Mensaje:", error)

        registrar_log(
            f"ReservaError: {error}. "
            f"Causa original: {error.__cause__}",
            "ERROR"
        )

    else:
        print("Reserva procesada correctamente.")

    finally:
        registrar_log(
            "Finalizo la prueba de excepciones.",
            "INFO"
        )
        print("Prueba de excepciones finalizada.")


if __name__ == "__main__":
    ejecutar_prueba()
