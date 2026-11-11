
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: reserva.py
# RESPONSABLE: Isabella Pineda Rodríguez
# ============================================================

# La clase Entidad proporciona la estructura abstracta
# y el identificador común de las entidades del sistema
from entidad import Entidad

# La clase Cliente permite comprobar la asociación
# de cada reserva con un cliente valido
from cliente import Cliente

# El módulo math proporciona isfinite para verificar
# que los valores numéricos sean finitos
import math


# La clase Reserva representa la contratación de un
# servicio por parte de un cliente de Software FJ
# Hereda de Entidad e implementa mostrar_informacion
class Reserva(Entidad):

    # Las constantes identifican los estados permitidos
    # y evitan inconsistencias en las comparaciones.
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    # El constructor establece los datos iniciales
    # de una reserva y verifica su validez
    def __init__(self, identificador, cliente, servicio, duracion):

        # El constructor de Entidad valida y almacena
        # el identificador de la reserva.
        super().__init__(identificador)

        # La asociación requiere una instancia de Cliente.
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "La reserva requiere un objeto Cliente válido."
            )

        # Se comprueba que el servicio disponga de un
        # método ejecutable para calcular su costo.
        # Esta interfaz permitirá integrar las clases
        # desarrolladas por el módulo de servicios.
        metodo_costo = getattr(servicio, "calcular_costo", None)

        if not callable(metodo_costo):
            raise TypeError(
                "El servicio debe implementar calcular_costo(duracion)."
            )

        # La duración se valida antes de almacenarla.
        duracion_validada = self.validar_duracion(duracion)

        # Los atributos privados conservan las referencias
        # al cliente y al servicio asociados
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion_validada

        # La reserva inicia pendiente y sin costo procesado.
        self.__estado = self.PENDIENTE
        self.__costo_total = None

    # Este método comprueba que la duración sea numérica,
    # positiva y finita, y devuelve el valor validado
    @staticmethod
    def validar_duracion(duracion):

        # Los booleanos se rechazan porque Python los
        # considera subtipos de los números enteros
        if isinstance(duracion, bool):
            raise TypeError(
                "La duración debe ser un número, no un booleano."
            )

        # La duración debe ser entera o decimal.
        if not isinstance(duracion, (int, float)):
            raise TypeError(
                "La duración debe ser un valor numérico."
            )

        # Se rechazan valores infinitos o indefinidos.
        if not math.isfinite(duracion):
            raise ValueError(
                "La duración debe ser un número finito."
            )

        # La duración debe ser estrictamente positiva.
        if duracion <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        # Se devuelve la duración validada
        return duracion

    # Las propiedades permiten consultar los datos
    # almacenados sin modificarlos directamente
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

    # Este método permite modificar la duración
    # únicamente cuando la reserva está pendiente.
    def actualizar_duracion(self, nueva_duracion):

        # Se impiden cambios en reservas confirmadas
        # o canceladas para proteger su consistencia.
        if self.__estado != self.PENDIENTE:
            raise ValueError(
                "Solo se puede modificar una reserva pendiente."
            )

        # La nueva duración se valida antes de almacenarla.
        duracion_validada = self.validar_duracion(nueva_duracion)

        # El atributo se modifica después de la validación.
        self.__duracion = duracion_validada

        # Se devuelve un mensaje de confirmación.
        return "Duración actualizada correctamente."

    # Este método solicita al servicio el costo
    # correspondiente a las horas contratadas.
    def calcular_costo(self):

        # Las reservas canceladas no pueden calcular
        # nuevamente el costo de una contratación.
        if self.__estado == self.CANCELADA:
            raise ValueError(
                "No se puede calcular el costo de una reserva cancelada."
            )

        # Se invoca el comportamiento del servicio.
        # Cada clase concreta podrá aplicar una tarifa
        # y una fórmula de cálculo diferentes.
        costo = self.__servicio.calcular_costo(
            self.__duracion
        )

        # El resultado debe ser un número real.
        # Los valores booleanos se rechazan explícitamente.
        if isinstance(costo, bool) or not isinstance(
            costo, (int, float)
        ):
            raise TypeError(
                "El servicio debe devolver un costo numérico."
            )

        # Se impiden valores infinitos o indefinidos.
        if not math.isfinite(costo):
            raise ValueError(
                "El costo calculado debe ser finito."
            )

        # El costo no puede ser negativo.
        if costo < 0:
            raise ValueError(
                "El costo calculado no puede ser negativo."
            )

        # Se devuelve el resultado sin cambiar el estado.
        return costo

    # Este método confirma una reserva pendiente.
    def confirmar_reserva(self):

        # Se verifica que la transición de estado
        # esté permitida antes de procesar el costo.
        if self.__estado != self.PENDIENTE:
            raise ValueError(
                "Solo se pueden confirmar reservas pendientes."
            )

        # El costo se calcula y valida previamente.
        # Si se genera una excepción, el estado
        # permanece pendiente y sin modificaciones
        costo_validado = self.calcular_costo()

        # El costo se almacena cuando es válido
        self.__costo_total = costo_validado

        # El estado cambia después del cálculo exitoso
        self.__estado = self.CONFIRMADA

        # Se informa el resultado de la operación
        return "Reserva confirmada correctamente."

    # Este método permite cancelar reservas pendientes
    # o confirmadas, pero impide repetir la cancelación
    def cancelar_reserva(self):

        # Se rechaza la cancelación de una reserva
        # que ya se encuentra cancelada
        if self.__estado == self.CANCELADA:
            raise ValueError(
                "La reserva ya se encuentra cancelada."
            )

        # Se actualiza el estado de la reserva.
        self.__estado = self.CANCELADA

        # Se devuelve un mensaje de confirmación.
        return "Reserva cancelada correctamente."

    # Este método coordina el procesamiento de una reserva.
    # Reutiliza las reglas de confirmación para evitar
    # duplicación de código y validaciones.
    def procesar_reserva(self):

        # La operación se delega al método que valida
        # el estado y calcula el costo correspondiente.
        return self.confirmar_reserva()

    # Este método implementa la operación abstracta
    # mostrar_informacion heredada de Entidad.
    def mostrar_informacion(self):

        # Se consulta el nombre del servicio cuando existe
        # En caso contrario, se utiliza el nombre de la clase
        nombre_servicio = getattr(
            self.__servicio,
            "nombre",
            type(self.__servicio).__name__
        )

        # El costo se presenta como pendiente cuando
        # todavía no se ha confirmado la reserva.
        if self.__costo_total is None:
            costo_texto = "Pendiente de cálculo"
        else:
            costo_texto = f"{self.__costo_total:,.2f}"

        # Se construye una descripción organizada
        # de los datos principales de la reserva
        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {nombre_servicio}\n"
            f"Duración: {self.__duracion} horas\n"
            f"Estado: {self.__estado}\n"
            f"Costo total: {costo_texto}"
        )
