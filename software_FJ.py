
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACION (213023)
# FASE 4: PRACTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ============================================================

import unittest
import sys

# ============================================================
# 1. IMPORTACION DE MODULOS DEL PROYECTO
# ============================================================

from entidad import Entidad
from cliente import Cliente
from reserva import Reserva
from servicios import (
    Servicio,
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas,
)


# ============================================================
# 2. SERVICIOS FICTICIOS PARA LAS PRUEBAS UNITARIAS
# ============================================================

class ServicioTemporal:

    def __init__(self, tarifa_hora=45000):
        self.nombre = "Reserva de sala"
        self.tarifa_hora = tarifa_hora

    def calcular_costo(self, duracion):
        return self.tarifa_hora * duracion


class ServicioCostoInvalido:

    def __init__(self, resultado):
        self.nombre = "Servicio de prueba"
        self.resultado = resultado

    def calcular_costo(self, duracion):
        return self.resultado


# ============================================================
# 3. PRUEBAS UNITARIAS
# ============================================================

class PruebasSoftwareFJ(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(
            "FJ-CLI-005",
            "Julieta Salazar",
            "julieta.salazar@example.com",
            "3105550105"
        )

        self.servicio = ServicioTemporal()

    def crear_reserva(self, duracion=2, servicio=None):
        if servicio is None:
            servicio = self.servicio

        return Reserva(
            "FJ-RES-005",
            self.cliente,
            servicio,
            duracion
        )

    def test_reserva_inicia_pendiente(self):
        reserva = self.crear_reserva()
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertIsNone(reserva.costo_total)

    def test_confirmacion_calcula_costo(self):
        reserva = self.crear_reserva()
        reserva.confirmar_reserva()
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)
        self.assertEqual(reserva.costo_total, 90000)

    def test_duracion_decimal(self):
        reserva = self.crear_reserva(1.5)
        self.assertEqual(reserva.calcular_costo(), 67500)

    def test_duracion_cero(self):
        with self.assertRaises(ValueError):
            self.crear_reserva(0)

    def test_duracion_booleana(self):
        with self.assertRaises(TypeError):
            self.crear_reserva(True)

    def test_duracion_infinita(self):
        with self.assertRaises(ValueError):
            self.crear_reserva(float("inf"))

    def test_servicio_sin_metodo(self):
        with self.assertRaises(TypeError):
            self.crear_reserva(servicio=object())

    def test_costo_negativo(self):
        servicio = ServicioCostoInvalido(-100)
        reserva = self.crear_reserva(servicio=servicio)

        with self.assertRaises(ValueError):
            reserva.confirmar_reserva()

        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertIsNone(reserva.costo_total)

    def test_costo_no_numerico(self):
        servicio = ServicioCostoInvalido("No disponible")
        reserva = self.crear_reserva(servicio=servicio)

        with self.assertRaises(TypeError):
            reserva.confirmar_reserva()

        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

    def test_actualizar_duracion_pendiente(self):
        reserva = self.crear_reserva()
        reserva.actualizar_duracion(3)

        self.assertEqual(reserva.duracion, 3)
        self.assertEqual(reserva.calcular_costo(), 135000)

    def test_no_modificar_reserva_confirmada(self):
        reserva = self.crear_reserva()
        reserva.confirmar_reserva()

        with self.assertRaises(ValueError):
            reserva.actualizar_duracion(4)

        self.assertEqual(reserva.duracion, 2)

    def test_no_confirmar_reserva_cancelada(self):
        reserva = self.crear_reserva()
        reserva.cancelar_reserva()

        with self.assertRaises(ValueError):
            reserva.procesar_reserva()

        self.assertEqual(reserva.estado, Reserva.CANCELADA)

    def test_actualizar_nombre_cliente(self):
        self.cliente.actualizar_nombre("Julieta Mendoza")

        self.assertEqual(
            self.cliente.nombre,
            "Julieta Mendoza"
        )

    def test_nombre_invalido_conserva_dato(self):
        nombre_original = self.cliente.nombre

        with self.assertRaises(ValueError):
            self.cliente.actualizar_nombre("   ")

        self.assertEqual(
            self.cliente.nombre,
            nombre_original
        )


# ============================================================
# 4. PROGRAMA PRINCIPAL DE INTEGRACION
# ============================================================

def ejecutar_sistema():

    print("=" * 60)
    print("SISTEMA INTEGRAL SOFTWARE FJ")
    print("UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD")
    print("=" * 60)

    try:
        # CREACION DEL CLIENTE

        cliente = Cliente(
            "C001",
            "Maria Perez",
            "maria@gmail.com",
            "3001234567"
        )

        print("\nINFORMACION DEL CLIENTE")
        print(cliente.mostrar_informacion())

        # CREACION DE LOS SERVICIOS

        sala = ReservaSalas(
            "S001",
            "Sala de reuniones",
            20,
            "Piso 2"
        )

        equipos = AlquilerEquipos(
            "E001",
            "Alquiler de computadores",
            "Computadores",
            2
        )

        asesoria = AsesoriasEspecializadas(
            "A001",
            "Asesoria de software",
            "Desarrollo de software",
            "Carlos Ramirez"
        )

        servicios = [sala, equipos, asesoria]

        # PRUEBAS DE COSTOS, DESCUENTOS E IMPUESTOS

        print("\n")
        print("=" * 60)
        print("PRUEBAS DE DESCUENTOS E IMPUESTOS")
        print("=" * 60)

        for servicio in servicios:

            print(f"\nServicio: {servicio.nombre}")

            print(
                "Tarifa original:",
                f"${servicio.TARIFA_POR_HORA:,.0f}"
            )

            print(
                "Costo normal:",
                f"${servicio.calcular_costo(2):,.2f}"
            )

            print(
                "Con descuento del 10%:",
                f"${servicio.calcular_costo(2, descuento=10):,.2f}"
            )

            print(
                "Con descuento e impuesto:",
                f"${servicio.calcular_costo(2, descuento=10, impuesto=19):,.2f}"
            )

        # CREACION DE LAS RESERVAS

        reserva1 = Reserva("R001", cliente, sala, 1.5)
        reserva2 = Reserva("R002", cliente, equipos, 1.5)
        reserva3 = Reserva("R003", cliente, asesoria, 1.25)

        reservas = [reserva1, reserva2, reserva3]

        # CONFIRMACION DE RESERVAS

        print("\n")
        print("=" * 60)
        print("CONFIRMACION DE RESERVAS")
        print("=" * 60)

        for reserva in reservas:

            print("\n" + reserva.confirmar_reserva())
            print(reserva.mostrar_informacion())
            print("-" * 60)

        print("\nSistema ejecutado correctamente.")

    except (TypeError, ValueError) as error:
        print("\nERROR EN EL SISTEMA:", error)


# ============================================================
# 5. EJECUCION DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    # Si se ejecuta con --test, se ejecutan las pruebas unitarias.

    if "--test" in sys.argv:

        unittest.main(
            argv=[sys.argv[0]],
            verbosity=2
        )

    else:
        ejecutar_sistema()
