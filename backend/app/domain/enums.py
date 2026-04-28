from enum import Enum


class TipoCarga(str, Enum):
    SECA = "Carga Seca"
    REFRIGERADA = "Refrigerada"
    PELIGROSA = "Peligrosa"
    FRAGIL = "Frágil"
    NODRIZA = "Nodriza"


class EstadoContenedor(str, Enum):
    EN_PATIO = "En Patio"
    ASIGNADO = "Asignado a Camión"
    EN_VERIFICACION = "En Verificación"
    CARGANDO = "Cargando"
    DESPACHADO = "Despachado"
    REPROGRAMADO = "Reprogramado"
