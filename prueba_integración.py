from cliente import Cliente
from reserva import Reserva
from servicios import (
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas
)


# Creamos un cliente
cliente = Cliente(
    "C001",
    "Maria Perez",
    "maria@gmail.com",
    "3001234567"
)


# Creamos los servicios
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


# Creamos las reservas
print("\nPRUEBAS DE DESCUENTOS E IMPUESTOS")

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


# Confirmamos las reservas
for reserva in [reserva1, reserva2, reserva3]:
    print(reserva.confirmar_reserva())
    print(reserva.mostrar_informacion())
    print("-" * 40)