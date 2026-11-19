"""
Módulo: logs.py
Gestiona el registro persistente de eventos y errores del sistema
Software FJ en un archivo .log sin usar base de datos.
"""

from datetime import datetime


class GestorLogs:
    """
    Esta clase se encarga de escribir la trazabilidad de operaciones y excepciones
    en un archivo de logs, asegurando que un fallo de escritura no detenga
    la ejecución principal del programa.
    """

    def __init__(self, ruta_archivo="eventos_sistema.log"):
        self.ruta_archivo = ruta_archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        """Crea o verifica el archivo de log al iniciar el gestor."""
        try:
            with open(self.ruta_archivo, mode="a", encoding="utf-8") as archivo:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archivo.write(f"\n{'='*60}\n")
                archivo.write(f"[{fecha_hora}] [INICIO] Sesión de registro iniciada en Software FJ\n")
                archivo.write(f"{'='*60}\n")
        except OSError as error_io:
            print(f"[ADVERTENCIA CRÍTICA] No se pudo inicializar el archivo de log: {error_io}")

    def registrar_evento(self, modulo, mensaje):
        """
        Registra una operación exitosa o evento informativo en el archivo de log.
        Implementa la estructura try / except / else / finally exigida en la guía.
        """
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{fecha_hora}] [INFO] [{modulo}] {mensaje}\n"
        archivo = None

        try:
            archivo = open(self.ruta_archivo, mode="a", encoding="utf-8")
            archivo.write(linea)
        except OSError as error_io:
            print(f"[FALLO DE LOG] No se pudo guardar el evento: {error_io}")
        else:
            # Se ejecuta únicamente si la escritura en el archivo fue exitosa
            pass
        finally:
            # Garantiza el cierre seguro del recurso en memoria
            if archivo and not archivo.closed:
                archivo.close()

    def registrar_error(self, modulo, excepcion, contexto=""):
        """
        Registra una excepción capturada (personalizada o nativa) junto con su
        causa encadenada si existe, manteniendo la aplicación estable.
        """
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tipo_error = type(excepcion).__name__
        detalle_causa = ""

        # Verifica si hubo encadenamiento de excepciones (raise ... from e)
        if excepcion.__cause__ is not None:
            detalle_causa = f" | Causa original: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}"

        info_contexto = f" ({contexto})" if contexto else ""
        linea = f"[{fecha_hora}] [ERROR] [{modulo}]{info_contexto} {tipo_error}: {excepcion}{detalle_causa}\n"
        archivo = None

        try:
            archivo = open(self.ruta_archivo, mode="a", encoding="utf-8")
            archivo.write(linea)
        except OSError as error_io:
            print(f"[FALLO DE LOG] No se pudo registrar el error en disco: {error_io}")
        finally:
            if archivo and not archivo.closed:
                archivo.close()