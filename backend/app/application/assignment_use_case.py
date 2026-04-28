import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from app.domain.contenedor import Contenedor
from app.domain.enums import TipoCarga
from app.domain.linea_transportista import LineaTransportista

_EIR_RIESGO_CARGA: Dict[TipoCarga, float] = {
    TipoCarga.PELIGROSA: 0.15,
    TipoCarga.REFRIGERADA: 0.12,
    TipoCarga.FRAGIL: 0.10,
    TipoCarga.NODRIZA: 0.08,
    TipoCarga.SECA: 0.05,
}


@dataclass
class AssignmentResult:
    mejor: Optional[Dict]
    resultados: List[Dict]


class AssignmentUseCase:
    def ejecutar(
        self, contenedor: Contenedor, lineas: List[LineaTransportista]
    ) -> AssignmentResult:
        resultados: List[Dict] = []

        for linea in lineas:
            if not linea.disponible:
                continue

            lead_time = random.uniform(2, 8)
            espera = random.uniform(1, 5)
            reprogramaciones = int((100 - linea.porcentaje_cumplimiento) / 25)

            puntaje = (
                (linea.porcentaje_cumplimiento * 0.5)
                + (linea.porcentaje_puntualidad * 0.3)
                + ((10 - lead_time) * 2)
            )

            linea_info: Dict = {
                "línea": linea.nombre,
                "cumplimiento": linea.porcentaje_cumplimiento,
                "puntualidad": linea.porcentaje_puntualidad,
                "reprogramaciones": reprogramaciones,
                "espera_promedio": espera,
                "lead_time": lead_time,
                "puntaje": puntaje,
                "contacto": linea.contacto,
            }

            tiene_eir, prob_fallo = self._calcular_eir(contenedor, linea_info)
            linea_info["tiene_eir"] = tiene_eir
            linea_info["probabilidad_sin_eir"] = round(prob_fallo * 100, 2)
            linea_info["estado_documental"] = "EIR Completo" if tiene_eir else "SIN EIR"

            if not tiene_eir:
                linea_info["puntaje"] = puntaje * 0.6
                linea_info["observaciones"] = "Requiere completar documentación EIR"
            else:
                linea_info["observaciones"] = "Documentación completa"

            resultados.append(linea_info)

        mejor = max(resultados, key=lambda x: x["puntaje"]) if resultados else None
        return AssignmentResult(mejor=mejor, resultados=resultados)

    def _calcular_eir(self, contenedor: Contenedor, linea_info: Dict):
        riesgo_cumplimiento = (100 - linea_info["cumplimiento"]) / 100
        riesgo_puntualidad = (100 - linea_info["puntualidad"]) / 100
        riesgo_reprogramaciones = min(linea_info["reprogramaciones"] / 5, 1.0)

        lt = linea_info["lead_time"]
        if lt < 3:
            riesgo_lead_time = 0.4
        elif lt < 5:
            riesgo_lead_time = 0.2
        else:
            riesgo_lead_time = 0.05

        riesgo_puntaje = max(0, 1 - (linea_info["puntaje"] / 100))
        riesgo_tipo_carga = _EIR_RIESGO_CARGA.get(contenedor.carga_tipo, 0.05)
        riesgo_tamano = 0.08 if contenedor.tamano_pies == 40 else 0.03

        comprador = contenedor.comprador or ""
        if "S.A." in comprador:
            riesgo_comprador = 0.05
        elif "Corp" in comprador:
            riesgo_comprador = 0.03
        else:
            riesgo_comprador = 0.10

        prob = (
            riesgo_cumplimiento * 0.25
            + riesgo_puntualidad * 0.20
            + riesgo_reprogramaciones * 0.15
            + riesgo_lead_time * 0.15
            + riesgo_puntaje * 0.10
            + riesgo_tipo_carga * 0.08
            + riesgo_tamano * 0.04
            + riesgo_comprador * 0.03
        )
        prob = max(0.02, min(prob, 0.65))
        return random.random() > prob, prob
