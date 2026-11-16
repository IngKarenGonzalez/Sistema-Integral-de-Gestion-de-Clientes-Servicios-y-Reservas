# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: simulacion.py
# RESPONSABLE: [Jhon Alexis Sabogal Castañeda]
# FUNCIÓN: Simulaciones, pruebas de estabilidad y verificación de logs
# ============================================================
#
# NOTA DE INTEGRACIÓN: si el equipo agrega excepciones personalizadas,
# basta con que hereden de ValueError o TypeError para que las
# operaciones sigan reconociendo los errores esperados. Si no, se
# actualiza el tercer valor de cada fila en la lista OPERACIONES.
#
# Este script ejecuta 20 operaciones sobre las clases del proyecto
# (válidas e inválidas). Cada operación se ejecuta de forma aislada:
# si una falla, el programa continúa con la siguiente.
#
# Cada operación queda registrada en "logs_software_fj.log".
# Al final se muestra un resumen y se verifica el contenido del log.
#
# Veredictos posibles:
#   OK                    -> operación válida que funcionó
#   OK (error controlado) -> operación inválida rechazada con la
#                            excepción esperada
#   DEFECTO               -> el sistema NO se comportó como debía
#                            (se reporta al responsable del componente)

import logging
import os

from cliente import Cliente
from reserva import Reserva
from servicios import (
    Servicio,
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas,
)

RUTA_LOG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "logs_software_fj.log"
)


# ------------------------------------------------------------
# CONFIGURACIÓN DEL ARCHIVO DE LOGS
# ------------------------------------------------------------

def configurar_log():
    """Crea el logger que escribe eventos y errores en el archivo."""
    logger = logging.getLogger("software_fj")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # mode="w" reinicia el archivo en cada ejecución para que
    # la verificación final cuente solo esta corrida.
    manejador = logging.FileHandler(RUTA_LOG, mode="w", encoding="utf-8")
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    )
    logger.addHandler(manejador)
    return logger


log = configurar_log()

# Resultados de cada operación y objetos compartidos entre operaciones.
resultados = []
contexto = {}


# ------------------------------------------------------------
# EJECUTOR DE OPERACIONES (aísla cada operación)
# ------------------------------------------------------------

def exigir(condicion, mensaje):
    """Falla la operación si el resultado no es el esperado."""
    if not condicion:
        raise AssertionError(mensaje)


def ejecutar_operacion(numero, descripcion, funcion, error_esperado=None):
    """
    Ejecuta una operación sin que sus errores detengan el programa.

    error_esperado: tipo de excepción que DEBE producir la operación
                    (None si debe terminar correctamente).
    """
    etiqueta = f"OP-{numero:02d}"
    veredicto = "DEFECTO"
    detalle = ""

    log.info("%s INICIO: %s", etiqueta, descripcion)

    try:
        resultado = funcion()

    except Exception as error:
        tipo = type(error).__name__
        detalle = f"{tipo}: {error}"

        if error_esperado is not None and isinstance(error, error_esperado):
            veredicto = "OK (error controlado)"
            log.warning(
                "%s ERROR CONTROLADO (%s): %s", etiqueta, tipo, error
            )
        else:
            veredicto = "DEFECTO"
            log.error(
                "%s ERROR INESPERADO (%s): %s",
                etiqueta, tipo, error, exc_info=True
            )

    else:
        detalle = str(resultado)

        if error_esperado is None:
            veredicto = "OK"
            log.info("%s COMPLETADA: %s", etiqueta, resultado)
        else:
            veredicto = "DEFECTO"
            log.error(
                "%s DEBIÓ FALLAR con %s pero terminó sin error. "
                "Resultado: %r",
                etiqueta, error_esperado.__name__, resultado
            )

    finally:
        log.info("%s FIN", etiqueta)
        resultados.append((numero, descripcion, veredicto, detalle))


# ------------------------------------------------------------
# DEFINICIÓN DE LAS 20 OPERACIONES
# ------------------------------------------------------------

def op_cliente_valido():
    contexto["cliente"] = Cliente(
        "C001", "María Pérez", "maria@gmail.com", "3001234567"
    )
    return contexto["cliente"].mostrar_informacion().replace("\n", " | ")


def op_cliente_correo_invalido():
    return Cliente("C002", "Juan Gómez", "juan-sin-arroba.com", "3001234567")


