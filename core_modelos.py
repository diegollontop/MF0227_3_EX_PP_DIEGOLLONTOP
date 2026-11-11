from abc import ABC, abstractmethod


# Excepción personalizada para el manejo de errores de negocio
class EstadoInvalidoError(Exception):
    """Se lanza cuando se intenta realizar una transición de estado no permitida."""
    pass


class TicketTecnico(ABC):
    """Clase base abstracta que representa un ticket técnico genérico."""

    ESTADOS_VALIDOS = ("Abierto", "En Proceso", "Cerrado")
    PRIORIDADES_VALIDAS = ("Baja", "Media", "Alta", "Critica")

    # Reglas de transición: clave = estado actual, valor = estados permitidos siguientes
    TRANSICIONES_PERMITIDAS = {
        "Abierto": ["En Proceso", "Cerrado"],
        "En Proceso": ["Cerrado"],
        "Cerrado": []  # Un ticket cerrado no puede volver a abrirse ni pasar a 'En Proceso'
    }

    def __init__(self, id_ticket: int, titulo: str, prioridad: str = "Media"):
        self._id = id_ticket
        self._titulo = titulo
        self._estado = "Abierto"  # Todo ticket nace abierto

        if prioridad not in self.PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridad inválida. Debe ser una de: {self.PRIORIDADES_VALIDAS}")
        self._prioridad = prioridad

    # --- ENCAPSULAMIENTO (Getters con @property) ---
    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def prioridad(self) -> str:
        return self._prioridad

    # --- LÓGICA DE NEGOCIO Y VALIDACIÓN ---
    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Valida y actualiza el estado del ticket según las reglas de transición."""
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise EstadoInvalidoError(f"El estado '{nuevo_estado}' no existe en el sistema.")

        estados_siguientes = self.TRANSICIONES_PERMITIDAS.get(self._estado, [])
        if nuevo_estado not in estados_siguientes:
            raise EstadoInvalidoError(
                f"Transición prohibida: No se puede pasar de '{self._estado}' a '{nuevo_estado}'."
            )

        self._estado = nuevo_estado

    # --- POLIMORFISMO (Método abstracto) ---
    @abstractmethod
    def calcular_sla(self) -> int:
        """Calcula y devuelve las horas máximas de resolución según tipo y prioridad."""
        pass

    def __str__(self) -> str:
        return (
            f"[{self.__class__.__name__} #{self._id}] '{self._titulo}' | "
            f"Estado: {self._estado} | Prioridad: {self._prioridad} | "
            f"SLA: {self.calcular_sla()}h"
        )


# --- HERENCIA Y POLIMORFISMO ---
class TicketHardware(TicketTecnico):
    """Subclase especializada en incidencias físicas o de equipamiento."""

    def __init__(self, id_ticket: int, titulo: str, componente: str, prioridad: str = "Media"):
        super().__init__(id_ticket, titulo, prioridad)
        self._componente = componente

    @property
    def componente(self) -> str:
        return self._componente

    def calcular_sla(self) -> int:
        # Los problemas de hardware suelen requerir desplazamiento o repuestos (tiempos mayores)
        tiempos_sla = {
            "Critica": 4,
            "Alta": 12,
            "Media": 24,
            "Baja": 72
        }
        return tiempos_sla[self._prioridad]

    def __str__(self) -> str:
        return f"{super().__str__()} | Componente: {self._componente}"


class TicketSoftware(TicketTecnico):
    """Subclase especializada en incidencias lógicas, aplicaciones o sistemas."""

    def __init__(self, id_ticket: int, titulo: str, sistema_operativo: str, prioridad: str = "Media"):
        super().__init__(id_ticket, titulo, prioridad)
        self._sistema_operativo = sistema_operativo

    @property
    def sistema_operativo(self) -> str:
        return self._sistema_operativo

    def calcular_sla(self) -> int:
        # Los problemas de software suelen resolverse en remoto (tiempos menores)
        tiempos_sla = {
            "Critica": 2,
            "Alta": 6,
            "Media": 16,
            "Baja": 48
        }
        return tiempos_sla[self._prioridad]

    def __str__(self) -> str:
        return f"{super().__str__()} | SO: {self._sistema_operativo}"


# --- BLOQUE DE PRUEBAS UNITARIAS BÁSICAS ---
if __name__ == "__main__":
    print("=== INICIANDO PRUEBAS DE MODELOS POO ===\n")

    # 1. Creación de instancias (Polimorfismo en acción)
    t_hw = TicketHardware(101, "Fallo en fuente de alimentación", "Servidor Rack", "Critica")
    t_sw = TicketSoftware(102, "Error de permisos en base de datos", "Ubuntu 24.04", "Alta")

    tickets = [t_hw, t_sw]
    for ticket in tickets:
        print(ticket)

    print("\n--- Probando transiciones de estado válidas ---")
    t_hw.cambiar_estado("En Proceso")
    print(f"Nuevo estado Ticket #{t_hw.id}: {t_hw.estado}")

    t_hw.cambiar_estado("Cerrado")
    print(f"Nuevo estado Ticket #{t_hw.id}: {t_hw.estado}")

    print("\n--- Probando manejo de excepciones (Transición inválida) ---")
    try:
        # Intentamos pasar de 'Cerrado' a 'En Proceso' (debe fallar)
        t_hw.cambiar_estado("En Proceso")
    except EstadoInvalidoError as e:
        print(f"[EXCEPCIÓN CAPTURADA CORRECTAMENTE]: {e}")

    try:
        # Intentamos asignar un estado inventado
        t_sw.cambiar_estado("En Pausa")
    except EstadoInvalidoError as e:
        print(f"[EXCEPCIÓN CAPTURADA CORRECTAMENTE]: {e}")
