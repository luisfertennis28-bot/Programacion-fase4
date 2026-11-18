import logging
from clientes import Cliente
from servicios import Servicio
from excepciones import ServicioNoDisponibleError, ErrorReservaInvalida, ErrorCostoInvalido

class Reserva:
    def __init__(self, cliente: Cliente, servicio: Servicio, cantidad: int):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Creada"
        self.costo_final = 0.0

    def confirmar_reserva(self, *args, **kwargs):
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre_servicio}' no está disponible actualmente.")
            if self.estado == "Confirmada":
                raise ErrorReservaInvalida("La reserva ya fue confirmada previamente; no se puede confirmar dos veces.")

            self.costo_final = self.servicio.calcular_costo(self.cantidad, *args, **kwargs)
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada exitosamente para {self.cliente.nombre}. Costo: {self.costo_final}")
            
        except (ServicioNoDisponibleError, ErrorReservaInvalida, ErrorCostoInvalido) as e:
            self.estado = "Fallida"
            logging.error(f"Fallo controlado al confirmar reserva: {e}")
            raise
        except Exception as e:
            self.estado = "Fallida"
            logging.error(f"Fallo inesperado al confirmar reserva: {e}")
            raise ErrorReservaInvalida(f"No se pudo procesar la reserva: {e}") from e
        else:
            print(f"-> ¡Éxito! Reserva procesada para el cliente {self.cliente.nombre}. Total: ${self.costo_final}")
        finally:
            print(f"-> Operación de reserva finalizada con estado: {self.estado}\n")

    def cancelar_reserva(self):
        try:
            if self.estado != "Confirmada":
                raise ErrorReservaInvalida(f"No se puede cancelar una reserva en estado '{self.estado}'.")
            self.estado = "Cancelada"
            logging.info(f"Reserva cancelada exitosamente para el cliente {self.cliente.nombre}")
        except ErrorReservaInvalida as e:
            logging.error(f"Error al cancelar reserva: {e}")
            raise
        else:
            print(f"-> Aviso: Reserva de {self.cliente.nombre} cancelada correctamente.")
        finally:
            print(f"-> Estado actual tras cancelación: {self.estado}\n")