def op_cliente_telefono_letras():
    return Cliente("C003", "Ana Ruiz", "ana@mail.com", "30012ABC67")


def op_cliente_nombre_none():
    return Cliente("C004", None, "x@mail.com", "3001234567")


def op_sala_valida():
    contexto["sala"] = ReservaSalas("S001", "Sala de reuniones", 20, "Piso 2")
    return f"Sala creada, capacidad {contexto['sala'].capacidad}"


def op_sala_capacidad_negativa():
    return ReservaSalas("S002", "Sala errónea", -5, "Piso 1")


def op_equipos_cantidad_decimal():
    return AlquilerEquipos("E002", "Equipos", "Portátiles", 2.5)


def op_servicio_abstracto():
    return Servicio("X001", "Servicio genérico")


def op_asesoria_costo_con_descuento_e_impuesto():
    asesoria = AsesoriasEspecializadas(
        "A001", "Asesoría de software", "Desarrollo", "Carlos Ramírez"
    )
    costo = asesoria.calcular_costo(2, descuento=10, impuesto=19)
    # 80.000 x 2 = 160.000 -> -10% = 144.000 -> +19% = 171.360
    exigir(abs(costo - 171360) < 0.01, f"Costo incorrecto: {costo}")
    return f"Costo calculado: {costo:,.2f}"


def op_descuento_mayor_a_100():
    return contexto["sala"].calcular_costo(2, descuento=150)


def op_reserva_valida_y_confirmada():
    reserva = Reserva("R001", contexto["cliente"], contexto["sala"], 1.5)
    mensaje = reserva.confirmar_reserva()
    exigir(reserva.estado == Reserva.CONFIRMADA, "No quedó CONFIRMADA")
    exigir(reserva.costo_total == 75000, f"Costo: {reserva.costo_total}")
    contexto["reserva"] = reserva
    return f"{mensaje} Costo: {reserva.costo_total:,.0f}"


def op_reserva_duracion_cero():
    return Reserva("R002", contexto["cliente"], contexto["sala"], 0)


def op_reserva_cliente_invalido():
    return Reserva("R003", "no soy un cliente", contexto["sala"], 2)


def op_confirmar_reserva_ya_confirmada():
    return contexto["reserva"].confirmar_reserva()


def op_cancelar_dos_veces():
    reserva = Reserva("R004", contexto["cliente"], contexto["sala"], 1)
    reserva.cancelar_reserva()       # primera cancelación: válida
    return reserva.cancelar_reserva()  # segunda: debe fallar


def op_confirmar_reserva_cancelada():
    reserva = Reserva("R005", contexto["cliente"], contexto["sala"], 1)
    reserva.cancelar_reserva()
    return reserva.procesar_reserva()


def op_servicio_duracion_nan():
    return contexto["sala"].calcular_costo(float("nan"))


def op_servicio_impuesto_infinito():
    return contexto["sala"].calcular_costo(2, impuesto=float("inf"))


def op_cancelar_confirmada_limpia_costo():
    reserva = Reserva("R006", contexto["cliente"], contexto["sala"], 2)
    reserva.confirmar_reserva()
    reserva.cancelar_reserva()
    exigir(
        reserva.costo_total in (None, 0),
        f"La reserva cancelada conserva costo_total = {reserva.costo_total}"
    )
    return "Costo limpio tras cancelar"


def op_estabilidad_final():
    cliente = contexto["cliente"]
    reserva = contexto["reserva"]
    exigir(cliente.nombre == "María Pérez", "Cliente alterado")
    exigir(cliente.correo == "maria@gmail.com", "Correo alterado")
    exigir(reserva.estado == Reserva.CONFIRMADA, "Reserva alterada")
    exigir(reserva.costo_total == 75000, "Costo de reserva alterado")
    return "Objetos válidos intactos después de todos los errores"


