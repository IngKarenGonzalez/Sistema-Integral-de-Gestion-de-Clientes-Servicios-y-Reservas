
# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACION (213023)
# FASE 4: PRACTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ============================================================
#
# DESCRIPCION GENERAL:
#
# Este archivo constituye el punto de entrada principal del
# Sistema Integral Software FJ, desarrollado mediante el
# paradigma de programacion orientada a objetos (POO).
#
# Su finalidad es integrar los modulos encargados de:
#
# - Gestionar la informacion de los clientes.
# - Representar los servicios disponibles.
# - Crear, confirmar y administrar reservas.
# - Calcular costos, descuentos e impuestos.
# - Validar datos y controlar operaciones incorrectas.
# - Gestionar excepciones y registrar eventos del sistema.
# - Ejecutar pruebas unitarias de funcionamiento.
#
# El proyecto utiliza una arquitectura modular, de manera que
# cada archivo Python contiene responsabilidades especificas.
#
# Este modulo permite dos modalidades de ejecucion:
#
# 1. Ejecucion normal:
#    python software_FJ.py
#
# 2. Ejecucion de pruebas unitarias:
#    python software_FJ.py --test
#
# ============================================================


# ============================================================
# 1. IMPORTACION DE LIBRERIAS Y MODULOS DEL PROYECTO
# ============================================================

# unittest es una biblioteca estandar de Python que permite
# crear pruebas automatizadas y verificar resultados esperados.
import unittest

# sys permite consultar los argumentos proporcionados al
# ejecutar el programa desde la terminal.
import sys


# ------------------------------------------------------------
# IMPORTACION DE CLASES DEL SISTEMA
# ------------------------------------------------------------

# Entidad es la clase base del modelo de objetos del proyecto.
# Su importacion permite identificar la estructura general
# de herencia utilizada por los modulos del sistema.
from entidad import Entidad

# Cliente representa a los usuarios que solicitan servicios
# y realizan reservas dentro del sistema.
from cliente import Cliente

# Reserva administra la relacion entre un cliente, un
# servicio y la duracion solicitada. Tambien controla
# los estados y costos de cada reserva.
from reserva import Reserva

# Se importan la clase abstracta Servicio y sus tres
# implementaciones concretas.
#
# Esta organizacion permite aplicar los principios de
# abstraccion, herencia y polimorfismo.
from servicios import (
    Servicio,
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas,
)


# ------------------------------------------------------------
# IMPORTACION DE HERRAMIENTAS DE EXCEPCIONES Y LOGS
# ------------------------------------------------------------

# registrar_log permite guardar informacion sobre los
# acontecimientos relevantes durante la ejecucion.
#
# Los registros facilitan el seguimiento del sistema
# y la identificacion de posibles errores.
from logger import registrar_log

# SoftwareFJError representa una excepcion personalizada
# utilizada para identificar errores propios del proyecto.
#
# Su uso permite diferenciar los problemas del sistema
# de las excepciones generales de Python.
from excepciones import SoftwareFJError


# ============================================================
# 2. CLASES AUXILIARES PARA LAS PRUEBAS UNITARIAS
# ============================================================
#
# Las siguientes clases simulan servicios con comportamientos
# controlados para comprobar las validaciones de Reserva.
#
# No reemplazan las clases reales de servicios.py.
# Se utilizan exclusivamente como apoyo para las pruebas.
# ============================================================


class ServicioTemporal:
    """
    Representa un servicio ficticio con una tarifa por hora.

    Esta clase permite comprobar que la clase Reserva
    calcula correctamente el costo de una operacion
    cuando recibe un servicio valido.

    Attributes:
        nombre (str):
            Nombre descriptivo del servicio de prueba.

        tarifa_hora (int o float):
            Valor monetario correspondiente a una hora.
    """

    def __init__(self, tarifa_hora=45000):
        """
        Inicializa el servicio ficticio.

        Args:
            tarifa_hora (int o float):
                Tarifa utilizada en los calculos.
                Su valor predeterminado es 45000.
        """

        # Nombre utilizado para identificar el servicio.
        self.nombre = "Reserva de sala"

        # Tarifa que se multiplicara por la duracion.
        self.tarifa_hora = tarifa_hora

    def calcular_costo(self, duracion):
        """
        Calcula el costo del servicio segun su duracion.

        Args:
            duracion (int o float):
                Cantidad de horas solicitadas.

        Returns:
            int o float:
                Resultado de multiplicar la tarifa
                por la duracion indicada.
        """

        # Formula: costo = tarifa por hora * horas.
        return self.tarifa_hora * duracion


class ServicioCostoInvalido:
    """
    Simula un servicio que devuelve un costo incorrecto.

    Se utiliza para comprobar que Reserva detecta
    resultados no permitidos, como costos negativos
    o valores que no son numericos.

    Attributes:
        nombre (str):
            Nombre descriptivo del servicio.

        resultado:
            Valor que devolvera calcular_costo().
    """

    def __init__(self, resultado):
        """
        Configura el resultado que utilizara la prueba.

        Args:
            resultado:
                Valor de costo que se desea evaluar.
        """

        self.nombre = "Servicio de prueba"

        # Se conserva el valor recibido para devolverlo
        # posteriormente sin realizar modificaciones.
        self.resultado = resultado

    def calcular_costo(self, duracion):
        """
        Devuelve el resultado configurado previamente.

        Args:
            duracion:
                Parametro recibido para mantener una
                interfaz compatible con otros servicios.

        Returns:
            El valor almacenado en self.resultado.

        Nota:
            La duracion no interviene en el calculo
            porque esta clase simula respuestas incorrectas.
        """

        return self.resultado


# ============================================================
# 3. PRUEBAS UNITARIAS DEL SISTEMA
# ============================================================
#
# Las pruebas unitarias permiten verificar el comportamiento
# de las clases ante entradas validas e invalidas.
#
# Se utiliza unittest.TestCase para comprobar:
#
# - Estados iniciales de las reservas.
# - Confirmacion y calculo de costos.
# - Validacion de duraciones.
# - Validacion de servicios.
# - Prevencion de costos incorrectos.
# - Restricciones segun el estado de una reserva.
# - Actualizacion y validacion de datos del cliente.
#
# Cada metodo cuyo nombre comienza con "test_" constituye
# una prueba que unittest puede ejecutar automaticamente.
# ============================================================


