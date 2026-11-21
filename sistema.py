"""
Módulo: sistema.py
Descripción: Controlador principal de Software FJ. Gestiona clientes, servicios
y reservas mediante listas internas en memoria (sin bases de datos), aplicando
manejo avanzado de excepciones, encadenamiento de errores y registro en logs.
"""

from excepciones import (
    ErrorSistemaFJ,
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)
from modelo import Cliente, Servicio, Reserva
from logs import GestorLogs


class SistemaSoftwareFJ:
    """
    Orquesta todas las operaciones de negocio de Software FJ garantizando que
    cualquier error sea capturado, encadenado y registrado sin detener el programa.
    """

    def __init__(self, ruta_log="eventos_sistema.log"):
        # Almacenamiento exclusivo en listas internas (sin bases de datos)
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = GestorLogs(ruta_log)

    # GESTIÓN DE CLIENTES

    def registrar_cliente(self, id_cliente, nombre, correo, telefono):
        """
        Crea y almacena un nuevo cliente en la lista interna.
        Usa try / except / else para validar duplicados y registrar eventos.
        """
        try:
            # Verificar que no exista un cliente con el mismo ID
            if any(c.id_entidad == str(id_cliente).strip() for c in self.clientes):
                raise OperacionNoPermitidaError(
                    f"El cliente con ID '{id_cliente}' ya se encuentra registrado."
                )

            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)

        except ErrorSistemaFJ as error_negocio:
            self.logger.registrar_error("Clientes", error_negocio, f"ID: {id_cliente}")
            print(f"[ERROR CONTROLADO] {error_negocio}")
            return None
        except Exception as error_inesperado:
            # Encadenamiento de excepciones para errores técnicos no previstos
            error_encadenado = ErrorSistemaFJ(
                f"Fallo inesperado al registrar cliente '{id_cliente}'."
            )
            error_encadenado.__cause__ = error_inesperado
            self.logger.registrar_error("Clientes", error_encadenado)
            print(f"[ERROR CRÍTICO CONTROLADO] {error_encadenado}")
            return None
        else:
            # Se ejecuta solo si no hubo ninguna excepción
            self.clientes.append(nuevo_cliente)
            self.logger.registrar_evento(
                "Clientes", f"Cliente registrado exitosamente -> {nuevo_cliente.obtener_resumen()}"
            )
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def buscar_cliente(self, id_cliente):
        """Busca un cliente en la lista interna por su ID."""
        for cliente in self.clientes:
            if cliente.id_entidad == str(id_cliente).strip():
                return cliente
        raise DatosInvalidosError(f"No existe ningún cliente registrado con ID '{id_cliente}'.")

    # GESTIÓN DE SERVICIOS

    def agregar_servicio(self, servicio):
        """
        Registra una instancia de subclase de Servicio en el catálogo en memoria.
        """
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto proporcionado no es una instancia válida de Servicio.")

            if any(s.id_entidad == servicio.id_entidad for s in self.servicios):
                raise OperacionNoPermitidaError(
                    f"Ya existe un servicio registrado con ID '{servicio.id_entidad}'."
                )

            self.servicios.append(servicio)
            self.logger.registrar_evento(
                "Servicios", f"Servicio agregado -> {servicio.describir_servicio()}"
            )
            print(f"[OK] Servicio agregado: {servicio.describir_servicio()}")
            return servicio

        except ErrorSistemaFJ as error_servicio:
            self.logger.registrar_error("Servicios", error_servicio)
            print(f"[ERROR CONTROLADO] {error_servicio}")
            return None

    def buscar_servicio(self, id_servicio):
        """Busca un servicio en la lista interna por su ID."""
        for servicio in self.servicios:
            if servicio.id_entidad == str(id_servicio).strip():
                return servicio
        raise ServicioNoDisponibleError(f"ID de servicio '{id_servicio}' no encontrado en el catálogo")

    # GESTIÓN DE RESERVAS (CON ENCADENAMIENTO DE EXCEPCIONES Y FINALLY)
    
    def crear_reserva(self, id_reserva, id_cliente, id_servicio, duracion, descuento_pct=0.0):
        """
        Crea una reserva vinculando cliente y servicio.
        Demuestra encadenamiento de excepciones (raise ... from e) y bloque finally.
        """
        reserva_creada = None
        try:
            if any(r.id_entidad == str(id_reserva).strip() for r in self.reservas):
                raise OperacionNoPermitidaError(f"El ID de reserva '{id_reserva}' ya existe.")

            try:
                cliente = self.buscar_cliente(id_cliente)
                servicio = self.buscar_servicio(id_servicio)
            except ErrorSistemaFJ as error_busqueda:
                # Encadenamiento explícito: conserva la causa original del fallo
                raise ReservaInvalidaError(
                    f"Imposible crear la reserva '{id_reserva}' por referencias inválidas."
                ) from error_busqueda

            reserva_creada = Reserva(id_reserva, cliente, servicio, duracion, descuento_pct)

        except ErrorSistemaFJ as error_reserva:
            self.logger.registrar_error("Reservas", error_reserva, f"Reserva: {id_reserva}")
            print(f"[ERROR CONTROLADO] {error_reserva}")
            return None
        else:
            self.reservas.append(reserva_creada)
            self.logger.registrar_evento(
                "Reservas", f"Reserva creada -> {reserva_creada.obtener_resumen()}"
            )
            print(f"[OK] {reserva_creada.obtener_resumen()}")
            return reserva_creada
        finally:
            # Auditoría obligatoria que siempre se ejecuta haya o no error
            self.logger.registrar_evento(
                "Auditoria", f"Intento de creación de reserva '{id_reserva}' finalizado."
            )

    def gestionar_estado_reserva(self, id_reserva, accion):
        """
        Permite confirmar, procesar o cancelar una reserva existente aplicando
        control de errores sobre transiciones de estado.
        """
        try:
            reserva = next((r for r in self.reservas if r.id_entidad == str(id_reserva).strip()), None)
            if reserva is None:
                raise ReservaInvalidaError(f"La reserva '{id_reserva}' no existe en el sistema.")

            accion_norm = accion.strip().upper()
            if accion_norm == "CONFIRMAR":
                reserva.confirmar()
            elif accion_norm == "PROCESAR":
                reserva.procesar()
            elif accion_norm == "CANCELAR":
                reserva.cancelar()
            else:
                raise OperacionNoPermitidaError(f"Acción de reserva desconocida: '{accion}'.")

        except ErrorSistemaFJ as error_estado:
            self.logger.registrar_error("EstadoReserva", error_estado, f"ID: {id_reserva}")
            print(f"[ERROR CONTROLADO] {error_estado}")
            return False
        else:
            self.logger.registrar_evento(
                "EstadoReserva",
                f"Reserva '{id_reserva}' actualizada a estado {reserva.estado}."
            )
            print(f"[OK] Reserva '{id_reserva}' -> Nuevo estado: {reserva.estado}")
            return True

    def mostrar_resumen_general(self):
        """Imprime el estado actual de todas las listas internas en memoria."""
        print("\n" + "=" * 65)
        print("RESUMEN ACTUAL DEL SISTEMA SOFTWARE FJ (EN MEMORIA)")
        print("=" * 65)
        print(f"Total Clientes registrados : {len(self.clientes)}")
        print(f"Total Servicios en catálogo: {len(self.servicios)}")
        print(f"Total Reservas gestionadas : {len(self.reservas)}")
        print("-" * 65)
        for r in self.reservas:
            print(" •", r.obtener_resumen())
        print("=" * 65 + "\n")