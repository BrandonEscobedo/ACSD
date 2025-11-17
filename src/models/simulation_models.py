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