class PruebasSoftwareFJ(unittest.TestCase):
    """
    Agrupa las pruebas unitarias del Sistema Integral FJ.

    Hereda de unittest.TestCase para utilizar metodos
    de verificacion como assertEqual, assertIsNone
    y assertRaises.

    Las pruebas se ejecutan de forma independiente
    mediante los objetos creados en setUp().
    """

    def setUp(self):
        """
        Prepara los objetos necesarios para cada prueba.

        unittest ejecuta este metodo antes de cada test,
        lo que permite trabajar con datos iniciales
        independientes y evitar interferencias.
        """

        # Cliente ficticio utilizado como referencia.
        self.cliente = Cliente(
            "FJ-CLI-005",
            "Julieta Salazar",
            "julieta.salazar@example.com",
            "3105550105"
        )

        # Servicio auxiliar con tarifa de 45000 por hora.
        self.servicio = ServicioTemporal()

    def crear_reserva(self, duracion=2, servicio=None):
        """
        Construye una reserva de prueba.

        Args:
            duracion (int o float):
                Duracion solicitada. Por defecto, 2 horas.

            servicio:
                Servicio que se asociara a la reserva.
                Si no se proporciona, se utiliza
                el servicio auxiliar de setUp().

        Returns:
            Reserva:
                Objeto de reserva creado para la prueba.
        """

        # Se utiliza el servicio predeterminado cuando
        # no se proporciona otro servicio.
        if servicio is None:
            servicio = self.servicio

        # Se construye una reserva con identificador,
        # cliente, servicio y duracion.
        return Reserva(
            "FJ-RES-005",
            self.cliente,
            servicio,
            duracion
        )

    # --------------------------------------------------------
    # PRUEBA 01: ESTADO INICIAL DE UNA RESERVA
    # --------------------------------------------------------

    def test_reserva_inicia_pendiente(self):
        """
        Verifica que una reserva nueva comience pendiente
        y que todavia no tenga un costo total confirmado.
        """

        reserva = self.crear_reserva()

        # La reserva debe iniciar en estado PENDIENTE.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

        # El costo total debe permanecer sin asignar.
        self.assertIsNone(reserva.costo_total)

    # --------------------------------------------------------
    # PRUEBA 02: CONFIRMACION Y CALCULO DEL COSTO
    # --------------------------------------------------------

    def test_confirmacion_calcula_costo(self):
        """
        Comprueba que confirmar una reserva actualice
        su estado y almacene el costo correspondiente.
        """

        reserva = self.crear_reserva()

        # Se confirma una reserva inicialmente pendiente.
        reserva.confirmar_reserva()

        # Se comprueba el cambio de estado.
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)

        # Dos horas a 45000 producen un costo de 90000.
        self.assertEqual(reserva.costo_total, 90000)

    # --------------------------------------------------------
    # PRUEBA 03: DURACIONES DECIMALES
    # --------------------------------------------------------

    def test_duracion_decimal(self):
        """
        Verifica que el sistema admita duraciones
        decimales positivas y calcule su costo.
        """

        reserva = self.crear_reserva(1.5)

        # 45000 * 1.5 = 67500.
        self.assertEqual(reserva.calcular_costo(), 67500)

    # --------------------------------------------------------
    # PRUEBA 04: DURACION IGUAL A CERO
    # --------------------------------------------------------

    def test_duracion_cero(self):
        """
        Comprueba que no se permita crear una reserva
        cuya duracion sea igual a cero.
        """

        # Se espera ValueError porque cero no representa
        # una duracion valida para una reserva.
        with self.assertRaises(ValueError):
            self.crear_reserva(0)

    # --------------------------------------------------------
    # PRUEBA 05: DURACION BOOLEANA
    # --------------------------------------------------------

    def test_duracion_booleana(self):
        """
        Comprueba que un valor booleano no sea aceptado
        como duracion de una reserva.
        """

        # Aunque bool se relaciona con int en Python,
        # el sistema debe rechazar True como duracion.
        with self.assertRaises(TypeError):
            self.crear_reserva(True)

    # --------------------------------------------------------
    # PRUEBA 06: DURACION INFINITA
    # --------------------------------------------------------

    def test_duracion_infinita(self):
        """
        Verifica que una duracion infinita sea rechazada
        para evitar operaciones numericas incorrectas.
        """

        # float("inf") representa infinito positivo.
        with self.assertRaises(ValueError):
            self.crear_reserva(float("inf"))

    # --------------------------------------------------------
    # PRUEBA 07: SERVICIO SIN METODO DE COSTO
    # --------------------------------------------------------

    def test_servicio_sin_metodo(self):
        """
        Comprueba que una reserva rechace un objeto
        que no tenga el comportamiento requerido
        para calcular el costo del servicio.
        """

        # object() no proporciona calcular_costo().
        with self.assertRaises(TypeError):
            self.crear_reserva(servicio=object())

    # --------------------------------------------------------
    # PRUEBA 08: COSTO NEGATIVO
    # --------------------------------------------------------

    def test_costo_negativo(self):
        """
        Comprueba que no se confirme una reserva cuando
        el servicio devuelve un costo negativo.

        Tambien verifica que la operacion fallida
        no modifique el estado ni el costo almacenado.
        """

        # Se crea un servicio que devuelve -100.
        servicio = ServicioCostoInvalido(-100)

        reserva = self.crear_reserva(servicio=servicio)

        # El costo negativo debe generar ValueError.
        with self.assertRaises(ValueError):
            reserva.confirmar_reserva()

        # La reserva debe permanecer pendiente.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

        # No debe almacenarse un costo incorrecto.
        self.assertIsNone(reserva.costo_total)

    # --------------------------------------------------------
    # PRUEBA 09: COSTO NO NUMERICO
    # --------------------------------------------------------

    def test_costo_no_numerico(self):
        """
        Verifica que un costo expresado como texto
        sea rechazado durante la confirmacion.

        La reserva debe conservar su estado pendiente.
        """

        # Se simula un servicio que devuelve texto.
        servicio = ServicioCostoInvalido("No disponible")

        reserva = self.crear_reserva(servicio=servicio)

        # Se espera TypeError por el tipo incorrecto.
        with self.assertRaises(TypeError):
            reserva.confirmar_reserva()

        # La operacion fallida no debe confirmar la reserva.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

    # --------------------------------------------------------
    # PRUEBA 10: ACTUALIZACION DE DURACION
    # --------------------------------------------------------

    def test_actualizar_duracion_pendiente(self):
        """
        Comprueba que una reserva pendiente permita
        modificar su duracion y recalcular el costo.
        """

        reserva = self.crear_reserva()

        # Se cambia la duracion inicial de 2 a 3 horas.
        reserva.actualizar_duracion(3)

        # Se verifica que el nuevo valor fue almacenado.
        self.assertEqual(reserva.duracion, 3)

        # 45000 * 3 = 135000.
        self.assertEqual(reserva.calcular_costo(), 135000)

    # --------------------------------------------------------
    # PRUEBA 11: RESTRICCION SOBRE RESERVAS CONFIRMADAS
    # --------------------------------------------------------

    def test_no_modificar_reserva_confirmada(self):
        """
        Verifica que una reserva confirmada no permita
        modificar posteriormente su duracion.
        """

        reserva = self.crear_reserva()

        # Primero se confirma la reserva.
        reserva.confirmar_reserva()

        # La modificacion debe generar ValueError.
        with self.assertRaises(ValueError):
            reserva.actualizar_duracion(4)

        # La duracion original debe mantenerse.
        self.assertEqual(reserva.duracion, 2)

    # --------------------------------------------------------
    # PRUEBA 12: RESTRICCION SOBRE RESERVAS CANCELADAS
    # --------------------------------------------------------

    def test_no_confirmar_reserva_cancelada(self):
        """
        Comprueba que una reserva cancelada no pueda
        procesarse nuevamente como una reserva valida.
        """

        reserva = self.crear_reserva()

        # Se cancela la reserva antes de procesarla.
        reserva.cancelar_reserva()

        # Se espera ValueError al intentar procesarla.
        with self.assertRaises(ValueError):
            reserva.procesar_reserva()

        # La reserva debe continuar cancelada.
        self.assertEqual(reserva.estado, Reserva.CANCELADA)

    # --------------------------------------------------------
    # PRUEBA 13: ACTUALIZACION DEL NOMBRE DEL CLIENTE
    # --------------------------------------------------------

    def test_actualizar_nombre_cliente(self):
        """
        Verifica que un cliente permita actualizar
        su nombre cuando recibe un valor valido.
        """

        # Se solicita la actualizacion del nombre.
        self.cliente.actualizar_nombre("Julieta Mendoza")

        # Se verifica que el cambio se haya realizado.
        self.assertEqual(
            self.cliente.nombre,
            "Julieta Mendoza"
        )

    # --------------------------------------------------------
    # PRUEBA 14: CONSERVACION DEL NOMBRE ANTE UN ERROR
    # --------------------------------------------------------

    def test_nombre_invalido_conserva_dato(self):
        """
        Comprueba que un intento de actualizacion
        con un nombre compuesto solo por espacios
        no altere la informacion existente.
        """

        # Se conserva el nombre antes de la operacion.
        nombre_original = self.cliente.nombre

        # Una cadena sin contenido significativo
        # debe provocar una excepcion ValueError.
        with self.assertRaises(ValueError):
            self.cliente.actualizar_nombre("   ")

        # El nombre debe conservar su valor original.
        self.assertEqual(
            self.cliente.nombre,
            nombre_original
        )
    
    # --------------------------------------------------------
    # PRUEBA 15: CANCELACION DE UNA RESERVA CONFIRMADA
    # --------------------------------------------------------

    def test_cancelar_reserva_confirmada_limpia_costo(self):
        """
        Verifica que una reserva previamente confirmada
        pueda cancelarse correctamente.

        Esta prueba comprueba que:
        1. La reserva inicia en estado PENDIENTE.
        2. La confirmacion calcula y almacena su costo.
        3. La cancelacion cambia el estado a CANCELADA.
        4. El costo total se limpia y vuelve a ser None.

        Esta validacion evita conservar valores asociados
        a reservas que ya no se encuentran activas.
        """

        # Se crea una reserva valida de dos horas.
        reserva = self.crear_reserva(duracion=2)

        # Se confirma y se verifica el costo calculado.
        reserva.confirmar_reserva()

        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)
        self.assertEqual(reserva.costo_total, 90000)

        # Se cancela la reserva previamente confirmada.
        reserva.cancelar_reserva()

        # El estado debe cambiar a CANCELADA.
        self.assertEqual(reserva.estado, Reserva.CANCELADA)

        # El costo no debe conservarse despues de cancelar.
        self.assertIsNone(reserva.costo_total)


