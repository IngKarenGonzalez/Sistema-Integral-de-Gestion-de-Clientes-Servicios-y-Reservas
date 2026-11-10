
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACION (213023)
# FASE 4: PRACTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ============================================================

import re
import math
import unittest
import sys
from abc import ABC, abstractmethod

# ============================================================
# 1. CLASE ABSTRACTA ENTIDAD
# ============================================================

class Entidad(ABC):

    def __init__(self, identificador):

        if not isinstance(identificador, str):
            raise TypeError(
                "El identificador debe ser una cadena de texto."
            )

        identificador = identificador.strip()

        if not identificador:
            raise ValueError(
                "El identificador no puede estar vacio."
            )

        self.__identificador = identificador

    @property
    def identificador(self):
        return self.__identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass

# ============================================================
# 2. CLASE CLIENTE
# ============================================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        self.__nombre = self.validar_nombre(nombre)
        self.__correo = self.validar_correo(correo)
        self.__telefono = self.validar_telefono(telefono)

    @staticmethod
    def validar_nombre(nombre):

        if not isinstance(nombre, str):
            raise TypeError(
                "El nombre debe ser una cadena de texto."
            )

        nombre = " ".join(nombre.split())

        if not nombre:
            raise ValueError(
                "El nombre del cliente no puede estar vacio."
            )

        if len(nombre) < 2:
            raise ValueError(
                "El nombre debe contener al menos dos caracteres."
            )

        return nombre

    @staticmethod
    def validar_correo(correo):

        if not isinstance(correo, str):
            raise TypeError(
                "El correo electronico debe ser un texto."
            )

        correo = correo.strip().lower()

        if not correo:
            raise ValueError(
                "El correo electronico no puede estar vacio."
            )

        patron = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        if re.fullmatch(patron, correo) is None:
            raise ValueError(
                "El correo electronico tiene un formato invalido."
            )

        return correo

    @staticmethod
    def validar_telefono(telefono):

        if not isinstance(telefono, str):
            raise TypeError(
                "El telefono debe proporcionarse como texto."
            )

        telefono = telefono.strip()

        if re.fullmatch(r"[0-9]+", telefono) is None:
            raise ValueError(
                "El telefono debe contener unicamente numeros."
            )

        if not 7 <= len(telefono) <= 15:
            raise ValueError(
                "El telefono debe contener entre 7 y 15 digitos."
            )

        return telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def actualizar_nombre(self, nuevo_nombre):
        self.__nombre = self.validar_nombre(nuevo_nombre)
        return "Nombre actualizado correctamente."

    def actualizar_correo(self, nuevo_correo):
        self.__correo = self.validar_correo(nuevo_correo)
        return "Correo electronico actualizado correctamente."

    def actualizar_telefono(self, nuevo_telefono):
        self.__telefono = self.validar_telefono(nuevo_telefono)
        return "Telefono actualizado correctamente."

    def mostrar_informacion(self):
        return (
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Telefono: {self.telefono}"
        )

# ============================================================
# 3. CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(Entidad):

    def __init__(self, identificador, nombre):
        super().__init__(identificador)

        if not isinstance(nombre, str):
            raise TypeError(
                "El nombre del servicio debe ser texto."
            )

        nombre = nombre.strip()

        if not nombre:
            raise ValueError(
                "El nombre del servicio no puede estar vacio."
            )

        self.__nombre = nombre

    @property
    def nombre(self):
        return self.__nombre

    def _validar_parametros_calculo(
        self, duracion, descuento, impuesto
    ):

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
        ):
            raise TypeError(
                "La duracion debe ser un numero."
            )

        if not math.isfinite(duracion):
            raise ValueError(
                "La duracion debe ser un numero finito."
            )

        if duracion <= 0:
            raise ValueError(
                "La duracion debe ser mayor que cero."
            )

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
        ):
            raise TypeError(
                "El descuento debe ser un numero."
            )

        if not math.isfinite(descuento):
            raise ValueError(
                "El descuento debe ser finito."
            )

        if not 0 <= descuento <= 100:
            raise ValueError(
                "El descuento debe estar entre 0 y 100."
            )

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
        ):
            raise TypeError(
                "El impuesto debe ser un numero."
            )

        if not math.isfinite(impuesto):
            raise ValueError(
                "El impuesto debe ser finito."
            )

        if impuesto < 0:
            raise ValueError(
                "El impuesto no puede ser negativo."
            )

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

# ============================================================
# 4. SERVICIO: RESERVA DE SALAS
# ============================================================

class ReservaSalas(Servicio):

    TARIFA_POR_HORA = 50000

    def __init__(self, identificador, nombre, capacidad, ubicacion):
        super().__init__(identificador, nombre)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool):
            raise TypeError(
                "La capacidad debe ser un numero entero."
            )

        if capacidad <= 0:
            raise ValueError(
                "La capacidad debe ser mayor que cero."
            )

        if not isinstance(ubicacion, str):
            raise TypeError(
                "La ubicacion debe ser texto."
            )

        ubicacion = ubicacion.strip()

        if not ubicacion:
            raise ValueError(
                "La ubicacion no puede estar vacia."
            )

        self.__capacidad = capacidad
        self.__ubicacion = ubicacion

    @property
    def capacidad(self):
        return self.__capacidad

    @property
    def ubicacion(self):
        return self.__ubicacion

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self._validar_parametros_calculo(
            duracion, descuento, impuesto
        )

        subtotal = self.TARIFA_POR_HORA * duracion
        subtotal -= subtotal * (descuento / 100)

        return subtotal + subtotal * (impuesto / 100)

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Reserva de salas\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Ubicacion: {self.ubicacion}\n"
            f"Tarifa por hora: ${self.TARIFA_POR_HORA:,.0f}"
        )

# ============================================================
# 5. SERVICIO: ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipos(Servicio):

    TARIFA_POR_HORA = 35000

    def __init__(self, identificador, nombre, tipo_equipo, cantidad):
        super().__init__(identificador, nombre)

        if not isinstance(tipo_equipo, str):
            raise TypeError(
                "El tipo de equipo debe ser texto."
            )

        tipo_equipo = tipo_equipo.strip()

        if not tipo_equipo:
            raise ValueError(
                "El tipo de equipo no puede estar vacio."
            )

        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError(
                "La cantidad debe ser un numero entero."
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        self.__tipo_equipo = tipo_equipo
        self.__cantidad = cantidad

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @property
    def cantidad(self):
        return self.__cantidad

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self._validar_parametros_calculo(
            duracion, descuento, impuesto
        )

        subtotal = (
            self.TARIFA_POR_HORA * duracion * self.cantidad
        )

        subtotal -= subtotal * (descuento / 100)

        return subtotal + subtotal * (impuesto / 100)

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Alquiler de equipos\n"
            f"Equipo: {self.tipo_equipo}\n"
            f"Cantidad: {self.cantidad}\n"
            f"Tarifa por hora y equipo: ${self.TARIFA_POR_HORA:,.0f}"
        )

# ============================================================
# 6. SERVICIO: ASESORIAS ESPECIALIZADAS
# ============================================================

class AsesoriasEspecializadas(Servicio):

    TARIFA_POR_HORA = 80000

    def __init__(self, identificador, nombre, especialidad, asesor):
        super().__init__(identificador, nombre)

        if not isinstance(especialidad, str):
            raise TypeError(
                "La especialidad debe ser texto."
            )

        especialidad = especialidad.strip()

        if not especialidad:
            raise ValueError(
                "La especialidad no puede estar vacia."
            )

        if not isinstance(asesor, str):
            raise TypeError(
                "El nombre del asesor debe ser texto."
            )

        asesor = asesor.strip()

        if not asesor:
            raise ValueError(
                "El nombre del asesor no puede estar vacio."
            )

        self.__especialidad = especialidad
        self.__asesor = asesor

    @property
    def especialidad(self):
        return self.__especialidad

    @property
    def asesor(self):
        return self.__asesor

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self._validar_parametros_calculo(
            duracion, descuento, impuesto
        )

        subtotal = self.TARIFA_POR_HORA * duracion
        subtotal -= subtotal * (descuento / 100)

        return subtotal + subtotal * (impuesto / 100)

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Asesoria especializada\n"
            f"Especialidad: {self.especialidad}\n"
            f"Asesor: {self.asesor}\n"
            f"Tarifa por hora: ${self.TARIFA_POR_HORA:,.0f}"
        )

