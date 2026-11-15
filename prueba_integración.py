# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: PROGRAMACIÓN (213023)
# Fase 4: PRÁCTICAS SIMULADAS
# Trabajo: SISTEMA INTEGRAL SOFTWARE FJ
# Nombre del producto: prueba_integracion.py
# Autora: María Paula Marín Tolosa

#Importo las clases necesarias para realizar la prueba de integración con mi programa servicios y los de mi compañera.

from cliente import Cliente
from reserva import Reserva
from servicios import (
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas
)


# Inicio creando un cliente, donde se ejecutan las validaciones definidas en el cosntructor de cliente para verificar que los datos sean correctos
cliente = Cliente(
    "C001",
    "Maria Perez",
    "maria@gmail.com",
    "3001234567"
)


# Creo los servicios donde la clase de servicios heredad de Servicio y esta a su vez hereda de entidad, permitiendo reutilziar características comunes y definir propiedades particulares para cada tipo de servicio.
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


# Creo las reservas, se inicia la prueba de los cálculos de costos para los 3 servisios
print("\nPRUEBAS DE DESCUENTOS E IMPUESTOS")

#Se recorren los diferentes servicios utilizando el mismo método , donde cada clase calcula el costo de acuerdo a sus características demostrando el polimorfismo

for servicio in [sala, equipos, asesoria]:
    print(f"\nServicio: {servicio.nombre}")
    print("Tarifa original:", f"${servicio.TARIFA_POR_HORA:,.0f}")
    print("Costo normal:", f"${servicio.calcular_costo(2):,.2f}")
    print("Con descuento:", f"${servicio.calcular_costo(2, descuento=10):,.2f}")
    print(
        "Con descuento e impuesto:",
        f"${servicio.calcular_costo(2, descuento=10, impuesto=19):,.2f}"
    )

reserva1 = Reserva("R001", cliente, sala, 1.5)
reserva2 = Reserva("R002", cliente, equipos, 1.5)
reserva3 = Reserva("R003", cliente, asesoria, 1.25)


# Confirmamos las reservas,donde se recorre cada reserva para ejecutar su proceso de confirmación, durante el procedimiento se calcula el costo correspondiente y se actualiza el estado de la reserva cuando la operación es valida
for reserva in [reserva1, reserva2, reserva3]:
    print(reserva.confirmar_reserva())
    print(reserva.mostrar_informacion())
    print("-" * 40)
