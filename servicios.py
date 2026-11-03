# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: PROGRAMACIÓN (213023)
# Fase 4: PRÁCTICAS SIMULADAS
# Trabajo: SISTEMA INTEGRAL SOFTWARE FJ
# Nombre del producto: servicios.py
# Autora: María Paula Marín Tolosa

# Importo la información de los programas de mi compañera Isabella, para generar la integración

from entidad import Entidad
from abc import abstractmethod

#Creo la clase base para los 3 tipos de servicios, donde la clase hereda de Entidad para recibir sus características.
#Además es una clase abstracta ya que sirve como estructura de las clases hijas estableciendo lo que todas implementan (el método de calcular costo)

class Servicio(Entidad):
# Inicializo el servicio recibiendo un identificador y un nombre. Con super().__init__(identificador) llamo al constructor de Entidad para validar y almacenar el identificador heredado.
    def __init__(self, identificador, nombre):
        super().__init__(identificador)

        if not isinstance(nombre, str): #Comprueba que el nombre sea texto
            raise TypeError("El nombre del servicio debe ser texto.") #Genera un error en caso de que el nombre no sea texto

        nombre = nombre.strip()#Elimina los espacios al inicio y al final

#Comprueba que el espacio de nombre no quede vacio y en caso de que este genera el error correspondiente
        if not nombre:
            raise ValueError("El nombre del servicio no puede estar vacío")

        self.__nombre = nombre

#Esto me permite al programa consultar el nombre del servicio desde fuera de la clase sin acceder directamente al atributo privado de __nombre
    @property
    def nombre(self):
        return self.__nombre
#Este metodo permite centralizar las validaciones necesarias antes de calcular el costo de cualquier servicio, comprobando la duración (debe ser mayor de 0), el descuento (entre 0 y 100), Y que el impuesto sea un número positivo
    def _validar_parametros_calculo(self, duracion, descuento, impuesto):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise TypeError("La duración debe ser un número.")

        if duracion <=0:
            raise ValueError("La duración debe ser mayor que cero")

        if not isinstance(descuento, (int, float)) or isinstance(descuento, bool):
            raise TypeError("El descuento debe ser un número.")

        if not 0 <= descuento <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")

        if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool):
            raise TypeError("El impuesto debe ser un número.")

        if impuesto < 0:
            raise ValueError("El impuesto no puede ser negativo.")
        
#Establezco que el metodo abstractmethod se implementara en todas las clases hijas con sus parametros correspondientes antes explicadas
#Aplico el polimorfismo al implementar el mismo método heredado con comportamientos diferentes según el tipo de servicio
# Y tambien aplico la sobrecarga mediante parámetros predeterminados que permiten llamar al método con diferentes cantidades de argumentos
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass
#creo la primera clase especializada que hereda de servicio, por lo cual tiene sus caracteristicas e implementa los métodos abstractos establecidos por esta clase base
class ReservaSalas(Servicio):
    TARIFA_POR_HORA = 50000
#Inicializo una reserva de sala con sus datos particulares y los datos heredados de servicio, donde el constructor recibe datos de identificación, nombre, capacidad y ubicación
    def __init__(self, identificador, nombre, capacidad, ubicacion):
        super().__init__(identificador, nombre)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool):
            raise TypeError("La capacidad debe ser un número entero.")

        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        if not isinstance(ubicacion, str):
            raise TypeError("La ubicación debe ser texto.")

        ubicacion = ubicacion.strip()

        if not ubicacion:
            raise ValueError("La ubicación no puede estar vacía.")

        self.__capacidad = capacidad
        self.__ubicacion = ubicacion

    @property
    def capacidad(self):
        return self.__capacidad

    @property
    def ubicacion(self):
        return self.__ubicacion

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self._validar_parametros_calculo(duracion, descuento, impuesto)

        subtotal = self.TARIFA_POR_HORA*duracion
        subtotal -= subtotal*(descuento/100)

        return subtotal + subtotal * (impuesto/100)
#Muestro la información del servicio, capacidad, ubicación y tarifa correspondiente
    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Reserva de salas\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Ubicación: {self.ubicacion}\n"
            f"Tarifa por hora: ${self.TARIFA_POR_HORA:,.0f}"
        )
#Inicializo la clase de alquiler de equipos que recibe sus datos particulares y heredados de la clase base servicio, mediante su super().__init__
class AlquilerEquipos(Servicio):
    TARIFA_POR_HORA = 35000

    def __init__(self, identificador, nombre, tipo_equipo, cantidad):
        super().__init__(identificador, nombre)
#Verifico que el tipo de equipo recibido sea un texto
        if not isinstance(tipo_equipo, str):
            raise TypeError("El tipo de equipo debe ser texto.")

        tipo_equipo = tipo_equipo.strip()

        if not tipo_equipo:
            raise ValueError("El tipo de equipo no puede estar vacío.")

        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
#Almaceno el tipo de equipo y la cantidad mediante atributos privados para aplicar el encapsulamiento
        self.__tipo_equipo = tipo_equipo
        self.__cantidad = cantidad

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @property
    def cantidad(self):
        return self.__cantidad

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self._validar_parametros_calculo(duracion, descuento, impuesto)

        subtotal = self.TARIFA_POR_HORA * duracion * self.cantidad
        subtotal -= subtotal * (descuento / 100)

        return subtotal + subtotal * (impuesto/100)

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Alquiler de equipos\n"
            f"Equipo: {self.tipo_equipo}\n"
            f"Cantidad: {self.cantidad}\n"
            f"Tarifa por hora y equipo: ${self.TARIFA_POR_HORA:,.0f}"
        )

#Inicializo una asesoría especializada recibiendo sus datos particulares y los datos heredados de Servicio mediante super().__init__
class AsesoriasEspecializadas(Servicio):
    TARIFA_POR_HORA = 80000

    def __init__(self, identificador, nombre, especialidad, asesor):
        super().__init__(identificador, nombre)

        if not isinstance(especialidad, str):
            raise TypeError("La especialidad debe ser texto.")

        especialidad = especialidad.strip()

        if not especialidad:
            raise ValueError("La especialidad no puede estar vacía.")

        if not isinstance(asesor, str):
            raise TypeError("El nombre del asesor debe ser texto.")

        asesor = asesor.strip()

        if not asesor:
            raise ValueError("El nombre del asesor no puede estar vacío.")

        self.__especialidad = especialidad
        self.__asesor = asesor

    @property
    def especialidad(self):
        return self.__especialidad

    @property
    def asesor(self):
        return self.__asesor

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self._validar_parametros_calculo(duracion, descuento, impuesto)

        subtotal = self.TARIFA_POR_HORA * duracion
        subtotal -= subtotal * (descuento / 100)

        return subtotal + subtotal * (impuesto / 100)

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Asesoría especializada\n"
            f"Especialidad: {self.especialidad}\n"
            f"Asesor: {self.asesor}\n"
            f"Tarifa por hora: ${self.TARIFA_POR_HORA:,.0f}"
        )