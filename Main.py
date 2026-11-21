"""
Módulo: Main.py
Descripción: Script principal de ejecución y simulación para Software FJ.
Ejecuta 12 operaciones completas (válidas e inválidas) demostrando estabilidad,
polimorfismo, sobrecarga de métodos y manejo avanzado de excepciones sin BD.
"""

from sistema import SistemaSoftwareFJ
from modelo import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSistemaFJ


def ejecutar_simulacion():
    print("=" * 70)
    print("INICIANDO SIMULACIÓN - SISTEMA INTEGRAL SOFTWARE FJ")
    print("=" * 70)

    # Instancia principal del sistema (trabaja en la memoria ademas del archivo .log)
    app = SistemaSoftwareFJ(ruta_log="eventos_sistema.log")

    # OPERACIÓN 1 (LA QUE VÁLIDA): Registro de clientes con datos correctos

    print("\n--- [OP 1] Registro de clientes válidos ---")
    app.registrar_cliente("C001", "Laura Martínez", "laura.martinez@correo.com", "3104567890")
    app.registrar_cliente("C002", "Carlos Gómez", "carlos.gomez@empresa.co", "3209876543")

    # OPERACIÓN 2 (LA QUE INVÁLIDA): Registro de cliente con datos erróneos como el correo o teléfono

    print("\n--- [OP 2] Intento de registro de clientes con datos inválidos ---")
    app.registrar_cliente("C003", "An", "correo_sin_arroba.com", "123")
    app.registrar_cliente("C001", "Laura Duplicada", "otra@correo.com", "3001112233")

    # OPERACIÓN 3 (VÁLIDA): Creación y registro de los 3 tipos de servicios

    print("\n--- [OP 3] Agregando catálogo de servicios especializados ---")
    sala_juntas = ReservaSala("S001", "Sala Innovación Norte", tarifa_hora=80.0, capacidad_personas=12)
    equipo_servidor = AlquilerEquipo("S002", "Workstation Dell Precision", tarifa_dia=120.0, gama="Alta")
    asesoria_cloud = AsesoriaEspecializada("S003", "Arquitectura Cloud y Python", tarifa_hora=150.0, especialista="Ing. Luis Donneys")

    app.agregar_servicio(sala_juntas)
    app.agregar_servicio(equipo_servidor)
    app.agregar_servicio(asesoria_cloud)

    # OPERACIÓN 4 (INVÁLIDA): Creación de servicio con tarifa negativa ( una captura directa)

    print("\n--- [OP 4] Intento de creación de servicio con tarifa inválida ---")
    try:
        servicio_erroneo = ReservaSala("S004", "Sala Defectuosa", tarifa_hora=-50.0, capacidad_personas=5)
        app.agregar_servicio(servicio_erroneo)
    except ErrorSistemaFJ as e:
        app.logger.registrar_error("Main_Servicios", e, "Creación directa de servicio inválido")
        print(f"[ERROR CONTROLADO EN MAIN] {e}")

    # OPERACIÓN 5 (VÁLIDA - SOBRECARGA): Reserva de sala sin descuento (impuesto por defecto)

    print("\n--- [OP 5] Reserva válida de sala (cálculo base con IVA 19%) ---")
    app.crear_reserva("R001", "C001", "S001", duracion=4)


    # OPERACIÓN 6 (VÁLIDA - SOBRECARGA): Alquiler de equipo con descuento del 15%

    print("\n--- [OP 6] Reserva válida de equipo con descuento aplicado (15%) ---")
    app.crear_reserva("R002", "C002", "S002", duracion=5, descuento_pct=15.0)


    # OPERACIÓN 7 (INVÁLIDA - ENCADENAMIENTO): Reserva con cliente inexistente

    print("\n--- [OP 7] Intento de reserva con cliente inexistente (Encadenamiento) ---")
    app.crear_reserva("R003", "C999", "S003", duracion=2)

    # OPERACIÓN 8 (INVÁLIDA): Reserva con duración fuera de rango permitido

    print("\n--- [OP 8] Intento de reserva de sala excediendo el límite de 12 horas ---")
    app.crear_reserva("R004", "C001", "S003", duracion=0.1)

    # OPERACIÓN 9 (VÁLIDA): Confirmación y procesamiento exitoso de reserva R001

    print("\n--- [OP 9] Flujo completo de estados en reserva R001 (Confirmar -> Procesar) ---")
    app.gestionar_estado_reserva("R001", "CONFIRMAR")
    app.gestionar_estado_reserva("R001", "PROCESAR")


    # OPERACIÓN 10 (INVÁLIDA): Intento de cancelar una reserva ya procesada (R001) para probar manejo de excepciones y logging
    print("\n--- [OP 10] Intento de cancelar reserva R001 ya procesada ---")
    app.gestionar_estado_reserva("R001", "CANCELAR")

    # OPERACIÓN 11 (INVÁLIDA): Intentar reservar un servicio ocupado (S002 está reservado/confirmado)

    print("\n--- [OP 11] Confirmación de R002 y bloqueo de disponibilidad del servicio ---")
    app.gestionar_estado_reserva("R002", "CONFIRMAR")
    app.crear_reserva("R005", "C001", "S002", duracion=2)

    # OPERACIÓN 12 (VÁLIDA): Cancelación de R002 libera el equipo para nueva reserva

    print("\n--- [OP 12] Cancelación de R002 y nueva reserva exitosa sobre el equipo liberado ---")
    app.gestionar_estado_reserva("R002", "CANCELAR")
    app.crear_reserva("R006", "C001", "S002", duracion=3, descuento_pct=10.0)

    # Mostrar resumen final en consola y confirmar que el programa sigue estable
    app.mostrar_resumen_general()
    print("[ÉXITO] Simulación finalizada sin interrupciones. Revisa 'eventos_sistema.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()