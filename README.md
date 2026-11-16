from abc import ABC, abstractmethod
from datetime import datetime
import logging

# Configuración del archivo de logs para registrar eventos y errores
import os

# Asegurar que el log se guarde en la misma carpeta del script
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sistema_software_fj.log')

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorClienteInvalido(Exception):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

class ErrorReservaInvalida(Exception):
    """Excepción lanzada cuando se intenta realizar una reserva con parámetros incorrectos."""
    pass

class ServicioNoDisponibleError(Exception):
    """Excepción lanzada cuando el servicio solicitado no está disponible."""
    pass


# ==========================================
# CLASE ABSTRACTA BASE
# ==========================================
class EntidadBase(ABC):
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass


# ==========================================
# CLASE CLIENTE
# ==========================================
class Cliente(EntidadBase):
    def __init__(self, identificador: str, nombre: str, correo: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str):
            logging.error(f"Intento de registrar cliente con nombre inválido: {valor}")
            raise ErrorClienteInvalido("El nombre del cliente no puede estar vacío y debe ser texto.")
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            logging.error(f"Intento de registrar cliente con correo inválido: {valor}")
            raise ErrorClienteInvalido("El formato del correo electrónico no es válido.")
        self._correo = valor

    def obtener_detalles(self) -> str:
        return f"Cliente ID: {self._identificador}, Nombre: {self._nombre}, Correo: {self._correo}"


# ==========================================
# CLASE ABSTRACTA SERVICIO Y POLIMORFISMO
# ==========================================
class Servicio(EntidadBase, ABC):
    def __init__(self, identificador: str, nombre_servicio: str, costo_base: float):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass


# 1. Servicio Especializado: Reserva de Salas
class ReservaSala(Servicio):
    def __init__(self, identificador: str, costo_base: float, capacidad: int):
        super().__init__(identificador, "Reserva de Sala", costo_base)
        self.capacidad = capacidad

    # Método sobrecargado / flexible para cálculo de costos (con o sin descuento/impuesto)
    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        try:
            if horas <= 0:
                raise ValueError("Las horas de reserva deben ser mayores a cero.")
            costo_total = (self.costo_base * horas) * (1 - descuento)
            logging.info(f"Costo calculado para Sala {self._identificador}: {costo_total}")
            return costo_total
        except Exception as e:
            logging.error(f"Error calculando costo de sala: {e}")
            raise

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Capacidad: {self.capacidad} personas | Costo base: {self.costo_base}"


# 2. Servicio Especializado: Alquiler de Equipos
class AlquilerEquipo(Servicio):
    def __init__(self, identificador: str, costo_base: float, tipo_equipo: str):
        super().__init__(identificador, "Alquiler de Equipo", costo_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int, seguro: bool = False) -> float:
        try:
            if dias <= 0:
                raise ValueError("Los días de alquiler deben ser mayores a cero.")
            adicional_seguro = 15.0 if seguro else 0.0
            costo_total = (self.costo_base * dias) + adicional_seguro
            logging.info(f"Costo calculado para Equipo {self.tipo_equipo}: {costo_total}")
            return costo_total
        except Exception as e:
            logging.error(f"Error calculando costo de equipo: {e}")
            raise

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Equipo: {self.tipo_equipo} | Costo base: {self.costo_base}"


# 3. Servicio Especializado: Asesorías Especializadas
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


# ==========================================
# CLASE RESERVA CON MANEJO DE EXCEPCIONES
# ==========================================
class Reserva:
    def __init__(self, cliente: Cliente, servicio: Servicio, cantidad: int):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Creada"

    def confirmar_reserva(self, *args, **kwargs):
        try:
            # Bloque try - except - else - finally exigido por la guía
            self.costo_final = self.servicio.calcular_costo(self.cantidad, *args, **kwargs)
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada exitosamente para {self.cliente.nombre}")
        except Exception as e:
            self.estado = "Fallida"
            logging.error(f"Fallo al confirmar reserva: {e}")
            raise ErrorReservaInvalida(f"No se pudo procesar la reserva: {e}") from e
        else:
            print(f"-> ¡Éxito! Reserva procesada para el cliente {self.cliente.nombre}.")
        finally:
            print(f"-> Operación de reserva finalizada con estado: {self.estado}\n")


# ==========================================
# SIMULACIÓN DE 10 OPERACIONES (Válidas e Inválidas)
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO SIMULACIÓN DE OPERACIONES SOFTWARE FJ ---")
    
    # Lista para almacenar operaciones y demostrar el uso de listas sin bases de datos
    operaciones_realizadas = []

    # Operación 1: Registro de Cliente Válido
    try:
        c1 = Cliente("C001", "Carlos Pérez", "carlos@mail.com")
        operaciones_realizadas.append(c1)
        print(c1.obtener_detalles())
    except ErrorClienteInvalido as err:
        print(f"Capturado error de cliente: {err}")

    # Operación 2: Registro de Cliente Inválido (Provocando excepción)
    try:
        c_malo = Cliente("C002", "Ana Gómez", "correo-invalido-sin-arroba")
    except ErrorClienteInvalido as err:
        print(f"[EXCEPCIÓN CONTROLADA] Registro inválido evitado: {err}")

    # Operación 3: Creación de Servicio de Sala
    sala = ReservaSala("S01", 50.0, 10)
    print(sala.obtener_detalles())

    # Operación 4: Creación de Servicio de Equipo
    equipo = AlquilerEquipo("E01", 20.0, "Proyector 4K")
    print(equipo.obtener_detalles())

    # Operación 5: Creación de Servicio de Asesoría
    asesoria = AsesoriaEspecializada("A01", 100.0, "Arquitectura de Software")
    print(asesoria.obtener_detalles())

    # Operación 6: Reserva Exitosa de Sala
    if 'c1' in locals():
        res1 = Reserva(c1, sala, 3)
        res1.confirmar_reserva(descuento=0.1)

    # Operación 7: Reserva Exitosa de Equipo
        res2 = Reserva(c1, equipo, 5)
        res2.confirmar_reserva(seguro=True)

    # Operación 8: Reserva Exitosa de Asesoría
        res3 = Reserva(c1, asesoria, 2)
        res3.confirmar_reserva(complejidad_alta=True)

    # Operación 9: Reserva Inválida (Horas negativas - prueba robustez)
    try:
        res_fallida = Reserva(c1, sala, -2)
        res_fallida.confirmar_reserva()
    except ErrorReservaInvalida as e:
        print(f"[EXCEPCIÓN CONTROLADA] Reserva rechazada correctamente: {e}")

    # Operación 10: Validación de estabilidad general del sistema tras errores
    print("--- Simulación finalizada. El sistema se mantuvo estable y generó el archivo 'sistema_software_fj.log'. ---")# fundamentos-programacion-fase5
Solución del Problemas de la Fase 5 del curso Fundamentos de Programación - UNAD.
