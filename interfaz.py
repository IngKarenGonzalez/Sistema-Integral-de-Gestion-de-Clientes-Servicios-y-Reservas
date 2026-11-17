# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4: PRÁCTICAS SIMULADAS
# PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
# ARCHIVO: INTERFAZ GRÁFICA TKINTER
# DESARROLLO ORIGINAL: MARÍA PAULA (INTERFAZ)
# AJUSTES COLABORATIVOS: ESTADOS, VALIDACIONES Y LOGS
# ============================================================

# Tkinter permite construir la ventana y sus elementos visuales.
import tkinter as tk
# ttk incorpora listas desplegables y barras de desplazamiento.
from tkinter import ttk, messagebox
# math permite rechazar números infinitos o NaN en los formularios.
import math

# Importar las clases existentes para reutilizar las reglas de negocio.
from cliente import Cliente
from reserva import Reserva
from servicios import ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas
# Importar las excepciones personalizadas del proyecto.
from excepciones import SoftwareFJError, ServicioNoDisponibleError, ReservaError
# Reutilizar la función de logging ya configurada por el equipo.
from logger import registrar_log


# Esta clase coordina la interfaz sin reemplazar la lógica de los módulos.
class InterfazSoftwareFJ:
    """Interfaz en inglés para administrar clientes y reservas de Software FJ."""

    def __init__(self, ventana):
        """Configura la ventana principal, las estructuras y los botones."""
        # Guardar la ventana que administra Tkinter.
        self.ventana = ventana
        # Configurar título, dimensiones y color de fondo originales.
        self.ventana.title("Software FJ - Reservation Management")
        self.ventana.geometry("1100x750")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#F0F2F5")

        # Guardar temporalmente los clientes y las reservas en memoria.
        self.clientes = []
        self.reservas = []
        # Relacionar los servicios con sus identificadores.
        self.servicios = {}
        # Conservar descuentos, impuestos y resúmenes de costos.
        self.datos_costos = {}
        # Relacionar cada reserva con la etiqueta de su tarjeta izquierda.
        self.elementos_reservas = {}
        # Indicar qué reserva se visualiza actualmente.
        self.reserva_seleccionada = None

        # Construir los dos paneles y su mensaje inicial.
        self.crear_interfaz()
        self.mostrar_mensaje_inicial()

        # Crear el botón que abre el formulario de reservas nuevas.
        self.boton_nueva_reserva = tk.Button(
            self.panel_izquierdo,
            text="ADD NEW RESERVATION", font=("Arial", 10),
            bg="#B888B0", fg="white", activebackground="#A4779B",
            relief="flat", cursor="hand2", command=self.nueva_reserva
        )
        # Ubicarlo debajo de la lista, conservando el estilo original.
        self.boton_nueva_reserva.pack(side="bottom", fill="x", pady=10)

        # Crear el botón de confirmación, inicialmente deshabilitado.
        self.boton_confirmar = tk.Button(
            self.panel_derecho.master,
            text="CONFIRM", font=("Arial", 10),
            bg="#B888B0", fg="white", activebackground="#A4779B",
            relief="flat", cursor="hand2", state="disabled",
            command=self.confirmar_reserva
        )
        # Conservar la ubicación inferior utilizada por Pau.
        self.boton_confirmar.place(relx=0.60, rely=0.92,
                                   anchor="center", width=110)

        # Crear el botón para cancelar una reserva existente.
        self.boton_cancelar = tk.Button(
            self.panel_derecho.master,
            text="CANCEL", font=("Arial", 10),
            bg="#B888B0", fg="white", activebackground="#A4779B",
            relief="flat", cursor="hand2", state="disabled",
            command=self.cancelar_reserva
        )
        # Ubicar el botón junto al de confirmación.
        self.boton_cancelar.place(relx=0.71, rely=0.92,
                                  anchor="center", width=110)

    def crear_interfaz(self):
        """Construye la cabecera y los paneles principales de la aplicación."""
        # Mostrar el nombre del proyecto en la franja superior.
        titulo = tk.Label(
            self.ventana, text="SOFTWARE FJ", font=("Arial", 24, "bold"),
            bg="#B888B0", fg="white", pady=18
        )
        titulo.pack(fill="x")

        # Mostrar un subtítulo en inglés debajo del nombre.
        subtitulo = tk.Label(
            self.ventana, text="RESERVATION MANAGEMENT SYSTEM",
            font=("Arial", 10), bg="#B888B0", fg="#DCE6F1", pady=5
        )
        subtitulo.pack(fill="x")

        # Agrupar los paneles en un contenedor central.
        contenedor = tk.Frame(self.ventana, bg="#F0F2F5")
        contenedor.pack(fill="both", expand=True, padx=20, pady=20)

        # El panel izquierdo contiene las tarjetas de las reservas.
        self.panel_izquierdo = tk.LabelFrame(
            contenedor, text="Reservations", font=("Arial", 12, "bold"),
            bg="white", fg="#B888B0", padx=10, pady=10, width=350
        )
        self.panel_izquierdo.pack(side="left", fill="both",
                                  padx=(0, 10), pady=(0, 100))
        # Respetar el ancho establecido para la lista.
        self.panel_izquierdo.pack_propagate(False)

        # Crear el área donde se insertarán las tarjetas individuales.
        self.lista_reservas = tk.Frame(self.panel_izquierdo, bg="white")
        self.lista_reservas.pack(fill="both", expand=True, pady=10)

        # El panel derecho muestra el formulario o los detalles de la reserva.
        self.panel_derecho = tk.LabelFrame(
            contenedor, text="Reservation Details",
            font=("Arial", 12, "bold"), bg="white", fg="#B888B0",
            padx=15, pady=15
        )
        self.panel_derecho.pack(side="right", fill="both", expand=True,
                                pady=(0, 100))

    def mostrar_mensaje_inicial(self):
        """Indica que todavía no hay una reserva seleccionada."""
        # Crear una etiqueta descriptiva en el centro del panel derecho.
        self.mensaje_inicial = tk.Label(
            self.panel_derecho, text="No reservation selected",
            font=("Arial", 14), bg="white", fg="#555555"
        )
        self.mensaje_inicial.pack(expand=True)

    def estado_en_ingles(self, reserva):
        """Obtiene una descripción en inglés del estado real de Reserva."""
        # Mantener la traducción de los tres estados del modelo.
        estados = {
            Reserva.PENDIENTE: "PENDING",
            Reserva.CONFIRMADA: "CONFIRMED",
            Reserva.CANCELADA: "CANCELLED"
        }
        # Usar el estado actual; no conservar un texto fijo desactualizado.
        return estados.get(reserva.estado, str(reserva.estado))

    def actualizar_tarjeta_reserva(self, reserva):
        """Sincroniza la tarjeta izquierda con el estado real de la reserva."""
        # Recuperar la etiqueta guardada al crear la tarjeta.
        etiqueta = self.elementos_reservas.get(reserva.identificador)
        # No hacer nada si la tarjeta todavía no existe.
        if etiqueta is None:
            return
        # Preparar el texto de acuerdo con los datos reales del objeto.
        texto = (
            f"{reserva.identificador}\n"
            f"{reserva.cliente.nombre}\n"
            f"{reserva.servicio.nombre}\n"
            f"Status: {self.estado_en_ingles(reserva)}"
        )
        # Reemplazar el texto visible, sin crear una segunda tarjeta.
        etiqueta.config(text=texto)

    def ocultar_botones_formulario(self):
        """Elimina botones temporales que ya no corresponden a la vista."""
        # Los botones del formulario viven fuera del panel de detalles.
        for nombre in ("boton_guardar", "boton_cancelar_formulario"):
            # Consultar si el botón fue creado en una visita anterior.
            boton = getattr(self, nombre, None)
            # Eliminarlo solo si aún existe en Tkinter.
            if boton is not None and boton.winfo_exists():
                boton.destroy()
            # Restablecer la referencia para evitar reutilizarlo.
            setattr(self, nombre, None)

    def seleccionar_reserva(self, reserva):
        """Muestra el detalle actualizado de la reserva seleccionada."""
        # El objeto seleccionado es la fuente real del estado.
        self.reserva_seleccionada = reserva
        # Quitar los botones de formulario de creación, si existen.
        self.ocultar_botones_formulario()
        # Mantener la lista de campos que se muestran bloqueados.
        self.campos_detalle = []

        # Borrar la vista anterior antes de reconstruir los detalles.
        for widget in self.panel_derecho.winfo_children():
            widget.destroy()

        # Crear un contenedor que admite desplazamiento vertical.
        contenedor_formulario = tk.Frame(self.panel_derecho, bg="white")
        contenedor_formulario.pack(fill="both", expand=True,
                                   padx=5, pady=5)
        # Canvas permite desplazarse por campos y resumen de costos.
        canvas = tk.Canvas(contenedor_formulario, bg="white",
                           highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        # Vincular una barra de desplazamiento a la vista del canvas.
        barra = ttk.Scrollbar(contenedor_formulario, orient="vertical",
                              command=canvas.yview)
        barra.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=barra.set)

        # El formulario interior alojará los cuadros de información.
        formulario = tk.Frame(canvas, bg="white")
        ventana_formulario = canvas.create_window((0, 0),
                                                  window=formulario,
                                                  anchor="nw")

        # Recalcular el desplazamiento cuando cambie el contenido.
        def actualizar_area(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Ajustar el ancho de la sección interior al canvas.
        def ajustar_ancho(event):
            canvas.itemconfig(ventana_formulario, width=event.width)

        # Conectar ambos cambios de tamaño a Tkinter.
        formulario.bind("<Configure>", actualizar_area)
        canvas.bind("<Configure>", ajustar_ancho)

        # Crear una pareja etiqueta/campo de solo lectura.
        def agregar_campo(contenedor, etiqueta, valor, fila, columna):
            # Mostrar el nombre del dato en inglés.
            tk.Label(contenedor, text=etiqueta, font=("Arial", 9),
                     bg="white").grid(row=fila, column=columna * 2,
                                        sticky="w", padx=5, pady=7)
            # Utilizar color verde suave si la reserva está confirmada.
            color = ("#E8F5E9" if reserva.estado == Reserva.CONFIRMADA
                     else "#F0F2F5")
            # Los campos están bloqueados para prevenir cambios directos.
            campo = tk.Entry(contenedor, width=25, font=("Arial", 9),
                             disabledbackground=color,
                             disabledforeground="#333333")
            campo.grid(row=fila, column=columna * 2 + 1, padx=5, pady=7)
            campo.insert(0, str(valor))
            campo.config(state="disabled")
            self.campos_detalle.append(campo)

        # Encabezado de la vista de detalles.
        tk.Label(formulario, text="Reservation Information",
                 font=("Arial", 16, "bold"), bg="white",
                 fg="#B888B0").pack(anchor="w", pady=(5, 12))

        # Mostrar información del cliente asociado a la reserva.
        datos_cliente = tk.LabelFrame(
            formulario, text="Client Information",
            font=("Arial", 10, "bold"), bg="white", padx=10, pady=5
        )
        datos_cliente.pack(fill="x", pady=5)
        agregar_campo(datos_cliente, "Client ID", reserva.cliente.identificador, 0, 0)
        agregar_campo(datos_cliente, "Full Name", reserva.cliente.nombre, 0, 1)
        agregar_campo(datos_cliente, "Email", reserva.cliente.correo, 1, 0)
        agregar_campo(datos_cliente, "Phone", reserva.cliente.telefono, 1, 1)

        # Mostrar los valores básicos de la reserva seleccionada.
        datos_reserva = tk.LabelFrame(
            formulario, text="Reservation Details",
            font=("Arial", 10, "bold"), bg="white", padx=10, pady=5
        )
        datos_reserva.pack(fill="x", pady=5)
        agregar_campo(datos_reserva, "Reservation ID", reserva.identificador, 0, 0)
        agregar_campo(datos_reserva, "Service Type", reserva.servicio.nombre, 0, 1)
        agregar_campo(datos_reserva, "Duration (hours)", reserva.duracion, 1, 0)
        # Traducir el valor real del estado para el panel derecho.
        agregar_campo(datos_reserva, "Status", self.estado_en_ingles(reserva), 1, 1)

        # Describir las propiedades específicas del servicio elegido.
        datos_servicio = tk.LabelFrame(
            formulario, text="Specific Service Information",
            font=("Arial", 10, "bold"), bg="white", padx=10, pady=5
        )
        datos_servicio.pack(fill="x", pady=5)
        servicio = reserva.servicio

        # Las salas muestran capacidad y ubicación.
        if isinstance(servicio, ReservaSalas):
            agregar_campo(datos_servicio, "Capacity", servicio.capacidad, 0, 0)
            agregar_campo(datos_servicio, "Location", servicio.ubicacion, 0, 1)
        # Los equipos muestran tipo y cantidad solicitada.
        elif isinstance(servicio, AlquilerEquipos):
            agregar_campo(datos_servicio, "Equipment Type", servicio.tipo_equipo, 0, 0)
            agregar_campo(datos_servicio, "Quantity", servicio.cantidad, 0, 1)
        # Las asesorías muestran especialidad y asesor.
        elif isinstance(servicio, AsesoriasEspecializadas):
            agregar_campo(datos_servicio, "Specialty", servicio.especialidad, 0, 0)
            agregar_campo(datos_servicio, "Advisor", servicio.asesor, 0, 1)

        # Mostrar los costos únicamente si la reserva está confirmada.
        costos = self.datos_costos.get(reserva.identificador, {})
        claves_costos = {"subtotal", "descuento", "valor_descuento",
                        "impuesto", "valor_impuesto", "total"}
        if (reserva.estado == Reserva.CONFIRMADA
                and claves_costos.issubset(costos)):
            # Crear el recuadro con el desglose calculado.
            resumen = tk.LabelFrame(formulario, text="Cost Summary",
                                     font=("Arial", 10, "bold"),
                                     bg="white", padx=10, pady=5)
            resumen.pack(fill="x", pady=8)
            # Presentar el precio base sin impuestos ni descuentos.
            tk.Label(resumen, text=f"Subtotal: ${costos['subtotal']:,.2f}",
                     font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
            # Presentar el descuento elegido para la reserva.
            tk.Label(resumen,
                     text=(f"Discount ({costos['descuento']}%): "
                           f"-${costos['valor_descuento']:,.2f}"),
                     font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
            # Mostrar el impuesto aplicado al valor descontado.
            tk.Label(resumen,
                     text=(f"Tax ({costos['impuesto']}%): "
                           f"${costos['valor_impuesto']:,.2f}"),
                     font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
            # Destacar el total final en color verde.
            tk.Label(resumen, text=f"TOTAL: ${costos['total']:,.2f}",
                     font=("Arial", 12, "bold"), fg="#2E7D32",
                     bg="white").pack(anchor="w", pady=5)

        # Habilitar los botones según las reglas del estado actual.
        if reserva.estado == Reserva.PENDIENTE:
            # Una reserva pendiente puede confirmarse o cancelarse.
            self.boton_confirmar.config(state="normal")
            self.boton_cancelar.config(state="normal")
        elif reserva.estado == Reserva.CONFIRMADA:
            # Una reserva confirmada solo puede cancelarse.
            self.boton_confirmar.config(state="disabled")
            self.boton_cancelar.config(state="normal")
        else:
            # Una reserva cancelada no admite nuevas acciones.
            self.boton_confirmar.config(state="disabled")
            self.boton_cancelar.config(state="disabled")

        # Asegurar que los botones se vean en la vista de detalles.
        self.boton_confirmar.place(relx=0.60, rely=0.92,
                                   anchor="center", width=110)
        self.boton_cancelar.place(relx=0.71, rely=0.92,
                                  anchor="center", width=110)

    def confirmar_reserva(self):
        """Confirma una reserva, registra el resultado y actualiza ambos paneles."""
        # No operar si todavía no se seleccionó una reserva.
        if self.reserva_seleccionada is None:
            return
        # Conservar la referencia al mismo objeto usado por ambos paneles.
        reserva = self.reserva_seleccionada
        try:
            # Recuperar la configuración de descuento e impuesto.
            identificador = reserva.identificador
            descuento = self.datos_costos[identificador]["descuento"]
            impuesto = self.datos_costos[identificador]["impuesto"]

            # Calcular el subtotal sin descuentos ni impuestos.
            subtotal = reserva.servicio.calcular_costo(reserva.duracion, 0, 0)
            # Calcular el ahorro que corresponde al descuento.
            valor_descuento = subtotal * (descuento / 100)
            # Restar el descuento del subtotal.
            subtotal_descuento = subtotal - valor_descuento
            # Calcular el impuesto sobre el subtotal descontado.
            valor_impuesto = subtotal_descuento * (impuesto / 100)
            # Obtener el total a partir del método del servicio.
            total = reserva.servicio.calcular_costo(
                reserva.duracion, descuento, impuesto
            )

            # Cambiar el estado de la reserva mediante su método original.
            reserva.confirmar_reserva()
            # Guardar el desglose para mostrarlo en el panel de detalles.
            self.datos_costos[identificador] = {
                "descuento": descuento,
                "impuesto": impuesto,
                "subtotal": subtotal,
                "valor_descuento": valor_descuento,
                "valor_impuesto": valor_impuesto,
                "total": total
            }
            # Conservar el registro de costos en la consola como apoyo.
            print("COST SUMMARY:", self.datos_costos[identificador])
            # Registrar la confirmación exitosa en el sistema de logs.
            registrar_log(f"Reservation {identificador} confirmed successfully.")

            # CORRECCIÓN: actualizar la tarjeta que antes decía PENDING.
            self.actualizar_tarjeta_reserva(reserva)
            # Reconstruir los detalles con el estado CONFIRMED y los costos.
            self.seleccionar_reserva(reserva)
            # Informar en inglés que la operación fue satisfactoria.
            messagebox.showinfo(
                "Reservation Confirmed",
                "The reservation has been confirmed successfully."
            )
        except (SoftwareFJError, ValueError, TypeError,
                ArithmeticError, KeyError) as error:
            # Registrar el mensaje original para conservar la trazabilidad.
            registrar_log(f"Error confirming reservation: {error}", "ERROR")
            # Mostrar un mensaje traducido sin cerrar la ventana.
            messagebox.showerror("Confirmation Error",
                                 self.traducir_error(str(error)))

    def cancelar_reserva(self):
        """Cancela una reserva y actualiza las tarjetas y los detalles."""
        # Cancelar la acción si no hay una reserva seleccionada.
        if self.reserva_seleccionada is None:
            return
        reserva = self.reserva_seleccionada
        # Solicitar confirmación antes de ejecutar un cambio irreversible.
        respuesta = messagebox.askyesno(
            "Cancel Reservation",
            "Are you sure you want to cancel this reservation?"
        )
        # Respetar la respuesta negativa del usuario.
        if not respuesta:
            return
        try:
            # Cambiar el estado con la lógica de la clase Reserva.
            reserva.cancelar_reserva()
            # Registrar el resultado satisfactorio de cancelación.
            registrar_log(
                f"Reservation {reserva.identificador} cancelled successfully."
            )
            # CORRECCIÓN: mostrar CANCELLED en la tarjeta izquierda.
            self.actualizar_tarjeta_reserva(reserva)
            # Reconstruir el panel derecho con el nuevo estado.
            self.seleccionar_reserva(reserva)
            # Mostrar confirmación en inglés al usuario.
            messagebox.showinfo(
                "Reservation Cancelled",
                "The reservation has been cancelled successfully."
            )
        except (SoftwareFJError, ValueError, TypeError) as error:
            # CORRECCIÓN: registrar los errores que antes no se guardaban.
            registrar_log(f"Error cancelling reservation: {error}", "ERROR")
            # Mostrar el motivo en inglés y mantener la ventana abierta.
            messagebox.showerror("Cancellation Error",
                                 self.traducir_error(str(error)))

    def mostrar_formulario_reserva(self):
        """Construye el formulario para registrar un cliente y una reserva."""
        # Crear el contenedor principal de la nueva reserva.
        self.panel_formulario = tk.Frame(self.panel_derecho, bg="white")
        self.panel_formulario.pack(fill="both", expand=True)
        formulario = self.panel_formulario

        # Identificar claramente la operación que realizará el usuario.
        tk.Label(formulario, text="New Reservation",
                 font=("Arial", 16, "bold"), bg="white",
                 fg="#B888B0").pack(anchor="w", pady=(5, 15))

        # Grupo que contiene los datos del cliente.
        datos_cliente = tk.LabelFrame(
            formulario, text="Client Information",
            font=("Arial", 10, "bold"), bg="white", padx=10, pady=10
        )
        datos_cliente.pack(fill="x", pady=5)

        # Crear el campo de identificación del cliente.
        tk.Label(datos_cliente, text="Client ID", bg="white").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        self.campo_identificacion = tk.Entry(datos_cliente, width=25)
        self.campo_identificacion.grid(row=0, column=1, padx=5, pady=5)

        # Crear el campo del nombre completo.
        tk.Label(datos_cliente, text="Full Name", bg="white").grid(
            row=0, column=2, sticky="w", padx=5, pady=5)
        self.campo_nombre = tk.Entry(datos_cliente, width=25)
        self.campo_nombre.grid(row=0, column=3, padx=5, pady=5)

        # Crear el campo del correo electrónico.
        tk.Label(datos_cliente, text="Email", bg="white").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        self.campo_correo = tk.Entry(datos_cliente, width=25)
        self.campo_correo.grid(row=1, column=1, padx=5, pady=5)

        # Crear el campo del teléfono de contacto.
        tk.Label(datos_cliente, text="Phone", bg="white").grid(
            row=1, column=2, sticky="w", padx=5, pady=5)
        self.campo_telefono = tk.Entry(datos_cliente, width=25)
        self.campo_telefono.grid(row=1, column=3, padx=5, pady=5)

        # Agrupar los datos generales de la reserva.
        datos_reserva = tk.LabelFrame(
            formulario, text="Reservation Information",
            font=("Arial", 10, "bold"), bg="white", padx=10, pady=10
        )
        datos_reserva.pack(fill="x", pady=10)

        # Ofrecer los tres servicios desarrollados por el equipo.
        tk.Label(datos_reserva, text="Service Type", bg="white").grid(
            row=0, column=0, sticky="w", padx=5, pady=8)
        self.lista_servicios = ttk.Combobox(
            datos_reserva,
            values=["Room Reservation", "Equipment Rental",
                    "Specialized Consulting"],
            state="readonly", width=30
        )
        self.lista_servicios.grid(row=0, column=1, padx=5, pady=8)
        # Mostrar campos específicos cuando se selecciona el servicio.
        self.lista_servicios.bind("<<ComboboxSelected>>",
                                  self.mostrar_campos_servicio)

        # Pedir duración en horas para calcular el costo.
        tk.Label(datos_reserva, text="Duration (hours)", bg="white").grid(
            row=1, column=0, sticky="w", padx=5, pady=8)
        self.campo_duracion = tk.Entry(datos_reserva, width=15)
        self.campo_duracion.grid(row=1, column=1, sticky="w", padx=5, pady=8)

        # El descuento inicia en 0 %, pero puede modificarse.
        tk.Label(datos_reserva, text="Discount (%)", bg="white").grid(
            row=2, column=0, sticky="w", padx=5, pady=8)
        self.campo_descuento = tk.Entry(datos_reserva, width=15)
        self.campo_descuento.insert(0, "0")
        self.campo_descuento.grid(row=2, column=1, sticky="w", padx=5, pady=8)

        # Mantener el impuesto predeterminado de 19 %.
        tk.Label(datos_reserva, text="Tax (%)", bg="white").grid(
            row=3, column=0, sticky="w", padx=5, pady=8)
        self.campo_impuesto = tk.Entry(datos_reserva, width=15)
        self.campo_impuesto.insert(0, "19")
        self.campo_impuesto.grid(row=3, column=1, sticky="w", padx=5, pady=8)

    @staticmethod
    def convertir_decimal(texto, nombre_campo):
        """Convierte un campo decimal y describe específicamente sus errores."""
        # Impedir que un campo obligatorio se procese como un número vacío.
        if not texto:
            raise ValueError(f"{nombre_campo} is required.")
        # Convertir el texto proporcionado por los controles Tkinter.
        try:
            numero = float(texto)
        except (ValueError, TypeError) as error:
            # Conservar la causa original mediante encadenamiento de excepciones.
            raise ValueError(f"{nombre_campo} must be a valid number.") from error
        # NaN y los números infinitos no son datos válidos para los cálculos.
        if not math.isfinite(numero):
            raise ValueError(f"{nombre_campo} must be a finite number.")
        # Entregar el dato numérico ya validado al método que lo solicitó.
        return numero

    @staticmethod
    def convertir_entero(texto, nombre_campo):
        """Convierte capacidad o cantidad a entero con errores identificables."""
        # Distinguir los campos vacíos de los datos no numéricos.
        if not texto:
            raise ValueError(f"{nombre_campo} is required.")
        # Un número entero no debe contener letras ni cifras decimales.
        try:
            numero = int(texto)
        except (ValueError, TypeError) as error:
            # Informar el nombre del campo sin exponer el error técnico de Python.
            raise ValueError(f"{nombre_campo} must be a valid whole number.") from error
        # Devolver el entero para que su rango se compruebe más adelante.
        return numero

    
    def validar_datos_cliente(self):
        """
        Valida los datos ingresados para registrar un cliente.

        Comprueba que el nombre contenga letras y no números,
        reutiliza las validaciones originales de Cliente y
        registra cualquier error sin cerrar la interfaz.
        """

        # Obtener y limpiar la información del formulario.
        identificacion = self.campo_identificacion.get().strip()
        nombre = " ".join(self.campo_nombre.get().split())
        correo = self.campo_correo.get().strip()
        telefono = self.campo_telefono.get().strip()

        try:
            # Comprobar que el nombre no esté vacío.
            if not nombre:
                raise ValueError(
                    "Customer name is required."
                )

            # Exigir al menos dos letras en el nombre.
            cantidad_letras = sum(
                caracter.isalpha() for caracter in nombre
            )

            if cantidad_letras < 2:
                raise ValueError(
                    "Customer name must contain at least two letters."
                )

            # Admitir letras, espacios, guiones y apóstrofes.
            # Rechazar números y otros caracteres no permitidos.
            if not all(
                caracter.isalpha() or caracter in " -'’"
                for caracter in nombre
            ):
                raise ValueError(
                    "Customer name must contain only letters, "
                    "spaces, hyphens or apostrophes."
                )

            # Crear el cliente usando las clases originales.
            # Se conservan las validaciones de Entidad y Cliente.
            cliente = Cliente(
                identificacion,
                nombre,
                correo,
                telefono
            )

            # Registrar la validación exitosa.
            registrar_log(
                f"Customer validated successfully: "
                f"{cliente.identificador}",
                "INFO"
            )

            # Devolver el objeto validado.
            return cliente

        except (SoftwareFJError, TypeError, ValueError) as error:

            # Conservar el detalle del error en el log.
            registrar_log(
                f"Error validating customer data: {error}",
                "ERROR"
            )

            # Mostrar un mensaje específico en inglés.
            messagebox.showerror(
                "Client Information Error",
                self.traducir_error(str(error))
            )

            # Impedir que se guarde la reserva.
            return None

    def validar_datos_reserva(self):
        """Comprueba servicio y valores de duración, descuento e impuesto."""
        # Obtener los datos escritos y la opción seleccionada.
        servicio = self.lista_servicios.get().strip()
        duracion_texto = self.campo_duracion.get().strip()
        descuento_texto = self.campo_descuento.get().strip()
        impuesto_texto = self.campo_impuesto.get().strip()
        try:
            # Pedir al usuario que elija un servicio válido.
            if not servicio:
                raise ServicioNoDisponibleError("You must select a service.")
            disponibles = (
                "Room Reservation", "Equipment Rental", "Specialized Consulting"
            )
            if servicio not in disponibles:
                raise ServicioNoDisponibleError("The selected service is not available.")
            # Convertir los tres campos uno por uno; cada mensaje dirá cuál falló.
            duracion = self.convertir_decimal(duracion_texto, "Duration")
            descuento = self.convertir_decimal(descuento_texto, "Discount")
            impuesto = self.convertir_decimal(impuesto_texto, "Tax")
            # La duración de una reserva debe ser estrictamente positiva.
            if duracion <= 0:
                raise ValueError("Duration must be greater than zero.")
            # El descuento corresponde a un porcentaje entre 0 y 100.
            if not 0 <= descuento <= 100:
                raise ValueError("Discount must be between 0 and 100.")
            # Un impuesto negativo es incompatible con las reglas del sistema.
            if impuesto < 0:
                raise ValueError("Tax cannot be negative.")
            # Entregar la información verificada para crear el objeto Reserva.
            return servicio, duracion, descuento, impuesto
        except (SoftwareFJError, ValueError, TypeError) as error:
            # Registrar el error del campo en el archivo de logs del equipo.
            registrar_log(f"Reservation information error: {error}", "ERROR")
            # Mostrar una explicación concreta en inglés y mantener el formulario.
            messagebox.showerror(
                "Invalid Reservation Information",
                self.traducir_error(str(error))
            )
            return None

    def validar_datos_servicio(self, servicio):
        """Valida por separado los campos de cada servicio especializado."""
        try:
            # Para salas, comprobar primero la capacidad y luego la ubicación.
            if servicio == "Room Reservation":
                capacidad_texto = self.campo_capacidad.get().strip()
                ubicacion = self.campo_ubicacion.get().strip()
                capacidad = self.convertir_entero(capacidad_texto, "Capacity")
                if capacidad <= 0:
                    raise ValueError("Capacity must be greater than zero.")
                if not ubicacion:
                    raise ValueError("Location is required.")
                return capacidad, ubicacion
            # Para alquiler de equipos, comprobar tipo y cantidad por separado.
            elif servicio == "Equipment Rental":
                tipo_equipo = self.campo_tipo_equipo.get().strip()
                cantidad_texto = self.campo_cantidad.get().strip()
                if not tipo_equipo:
                    raise ValueError("Equipment type is required.")
                cantidad = self.convertir_entero(cantidad_texto, "Quantity")
                if cantidad <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                return tipo_equipo, cantidad
            # Para asesorías, no permitir especialidad ni asesor vacíos.
            elif servicio == "Specialized Consulting":
                especialidad = self.campo_especialidad.get().strip()
                asesor = self.campo_asesor.get().strip()
                if not especialidad:
                    raise ValueError("Specialty is required.")
                if not asesor:
                    raise ValueError("Advisor is required.")
                return especialidad, asesor
            # Rechazar cualquier tipo de servicio no ofrecido por el sistema.
            raise ServicioNoDisponibleError("The selected service is not available.")
        except (SoftwareFJError, ValueError, TypeError) as error:
            # Registrar el motivo para su revisión posterior en el log.
            registrar_log(f"Service information error: {error}", "ERROR")
            # Mostrar el error correspondiente y conservar la interfaz abierta.
            messagebox.showerror(
                "Service Information Error",
                self.traducir_error(str(error))
            )
            return None

    def mostrar_campos_servicio(self, event=None):
        """Muestra los campos específicos del servicio seleccionado."""
        # Quitar los campos del servicio anteriormente elegido, si existen.
        if hasattr(self, "panel_campos_servicio"):
            self.panel_campos_servicio.destroy()
        # Crear un marco para los nuevos campos del servicio.
        self.panel_campos_servicio = tk.LabelFrame(
            self.panel_formulario, text="Specific Service Information",
            font=("Arial", 10, "bold"), bg="white", padx=10, pady=10
        )
        self.panel_campos_servicio.pack(fill="x", pady=10)
        # Consultar el servicio que eligió el usuario.
        servicio = self.lista_servicios.get()

        # Para salas, permitir capacidad y piso/ubicación.
        if servicio == "Room Reservation":
            tk.Label(self.panel_campos_servicio, text="Capacity", bg="white").grid(
                row=0, column=0, sticky="w", padx=5, pady=5)
            self.campo_capacidad = tk.Entry(self.panel_campos_servicio, width=25)
            self.campo_capacidad.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(self.panel_campos_servicio, text="Location", bg="white").grid(
                row=0, column=2, sticky="w", padx=5, pady=5)
            self.campo_ubicacion = ttk.Combobox(
                self.panel_campos_servicio, values=["Floor 1", "Floor 2", "Floor 3"],
                state="readonly", width=10
            )
            self.campo_ubicacion.grid(row=0, column=3, padx=5, pady=5)

        # Para equipos, permitir tipo de dispositivo y cantidad.
        elif servicio == "Equipment Rental":
            tk.Label(self.panel_campos_servicio, text="Equipment Type",
                     bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.campo_tipo_equipo = ttk.Combobox(
                self.panel_campos_servicio,
                values=["Computers", "Projectors", "Tablets", "Laptops"],
                state="readonly", width=22
            )
            self.campo_tipo_equipo.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(self.panel_campos_servicio, text="Quantity", bg="white").grid(
                row=0, column=2, sticky="w", padx=5, pady=5)
            self.campo_cantidad = tk.Entry(self.panel_campos_servicio, width=10)
            self.campo_cantidad.grid(row=0, column=3, padx=5, pady=5)

        # Para asesorías, permitir elegir especialidad y asesor.
        elif servicio == "Specialized Consulting":
            tk.Label(self.panel_campos_servicio, text="Specialty", bg="white").grid(
                row=0, column=0, sticky="w", padx=5, pady=5)
            self.campo_especialidad = ttk.Combobox(
                self.panel_campos_servicio,
                values=["Software Engineering", "Programming", "Systems Analysis",
                        "Database Management"],
                state="readonly", width=25
            )
            self.campo_especialidad.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(self.panel_campos_servicio, text="Advisor", bg="white").grid(
                row=0, column=2, sticky="w", padx=5, pady=5)
            self.campo_asesor = ttk.Combobox(
                self.panel_campos_servicio,
                values=["Carlos Ramirez", "Laura Martinez", "Andres Gomez"],
                state="readonly", width=18
            )
            self.campo_asesor.grid(row=0, column=3, padx=5, pady=5)

    def nueva_reserva(self):
        """Abre un formulario nuevo y oculta acciones de reservas anteriores."""
        # Dejar de señalar una reserva seleccionada previamente.
        self.reserva_seleccionada = None
        # Eliminar el contenido actual del panel de detalles.
        for widget in self.panel_derecho.winfo_children():
            widget.destroy()
        # Retirar los botones temporales de formularios anteriores.
        self.ocultar_botones_formulario()
        # Ocultar las acciones de confirmar y cancelar reservas existentes.
        self.boton_confirmar.place_forget()
        self.boton_cancelar.place_forget()
        self.boton_confirmar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")
        # Construir los controles del nuevo formulario.
        self.mostrar_formulario_reserva()

        # Botón para validar y guardar la nueva reserva.
        self.boton_guardar = tk.Button(
            self.panel_derecho.master,
            text="SAVE", font=("Arial", 10), bg="#B888B0", fg="white",
            activebackground="#A4779B", relief="flat", cursor="hand2",
            command=self.guardar_reserva
        )
        self.boton_guardar.place(relx=0.60, rely=0.92,
                                 anchor="center", width=110)
        # Botón para descartar los datos sin guardar una reserva.
        self.boton_cancelar_formulario = tk.Button(
            self.panel_derecho.master,
            text="CANCEL", font=("Arial", 10), bg="#B888B0", fg="white",
            activebackground="#A4779B", relief="flat", cursor="hand2",
            command=self.cancelar_nueva_reserva
        )
        self.boton_cancelar_formulario.place(relx=0.71, rely=0.92,
                                             anchor="center", width=110)

    def cancelar_nueva_reserva(self):
        """Cierra el formulario nuevo y devuelve la vista inicial."""
        # Retirar el formulario y todos sus campos de entrada.
        for widget in self.panel_derecho.winfo_children():
            widget.destroy()
        # Eliminar los botones de SAVE y CANCEL del formulario nuevo.
        self.ocultar_botones_formulario()
        # Olvidar la reserva seleccionada antes de volver al inicio.
        self.reserva_seleccionada = None
        # Dejar visible el mensaje de selección inicial.
        self.mostrar_mensaje_inicial()
        # Los botones de reserva permanecen deshabilitados sin selección.
        self.boton_confirmar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")
        self.boton_confirmar.place(relx=0.60, rely=0.92,
                                   anchor="center", width=110)
        self.boton_cancelar.place(relx=0.71, rely=0.92,
                                  anchor="center", width=110)

    def guardar_reserva(self):
        """Crea los objetos y dibuja una tarjeta que puede actualizarse."""
        try:
            # Verificar los datos del cliente con la clase Cliente.
            cliente = self.validar_datos_cliente()
            if cliente is None:
                return
            # Verificar las condiciones generales de la reserva.
            datos_reserva = self.validar_datos_reserva()
            if datos_reserva is None:
                return
            tipo_servicio, duracion, descuento, impuesto = datos_reserva
            # Verificar las propiedades del servicio elegido.
            datos_servicio = self.validar_datos_servicio(tipo_servicio)
            if datos_servicio is None:
                return

            # Crear un identificador para el nuevo servicio.
            identificador_servicio = f"SRV-{len(self.servicios) + 1:03d}"
            # Construir la clase especializada que corresponda al tipo.
            if tipo_servicio == "Room Reservation":
                capacidad, ubicacion = datos_servicio
                servicio = ReservaSalas(
                    identificador_servicio, "Room Reservation", capacidad, ubicacion
                )
            elif tipo_servicio == "Equipment Rental":
                tipo_equipo, cantidad = datos_servicio
                servicio = AlquilerEquipos(
                    identificador_servicio, "Equipment Rental", tipo_equipo, cantidad
                )
            elif tipo_servicio == "Specialized Consulting":
                especialidad, asesor = datos_servicio
                servicio = AsesoriasEspecializadas(
                    identificador_servicio, "Specialized Consulting",
                    especialidad, asesor
                )
            else:
                raise ServicioNoDisponibleError("The selected service is not available.")

            # Construir el identificador incremental de la nueva reserva.
            identificador_reserva = f"FJ-RES-{len(self.reservas) + 1:03d}"
            # Crear el objeto que administrará su propio estado.
            reserva = Reserva(identificador_reserva, cliente, servicio, duracion)
            # Conservar parámetros que se utilizarán al confirmar.
            self.datos_costos[reserva.identificador] = {
                "descuento": descuento,
                "impuesto": impuesto
            }
            # Guardar las referencias de clientes, servicios y reservas.
            self.clientes.append(cliente)
            self.servicios[identificador_servicio] = servicio
            self.reservas.append(reserva)

            # Crear la tarjeta con el diseño original de Pau.
            elemento_reserva = tk.Label(
                self.lista_reservas, text="", font=("Arial", 10),
                bg="#F0F2F5", fg="#333333", justify="left",
                anchor="w", padx=10, pady=10, cursor="hand2"
            )
            # Hacer que un clic seleccione este mismo objeto Reserva.
            elemento_reserva.bind(
                "<Button-1>",
                lambda event, reserva=reserva: self.seleccionar_reserva(reserva)
            )
            # Insertar la tarjeta en la lista del panel izquierdo.
            elemento_reserva.pack(fill="x", pady=5)
            # CORRECCIÓN: guardar la etiqueta para futuras actualizaciones.
            self.elementos_reservas[reserva.identificador] = elemento_reserva
            # Mostrar PENDING usando el estado del objeto, no un texto fijo.
            self.actualizar_tarjeta_reserva(reserva)

            # Registrar la creación de la reserva en el archivo de logs.
            registrar_log(
                f"Reservation {identificador_reserva} created successfully."
            )
            # Informar el resultado de la creación mediante una ventana.
            messagebox.showinfo("Success", "The reservation was created successfully.")
            # Cerrar el formulario y volver al panel inicial.
            self.cancelar_nueva_reserva()
        except (SoftwareFJError, ValueError, TypeError, ArithmeticError) as error:
            # Registrar el error original para su análisis.
            registrar_log(f"Reservation creation error: {error}", "ERROR")
            # Comunicar en inglés el error y permitir corregir los datos.
            messagebox.showerror("Reservation Error",
                                 self.traducir_error(str(error)))

    def traducir_error(self, mensaje):
        """Traduce errores conocidos; otros se muestran de forma general."""
        # Mantener los mensajes internos originales de las clases del equipo.
        traducciones = {
            # Validaciones de identificadores en Entidad.
            "El identificador debe ser una cadena de texto.": "Identifier must be a text string.",
            "El identificador no puede estar vacío.": "Identifier cannot be empty.",
            # Validaciones de nombres, correos y teléfonos en Cliente.
            "El nombre debe ser una cadena de texto.": "Name must be a text string.",
            "El nombre del cliente no puede estar vacío.": "Customer name cannot be empty.",
            "El nombre debe contener al menos dos caracteres.": "Name must contain at least two characters.",
            "El correo electrónico debe ser un texto.": "Email must be a text string.",
            "El correo electrónico no puede estar vacío.": "Email cannot be empty.",
            "El correo electrónico tiene un formato inválido.": "Invalid email format.",
            "El teléfono debe proporcionarse como texto.": "Phone number must be provided as text.",
            "El teléfono debe contener únicamente números.": "Phone number must contain only digits.",
            "El teléfono debe contener entre 7 y 15 dígitos.": "Phone number must contain between 7 and 15 digits.",
            # Validaciones de objetos y estados en Reserva.
            "La reserva requiere un objeto Cliente válido.": "Reservation requires a valid Customer object.",
            "El servicio debe implementar calcular_costo(duracion).": "Service must implement calcular_costo(duracion).",
            "La duración debe ser un número, no un booleano.": "Duration must be a number, not a boolean.",
            "La duración debe ser un valor numérico.": "Duration must be a numeric value.",
            "La duración debe ser un número finito.": "Duration must be a finite number.",
            "La duración debe ser mayor que cero.": "Duration must be greater than zero.",
            "Solo se puede modificar una reserva pendiente.": "Only pending reservations can be modified.",
            "No se puede calcular el costo de una reserva cancelada.": "Cannot calculate the cost of a cancelled reservation.",
            "El servicio debe devolver un costo numérico.": "Service must return a numeric cost.",
            "El costo calculado debe ser finito.": "Calculated cost must be finite.",
            "El costo calculado no puede ser negativo.": "Calculated cost cannot be negative.",
            "Solo se pueden confirmar reservas pendientes.": "Only pending reservations can be confirmed.",
            "La reserva ya se encuentra cancelada.": "Reservation is already cancelled.",
            # Validaciones generales de los servicios.
            "El nombre del servicio debe ser texto.": "Service name must be text.",
            "El nombre del servicio no puede estar vacío": "Service name cannot be empty.",
            "La duración debe ser un número.": "Duration must be a number.",
            "El descuento debe ser un número.": "Discount must be a number.",
            "El descuento debe ser un número finito.": "Discount must be a finite number.",
            "El descuento debe estar entre 0 y 100.": "Discount must be between 0 and 100.",
            "El impuesto debe ser un número.": "Tax must be a number.",
            "El impuesto debe ser un número finito.": "Tax must be a finite number.",
            "El impuesto no puede ser negativo.": "Tax cannot be negative.",
            # Datos particulares de reserva de salas.
            "La capacidad debe ser un número entero.": "Capacity must be an integer.",
            "La capacidad debe ser mayor que cero.": "Capacity must be greater than zero.",
            "La ubicación debe ser texto.": "Location must be text.",
            "La ubicación no puede estar vacía.": "Location cannot be empty.",
            # Datos particulares de alquiler de equipos.
            "El tipo de equipo debe ser texto.": "Equipment type must be text.",
            "El tipo de equipo no puede estar vacío.": "Equipment type cannot be empty.",
            "La cantidad debe ser un número entero.": "Quantity must be an integer.",
            "La cantidad debe ser mayor que cero.": "Quantity must be greater than zero.",
            # Datos particulares de asesorías especializadas.
            "La especialidad debe ser texto.": "Specialty must be text.",
            "La especialidad no puede estar vacía.": "Specialty cannot be empty.",
            "El nombre del asesor debe ser texto.": "Advisor name must be text.",
            "El nombre del asesor no puede estar vacío.": "Advisor name cannot be empty."
        }
        # Traducir exactamente los errores internos conocidos.
        if mensaje in traducciones:
            return traducciones[mensaje]
        # Los errores escritos por la interfaz ya están en inglés.
        mensajes_interfaz = (
            "You must", "All reservation", "Duration", "Discount", "Tax",
            "The selected", "Capacity", "Location", "Equipment", "Quantity",
            "Specialty", "Advisor", "Client ID", "Full name", "Identifier", "Customer", "Email", "Phone",
            "Reservation", "Service"
        )
        if mensaje.startswith(mensajes_interfaz):
            return mensaje
        # Evitar mostrar errores no traducidos o mensajes técnicos al usuario.
        # El detalle original permanece disponible en el archivo de logs.
        return "The operation could not be completed. Please check the entered information."


# Ejecutar la interfaz únicamente cuando se abre este archivo directamente.
if __name__ == "__main__":
    # Crear la ventana principal de Tkinter.
    ventana_principal = tk.Tk()
    # Asociar la ventana con el controlador de Software FJ.
    aplicacion = InterfazSoftwareFJ(ventana_principal)
    # Mantener la ventana activa para responder a las acciones del usuario.
    ventana_principal.mainloop()