"""
Módulo: modelo.py
Descripción: Define la jerarquía de clases del dominio para Software FJ aplicando
abstracción, encapsulación, herencia, polimorfismo y sobrecarga de métodos.
"""

from abc import ABC, abstractmethod
from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError
)


# ==============================================================================
# 1. CLASE ABSTRACTA BASE PARA ENTIDADES DEL SISTEMA
# ==============================================================================
class EntidadSistema(ABC):
    """
    Clase abstracta base que representa cualquier entidad general dentro de Software FJ.
    Obliga a todas las subclases a implementar su propia representación y validación.
    """

    def __init__(self, id_entidad):
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("id_entidad")
        self._id = str(id_entidad).strip()

    @property
    def id_entidad(self):
        return self._id

    @abstractmethod
    def obtener_resumen(self):
        """Método abstracto que debe ser sobrescrito por cada entidad."""
        pass


# ==============================================================================
# 2. CLASE CLIENTE (CON ENCAPSULACIÓN Y VALIDACIONES ESTRICTAS)
# ==============================================================================
class Cliente(EntidadSistema):
    """
    Representa al cliente registrado en Software FJ.
    Protegiendo sus atributos mediante propiedades (@property) y validaciones.
    """

    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError(f"El nombre '{valor}' es inválido ( pon mínimo 3 caracteres).")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in str(valor) or "." not in str(valor):
            raise DatosInvalidosError(f"El correo electrónico '{valor}' no es válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or len(tel_limpio) < 7:
            raise DatosInvalidosError(f"El teléfono '{valor}' debe contener como minimo 7 dígitos numericos.")
        self.__telefono = tel_limpio

    def obtener_resumen(self):
        return f"Cliente [{self.id_entidad}]: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


# ==============================================================================
# 3. CLASE ABSTRACTA SERVICIO Y SUS 3 SUBCLASES (HERENCIA Y POLIMORFISMO)
# ==============================================================================
class Servicio(EntidadSistema, ABC):
    """
    Clase abstracta base para los servicios ofrecidos por Software FJ.
    Define la interfaz común para validación, descripción y cálculo sobrecargado.
    """

    def __init__(self, id_servicio, nombre_servicio, tarifa_base, disponible=True):
        super().__init__(id_servicio)
        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ParametroFaltanteError("nombre_servicio")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError(f"La tarifa base ({tarifa_base}) debe ser un número mayor a cero.")

        self.nombre_servicio = nombre_servicio.strip()
        self.tarifa_base = float(tarifa_base)
        self.disponible = bool(disponible)

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida reglas específicas según el tipo de servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Devuelve una descripción detallada y polimórfica del servicio."""
        pass

    def calcular_costo(self, duracion, descuento_pct=0.0, impuesto_pct=0.19):
        """
        Método sobrecargado mediante parámetros opcionales:
        - Puede llamarse solo con (duracion)
        - Con descuento: (duracion, descuento_pct=10)
        - Con descuento e impuestos personalizados: (duracion, descuento_pct=10, impuesto_pct=0.19)
        """
        self.validar_parametros(duracion)

        if descuento_pct < 0 or descuento_pct >= 100:
            raise CalculoInconsistenteError(f"Porcentaje de descuento no válido: {descuento_pct}%.")
        if impuesto_pct < 0:
            raise CalculoInconsistenteError(f"Porcentaje de impuesto no válido: {impuesto_pct}.")

        subtotal = self.tarifa_base * duracion
        monto_descuento = subtotal * (descuento_pct / 100.0)
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + impuesto_pct)

        if total <= 0:
            raise CalculoInconsistenteError("El calculo final del servicio arrojó un valor menor o igual a cero.")

        return round(total, 2)

    def obtener_resumen(self):
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio especializado: Reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio, nombre_sala, tarifa_hora, capacidad_personas, disponible=True):
        super().__init__(id_servicio, nombre_sala, tarifa_hora, disponible)
        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad_personas = capacidad_personas

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion < 1 or duracion > 12:
            raise ReservaInvalidaError("La reserva de sala debe ser entre 1 y 12 horas.")

    def describir_servicio(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"[Sala] {self.nombre_servicio} (Cap: {self.capacidad_personas} pers.) - ${self.tarifa_base}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado: Alquiler de hardware y equipos tecnológicos."""

    def __init__(self, id_servicio, nombre_equipo, tarifa_dia, gama, disponible=True):
        super().__init__(id_servicio, nombre_equipo, tarifa_dia, disponible)
        if not gama or str(gama).strip() == "":
            raise ParametroFaltanteError("gama")
        self.gama = gama.strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise ReservaInvalidaError("El alquiler de equipos requiere días en enteros entre 1 y 30.")

    def describir_servicio(self):
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"[Equipo] {self.nombre_servicio} (Gama {self.gama}) - ${self.tarifa_base}/día [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado: Consultoría técnica y desarrollo a medida."""

    def __init__(self, id_servicio, tema_asesoria, tarifa_hora, especialista, disponible=True):
        super().__init__(id_servicio, tema_asesoria, tarifa_hora, disponible)
        if not especialista or str(especialista).strip() == "":
            raise ParametroFaltanteError("especialista")
        self.especialista = especialista.strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion < 0.5:
            raise ReservaInvalidaError("La asesoría especializada requiere una duración mínima de 0.5 horas.")

    def describir_servicio(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[Asesoría] {self.nombre_servicio} con {self.especialista} - ${self.tarifa_base}/h [{estado}]"



# 4) CLASE RESERVA (INTEGRACIÓN Y GESTIÓN DE ESTADOS)
class Reserva(EntidadSistema):
    """
    Integra un Cliente, un Servicio, a demas de la duración y el estado de la reserva,
    controlando transiciones de estado con excepciones personalizadas.
    """

    def __init__(self, id_reserva, cliente, servicio, duracion, descuento_pct=0.0):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("La reserva requiere una instancia valida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("La reserva requiere una instancia valida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre_servicio)

        # Valida la duración según el tipo específico de servicio (polimorfismo)
        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.descuento_pct = descuento_pct
        self.estado = "PENDIENTE"
        self.costo_total = self.servicio.calcular_costo(duracion, descuento_pct=descuento_pct)

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.id_entidad} porque está en estado '{self.estado}'."
            )
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(self.servicio.nombre_servicio)

        self.estado = "CONFIRMADA"
        self.servicio.disponible = False

    def procesar(self):
        if self.estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: '{self.estado}')."
            )
        self.estado = "PROCESADA"

    def cancelar(self):
        if self.estado == "PROCESADA":
            raise OperacionNoPermitidaError(
                f"La reserva {self.id_entidad} ya fue PROCESADA y no puede cancelarse."
            )
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id_entidad} ya se encuentra CANCELADA.")

        self.estado = "CANCELADA"
        self.servicio.disponible = True

    def obtener_resumen(self):
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self.estado} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_servicio} | "
            f"Duración: {self.duracion} | Total: ${self.costo_total}"
        )