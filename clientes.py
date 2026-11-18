from abc import ABC, abstractmethod
import logging
from excepciones import ErrorClienteInvalido

class EntidadBase(ABC):
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass

class Cliente(EntidadBase):
    def __init__(self, identificador: str, nombre: str, telefono: str, correo: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        if valor is None or not isinstance(valor, str) or not valor.strip():
            logging.error(f"Intento de registrar cliente con nombre inválido: {valor}")
            raise ErrorClienteInvalido("El nombre del cliente no puede estar vacío o ser nulo y debe ser texto.")
        self._nombre = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or not isinstance(valor, str) or not valor.strip():
            logging.error(f"Intento de registrar cliente con teléfono inválido: {valor}")
            raise ErrorClienteInvalido("El teléfono del cliente es obligatorio y debe ser texto válido.")
        self._telefono = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if valor is None or not isinstance(valor, str) or "@" not in valor or "." not in valor:
            logging.error(f"Intento de registrar cliente con correo inválido: {valor}")
            raise ErrorClienteInvalido("El formato del correo electrónico no es válido o llegó vacío.")
        self._correo = valor

    def obtener_detalles(self) -> str:
        return f"Cliente ID: {self._identificador}, Nombre: {self._nombre}, Tel: {self._telefono}, Correo: {self._correo}"