from abc import ABC, abstractmethod
import logging
from clientes import EntidadBase
from excepciones import ErrorCostoInvalido

class Servicio(EntidadBase, ABC):
    def __init__(self, identificador: str, nombre_servicio: str, costo_base: float):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass

class ReservaSala(Servicio):
    def __init__(self, identificador: str, costo_base: float, capacidad: int):
        super().__init__(identificador, "Reserva de Sala", costo_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        try:
            if horas <= 0:
                raise ValueError("Las horas de reserva deben ser mayores a cero.")
            if descuento < 0 or descuento > 1.0:
                raise ErrorCostoInvalido(f"Descuento inválido ({descuento*100}%): no puede ser negativo ni mayor al 100%.")
            costo_total = (self.costo_base * horas) * (1 - descuento)
            if costo_total < 0:
                raise ErrorCostoInvalido("El costo total calculado no puede ser negativo.")
            logging.info(f"Costo calculado para Sala {self._identificador}: {costo_total}")
            return costo_total
        except Exception as e:
            logging.error(f"Error calculando costo de sala: {e}")
            raise

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Capacidad: {self.capacidad} personas | Costo base: {self.costo_base}"

class AlquilerEquipo(Servicio):
    def __init__(self, identificador: str, costo_base: float, tipo_equipo: str):
        super().__init__(identificador, "Alquiler de Equipo", costo_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int, seguro: bool = False, descuento_fijo: float = 0.0) -> float:
        try:
            if dias <= 0:
                raise ValueError("Los días de alquiler deben ser mayores a cero.")
            if descuento_fijo < 0:
                raise ErrorCostoInvalido("El descuento fijo no puede ser negativo.")
            adicional_seguro = 15.0 if seguro else 0.0
            costo_total = (self.costo_base * dias) + adicional_seguro - descuento_fijo
            if costo_total < 0:
                raise ErrorCostoInvalido("El descuento aplicado supera el costo total del alquiler.")
            logging.info(f"Costo calculado para Equipo {self.tipo_equipo}: {costo_total}")
            return costo_total
        except Exception as e:
            logging.error(f"Error calculando costo de equipo: {e}")
            raise

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Equipo: {self.tipo_equipo} | Costo base: {self.costo_base}"

class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador: str, costo_base: float, area: str):
        super().__init__(identificador, "Asesoría Especializada", costo_base)
        self.area = area

    def calcular_costo(self, sesiones: int, complejidad_alta: bool = False) -> float:
        try:
            if sesiones <= 0:
                raise ValueError("El número de sesiones debe ser mayor a cero.")
            multiplicador = 1.3 if complejidad_alta else 1.0
            costo_total = (self.costo_base * sesiones) * multiplicador
            logging.info(f"Costo calculado para Asesoría en {self.area}: {costo_total}")
            return costo_total
        except Exception as e:
            logging.error(f"Error calculando costo de asesoría: {e}")
            raise

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Área: {self.area} | Costo base: {self.costo_base}"