OPERACIONES = [
    ("Registrar cliente válido", op_cliente_valido, None),
    ("Cliente con correo inválido", op_cliente_correo_invalido, ValueError),
    ("Cliente con teléfono con letras", op_cliente_telefono_letras, ValueError),
    ("Cliente con nombre None", op_cliente_nombre_none, TypeError),
    ("Crear servicio de sala válido", op_sala_valida, None),
    ("Sala con capacidad negativa", op_sala_capacidad_negativa, ValueError),
    ("Equipos con cantidad decimal", op_equipos_cantidad_decimal, TypeError),
    ("Instanciar clase abstracta Servicio", op_servicio_abstracto, TypeError),
    ("Asesoría: costo con descuento e impuesto",
     op_asesoria_costo_con_descuento_e_impuesto, None),
    ("Costo con descuento mayor a 100%", op_descuento_mayor_a_100, ValueError),
    ("Reserva válida y confirmada", op_reserva_valida_y_confirmada, None),
    ("Reserva con duración cero", op_reserva_duracion_cero, ValueError),
    ("Reserva con cliente inválido", op_reserva_cliente_invalido, TypeError),
    ("Confirmar reserva ya confirmada",
     op_confirmar_reserva_ya_confirmada, ValueError),
    ("Cancelar una reserva dos veces", op_cancelar_dos_veces, ValueError),
    ("Confirmar una reserva cancelada",
     op_confirmar_reserva_cancelada, ValueError),
    ("Servicio con duración NaN", op_servicio_duracion_nan, ValueError),
    ("Servicio con impuesto infinito",
     op_servicio_impuesto_infinito, ValueError),
    ("Coherencia: reserva cancelada sin costo",
     op_cancelar_confirmada_limpia_costo, None),
    ("Estabilidad: objetos válidos intactos", op_estabilidad_final, None),
]


# ------------------------------------------------------------
# VERIFICACIÓN DEL ARCHIVO DE LOGS
# ------------------------------------------------------------

def verificar_log():
    """Comprueba que el log contenga el registro de cada operación."""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DEL ARCHIVO DE LOGS")
    print("=" * 70)

    if not os.path.exists(RUTA_LOG):
        print("DEFECTO: el archivo de logs no existe.")
        return

    with open(RUTA_LOG, encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()

    sin_registro = []
    for numero, *_ in resultados:
        etiqueta = f"OP-{numero:02d}"
        tiene_inicio = any(f"{etiqueta} INICIO" in l for l in lineas)
        tiene_fin = any(f"{etiqueta} FIN" in l for l in lineas)
        if not (tiene_inicio and tiene_fin):
            sin_registro.append(etiqueta)

    controlados = sum("ERROR CONTROLADO" in l for l in lineas)
    inesperados = sum(
        "ERROR INESPERADO" in l or "DEBIÓ FALLAR" in l for l in lineas
    )

    print(f"Archivo: {RUTA_LOG}")
    print(f"Líneas registradas: {len(lineas)}")
    print(f"Operaciones con INICIO y FIN registrados: "
          f"{len(resultados) - len(sin_registro)}/{len(resultados)}")
    print(f"Errores controlados registrados: {controlados}")
    print(f"Defectos registrados: {inesperados}")

    if sin_registro:
        print("DEFECTO: operaciones sin registro completo:", sin_registro)
    else:
        print("OK: todas las operaciones quedaron registradas en el log.")


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

def ejecutar_simulaciones():
    print("=" * 70)
    print("SIMULACIONES - SISTEMA INTEGRAL SOFTWARE FJ")
    print("=" * 70)

    log.info("===== INICIO DE LAS SIMULACIONES =====")

    for numero, (descripcion, funcion, error) in enumerate(OPERACIONES, 1):
        ejecutar_operacion(numero, descripcion, funcion, error)

    log.info("===== FIN DE LAS SIMULACIONES =====")

    print(f"\n{'#':<4}{'VEREDICTO':<24}OPERACIÓN")
    print("-" * 70)
    for numero, descripcion, veredicto, _ in resultados:
        print(f"{numero:<4}{veredicto:<24}{descripcion}")

    total = len(resultados)
    ok = sum(v.startswith("OK") for _, _, v, _ in resultados)
    defectos = [(n, d, det) for n, d, v, det in resultados if v == "DEFECTO"]

    print("-" * 70)
    print(f"Operaciones ejecutadas: {total} | OK: {ok} | "
          f"Defectos: {len(defectos)}")
    print("El programa terminó las operaciones sin detenerse "
          "(prueba de estabilidad).")

    if defectos:
        print("\nDEFECTOS PARA REPORTAR AL EQUIPO:")
        for numero, descripcion, detalle in defectos:
            print(f"  OP-{numero:02d} {descripcion}\n      -> {detalle}")

    verificar_log()


if __name__ == "__main__":
    ejecutar_simulaciones()
