class ErrorSistemaSoftwareFJ(Exception):
    """Excepción base del sistema."""
    pass

class ErrorClienteInvalido(ErrorSistemaSoftwareFJ):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

class ErrorReservaInvalida(ErrorSistemaSoftwareFJ):
    """Excepción lanzada cuando se intenta realizar una reserva con parámetros incorrectos."""
    pass

class ServicioNoDisponibleError(ErrorSistemaSoftwareFJ):
    """Excepción lanzada cuando el servicio solicitado no está disponible."""
    pass

class ErrorCostoInvalido(ErrorSistemaSoftwareFJ):
    """Excepción lanzada cuando el cálculo de costos resulta negativo o inválido."""
    pass