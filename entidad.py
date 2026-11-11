
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: entidad.py
# RESPONSABLE: Isabella Pineda Rodríguez
# ============================================================

# La biblioteca abc proporciona las herramientas necesarias
# para definir clases abstractas en Python
# ABC permite establecer una clase base abstracta, mientras
# que abstractmethod identifica los métodos que deben ser
# implementados obligatoriamente por las clases derivadas
from abc import ABC, abstractmethod


# La clase Entidad representa una estructura abstracta general
# para los diferentes elementos que conforman el sistema.
# La herencia de ABC permite definir comportamientos comunes
# sin permitir la creación directa de objetos de esta clase
# mientras existan métodos abstractos sin implementar
class Entidad(ABC):

    # El método constructor inicializa los atributos comunes
    # de cada entidad mediante un identificador.
    # El parámetro identificador representa el código único
    # utilizado para distinguir una entidad dentro del sistema.
    def __init__(self, identificador):

        # La función isinstance verifica que el identificador
        # proporcionado corresponda al tipo de dato str
        # Si el valor pertenece a otro tipo de dato, se genera
        # una excepción TypeError mediante la instrucción raise
        if not isinstance(identificador, str):
            raise TypeError(
                "El identificador debe ser una cadena de texto."
            )

        # El método strip elimina los espacios en blanco
        # ubicados al inicio y al final del identificador
        identificador = identificador.strip()

        # Esta condición comprueba que el identificador
        # contenga caracteres después de eliminar los espacios.
        # Si la cadena está vacía, se genera una excepción
        # ValueError para impedir el almacenamiento de datos
        # que no cumplen con los requisitos establecidos
        if not identificador:
            raise ValueError(
                "El identificador no puede estar vacío."
            )

        # El identificador validado se almacena mediante
        # un atributo con doble guion bajo
        # Esta convención activa el mecanismo name mangling,
        # que dificulta el acceso directo accidental al atributo
        # desde el exterior de la clase
        self.__identificador = identificador

    # El decorador property permite consultar el identificador
    # mediante una propiedad de solo lectura
    # Este mecanismo facilita el acceso controlado al dato
    # sin exponer directamente el atributo encapsulado.
    @property
    def identificador(self):

        # La instrucción return devuelve el identificador
        # previamente validado y almacenado en el objeto.
        return self.__identificador

    # El decorador abstractmethod establece que el método
    # mostrar_informacion debe ser implementado por cada
    # clase derivada concreta
    # Su finalidad es garantizar que las entidades del sistema
    # dispongan de un mecanismo para presentar su información.
    @abstractmethod
    def mostrar_informacion(self):

        # La instrucción pass funciona como marcador de posición.
        # La implementación específica del método corresponde
        # a las clases derivadas que hereden de Entidad.
        pass