# ============================================================
# 7. CLASE RESERVA
# ============================================================

class Reserva(Entidad):

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise TypeError(
                "La reserva requiere un objeto Cliente valido."
            )

        metodo_costo = getattr(servicio, "calcular_costo", None)

        if not callable(metodo_costo):
            raise TypeError(
                "El servicio debe implementar calcular_costo(duracion)."
            )

        duracion_validada = self.validar_duracion(duracion)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion_validada
        self.__estado = self.PENDIENTE
        self.__costo_total = None

    @staticmethod
    def validar_duracion(duracion):

        if isinstance(duracion, bool):
            raise TypeError(
                "La duracion debe ser un numero, no un booleano."
            )

        if not isinstance(duracion, (int, float)):
            raise TypeError(
                "La duracion debe ser un valor numerico."
            )

        if not math.isfinite(duracion):
            raise ValueError(
                "La duracion debe ser un numero finito."
            )

        if duracion <= 0:
            raise ValueError(
                "La duracion debe ser mayor que cero."
            )

        return duracion

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def actualizar_duracion(self, nueva_duracion):

        if self.__estado != self.PENDIENTE:
            raise ValueError(
                "Solo se puede modificar una reserva pendiente."
            )

        duracion_validada = self.validar_duracion(nueva_duracion)
        self.__duracion = duracion_validada

        return "Duracion actualizada correctamente."

    def calcular_costo(self):

        if self.__estado == self.CANCELADA:
            raise ValueError(
                "No se puede calcular el costo de una reserva cancelada."
            )

        costo = self.__servicio.calcular_costo(
            self.__duracion
        )

        if isinstance(costo, bool) or not isinstance(
            costo, (int, float)
        ):
            raise TypeError(
                "El servicio debe devolver un costo numerico."
            )

        if not math.isfinite(costo):
            raise ValueError(
                "El costo calculado debe ser finito."
            )

        if costo < 0:
            raise ValueError(
                "El costo calculado no puede ser negativo."
            )

        return costo

    def confirmar_reserva(self):

        if self.__estado != self.PENDIENTE:
            raise ValueError(
                "Solo se pueden confirmar reservas pendientes."
            )

        costo_validado = self.calcular_costo()

        self.__costo_total = costo_validado
        self.__estado = self.CONFIRMADA

        return "Reserva confirmada correctamente."

    def cancelar_reserva(self):

        if self.__estado == self.CANCELADA:
            raise ValueError(
                "La reserva ya se encuentra cancelada."
            )

        self.__estado = self.CANCELADA

        return "Reserva cancelada correctamente."

    def procesar_reserva(self):
        return self.confirmar_reserva()

    def mostrar_informacion(self):

        nombre_servicio = getattr(
            self.__servicio,
            "nombre",
            type(self.__servicio).__name__
        )

        if self.__costo_total is None:
            costo_texto = "Pendiente de calculo"
        else:
            costo_texto = f"${self.__costo_total:,.2f}"

        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {nombre_servicio}\n"
            f"Duracion: {self.__duracion} horas\n"
            f"Estado: {self.__estado}\n"
            f"Costo total: {costo_texto}"
        )

# ============================================================
# 8. SERVICIOS FICTICIOS PARA LAS PRUEBAS UNITARIAS
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
# 9. PRUEBAS UNITARIAS
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
# 10. PROGRAMA PRINCIPAL DE INTEGRACION
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
# 11. EJECUCION DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    # Si se ejecuta con el argumento --test,
    # se ejecutan las pruebas unitarias.

    if "--test" in sys.argv:

        unittest.main(
            argv=[sys.argv[0]],
            verbosity=2
        )

    else:

        ejecutar_sistema()