# ============================================================
# 4. PROGRAMA PRINCIPAL DE INTEGRACION
# ============================================================
#
# Esta funcion demuestra el funcionamiento conjunto
# de los diferentes componentes del sistema.
#
# La secuencia general consiste en:
#
# 1. Presentar el encabezado del programa.
# 2. Registrar el inicio de la ejecucion.
# 3. Crear un cliente valido.
# 4. Instanciar tres servicios especializados.
# 5. Calcular costos, descuentos e impuestos.
# 6. Crear reservas asociadas al cliente.
# 7. Confirmar las reservas.
# 8. Registrar los eventos correspondientes.
# 9. Controlar posibles excepciones.
# 10. Registrar la finalizacion del proceso.
#
# La estructura try/except/else/finally permite
# organizar el manejo de errores y la finalizacion.
# ============================================================


def ejecutar_sistema():
    """
    Ejecuta una demostracion integrada del Software FJ.

    Integra los modulos de clientes, servicios, reservas,
    excepciones personalizadas y registro de eventos.

    El procedimiento utiliza objetos de ejemplo para
    mostrar las principales operaciones del sistema.

    Las excepciones previstas se gestionan mediante
    bloques try/except y los eventos se registran
    utilizando la funcion registrar_log().
    """

    # --------------------------------------------------------
    # 4.1. PRESENTACION DEL SISTEMA
    # --------------------------------------------------------

    # Se muestra un encabezado para identificar el programa
    # y la institucion a la que pertenece el proyecto.
    print("=" * 60)
    print("SISTEMA INTEGRAL SOFTWARE FJ")
    print("UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD")
    print("=" * 60)

    # Se registra el inicio de la ejecucion.
    # INFO identifica un acontecimiento informativo.
    registrar_log(
        "Inicio de la ejecucion del Sistema Integral Software FJ.",
        "INFO"
    )

    # --------------------------------------------------------
    # 4.2. BLOQUE PRINCIPAL DE OPERACIONES
    # --------------------------------------------------------

    # try contiene las operaciones que pueden generar
    # excepciones durante la ejecucion del sistema.
    try:

        # ----------------------------------------------------
        # 4.2.1. CREACION DEL CLIENTE
        # ----------------------------------------------------

        # Se instancia un cliente con los datos requeridos:
        # identificador, nombre, correo electronico y telefono.
        cliente = Cliente(
            "C001",
            "Maria Perez",
            "maria@gmail.com",
            "3001234567"
        )

        # Se presenta la informacion del cliente mediante
        # el metodo definido en la clase correspondiente.
        print("\nINFORMACION DEL CLIENTE")
        print(cliente.mostrar_informacion())

        # Se deja evidencia de la creacion del cliente.
        registrar_log(
            "Cliente creado correctamente.",
            "INFO"
        )

        # ----------------------------------------------------
        # 4.2.2. CREACION DE LOS SERVICIOS
        # ----------------------------------------------------

        # Se crean objetos de las tres clases especializadas.
        #
        # Estas clases representan diferentes modalidades
        # de servicio y comparten una interfaz de calculo
        # definida por su estructura de herencia.

        # Servicio de reserva de salas.
        # Se especifican identificador, nombre, capacidad
        # y ubicacion.
        sala = ReservaSalas(
            "S001",
            "Sala de reuniones",
            20,
            "Piso 2"
        )

        # Servicio de alquiler de equipos.
        # Se especifican identificador, nombre,
        # tipo de equipo y cantidad.
        equipos = AlquilerEquipos(
            "E001",
            "Alquiler de computadores",
            "Computadores",
            2
        )

        # Servicio de asesorias especializadas.
        # Se especifican identificador, nombre,
        # especialidad y profesional responsable.
        asesoria = AsesoriasEspecializadas(
            "A001",
            "Asesoria de software",
            "Desarrollo de software",
            "Carlos Ramirez"
        )

        # Los tres objetos se almacenan en una lista.
        #
        # Esto permite recorrerlos con un mismo ciclo
        # y ejecutar operaciones comunes.
        servicios = [sala, equipos, asesoria]

        # Se registra que los tres servicios fueron creados.
        registrar_log(
            "Se crearon correctamente los tres servicios.",
            "INFO"
        )

        # ----------------------------------------------------
        # 4.2.3. CALCULO DE COSTOS, DESCUENTOS E IMPUESTOS
        # ----------------------------------------------------

        # Se presenta un encabezado para identificar
        # las operaciones de calculo.
        print("\n")
        print("=" * 60)
        print("PRUEBAS DE DESCUENTOS E IMPUESTOS")
        print("=" * 60)

        # Se recorre la lista de servicios.
        #
        # POLIMORFISMO:
        # Cada objeto implementa calcular_costo()
        # segun las caracteristicas de su clase.
        #
        # El programa utiliza el mismo nombre de metodo
        # sin necesidad de comprobar manualmente el tipo
        # concreto de cada servicio.
        for servicio in servicios:

            # Se presenta el nombre del servicio.
            print(f"\nServicio: {servicio.nombre}")

            # Se consulta la tarifa por hora definida
            # en la clase correspondiente.
            #
            # El formato :,.0f presenta el valor
            # con separadores de miles y sin decimales.
            print(
                "Tarifa original:",
                f"${servicio.TARIFA_POR_HORA:,.0f}"
            )

            # CASO 1: COSTO NORMAL.
            #
            # Se calcula el costo correspondiente
            # a dos horas sin descuento ni impuesto.
            print(
                "Costo normal:",
                f"${servicio.calcular_costo(2):,.2f}"
            )

            # CASO 2: COSTO CON DESCUENTO.
            #
            # Se aplica un descuento del 10%
            # al costo correspondiente a dos horas.
            print(
                "Con descuento del 10%:",
                f"${servicio.calcular_costo(2, descuento=10):,.2f}"
            )

            # CASO 3: DESCUENTO E IMPUESTO.
            #
            # Se calcula el costo aplicando un descuento
            # del 10% y un impuesto del 19%.
            #
            # La implementacion del calculo se encuentra
            # en el modulo servicios.py.
            print(
                "Con descuento e impuesto:",
                f"${servicio.calcular_costo(2, descuento=10, impuesto=19):,.2f}"
            )

            # Se registra la finalizacion de los calculos
            # correspondientes al servicio procesado.
            registrar_log(
                f"Calculos de costos completados para el servicio: {servicio.nombre}",
                "INFO"
            )

        # ----------------------------------------------------
        # 4.2.4. CREACION DE LAS RESERVAS
        # ----------------------------------------------------

        # Se crean tres reservas asociadas al mismo cliente.
        #
        # Cada reserva tiene:
        # - Un identificador unico dentro del ejemplo.
        # - Una referencia al cliente.
        # - Una referencia al servicio solicitado.
        # - Una duracion expresada en horas.

        # Reserva de sala durante 1.5 horas.
        reserva1 = Reserva("R001", cliente, sala, 1.5)

        # Reserva de equipos durante 1.5 horas.
        reserva2 = Reserva("R002", cliente, equipos, 1.5)

        # Reserva de asesoria durante 1.25 horas.
        reserva3 = Reserva("R003", cliente, asesoria, 1.25)

        # Se agrupan las reservas para procesarlas
        # de forma secuencial.
        reservas = [reserva1, reserva2, reserva3]

        # Se registra la creacion de las tres reservas.
        registrar_log(
            "Se crearon correctamente las tres reservas.",
            "INFO"
        )

        # ----------------------------------------------------
        # 4.2.5. CONFIRMACION DE LAS RESERVAS
        # ----------------------------------------------------

        # Se presenta el encabezado de esta etapa.
        print("\n")
        print("=" * 60)
        print("CONFIRMACION DE RESERVAS")
        print("=" * 60)

        # Se recorre la lista para confirmar cada reserva.
        for reserva in reservas:

            # confirmar_reserva() realiza la operacion
            # de confirmacion y devuelve un mensaje.
            #
            # La clase Reserva es responsable de validar
            # las condiciones de la operacion y actualizar
            # el estado y el costo cuando corresponde.
            print("\n" + reserva.confirmar_reserva())

            # Se muestra la informacion actualizada
            # de la reserva procesada.
            print(reserva.mostrar_informacion())

            # Separador visual entre reservas.
            print("-" * 60)

            # Se registra la confirmacion realizada.
            registrar_log(
                "Reserva confirmada correctamente.",
                "INFO"
            )

        # Este mensaje se muestra si el flujo principal
        # llega hasta el final de las operaciones.
        print("\nSistema ejecutado correctamente.")

    # --------------------------------------------------------
    # 4.3. MANEJO DE EXCEPCIONES
    # --------------------------------------------------------

    # except captura las excepciones indicadas:
    #
    # TypeError:
    #   Problemas relacionados con tipos de datos.
    #
    # ValueError:
    #   Valores incorrectos para una operacion.
    #
    # SoftwareFJError:
    #   Excepciones personalizadas del proyecto.
    #
    # El objetivo es presentar un mensaje comprensible
    # y registrar el error detectado.
    except (TypeError, ValueError, SoftwareFJError) as error:

        # Se informa al usuario sobre el problema.
        print("\nERROR EN EL SISTEMA:", error)

        # ERROR identifica un evento que requiere
        # atencion por parte del sistema.
        registrar_log(
            f"Error durante la ejecucion del sistema: {error}",
            "ERROR"
        )

    # --------------------------------------------------------
    # 4.4. EJECUCION SIN EXCEPCIONES
    # --------------------------------------------------------

    # else se ejecuta cuando el bloque try termina
    # sin producir una excepcion.
    #
    # Esto permite registrar el resultado satisfactorio
    # de las operaciones principales.
    else:

        registrar_log(
            "Sistema ejecutado correctamente.",
            "INFO"
        )

    # --------------------------------------------------------
    # 4.5. FINALIZACION DEL PROCESO
    # --------------------------------------------------------

    # finally se ejecuta al finalizar la estructura
    # try/except/else, tanto si se produjo una excepcion
    # como si las operaciones terminaron normalmente.
    #
    # Se utiliza para dejar constancia de la finalizacion
    # del proceso en el registro de eventos.
    finally:

        registrar_log(
            "Finalizo el proceso de ejecucion del sistema.",
            "INFO"
        )


