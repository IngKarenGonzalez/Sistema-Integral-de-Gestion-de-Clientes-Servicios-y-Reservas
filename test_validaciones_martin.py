# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: test_validaciones_martin.py
# RESPONSABLE: Martín García
# ISSUE: #13 - Incorporar pruebas adicionales y fortalecer validaciones
# ============================================================

import unittest

from entidad import Entidad
from cliente import Cliente
from reserva import Reserva
from servicios import (
    Servicio,
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas,
)
from excepciones import (
    SoftwareFJError,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaError,
)


class PruebasValidacionesMartin(unittest.TestCase):
    """
    Batería de pruebas unitarias adicionales enfocadas en validar
    reglas de negocio, herencia de Entidad, servicios especializados,
    consistencia de datos y jerarquía de excepciones personalizadas.
    """

    def setUp(self):
        """Prepara instancias válidas antes de ejecutar cada prueba."""
        self.cliente = Cliente(
            "FJ-CLI-101",
            "Martín García",
            "martin.garcia@unadvirtual.edu.co",
            "3154897620"
        )
        self.sala = ReservaSalas("FJ-SAL-101", "Sala Ejecutiva", 15, "Piso 3")
        self.equipos = AlquilerEquipos("FJ-EQU-101", "Portátiles Dell", "Laptop", 3)
        self.asesoria = AsesoriasEspecializadas(
            "FJ-ASE-101",
            "Consultoría Python",
            "Arquitectura de Software",
            "Ing. Carlos Ramírez"
        )

    # --------------------------------------------------------
    # PRUEBA 01: VALIDACIÓN DE IDENTIFICADOR EN CLASE BASE ENTIDAD
    # --------------------------------------------------------
    def test_identificador_invalido_en_entidad(self):
        """Verifica que Entidad rechace identificadores vacíos o no textuales."""
        with self.assertRaises(ValueError):
            Cliente("   ", "Carlos Ruiz", "carlos@mail.com", "3001112233")

        with self.assertRaises(TypeError):
            Cliente(12345, "Carlos Ruiz", "carlos@mail.com", "3001112233")

    # --------------------------------------------------------
    # PRUEBA 02: PROHIBICIÓN DE INSTANCIAR CLASES ABSTRACTAS
    # --------------------------------------------------------
    def test_no_instanciar_clases_abstractas(self):
        """Verifica que no se puedan instanciar Entidad ni Servicio directamente."""
        with self.assertRaises(TypeError):
            Entidad("ENT-001")

        with self.assertRaises(TypeError):
            Servicio("SER-000", "Servicio Genérico")

    # --------------------------------------------------------
    # PRUEBA 03: ACTUALIZACIÓN Y VALIDACIÓN DE CORREO EN CLIENTE
    # --------------------------------------------------------
    def test_actualizar_correo_valido_e_invalido(self):
        """Verifica normalización de correo válido y rechazo de formato inválido."""
        self.cliente.actualizar_correo("  NUEVO.CORREO@UNAD.EDU.CO  ")
        self.assertEqual(self.cliente.correo, "nuevo.correo@unad.edu.co")

        with self.assertRaises(ValueError):
            self.cliente.actualizar_correo("correo_sin_arroba.com")

        # El correo válido anterior debe conservarse tras el error
        self.assertEqual(self.cliente.correo, "nuevo.correo@unad.edu.co")

    # --------------------------------------------------------
    # PRUEBA 04: ACTUALIZACIÓN Y VALIDACIÓN DE TELÉFONO EN CLIENTE
    # --------------------------------------------------------
    def test_actualizar_telefono_longitud_y_formato(self):
        """Verifica rechazo de teléfonos muy cortos o con caracteres no numéricos."""
        telefono_inicial = self.cliente.telefono

        with self.assertRaises(ValueError):
            self.cliente.actualizar_telefono("12345")

        with self.assertRaises(ValueError):
            self.cliente.actualizar_telefono("300-456-7890")

        self.assertEqual(self.cliente.telefono, telefono_inicial)

    # --------------------------------------------------------
    # PRUEBA 05: VALIDACIÓN DE CAPACIDAD Y UBICACIÓN EN SALAS
    # --------------------------------------------------------
    def test_reserva_salas_parametros_invalidos(self):
        """Comprueba que ReservaSalas rechace capacidad <= 0, decimal o ubicación vacía."""
        with self.assertRaises(ValueError):
            ReservaSalas("S-ERR-1", "Sala Norte", 0, "Piso 1")

        with self.assertRaises(TypeError):
            ReservaSalas("S-ERR-2", "Sala Norte", 10.5, "Piso 1")

        with self.assertRaises(ValueError):
            ReservaSalas("S-ERR-3", "Sala Norte", 10, "   ")

    # --------------------------------------------------------
    # PRUEBA 06: VALIDACIÓN DE CANTIDAD Y EQUIPO EN ALQUILER
    # --------------------------------------------------------
    def test_alquiler_equipos_parametros_invalidos(self):
        """Comprueba que AlquilerEquipos rechace cantidad <= 0 o tipo vacío."""
        with self.assertRaises(ValueError):
            AlquilerEquipos("E-ERR-1", "Proyector", "VideoBeam", 0)

        with self.assertRaises(ValueError):
            AlquilerEquipos("E-ERR-2", "Proyector", "   ", 2)

    # --------------------------------------------------------
    # PRUEBA 07: VALIDACIÓN DE ESPECIALIDAD Y ASESOR EN ASESORÍAS
    # --------------------------------------------------------
    def test_asesorias_parametros_invalidos(self):
        """Comprueba que AsesoriasEspecializadas rechace especialidad o asesor vacíos."""
        with self.assertRaises(ValueError):
            AsesoriasEspecializadas("A-ERR-1", "Asesoría", "", "Carlos")

        with self.assertRaises(ValueError):
            AsesoriasEspecializadas("A-ERR-2", "Asesoría", "Redes", "   ")

    # --------------------------------------------------------
    # PRUEBA 08: CÁLCULO POLIMÓRFICO CON CANTIDAD EN EQUIPOS
    # --------------------------------------------------------
    def test_calculo_costo_alquiler_equipos_por_cantidad(self):
        """Verifica que AlquilerEquipos multiplique tarifa * duración * cantidad."""
        # 35.000 * 2 horas * 3 equipos = 210.000
        costo = self.equipos.calcular_costo(2)
        self.assertEqual(costo, 210000)

    # --------------------------------------------------------
    # PRUEBA 09: DESCUENTO NEGATIVO Y MAYOR A 100% EN SERVICIOS
    # --------------------------------------------------------
    def test_descuento_fuera_de_rango(self):
        """Comprueba que no se acepten descuentos negativos ni mayores al 100%."""
        with self.assertRaises(ValueError):
            self.sala.calcular_costo(2, descuento=-5)

        with self.assertRaises(ValueError):
            self.sala.calcular_costo(2, descuento=101)

    # --------------------------------------------------------
    # PRUEBA 10: IMPUESTO NEGATIVO O BOOLEANO EN SERVICIOS
    # --------------------------------------------------------
    def test_impuesto_invalido(self):
        """Comprueba que se rechacen impuestos negativos o booleanos."""
        with self.assertRaises(ValueError):
            self.asesoria.calcular_costo(2, impuesto=-19)

        with self.assertRaises(TypeError):
            self.asesoria.calcular_costo(2, impuesto=True)

    # --------------------------------------------------------
    # PRUEBA 11: CÁLCULO INTEGRAL CON DESCUENTO E IMPUESTO
    # --------------------------------------------------------
    def test_calculo_completo_asesoria_descuento_impuesto(self):
        """Verifica el cálculo exacto con descuento del 10% e IVA del 19%."""
        # 80.000 * 2 = 160.000 -> -10% = 144.000 -> +19% = 171.360
        costo = self.asesoria.calcular_costo(2, descuento=10, impuesto=19)
        self.assertAlmostEqual(costo, 171360.0, places=2)

    # --------------------------------------------------------
    # PRUEBA 12: INTEGRACIÓN REAL RESERVA + SERVICIO ESPECIALIZADO
    # --------------------------------------------------------
    def test_reserva_con_servicio_real_confirmada(self):
        """Verifica creación y confirmación de Reserva usando ReservaSalas real."""
        reserva = Reserva("FJ-RES-201", self.cliente, self.sala, 3)
        mensaje = reserva.confirmar_reserva()

        self.assertEqual(mensaje, "Reserva confirmada correctamente.")
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)
        self.assertEqual(reserva.costo_total, 150000)

    # --------------------------------------------------------
    # PRUEBA 13: IMPEDIR CÁLCULO DE COSTO EN RESERVA CANCELADA
    # --------------------------------------------------------
    def test_no_calcular_costo_reserva_cancelada(self):
        """Comprueba que calcular_costo falle si la reserva ya fue cancelada."""
        reserva = Reserva("FJ-RES-202", self.cliente, self.equipos, 2)
        reserva.cancelar_reserva()

        with self.assertRaises(ValueError):
            reserva.calcular_costo()

    # --------------------------------------------------------
    # PRUEBA 14: JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
    # --------------------------------------------------------
    def test_jerarquia_excepciones_personalizadas(self):
        """Verifica que todas las excepciones específicas hereden de SoftwareFJError."""
        self.assertTrue(issubclass(ClienteInvalidoError, SoftwareFJError))
        self.assertTrue(issubclass(ServicioNoDisponibleError, SoftwareFJError))
        self.assertTrue(issubclass(ReservaError, SoftwareFJError))

    # --------------------------------------------------------
    # PRUEBA 15: ENCADENAMIENTO DE EXCEPCIONES CON DATOS REALES
    # --------------------------------------------------------
    def test_encadenamiento_excepcion_cliente_y_reserva(self):
        """Verifica el encadenamiento (raise ... from ...) ante fallos de validación."""
        with self.assertRaises(ClienteInvalidoError) as contexto_cliente:
            try:
                Cliente("C-ERR", "Ana", "correo_invalido", "3001234567")
            except ValueError as err:
                raise ClienteInvalidoError("Fallo al registrar cliente.") from err

        self.assertIsInstance(contexto_cliente.exception.__cause__, ValueError)

        with self.assertRaises(ReservaError) as contexto_reserva:
            try:
                reserva = Reserva("R-ERR", self.cliente, self.sala, 2)
                reserva.cancelar_reserva()
                reserva.confirmar_reserva()
            except ValueError as err:
                raise ReservaError("No se pudo confirmar reserva cancelada.") from err

        self.assertIsInstance(contexto_reserva.exception.__cause__, ValueError)


if __name__ == "__main__":
    unittest.main(verbosity=2)
