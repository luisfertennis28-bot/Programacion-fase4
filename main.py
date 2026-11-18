import logging
import os
from excepciones import ErrorClienteInvalido, ErrorReservaInvalida, ServicioNoDisponibleError, ErrorCostoInvalido
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sistema_software_fj.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("--- INICIANDO SIMULACIÓN DE OPERACIONES SOFTWARE FJ ---\n")
    operaciones_realizadas = []

    # Operación 1: Registro de Cliente Válido
    print("1. Registro de Cliente Válido:")
    try:
        c1 = Cliente("C001", "Carlos Pérez", "3101234567", "carlos@mail.com")
        operaciones_realizadas.append(c1)
        print(c1.obtener_detalles() + "\n")
    except ErrorClienteInvalido as err:
        print(f"Capturado error de cliente: {err}\n")

    # Operación 2: Registro de Cliente Inválido (Correo sin @)
    print("2. Registro de Cliente Inválido (Correo mal formado):")
    try:
        c_malo = Cliente("C002", "Ana Gómez", "3209876543", "correo-invalido-sin-arroba")
    except ErrorClienteInvalido as err:
        print(f"[EXCEPCIÓN CONTROLADA] Registro inválido evitado: {err}\n")

    # Operación 3: Registro de Cliente Inválido (Teléfono vacío y correo None)
    print("3. Registro de Cliente Inválido (Teléfono vacío y correo None):")
    try:
        c_nulo = Cliente("C003", "Luis Díaz", "", None)
    except ErrorClienteInvalido as err:
        print(f"[EXCEPCIÓN CONTROLADA] Validación de datos nulos exitosa: {err}\n")

    # Operación 4: Creación de Servicios
    print("4. Creación de Catálogo de Servicios:")
    sala = ReservaSala("S01", 50.0, 10)
    equipo = AlquilerEquipo("E01", 20.0, "Proyector 4K")
    asesoria = AsesoriaEspecializada("A01", 100.0, "Arquitectura de Software")
    equipo_no_disp = AlquilerEquipo("E02", 30.0, "Servidor Dedicado")
    equipo_no_disp.disponible = False
    print(sala.obtener_detalles())
    print(equipo.obtener_detalles())
    print(asesoria.obtener_detalles() + "\n")

    # Operación 5: Reserva Exitosa de Sala
    print("5. Reserva Exitosa de Sala:")
    res1 = Reserva(c1, sala, 3)
    res1.confirmar_reserva(descuento=0.1)

    # Operación 6: Intento de confirmar dos veces la misma reserva
    print("6. Intento de Doble Confirmación:")
    try:
        res1.confirmar_reserva(descuento=0.1)
    except ErrorReservaInvalida as e:
        print(f"[EXCEPCIÓN CONTROLADA] Doble confirmación bloqueada: {e}\n")

    # Operación 7: Reserva Exitosa de Equipo y Cancelación posterior
    print("7. Reserva Exitosa de Equipo y Cancelación:")
    res2 = Reserva(c1, equipo, 5)
    res2.confirmar_reserva(seguro=True)
    res2.cancelar_reserva()

    # Operación 8: Intento de cancelar una reserva no confirmada
    print("8. Intento de Cancelar Reserva Pendiente:")
    try:
        res_pendiente = Reserva(c1, asesoria, 2)
        res_pendiente.cancelar_reserva()
    except ErrorReservaInvalida as e:
        print(f"[EXCEPCIÓN CONTROLADA] Cancelación inválida evitada: {e}\n")

    # Operación 9: Descuento mayor al costo total
    print("9. Reserva con Descuento Mayor al Costo:")
    try:
        res_desc_malo = Reserva(c1, equipo, 1)
        res_desc_malo.confirmar_reserva(descuento_fijo=500.0)
    except ErrorCostoInvalido as e:
        print(f"[EXCEPCIÓN CONTROLADA] Costo negativo bloqueado: {e}\n")

    # Operación 10: Reserva Inválida (Servicio no disponible y horas en cero)
    print("10. Reserva de Servicio No Disponible y Horas en Cero:")
    try:
        res_indisp = Reserva(c1, equipo_no_disp, 2)
        res_indisp.confirmar_reserva()
    except ServicioNoDisponibleError as e:
        print(f"[EXCEPCIÓN CONTROLADA] Servicio inactivo detectado: {e}\n")

    try:
        res_cero = Reserva(c1, sala, 0)
        res_cero.confirmar_reserva()
    except ErrorReservaInvalida as e:
        print(f"[EXCEPCIÓN CONTROLADA] Horas en cero rechazadas (Causa: {e.__cause__}): {e}\n")

    print("--- Simulación finalizada. El sistema se mantuvo estable y generó el archivo 'sistema_software_fj.log'. ---")