# ============================================================
# 5. PUNTO DE ENTRADA Y MODALIDADES DE EJECUCION
# ============================================================
#
# Python asigna el valor "__main__" a la variable __name__
# cuando un archivo se ejecuta directamente.
#
# Esta condicion permite diferenciar la ejecucion directa
# de la importacion del archivo desde otro modulo.
#
# El programa admite dos modalidades:
#
# A. Pruebas unitarias:
#    python software_FJ.py --test
#
# B. Demostracion del sistema:
#    python software_FJ.py
#
# De esta manera, el mismo archivo sirve para ejecutar
# el programa y verificar automaticamente sus funciones.
# ============================================================


if __name__ == "__main__":

    # Se comprueba si el usuario proporciono el argumento
    # "--test" al ejecutar el archivo.
    if "--test" in sys.argv:

        # unittest.main() descubre y ejecuta los metodos
        # de prueba definidos en PruebasSoftwareFJ.
        #
        # argv=[sys.argv[0]]:
        # Evita que unittest interprete "--test"
        # como un argumento propio.
        #
        # verbosity=2:
        # Presenta informacion detallada sobre
        # el resultado individual de cada prueba.
        unittest.main(
            argv=[sys.argv[0]],
            verbosity=2
        )

    else:

        # Cuando no se proporciona "--test",
        # se ejecuta la demostracion principal.
        ejecutar_sistema()
