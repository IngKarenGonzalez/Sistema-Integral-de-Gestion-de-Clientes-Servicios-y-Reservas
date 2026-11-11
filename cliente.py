
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: cliente.py
# RESPONSABLE: Isabella Pineda Rodríguez
# ============================================================

# La clase Entidad se importa desde el archivo entidad.py
# Esta importación permite reutilizar el identificado
# encapsulado y el contrato del método mostrar_informacion.
from entidad import Entidad

# El módulo re proporciona herramientas para verificar
# patrones de texto mediante expresiones regulares
# En este caso, se utiliza para validar el formato del correo.
import re


# La clase Cliente hereda de Entidad y representa a los
# clientes que solicitan servicios dentro de Software FJ.
# Su responsabilidad es almacenar información de contacto
# y garantizar que los datos cumplan las validaciones.
class Cliente(Entidad):

    # El constructor recibe los datos necesarios para
    # registrar un nuevo cliente dentro del sistema.
    #
    # identificador: código que distingue al cliente.
    # nombre: nombre completo del cliente.
    # correo: dirección electrónica de contacto.
    # telefono: número telefónico de contacto.
    def __init__(self, identificador, nombre, correo, telefono):

        # super() permite ejecutar el constructor de Entidad.
        # De esta manera, el identificador se valida y
        # almacena mediante el mecanismo de la clase base.
        super().__init__(identificador)

        # Los atributos privados almacenan únicamente
        # valores que han superado las validaciones.
        # Los métodos estáticos verifican cada dato antes
        # de permitir su incorporación al objeto
        self.__nombre = self.validar_nombre(nombre)
        self.__correo = self.validar_correo(correo)
        self.__telefono = self.validar_telefono(telefono)

    # staticmethod permite utilizar este método sin depender
    # de los atributos de una instancia particular
    # Su finalidad es validar y normalizar nombres completos.
    @staticmethod
    def validar_nombre(nombre):

        # isinstance comprueba que el nombre sea un texto
        # Si el dato pertenece a otro tipo, se genera TypeError
        if not isinstance(nombre, str):
            raise TypeError(
                "El nombre debe ser una cadena de texto."
            )

        # split separa el texto en palabras y join las une
        # con un solo espacio, eliminando espacios sobrantes.
        nombre = " ".join(nombre.split())

        # Esta condición impide registrar nombres vacíos.
        if not nombre:
            raise ValueError(
                "El nombre del cliente no puede estar vacío."
            )

        # Se exige una longitud mínima de dos caracteres
        # para evitar registros evidentemente incompletos.
        if len(nombre) < 2:
            raise ValueError(
                "El nombre debe contener al menos dos caracteres."
            )

        # El valor validado se devuelve al constructor.
        return nombre

    # Este método estático verifica que el correo electrónico
    # corresponda a un formato básico de dirección válida.
    @staticmethod
    def validar_correo(correo):

        # La validación de tipo evita aplicar operaciones
        # de texto sobre valores incompatibles.
        if not isinstance(correo, str):
            raise TypeError(
                "El correo electrónico debe ser un texto."
            )

        # strip elimina espacios exteriores y lower convierte
        # los caracteres a minúsculas para normalizar el dato.
        correo = correo.strip().lower()

        # La condición impide almacenar correos vacíos.
        if not correo:
            raise ValueError(
                "El correo electrónico no puede estar vacío."
            )

        # La expresión regular comprueba una estructura
        # básica compuesta por usuario, arroba y dominio.
        # fullmatch exige que todo el texto cumpla el patrón.
        patron = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        # Si el correo no coincide con el patrón establecido,
        # se genera ValueError para informar el problema.
        if re.fullmatch(patron, correo) is None:
            raise ValueError(
                "El correo electrónico tiene un formato inválido."
            )

        # El correo normalizado se devuelve al constructor.
        return correo

    # Este método comprueba que el número telefónico
    # contenga únicamente dígitos y tenga una longitud
    # razonable para un dato de contacto.
    @staticmethod
    def validar_telefono(telefono):

        # El teléfono debe recibirse como cadena de texto.
        # Este criterio permite conservar ceros iniciales.
        if not isinstance(telefono, str):
            raise TypeError(
                "El teléfono debe proporcionarse como texto."
            )

        # strip elimina los espacios exteriores.
        telefono = telefono.strip()

        
        # La expresión regular verifica que el teléfono
        # contenga exclusivamente dígitos del 0 al 9.
        # fullmatch exige que toda la cadena cumpla el patrón.
        if re.fullmatch(r"[0-9]+", telefono) is None:
            raise ValueError(
                "El teléfono debe contener únicamente números."
            )

        # La longitud permitida se establece entre
        # 7 y 15 dígitos para admitir diferentes formatos
        # de contacto sin imponer un único país.
        if not 7 <= len(telefono) <= 15:
            raise ValueError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        # El teléfono validado se devuelve al constructor.
        return telefono

    # La propiedad nombre permite consultar el dato
    # sin acceder directamente al atributo privado.
    @property
    def nombre(self):
        return self.__nombre

    # La propiedad correo permite consultar la dirección
    # electrónica almacenada en el objeto.
    @property
    def correo(self):
        return self.__correo

    # La propiedad telefono permite consultar el número
    # de contacto previamente validado.
    @property
    def telefono(self):
        return self.__telefono

    
    # Este método permite modificar el nombre de un cliente
    # sin alterar su identificador ni sus datos de contacto.
    # La actualización utiliza las mismas validaciones
    # establecidas durante la creación del objeto.
    def actualizar_nombre(self, nuevo_nombre):

        # El nuevo nombre se valida antes de modificar
        # el atributo privado, evitando almacenar datos
        # vacíos o incompatibles con el tipo esperado.
        nombre_validado = self.validar_nombre(nuevo_nombre)

        # El atributo se actualiza únicamente después
        # de superar satisfactoriamente la validación.
        self.__nombre = nombre_validado

        # El método devuelve un mensaje de confirmación.
        return "Nombre actualizado correctamente."

    # Este método permite modificar el correo electrónico
    # de un cliente existente.
    # La actualización solo se realiza si el nuevo valor
    # supera las mismas validaciones del constructor.
    def actualizar_correo(self, nuevo_correo):

        # El nuevo correo se valida antes de reemplazar
        # el valor almacenado en el atributo privado.
        self.__correo = self.validar_correo(nuevo_correo)

        # El método devuelve un mensaje de confirmación.
        return "Correo electrónico actualizado correctamente."

    # Este método permite actualizar el número telefónico
    # sin modificar los demás datos del cliente
    def actualizar_telefono(self, nuevo_telefono):

        # La validación impide reemplazar el teléfono actual
        # por un valor que no cumpla los requisitos
        self.__telefono = self.validar_telefono(nuevo_telefono)

        # Se devuelve un mensaje que confirma la operación.
        return "Teléfono actualizado correctamente."

    # Este método implementa el comportamiento abstracto
    # mostrar_informacion definido originalmente en Entidad
    # Su finalidad es presentar los datos del cliente
    # mediante una cadena de texto organizada
    def mostrar_informacion(self):

        # La expresión f-string permite insertar los
        # atributos del objeto dentro de una cadena.
        # Los saltos de línea organizan la presentación.
        return (
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )
