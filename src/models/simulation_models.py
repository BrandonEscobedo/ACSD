from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field
class Prioridad(Enum):
    """Niveles de prioridad para contenedores"""
    ALTA = 3
    MEDIA = 2
    BAJA = 1


class EstadoContenedor(Enum):
    """Estados posibles de un contenedor"""
    EN_PATIO = "En Patio"
    ASIGNADO = "Asignado a Camión"
    EN_VERIFICACION = "En Verificación"
    CARGANDO = "Cargando"
    DESPACHADO = "Despachado"
    REPROGRAMADO = "Reprogramado"


class TipoCarga(Enum):
    """Tipos de carga (opcional para extensión futura)"""
    SECA = "Carga Seca"
    REFRIGERADA = "Refrigerada"
    PELIGROSA = "Peligrosa"
    FRAGIL = "Frágil"
    NODRIZA = "Nodriza"

@dataclass
class Contenedor:
    """
    Representa un contenedor en el sistema de logística.
    
    Attributes:
        id: Identificador único del contenedor
        prioridad: Nivel de prioridad (Alta/Media/Baja)
        tiempo_llegada: Momento en que llegó al patio (en horas de simulación)
        linea_asignada: Nombre de la línea transportista originalmente asignada
        sla_horas: Service Level Agreement - tiempo máximo permitido en horas
        tipo_carga: Tipo de mercancía (opcional)
        estado: Estado actual del contenedor
        tiempo_asignacion: Momento en que fue asignado a un camión
        tiempo_salida: Momento en que salió del patio
        reprogramaciones: Contador de veces que cambió de línea
        historial_estados: Lista con cambios de estado y timestamps
    """
    id: str
    prioridad: Prioridad
    tiempo_llegada: float
    linea_asignada: str
    sla_horas: float = 72.0
    tipo_carga: TipoCarga = TipoCarga.SECA
    estado: EstadoContenedor = EstadoContenedor.EN_PATIO
    tiempo_asignacion: Optional[float] = None
    tiempo_salida: Optional[float] = None
    reprogramaciones: int = 0
    historial_estados: List[tuple] = field(default_factory=list)
    linea_original: Optional[str] = None  
    
    def __post_init__(self):
        """Inicialización adicional después de crear el objeto"""
        if self.linea_original is None:
            self.linea_original = self.linea_asignada
        self.registrar_estado(self.estado, self.tiempo_llegada)
    
    def registrar_estado(self, nuevo_estado: EstadoContenedor, tiempo: float):
        """Registra un cambio de estado con timestamp"""
        self.historial_estados.append((tiempo, nuevo_estado))
        self.estado = nuevo_estado
    
    def tiempo_en_patio(self, tiempo_actual: float) -> float:
        """Calcula el tiempo que lleva en el patio"""
        if self.tiempo_salida:
            return self.tiempo_salida - self.tiempo_llegada
        return tiempo_actual - self.tiempo_llegada
    
    def tiempo_restante_sla(self, tiempo_actual: float) -> float:
        """Calcula cuánto tiempo falta para violar el SLA"""
        tiempo_transcurrido = self.tiempo_en_patio(tiempo_actual)
        return self.sla_horas - tiempo_transcurrido
    
    def viola_sla(self, tiempo_actual: float) -> bool:
        """Verifica si el contenedor ha violado su SLA"""
        return self.tiempo_restante_sla(tiempo_actual) <= 0
    
    def calcular_penalizacion(self, tiempo_actual: float, costo_por_hora: float = 2.08) -> float:
        """
        Calcula la penalización por almacenamiento excedido.
        Default: $50/día = $2.08/hora
        """
        tiempo_excedido = max(0, self.tiempo_en_patio(tiempo_actual) - self.sla_horas)
        return tiempo_excedido * costo_por_hora
    
    def reasignar_linea(self, nueva_linea: str, tiempo: float):
        """Reasigna el contenedor a una nueva línea transportista"""
        if nueva_linea != self.linea_asignada:
            self.linea_asignada = nueva_linea
            self.reprogramaciones += 1
            self.registrar_estado(EstadoContenedor.REPROGRAMADO, tiempo)
    
    def get_urgencia(self, tiempo_actual: float) -> float:
        """
        Calcula un score de urgencia basado en:
        - Tiempo restante de SLA (menor = más urgente)
        - Prioridad del contenedor
        
        Returns: Score donde valores más altos = más urgente
        """
        tiempo_restante = self.tiempo_restante_sla(tiempo_actual)
        
        peso_prioridad = self.prioridad.value * 10
        
        if tiempo_restante <= 0:
            urgencia_temporal = 100
        else:
            urgencia_temporal = 100 / max(tiempo_restante, 1)
        
        return urgencia_temporal + peso_prioridad
    
    def __repr__(self):
        return (f"Contenedor(id={self.id}, prioridad={self.prioridad.name}, "
                f"línea={self.linea_asignada}, estado={self.estado.value})")
    
    def to_dict(self) -> dict:
        """Convierte el contenedor a diccionario para análisis"""
        return {
            'id': self.id,
            'prioridad': self.prioridad.name,
            'tiempo_llegada': self.tiempo_llegada,
            'linea_original': self.linea_original,
            'linea_final': self.linea_asignada,
            'sla_horas': self.sla_horas,
            'tipo_carga': self.tipo_carga.value,
            'estado': self.estado.value,
            'tiempo_asignacion': self.tiempo_asignacion,
            'tiempo_salida': self.tiempo_salida,
            'reprogramaciones': self.reprogramaciones,
            'tiempo_total_patio': self.tiempo_en_patio(self.tiempo_salida) if self.tiempo_salida else None
        }
