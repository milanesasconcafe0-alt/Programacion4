"""
Módulo: excepciones.py
Descripción: Define la jerarquía de excepciones personalizadas para el Sistema
Integral de Gestión de Clientes, Servicios y Reservas de Software FJ.
"""

class ErrorSistemaFJ(Exception):
    """
    Excepción base para todos los errores controlados dentro de Software FJ.
    Permite capturar cualquier fallo propio de la lógica de negocio de forma unificada.
    """
    def __init__(self, mensaje="Ha ocurrido un error general en el sistema Software FJ.", codigo_error="ERR-000"):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class DatosInvalidosError(ErrorSistemaFJ):
    """
    Pasa cuando los datos ingresados para un cliente, servicio o reserva
    no cumplen con el formato, tipo de dato o reglas de validación estrictas.
    """
    def __init__(self, mensaje="Los datos proporcionados son inválidos o están incompletos."):
        super().__init__(mensaje, codigo_error="ERR-101")


class ParametroFaltanteError(ErrorSistemaFJ):
    """
    Ocurre cuando se omite un parámetro obligatorio necesario para ejecutar
    una operación o crear una entidad.
    """
    def __init__(self, nombre_parametro="desconocido"):
        mensaje = f"Falta el parámetro obligatorio: '{nombre_parametro}'."
        super().__init__(mensaje, codigo_error="ERR-102")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """
    Aparece cuando se intenta reservar o asignar un servicio que no existe,
    está inactivo o no cuenta con disponibilidad (salas, equipos o asesores).
    """
    def __init__(self, servicio="Servicio solicitado"):
        mensaje = f"El servicio '{servicio}' no se encuentra disponible actualmente."
        super().__init__(mensaje, codigo_error="ERR-201")


class ReservaInvalidaError(ErrorSistemaFJ):
    """
    Ocurre despues de varios intentos de reserva incorrectos: duración negativa o cero,
    cliente no registrado, o transiciones de estado no permitidas (ej. cancelar
    una reserva ya procesada).
    """
    def __init__(self, mensaje="La operación de reserva no es válida."):
        super().__init__(mensaje, codigo_error="ERR-301")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """
    Aparece cuando se intenta ejecutar una acción restringida por las reglas
    de negocio (ej. duplicar un cliente existente o modificar un registro cerrado).
    """
    def __init__(self, mensaje="Operación no permitida por las políticas del sistema."):
        super().__init__(mensaje, codigo_error="ERR-401")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """
    Se lanza cuando el cálculo de tarifas, impuestos o descuentos arroja un
    resultado negativo, nulo o matemáticamente inconsistente.
    """
    def __init__(self, mensaje="Inconsistencia detectada en el cálculo de costos o tarifas."):
        super().__init__(mensaje, codigo_error="ERR-501")