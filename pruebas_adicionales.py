
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: pruebas_adicionales.py
# RESPONSABLE: Isabella Pineda Rodríguez
# ============================================================

# unittest proporciona herramientas para comprobar
# automáticamente el comportamiento del programa.
import unittest

# Se importan las clases que serán evaluadas.
from cliente import Cliente
from reserva import Reserva


# Esta clase representa un servicio ficticio de prueba.
# No forma parte del módulo definitivo de María Paula.
class ServicioTemporal:

    # El constructor recibe un costo por hora.
    def __init__(self, tarifa_hora=45000):
        self.nombre = "Reserva de sala"
        self.tarifa_hora = tarifa_hora

    # El método calcula el costo según la duración.
    def calcular_costo(self, duracion):
        return self.tarifa_hora * duracion


# Esta clase permite simular servicios que devuelven
# costos inválidos para comprobar las excepciones.
class ServicioCostoInvalido:

    # El constructor almacena el resultado simulado.
    def __init__(self, resultado):
        self.nombre = "Servicio de prueba"
        self.resultado = resultado

    # El método devuelve el valor indicado para la prueba.
    def calcular_costo(self, duracion):
        return self.resultado


# TestCase proporciona métodos para verificar resultados,
# comparar valores y comprobar excepciones esperadas.
class PruebasSoftwareFJ(unittest.TestCase):

    # setUp se ejecuta antes de cada prueba.
    # Esto garantiza que cada escenario utilice objetos
    # nuevos e independientes de las demás operaciones.
    def setUp(self):

        # Se crea un cliente ficticio con datos válidos.
        self.cliente = Cliente(
            "FJ-CLI-005",
            "Julieta Salazar",
            "julieta.salazar@example.com",
            "3105550105"
        )

        # Se crea un servicio temporal con tarifa por hora.
        self.servicio = ServicioTemporal()

    # Este método auxiliar construye una reserva válida
    # para reutilizarla en diferentes escenarios.
    def crear_reserva(self, duracion=2, servicio=None):

        # Se utiliza el servicio temporal cuando no
        # se proporciona uno diferente.
        if servicio is None:
            servicio = self.servicio

        # Se devuelve una reserva nueva y pendiente.
        return Reserva(
            "FJ-RES-005",
            self.cliente,
            servicio,
            duracion
        )

    # PRUEBA 1: CREACIÓN CORRECTA DE UNA RESERVA.
    def test_reserva_inicia_pendiente(self):

        # Se crea una reserva con información válida.
        reserva = self.crear_reserva()

        # Se verifica que el estado inicial sea PENDIENTE.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

        # Se comprueba que todavía no exista un costo final.
        self.assertIsNone(reserva.costo_total)

    # PRUEBA 2: CONFIRMACIÓN Y CÁLCULO DE COSTO.
    def test_confirmacion_calcula_costo(self):

        # Se crea y confirma una reserva.
        reserva = self.crear_reserva()
        reserva.confirmar_reserva()

        # Se comprueban el estado y el costo calculado.
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)
        self.assertEqual(reserva.costo_total, 90000)

    # PRUEBA 3: DURACIÓN DECIMAL VÁLIDA.
    def test_duracion_decimal(self):

        # Se crea una reserva de una hora y media.
        reserva = self.crear_reserva(1.5)

        # Se verifica el cálculo correspondiente.
        self.assertEqual(reserva.calcular_costo(), 67500)

    # PRUEBA 4: DURACIÓN IGUAL A CERO.
    def test_duracion_cero(self):

        # assertRaises comprueba que la operación
        # genere una excepción del tipo esperado.
        with self.assertRaises(ValueError):
            self.crear_reserva(0)

    # PRUEBA 5: DURACIÓN BOOLEANA.
    def test_duracion_booleana(self):

        # Se verifica que True no sea aceptado
        # como una duración numérica válida.
        with self.assertRaises(TypeError):
            self.crear_reserva(True)

    # PRUEBA 6: DURACIÓN INFINITA.
    def test_duracion_infinita(self):

        # Se comprueba el rechazo de valores infinitos.
        with self.assertRaises(ValueError):
            self.crear_reserva(float("inf"))

    # PRUEBA 7: SERVICIO SIN MÉTODO DE COSTO.
    def test_servicio_sin_metodo(self):

        # Un objeto sin calcular_costo no debe
        # ser aceptado como servicio de una reserva.
        with self.assertRaises(TypeError):
            self.crear_reserva(servicio=object())

    # PRUEBA 8: COSTO NEGATIVO.
    def test_costo_negativo(self):

        # Se crea un servicio que devuelve un costo inválido.
        servicio = ServicioCostoInvalido(-100)

        # Se crea una reserva asociada al servicio.
        reserva = self.crear_reserva(servicio=servicio)

        # La confirmación debe generar ValueError.
        with self.assertRaises(ValueError):
            reserva.confirmar_reserva()

        # La reserva debe conservar su estado inicial.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertIsNone(reserva.costo_total)

    # PRUEBA 9: COSTO NO NUMÉRICO.
    def test_costo_no_numerico(self):

        # Se simula un servicio que devuelve texto.
        servicio = ServicioCostoInvalido("No disponible")
        reserva = self.crear_reserva(servicio=servicio)

        # Se comprueba el rechazo del resultado.
        with self.assertRaises(TypeError):
            reserva.confirmar_reserva()

        # El estado debe permanecer sin modificaciones.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

    # PRUEBA 10: ACTUALIZACIÓN VÁLIDA DE DURACIÓN.
    def test_actualizar_duracion_pendiente(self):

        # Se crea una reserva y se modifica su duración.
        reserva = self.crear_reserva()
        reserva.actualizar_duracion(3)

        # Se comprueban la duración y el nuevo costo.
        self.assertEqual(reserva.duracion, 3)
        self.assertEqual(reserva.calcular_costo(), 135000)

    # PRUEBA 11: MODIFICACIÓN DE RESERVA CONFIRMADA.
    def test_no_modificar_reserva_confirmada(self):

        # Se confirma la reserva antes de modificarla.
        reserva = self.crear_reserva()
        reserva.confirmar_reserva()

        # Se comprueba que el cambio sea rechazado.
        with self.assertRaises(ValueError):
            reserva.actualizar_duracion(4)

        # La duración original debe conservarse.
        self.assertEqual(reserva.duracion, 2)

    # PRUEBA 12: CONFIRMACIÓN DE RESERVA CANCELADA.
    def test_no_confirmar_reserva_cancelada(self):

        # Se crea y cancela una reserva pendiente.
        reserva = self.crear_reserva()
        reserva.cancelar_reserva()

        # Se verifica que no pueda confirmarse.
        with self.assertRaises(ValueError):
            reserva.procesar_reserva()

        # El estado debe permanecer CANCELADA.
        self.assertEqual(reserva.estado, Reserva.CANCELADA)

    # PRUEBA 13: ACTUALIZACIÓN VÁLIDA DEL NOMBRE.
    def test_actualizar_nombre_cliente(self):

        # Se actualiza el nombre del cliente.
        self.cliente.actualizar_nombre("Julieta Mendoza")

        # Se comprueba que el nuevo valor se almacene.
        self.assertEqual(
            self.cliente.nombre,
            "Julieta Mendoza"
        )

    # PRUEBA 14: ACTUALIZACIÓN INVÁLIDA DEL NOMBRE.
    def test_nombre_invalido_conserva_dato(self):

        # Se almacena el nombre original.
        nombre_original = self.cliente.nombre

        # Se intenta actualizarlo con espacios vacíos.
        with self.assertRaises(ValueError):
            self.cliente.actualizar_nombre("   ")

        # Se verifica que el nombre no haya cambiado.
        self.assertEqual(
            self.cliente.nombre,
            nombre_original
        )


# Esta condición permite ejecutar las pruebas
# cuando el archivo se inicia directamente.
if __name__ == "__main__":

    # verbosity=2 presenta el nombre y resultado
    # individual de cada prueba ejecutada.
    unittest.main(verbosity=2)
